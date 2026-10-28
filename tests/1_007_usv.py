# Automatisch erzeugt aus lehrkraft/muster/1_007_usv.py - nicht von Hand ändern.
# vorlage-hash: 4286c3b10054fae2
# thema: texte_zahlen
# inhalt: Runden mit round

EINGABEN = ["1000", "450"]

# Bei 1000 Wh und 450 W hält die USV etwa 133 Minuten
assert AUSGABE == "Die USV hält etwa 133 Minuten.\nDas sind etwa 2.2 Stunden.", (
    "Bei Eingabe 1000 und 450 erwartet:\nDie USV hält etwa 133 Minuten.\nDas sind etwa 2.2 Stunden.\n"
    f"Ihr Programm gibt aus:\n{AUSGABE}\n"
    "Tipp: round(minuten) rundet auf ganze Minuten, round(minuten / 60, 1) auf eine Nachkommastelle."
)

# Bei 1000 Wh und 700 W wird aufgerundet: 85.71 Minuten sind etwa 86 Minuten
ausgabe_auf = starte("1000", "700")
assert ausgabe_auf == "Die USV hält etwa 86 Minuten.\nDas sind etwa 1.4 Stunden.", (
    "Bei Eingabe 1000 und 700 erwartet:\nDie USV hält etwa 86 Minuten.\nDas sind etwa 1.4 Stunden.\n"
    f"Ihr Programm gibt aus:\n{ausgabe_auf}\n"
    "Tipp: Die Laufzeit ist 85.71 Minuten. int(...) schneidet nur ab und ergibt 85; round(...) rundet auf 86."
)

# Andere Werte ergeben eine andere Laufzeit (nicht fest 133 hinschreiben!)
ausgabe_lang = starte("800", "300")
assert ausgabe_lang == "Die USV hält etwa 160 Minuten.\nDas sind etwa 2.7 Stunden.", (
    "Bei Eingabe 800 und 300 erwartet:\nDie USV hält etwa 160 Minuten.\nDas sind etwa 2.7 Stunden.\n"
    f"Ihr Programm gibt aus:\n{ausgabe_lang}"
)

# Ganze Minuten erscheinen ohne .0
ausgabe_glatt = starte("600", "250")
assert ausgabe_glatt == "Die USV hält etwa 144 Minuten.\nDas sind etwa 2.4 Stunden.", (
    "Bei Eingabe 600 und 250 erwartet:\nDie USV hält etwa 144 Minuten.\nDas sind etwa 2.4 Stunden.\n"
    f"Ihr Programm gibt aus:\n{ausgabe_glatt}\n"
    "Tipp: round(minuten) ohne zweite Zahl liefert eine ganze Zahl (144), round(minuten, 0) dagegen 144.0."
)

# Ränder: großer Akku an kleiner Last und kleiner Akku an großer Last
raender = [
    ("10000", "1", "Die USV hält etwa 600000 Minuten.\nDas sind etwa 10000.0 Stunden."),
    ("1", "10000", "Die USV hält etwa 0 Minuten.\nDas sind etwa 0.0 Stunden."),
]
for energie_test, leistung_test, erwartet in raender:
    ausgabe = starte(energie_test, leistung_test)
    assert ausgabe == erwartet, (
        f"Bei Eingabe {energie_test} und {leistung_test} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"
    )

# 50 zufällige Akkus und Lasten zwischen 1 und 10 000
zufall = Zufall(1007)
for _ in range(50):
    energie_test = zufall.randint(1, 10000)
    leistung_test = zufall.randint(1, 10000)
    # Mit ganzen Zahlen gerechnet: Die Laufzeit ist 60 * energie / leistung Minuten, also auf ganze Minuten
    # gerundet (120 * energie + leistung) // (2 * leistung). Für Zehntelstunden entsprechend mit 20 statt 120.
    # Fälle genau auf der Mitte (x.5) lässt der Test aus, dort rundet round auf die gerade Zahl.
    if (120 * energie_test) % leistung_test == 0 and (120 * energie_test // leistung_test) % 2 == 1:
        continue
    if (20 * energie_test) % leistung_test == 0 and (20 * energie_test // leistung_test) % 2 == 1:
        continue
    minuten_erwartet = (120 * energie_test + leistung_test) // (2 * leistung_test)
    zehntelstunden = (20 * energie_test + leistung_test) // (2 * leistung_test)
    erwartet = (
        f"Die USV hält etwa {minuten_erwartet} Minuten.\n"
        f"Das sind etwa {zehntelstunden // 10}.{zehntelstunden % 10} Stunden."
    )
    ausgabe = starte(str(energie_test), str(leistung_test))
    assert ausgabe == erwartet, (
        f"Bei Eingabe {energie_test} und {leistung_test} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"
    )
