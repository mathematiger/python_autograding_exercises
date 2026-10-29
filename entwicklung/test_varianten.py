"""Lösungsvarianten: je fünf Lösungen für drei Aufgaben, wie SuS sie abgeben könnten.

Jede Variante wird in die echte Vorlage eingesetzt und wie bei SuS mit ``python pruefe.py 2_002`` geprüft.
So wird genau der Bericht getestet, den SuS sehen.
"""

from __future__ import annotations

import subprocess
import sys

import pytest
from conftest import PROJEKT, TESTS, Schreibe, bearbeite_vorlage

import pruefe

# (Aufgabe, Beschreibung, eingesetzter Code, erwartete ✓/✗, Programmfehler enthält, Meldungen enthalten)
VARIANTEN = [
    # 1_002: input, EINGABEN = ["Anna"], zweiter Lauf mit starte("Bo")
    ("1_002_begruessung", "Musterlösung", 'print("Hallo " + name + "!")', "✓✓✓✓", None, []),
    ("1_002_begruessung", "f-String", 'print(f"Hallo {name}!")', "✓✓✓✓", None, []),
    (
        "1_002_begruessung",
        "print mit end= und Leerzeichen am Zeilenende",
        'print("Hallo", name, end="")\nprint("!   ")',
        "✓✓✓✓",
        None,
        [],
    ),
    (
        "1_002_begruessung",
        "Name fest eingetippt",
        'print("Hallo Anna!")',
        "✓✗✗✗",
        None,
        ['Ihr Programm: "Hallo Anna!"'],
    ),
    (
        "1_002_begruessung",
        "fragt ein zweites Mal nach einer Eingabe",
        'alter = input("Wie alt sind Sie? ")\nprint("Hallo " + name + "!")',
        "✗✗✗✗",
        "öfter nach einer Eingabe",
        ['Ihr Programm: ""', "Mit den Eingaben ['Bo']"],
    ),
    # 1_003: Variablen und Ausgabe
    (
        "1_003_rechteck",
        "Musterlösung",
        'flaeche = breite * hoehe\numfang = 2 * (breite + hoehe)\nprint("Fläche:", flaeche)\nprint("Umfang:", umfang)',
        "✓✓✓✓✓✓",
        None,
        [],
    ),
    (
        "1_003_rechteck",
        "andere Rechnung, f-String mit \\n",
        'flaeche = hoehe * breite\numfang = breite + hoehe + breite + hoehe\nprint(f"Fläche: {flaeche}\\nUmfang: {umfang}")',
        "✓✓✓✓✓✓",
        None,
        [],
    ),
    (
        "1_003_rechteck",
        "Umfang falsch berechnet",
        'flaeche = breite * hoehe\numfang = breite + hoehe\nprint("Fläche:", flaeche)\nprint("Umfang:", umfang)',
        "✓✗✗✗✗✗",
        None,
        ["umfang ist 7, erwartet war 14."],
    ),
    (
        "1_003_rechteck",
        "nur ausgegeben, keine Variablen",
        'print("Fläche:", breite * hoehe)\nprint("Umfang:", 2 * (breite + hoehe))',
        "✗✗✓✓✓✓",
        None,
        ["`flaeche` gibt es nicht", "`umfang` gibt es nicht"],
    ),
    (
        "1_003_rechteck",
        "Zahl und Text mit + verbunden",
        'flaeche = breite * hoehe\numfang = 2 * (breite + hoehe)\nprint("Fläche: " + flaeche)',
        "✓✓✗✗✗✗",
        "TypeError",
        [],
    ),
    # 2_002: Funktion mit return
    ("2_002_verdoppeln", "Musterlösung", "return 2 * zahl", "✓✓✓✓✓", None, []),
    (
        "2_002_verdoppeln",
        "zahl + zahl über Hilfsvariable",
        "ergebnis = zahl + zahl\nreturn ergebnis",
        "✓✓✓✓✓",
        None,
        [],
    ),
    ("2_002_verdoppeln", "print statt return", "print(2 * zahl)", "✗✗✗✗✗", None, ["return vergessen", "ergibt None"]),
    (
        "2_002_verdoppeln",
        "negative Zahlen vergessen",
        "if zahl > 0:\n    return 2 * zahl\nreturn zahl",
        "✓✓✗✗✗",
        None,
        ["verdopple(-4) ergibt -4, erwartet war -8."],
    ),
    ("2_002_verdoppeln", "Endlosschleife", "while True:\n    pass", "", "Endlosschleife", []),
]


@pytest.mark.parametrize(
    ("aufgabe", "beschreibung", "code", "erwartet", "programmfehler", "meldungen"),
    VARIANTEN,
    ids=[f"{v[0]}: {v[1]}" for v in VARIANTEN],
)
def test_variante(
    schreibe: Schreibe,
    aufgabe: str,
    beschreibung: str,
    code: str,
    erwartet: str,
    programmfehler: str | None,
    meldungen: list[str],
) -> None:
    skript = schreibe(f"{aufgabe}/{aufgabe}.py", bearbeite_vorlage(aufgabe, code))
    befehl = [sys.executable, str(PROJEKT / "pruefe.py"), aufgabe[:5], "--aufgaben", str(skript.parent)]
    lauf = subprocess.run(befehl, capture_output=True, text=True, encoding="utf-8", check=False)
    bericht = lauf.stdout
    zeilen = bericht.splitlines()

    assert zeilen[0] == f"── {aufgabe} ──"
    assert "".join(z[0] for z in zeilen if z[:1] in ("✓", "✗")) == erwartet, bericht
    fehlerzeilen = [z for z in zeilen if z.startswith("⚠ Fehler in Ihrem Programm:")]
    if programmfehler is None:
        assert fehlerzeilen == [], bericht
    else:
        assert programmfehler in "".join(fehlerzeilen), bericht
    for text in meldungen:
        assert text in bericht

    soll_bestanden = programmfehler is None and set(erwartet) == {"✓"}
    assert lauf.returncode == (0 if soll_bestanden else 1), bericht + lauf.stderr
    assert lauf.stderr == ""


@pytest.mark.parametrize("aufgabe", ["1_002_begruessung", "1_003_rechteck", "2_002_verdoppeln"])
def test_fuenf_varianten_pro_aufgabe(aufgabe: str) -> None:
    assert sum(v[0] == aufgabe for v in VARIANTEN) == 5


def test_testnamen_kommen_aus_den_kommentaren(schreibe: Schreibe) -> None:
    skript = schreibe("1_002_begruessung.py", bearbeite_vorlage("1_002_begruessung", 'print("Hallo Anna!")'))
    auswertung = pruefe.pruefe_loesung(skript, TESTS / "1_002_begruessung.py")
    assert [t.name for t in auswertung.tests] == [
        'Begrüßung bei Eingabe "Anna"',
        'Begrüßung bei Eingabe "Bo" (nicht fest "Anna" hinschreiben!)',
        "Ränder: ein Name aus einem einzigen Buchstaben und einer aus 30 Buchstaben",
        "40 zufällige Namen",
    ]
