# Automatisch erzeugt aus lehrkraft/muster/16_bildschirm.py - nicht von Hand ändern.
# vorlage-hash: 2ef8999bc48db2eb

EINGABEN = ["80", "60"]

# Bei Breite 80 und Höhe 60 ist die Diagonale 100 cm
assert AUSGABE == "Die Diagonale ist 100.0 cm lang.", (
    f'Bei Eingabe 80 und 60 erwartet: "Die Diagonale ist 100.0 cm lang." – Ihr Programm: "{AUSGABE}"\n'
    "Tipp: Erst quadrieren und addieren, dann die Wurzel ziehen: math.sqrt(breite ** 2 + hoehe ** 2)."
)

# Andere Maße ergeben eine andere Diagonale (nicht fest 100.0 hinschreiben!)
ausgabe_klein = starte("40", "30")
assert ausgabe_klein == "Die Diagonale ist 50.0 cm lang.", (
    f'Bei Eingabe 40 und 30 erwartet: "Die Diagonale ist 50.0 cm lang." – Ihr Programm: "{ausgabe_klein}"'
)

# Ein hochkant stehender Bildschirm: die Höhe ist größer als die Breite
ausgabe_hoch = starte("5", "12")
assert ausgabe_hoch == "Die Diagonale ist 13.0 cm lang.", (
    f'Bei Eingabe 5 und 12 erwartet: "Die Diagonale ist 13.0 cm lang." – Ihr Programm: "{ausgabe_hoch}"\n'
    "Tipp: Beide Seiten werden quadriert; die Wurzel zieht man erst aus der Summe, nicht aus jeder Seite einzeln."
)

# Auch Kommazahlen funktionieren
ausgabe_komma = starte("2.5", "6")
assert ausgabe_komma == "Die Diagonale ist 6.5 cm lang.", (
    f'Bei Eingabe 2.5 und 6 erwartet: "Die Diagonale ist 6.5 cm lang." – Ihr Programm: "{ausgabe_komma}"'
)
