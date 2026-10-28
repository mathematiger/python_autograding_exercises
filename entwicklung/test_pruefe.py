"""Bausteine von pruefe.py."""

from __future__ import annotations

import builtins
import multiprocessing
import re
import subprocess
import sys
import textwrap
import time
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import (
    ENDLOS,
    PROJEKT,
    TESTS,
    KopiereVorlagen,
    Main,
    PruefeProgramm,
    Schreibe,
    bearbeite_vorlage,
    symbole,
)

import pruefe

Starte = Callable[..., pruefe.Lauf]
mit_kurzem_zeitlimit = pytest.mark.usefixtures("kurzes_zeitlimit")


@pytest.mark.parametrize(
    ("text", "erwartet"),
    [
        ("a  \r\nb\n\n", "a\nb"),
        ("", ""),
        ("\n\nx", "\n\nx"),  # führende Leerzeilen bleiben
        ("a\t \rb", "a\nb"),
        ("  eingerückt", "  eingerückt"),
    ],
)
def test_normalisiere(text: str, erwartet: str) -> None:
    assert pruefe.normalisiere(text) == erwartet


class TestVorlageHash:
    def test_zeilenenden_egal(self) -> None:
        assert pruefe.vorlage_hash("a\nb\n") == pruefe.vorlage_hash("a\r\nb\r\n")

    def test_aenderung_gibt_anderen_hash(self) -> None:
        assert pruefe.vorlage_hash("pass\n") != pruefe.vorlage_hash("print(1)\n")

    def test_form(self) -> None:
        h = pruefe.vorlage_hash("x")
        assert len(h) == 16
        int(h, 16)


class TestZeitlimit:
    def test_rueckgabewert(self) -> None:
        assert pruefe._mit_zeitlimit(lambda: 42) == 42

    def test_fehler_wird_weitergereicht(self) -> None:
        with pytest.raises(ZeroDivisionError):
            pruefe._mit_zeitlimit(lambda: 1 / 0)

    def test_system_exit_wird_weitergereicht(self) -> None:
        with pytest.raises(SystemExit):
            pruefe._mit_zeitlimit(sys.exit)

    @mit_kurzem_zeitlimit
    def test_endlosschleife(self) -> None:
        with pytest.raises(pruefe.Endlosschleife):
            pruefe._mit_zeitlimit(lambda: exec(ENDLOS, {}))  # noqa: S102 - eigener Testcode, keine fremde Eingabe


class TestFehlertext:
    def test_syntaxfehler(self, pruefe_programm: PruefeProgramm) -> None:
        auswertung = pruefe_programm("x = 1\nprint(x\n", "assert True")
        assert (auswertung.programmfehler or "").startswith("Syntaxfehler in Zeile 2")

    def test_nameerror_mit_zeile_und_name(self, pruefe_programm: PruefeProgramm) -> None:
        auswertung = pruefe_programm("a = 1\nprint(b)\n", "assert True")
        assert (
            auswertung.programmfehler
            == "Zeile 2: `b` gibt es nicht - Tippfehler, oder fehlt die Variable/Funktion noch?"
        )

    def test_fehler_in_funktion_der_sus_aus_test_aufgerufen(self, pruefe_programm: PruefeProgramm) -> None:
        auswertung = pruefe_programm("def f():\n    return 1 / 0\n", "assert f() == 1")
        assert auswertung.tests[0].meldung == "Zeile 2: ZeroDivisionError: division by zero"

    def test_fehler_nur_in_testdatei_ohne_zeile(self, pruefe_programm: PruefeProgramm) -> None:
        auswertung = pruefe_programm("x = 1\n", "assert 1 / 0")
        assert auswertung.tests[0].meldung == "ZeroDivisionError: division by zero"

    def test_eigene_fehlerarten(self) -> None:
        skript = Path("egal.py")
        assert "öfter nach einer Eingabe" in pruefe.fehlertext(pruefe._KeineEingabeMehr(), skript)
        assert pruefe.fehlertext(pruefe.ProgrammFehler("schon formuliert"), skript) == "schon formuliert"

    def test_exit_im_programm_beendet_pruefung_nicht(self, pruefe_programm: PruefeProgramm) -> None:
        auswertung = pruefe_programm("print('a')\nexit()\nprint('b')\n", "assert AUSGABE == 'a'")
        assert "SystemExit" in (auswertung.programmfehler or "")
        assert symbole(auswertung) == "✓"


