# Automatisch erzeugt aus lehrkraft/muster/2_008_stromverbrauch.py - nicht von Hand ändern.
# vorlage-hash: 128e8d7ea4fbba82
# text-hash: a4e31a63d1b98e23
# thema: kontrollfluss
# inhalt: Schleife mit continue

# Das Beispiel aus der Aufgabe: der defekte Monat zählt nicht mit
ergebnis = mittlerer_verbrauch([400, -1, 500, 600])
assert ergebnis == 500, (
    f"mittlerer_verbrauch([400, -1, 500, 600]) ergibt {ergebnis!r}, erwartet war 500.0.\n"
    "Tipp: Der Wert -1 darf weder in die Summe noch in die Anzahl eingehen. Überspringen Sie ihn mit continue."
)

# Weitere Messreihen (nicht fest 500 hinschreiben!)
for verbraeuche, erwartet in [
    ([100, 200, 300], 200),
    ([-1, 250], 250),
    ([120, -1, -1, 80, -1, 100], 100),
    ([45], 45),
]:
    ergebnis = mittlerer_verbrauch(verbraeuche)
    assert ergebnis == erwartet, f"mittlerer_verbrauch({verbraeuche}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Defekte Monate zählen auch bei der Anzahl nicht mit
ergebnis = mittlerer_verbrauch([600, -1, -1, 600])
assert ergebnis == 600, (
    f"mittlerer_verbrauch([600, -1, -1, 600]) ergibt {ergebnis!r}, erwartet war 600.0.\n"
    "Tipp: Teilen Sie durch die Anzahl der gemessenen Monate (2), nicht durch die Länge der Liste (4)."
)

# Ein Verbrauch von 0 kWh ist ein echter Messwert
ergebnis = mittlerer_verbrauch([300, 0, -1])
assert ergebnis == 150, (
    f"mittlerer_verbrauch([300, 0, -1]) ergibt {ergebnis!r}, erwartet war 150.0.\n"
    "Tipp: Überspringen Sie nur den Wert -1, nicht die 0."
)

# Ohne gemessenen Monat ist das Ergebnis 0
for verbraeuche in [[-1, -1], []]:
    try:
        ergebnis = mittlerer_verbrauch(verbraeuche)
        fehler = None
    except ZeroDivisionError as ausnahme:
        ergebnis = None
        fehler = ausnahme
    assert fehler is None and ergebnis == 0, (
        f"mittlerer_verbrauch({verbraeuche}) ergibt {ergebnis!r} bzw. löst {fehler!r} aus, erwartet war 0.\n"
        "Tipp: Ist die Anzahl nach der Schleife 0, geben Sie 0 zurück, statt durch 0 zu teilen."
    )

# Eine for-Schleife wird benutzt
assert verwendet("for"), "Gehen Sie die Monate mit einer for-Schleife durch und überspringen Sie defekte mit continue."

# Die Ausgabe des Programms stimmt
assert AUSGABE == "500.0", f'Erwartete Ausgabe: "500.0" – Ihr Programm: "{AUSGABE}"'

# Viele zufällige Messreihen
zufall = Zufall(2007)
for _ in range(500):
    verbraeuche = []
    for _ in range(zufall.randint(0, 10)):
        # Defekte Monate (-1) und Monate mit 0 kWh sollen oft vorkommen
        verbraeuche.append(zufall.choice([-1, 0, zufall.randint(1, 1000)]))
    # Vergleichsrechnung: erst alle gemessenen Werte heraussuchen, dann mit sum und len teilen
    gemessen = [verbrauch for verbrauch in verbraeuche if verbrauch != -1]
    erwartet = sum(gemessen) / len(gemessen) if gemessen else 0
    ergebnis = mittlerer_verbrauch(verbraeuche)
    assert ergebnis is not None and abs(ergebnis - erwartet) < 0.000001, (
        f"mittlerer_verbrauch({verbraeuche}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    )

# An der oberen Grenze: 1000 Monate
for verbraeuche, erwartet in [
    ([100_000] * 1000, 100_000.0),
    ([-1] * 999 + [100_000], 100_000.0),
    ([-1] * 1000, 0),
    ([0, 100_000] * 500, 50_000.0),
]:
    ergebnis = mittlerer_verbrauch(verbraeuche)
    assert ergebnis == erwartet, (
        f"Bei 1000 Monaten, beginnend mit {verbraeuche[:3]}, ergibt mittlerer_verbrauch {ergebnis!r}, "
        f"erwartet war {erwartet}."
    )
