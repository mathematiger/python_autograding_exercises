"""Prüft Ihre Lösungen.

Benutzung (im Projektordner):
    python pruefe.py 1_003        → prüft aufgaben/1_003_….py
    python pruefe.py 1_001 1_003  → prüft die Aufgaben 1_001 und 1_003
    python pruefe.py 2            → prüft alle Aufgaben der Stufe 2
    python pruefe.py              → prüft alle Aufgaben, die Sie schon bearbeitet haben

Auf GitHub ruft der Workflow dasselbe Skript auf, nur mit anderen Ordnern:
    python pruefe.py --tests <ordner> --aufgaben <ordner>

Für Lehrkräfte - in den Tests steht zur Verfügung:
    AUSGABE            alles, was das Programm mit print ausgegeben hat
                       (ohne Leerzeichen am Zeilenende und Leerzeilen am Schluss)
    EINGABEN = [...]   in den Tests setzen: Eingaben für input() beim ersten Lauf
    starte(*eingaben)  startet das Programm neu mit anderen Eingaben, gibt dessen AUSGABE zurück
    verwendet("for")   True, wenn for/while/if/def/return/class oder ein Aufruf wie range(...) im Code vorkommt
    sowie alle Variablen und Funktionen aus dem Programm der SuS.
"""

from __future__ import annotations  # erlaubt `str | None` usw. auch vor Python 3.10

import argparse
import ast
import builtins
import functools
import hashlib
import io
import multiprocessing
import os
import sys
import threading
import traceback
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from multiprocessing.connection import Connection
from pathlib import Path
from typing import Any, NoReturn, TypeVar

if sys.version_info < (3, 9):  # noqa: UP036 - freundliche Meldung statt Absturz bei zu altem Python
    sys.exit("Ihr Python ist zu alt. Bitte installieren Sie Python 3.9 oder neuer von python.org.")

T = TypeVar("T")
PROJEKT = Path(__file__).resolve().parent
ZEITLIMIT_SEKUNDEN = 5.0

_SPRACHMITTEL: dict[str, type[ast.AST]] = {
    "for": ast.For,
    "while": ast.While,
    "if": ast.If,
    "def": ast.FunctionDef,
    "return": ast.Return,
    "class": ast.ClassDef,
}


class Endlosschleife(Exception):
    """Programm oder Test ist nicht innerhalb des Zeitlimits fertig geworden."""


class _KeineEingabeMehr(Exception):
    """Das Programm ruft öfter ``input()`` auf, als Eingaben vorgesehen sind."""


class ProgrammFehler(Exception):
    """Fehler beim Neustart über ``starte``; der Text ist schon für SuS formuliert."""


@dataclass(frozen=True)
class Lauf:
    """Ergebnis eines Programmlaufs.

    Attributes:
        ausgabe: Normalisierte print-Ausgabe.
        namensraum: Variablen und Funktionen des Programms (auch nach einem Fehler, bis dorthin).
        fehler: Verständliche Fehlermeldung oder ``None``.
    """

    ausgabe: str
    namensraum: dict[str, Any]
    fehler: str | None


@dataclass(frozen=True)
class Schritt:
    """Eine Anweisung aus der Testdatei.

    Attributes:
        name: Anzeigename (Kommentar darüber oder die Bedingung selbst).
        anweisung: Die Anweisung als Syntaxbaum.
        ist_test: Enthält ein ``assert`` - sonst ist es Vorbereitung (z. B. eine Zuweisung).
    """

    name: str
    anweisung: ast.stmt
    ist_test: bool


@dataclass(frozen=True)
class Testdatei:
    """Geladene Testdatei: Schritte, Eingaben für den ersten Lauf und Fingerabdruck der Vorlage."""

    schritte: list[Schritt]
    eingaben: list[str]
    vorlage_hash: str | None


@dataclass(frozen=True)
class TestErgebnis:
    """Ergebnis eines Tests; ``meldung`` ist ``None``, wenn er bestanden ist."""

    name: str
    meldung: str | None