class TestStarteProgramm:
    @pytest.fixture
    def lauf(self, schreibe: Schreibe) -> Starte:
        """Liefert eine Funktion, die ein Programm mit den gegebenen Eingaben einmal laufen lässt."""

        def starte(programm: str, *eingaben: str) -> pruefe.Lauf:
            """Startet ``programm`` über ``pruefe._starte_programm``."""
            return pruefe._starte_programm(schreibe("p.py", programm), programm, eingaben)

        return starte

    def test_ausgabe_ohne_input_text_und_eingaben_in_reihenfolge(self, lauf: Starte) -> None:
        ergebnis = lauf("a = input('Erste? ')\nb = input('Zweite? ')\nprint(a, b)\n", "x", "y")
        assert ergebnis.ausgabe == "x y"
        assert ergebnis.fehler is None

    def test_zu_wenige_eingaben(self, lauf: Starte) -> None:
        ergebnis = lauf("a = input()\nb = input()\n", "x")
        assert "öfter nach einer Eingabe" in (ergebnis.fehler or "")
        assert ergebnis.namensraum["a"] == "x"

    def test_variablen_vor_fehler_bleiben(self, lauf: Starte) -> None:
        ergebnis = lauf("x = 5\nprint('vorher')\n1 / 0\ny = 6\n")
        assert ergebnis.namensraum["x"] == 5
        assert "y" not in ergebnis.namensraum
        assert ergebnis.ausgabe == "vorher"

    def test_main_block_laeuft(self, lauf: Starte) -> None:
        assert lauf("if __name__ == '__main__':\n    print('main')\n").ausgabe == "main"

    def test_print_mit_sep_und_end(self, lauf: Starte) -> None:
        assert lauf("print(1, 2, sep='-', end='')\nprint('!', end=None)\n").ausgabe == "1-2!"

    def test_print_und_input_global_unveraendert(self, lauf: Starte) -> None:
        original = builtins.print, builtins.input
        lauf("print('x')\n")
        assert (builtins.print, builtins.input) == original

    def test_eingaben_als_zeichenketten(self, lauf: Starte) -> None:
        assert lauf("print(type(input()).__name__)\n", "5").ausgabe == "str"


class TestVerwendet:
    def test_sprachmittel(self) -> None:
        code = (
            "def f(n):\n    for i in range(n):\n        if i:\n            return i\n    while False:\n        pass\n"
        )
        for was in ("def", "for", "if", "return", "while", "range"):
            assert pruefe.verwendet(code, was), was
        assert not pruefe.verwendet(code, "class")
        assert not pruefe.verwendet(code, "print")

    @pytest.mark.parametrize("was", ["for", "while", "range"])
    def test_kommentare_und_strings_zaehlen_nicht(self, was: str) -> None:
        code = '"""for i in range(3)"""\n# for x in y\ntext = "while True"\n'
        assert not pruefe.verwendet(code, was)

    def test_methodenaufruf_zaehlt_nicht_als_funktion(self) -> None:
        assert not pruefe.verwendet("x = []\nx.append(1)\n", "append")

    def test_syntaxfehler(self) -> None:
        assert not pruefe.verwendet("for for", "for")

    def test_im_test_verfuegbar(self, pruefe_programm: PruefeProgramm) -> None:
        programm = "for i in range(2):\n    print(i)\n"
        assert pruefe_programm(programm, "assert verwendet('for')\nassert not verwendet('while')\n").bestanden


