"""Erzeugt aus den Musterdateien die Vorlagen für die SuS und die Tests.

Benutzung (im Projektordner):
    python erstelle_aufgaben.py

Liest     eigene_aufgaben/<name>.py    (SuS)
          lehrkraft/muster/<name>.py   (Lehrkraft, falls vorhanden)
Schreibt  aufgaben/<name>.py   Vorlage: Lösungen durch Platzhalter ersetzt, Tests entfernt
          tests/<name>.py      nur die Tests
          README.md            die Aufgabenlisten nach Thema und Stufe (aus allen Dateien in tests/)
und prüft, dass jede Musterlösung ihre eigenen Tests besteht und die leere Vorlage nicht.

Bei neuen Aufgaben (Testdatei noch nicht in git) wird die Musterlösung außerdem an je einer
Stelle verändert, z. B. ``<`` statt ``<=`` oder eine Zeile gestrichen. Jede solche Änderung
sollte mindestens ein Test bemerken; sonst gibt es eine Warnung ⚠ (die Änderung kann aber auch
gleichwertig sein, dann ist sie harmlos).

Die Musterdatei beginnt mit zwei Kopfzeilen, die in die Testdatei wandern (nicht in die Vorlage):
    # Thema: kontrollfluss          → eines der Themen aus THEMEN in pruefe.py
    # Inhalt: Schleife mit break    → Kurzbeschreibung für die README

Marker in der Musterdatei (je eine eigene Zeile, wie bei nbgrader):
    ### BEGIN SOLUTION  …  ### END SOLUTION   → wird in der Vorlage zu `pass  # ← Ersetzen Sie …`
    ### BEGIN TESTS     …  ### END TESTS      → wandert in die Testdatei
``### BEGIN HIDDEN TESTS`` wird wie TESTS behandelt (verstecken geht ohne Server nicht).
"""

import ast
import copy
import re
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path

PROJEKT = Path(__file__).resolve().parent
MUSTER_ORDNER = (PROJEKT / "lehrkraft" / "muster", PROJEKT / "eigene_aufgaben")
sys.path.insert(0, str(PROJEKT))

from pruefe import THEMEN, Auswertung, formatiere, lies_inhalt, lies_thema, nach_thema, pruefe_loesung, vorlage_hash

MARKER = re.compile(
    r"^(?P<einrueckung>\s*)###\s*(?P<art>BEGIN|END)\s+(?P<bereich>SOLUTION|TESTS|HIDDEN TESTS)\s*(?:###)?\s*$"
)
KOPFZEILE = re.compile(r"^# (?P<schluessel>Thema|Inhalt):(?P<wert>.*)$")
PLATZHALTER = "pass  # ← Ersetzen Sie diese Zeile durch Ihren Code"
# Für die Prüfung der Tests: jeweils ein typischer Fehler beim Vergleichen und Rechnen.
VERTAUSCHTE_VERGLEICHE: dict[type[ast.cmpop], type[ast.cmpop]] = {
    ast.Lt: ast.LtE,
    ast.LtE: ast.Lt,
    ast.Gt: ast.GtE,
    ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
    ast.In: ast.NotIn,
    ast.NotIn: ast.In,
}
VERTAUSCHTE_RECHENZEICHEN: dict[type[ast.operator], type[ast.operator]] = {
    ast.Add: ast.Sub,
    ast.Sub: ast.Add,
    ast.Mult: ast.Div,
    ast.Div: ast.Mult,
    ast.FloorDiv: ast.Div,
    ast.Mod: ast.FloorDiv,
}
STREICHBARE_ANWEISUNGEN = (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Expr, ast.Raise, ast.Break, ast.Continue)
# Zwischen diesen Markern schreibt aktualisiere_readme die Aufgabenlisten neu, der Rest der README bleibt.
README_ANFANG = "<!-- AUFGABEN-ANFANG: erzeugt von erstelle_aufgaben.py, nicht von Hand ändern -->"
README_ENDE = "<!-- AUFGABEN-ENDE -->"
STUFEN: dict[str, str] = {
    "1": "Erste Schritte mit vorgegebenem Code",
    "2": "Kontrollfluss, Funktionen, Datenstrukturen",
    "3": "Algorithmen, Fehlerbehandlung, Programmorganisation",
    "4": "Die Sprache beherrschen",
    "5": "Unter der Haube",
}


