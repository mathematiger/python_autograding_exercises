# SPDX-License-Identifier: MIT
"""Prüft einen Pull Request mit eingereichten Aufgaben, bevor die Lehrkraft ihn übernimmt.

Benutzung:
    python .github/pruefe_einreichung.py <stand vorher> <stand mit pull request>

GitHub ruft das bei jedem Pull Request auf (.github/workflows/einreichung.yml). Geprüft wird:
  - Der Pull Request ändert nur aufgaben/*.py, tests/*.py, loesungen/*.py (nicht für Stufe 4 und 5,
    deren Lösungen bleiben privat), README.md und die Werkzeuge
    (pruefe.py, erstelle_aufgaben.py, entwicklung/*.py - die testet .github/workflows/entwicklung.yml).
  - Zu jeder Aufgabe gibt es Vorlage und Testdatei, bei neuen Aufgaben beide aus demselben Lauf
    von erstelle_aufgaben.py und mit Thema und Inhalt im Kopf der Testdatei. Bestehende Aufgaben
    dürfen von Hand geändert sein.
  - Vorlage und Tests enthalten nichts, womit sie auf den Rechnern der SuS Dateien lesen,
    schreiben oder Programme starten könnten (kein import außer den Bibliotheken aus requirements.txt,
    kein open, eval, exec, __…__ usw.).
  - Die leere Vorlage besteht die Tests nicht. Liegt eine Lösung in loesungen/ bei (freiwillig),
    gilt für sie dieselbe Sperrliste, und sie besteht die Tests.

Ein ✓ ersetzt nicht den Blick auf Aufgabentext und Tests.
"""

import ast
import re
import sys
from pathlib import Path

PROJEKT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJEKT))

from pruefe import (  # erst nach sys.path.insert
    BIBLIOTHEKEN,
    PRIVATE_STUFEN,
    THEMEN,
    entspricht_vorlage,
    lies_inhalt,
    lies_thema,
    pruefe_loesung,
)

AUFGABEN_DATEIEN = re.compile(r"(aufgaben|tests|loesungen)/[^/]+\.py")
# .github/ bleibt gesperrt: Von dort kommen die Prüfungen selbst.
WEITERE_ERLAUBTE_DATEIEN = re.compile(r"README\.md|pruefe\.py|erstelle_aufgaben\.py|entwicklung/[^/]+\.py")
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
    if isinstance(knoten, ast.Import):
        return any(not _ist_bibliothek(alias.name) for alias in knoten.names)
    if isinstance(knoten, ast.ImportFrom):
        # _… wie bei Attributen: über interne Namen einer Bibliothek käme man z. B. an deren os-Modul
        interne = any(alias.name.startswith("_") for alias in knoten.names)
        return knoten.level > 0 or interne or not _ist_bibliothek(knoten.module or "")
    if isinstance(knoten, ast.Name):
        # __name__ braucht man für `if __name__ == "__main__":`, alle anderen __…__ nicht.
        return knoten.id in VERBOTENE_NAMEN or (knoten.id.startswith("__") and knoten.id != "__name__")
    if isinstance(knoten, ast.Attribute):
        return knoten.attr.startswith("_") or knoten.attr in VERBOTENE_ATTRIBUTE
    return False


def _ist_bibliothek(modul: str) -> bool:
    """Prüft, ob ``modul`` (z. B. ``pandas`` oder ``numpy.linalg``) zu einer erlaubten Bibliothek gehört."""
    return modul.partition(".")[0] in BIBLIOTHEKEN