@dataclass
class Auswertung:
    """Gesamtergebnis einer Aufgabe."""

    programmfehler: str | None = None
    tests: list[TestErgebnis] = field(default_factory=list)
    abgebrochen: bool = False

    @property
    def bestanden(self) -> bool:
        """Alles grün: kein Programmfehler, kein Abbruch, mindestens ein Test, alle bestanden.

        Testen: leere Testliste → ``False``; ein ✗ → ``False``; Programmfehler trotz grüner Tests → ``False``.
        """
        return (
            self.programmfehler is None
            and not self.abgebrochen
            and bool(self.tests)
            and all(t.meldung is None for t in self.tests)
        )


# --- Hilfsfunktionen: Text, Zeitlimit, Fehlermeldungen ---


def normalisiere(text: str) -> str:
    """Vereinheitlicht Zeilenenden, entfernt Leerzeichen am Zeilenende und Leerzeilen am Schluss.

    Testen: ``"a  \\r\\nb\\n\\n"`` → ``"a\\nb"``; ``""`` → ``""``; führende Leerzeilen bleiben.
    """
    return "\n".join(zeile.rstrip() for zeile in text.splitlines()).rstrip("\n")


def vorlage_hash(text: str) -> str:
    """Fingerabdruck einer Vorlage, unabhängig von Zeilenenden (Windows-Downloads!).

    Testen: gleicher Text mit ``\\r\\n`` und ``\\n`` → gleicher Hash; eine Änderung → anderer Hash.
    """
    return hashlib.sha256(normalisiere(text).encode()).hexdigest()[:16]


def _mit_zeitlimit(aufgabe: Callable[[], T]) -> T:
    """Führt ``aufgabe`` in einem Hintergrund-Thread mit Zeitlimit aus.

    Thread statt ``signal.alarm``, damit es auch unter Windows läuft. Bei
    Zeitüberschreitung läuft der Thread im Hintergrund weiter; der Aufrufer
    bricht die Aufgabe ab.

    Testen: Rückgabewert kommt durch; Exception aus ``aufgabe`` wird weitergereicht;
    ``while True: pass`` → ``Endlosschleife``.
    """
    ergebnis: list[T] = []
    fehler: list[BaseException] = []

    def ziel() -> None:
        """Führt ``aufgabe`` im Faden aus und merkt sich Ergebnis oder Fehler."""
        try:
            ergebnis.append(aufgabe())
        except BaseException as e:  # noqa: BLE001 - Code der SuS kann alles werfen
            fehler.append(e)

    faden = threading.Thread(target=ziel, daemon=True)
    faden.start()
    faden.join(ZEITLIMIT_SEKUNDEN)
    if fehler:
        raise fehler[0]
    if not ergebnis:
        raise Endlosschleife
    return ergebnis[0]


def fehlertext(fehler: BaseException, skript: Path) -> str:
    """Formuliert einen Fehler verständlich, mit Zeilennummer in der Datei der SuS.

    Testen: ``SyntaxError`` → "Syntaxfehler in Zeile n"; ``NameError`` → Hinweis auf
    fehlende Variable mit deren Namen; Fehler in Zeile 3 der SuS-Datei → "Zeile 3:";
    Fehler nur in der Testdatei → ohne Zeilenangabe; zu viele ``input()`` → eigener Hinweis.
    """
    if isinstance(fehler, ProgrammFehler):
        return str(fehler)
    if isinstance(fehler, _KeineEingabeMehr):
        return "Ihr Programm fragt öfter nach einer Eingabe (input), als die Tests vorsehen."
    if isinstance(fehler, SyntaxError):
        return f"Syntaxfehler in Zeile {fehler.lineno}: {fehler.msg}"
    if isinstance(fehler, NameError):
        # fehler.name gibt es erst ab Python 3.10; vorher steht der Name nur im Text: name 'x' is not defined
        name = getattr(fehler, "name", None) or str(fehler).partition("'")[2].partition("'")[0]
        text = f"`{name}` gibt es nicht - Tippfehler, oder fehlt die Variable/Funktion noch?"
    else:
        text = f"{type(fehler).__name__}: {fehler}"
    zeilen = [f.lineno for f in traceback.extract_tb(fehler.__traceback__) if f.filename == str(skript)]
    return f"Zeile {zeilen[-1]}: {text}" if zeilen else text


# --- Programm der SuS ausführen ---