@dataclass(frozen=True)
class Zerlegt:
    """Die drei Teile einer Musterdatei und ihre Kopfzeilen.

    ``loesung`` hat dieselben Zeilennummern wie die Musterdatei (Kopfzeilen, Marker und Tests sind
    Leerzeilen), ``loesungszeilen`` sind die Nummern der Zeilen zwischen BEGIN und END SOLUTION.
    """

    vorlage: str
    loesung: str
    tests: str
    loesungszeilen: frozenset[int]
    thema: str
    inhalt: str


# --- Musterdatei zerlegen ---


def _als_text(zeilen: list[str]) -> str:
    """Fügt Zeilen zusammen, ohne Leerzeilen am Anfang und Ende."""
    return "\n".join(zeilen).strip("\n") + "\n"


def zerlege(muster: str, quelle: str) -> Zerlegt:
    """Zerlegt eine Musterdatei in Vorlage, Musterlösung und Tests.

    Testen: SOLUTION oben und eingerückt in einer Funktion → Platzhalter mit gleicher
    Einrückung; Testzeilen nur in ``tests``; ``loesung`` ohne Marker und ohne Tests;
    ``### BEGIN SOLUTION ###`` (mit ### am Ende) wird erkannt; END ohne BEGIN und
    fehlendes END → ``ValueError`` mit Dateiname und Zeile; Kopfzeilen landen in ``thema``
    und ``inhalt``, nicht in Vorlage und Lösung.
    """
    zeilen = muster.splitlines()
    kopf = _kopfzeilen(zeilen)
    thema, inhalt = _thema_und_inhalt(dict(kopf), quelle)
    vorlage: list[str] = []
    loesung: list[str] = []
    tests: list[str] = []
    loesungszeilen: set[int] = set()
    offen: str | None = None
    # Kopfzeilen als Leerzeilen, damit die Lösung die Zeilennummern der Musterdatei behält
    for nummer, zeile in enumerate([""] * len(kopf) + zeilen[len(kopf) :], start=1):
        treffer = MARKER.match(zeile)
        if treffer is None:
            if offen == "TESTS":
                tests.append(zeile)
                loesung.append("")
            else:
                loesung.append(zeile)
                if offen is None:
                    vorlage.append(zeile)
                else:
                    loesungszeilen.add(nummer)
            continue
        loesung.append("")  # damit Fehlermeldungen der Musterlösung die Zeilen der Musterdatei nennen
        bereich = "TESTS" if "TESTS" in treffer["bereich"] else "SOLUTION"
        if treffer["art"] == "BEGIN":
            if offen is not None:
                raise ValueError(f"{quelle}, Zeile {nummer}: BEGIN {bereich}, obwohl {offen} noch offen ist")
            offen = bereich
            if bereich == "SOLUTION":
                vorlage.append(treffer["einrueckung"] + PLATZHALTER)
        else:
            if offen != bereich:
                raise ValueError(f"{quelle}, Zeile {nummer}: END {bereich} ohne passendes BEGIN")
            offen = None
    if offen is not None:
        raise ValueError(f"{quelle}: {offen} wird mit BEGIN geöffnet, aber nie mit END geschlossen")
    loesung_mit_zeilennummern = "\n".join(loesung).rstrip("\n") + "\n"
    return Zerlegt(
        _als_text(vorlage),
        loesung_mit_zeilennummern,
        textwrap.dedent(_als_text(tests)),
        frozenset(loesungszeilen),
        thema,
        inhalt,
    )


def _kopfzeilen(zeilen: list[str]) -> list[tuple[str, str]]:
    """Liefert die Kopfzeilen ``# Thema: …`` und ``# Inhalt: …`` am Dateianfang als (Schlüssel, Wert)."""
    kopf: list[tuple[str, str]] = []
    for zeile in zeilen:
        treffer = KOPFZEILE.match(zeile)
        if treffer is None:
            break
        kopf.append((treffer["schluessel"], treffer["wert"].strip()))
    return kopf


