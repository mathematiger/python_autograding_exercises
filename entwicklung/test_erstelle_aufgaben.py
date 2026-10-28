"""Erzeugen der Vorlagen und Tests mit erstelle_aufgaben.py."""

from __future__ import annotations

import ast
import textwrap
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import AUFGABEN, MUSTER, TESTS, Schreibe

import erstelle_aufgaben
import pruefe
from erstelle_aufgaben import PLATZHALTER, Zerlegt, zerlege

MUSTERDATEI = textwrap.dedent(
    '''\
    """Aufgabe 99 – Test"""

    zahl = 3

    ### BEGIN SOLUTION
    quadrat = zahl * zahl
    ### END SOLUTION


    def doppelt(x):
        ### BEGIN SOLUTION ###
        return 2 * x
        ### END SOLUTION ###


    ### BEGIN TESTS
    # quadrat stimmt
    assert quadrat == 9
    ### END TESTS

    ### BEGIN HIDDEN TESTS
    # doppelt stimmt
    assert doppelt(2) == 4
    ### END HIDDEN TESTS
    '''
)
MUSTERDATEIEN = sorted(MUSTER.glob("*.py"))
VORLAGEN = sorted(AUFGABEN.glob("*.py"))

Erstelle = Callable[[str], "tuple[bool, str]"]


class TestZerlege:
    @pytest.fixture
    def teile(self) -> Zerlegt:
        """Die zerlegte Beispiel-Musterdatei."""
        return zerlege(MUSTERDATEI, "99_test.py")

    def test_vorlage(self, teile: Zerlegt) -> None:
        assert teile.vorlage == (
            f'"""Aufgabe 99 – Test"""\n\nzahl = 3\n\n{PLATZHALTER}\n\n\ndef doppelt(x):\n    {PLATZHALTER}\n'
        )
        compile(teile.vorlage, "vorlage", "exec")

    def test_loesung_ohne_marker_und_tests(self, teile: Zerlegt) -> None:
        assert "###" not in teile.loesung
        assert "assert" not in teile.loesung
        assert "quadrat = zahl * zahl" in teile.loesung
        assert "    return 2 * x" in teile.loesung

    def test_loesung_behaelt_zeilennummern(self, teile: Zerlegt) -> None:
        assert teile.loesungszeilen == {6, 12}
        zeilen = teile.loesung.splitlines()
        assert zeilen[5] == "quadrat = zahl * zahl"
        assert zeilen[11] == "    return 2 * x"

    def test_tests_inklusive_hidden(self, teile: Zerlegt) -> None:
        assert teile.tests == "# quadrat stimmt\nassert quadrat == 9\n# doppelt stimmt\nassert doppelt(2) == 4\n"

    def test_eingerueckte_tests_werden_ausgerueckt(self) -> None:
        teile = zerlege("if True:\n    ### BEGIN TESTS\n    assert 1\n    ### END TESTS\n", "x.py")
        assert teile.tests == "assert 1\n"

    @pytest.mark.parametrize(
        ("text", "meldung"),
        [
            ("### END SOLUTION\n", "Zeile 1: END SOLUTION ohne passendes BEGIN"),
            ("### BEGIN SOLUTION\nx = 1\n", "nie mit END geschlossen"),
            ("### BEGIN SOLUTION\n### BEGIN TESTS\n", "Zeile 2: BEGIN TESTS, obwohl SOLUTION noch offen ist"),
            ("### BEGIN TESTS\n### END SOLUTION\n", "Zeile 2: END SOLUTION ohne passendes BEGIN"),
        ],
    )
    def test_fehlerhafte_marker(self, text: str, meldung: str) -> None:
        with pytest.raises(ValueError) as fehler:
            zerlege(text, "kaputt.py")
        assert "kaputt.py" in str(fehler.value)
        assert meldung in str(fehler.value)

    def test_marker_mitten_in_zeile_ist_kein_marker(self) -> None:
        teile = zerlege("x = 1  ### BEGIN SOLUTION\n", "x.py")
        assert teile.vorlage == "x = 1  ### BEGIN SOLUTION\n"