def _starte_programm(skript: Path, quelltext: str, eingaben: Sequence[str]) -> Lauf:
    """Führt das Programm der SuS mit umgeleitetem ``print`` und vorgegebenen Eingaben aus.

    ``print``/``input`` werden nur im Namensraum des Programms ersetzt, nicht global.
    Der Text in ``input("...")`` zählt nicht zur Ausgabe.

    Testen: Ausgabe landet in ``ausgabe``; Eingaben kommen in Reihenfolge an;
    Variablen vor einem Fehler bleiben im Namensraum; ``if __name__ == "__main__"`` läuft.
    """
    puffer = io.StringIO()
    rest = list(eingaben)

    def eigenes_print(*werte: object, sep: str | None = " ", end: str | None = "\n", **_: object) -> None:
        """Wie ``print``, schreibt aber in den Puffer statt auf den Bildschirm."""
        builtins.print(*werte, sep=sep, end=end, file=puffer)

    def eigenes_input(_prompt: object = "") -> str:
        """Wie ``input``, liefert aber die nächste vorgegebene Eingabe."""
        if not rest:
            raise _KeineEingabeMehr
        return rest.pop(0)

    namensraum: dict[str, Any] = {
        "__name__": "__main__",
        "__file__": str(skript),
        "print": eigenes_print,
        "input": eigenes_input,
    }
    fehler: str | None = None
    try:
        exec(compile(quelltext, str(skript), "exec"), namensraum)  # noqa: S102 - genau dafür ist pruefe.py da
    except BaseException as e:  # noqa: BLE001 - Code der SuS kann alles werfen
        fehler = fehlertext(e, skript)
    return Lauf(normalisiere(puffer.getvalue()), namensraum, fehler)


def verwendet(quelltext: str, was: str) -> bool:
    """Prüft am Syntaxbaum, ob ``was`` im Code vorkommt (Kommentare und Strings zählen nicht).

    ``was`` ist ein Schlüsselwort aus ``_SPRACHMITTEL`` oder der Name einer aufgerufenen Funktion.

    Testen: ``for`` im Code → ``True``; ``for`` nur im Kommentar/Docstring → ``False``;
    ``"range"`` erkennt ``range(5)``; Syntaxfehler → ``False``.
    """
    try:
        baum = ast.parse(quelltext)
    except SyntaxError:
        return False
    knotentyp = _SPRACHMITTEL.get(was)
    for knoten in ast.walk(baum):
        if knotentyp is not None and isinstance(knoten, knotentyp):
            return True
        if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Name) and knoten.func.id == was:
            return True
    return False


# --- Testdateien lesen ---


def lies_vorlage_hash(testdatei: Path) -> str | None:
    """Liest den Fingerabdruck der Vorlage aus dem Kopf der Testdatei (``# vorlage-hash: …``)."""
    for zeile in testdatei.read_text(encoding="utf-8").splitlines():
        if zeile.startswith("# vorlage-hash:"):
            return zeile.split(":", 1)[1].strip()
    return None


def entspricht_vorlage(skript: Path, testdatei: Path) -> bool:
    """Prüft, ob ``skript`` genau die Vorlage ist, aus der ``testdatei`` erzeugt wurde.

    Testen: frisch erzeugte Vorlage → ``True``; nur Zeilenenden geändert → ``True``; ein Zeichen geändert → ``False``.
    """
    return vorlage_hash(skript.read_text(encoding="utf-8-sig")) == lies_vorlage_hash(testdatei)


def lade_tests(testdatei: Path) -> Testdatei:
    """Zerlegt die Testdatei in Schritte und liest ``EINGABEN``.

    Name eines Tests: Kommentar in der Zeile direkt über dem Test oder über der
    Vorbereitung davor; sonst die Bedingung des ``assert``.

    Testen: Kommentar über ``assert`` wird Name; Kommentar über Vorbereitung gilt
    für das folgende ``assert``; ohne Kommentar → Bedingung als Name;
    ``EINGABEN = ["a"]`` → ``eingaben == ["a"]``; Kopfkommentar mit Leerzeile wird kein Name.
    """
    text = testdatei.read_text(encoding="utf-8")
    zeilen = text.splitlines()
    schritte: list[Schritt] = []
    eingaben: list[str] = []
    offener_name = ""
    for anweisung in ast.parse(text, filename=str(testdatei)).body:
        offener_name = _kommentar_darueber(zeilen, anweisung) or offener_name
        neue_eingaben = _eingaben_aus(anweisung)
        if neue_eingaben is not None:
            eingaben = neue_eingaben
        ist_test = any(isinstance(k, ast.Assert) for k in ast.walk(anweisung))
        schritte.append(Schritt(offener_name or _standardname(text, anweisung), anweisung, ist_test))
        if ist_test:
            offener_name = ""
    return Testdatei(schritte, eingaben, lies_vorlage_hash(testdatei))


