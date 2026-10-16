"""Erzeugt aus den Musterdateien die Vorlagen für die SuS und die Tests.

Benutzung (im Projektordner):
    python erstelle_aufgaben.py

Liest     eigene_aufgaben/<name>.py    (SuS)
          lehrkraft/muster/<name>.py   (Lehrkraft, falls vorhanden)
Schreibt  aufgaben/<name>.py   Vorlage: Lösungen durch Platzhalter ersetzt, Tests entfernt
          tests/<name>.py      nur die Tests
und prüft, dass jede Musterlösung ihre eigenen Tests besteht und die leere Vorlage nicht.

Marker in der Musterdatei (je eine eigene Zeile, wie bei nbgrader):
    ### BEGIN SOLUTION  …  ### END SOLUTION   → wird in der Vorlage zu `pass  # ← Ersetzen Sie …`
    ### BEGIN TESTS     …  ### END TESTS      → wandert in die Testdatei
``### BEGIN HIDDEN TESTS`` wird wie TESTS behandelt (verstecken geht ohne Server nicht).
"""

import re
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path

PROJEKT = Path(__file__).resolve().parent
MUSTER_ORDNER = (PROJEKT / "lehrkraft" / "muster", PROJEKT / "eigene_aufgaben")
sys.path.insert(0, str(PROJEKT))

from pruefe import formatiere, pruefe_loesung, vorlage_hash  # noqa: E402

MARKER = re.compile(
    r"^(?P<einrueckung>\s*)###\s*(?P<art>BEGIN|END)\s+(?P<bereich>SOLUTION|TESTS|HIDDEN TESTS)\s*(?:###)?\s*$"
)
PLATZHALTER = "pass  # ← Ersetzen Sie diese Zeile durch Ihren Code"


@dataclass(frozen=True)
class Zerlegt:
    """Die drei Teile einer Musterdatei."""

    vorlage: str
    loesung: str
    tests: str


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
    offen: str | None = None
    for nummer, zeile in enumerate(muster.splitlines(), start=1):
        treffer = MARKER.match(zeile)
        if treffer is None:
            if offen == "TESTS":
                tests.append(zeile)
            else:
                loesung.append(zeile)
                if offen is None:
                    vorlage.append(zeile)
            continue
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
    return Zerlegt(_als_text(vorlage), _als_text(loesung), textwrap.dedent(_als_text(tests)))


def erstelle(muster_ordner: Path, aufgaben_ordner: Path, tests_ordner: Path) -> bool:
    """Erzeugt Vorlagen und Tests für alle Musterdateien und prüft sie.

    Testen: pro Musterdatei entstehen genau zwei Dateien; Testdatei beginnt mit
    ``# vorlage-hash:``; fehlerhafte Musterlösung → ``False`` mit Bericht;
    Vorlage, die schon alle Tests besteht → Warnung und ``False``.
    """
    alles_ok = True
    for muster in sorted(muster_ordner.glob("*.py")):
        teile = zerlege(muster.read_text(encoding="utf-8"), muster.name)
        vorlage = aufgaben_ordner / muster.name
        testdatei = tests_ordner / muster.name
        vorlage.write_text(teile.vorlage, encoding="utf-8")
        testdatei.write_text(
            f"# Automatisch erzeugt aus {muster.relative_to(PROJEKT).as_posix()} - nicht von Hand ändern.\n"
            f"# vorlage-hash: {vorlage_hash(teile.vorlage)}\n\n{teile.tests}",
            encoding="utf-8",
        )
        with tempfile.TemporaryDirectory() as ordner:
            loesung = Path(ordner) / muster.name
            loesung.write_text(teile.loesung, encoding="utf-8")
            mit_loesung = pruefe_loesung(loesung, testdatei)
        ohne_loesung = pruefe_loesung(vorlage, testdatei)

        if not mit_loesung.bestanden:
            print(f"✗ {muster.name}: Die Musterlösung besteht ihre Tests nicht.")
            print(textwrap.indent(formatiere(muster.stem, mit_loesung), "    "))
            alles_ok = False
        elif ohne_loesung.bestanden:
            print(f"✗ {muster.name}: Schon die leere Vorlage besteht alle Tests - die Tests prüfen zu wenig.")
            alles_ok = False
        else:
            print(f"✓ {muster.name} ({len(mit_loesung.tests)} Tests)")
    return alles_ok


if __name__ == "__main__":
    vorhanden = [ordner for ordner in MUSTER_ORDNER if any(ordner.glob("*.py"))]
    if not vorhanden:
        print("✗ Keine Musterdateien gefunden. Legen Sie Ihre Aufgabe in den Ordner eigene_aufgaben/.")
        sys.exit(1)
    try:
        ok = all([erstelle(ordner, PROJEKT / "aufgaben", PROJEKT / "tests") for ordner in vorhanden])
    except ValueError as fehler:  # fehlerhafte Marker in einer Musterdatei
        print(f"✗ {fehler}")
        ok = False
    sys.exit(0 if ok else 1)
