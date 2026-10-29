# SPDX-License-Identifier: MIT
"""Prüft Ihre Lösungen.

Benutzung (im Projektordner):
    python pruefe.py 1_003        → prüft aufgaben/1_003_….py
    python pruefe.py 1_001 1_003  → prüft die Aufgaben 1_001 und 1_003
    python pruefe.py 2            → prüft alle Aufgaben der Stufe 2
    python pruefe.py funktionen   → prüft alle Aufgaben zum Thema Funktionen
    python pruefe.py 2 funktionen → prüft die Aufgaben der Stufe 2 zum Thema Funktionen
    python pruefe.py              → prüft alle Aufgaben, die Sie schon bearbeitet haben
    python pruefe.py --liste      → zeigt alle Aufgaben nach Thema mit Ihrem Stand
    python pruefe.py --liste 2    → dasselbe nur für Stufe 2 (geht auch mit Themen)

Mehrere Namensanfänge oder mehrere Themen ergänzen sich; Namensanfänge und Themen
zusammen wählen nur die Aufgaben, die zu beidem passen. Die Themen stehen ganz unten.

Auf GitHub ruft der Workflow dasselbe Skript auf, nur mit anderen Ordnern:
    python pruefe.py --tests <ordner> --aufgaben <ordner>

Für Lehrkräfte - in den Tests steht zur Verfügung:
    AUSGABE            alles, was das Programm mit print ausgegeben hat
                       (ohne Leerzeichen am Zeilenende und Leerzeilen am Schluss)
    EINGABEN = [...]   in den Tests setzen: Eingaben für input() beim ersten Lauf
    starte(*eingaben)  startet das Programm neu mit anderen Eingaben, gibt dessen AUSGABE zurück
    verwendet("for")   True, wenn for/while/if/def/return/class oder ein Aufruf wie range(...) im Code vorkommt
    Zaehlliste(werte)  wie eine Liste, zählt aber lesezugriffe und schreibzugriffe über den Index
    zaehle_schritte(f, *argumente)
                       ruft f(*argumente) auf, gibt (ergebnis, ausgeführte Zeilen im Programm) zurück
    Zufall(42)         eigener Zufallsgenerator (random.Random) für Zufallstests, ohne import
    sowie alle Variablen und Funktionen aus dem Programm der SuS.
"""

import argparse
import ast
import builtins
import contextlib
import functools
import hashlib
import importlib
import io
import multiprocessing
import os
import random
import sys
import threading
import traceback
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from multiprocessing.connection import Connection
from pathlib import Path
from types import FrameType
from typing import Any, NoReturn, TypeVar

if sys.version_info < (3, 11):  # noqa: UP036 - freundliche Meldung statt Absturz bei zu altem Python
    sys.exit("Ihr Python ist zu alt. Bitte installieren Sie Python 3.11 oder neuer von python.org.")

T = TypeVar("T")
PROJEKT = Path(__file__).resolve().parent
ZEITLIMIT_SEKUNDEN = 5.0
# Bibliotheken aus requirements.txt, die Aufgaben importieren dürfen. .github/pruefe_einreichung.py
# lässt in eingereichten Aufgaben nur Importe dieser Bibliotheken durch.
BIBLIOTHEKEN = ("duckdb", "numpy", "pandas", "polars")
# Die Musterlösungen dieser Stufen bleiben privat: erstelle_aufgaben.py schreibt sie nicht nach loesungen/,
# .github/pruefe_einreichung.py lässt sie in Pull Requests nicht zu.
PRIVATE_STUFEN = ("4", "5")
# Jede Aufgabe hat genau ein Thema: das Sprachmittel, das sie neu einführt. Schlüssel = was man bei
# pruefe.py angibt; die Reihenfolge gilt auch für die README. Steht hier, weil pruefe.py eigenständig
# bleiben muss und erstelle_aufgaben.py und .github/pruefe_einreichung.py die Liste von hier importieren.
THEMEN: dict[str, str] = {
    "texte_zahlen": "Texte, Zahlen & Dateien",
    "kontrollfluss": "Bedingungen & Schleifen",
    "funktionen": "Funktionen",
    "algorithmen": "Algorithmen & Rekursion",
    "datenstrukturen": "Datenstrukturen",
    "fehler": "Fehler & Testen",
    "klassen": "Klassen & Objekte",
    "programmaufbau": "Programmaufbau",
    "nebenlaeufigkeit": "Nebenläufigkeit",
    "datenanalyse": "Datenanalyse",
}

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
    """Fingerabdruck des Codes einer Vorlage, unabhängig von Zeilenenden (Windows-Downloads!) und vom Aufgabentext.

    Der Aufgabentext zählt nicht mit, damit ein überarbeiteter Text (z. B. der Hintergrund) unveränderte
    Vorlagen nicht plötzlich als bearbeitet erscheinen lässt.
    Testen: gleicher Text mit ``\\r\\n`` und ``\\n`` → gleicher Hash; anderer Docstring → gleicher Hash;
    eine Änderung im Code → anderer Hash.
    """
    return _fingerabdruck(ohne_aufgabentext(text))