def _kommentar_darueber(zeilen: list[str], anweisung: ast.stmt) -> str:
    """Liefert den Kommentar in der Zeile direkt über der Anweisung ohne ``#``, sonst ``""``."""
    if anweisung.lineno < 2:
        return ""
    darueber = zeilen[anweisung.lineno - 2].strip()
    return darueber.lstrip("#").strip() if darueber.startswith("#") else ""


def _eingaben_aus(anweisung: ast.stmt) -> list[str] | None:
    """Liest die Liste aus ``EINGABEN = [...]``; ``None``, wenn die Anweisung etwas anderes ist."""
    if not isinstance(anweisung, ast.Assign):
        return None
    if not any(isinstance(ziel, ast.Name) and ziel.id == "EINGABEN" for ziel in anweisung.targets):
        return None
    return [str(eingabe) for eingabe in ast.literal_eval(anweisung.value)]


def _standardname(text: str, anweisung: ast.stmt) -> str:
    """Name eines Schritts ohne Kommentar: die Bedingung des ``assert``, sonst die erste Zeile, höchstens 70 Zeichen."""
    if isinstance(anweisung, ast.Assert):
        return ast.unparse(anweisung.test)[:70]
    return (ast.get_source_segment(text, anweisung) or "").splitlines()[0][:70]


# --- Lösung prüfen ---


def pruefe_loesung(skript: Path, testdatei: Path) -> Auswertung:
    """Prüft eine Lösung in einem eigenen Prozess, der danach immer beendet wird.

    Ohne eigenen Prozess würde ein abgebrochenes Programm (Endlosschleife) im Hintergrund
    weiterrechnen und immer mehr Speicher belegen, während die nächste Aufgabe geprüft wird.
    Außerdem stoppt das Gesamtlimit auch Rechnungen wie ``10 ** 10 ** 9``, die das Zeitlimit
    per Thread nicht unterbrechen kann.

    Testen: Ergebnis wie bei ``_pruefe_direkt``; danach läuft kein Kindprozess mehr;
    ``os._exit`` im Programm → Hinweis statt Absturz; riesige Rechnung → Abbruch nach dem Gesamtlimit.
    """
    # Höchstens ein Zeitlimit wird pro Lösung ausgeschöpft (danach Abbruch), der Rest ist Puffer
    # für den Start des Prozesses (auf Schulrechnern langsam) und die übrigen Tests.
    gesamtlimit = 3 * ZEITLIMIT_SEKUNDEN
    kontext = multiprocessing.get_context("spawn")  # Standard unter Windows und macOS, so läuft es überall gleich
    empfaenger, sender = kontext.Pipe(duplex=False)
    prozess = kontext.Process(target=_pruefe_im_prozess, args=(skript, testdatei, ZEITLIMIT_SEKUNDEN, sender))
    prozess.start()
    sender.close()  # nur der Kindprozess schreibt; so merkt recv(), wenn er ohne Ergebnis endet
    try:
        if not empfaenger.poll(gesamtlimit):
            return Auswertung(
                programmfehler=f"Die Prüfung ist nach {gesamtlimit:g} Sekunden nicht fertig geworden - "
                "vielleicht eine Endlosschleife oder eine riesige Rechnung?",
                abgebrochen=True,
            )
        ergebnis: Auswertung = empfaenger.recv()
        return ergebnis
    except EOFError:
        return Auswertung(
            programmfehler="Die Prüfung ist abgestürzt - braucht Ihr Programm zu viel Speicher "
            "oder beendet es Python mit os._exit?",
            abgebrochen=True,
        )
    finally:
        prozess.kill()  # auch wenn er schon fertig ist: hängende Threads darin sollen nicht weiterlaufen
        prozess.join()
        empfaenger.close()


