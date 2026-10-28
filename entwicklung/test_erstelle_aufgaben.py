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

KOPF = "# Thema: kontrollfluss\n# Inhalt: Quadrat und Verdoppeln\n"
MUSTERDATEI = KOPF + textwrap.dedent(
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
        assert teile.loesungszeilen == {8, 14}
        zeilen = teile.loesung.splitlines()
        assert zeilen[7] == "quadrat = zahl * zahl"
        assert zeilen[13] == "    return 2 * x"

    def test_tests_inklusive_hidden(self, teile: Zerlegt) -> None:
        assert teile.tests == "# quadrat stimmt\nassert quadrat == 9\n# doppelt stimmt\nassert doppelt(2) == 4\n"

    def test_eingerueckte_tests_werden_ausgerueckt(self) -> None:
        teile = zerlege(KOPF + "if True:\n    ### BEGIN TESTS\n    assert 1\n    ### END TESTS\n", "x.py")
        assert teile.tests == "assert 1\n"

    @pytest.mark.parametrize(
        ("text", "meldung"),
        [
            ("### END SOLUTION\n", "Zeile 3: END SOLUTION ohne passendes BEGIN"),
            ("### BEGIN SOLUTION\nx = 1\n", "nie mit END geschlossen"),
            ("### BEGIN SOLUTION\n### BEGIN TESTS\n", "Zeile 4: BEGIN TESTS, obwohl SOLUTION noch offen ist"),
            ("### BEGIN TESTS\n### END SOLUTION\n", "Zeile 4: END SOLUTION ohne passendes BEGIN"),
        ],
    )
    def test_fehlerhafte_marker(self, text: str, meldung: str) -> None:
        with pytest.raises(ValueError) as fehler:
            zerlege(KOPF + text, "kaputt.py")
        assert "kaputt.py" in str(fehler.value)
        assert meldung in str(fehler.value)

    def test_kopfzeilen(self, teile: Zerlegt) -> None:
        assert (teile.thema, teile.inhalt) == ("kontrollfluss", "Quadrat und Verdoppeln")
        assert "Thema" not in teile.vorlage
        assert "Thema" not in teile.loesung

    def test_kopfzeilen_aendern_vorlage_hash_nicht(self, teile: Zerlegt) -> None:
        anderer_kopf = MUSTERDATEI.replace(KOPF, "# Thema: funktionen\n# Inhalt: etwas anderes\n")
        assert pruefe.vorlage_hash(zerlege(anderer_kopf, "x.py").vorlage) == pruefe.vorlage_hash(teile.vorlage)

    @pytest.mark.parametrize(
        ("kopf", "meldung"),
        [
            ("# Inhalt: x\n", "Am Anfang fehlt die Zeile „# Thema: …“. Erlaubte Themen: texte_zahlen, "),
            ("# Thema: schleifen\n# Inhalt: x\n", "Unbekanntes Thema „schleifen“. Erlaubte Themen: texte_zahlen, "),
            ('"""Text"""\n# Thema: funktionen\n# Inhalt: x\n', "Am Anfang fehlt die Zeile „# Thema: …“"),
            ("# Thema: funktionen\n", "Am Anfang fehlt die Zeile „# Inhalt: …“"),
            ("# Thema: funktionen\n# Inhalt:   \n", "Am Anfang fehlt die Zeile „# Inhalt: …“"),
        ],
    )
    def test_fehlerhafte_kopfzeilen(self, kopf: str, meldung: str) -> None:
        with pytest.raises(ValueError) as fehler:
            zerlege(kopf + "x = 1\n", "kaputt.py")
        assert str(fehler.value).startswith(f"kaputt.py: {meldung}")

    def test_marker_mitten_in_zeile_ist_kein_marker(self) -> None:
        teile = zerlege(KOPF + "x = 1  ### BEGIN SOLUTION\n", "x.py")
        assert teile.vorlage == "x = 1  ### BEGIN SOLUTION\n"

    def test_loesungsdatei(self, teile: Zerlegt) -> None:
        """Lösung zum Lesen: ohne Kopfzeilen, Marker und Tests, ohne die Leerzeilen dafür."""
        assert teile.loesungsdatei == (
            '"""Aufgabe 99 – Test"""\n\nzahl = 3\n\nquadrat = zahl * zahl\n\n\ndef doppelt(x):\n    return 2 * x\n'
        )

    def test_loesungsweg_nur_in_loesungsdatei(self) -> None:
        teile = zerlege(KOPF + "x = 1\n### BEGIN LOESUNGSWEG\n# Geht auch in O(1).\n\n### END LOESUNGSWEG\n", "x.py")
        assert teile.loesungsdatei == "x = 1\n# Geht auch in O(1).\n"
        assert teile.vorlage == "x = 1\n"
        assert not teile.loesungszeilen

    def test_loesungsweg_nur_mit_kommentaren(self) -> None:
        with pytest.raises(ValueError, match=r"x\.py, Zeile 5: Im LOESUNGSWEG sind nur Kommentarzeilen"):
            zerlege(KOPF + "### BEGIN LOESUNGSWEG\n# gut\ny = 2\n### END LOESUNGSWEG\n", "x.py")


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
            ok = erstelle_aufgaben.erstelle(
                tmp_path / "eigene_aufgaben", tmp_path / "aufgaben", tmp_path / "tests", tmp_path / "loesungen"
            )
            return ok, capsys.readouterr().out

        return erstelle_aus

    def test_gute_musterdatei(self, erstelle: Erstelle, tmp_path: Path) -> None:
        ok, ausgabe = erstelle(MUSTERDATEI)
        assert ok, ausgabe
        assert ausgabe == "✓ 99_test.py (2 Tests, 5 von 5 Änderungen bemerkt)\n"
        vorlage = (tmp_path / "aufgaben" / "99_test.py").read_text(encoding="utf-8")
        tests = (tmp_path / "tests" / "99_test.py").read_text(encoding="utf-8")
        assert vorlage == zerlege(MUSTERDATEI, "").vorlage
        assert tests.splitlines()[:5] == [
            "# Automatisch erzeugt aus eigene_aufgaben/99_test.py - nicht von Hand ändern.",
            f"# vorlage-hash: {pruefe.vorlage_hash(vorlage)}",
            "# thema: kontrollfluss",
            "# inhalt: Quadrat und Verdoppeln",
            "",
        ]
        assert pruefe.lies_thema(tmp_path / "tests" / "99_test.py") == "kontrollfluss"
        assert "zahl * zahl" not in tests
        assert "assert" not in vorlage
        # der Name der Testzeile ist nicht der Kopf der Testdatei
        assert pruefe.lade_tests(tmp_path / "tests" / "99_test.py").schritte[0].name == "quadrat stimmt"
        loesung = tmp_path / "loesungen" / "99_test.py"
        assert loesung.read_text(encoding="utf-8").endswith("\n\n" + zerlege(MUSTERDATEI, "").loesungsdatei)
        assert pruefe.pruefe_loesung(loesung, tmp_path / "tests" / "99_test.py").bestanden

    def test_musterloesung_falsch(self, erstelle: Erstelle) -> None:
        ok, ausgabe = erstelle(MUSTERDATEI.replace("assert quadrat == 9", "assert quadrat == 10"))
        assert not ok
        assert "Die Musterlösung besteht ihre Tests nicht" in ausgabe
        assert "✗ quadrat stimmt" in ausgabe

    def test_tests_pruefen_zu_wenig(self, erstelle: Erstelle) -> None:
        schwach = (
            KOPF + "x = 1\n### BEGIN SOLUTION\ny = 2\n### END SOLUTION\n### BEGIN TESTS\nassert x == 1\n### END TESTS\n"
        )
        ok, ausgabe = erstelle(schwach)
        assert not ok
        assert "Schon die leere Vorlage besteht alle Tests" in ausgabe

    def test_unbemerkte_aenderung_ist_nur_warnung(self, erstelle: Erstelle) -> None:
        ok, ausgabe = erstelle(MUSTERDATEI.replace("assert doppelt(2) == 4", "assert doppelt(0) == 0"))
        assert ok, ausgabe
        assert "(2 Tests, 4 von 5 Änderungen bemerkt)" in ausgabe
        assert "    ⚠ Kein Test bemerkt: Zeile 14: 2  →  3\n" in ausgabe

    def test_aufgabe_schon_in_git(self, erstelle: Erstelle, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(erstelle_aufgaben, "_bekannte_testdateien", lambda ordner: {"99_test.py"})
        ok, ausgabe = erstelle(MUSTERDATEI)
        assert ok
        assert ausgabe == "✓ 99_test.py (2 Tests)\n"


class TestReadme:
    @pytest.fixture
    def testdateien(self, schreibe: Schreibe) -> list[Path]:
        """Drei Aufgaben: zwei zu Funktionen in Stufe 1 und 2, eine ohne Thema in Stufe 2."""
        return [
            schreibe("tests/1_001_a.py", "# thema: funktionen\n# inhalt: Erste\n"),
            schreibe("tests/2_001_b.py", "# thema: funktionen\n# inhalt: Zweite\n"),
            schreibe("tests/2_002_ohne.py", "# inhalt: Dritte\n"),
        ]

    def test_aufgabenlisten(self, testdateien: list[Path]) -> None:
        listen = erstelle_aufgaben.aufgabenlisten(testdateien)
        assert "| [Funktionen](#thema-funktionen) | 1 | 1 |  |  |  | `python pruefe.py funktionen` |" in listen
        assert "Texte, Zahlen" not in listen  # Thema ohne Aufgabe
        assert '<a name="thema-funktionen"></a>\n<details>\n<summary><b>Funktionen</b> (2 Aufgaben)</summary>' in listen
        assert "| [1_001_a](aufgaben/1_001_a.py) | ★☆☆☆☆ | Erste |" in listen
        assert "<summary><b>Stufe 1 ★☆☆☆☆: Erste Schritte mit vorgegebenem Code</b> (1 Aufgabe)</summary>" in listen
        assert "| [2_002_ohne](aufgaben/2_002_ohne.py) |  | Dritte |" in listen  # ohne Thema nur bei der Stufe
        assert listen.count("2_002_ohne") == 2  # Text und Ziel des Links, einmal
        assert "Stufe 3 ★" not in listen  # Stufe ohne Aufgabe

    def test_nur_zwischen_den_markern(self, schreibe: Schreibe, testdateien: list[Path], tmp_path: Path) -> None:
        anfang, ende = erstelle_aufgaben.README_ANFANG, erstelle_aufgaben.README_ENDE
        readme = schreibe("README.md", f"# Kopf\n\n{anfang}\nveraltete Liste\n{ende}\n\n## Rest\n")
        erstelle_aufgaben.aktualisiere_readme(readme, tmp_path / "tests")
        text = readme.read_text(encoding="utf-8")
        assert text.startswith(f"# Kopf\n\n{anfang}\n\n### Nach Thema\n")
        assert text.endswith(f"</details>\n\n{ende}\n\n## Rest\n")
        assert "veraltete Liste" not in text
        erstelle_aufgaben.aktualisiere_readme(readme, tmp_path / "tests")
        assert readme.read_text(encoding="utf-8") == text  # zweiter Lauf ändert nichts


@pytest.mark.skipif(not MUSTER.is_dir(), reason="lehrkraft/muster fehlt")
class TestGenerierteDateien:
    """Die Dateien im Repo passen zu den Musterdateien und funktionieren."""

    def test_aufgaben_und_tests_gehoeren_zusammen(self) -> None:
        assert sorted(p.name for p in AUFGABEN.glob("*.py")) == sorted(p.name for p in TESTS.glob("*.py"))

    def test_readme_aktuell(self) -> None:
        """Nur mit lehrkraft/: SuS reichen neue Aufgaben ohne README ein, die Lehrkraft erzeugt sie danach neu."""
        listen = erstelle_aufgaben.aufgabenlisten(sorted(TESTS.glob("*.py")))
        readme = (TESTS.parent / "README.md").read_text(encoding="utf-8")
        assert f"{erstelle_aufgaben.README_ANFANG}\n\n{listen}\n\n{erstelle_aufgaben.README_ENDE}" in readme, (
            "README veraltet - erstelle_aufgaben.py starten"
        )

    @pytest.mark.parametrize("muster", MUSTERDATEIEN, ids=lambda p: p.name)
    def test_aktuell_erzeugt(self, muster: Path) -> None:
        teile = zerlege(muster.read_text(encoding="utf-8"), muster.name)
        assert (AUFGABEN / muster.name).read_text(encoding="utf-8") == teile.vorlage
        tests = (TESTS / muster.name).read_text(encoding="utf-8")
        assert tests.endswith("\n\n" + teile.tests), "Tests veraltet - erstelle_aufgaben.py starten"
        loesung = (TESTS.parent / "loesungen" / muster.name).read_text(encoding="utf-8")
        assert loesung.endswith("\n\n" + teile.loesungsdatei), "Lösung veraltet - erstelle_aufgaben.py starten"
        assert pruefe.lies_thema(TESTS / muster.name) == teile.thema
        assert pruefe.lies_inhalt(TESTS / muster.name) == teile.inhalt

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
