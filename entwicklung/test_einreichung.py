"""Prüfen eingereichter Aufgaben (Pull Requests) mit .github/pruefe_einreichung.py."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest
from conftest import PROJEKT

import pruefe

# pruefe_einreichung.py liegt in .github/ und ist kein Paket.
sys.path.insert(0, str(PROJEKT / ".github"))

import pruefe_einreichung  # erst nach dem Erweitern von sys.path importierbar

VORLAGE = "zahl = 0\n"
TESTS = "# zahl stimmt\nassert zahl == 3, 'zahl soll 3 sein'\n"
THEMA_UND_INHALT = "# thema: texte_zahlen\n# inhalt: Zahl festlegen\n"


@pytest.fixture
def vorher(tmp_path: Path) -> Path:
    """Stand vor dem Pull Request: Kopie von aufgaben/, tests/ und README.md."""
    shutil.copytree(PROJEKT / "aufgaben", tmp_path / "vorher" / "aufgaben")
    shutil.copytree(PROJEKT / "tests", tmp_path / "vorher" / "tests")
    shutil.copy(PROJEKT / "README.md", tmp_path / "vorher")
    return tmp_path / "vorher"


@pytest.fixture
def nachher(vorher: Path) -> Path:
    """Stand mit Pull Request: zunächst eine genaue Kopie von ``vorher``."""
    return Path(shutil.copytree(vorher, vorher.parent / "nachher"))


def reiche_ein(
    nachher: Path, vorlage: str, tests: str, vorlage_hash: str | None = None, thema_und_inhalt: str = THEMA_UND_INHALT
) -> None:
    """Legt Aufgabe 2_099_neu an, mit passendem ``vorlage-hash``, wenn keiner vorgegeben ist."""
    kopf = f"# vorlage-hash: {vorlage_hash or pruefe.vorlage_hash(vorlage)}\n{thema_und_inhalt}\n"
    (nachher / "aufgaben" / "2_099_neu.py").write_text(vorlage, encoding="utf-8")
    (nachher / "tests" / "2_099_neu.py").write_text(kopf + tests, encoding="utf-8")


def pruefe_pr(vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str]) -> tuple[int, str]:
    """Ruft ``main`` auf und liefert Exit-Code und Bildschirmausgabe."""
    code = pruefe_einreichung.main([str(vorher), str(nachher)])
    return code, capsys.readouterr().out


@pytest.mark.parametrize(
    ("code", "bedenklich"),
    [
        ("import os", True),
        ("from os import system", True),
        ("import os, pandas", True),
        ("from . import pruefe", True),
        ("import pandas as pd", False),
        ("from numpy.linalg import norm", False),
        ("from numpy import _utils", True),
        ("open('x')", True),
        ("x = ().__class__", True),
        ("g = (i for i in []).gi_frame", True),
        ("def f(", True),
        ("if __name__ == '__main__':\n    pass", False),
        ("for _ in range(3):\n    print(_)", False),
    ],
)
def test_bedenkliche_stellen(code: str, bedenklich: bool) -> None:
    """Sperrliste erkennt import, open, __…__ und Frame-Zugriffe, lässt normalen Code und die Bibliotheken durch."""
    assert bool(pruefe_einreichung.bedenkliche_stellen(code)) == bedenklich


def test_unveraendert(vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Ohne Änderung gibt es nichts zu beanstanden."""
    assert pruefe_pr(vorher, nachher, capsys)[0] == 0