def _pruefe_im_prozess(skript: Path, testdatei: Path, zeitlimit: float, sender: Connection) -> None:
    """Läuft im eigenen Prozess: prüft die Lösung und schickt die Auswertung zurück."""
    global ZEITLIMIT_SEKUNDEN  # der neue Prozess lädt pruefe.py frisch; einen geänderten Wert übernehmen
    ZEITLIMIT_SEKUNDEN = zeitlimit
    sender.send(_pruefe_direkt(skript, testdatei))


def _pruefe_direkt(skript: Path, testdatei: Path) -> Auswertung:
    """Führt das Programm einmal aus und danach die Tests Schritt für Schritt in dessen Namensraum.

    Testen: korrekte Lösung → ``bestanden``; ein falsches ``assert`` → dessen Meldung;
    ``assert`` ohne Meldung → "Bedingung nicht erfüllt."; Endlosschleife im Programm →
    ``abgebrochen`` mit Hinweis; ``starte`` mit anderen Eingaben liefert neue Ausgabe;
    fehlschlagende Vorbereitung → genau ein ✗, nicht zwei.
    """
    tests = lade_tests(testdatei)
    quelltext = skript.read_text(encoding="utf-8-sig")
    try:
        lauf = _mit_zeitlimit(lambda: _starte_programm(skript, quelltext, tests.eingaben))
    except Endlosschleife:
        return Auswertung(
            programmfehler=f"Ihr Programm ist nach {ZEITLIMIT_SEKUNDEN:g} Sekunden nicht fertig geworden - "
            "vielleicht eine Endlosschleife?",
            abgebrochen=True,
        )
    namensraum = _test_namensraum(lauf, skript, quelltext)
    ergebnisse, abgebrochen = _fuehre_tests_aus(tests.schritte, namensraum, skript, testdatei)
    return Auswertung(programmfehler=lauf.fehler, tests=ergebnisse, abgebrochen=abgebrochen)


def _test_namensraum(lauf: Lauf, skript: Path, quelltext: str) -> dict[str, Any]:
    """Ergänzt den Namensraum des Programms um ``AUSGABE``, ``starte`` und ``verwendet`` für die Tests."""

    def starte(*eingaben: str) -> str:
        """Startet das Programm erneut mit anderen Eingaben und liefert dessen Ausgabe."""
        neu = _starte_programm(skript, quelltext, eingaben)
        if neu.fehler:
            raise ProgrammFehler(f"Mit den Eingaben {list(eingaben)}: {neu.fehler}")
        return neu.ausgabe

    namensraum = lauf.namensraum
    namensraum.update(AUSGABE=lauf.ausgabe, starte=starte, verwendet=functools.partial(verwendet, quelltext))
    return namensraum


def _fuehre_tests_aus(
    schritte: list[Schritt], namensraum: dict[str, Any], skript: Path, testdatei: Path
) -> tuple[list[TestErgebnis], bool]:
    """Führt die Schritte nacheinander aus; liefert die Ergebnisse und ob nach einem Zeitlimit abgebrochen wurde.

    Schlägt eine Vorbereitung fehl, wird sie als ✗ gemeldet und der zugehörige Test übersprungen.
    """
    ergebnisse: list[TestErgebnis] = []
    ueberspringen = False
    for schritt in schritte:
        if ueberspringen:
            ueberspringen = not schritt.ist_test
            continue
        try:
            meldung = _fuehre_schritt_aus(schritt, namensraum, skript, testdatei)
        except Endlosschleife:
            ergebnisse.append(TestErgebnis(schritt.name, "Zeitlimit überschritten - vielleicht eine Endlosschleife?"))
            return ergebnisse, True
        if schritt.ist_test or meldung is not None:
            ergebnisse.append(TestErgebnis(schritt.name, meldung))
        ueberspringen = meldung is not None and not schritt.ist_test
    return ergebnisse, False