class TestErstelle:
    @pytest.fixture
    def erstelle(
        self,
        schreibe: Schreibe,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> Erstelle:
        """Liefert eine Funktion, die eine Musterdatei in ``tmp_path`` übersetzt."""

        def erstelle_aus(muster: str) -> tuple[bool, str]:
            """Erzeugt Vorlage und Tests aus ``muster``; liefert Erfolg und Bildschirmausgabe."""
            schreibe("eigene_aufgaben/99_test.py", muster)
            for ordner in ("aufgaben", "tests"):
                (tmp_path / ordner).mkdir(exist_ok=True)
            monkeypatch.setattr(erstelle_aufgaben, "PROJEKT", tmp_path)
            ok = erstelle_aufgaben.erstelle(tmp_path / "eigene_aufgaben", tmp_path / "aufgaben", tmp_path / "tests")
            return ok, capsys.readouterr().out

        return erstelle_aus

    def test_gute_musterdatei(self, erstelle: Erstelle, tmp_path: Path) -> None:
        ok, ausgabe = erstelle(MUSTERDATEI)
        assert ok, ausgabe
        assert ausgabe == "✓ 99_test.py (2 Tests, 5 von 5 Änderungen bemerkt)\n"
        vorlage = (tmp_path / "aufgaben" / "99_test.py").read_text(encoding="utf-8")
        tests = (tmp_path / "tests" / "99_test.py").read_text(encoding="utf-8")
        assert vorlage == zerlege(MUSTERDATEI, "").vorlage
        assert tests.splitlines()[:3] == [
            "# Automatisch erzeugt aus eigene_aufgaben/99_test.py - nicht von Hand ändern.",
            f"# vorlage-hash: {pruefe.vorlage_hash(vorlage)}",
            "",
        ]
        assert "zahl * zahl" not in tests
        assert "assert" not in vorlage
        # der Name der Testzeile ist nicht der Kopf der Testdatei
        assert pruefe.lade_tests(tmp_path / "tests" / "99_test.py").schritte[0].name == "quadrat stimmt"

    def test_musterloesung_falsch(self, erstelle: Erstelle) -> None:
        ok, ausgabe = erstelle(MUSTERDATEI.replace("assert quadrat == 9", "assert quadrat == 10"))
        assert not ok
        assert "Die Musterlösung besteht ihre Tests nicht" in ausgabe
        assert "✗ quadrat stimmt" in ausgabe

    def test_tests_pruefen_zu_wenig(self, erstelle: Erstelle) -> None:
        schwach = "x = 1\n### BEGIN SOLUTION\ny = 2\n### END SOLUTION\n### BEGIN TESTS\nassert x == 1\n### END TESTS\n"
        ok, ausgabe = erstelle(schwach)
        assert not ok
        assert "Schon die leere Vorlage besteht alle Tests" in ausgabe

    def test_unbemerkte_aenderung_ist_nur_warnung(self, erstelle: Erstelle) -> None:
        ok, ausgabe = erstelle(MUSTERDATEI.replace("assert doppelt(2) == 4", "assert doppelt(0) == 0"))
        assert ok, ausgabe
        assert "(2 Tests, 4 von 5 Änderungen bemerkt)" in ausgabe
        assert "    ⚠ Kein Test bemerkt: Zeile 12: 2  →  3\n" in ausgabe

    def test_aufgabe_schon_in_git(self, erstelle: Erstelle, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(erstelle_aufgaben, "_bekannte_testdateien", lambda ordner: {"99_test.py"})
        ok, ausgabe = erstelle(MUSTERDATEI)
        assert ok
        assert ausgabe == "✓ 99_test.py (2 Tests)\n"


@pytest.mark.skipif(not MUSTER.is_dir(), reason="lehrkraft/muster fehlt")
class TestGenerierteDateien:
    """Die Dateien im Repo passen zu den Musterdateien und funktionieren."""

    def test_aufgaben_und_tests_gehoeren_zusammen(self) -> None:
        assert sorted(p.name for p in AUFGABEN.glob("*.py")) == sorted(p.name for p in TESTS.glob("*.py"))

    @pytest.mark.parametrize("muster", MUSTERDATEIEN, ids=lambda p: p.name)
    def test_aktuell_erzeugt(self, muster: Path) -> None:
        teile = zerlege(muster.read_text(encoding="utf-8"), muster.name)
        assert (AUFGABEN / muster.name).read_text(encoding="utf-8") == teile.vorlage
        tests = (TESTS / muster.name).read_text(encoding="utf-8")
        assert tests.endswith("\n\n" + teile.tests), "Tests veraltet - erstelle_aufgaben.py starten"

    @pytest.mark.parametrize("muster", MUSTERDATEIEN, ids=lambda p: p.name)
    def test_musterloesung_besteht_vorlage_nicht(self, muster: Path, schreibe: Schreibe) -> None:
        loesung = schreibe(muster.name, zerlege(muster.read_text(encoding="utf-8"), muster.name).loesung)
        assert pruefe.pruefe_loesung(loesung, TESTS / muster.name).bestanden
        assert not pruefe.pruefe_loesung(AUFGABEN / muster.name, TESTS / muster.name).bestanden

    @pytest.mark.parametrize("vorlage", VORLAGEN, ids=lambda p: p.name)
    def test_vorlagen(self, vorlage: Path) -> None:
        text = vorlage.read_text(encoding="utf-8")
        baum = ast.parse(text, vorlage.name)
        assert PLATZHALTER in text
        assert "###" not in text
        # per AST statt Textsuche, weil Aufgaben über assert das Wort im Aufgabentext nennen
        assert not any(isinstance(knoten, ast.Assert) for knoten in ast.walk(baum))
        assert pruefe.lies_vorlage_hash(TESTS / vorlage.name) == pruefe.vorlage_hash(text)