def _thema_und_inhalt(kopf: dict[str, str], quelle: str) -> tuple[str, str]:
    """Prüft die Kopfzeilen und liefert Thema und Inhalt.

    Testen: Thema fehlt oder ist unbekannt → ``ValueError`` mit allen erlaubten Themen;
    Inhalt fehlt oder ist leer → ``ValueError``.
    """
    erlaubt = f"Erlaubte Themen: {', '.join(THEMEN)}"
    thema = kopf.get("Thema")
    if not thema:
        raise ValueError(f"{quelle}: Am Anfang fehlt die Zeile „# Thema: …“. {erlaubt}")
    if thema not in THEMEN:
        raise ValueError(f"{quelle}: Unbekanntes Thema „{thema}“. {erlaubt}")
    inhalt = kopf.get("Inhalt")
    if not inhalt:
        raise ValueError(f"{quelle}: Am Anfang fehlt die Zeile „# Inhalt: …“ mit einer Kurzbeschreibung der Aufgabe.")
    return thema, inhalt


# --- Tests mit absichtlich falschen Lösungen prüfen ---


def _varianten(knoten: ast.AST) -> list[ast.AST]:
    """Liefert absichtlich falsche Fassungen eines Knotens, z. B. ``<=`` statt ``<`` oder ``pass`` statt der Zeile."""
    varianten: list[ast.AST] = []
    if isinstance(knoten, ast.Compare):
        for index, vergleich in enumerate(knoten.ops):
            if type(vergleich) in VERTAUSCHTE_VERGLEICHE:
                neu = copy.copy(knoten)
                neu.ops = list(knoten.ops)
                neu.ops[index] = VERTAUSCHTE_VERGLEICHE[type(vergleich)]()
                varianten.append(neu)
    if isinstance(knoten, (ast.BinOp, ast.AugAssign)) and type(knoten.op) in VERTAUSCHTE_RECHENZEICHEN:
        neu_rechnung = copy.copy(knoten)
        neu_rechnung.op = VERTAUSCHTE_RECHENZEICHEN[type(knoten.op)]()
        varianten.append(neu_rechnung)
    if isinstance(knoten, ast.BoolOp):
        neu_logik = copy.copy(knoten)
        neu_logik.op = ast.Or() if isinstance(knoten.op, ast.And) else ast.And()
        varianten.append(neu_logik)
    if isinstance(knoten, ast.Constant):
        wert = knoten.value
        if isinstance(wert, (int, float)) and not isinstance(wert, bool):  # True ist auch ein int
            varianten.append(ast.Constant(wert + 1))
        elif isinstance(wert, str) and wert:
            varianten.append(ast.Constant(""))
    if isinstance(knoten, ast.Return) and knoten.value is not None:
        varianten.append(ast.Return(value=None))
    if isinstance(knoten, STREICHBARE_ANWEISUNGEN):
        varianten.append(ast.Pass())
    return varianten


class _Veraenderer(ast.NodeTransformer):
    """Baut die ``ziel``-te Variante in die Lösungszeilen ein und zählt dabei alle möglichen Varianten."""

    def __init__(self, loesungszeilen: frozenset[int], ziel: int) -> None:
        """Merkt sich, welche Zeilen verändert werden dürfen und welche Variante dran ist."""
        self.loesungszeilen = loesungszeilen
        self.ziel = ziel
        self.anzahl = 0
        self.beschreibung = ""

    def visit(self, knoten: ast.AST) -> ast.AST:
        """Besucht erst die Kinder, dann den Knoten selbst; ersetzt ihn, wenn seine Variante dran ist."""
        if isinstance(knoten, ast.Expr) and isinstance(knoten.value, ast.Constant):
            return knoten  # Docstring: eine Änderung daran kann kein Test bemerken
        self.generic_visit(knoten)
        zeile = getattr(knoten, "lineno", None)
        if zeile not in self.loesungszeilen:
            return knoten
        varianten = _varianten(knoten)
        erste = self.anzahl
        self.anzahl += len(varianten)
        if not erste <= self.ziel < self.anzahl:
            return knoten
        ersatz = varianten[self.ziel - erste]
        self.beschreibung = f"Zeile {zeile}: {ast.unparse(knoten)}  →  {ast.unparse(ersatz)}"
        return ersatz