def _fuehre_schritt_aus(schritt: Schritt, namensraum: dict[str, Any], skript: Path, testdatei: Path) -> str | None:
    """Führt einen Schritt mit Zeitlimit aus; liefert die Fehlermeldung oder ``None``, wenn alles klappt."""
    code = compile(ast.Module(body=[schritt.anweisung], type_ignores=[]), str(testdatei), "exec")
    try:
        _mit_zeitlimit(functools.partial(exec, code, namensraum))
    except Endlosschleife:
        raise  # sonst finge der allgemeine Fall unten auch das Zeitlimit ab
    except AssertionError as fehler:
        return str(fehler) or "Bedingung nicht erfüllt."
    except Exception as fehler:  # noqa: BLE001 - Code der SuS kann alles werfen
        return fehlertext(fehler, skript)
    return None


# --- Bericht ---


def _ueberschrift(name: str) -> str:
    """Erste Zeile im Bericht zu einer Aufgabe."""
    return f"── {name} ──"


def formatiere(name: str, auswertung: Auswertung) -> str:
    """Baut den Bericht für eine Aufgabe als Text.

    Testen: alles grün → "Alle Tests bestanden (n)"; Meldungen werden eingerückt;
    Programmfehler steht oben mit ⚠; Abbruch → "Prüfung abgebrochen".
    """
    zeilen = [_ueberschrift(name)]
    if auswertung.programmfehler:
        zeilen.append(f"⚠ Fehler in Ihrem Programm: {auswertung.programmfehler}")
    for test in auswertung.tests:
        zeilen.append(f"{'✓' if test.meldung is None else '✗'} {test.name}")
        if test.meldung is not None:
            zeilen.extend("    " + z for z in test.meldung.splitlines())
    anzahl = sum(t.meldung is None for t in auswertung.tests)
    if auswertung.bestanden:
        zeilen.append(f"→ Alle Tests bestanden ({anzahl}). Super!")
    elif auswertung.abgebrochen:
        zeilen.append("→ Prüfung abgebrochen.")
    else:
        zeilen.append(f"→ {anzahl} von {len(auswertung.tests)} Tests bestanden.")
    return "\n".join(zeilen)


def _schreibe_github_zusammenfassung(berichte: list[str]) -> None:
    """Hängt die Berichte an die Zusammenfassung des GitHub-Laufs an (nur in GitHub Actions)."""
    pfad = os.environ.get("GITHUB_STEP_SUMMARY")
    if pfad and berichte:
        with open(pfad, "a", encoding="utf-8") as datei:
            datei.write("## Ergebnis\n\n```\n" + "\n\n".join(berichte) + "\n```\n")


# --- Aufruf von der Kommandozeile ---


class _DeutscherParser(argparse.ArgumentParser):
    """argparse mit deutschen Texten: Hilfe ist der Kopf dieser Datei, Fehler ein Aufrufbeispiel."""

    def format_help(self) -> str:
        """Liefert den Kopf dieser Datei als Hilfetext."""
        return __doc__ or ""

    def error(self, message: str) -> NoReturn:
        """Beendet mit Aufrufbeispiel statt der englischen argparse-Meldung."""
        self.exit(
            2,
            "Aufruf nicht verstanden. So geht es:\n"
            "    python pruefe.py 1_003        → prüft Aufgabe 1_003\n"
            "    python pruefe.py 1_001 1_003  → prüft die Aufgaben 1_001 und 1_003\n"
            "    python pruefe.py 2            → prüft alle Aufgaben der Stufe 2\n"
            "    python pruefe.py              → prüft alle Aufgaben, die Sie schon bearbeitet haben\n",
        )


def _lies_argumente(argumente: list[str]) -> argparse.Namespace:
    """Wertet die Kommandozeile aus: Kennungen sowie die Ordner für Aufgaben und Tests."""
    parser = _DeutscherParser()
    parser.add_argument("kennungen", nargs="*")  # Anfänge der Aufgabennamen, z. B. 1_001 2
    parser.add_argument("--aufgaben", type=Path, default=PROJEKT / "aufgaben")  # Ordner mit den Lösungen
    parser.add_argument("--tests", type=Path, default=PROJEKT / "tests")  # Ordner mit den Tests
    return parser.parse_args(argumente)


