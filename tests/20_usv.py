# Automatisch erzeugt aus lehrkraft/muster/20_usv.py - nicht von Hand ändern.
# vorlage-hash: c1d83bf07e4090ab

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