def text_hash(text: str) -> str:
    """Fingerabdruck des Aufgabentexts einer Vorlage, unabhängig von Zeilenenden.

    Gegenstück zu ``vorlage_hash``: Daran erkennt ``pruefe.py``, dass eine Aufgabe überarbeitet wurde,
    nachdem die Datei kopiert wurde.
    Testen: anderer Code → gleicher Hash; anderer Docstring → anderer Hash.
    """
    return _fingerabdruck("\n".join(text.splitlines()[: _ende_aufgabentext(text)]))


def ohne_aufgabentext(text: str) -> str:
    """Entfernt den Docstring am Anfang eines Programms; ohne Docstring oder bei Syntaxfehler bleibt der Text, wie er ist."""
    return "\n".join(text.splitlines()[_ende_aufgabentext(text) :])


def _ende_aufgabentext(text: str) -> int:
    """Liefert die letzte Zeile des Docstrings am Anfang eines Programms; 0 ohne Docstring oder bei Syntaxfehler."""
    try:
        baum = ast.parse(text)
    except (SyntaxError, ValueError):  # ValueError: Nullbytes unter Python 3.11
        return 0
    if ast.get_docstring(baum, clean=False) is None:
        return 0
    return baum.body[0].end_lineno or 0


def _fingerabdruck(text: str) -> str:
    """Kurzer SHA-256-Fingerabdruck des normalisierten Texts."""
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
    Fehler nur in der Testdatei → ohne Zeilenangabe; zu viele ``input()`` → eigener Hinweis;
    fehlendes ``pandas`` → Hinweis auf ``requirements.txt``.
    """
    if isinstance(fehler, ProgrammFehler):
        return str(fehler)
    if isinstance(fehler, ModuleNotFoundError) and fehler.name in BIBLIOTHEKEN:
        return (
            f"Die Bibliothek `{fehler.name}` fehlt. Installieren Sie sie einmalig im Projektordner mit: "
            "python -m pip install -r requirements.txt"
        )
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


# --- Hilfen für Laufzeittests: zählen statt Zeit messen, damit langsame Rechner nicht durchfallen ---


class Zaehlliste:
    """Verhält sich beim Lesen und Schreiben über den Index wie eine Liste und zählt dabei mit.

    Absichtlich keine Unterklasse von ``list``: Deren Methoden wie ``in`` oder ``index`` liefen in C
    an ``__getitem__`` vorbei und würden nicht mitgezählt. So läuft auch ``for x in liste`` über ``__getitem__``.

    Testen: ``z[3]`` → 1 Lesezugriff; ``z[1:4]`` → 3; ``for x in z`` und ``x in z`` → je Element einer;
    ``z[0] = 5`` → 1 Schreibzugriff; ``len(z)`` zählt nicht.
    """

    def __init__(self, werte: Iterable[Any]) -> None:
        """Übernimmt die Werte und setzt beide Zähler auf 0."""
        self.werte = list(werte)
        self.lesezugriffe = 0
        self.schreibzugriffe = 0

    def __len__(self) -> int:
        """Anzahl der Werte; zählt nicht als Zugriff."""
        return len(self.werte)

    def __getitem__(self, index: int | slice) -> Any:
        """Liefert den Wert (bei einem Slice eine Liste) und zählt jeden gelesenen Wert."""
        ergebnis = self.werte[index]
        self.lesezugriffe += len(ergebnis) if isinstance(index, slice) else 1
        return ergebnis

    def __setitem__(self, index: int, wert: Any) -> None:
        """Ersetzt den Wert an ``index`` und zählt den Schreibzugriff."""
        self.werte[index] = wert
        self.schreibzugriffe += 1

    def __repr__(self) -> str:
        """Zeigt die Werte, damit Fehlermeldungen lesbar bleiben."""
        return f"Zaehlliste({self.werte!r})"


def zaehle_schritte(skript: Path, funktion: Callable[..., T], *argumente: Any) -> tuple[T, int]:
    """Ruft ``funktion(*argumente)`` auf und zählt die dabei ausgeführten Zeilen der Datei ``skript``.

    Zeilen in der Testdatei, in Bibliotheken und in Builtins zählen nicht: ``x in liste`` ist ein
    Schritt, egal wie lang die Liste ist. Dafür gibt es ``Zaehlliste``.

    Testen: Schleife über ``range(n)`` → wächst linear mit n; Funktion außerhalb von ``skript`` → 0 Schritte;
    der vorher gesetzte Trace (z. B. von coverage) ist danach wieder aktiv.
    """
    datei = str(skript)
    schritte = 0

    # Rückgabe Any: Der Typ einer Trace-Funktion verweist auf sich selbst, das lässt sich hier nicht hinschreiben.
    def verfolge(rahmen: FrameType, ereignis: str, _wert: object) -> Any:
        """Zählt Zeilen in ``skript``; für Aufrufe in anderen Dateien schaltet es das Verfolgen ab."""
        nonlocal schritte
        if rahmen.f_code.co_filename != datei:
            return None
        if ereignis == "line":
            schritte += 1
        return verfolge

    vorher = sys.gettrace()
    sys.settrace(verfolge)
    try:
        ergebnis = funktion(*argumente)
    finally:
        sys.settrace(vorher)
    return ergebnis, schritte


# --- Testdateien lesen ---


def lies_vorlage_hash(testdatei: Path) -> str | None:
    """Liest den Fingerabdruck der Vorlage aus dem Kopf der Testdatei (``# vorlage-hash: …``)."""
    return _lies_kopfzeile(testdatei, "vorlage-hash")


def lies_text_hash(testdatei: Path) -> str | None:
    """Liest den Fingerabdruck des Aufgabentexts aus dem Kopf der Testdatei (``# text-hash: …``)."""
    return _lies_kopfzeile(testdatei, "text-hash")


def lies_thema(testdatei: Path) -> str | None:
    """Liest das Thema der Aufgabe aus dem Kopf der Testdatei (``# thema: …``).

    Testen: ``# thema: funktionen`` → ``"funktionen"``; ohne die Zeile → ``None``.
    """
    return _lies_kopfzeile(testdatei, "thema")


def lies_inhalt(testdatei: Path) -> str | None:
    """Liest die Kurzbeschreibung der Aufgabe aus dem Kopf der Testdatei (``# inhalt: …``).

    Testen: ``# inhalt: Schleife mit break`` → ``"Schleife mit break"``; ohne die Zeile → ``None``.
    """
    return _lies_kopfzeile(testdatei, "inhalt")


def _lies_kopfzeile(testdatei: Path, schluessel: str) -> str | None:
    """Liest den Wert der Zeile ``# <schluessel>: …`` aus der Testdatei; ``None``, wenn es sie nicht gibt."""
    for zeile in testdatei.read_text(encoding="utf-8").splitlines():
        if zeile.startswith(f"# {schluessel}:"):
            return zeile.split(":", 1)[1].strip()
    return None


def nach_thema(testdateien: list[Path]) -> dict[str, list[Path]]:
    """Ordnet die Testdateien ihren Themen zu, in der Reihenfolge von ``THEMEN``; Themen ohne Aufgabe fehlen.

    Testen: Reihenfolge wie ``THEMEN``, nicht wie die Dateien; Testdatei ohne oder mit unbekanntem Thema → fehlt.
    """
    gruppen: dict[str, list[Path]] = {thema: [] for thema in THEMEN}
    for testdatei in testdateien:
        thema = lies_thema(testdatei)
        if thema is not None and thema in gruppen:
            gruppen[thema].append(testdatei)
    return {thema: dateien for thema, dateien in gruppen.items() if dateien}


def entspricht_vorlage(skript: Path, testdatei: Path) -> bool:
    """Prüft, ob ``skript`` genau die Vorlage ist, aus der ``testdatei`` erzeugt wurde.

    Testen: frisch erzeugte Vorlage → ``True``; nur Zeilenenden geändert → ``True``; ein Zeichen geändert → ``False``.
    """
    return vorlage_hash(skript.read_text(encoding="utf-8-sig")) == lies_vorlage_hash(testdatei)


def aufgabentext_veraltet(skript: Path, testdatei: Path) -> bool:
    """Prüft, ob der Aufgabentext in ``skript`` ein anderer ist als der, aus dem ``testdatei`` erzeugt wurde.

    Testen: nur der Code geändert → ``False``; Text geändert → ``True``; Testdatei ohne ``# text-hash:`` → ``False``.
    """
    erwartet = lies_text_hash(testdatei)
    return erwartet is not None and text_hash(skript.read_text(encoding="utf-8-sig")) != erwartet


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
    # für den Start des Prozesses (auf Schulrechnern langsam), den ersten Import großer Bibliotheken
    # (pandas direkt nach der Installation: über 8 Sekunden) und die übrigen Tests.
    gesamtlimit = 10 * ZEITLIMIT_SEKUNDEN
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
    _lade_bibliotheken_vorab(quelltext)
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


def _lade_bibliotheken_vorab(quelltext: str) -> None:
    """Importiert die Bibliotheken aus ``BIBLIOTHEKEN``, die im Programm vorkommen, schon vor dem Zeitlimit.

    Der erste Import von pandas nach der Installation dauert mehrere Sekunden; das soll nicht als
    Endlosschleife zählen. Fehlt eine Bibliothek, meldet das später der Lauf des Programms.

    Testen: ``import colorsys`` mit ``BIBLIOTHEKEN = ("colorsys",)`` → danach in ``sys.modules``;
    fehlende Bibliothek → kein Fehler.
    """
    for name in BIBLIOTHEKEN:
        if name in quelltext:  # grob, aber ein Import zu viel schadet nicht
            with contextlib.suppress(ImportError):
                importlib.import_module(name)


def _test_namensraum(lauf: Lauf, skript: Path, quelltext: str) -> dict[str, Any]:
    """Ergänzt den Namensraum des Programms um ``AUSGABE``, ``starte``, ``verwendet`` und die Hilfen für Tests."""

    def starte(*eingaben: str) -> str:
        """Startet das Programm erneut mit anderen Eingaben und liefert dessen Ausgabe."""
        neu = _starte_programm(skript, quelltext, eingaben)
        if neu.fehler:
            raise ProgrammFehler(f"Mit den Eingaben {list(eingaben)}: {neu.fehler}")
        return neu.ausgabe

    namensraum = lauf.namensraum
    namensraum.update(
        AUSGABE=lauf.ausgabe,
        starte=starte,
        verwendet=functools.partial(verwendet, quelltext),
        Zaehlliste=Zaehlliste,
        zaehle_schritte=functools.partial(zaehle_schritte, skript),
        # Nur die Klasse, nicht das Modul: Über random._os käme man sonst an os heran, und eingereichte
        # Tests dürfen nichts importieren (.github/pruefe_einreichung.py).
        Zufall=random.Random,
    )
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
            ergebnisse.append(
                TestErgebnis(
                    schritt.name,
                    "Zeitlimit überschritten - vielleicht eine Endlosschleife oder ein zu langsames Verfahren?",
                )
            )
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
        """Liefert den Kopf dieser Datei mit der Liste der Themen als Hilfetext."""
        return f"{__doc__}\nThemen:\n{_themenliste()}\n"

    def error(self, message: str) -> NoReturn:
        """Beendet mit Aufrufbeispiel statt der englischen argparse-Meldung."""
        self.exit(
            2,
            "Aufruf nicht verstanden. So geht es:\n"
            "    python pruefe.py 1_003        → prüft Aufgabe 1_003\n"
            "    python pruefe.py 1_001 1_003  → prüft die Aufgaben 1_001 und 1_003\n"
            "    python pruefe.py 2            → prüft alle Aufgaben der Stufe 2\n"
            "    python pruefe.py funktionen   → prüft alle Aufgaben zum Thema Funktionen\n"
            "    python pruefe.py 2 funktionen → prüft die Aufgaben der Stufe 2 zum Thema Funktionen\n"
            "    python pruefe.py              → prüft alle Aufgaben, die Sie schon bearbeitet haben\n"
            "    python pruefe.py --liste      → zeigt alle Aufgaben nach Thema mit Ihrem Stand\n",
        )


def _themenliste() -> str:
    """Liefert alle Themen als eingerückte Zeilen ``Schlüssel  Bezeichnung``."""
    breite = max(len(thema) for thema in THEMEN)
    return "\n".join(f"  {thema:<{breite}}  {bezeichnung}" for thema, bezeichnung in THEMEN.items())


def _lies_argumente(argumente: list[str]) -> argparse.Namespace:
    """Wertet die Kommandozeile aus: Kennungen sowie die Ordner für Aufgaben und Tests."""
    parser = _DeutscherParser()
    parser.add_argument("kennungen", nargs="*")  # Anfänge der Aufgabennamen oder Themen, z. B. 1_001 2 funktionen
    parser.add_argument("--aufgaben", type=Path, default=PROJEKT / "aufgaben")  # Ordner mit den Lösungen
    parser.add_argument("--tests", type=Path, default=PROJEKT / "tests")  # Ordner mit den Tests
    parser.add_argument("--liste", action="store_true")  # Übersicht mit Stand statt ausführlicher Berichte
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
    """Liefert die erste Kennung, die kein Thema ist und zu der es keine Aufgabe gibt, sonst ``None``."""
    for kennung in kennungen:
        if kennung not in THEMEN and not _passende_tests(alle, kennung):
            return kennung
    return None


def _waehle_aus(alle: list[Path], kennungen: list[str]) -> list[Path]:
    """Wählt nach Namensanfängen und Themen aus.

    Namensanfänge untereinander und Themen untereinander ergänzen sich, beide zusammen müssen passen:
    ``2 funktionen`` sind die Aufgaben der Stufe 2 zum Thema Funktionen.

    Testen: nur Themen → alle Aufgaben dieser Themen; nur Namensanfänge → wie ``_waehle_nach_kennungen``;
    Stufe und Thema → nur Aufgaben, die zu beidem passen; Testdatei ohne Thema → passt zu keinem Thema.
    """
    themen = [kennung for kennung in kennungen if kennung in THEMEN]
    anfaenge = [kennung for kennung in kennungen if kennung not in THEMEN]
    auswahl = _waehle_nach_kennungen(alle, anfaenge) if anfaenge else alle
    if not themen:
        return auswahl
    return [testdatei for testdatei in auswahl if lies_thema(testdatei) in themen]


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
    bericht = formatiere(testdatei.stem, auswertung)
    # In den Kopien der Lernenden bleibt der alte Text stehen, die Tests holt GitHub aber immer frisch.
    if not auswertung.bestanden and aufgabentext_veraltet(skript, testdatei):
        bericht += (
            "\n  Hinweis: Der Aufgabentext in Ihrer Datei weicht von der aktuellen Fassung ab - vermutlich wurde "
            "die Aufgabe überarbeitet. Die Tests prüfen die aktuelle Fassung; Sie finden sie unter "
            f"aufgaben/{testdatei.name} im Aufgaben-Repository."
        )
    # Wie bei LeetCode: Die Lösung zum Vergleich gibt es erst nach dem Bestehen zu sehen.
    musterloesung = testdatei.parent.parent / "loesungen" / testdatei.name
    if auswertung.bestanden and musterloesung.exists():
        bericht += f"\n  Zum Vergleich: Musterlösung und Lösungsweg in loesungen/{testdatei.name}"
    return bericht, auswertung.bestanden


def _stand(aufgaben_ordner: Path, testdatei: Path) -> str:
    """Liefert ○, wenn die Aufgabe unbearbeitet ist (Datei fehlt oder ist die Vorlage), sonst ✓ oder ✗.

    Nur bearbeitete Aufgaben werden geprüft, damit die Übersicht auch bei vielen Aufgaben schnell ist.
    """
    skript = aufgaben_ordner / testdatei.name
    if not skript.exists() or entspricht_vorlage(skript, testdatei):
        return "○"
    return "✓" if pruefe_loesung(skript, testdatei).bestanden else "✗"


def _zeige_uebersicht(aufgaben_ordner: Path, auswahl: list[Path]) -> None:
    """Gibt die Aufgaben nach Thema mit ihrem Stand aus, Zeile für Zeile, damit man den Fortschritt sieht."""
    breite = max((len(testdatei.stem) for testdatei in auswahl), default=0)
    staende: list[str] = []
    for thema, dateien in nach_thema(auswahl).items():
        print(f"{THEMEN[thema]}  (python pruefe.py {thema})")
        for testdatei in dateien:
            stand = _stand(aufgaben_ordner, testdatei)
            staende.append(stand)
            print(f"  {stand} {testdatei.stem:<{breite}}  {lies_inhalt(testdatei) or ''}", flush=True)
        print()
    print(f"→ ✓ {staende.count('✓')} bestanden, ✗ {staende.count('✗')} offen, ○ {staende.count('○')} unbearbeitet")


def main(argumente: list[str]) -> int:
    """Einstiegspunkt.

    Mit Kennungen: alle Aufgaben, deren Name mit einer davon beginnt, eingeschränkt auf die
    genannten Themen. Ohne: alle Aufgaben, deren Datei sich von der Vorlage unterscheidet.
    Mit ``--liste``: statt der Berichte nur eine Übersicht mit Stand, ohne Kennungen über alle Aufgaben.
    Exit-Code 1, wenn etwas nicht bestanden ist (GitHub zeigt dann ✗); die Übersicht endet immer mit 0.

    Testen: Kennung passt auf eine oder mehrere Aufgaben → alle diese; genau gleicher Name → nur dieser;
    unbekannte Kennung → Aufgaben und Themen auflisten, Exit 2; nichts passt zu Stufe und Thema → Exit 2;
    ohne Kennung und nichts bearbeitet → Hinweis, Exit 0; unveränderte Vorlagen werden übersprungen;
    ``--liste`` → ✓/✗/○ je Aufgabe nach Thema, Exit 0.
    """
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(errors="replace")  # ✓/✗ auch in Konsolen ohne UTF-8
    args = _lies_argumente(argumente)
    alle = sorted(args.tests.glob("*.py"))

    if args.kennungen:
        unbekannt = _unbekannte_kennung(alle, args.kennungen)
        if unbekannt is not None:
            print(f"Keine Aufgabe zu „{unbekannt}“, und das ist auch kein Thema. Vorhanden sind:")
            print("\n".join(f"  {t.stem}" for t in alle))
            print(f"Themen:\n{_themenliste()}")
            return 2
        auswahl = _waehle_aus(alle, args.kennungen)
        if not auswahl:
            print(f"Zu „{' '.join(args.kennungen)}“ gibt es (noch) keine Aufgabe.")
            return 2
    elif args.liste:
        auswahl = alle
    else:
        auswahl = _bearbeitete_aufgaben(alle, args.aufgaben)
        if not auswahl:
            print("Noch keine bearbeitete Aufgabe gefunden. Bearbeiten Sie eine Datei im Ordner „aufgaben“.")
            return 0

    if args.liste:
        _zeige_uebersicht(args.aufgaben, auswahl)
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