def _passende_tests(alle: list[Path], kennung: str) -> list[Path]:
    """Liefert die Tests, deren Name mit der Kennung beginnt; ein genau gleicher Name gewinnt.

    Ohne diesen Vorrang ließe sich „1_001_hallo“ nicht allein prüfen, wenn es auch „1_001_hallowelt“ gibt.
    """
    for testdatei in alle:
        if testdatei.stem == kennung:
            return [testdatei]
    return [t for t in alle if t.stem.startswith(kennung)]


def _unbekannte_kennung(alle: list[Path], kennungen: list[str]) -> str | None:
    """Liefert die erste Kennung, zu der es keine Aufgabe gibt, sonst ``None``."""
    for kennung in kennungen:
        if not _passende_tests(alle, kennung):
            return kennung
    return None


def _waehle_nach_kennungen(alle: list[Path], kennungen: list[str]) -> list[Path]:
    """Liefert die Tests zu allen Kennungen in deren Reihenfolge, jeden nur einmal."""
    auswahl: list[Path] = []
    for kennung in kennungen:
        for testdatei in _passende_tests(alle, kennung):
            if testdatei not in auswahl:  # bei „1_001 1_001_hallo“ nur einmal prüfen
                auswahl.append(testdatei)
    return auswahl


def _bearbeitete_aufgaben(alle: list[Path], aufgaben_ordner: Path) -> list[Path]:
    """Liefert die Tests der Aufgaben, deren Datei vorhanden ist und sich von der Vorlage unterscheidet."""
    auswahl: list[Path] = []
    for testdatei in alle:
        skript = aufgaben_ordner / testdatei.name
        if skript.exists() and not entspricht_vorlage(skript, testdatei):
            auswahl.append(testdatei)
    return auswahl


def _pruefe_aufgabe(aufgaben_ordner: Path, testdatei: Path) -> tuple[str, bool]:
    """Prüft die Lösung zu einer Testdatei; liefert den Bericht und ob alles bestanden ist."""
    skript = aufgaben_ordner / testdatei.name
    if not skript.exists():
        fehlt = f"✗ Die Datei {testdatei.name} fehlt im Ordner „{aufgaben_ordner.name}“."
        return f"{_ueberschrift(testdatei.stem)}\n{fehlt}", False
    auswertung = pruefe_loesung(skript, testdatei)
    return formatiere(testdatei.stem, auswertung), auswertung.bestanden


def main(argumente: list[str]) -> int:
    """Einstiegspunkt.

    Mit Kennungen: alle Aufgaben, deren Name mit einer davon beginnt. Ohne: alle Aufgaben,
    deren Datei sich von der Vorlage unterscheidet. Exit-Code 1, wenn etwas nicht bestanden
    ist (GitHub zeigt dann ✗).

    Testen: Kennung passt auf eine oder mehrere Aufgaben → alle diese; genau gleicher Name → nur dieser;
    unbekannte Kennung → Liste, Exit 2; ohne Kennung und nichts bearbeitet → Hinweis, Exit 0;
    unveränderte Vorlagen werden übersprungen.
    """
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(errors="replace")  # ✓/✗ auch in Konsolen ohne UTF-8
    args = _lies_argumente(argumente)
    alle = sorted(args.tests.glob("*.py"))

    if args.kennungen:
        unbekannt = _unbekannte_kennung(alle, args.kennungen)
        if unbekannt is not None:
            print(f"Keine Aufgabe zu „{unbekannt}“. Vorhanden sind:")
            print("\n".join(f"  {t.stem}" for t in alle))
            return 2
        auswahl = _waehle_nach_kennungen(alle, args.kennungen)
    else:
        auswahl = _bearbeitete_aufgaben(alle, args.aufgaben)
        if not auswahl:
            print("Noch keine bearbeitete Aufgabe gefunden. Bearbeiten Sie eine Datei im Ordner „aufgaben“.")
            return 0

    berichte: list[str] = []
    alles_bestanden = True
    for testdatei in auswahl:
        bericht, bestanden = _pruefe_aufgabe(args.aufgaben, testdatei)
        print(bericht + "\n")
        berichte.append(bericht)
        alles_bestanden = alles_bestanden and bestanden
    _schreibe_github_zusammenfassung(berichte)
    return 0 if alles_bestanden else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