def test_gueltige_aufgabe(vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Neue Aufgabe mit passenden Tests und README-Änderung → ✓."""
    reiche_ein(nachher, VORLAGE, TESTS)
    (nachher / "README.md").write_text("geändert", encoding="utf-8")
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 0, ausgabe
    assert "✓ 2_099_neu" in ausgabe


@pytest.mark.parametrize("pfad", ["pruefe.py", "erstelle_aufgaben.py", "entwicklung/test_neu.py"])
def test_werkzeug_datei(vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str], pfad: str) -> None:
    """Änderungen an den Werkzeugen sind erlaubt; die prüft entwicklung.yml."""
    (nachher / pfad).parent.mkdir(parents=True, exist_ok=True)
    (nachher / pfad).write_text("x = 1\n", encoding="utf-8")
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 0, ausgabe


@pytest.mark.parametrize(
    "pfad",
    [".github/pruefe_einreichung.py", ".github/workflows/x.yml", "aufgaben/unter/07.py", "tests/07.txt", "x.py"],
)
def test_andere_datei(vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str], pfad: str) -> None:
    """Änderungen außerhalb von Aufgaben, README.md und Werkzeugen → ✗."""
    (nachher / pfad).parent.mkdir(parents=True, exist_ok=True)
    (nachher / pfad).write_text("x = 1\n", encoding="utf-8")
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 1
    assert pfad in ausgabe


def test_geloeschte_testdatei(vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Fehlt die Testdatei zu einer Aufgabe → ✗."""
    (nachher / "tests" / "1_001_hallo_welt.py").unlink()
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 1
    assert "tests/1_001_hallo_welt.py fehlt" in ausgabe


def test_import_wird_nicht_ausgefuehrt(
    vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    """Bedenklicher Code → ✗, und er läuft gar nicht erst."""
    spur = tmp_path / "ausgefuehrt"
    reiche_ein(nachher, VORLAGE, f"import pathlib\npathlib.Path({str(spur)!r}).touch()\n" + TESTS)
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 1
    assert "import pathlib" in ausgabe
    assert not spur.exists()


@pytest.mark.parametrize(
    ("loesung", "code_erwartet", "meldung"),
    [
        ("zahl = 3\n", 0, "✓ 2_099_neu"),
        ("zahl = 4\n", 1, "loesungen/2_099_neu.py besteht die Tests nicht"),
        ("import os\nzahl = 3\n", 1, "loesungen/2_099_neu.py, Zeile 1: import os"),
    ],
)
def test_beigelegte_loesung(
    vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str], loesung: str, code_erwartet: int, meldung: str
) -> None:
    """Eine Lösung in loesungen/ ist freiwillig; liegt sie bei, gilt die Sperrliste, und sie besteht die Tests."""
    reiche_ein(nachher, VORLAGE, TESTS)
    (nachher / "loesungen").mkdir()
    (nachher / "loesungen" / "2_099_neu.py").write_text(loesung, encoding="utf-8")
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == code_erwartet, ausgabe
    assert meldung in ausgabe


def test_private_loesung_abgelehnt(vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Lösungen der Stufen 4 und 5 bleiben privat, auch wenn sie die Tests bestehen."""
    (nachher / "loesungen").mkdir()
    (nachher / "loesungen" / "4_001_konto.py").write_text("zahl = 3\n", encoding="utf-8")
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 1
    assert "✗ loesungen/4_001_konto.py: Diese Datei darf eine Einreichung nicht ändern." in ausgabe


def test_leere_vorlage_besteht(vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Tests, die schon die Vorlage besteht → ✗."""
    reiche_ein(nachher, VORLAGE, "assert zahl == 0\n")
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 1
    assert "prüfen zu wenig" in ausgabe


def test_falscher_vorlage_hash(vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Vorlage und Tests aus verschiedenen Läufen → ✗."""
    reiche_ein(nachher, VORLAGE, TESTS, vorlage_hash="0000000000000000")
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 1
    assert "passen nicht zusammen" in ausgabe


@pytest.mark.parametrize(
    ("thema_und_inhalt", "meldung"),
    [
        ("# inhalt: Zahl festlegen\n", "fehlt ein bekanntes Thema"),
        ("# thema: schleifen\n# inhalt: Zahl festlegen\n", "fehlt ein bekanntes Thema"),
        ("# thema: texte_zahlen\n", "fehlt der Inhalt"),
        ("# thema: texte_zahlen\n# inhalt:\n", "fehlt der Inhalt"),
    ],
)
def test_thema_oder_inhalt_fehlt(
    vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str], thema_und_inhalt: str, meldung: str
) -> None:
    """Neue Aufgabe ohne bekanntes Thema oder ohne Inhalt → ✗ mit Hinweis."""
    reiche_ein(nachher, VORLAGE, TESTS, thema_und_inhalt=thema_und_inhalt)
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 1
    assert meldung in ausgabe


def test_bestehende_aufgabe_von_hand_geaendert(vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Aufgabentext und Tests einer bestehenden Aufgabe im Browser geändert → ✓ trotz altem vorlage-hash."""
    vorlage = nachher / "aufgaben" / "1_003_rechteck.py"
    vorlage.write_text("# Tippfehler korrigiert\n" + vorlage.read_text(encoding="utf-8"), encoding="utf-8")
    testdatei = nachher / "tests" / "1_003_rechteck.py"
    testdatei.write_text(testdatei.read_text(encoding="utf-8") + "\nassert hoehe == 3\n", encoding="utf-8")
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 0, ausgabe
    assert "✓ 1_003_rechteck" in ausgabe


def test_bestehende_aufgabe_leere_vorlage_besteht(
    vorher: Path, nachher: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Auch bei bestehenden Aufgaben: Tests, die schon die Vorlage besteht → ✗."""
    (nachher / "tests" / "1_003_rechteck.py").write_text('EINGABEN = ["4", "3"]\nassert hoehe == 3\n', encoding="utf-8")
    code, ausgabe = pruefe_pr(vorher, nachher, capsys)
    assert code == 1
    assert "prüfen zu wenig" in ausgabe