class TestLadeTests:
    TEXT = textwrap.dedent(
        """\
        # Automatisch erzeugt aus x.py - nicht von Hand ändern.
        # vorlage-hash: abc123

        x = 1
        # Name A
        assert x == 1
        # Vorbereitung B
        y = 2
        assert y == 2
        assert x + 1 == 2, "meldung"
        for i in range(2):
            assert i < 2
        EINGABEN = [1, "b"]
        """
    )

    def test_schritte(self, schreibe: Schreibe) -> None:
        geladen = pruefe.lade_tests(schreibe("t.py", self.TEXT))
        assert [(s.name, s.ist_test) for s in geladen.schritte] == [
            ("x = 1", False),  # Kopfkommentar mit Leerzeile dazwischen wird kein Name
            ("Name A", True),
            ("Vorbereitung B", False),
            ("Vorbereitung B", True),  # Kommentar über der Vorbereitung gilt für den Test
            ("x + 1 == 2", True),  # ohne Kommentar: die Bedingung
            ("for i in range(2):", True),  # Block mit assert zählt als ein Test
            ('EINGABEN = [1, "b"]', False),
        ]
        assert geladen.eingaben == ["1", "b"]
        assert geladen.vorlage_hash == "abc123"

    def test_langer_name_wird_gekuerzt(self, schreibe: Schreibe) -> None:
        geladen = pruefe.lade_tests(schreibe("t.py", "assert " + " + ".join(["1"] * 60) + " > 0\n"))
        assert len(geladen.schritte[0].name) == 70

    def test_ohne_hash(self, schreibe: Schreibe) -> None:
        assert pruefe.lade_tests(schreibe("t.py", "assert True\n")).vorlage_hash is None

    def test_thema_und_inhalt(self, schreibe: Schreibe) -> None:
        testdatei = schreibe("t.py", "# vorlage-hash: abc\n# thema: funktionen\n# inhalt: Funktion mit return\n\n")
        assert pruefe.lies_thema(testdatei) == "funktionen"
        assert pruefe.lies_inhalt(testdatei) == "Funktion mit return"
        assert pruefe.lies_thema(schreibe("ohne.py", "assert True\n")) is None
        assert pruefe.lies_inhalt(schreibe("ohne.py", "assert True\n")) is None


