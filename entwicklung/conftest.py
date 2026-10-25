"""Gemeinsame Fixtures und Hilfsfunktionen für die Tests von pruefe.py und erstelle_aufgaben.py.

Aufruf im Projektordner:
    python3 -m pytest entwicklung

test_varianten.py spielt für drei Aufgaben je fünf Lösungen durch, wie SuS sie abgeben könnten.
test_pruefe.py testet die Bausteine von pruefe.py, test_erstelle_aufgaben.py das Erzeugen der
Vorlagen und Tests, test_einreichung.py die Prüfung von Pull Requests.
GitHub führt sie bei jedem Pull Request aus (.github/workflows/entwicklung.yml). Dort fehlt der private
Ordner lehrkraft/; Tests, die die Musterdateien brauchen, werden dann übersprungen.
"""

from __future__ import annotations

import sys
import textwrap
from collections.abc import Callable
from pathlib import Path

import pytest

PROJEKT = Path(__file__).resolve().parent.parent
# pruefe.py und erstelle_aufgaben.py liegen eine Ebene höher und sind kein Paket.
sys.path.insert(0, str(PROJEKT))

import pruefe  # erst nach dem Erweitern von sys.path importierbar
from erstelle_aufgaben import PLATZHALTER

AUFGABEN = PROJEKT / "aufgaben"
TESTS = PROJEKT / "tests"
MUSTER = PROJEKT / "lehrkraft" / "muster"
# Für _mit_zeitlimit direkt im Testprozess: schlafend statt rechnend, damit der weiterlaufende
# Faden die übrigen Tests nicht bremst. (pruefe_loesung beendet seinen Prozess selbst.)
ENDLOS = "import time\nwhile True:\n    time.sleep(0.1)\n"

Schreibe = Callable[..., Path]
PruefeProgramm = Callable[[str, str], pruefe.Auswertung]
Main = Callable[..., "tuple[int, str]"]
KopiereVorlagen = Callable[..., Path]


def bearbeite_vorlage(aufgabe: str, code: str) -> str:
    """Ersetzt in der echten Vorlage die Platzhalterzeile durch ``code`` - so wie SuS es tun."""
    vorlage = (AUFGABEN / f"{aufgabe}.py").read_text(encoding="utf-8")
    platzhalter = next(z for z in vorlage.splitlines() if z.strip() == PLATZHALTER)
    einrueckung = platzhalter[: len(platzhalter) - len(platzhalter.lstrip())]
    return vorlage.replace(platzhalter, textwrap.indent(textwrap.dedent(code).strip("\n"), einrueckung))


def symbole(auswertung: pruefe.Auswertung) -> str:
    """Kurzform der Ergebnisse, z. B. ``"✓✗"``."""
    return "".join("✓" if t.meldung is None else "✗" for t in auswertung.tests)


@pytest.fixture
def schreibe(tmp_path: Path) -> Schreibe:
    """Liefert eine Funktion, die eine Datei im leeren Testordner ``tmp_path`` anlegt."""

    def schreibe_datei(name: str, text: str, encoding: str = "utf-8") -> Path:
        """Schreibt ``text`` nach ``tmp_path / name`` und legt fehlende Ordner an."""
        pfad = tmp_path / name
        pfad.parent.mkdir(parents=True, exist_ok=True)
        pfad.write_text(text, encoding=encoding)
        return pfad

    return schreibe_datei


@pytest.fixture
def pruefe_programm(schreibe: Schreibe) -> PruefeProgramm:
    """Liefert eine Funktion, die ein kleines Programm gegen einen kleinen Testtext prüft."""

    def pruefe_text(programm: str, tests: str) -> pruefe.Auswertung:
        """Schreibt Programm und Tests in Dateien und prüft sie mit ``pruefe_loesung``."""
        return pruefe.pruefe_loesung(schreibe("loesung.py", programm), schreibe("tests.py", tests))

    return pruefe_text


@pytest.fixture
def kurzes_zeitlimit(monkeypatch: pytest.MonkeyPatch) -> None:
    """Endlosschleifen laufen als Hintergrund-Faden weiter; ein kurzes Limit hält die Tests schnell."""
    monkeypatch.setattr(pruefe, "ZEITLIMIT_SEKUNDEN", 0.5)


@pytest.fixture
def main(capsys: pytest.CaptureFixture[str]) -> Main:
    """Liefert eine Funktion, die ``pruefe.main`` aufruft."""

    def rufe_main_auf(*argumente: str) -> tuple[int, str]:
        """Ruft ``pruefe.main`` auf und liefert Exit-Code und Bildschirmausgabe."""
        code = pruefe.main(list(argumente))
        return code, capsys.readouterr().out

    return rufe_main_auf


@pytest.fixture
def kopiere_vorlagen(schreibe: Schreibe, tmp_path: Path) -> KopiereVorlagen:
    """Liefert eine Funktion, die unveränderte Kopien aller Vorlagen in ``tmp_path/aufgaben`` anlegt."""

    def kopiere(zeilenende: str = "\n", encoding: str = "utf-8") -> Path:
        """Kopiert die Vorlagen mit dem gewünschten Zeilenende und Encoding; liefert den Zielordner."""
        for vorlage in AUFGABEN.glob("*.py"):
            text = vorlage.read_text(encoding="utf-8").replace("\n", zeilenende)
            schreibe(f"aufgaben/{vorlage.name}", text, encoding=encoding)
        return tmp_path / "aufgaben"

    return kopiere