def bedenkliche_stellen(quelltext: str) -> list[str]:
    """Findet Stellen wie ``import os``, ``open(…)`` oder ``x.__class__``, jeweils mit Zeilennummer.

    ponytail: Sperrliste, keine Sandbox - fängt Unfug und naive Angriffe ab; die Lehrkraft liest trotzdem mit.
    Die erlaubten Bibliotheken können selbst Dateien lesen und schreiben (``read_csv``, ``to_csv``, SQL ``COPY``).

    Testen: ``import os`` → Treffer; ``import pandas as pd`` → kein Treffer; ``x.__class__`` → Treffer;
    ``if __name__ == "__main__"`` → kein Treffer; ``for _ in range(3)`` → kein Treffer; Syntaxfehler → Treffer.
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


def pruefe_aufgabe(vorher: Path, nachher: Path, dateiname: str) -> list[str]:
    """Prüft Vorlage und Tests einer Aufgabe im Stand mit Pull Request; liefert die Probleme (leer = in Ordnung).

    Den ``vorlage-hash``, das Thema und den Inhalt prüft es nur bei neuen Aufgaben. Änderungen an bestehenden Aufgaben übernimmt
    die Lehrkraft in ihre Musterdatei und erzeugt beide Dateien neu.
    """
    vorlage = nachher / "aufgaben" / dateiname
    testdatei = nachher / "tests" / dateiname
    loesung = nachher / "loesungen" / dateiname
    fehlende = _fehlende_dateien(nachher, [vorlage, testdatei])
    if fehlende:
        return fehlende
    verbotene = _verbotene_stellen(nachher, [datei for datei in (vorlage, testdatei, loesung) if datei.is_file()])
    if verbotene:
        return verbotene  # solchen Code gar nicht erst ausführen
    ist_neu = not (vorher / "tests" / dateiname).is_file()
    kopf = _pruefe_kopf_neuer_aufgabe(vorlage, testdatei) if ist_neu else []
    if kopf:
        return kopf
    leere_vorlage = _pruefe_leere_vorlage(vorlage, testdatei)
    if leere_vorlage or not loesung.is_file():
        return leere_vorlage
    return _pruefe_beigelegte_loesung(loesung, testdatei)


def _pruefe_kopf_neuer_aufgabe(vorlage: Path, testdatei: Path) -> list[str]:
    """Prüft den Kopf der Testdatei: ``vorlage-hash`` passt, Thema ist bekannt, Inhalt ist nicht leer.

    Testen: falscher Hash → nur dieser Hinweis; ohne ``# thema:`` oder mit unbekanntem Thema → Hinweis
    mit den erlaubten Themen; leerer Inhalt → Hinweis.
    """
    if not entspricht_vorlage(vorlage, testdatei):
        return ["Vorlage und Tests passen nicht zusammen. Erzeugen Sie beide neu und laden Sie beide hoch."]
    hinweise: list[str] = []
    if lies_thema(testdatei) not in THEMEN:
        hinweise.append(
            "Im Kopf der Testdatei fehlt ein bekanntes Thema. Tragen Sie in Ihrer Musterdatei "
            f"„# Thema: …“ ein ({', '.join(THEMEN)}) und erzeugen Sie beide Dateien neu."
        )
    if not lies_inhalt(testdatei):
        hinweise.append(
            "Im Kopf der Testdatei fehlt der Inhalt. Tragen Sie in Ihrer Musterdatei „# Inhalt: …“ "
            "mit einer Kurzbeschreibung ein und erzeugen Sie beide Dateien neu."
        )
    return hinweise


def _fehlende_dateien(nachher: Path, dateien: list[Path]) -> list[str]:
    """Liefert für jede Datei, die es nicht gibt, einen Hinweis."""
    hinweise: list[str] = []
    for datei in dateien:
        if not datei.is_file():
            hinweise.append(f"{datei.relative_to(nachher).as_posix()} fehlt - laden Sie immer beide Dateien hoch.")
    return hinweise


def _verbotene_stellen(nachher: Path, dateien: list[Path]) -> list[str]:
    """Liefert alle bedenklichen Stellen der Dateien, jeweils mit Dateiname."""
    hinweise: list[str] = []
    for datei in dateien:
        for stelle in bedenkliche_stellen(datei.read_text(encoding="utf-8-sig")):
            hinweise.append(f"{datei.relative_to(nachher).as_posix()}, {stelle} - ist nicht erlaubt.")
    return hinweise


def _pruefe_leere_vorlage(vorlage: Path, testdatei: Path) -> list[str]:
    """Führt die Tests mit der leeren Vorlage aus; sie sollen laufen, aber nicht bestehen."""
    auswertung = pruefe_loesung(vorlage, testdatei)
    if auswertung.abgebrochen:
        return [f"Die Prüfung der leeren Vorlage wurde abgebrochen: {auswertung.programmfehler or 'Zeitlimit'}"]
    if not auswertung.tests:
        return ["Die Testdatei enthält keine Tests."]
    if auswertung.bestanden:
        return ["Schon die leere Vorlage besteht alle Tests - die Tests prüfen zu wenig."]
    return []


def _pruefe_beigelegte_loesung(loesung: Path, testdatei: Path) -> list[str]:
    """Führt die Tests mit der Lösung aus ``loesungen/`` aus; sie soll alle bestehen."""
    if pruefe_loesung(loesung, testdatei).bestanden:
        return []
    hinweis = (
        f"loesungen/{loesung.name} besteht die Tests nicht. Erzeugen Sie die Dateien neu mit erstelle_aufgaben.py "
        "und prüfen Sie Ihre Musterlösung."
    )
    return [hinweis]


def _unerlaubte_dateien(geaendert: list[str]) -> list[str]:
    """Liefert die geänderten Pfade, die eine Einreichung nicht ändern darf."""
    return [pfad for pfad in geaendert if not _ist_erlaubt(pfad)]


def _ist_erlaubt(pfad: str) -> bool:
    """``True``, wenn eine Einreichung die Datei ``pfad`` ändern darf."""
    if pfad.startswith("loesungen/") and pfad.removeprefix("loesungen/").split("_", 1)[0] in PRIVATE_STUFEN:
        return False
    return bool(AUFGABEN_DATEIEN.fullmatch(pfad) or WEITERE_ERLAUBTE_DATEIEN.fullmatch(pfad))


def _eingereichte_aufgaben(geaendert: list[str]) -> list[str]:
    """Liefert die Dateinamen der Aufgaben, deren Vorlage oder Tests geändert sind, sortiert und ohne Doppelte."""
    aufgaben = {Path(pfad).name for pfad in geaendert if AUFGABEN_DATEIEN.fullmatch(pfad)}
    return sorted(aufgaben)


def _melde_aufgabe(vorher: Path, nachher: Path, dateiname: str) -> bool:
    """Gibt das Ergebnis für eine Aufgabe aus; ``True``, wenn nichts aufgefallen ist."""
    probleme = pruefe_aufgabe(vorher, nachher, dateiname)
    print(f"{'✗' if probleme else '✓'} {Path(dateiname).stem}")
    for problem in probleme:
        print(f"    {problem}")
    return not probleme


def main(argumente: list[str]) -> int:
    """Einstiegspunkt. Exit-Code 1, wenn etwas auffällt (GitHub zeigt dann ✗ am Pull Request).

    Testen: nichts geändert → 0; gültige neue Aufgabe → 0; andere Datei geändert → 1;
    ``import`` in den Tests → 1, ohne sie auszuführen; leere Vorlage besteht → 1; falscher vorlage-hash → 1;
    Aufgabentext einer bestehenden Aufgabe von Hand geändert → 0.
    """
    if len(argumente) != 2:
        print(__doc__)
        return 2
    vorher, nachher = Path(argumente[0]), Path(argumente[1])
    geaendert = geaenderte_dateien(vorher, nachher)

    unerlaubt = _unerlaubte_dateien(geaendert)
    for pfad in unerlaubt:
        print(f"✗ {pfad}: Diese Datei darf eine Einreichung nicht ändern.")
    ergebnisse = [_melde_aufgabe(vorher, nachher, dateiname) for dateiname in _eingereichte_aufgaben(geaendert)]
    alles_ok = not unerlaubt and all(ergebnisse)

    if alles_ok:
        print("→ Keine Auffälligkeiten. Aufgabentext und Tests trotzdem ansehen.")
    return 0 if alles_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
