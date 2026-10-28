# Automatisch erzeugt aus lehrkraft/muster/1_010_testbericht.py - nicht von Hand ändern.
# vorlage-hash: b0221aa71b5b5270
# thema: texte_zahlen
# inhalt: f-Strings mit Nachkommastellen

EINGABEN = ["47", "52"]

# Bei Eingabe 47 und 52 lautet der Bericht "… (90.38 %)"
if "90.384" in AUSGABE:
    hinweis = "\nTipp: Mit {quote:.2f} statt {quote} erscheinen genau zwei Nachkommastellen."
else:
    hinweis = ""
assert AUSGABE == "Testlauf: 47 von 52 Tests bestanden (90.38 %)", (
    'Bei Eingabe 47 und 52 erwartet: "Testlauf: 47 von 52 Tests bestanden (90.38 %)"\n'
    f'Ihr Programm: "{AUSGABE}"{hinweis}'
)

# Andere Zahlen erscheinen im Bericht (nicht fest 47 und 52 hinschreiben!)
ausgabe_drittel = starte("1", "3")
assert ausgabe_drittel == "Testlauf: 1 von 3 Tests bestanden (33.33 %)", (
    'Bei Eingabe 1 und 3 erwartet: "Testlauf: 1 von 3 Tests bestanden (33.33 %)"\n'
    f'Ihr Programm: "{ausgabe_drittel}"\n'
    "Tipp: Setzen Sie die Variablen bestanden, gesamt und quote in geschweiften Klammern ein."
)

# Die Quote wird gerundet: 2 von 3 sind 66.67 %
ausgabe_gerundet = starte("2", "3")
assert ausgabe_gerundet == "Testlauf: 2 von 3 Tests bestanden (66.67 %)", (
    'Bei Eingabe 2 und 3 erwartet: "Testlauf: 2 von 3 Tests bestanden (66.67 %)"\n'
    f'Ihr Programm: "{ausgabe_gerundet}"\n'
    "Tipp: :.2f rundet 66.666… auf 66.67; schneiden Sie nicht selbst ab."
)

# Auch bei 100 % stehen zwei Nachkommastellen da
ausgabe_alle = starte("52", "52")
assert ausgabe_alle == "Testlauf: 52 von 52 Tests bestanden (100.00 %)", (
    'Bei Eingabe 52 und 52 erwartet: "Testlauf: 52 von 52 Tests bestanden (100.00 %)"\n'
    f'Ihr Programm: "{ausgabe_alle}"\n'
    "Tipp: :.2f zeigt auch bei 100.0 genau zwei Nachkommastellen, also 100.00."
)

# Kein Test bestanden ergibt 0.00 %
ausgabe_keiner = starte("0", "8")
assert ausgabe_keiner == "Testlauf: 0 von 8 Tests bestanden (0.00 %)", (
    'Bei Eingabe 0 und 8 erwartet: "Testlauf: 0 von 8 Tests bestanden (0.00 %)"\n'
    f'Ihr Programm: "{ausgabe_keiner}"'
)