def unbemerkte_aenderungen(teile: Zerlegt, testdatei: Path) -> tuple[list[str], int]:
    """Verändert die Musterlösung an je einer Stelle und prüft jede Fassung mit den Tests.

    Liefert die Änderungen, mit denen trotzdem alle Tests bestehen, und die Anzahl aller Änderungen.

    Testen: Tests prüfen alles → keine Änderung bleibt unbemerkt; ``assert doppelt(0) == 0``
    bei ``return 2 * x`` → ``2  →  3`` bleibt unbemerkt; Code außerhalb von SOLUTION bleibt unverändert.
    """
    baum = ast.parse(teile.loesung)
    zaehler = _Veraenderer(teile.loesungszeilen, ziel=-1)
    zaehler.visit(copy.deepcopy(baum))
    unbemerkt: list[str] = []
    with tempfile.TemporaryDirectory() as ordner:
        skript = Path(ordner) / testdatei.name
        for ziel in range(zaehler.anzahl):
            veraenderer = _Veraenderer(teile.loesungszeilen, ziel)
            skript.write_text(ast.unparse(veraenderer.visit(copy.deepcopy(baum))), encoding="utf-8")
            if pruefe_loesung(skript, testdatei).bestanden:
                unbemerkt.append(veraenderer.beschreibung)
    return unbemerkt, zaehler.anzahl


# --- Aufgaben erzeugen und melden ---


def erstelle(muster_ordner: Path, aufgaben_ordner: Path, tests_ordner: Path) -> bool:
    """Erzeugt Vorlagen und Tests für alle Musterdateien eines Ordners; ``False``, wenn eine nicht taugt.

    Testen: pro Musterdatei entstehen genau zwei Dateien; Testdatei beginnt mit
    ``# vorlage-hash:``; fehlerhafte Musterlösung → ``False`` mit Bericht;
    Vorlage, die schon alle Tests besteht → Warnung und ``False``; unbemerkte Änderung
    der Musterlösung → Warnung ⚠, aber ``True``; Testdatei schon in git → keine Änderungen ausprobiert.
    """
    bekannt = _bekannte_testdateien(tests_ordner)
    ergebnisse = [
        _erstelle_aufgabe(muster, aufgaben_ordner / muster.name, tests_ordner / muster.name, bekannt)
        for muster in sorted(muster_ordner.glob("*.py"))
    ]
    return all(ergebnisse)


def _erstelle_aufgabe(muster: Path, vorlage: Path, testdatei: Path, bekannt: set[str]) -> bool:
    """Erzeugt Vorlage und Testdatei zu einer Musterdatei; ``False``, wenn sie nicht taugen."""
    teile = zerlege(muster.read_text(encoding="utf-8"), muster.name)
    _schreibe_aufgabe(muster, teile, vorlage, testdatei)
    return _melde_pruefung(muster, teile, vorlage, testdatei, bekannt)


def _schreibe_aufgabe(muster: Path, teile: Zerlegt, vorlage: Path, testdatei: Path) -> None:
    """Schreibt die Vorlage und die Testdatei mit Herkunft, ``vorlage-hash``, Thema und Inhalt im Kopf."""
    vorlage.write_text(teile.vorlage, encoding="utf-8")
    testdatei.write_text(
        f"# Automatisch erzeugt aus {muster.relative_to(PROJEKT).as_posix()} - nicht von Hand ändern.\n"
        f"# vorlage-hash: {vorlage_hash(teile.vorlage)}\n"
        f"# thema: {teile.thema}\n"
        f"# inhalt: {teile.inhalt}\n\n{teile.tests}",
        encoding="utf-8",
    )


def _melde_pruefung(muster: Path, teile: Zerlegt, vorlage: Path, testdatei: Path, bekannt: set[str]) -> bool:
    """Gibt aus, ob Musterlösung und leere Vorlage sich wie erwartet verhalten; ``False`` bei einem Fehler."""
    mit_loesung = _pruefe_musterloesung(teile, testdatei)
    if not mit_loesung.bestanden:
        print(f"✗ {muster.name}: Die Musterlösung besteht ihre Tests nicht.")
        print(textwrap.indent(formatiere(muster.stem, mit_loesung), "    "))
        return False
    if pruefe_loesung(vorlage, testdatei).bestanden:
        print(f"✗ {muster.name}: Schon die leere Vorlage besteht alle Tests - die Tests prüfen zu wenig.")
        return False
    if muster.name in bekannt:
        print(f"✓ {muster.name} ({len(mit_loesung.tests)} Tests)")
    else:
        _melde_aenderungen(muster, teile, testdatei, len(mit_loesung.tests))
    return True


