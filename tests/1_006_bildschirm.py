# Automatisch erzeugt aus lehrkraft/muster/1_006_bildschirm.py - nicht von Hand ändern.
# vorlage-hash: 934761650bfee336
# text-hash: 5c7e42960d519349
# thema: texte_zahlen
# inhalt: Potenz und Wurzel

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

# Hilfsfunktion für die folgenden Tests: Kommazahlen dürfen in der letzten Stelle abweichen
# (math.sqrt und ** 0.5 rechnen nicht immer auf die letzte Stelle gleich, beides ist richtig).
def diagonale_in(ausgabe):
    """Liest die Zahl aus "Die Diagonale ist … cm lang."; None, wenn die Ausgabe anders aussieht."""
    vorne = "Die Diagonale ist "
    hinten = " cm lang."
    if not (ausgabe.startswith(vorne) and ausgabe.endswith(hinten)):
        return None
    try:
        return float(ausgabe[len(vorne) : -len(hinten)])
    except ValueError:
        return None

# Ränder: kleinster und größter Bildschirm (1 und 1 cm, 1000 und 1000 cm)
for seite, erwartet in [("1", 1.4142135623730951), ("1000", 1414.213562373095)]:
    ausgabe = starte(seite, seite)
    wert = diagonale_in(ausgabe)
    assert wert is not None and abs(wert - erwartet) < 0.000001, (
        f'Bei Eingabe {seite} und {seite} erwartet: "Die Diagonale ist {erwartet} cm lang." – Ihr Programm: "{ausgabe}"'
    )

# 40 zufällige Bildschirme mit Breite und Höhe zwischen 1 und 1000 cm
zufall = Zufall(1006)
for _ in range(40):
    breite_test = str(zufall.randint(10, 10000) / 10)
    hoehe_test = str(zufall.randint(10, 10000) / 10)
    # Anders gerechnet als mit math.sqrt: hoch 0.5 ist auch die Wurzel
    erwartet = (float(breite_test) * float(breite_test) + float(hoehe_test) * float(hoehe_test)) ** 0.5
    ausgabe = starte(breite_test, hoehe_test)
    wert = diagonale_in(ausgabe)
    assert wert is not None and abs(wert - erwartet) < 0.000001, (
        f'Bei Eingabe {breite_test} und {hoehe_test} erwartet: "Die Diagonale ist {erwartet} cm lang."\n'
        f'Ihr Programm: "{ausgabe}"'
    )
