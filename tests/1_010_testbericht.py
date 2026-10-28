# Automatisch erzeugt aus lehrkraft/muster/1_010_testbericht.py - nicht von Hand ändern.
# vorlage-hash: 3fcff8384f538410
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

# Ränder: 1 Test insgesamt, 10 000 Tests, knapp über 0 % und knapp unter 100 %
raender = [
    ("0", "1", "Testlauf: 0 von 1 Tests bestanden (0.00 %)"),
    ("1", "1", "Testlauf: 1 von 1 Tests bestanden (100.00 %)"),
    ("1", "10000", "Testlauf: 1 von 10000 Tests bestanden (0.01 %)"),
    ("9999", "10000", "Testlauf: 9999 von 10000 Tests bestanden (99.99 %)"),
    ("10000", "10000", "Testlauf: 10000 von 10000 Tests bestanden (100.00 %)"),
]
for bestanden_test, gesamt_test, erwartet in raender:
    ausgabe = starte(bestanden_test, gesamt_test)
    assert ausgabe == erwartet, (
        f'Bei Eingabe {bestanden_test} und {gesamt_test} erwartet: "{erwartet}"\nIhr Programm: "{ausgabe}"'
    )

# 50 zufällige Testläufe mit bis zu 10 000 Tests
zufall = Zufall(1010)
for _ in range(50):
    gesamt_test = zufall.randint(1, 10000)
    bestanden_test = zufall.randint(0, gesamt_test)
    # Mit ganzen Zahlen gerechnet: Die Quote in Hundertstel Prozent ist 10000 * bestanden / gesamt, gerundet
    # (20000 * bestanden + gesamt) // (2 * gesamt). Fälle genau auf der Mitte lässt der Test aus, weil
    # Kommazahlen dort je nach letzter Stelle auf- oder abgerundet werden.
    if (20000 * bestanden_test) % gesamt_test == 0 and (20000 * bestanden_test // gesamt_test) % 2 == 1:
        continue
    hundertstel = (20000 * bestanden_test + gesamt_test) // (2 * gesamt_test)
    quote_text = f"{hundertstel // 100}.{hundertstel % 100:02d}"
    erwartet = f"Testlauf: {bestanden_test} von {gesamt_test} Tests bestanden ({quote_text} %)"
    ausgabe = starte(str(bestanden_test), str(gesamt_test))
    assert ausgabe == erwartet, (
        f'Bei Eingabe {bestanden_test} und {gesamt_test} erwartet: "{erwartet}"\nIhr Programm: "{ausgabe}"'
    )
