# Automatisch erzeugt aus lehrkraft/muster/2_004_countdown.py - nicht von Hand ändern.
# vorlage-hash: 8f5046a446883794
# thema: kontrollfluss
# inhalt: while-Schleife

EINGABEN = ["3"]

# Countdown ab 3
assert AUSGABE == "3\n2\n1\nStart!", f"Bei Eingabe 3 erwartet:\n3\n2\n1\nStart!\nIhr Programm gibt aus:\n{AUSGABE}"

# Countdown ab 5 (nicht fest 3, 2, 1 hinschreiben!)
ausgabe_fuenf = starte("5")
assert ausgabe_fuenf == "5\n4\n3\n2\n1\nStart!", (
    f"Bei Eingabe 5 erwartet:\n5\n4\n3\n2\n1\nStart!\nIhr Programm gibt aus:\n{ausgabe_fuenf}"
)

# Countdown ab 1: eine Zahl, dann Start!
ausgabe_eins = starte("1")
assert ausgabe_eins == "1\nStart!", f"Bei Eingabe 1 erwartet:\n1\nStart!\nIhr Programm gibt aus:\n{ausgabe_eins}"

# Countdown ab 0: nur Start!
ausgabe_null = starte("0")
assert ausgabe_null == "Start!", (
    f'Bei Eingabe 0 erwartet nur "Start!" – Ihr Programm gibt aus:\n{ausgabe_null}\n'
    "Tipp: Die Bedingung muss schon beim ersten Mal falsch sein, wenn die Zahl 0 ist."
)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."