class TestPruefeLoesung:
    def test_assert_ohne_meldung(self, pruefe_programm: PruefeProgramm) -> None:
        assert pruefe_programm("x = 1\n", "assert x == 2").tests[0].meldung == "Bedingung nicht erfüllt."

    def test_fehlschlagende_vorbereitung_gibt_genau_ein_kreuz(self, pruefe_programm: PruefeProgramm) -> None:
        tests = "# erster\nwert = gibts_nicht\nassert wert == 1\n# zweiter\nassert True\n"
        auswertung = pruefe_programm("x = 1\n", tests)
        assert symbole(auswertung) == "✗✓"
        assert [t.name for t in auswertung.tests] == ["erster", "zweiter"]
        assert "`gibts_nicht` gibt es nicht" in (auswertung.tests[0].meldung or "")

    def test_tests_teilen_namensraum(self, pruefe_programm: PruefeProgramm) -> None:
        assert pruefe_programm("x = 1\n", "x = x + 1\nassert x == 2\n").bestanden

    def test_starte_aendert_ersten_lauf_nicht(self, pruefe_programm: PruefeProgramm) -> None:
        tests = 'EINGABEN = ["a"]\nneu = starte("b")\nassert neu == "b"\nassert AUSGABE == "a"\nassert wort == "a"\n'
        assert symbole(pruefe_programm("wort = input()\nprint(wort)\n", tests)) == "✓✓✓"

    def test_ohne_tests_nicht_bestanden(self, pruefe_programm: PruefeProgramm) -> None:
        auswertung = pruefe_programm("x = 1\n", "x = 2\n")
        assert auswertung.tests == []
        assert not auswertung.bestanden

    def test_programmfehler_trotz_gruener_tests(self, pruefe_programm: PruefeProgramm) -> None:
        auswertung = pruefe_programm("x = 1\n1 / 0\n", "assert x == 1\n")
        assert symbole(auswertung) == "✓"
        assert not auswertung.bestanden

    @mit_kurzem_zeitlimit
    def test_endlosschleife_im_programm(self, pruefe_programm: PruefeProgramm) -> None:
        start = time.monotonic()
        auswertung = pruefe_programm("while True:\n    pass\n", "assert True\n")
        assert time.monotonic() - start < 3
        assert auswertung.abgebrochen
        assert auswertung.tests == []
        assert (
            auswertung.programmfehler
            == "Ihr Programm ist nach 0.5 Sekunden nicht fertig geworden - vielleicht eine Endlosschleife?"
        )
        assert multiprocessing.active_children() == [], "Prozess mit der Endlosschleife läuft noch"

    @mit_kurzem_zeitlimit
    def test_endlosschleife_im_test_bricht_ab(self, pruefe_programm: PruefeProgramm) -> None:
        programm = "def f():\n    while True:\n        pass\n"
        auswertung = pruefe_programm(programm, "# vorher\nassert True\n# hängt\nassert f()\n# danach\nassert True\n")
        assert auswertung.abgebrochen
        assert [t.name for t in auswertung.tests] == ["vorher", "hängt"]
        assert "Zeitlimit" in (auswertung.tests[1].meldung or "")
        assert "Prüfung abgebrochen" in pruefe.formatiere("x", auswertung)

    @mit_kurzem_zeitlimit
    def test_riesige_rechnung_wird_nach_gesamtlimit_abgebrochen(self, pruefe_programm: PruefeProgramm) -> None:
        # Eine einzige Rechnung in C blockiert alle Threads; nur das Beenden des Prozesses hilft.
        start = time.monotonic()
        auswertung = pruefe_programm("x = 10 ** 10 ** 9\n", "assert True\n")
        assert time.monotonic() - start < 4
        assert auswertung.abgebrochen
        assert "nicht fertig geworden" in (auswertung.programmfehler or "")
        assert multiprocessing.active_children() == []

    def test_os_exit_im_programm(self, pruefe_programm: PruefeProgramm) -> None:
        auswertung = pruefe_programm("import os\nos._exit(3)\n", "assert True\n")
        assert auswertung.abgebrochen
        assert "abgestürzt" in (auswertung.programmfehler or "")
        assert "Prüfung abgebrochen" in pruefe.formatiere("x", auswertung)

    def test_endlose_rekursion_wird_sofort_gemeldet(self, pruefe_programm: PruefeProgramm) -> None:
        programm = "def f(n):\n    return f(n + 1)\n"
        start = time.monotonic()
        auswertung = pruefe_programm(programm + "f(0)\n", "# rekursion\nassert f(0) == 1\n# danach\nassert True\n")
        assert time.monotonic() - start < 2
        assert auswertung.programmfehler == "Zeile 2: RecursionError: maximum recursion depth exceeded"
        assert symbole(auswertung) == "✗✓"
        assert "RecursionError" in (auswertung.tests[0].meldung or "")
        assert not auswertung.abgebrochen

    def test_tiefe_rekursion_ist_erlaubt(self, pruefe_programm: PruefeProgramm) -> None:
        programm = "def tief(n):\n    return 0 if n == 0 else 1 + tief(n - 1)\n\nergebnis = tief(900)\n"
        assert pruefe_programm(programm, "assert ergebnis == 900\nassert tief(900) == 900\n").bestanden

    def test_datei_mit_bom_und_crlf(self, schreibe: Schreibe) -> None:
        skript = schreibe("l.py", "\ufeffx = 1\r\nprint(x)\r\n")
        tests = schreibe("t.py", "assert AUSGABE == '1'\n")
        assert pruefe.pruefe_loesung(skript, tests).bestanden


class TestFormatiere:
    def test_alles_gruen(self) -> None:
        auswertung = pruefe.Auswertung(tests=[pruefe.TestErgebnis("a", None), pruefe.TestErgebnis("b", None)])
        assert pruefe.formatiere("1_001_x", auswertung) == "── 1_001_x ──\n✓ a\n✓ b\n→ Alle Tests bestanden (2). Super!"

    def test_fehler_und_meldung_eingerueckt(self) -> None:
        auswertung = pruefe.Auswertung(
            programmfehler="kaputt",
            tests=[pruefe.TestErgebnis("a", "Zeile 1\nZeile 2"), pruefe.TestErgebnis("b", None)],
        )
        assert pruefe.formatiere("1_001_x", auswertung) == (
            "── 1_001_x ──\n⚠ Fehler in Ihrem Programm: kaputt\n✗ a\n    Zeile 1\n    Zeile 2\n✓ b\n"
            "→ 1 von 2 Tests bestanden."
        )