def _pruefe_musterloesung(teile: Zerlegt, testdatei: Path) -> Auswertung:
    """Prüft die Musterlösung mit ihren Tests (in einer temporären Datei)."""
    with tempfile.TemporaryDirectory() as ordner:
        loesung = Path(ordner) / testdatei.name
        loesung.write_text(teile.loesung, encoding="utf-8")
        return pruefe_loesung(loesung, testdatei)


def _melde_aenderungen(muster: Path, teile: Zerlegt, testdatei: Path, anzahl_tests: int) -> None:
    """Gibt aus, wie viele Änderungen der Musterlösung die Tests bemerken, und warnt bei jeder unbemerkten."""
    unbemerkt, anzahl = unbemerkte_aenderungen(teile, testdatei)
    bemerkt = anzahl - len(unbemerkt)
    print(f"✓ {muster.name} ({anzahl_tests} Tests, {bemerkt} von {anzahl} Änderungen bemerkt)")
    for beschreibung in unbemerkt:
        print(f"    ⚠ Kein Test bemerkt: {beschreibung}")


def _bekannte_testdateien(tests_ordner: Path) -> set[str]:
    """Namen der Testdateien, die git schon kennt; leer, wenn git fehlt oder der Ordner in keinem Repo liegt."""
    try:
        ergebnis = subprocess.run(
            ["git", "ls-files"], cwd=tests_ordner, capture_output=True, text=True, check=True, encoding="utf-8"
        )
    except (OSError, subprocess.CalledProcessError):
        return set()
    return set(ergebnis.stdout.splitlines())


# --- Aufgabenlisten in der README ---


def aktualisiere_readme(readme: Path, tests_ordner: Path) -> None:
    """Ersetzt in der README alles zwischen ``README_ANFANG`` und ``README_ENDE`` durch die aktuellen Listen."""
    vorne, rest = readme.read_text(encoding="utf-8").split(README_ANFANG, 1)
    _, hinten = rest.split(README_ENDE, 1)
    listen = aufgabenlisten(sorted(tests_ordner.glob("*.py")))
    readme.write_text(f"{vorne}{README_ANFANG}\n\n{listen}\n\n{README_ENDE}{hinten}", encoding="utf-8")


def aufgabenlisten(testdateien: list[Path]) -> str:
    """Baut den Abschnitt der README: Übersicht Thema × Stufe, dann einklappbare Listen nach Thema und nach Stufe.

    Testen: Anzahl je Thema und Stufe in der Übersicht, 0 als leere Zelle; Thema verlinkt auf seine Liste;
    Stufe ohne Aufgabe fehlt; Aufgabe ohne Thema steht nur bei ihrer Stufe.
    """
    themen = nach_thema(testdateien)
    teile = ["### Nach Thema", _themenuebersicht(themen)]
    teile += [_themenliste(thema, dateien) for thema, dateien in themen.items()]
    teile.append("### Nach Stufe")
    for stufe in STUFEN:
        dateien = [testdatei for testdatei in testdateien if _stufe(testdatei) == stufe]
        if dateien:
            teile.append(_stufenliste(stufe, dateien))
    return "\n\n".join(teile)


def _themenuebersicht(themen: dict[str, list[Path]]) -> str:
    """Tabelle mit der Anzahl der Aufgaben je Thema und Stufe und dem passenden Aufruf von pruefe.py."""
    spalten = ["Thema", *(f"Stufe {stufe}" for stufe in STUFEN), "Prüfen mit"]
    zeilen: list[list[str]] = []
    for thema, dateien in themen.items():
        anzahlen = [_anzahl_in_stufe(dateien, stufe) for stufe in STUFEN]
        zeilen.append([f"[{THEMEN[thema]}](#thema-{thema})", *anzahlen, f"`python pruefe.py {thema}`"])
    return _tabelle(spalten, zeilen)


