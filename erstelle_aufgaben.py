"""Erzeugt aus den Musterdateien die Vorlagen für die SuS und die Tests.

Benutzung (im Projektordner):
    python erstelle_aufgaben.py

Liest     eigene_aufgaben/<name>.py    (SuS)
          lehrkraft/muster/<name>.py   (Lehrkraft, falls vorhanden)
Schreibt  aufgaben/<name>.py   Vorlage: Lösungen durch Platzhalter ersetzt, Tests entfernt
          tests/<name>.py      nur die Tests
und prüft, dass jede Musterlösung ihre eigenen Tests besteht und die leere Vorlage nicht.

Bei neuen Aufgaben (Testdatei noch nicht in git) wird die Musterlösung außerdem an je einer
Stelle verändert, z. B. ``<`` statt ``<=`` oder eine Zeile gestrichen. Jede solche Änderung
sollte mindestens ein Test bemerken; sonst gibt es eine Warnung ⚠ (die Änderung kann aber auch
gleichwertig sein, dann ist sie harmlos).

Marker in der Musterdatei (je eine eigene Zeile, wie bei nbgrader):
    ### BEGIN SOLUTION  …  ### END SOLUTION   → wird in der Vorlage zu `pass  # ← Ersetzen Sie …`
    ### BEGIN TESTS     …  ### END TESTS      → wandert in die Testdatei
``### BEGIN HIDDEN TESTS`` wird wie TESTS behandelt (verstecken geht ohne Server nicht).
"""

from __future__ import annotations  # erlaubt `str | None` usw. auch vor Python 3.10

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

from pruefe import Auswertung, formatiere, pruefe_loesung, vorlage_hash

MARKER = re.compile(
    r"^(?P<einrueckung>\s*)###\s*(?P<art>BEGIN|END)\s+(?P<bereich>SOLUTION|TESTS|HIDDEN TESTS)\s*(?:###)?\s*$"
)
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


@dataclass(frozen=True)
class Zerlegt:
    """Die drei Teile einer Musterdatei.

    ``loesung`` hat dieselben Zeilennummern wie die Musterdatei (Marker und Tests sind Leerzeilen),
    ``loesungszeilen`` sind die Nummern der Zeilen zwischen BEGIN und END SOLUTION.
    """

    vorlage: str
    loesung: str
    tests: str
    loesungszeilen: frozenset[int]


# --- Musterdatei zerlegen ---


def _als_text(zeilen: list[str]) -> str:
    """Fügt Zeilen zusammen, ohne Leerzeilen am Anfang und Ende."""
    return "\n".join(zeilen).strip("\n") + "\n"


def zerlege(muster: str, quelle: str) -> Zerlegt:
    """Zerlegt eine Musterdatei in Vorlage, Musterlösung und Tests.

    Testen: SOLUTION oben und eingerückt in einer Funktion → Platzhalter mit gleicher
    Einrückung; Testzeilen nur in ``tests``; ``loesung`` ohne Marker und ohne Tests;
    ``### BEGIN SOLUTION ###`` (mit ### am Ende) wird erkannt; END ohne BEGIN und
    fehlendes END → ``ValueError`` mit Dateiname und Zeile.
    """
    vorlage: list[str] = []
    loesung: list[str] = []
    tests: list[str] = []
    loesungszeilen: set[int] = set()
    offen: str | None = None
    for nummer, zeile in enumerate(muster.splitlines(), start=1):
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
        _als_text(vorlage), loesung_mit_zeilennummern, textwrap.dedent(_als_text(tests)), frozenset(loesungszeilen)
    )


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
    """Schreibt die Vorlage und die Testdatei mit Herkunft und ``vorlage-hash`` im Kopf."""
    vorlage.write_text(teile.vorlage, encoding="utf-8")
    testdatei.write_text(
        f"# Automatisch erzeugt aus {muster.relative_to(PROJEKT).as_posix()} - nicht von Hand ändern.\n"
        f"# vorlage-hash: {vorlage_hash(teile.vorlage)}\n\n{teile.tests}",
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


def main() -> int:
    """Einstiegspunkt: erzeugt die Aufgaben aus allen Musterordnern. Exit-Code 1, wenn etwas nicht taugt."""
    vorhanden = [ordner for ordner in MUSTER_ORDNER if any(ordner.glob("*.py"))]
    if not vorhanden:
        print("✗ Keine Musterdateien gefunden. Legen Sie Ihre Aufgabe in den Ordner eigene_aufgaben/.")
        return 1
    try:
        ok = all([erstelle(ordner, PROJEKT / "aufgaben", PROJEKT / "tests") for ordner in vorhanden])  # noqa: C419 - Liste, damit alle Ordner erzeugt werden, nicht nur bis zum ersten Fehler
    except ValueError as fehler:  # fehlerhafte Marker in einer Musterdatei
        print(f"✗ {fehler}")
        return 1
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