class TestMain:
    def test_kennung_eindeutig(self, main: Main, kopiere_vorlagen: KopiereVorlagen) -> None:
        code, ausgabe = main("1_003", "--aufgaben", str(kopiere_vorlagen()), "--tests", str(TESTS))
        assert code == 1  # leere Vorlage besteht nicht
        assert ausgabe.count("── ") == 1
        assert "── 1_003_rechteck ──" in ausgabe

    def test_kennung_unbekannt(self, main: Main) -> None:
        code, ausgabe = main("1_003", "9", "--tests", str(TESTS))
        assert code == 2
        assert "Keine Aufgabe zu „9“" in ausgabe
        assert "1_001_hallo_welt" in ausgabe
        assert "  datenanalyse      Datenanalyse" in ausgabe  # auch die Themen als Vorschlag
        assert "── " not in ausgabe  # bei Tippfehler gar nichts prüfen

    @pytest.mark.parametrize(
        ("kennungen", "erwartet"),
        [
            (["kontrollfluss"], ["1_001_a", "2_001_b"]),
            (["kontrollfluss", "funktionen"], ["1_001_a", "2_001_b", "2_002_c"]),
            (["2", "kontrollfluss"], ["2_001_b"]),
            (["1", "2", "funktionen"], ["2_002_c"]),
            (["2"], ["2_001_b", "2_002_c", "2_003_ohne_thema"]),
        ],
    )
    def test_auswahl_nach_thema(
        self, main: Main, schreibe: Schreibe, tmp_path: Path, kennungen: list[str], erwartet: list[str]
    ) -> None:
        """Namensanfänge untereinander und Themen untereinander vereinigt, beide Gruppen geschnitten."""
        themen = {"1_001_a": "kontrollfluss", "2_001_b": "kontrollfluss", "2_002_c": "funktionen"}
        for name in ("1_001_a", "2_001_b", "2_002_c", "2_003_ohne_thema"):
            kopf = f"# thema: {themen[name]}\n\n" if name in themen else ""
            schreibe(f"tests/{name}.py", kopf + "assert True\n")
            schreibe(f"aufgaben/{name}.py", "")
        argumente = [*kennungen, "--aufgaben", str(tmp_path / "aufgaben"), "--tests", str(tmp_path / "tests")]
        code, ausgabe = main(*argumente)
        assert code == 0, ausgabe
        assert re.findall(r"── (\S+) ──", ausgabe) == erwartet

    def test_stufe_und_thema_ohne_gemeinsame_aufgabe(self, main: Main, schreibe: Schreibe, tmp_path: Path) -> None:
        schreibe("tests/1_001_a.py", "# thema: funktionen\n\nassert True\n")
        schreibe("tests/2_001_b.py", "# thema: kontrollfluss\n\nassert True\n")
        code, ausgabe = main("1", "kontrollfluss", "--tests", str(tmp_path / "tests"))
        assert code == 2
        assert "Zu „1 kontrollfluss“ gibt es (noch) keine Aufgabe." in ausgabe

    def test_mehrere_kennungen(self, main: Main, kopiere_vorlagen: KopiereVorlagen) -> None:
        aufgaben = kopiere_vorlagen()
        code, ausgabe = main("1_001", "1_003", "1_001_hallo_welt", "--aufgaben", str(aufgaben), "--tests", str(TESTS))
        assert code == 1
        assert ausgabe.count("── ") == 2  # 1_001 doppelt angegeben, aber nur einmal geprüft
        assert "── 1_001_hallo_welt ──" in ausgabe
        assert "── 1_003_rechteck ──" in ausgabe

    def test_stufe_als_kennung(self, main: Main, kopiere_vorlagen: KopiereVorlagen) -> None:
        _, ausgabe = main("3", "--aufgaben", str(kopiere_vorlagen()), "--tests", str(TESTS))
        namen = re.findall(r"── (\S+) ──", ausgabe)
        assert len(namen) > 1
        assert all(name.startswith("3_") for name in namen), namen

    @pytest.mark.parametrize(
        ("kennung", "erwartet"), [("1_001", ["1_001_hallo", "1_001_hallowelt"]), ("1_001_hallo", ["1_001_hallo"])]
    )
    def test_mehrdeutige_kennung_prueft_alle_passenden(
        self, main: Main, schreibe: Schreibe, tmp_path: Path, kennung: str, erwartet: list[str]
    ) -> None:
        for name in ("1_001_hallo", "1_001_hallowelt", "1_002_anderes"):
            schreibe(f"tests/{name}.py", "assert True\n")
            schreibe(f"aufgaben/{name}.py", "")
        code, ausgabe = main(kennung, "--aufgaben", str(tmp_path / "aufgaben"), "--tests", str(tmp_path / "tests"))
        assert code == 0
        assert re.findall(r"── (\S+) ──", ausgabe) == erwartet

    # auch mit Windows-Zeilenenden oder BOM gilt eine Vorlage als unverändert
    @pytest.mark.parametrize(("zeilenende", "encoding"), [("\n", "utf-8"), ("\r\n", "utf-8"), ("\n", "utf-8-sig")])
    def test_nichts_bearbeitet(
        self, main: Main, kopiere_vorlagen: KopiereVorlagen, zeilenende: str, encoding: str
    ) -> None:
        aufgaben = kopiere_vorlagen(zeilenende, encoding)
        code, ausgabe = main("--aufgaben", str(aufgaben), "--tests", str(TESTS))
        assert code == 0
        assert "Noch keine bearbeitete Aufgabe" in ausgabe

    def test_nur_bearbeitete_werden_geprueft(self, main: Main, kopiere_vorlagen: KopiereVorlagen) -> None:
        aufgaben = kopiere_vorlagen()
        (aufgaben / "1_001_hallo_welt.py").write_text(bearbeite_vorlage("1_001_hallo_welt", 'print("Hallo Welt!")'))
        code, ausgabe = main("--aufgaben", str(aufgaben), "--tests", str(TESTS))
        assert code == 0, ausgabe
        assert ausgabe.count("── ") == 1
        assert "Alle Tests bestanden (1)" in ausgabe

        (aufgaben / "2_001_zaehlen.py").write_text(bearbeite_vorlage("2_001_zaehlen", 'print("1\\n2\\n3\\n4\\n5")'))
        code, ausgabe = main("--aufgaben", str(aufgaben), "--tests", str(TESTS))
        assert code == 1  # 2_001 ohne for-Schleife
        assert ausgabe.count("── ") == 2
        assert "Benutzen Sie eine for-Schleife" in ausgabe

    def test_datei_fehlt(self, main: Main, tmp_path: Path) -> None:
        code, ausgabe = main("1_001", "--aufgaben", str(tmp_path), "--tests", str(TESTS))
        assert code == 1
        assert "fehlt im Ordner" in ausgabe

    def test_github_zusammenfassung(
        self, main: Main, kopiere_vorlagen: KopiereVorlagen, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        zusammenfassung = tmp_path / "summary.md"
        monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(zusammenfassung))
        main("1_001", "--aufgaben", str(kopiere_vorlagen()), "--tests", str(TESTS))
        text = zusammenfassung.read_text(encoding="utf-8")
        assert text.startswith("## Ergebnis\n\n```\n── 1_001_hallo_welt ──"), text

    def test_unbekanntes_argument(self, main: Main, capsys: pytest.CaptureFixture[str]) -> None:
        with pytest.raises(SystemExit) as abbruch:
            main("--quatsch")
        assert abbruch.value.code == 2
        assert "Aufruf nicht verstanden" in capsys.readouterr().err

    def test_hilfe(self, main: Main, capsys: pytest.CaptureFixture[str]) -> None:
        with pytest.raises(SystemExit) as abbruch:
            main("--help")
        assert abbruch.value.code == 0
        assert "  kontrollfluss     Bedingungen & Schleifen" in capsys.readouterr().out

    def test_wie_im_github_workflow(self, kopiere_vorlagen: KopiereVorlagen, tmp_path: Path) -> None:
        """Aufruf als eigener Prozess aus einem anderen Ordner, wie in .github/workflows/pruefen.yml."""
        aufgaben = kopiere_vorlagen()
        (aufgaben / "1_002_begruessung.py").write_text(
            bearbeite_vorlage("1_002_begruessung", 'print(f"Hallo {name}!")')
        )
        befehl = [sys.executable, str(PROJEKT / "pruefe.py"), "--tests", str(TESTS), "--aufgaben", "aufgaben"]
        lauf = subprocess.run(befehl, cwd=tmp_path, capture_output=True, text=True, encoding="utf-8", check=False)
        assert lauf.returncode == 0, lauf.stdout + lauf.stderr
        assert "── 1_002_begruessung ──\n✓" in lauf.stdout

        (aufgaben / "1_002_begruessung.py").write_text(bearbeite_vorlage("1_002_begruessung", 'print("Hallo Anna!")'))
        lauf = subprocess.run(befehl, cwd=tmp_path, capture_output=True, text=True, encoding="utf-8", check=False)
        assert lauf.returncode == 1
        assert "1 von 2 Tests bestanden" in lauf.stdout

    @mit_kurzem_zeitlimit
    def test_endlosschleifen_bremsen_andere_aufgaben_nicht(self, main: Main, kopiere_vorlagen: KopiereVorlagen) -> None:
        """Mehrere hängende Aufgaben in einem Lauf: jede wird zeitnah abgebrochen, die richtigen bestehen trotzdem."""
        aufgaben = kopiere_vorlagen()
        loesungen = {
            # fängt mit except: auch "keine Eingabe mehr" ab
            "1_001_hallo_welt": "while True:\n    try:\n        input()\n    except:\n        pass",
            # hängt erst im zweiten Lauf über starte("Bo")
            "1_002_begruessung": 'if name == "Bo":\n    while True:\n        pass\nprint(f"Hallo {name}!")',
            "1_003_rechteck": "flaeche = breite * hoehe\numfang = 2 * (breite + hoehe)\n"
            'print("Fläche:", flaeche)\nprint("Umfang:", umfang)',
            # zahl += 1 vergessen, gibt endlos aus
            "2_001_zaehlen": "zahl = 1\nwhile zahl <= 5:\n    print(zahl)",
            "2_002_verdoppeln": "return verdopple(zahl)",
            "2_003_gerade": "return zahl % 2 == 0",
        }
        for aufgabe, code in loesungen.items():
            (aufgaben / f"{aufgabe}.py").write_text(bearbeite_vorlage(aufgabe, code), encoding="utf-8")
        start = time.monotonic()
        exit_code, ausgabe = main("--aufgaben", str(aufgaben), "--tests", str(TESTS))
        dauer = time.monotonic() - start
        berichte = {block.splitlines()[0].strip("─ "): block for block in ausgabe.strip().split("\n\n")}

        assert exit_code == 1
        assert dauer < 3 * pruefe.ZEITLIMIT_SEKUNDEN + 3, "drei Abbrüche dürfen nur je ein Zeitlimit dauern"
        assert multiprocessing.active_children() == []
        for aufgabe in ("1_001_hallo_welt", "2_001_zaehlen"):
            assert "nicht fertig geworden" in berichte[aufgabe]
            assert "Prüfung abgebrochen" in berichte[aufgabe]
        assert '✓ Begrüßung bei Eingabe "Anna"' in berichte["1_002_begruessung"]
        assert "Zeitlimit überschritten" in berichte["1_002_begruessung"]
        assert "Prüfung abgebrochen" in berichte["1_002_begruessung"]
        assert "RecursionError" in berichte["2_002_verdoppeln"]
        assert "0 von 3 Tests bestanden" in berichte["2_002_verdoppeln"]
        for aufgabe in ("1_003_rechteck", "2_003_gerade"):
            assert "Alle Tests bestanden" in berichte[aufgabe]