def _themenliste(thema: str, dateien: list[Path]) -> str:
    """Einklappbare Liste der Aufgaben eines Themas, mit Anker für den Link aus der Übersicht."""
    zeilen = [[_link(testdatei), _sterne(_stufe(testdatei)), lies_inhalt(testdatei) or ""] for testdatei in dateien]
    liste = _einklappbar(
        f"<b>{THEMEN[thema]}</b> ({_anzahl_aufgaben(len(dateien))})", ["Aufgabe", "Stufe", "Inhalt"], zeilen
    )
    return f'<a name="thema-{thema}"></a>\n{liste}'


def _stufenliste(stufe: str, dateien: list[Path]) -> str:
    """Einklappbare Liste der Aufgaben einer Stufe mit Thema und Inhalt."""
    zeilen = [[_link(testdatei), _themenname(testdatei), lies_inhalt(testdatei) or ""] for testdatei in dateien]
    titel = f"<b>Stufe {stufe} {_sterne(stufe)}: {STUFEN[stufe]}</b> ({_anzahl_aufgaben(len(dateien))})"
    return _einklappbar(titel, ["Aufgabe", "Thema", "Inhalt"], zeilen)


def _einklappbar(titel: str, spalten: list[str], zeilen: list[list[str]]) -> str:
    """Tabelle in einem ``<details>``-Block; die Leerzeilen braucht GitHub, damit es die Tabelle darin erkennt."""
    return f"<details>\n<summary>{titel}</summary>\n\n{_tabelle(spalten, zeilen)}\n\n</details>"


def _tabelle(spalten: list[str], zeilen: list[list[str]]) -> str:
    """Markdown-Tabelle aus Spaltenköpfen und Zeilen."""
    alle = [spalten, ["---"] * len(spalten), *zeilen]
    return "\n".join("| " + " | ".join(zeile) + " |" for zeile in alle)


def _stufe(testdatei: Path) -> str:
    """Die Stufe steht vorne im Namen: ``2_005_wuerfel`` → ``"2"``."""
    return testdatei.stem.split("_", 1)[0]


def _sterne(stufe: str) -> str:
    """Schwierigkeit als Sterne: ``"2"`` → ``"★★☆☆☆"``."""
    return "★" * int(stufe) + "☆" * (len(STUFEN) - int(stufe))


def _anzahl_in_stufe(dateien: list[Path], stufe: str) -> str:
    """Anzahl der Aufgaben dieser Stufe als Text; leer statt 0, damit die Übersicht ruhig bleibt."""
    anzahl = sum(_stufe(testdatei) == stufe for testdatei in dateien)
    return str(anzahl) if anzahl else ""


def _anzahl_aufgaben(anzahl: int) -> str:
    """``1`` → ``"1 Aufgabe"``, sonst ``"n Aufgaben"``."""
    return "1 Aufgabe" if anzahl == 1 else f"{anzahl} Aufgaben"


def _link(testdatei: Path) -> str:
    """Link auf die Vorlage zur Testdatei, beschriftet mit dem Namen der Aufgabe."""
    return f"[{testdatei.stem}](aufgaben/{testdatei.name})"


def _themenname(testdatei: Path) -> str:
    """Bezeichnung des Themas der Aufgabe, leer bei fehlendem oder unbekanntem Thema."""
    return THEMEN.get(lies_thema(testdatei) or "", "")


def main() -> int:
    """Einstiegspunkt: erzeugt die Aufgaben aus allen Musterordnern und die Listen in der README.

    Exit-Code 1, wenn etwas nicht taugt.
    """
    vorhanden = [ordner for ordner in MUSTER_ORDNER if any(ordner.glob("*.py"))]
    if not vorhanden:
        print("✗ Keine Musterdateien gefunden. Legen Sie Ihre Aufgabe in den Ordner eigene_aufgaben/.")
        return 1
    try:
        ok = all([erstelle(ordner, PROJEKT / "aufgaben", PROJEKT / "tests") for ordner in vorhanden])  # noqa: C419 - Liste, damit alle Ordner erzeugt werden, nicht nur bis zum ersten Fehler
    except ValueError as fehler:  # fehlerhafte Marker in einer Musterdatei
        print(f"✗ {fehler}")
        return 1
    aktualisiere_readme(PROJEKT / "README.md", PROJEKT / "tests")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
