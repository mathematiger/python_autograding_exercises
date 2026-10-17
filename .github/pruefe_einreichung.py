"""Prüft einen Pull Request mit eingereichten Aufgaben, bevor die Lehrkraft ihn übernimmt.

Benutzung:
    python .github/pruefe_einreichung.py <stand vorher> <stand mit pull request>

GitHub ruft das bei jedem Pull Request auf (.github/workflows/einreichung.yml). Geprüft wird:
  - Der Pull Request ändert nur aufgaben/*.py, tests/*.py und README.md.
  - Zu jeder Aufgabe gibt es Vorlage und Testdatei, beide aus demselben Lauf von erstelle_aufgaben.py.
  - Vorlage und Tests enthalten nichts, womit sie auf den Rechnern der SuS Dateien lesen,
    schreiben oder Programme starten könnten (kein import, open, eval, exec, __…__ usw.).
  - Die leere Vorlage besteht die Tests nicht.

Ein ✓ ersetzt nicht den Blick auf Aufgabentext und Tests.
"""

from __future__ import annotations  # erlaubt `str | None` usw. auch vor Python 3.10

import ast
import re
import sys
from pathlib import Path

PROJEKT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJEKT))

from pruefe import lies_vorlage_hash, pruefe_loesung, vorlage_hash  # erst nach sys.path.insert importierbar

ERLAUBTE_DATEIEN = re.compile(r"(aufgaben|tests)/[^/]+\.py|README\.md")
# Damit käme man an Dateien, Prozesse oder die Interna von pruefe.py heran.
VERBOTENE_NAMEN = {
    "open",
    "exec",
    "eval",
    "compile",
    "globals",
    "locals",
    "vars",
    "getattr",
    "setattr",
    "delattr",
    "breakpoint",
}
# Über Generatoren und Tracebacks kommt man auch ohne __ an die Builtins, z. B. gi_frame.f_builtins.
VERBOTENE_ATTRIBUTE = {"gi_frame", "cr_frame", "ag_frame", "tb_frame", "f_back", "f_builtins", "f_globals", "f_locals"}


def _dateien(ordner: Path) -> set[str]:
    """Liefert alle Dateien im Ordner als relative Pfade mit ``/``, ohne den Ordner ``.git``."""
    pfade: set[str] = set()
    for pfad in ordner.rglob("*"):
        relativ = pfad.relative_to(ordner)
        if pfad.is_file() and relativ.parts[0] != ".git":
            pfade.add(relativ.as_posix())
    return pfade


def geaenderte_dateien(vorher: Path, nachher: Path) -> list[str]:
    """Liefert die relativen Pfade aller Dateien, die neu, geändert oder gelöscht sind."""
    geaendert: list[str] = []
    for pfad in sorted(_dateien(vorher) | _dateien(nachher)):
        alt = vorher / pfad
        neu = nachher / pfad
        if not alt.is_file() or not neu.is_file() or alt.read_bytes() != neu.read_bytes():
            geaendert.append(pfad)
    return geaendert


def _ist_bedenklich(knoten: ast.AST) -> bool:
    """Prüft, ob ein Knoten mehr darf, als eine Übungsaufgabe braucht."""
    if isinstance(knoten, (ast.Import, ast.ImportFrom)):
        return True
    if isinstance(knoten, ast.Name):
        # __name__ braucht man für `if __name__ == "__main__":`, alle anderen __…__ nicht.
        return knoten.id in VERBOTENE_NAMEN or (knoten.id.startswith("__") and knoten.id != "__name__")
    if isinstance(knoten, ast.Attribute):
        return knoten.attr.startswith("_") or knoten.attr in VERBOTENE_ATTRIBUTE
    return False


def bedenkliche_stellen(quelltext: str) -> list[str]:
    """Findet Stellen wie ``import``, ``open(…)`` oder ``x.__class__``, jeweils mit Zeilennummer.

    ponytail: Sperrliste, keine Sandbox - fängt Unfug und naive Angriffe ab; die Lehrkraft liest trotzdem mit.

    Testen: ``import os`` → Treffer; ``x.__class__`` → Treffer; ``if __name__ == "__main__"`` → kein Treffer;
    ``for _ in range(3)`` → kein Treffer; Syntaxfehler → Treffer.
    """
    try:
        baum = ast.parse(quelltext)
    except SyntaxError as fehler:
        return [f"Zeile {fehler.lineno}: Syntaxfehler"]
    stellen: list[str] = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, (ast.stmt, ast.expr)) and _ist_bedenklich(knoten):
            stellen.append(f"Zeile {knoten.lineno}: {ast.unparse(knoten)}")
    return stellen


def pruefe_aufgabe(nachher: Path, dateiname: str) -> list[str]:
    """Prüft Vorlage und Tests einer Aufgabe im Stand mit Pull Request; liefert die Probleme (leer = in Ordnung)."""
    vorlage = nachher / "aufgaben" / dateiname
    testdatei = nachher / "tests" / dateiname
    for datei in (vorlage, testdatei):
        if not datei.is_file():
            return [f"{datei.relative_to(nachher).as_posix()} fehlt - laden Sie immer beide Dateien hoch."]

    probleme: list[str] = []
    for datei in (vorlage, testdatei):
        for stelle in bedenkliche_stellen(datei.read_text(encoding="utf-8-sig")):
            probleme.append(f"{datei.relative_to(nachher).as_posix()}, {stelle} - ist nicht erlaubt.")
    if probleme:
        return probleme  # solchen Code gar nicht erst ausführen

    if lies_vorlage_hash(testdatei) != vorlage_hash(vorlage.read_text(encoding="utf-8-sig")):
        return ["Vorlage und Tests passen nicht zusammen. Erzeugen Sie beide neu und laden Sie beide hoch."]
    auswertung = pruefe_loesung(vorlage, testdatei)
    if auswertung.abgebrochen:
        return [f"Die Prüfung der leeren Vorlage wurde abgebrochen: {auswertung.programmfehler or 'Zeitlimit'}"]
    if not auswertung.tests:
        return ["Die Testdatei enthält keine Tests."]
    if auswertung.bestanden:
        return ["Schon die leere Vorlage besteht alle Tests - die Tests prüfen zu wenig."]
    return []


def main(argumente: list[str]) -> int:
    """Einstiegspunkt. Exit-Code 1, wenn etwas auffällt (GitHub zeigt dann ✗ am Pull Request).

    Testen: nichts geändert → 0; gültige neue Aufgabe → 0; andere Datei geändert → 1;
    ``import`` in den Tests → 1, ohne sie auszuführen; leere Vorlage besteht → 1; falscher vorlage-hash → 1.
    """
    if len(argumente) != 2:
        print(__doc__)
        return 2
    vorher, nachher = Path(argumente[0]), Path(argumente[1])
    alles_ok = True
    aufgaben: set[str] = set()
    for pfad in geaenderte_dateien(vorher, nachher):
        if not ERLAUBTE_DATEIEN.fullmatch(pfad):
            print(f"✗ {pfad}: Diese Datei darf eine Einreichung nicht ändern.")
            alles_ok = False
        elif pfad != "README.md":
            aufgaben.add(Path(pfad).name)

    for dateiname in sorted(aufgaben):
        probleme = pruefe_aufgabe(nachher, dateiname)
        print(f"{'✗' if probleme else '✓'} {Path(dateiname).stem}")
        for problem in probleme:
            print(f"    {problem}")
        alles_ok = alles_ok and not probleme

    if alles_ok:
        print("→ Keine Auffälligkeiten. Aufgabentext und Tests trotzdem ansehen.")
    return 0 if alles_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
