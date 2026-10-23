# Automatisch erzeugt aus lehrkraft/muster/25_verfuegbarkeit.py - nicht von Hand ändern.
# vorlage-hash: ddea4c56ca21b751

# Das Beispiel aus der Aufgabe: 30 Minuten Ausfall im Monat
ergebnis = verfuegbarkeit(30, 43200)
assert ergebnis is not None and abs(ergebnis - 99.93055555555556) < 0.000001, (
    f"verfuegbarkeit(30, 43200) ergibt {ergebnis!r}, erwartet war etwa 99.93055555555556.\n"
    "Tipp: Rechnen Sie (gesamt - ausfall) / gesamt * 100 und geben Sie das Ergebnis mit return zurück."
)

# Weitere Werte (nicht fest 99.93 hinschreiben!)
for ausfall, gesamt, erwartet in [
    (0, 43200, 100.0),
    (5, 1000, 99.5),
    (10, 200, 95.0),
    (432, 43200, 99.0),
    (100, 100, 0.0),
]:
    ergebnis = verfuegbarkeit(ausfall, gesamt)
    assert ergebnis is not None and abs(ergebnis - erwartet) < 0.000001, (
        f"verfuegbarkeit({ausfall}, {gesamt}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    )

# Die Reihenfolge der Parameter stimmt: erst Ausfall, dann gesamt
ergebnis = verfuegbarkeit(1, 4)
assert ergebnis == 75.0, (
    f"verfuegbarkeit(1, 4) ergibt {ergebnis!r}, erwartet war 75.0 (1 von 4 Minuten ausgefallen).\n"
    "Tipp: Der erste Parameter ist die Ausfallzeit, der zweite die Gesamtzeit."
)

# Das Ziel wird erreicht oder verfehlt
for ausfall, gesamt, ziel, erwartet in [
    (30, 43200, 99.9, True),
    (60, 43200, 99.9, False),
    (0, 43200, 99.99, True),
    (432, 43200, 99.5, False),
    (432, 43200, 98.5, True),
]:
    ergebnis = ziel_erreicht(ausfall, gesamt, ziel)
    assert ergebnis is erwartet, f"ziel_erreicht({ausfall}, {gesamt}, {ziel}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Genau erreicht zählt als erreicht
ergebnis = ziel_erreicht(5, 1000, 99.5)
assert ergebnis is True, (
    f"ziel_erreicht(5, 1000, 99.5) ergibt {ergebnis!r}, erwartet war True (die Verfügbarkeit ist genau 99.5).\n"
    "Tipp: „Mindestens“ heißt >=, nicht >."
)

# ziel_erreicht benutzt die Hilfsfunktion verfuegbarkeit
original_verfuegbarkeit = verfuegbarkeit
aufrufe = []


def spion(ausfall, gesamt):
    """Merkt sich jeden Aufruf und rechnet dann wie die echte Funktion."""
    aufrufe.append((ausfall, gesamt))
    return original_verfuegbarkeit(ausfall, gesamt)


try:
    verfuegbarkeit = spion
    ziel_erreicht(30, 43200, 99.9)
finally:
    verfuegbarkeit = original_verfuegbarkeit
assert aufrufe == [(30, 43200)], (
    f"ziel_erreicht(30, 43200, 99.9) hat verfuegbarkeit {len(aufrufe)}-mal aufgerufen, erwartet war einmal "
    "mit den Werten 30 und 43200.\n"
    "Tipp: Rechnen Sie in ziel_erreicht nicht selbst, sondern benutzen Sie das Ergebnis von verfuegbarkeit(ausfall, gesamt)."
)

# Die Ausgabe des Programms stimmt
assert AUSGABE == "99.93055555555556\nTrue", f"Erwartete Ausgabe:\n99.93055555555556\nTrue\nIhr Programm:\n{AUSGABE}"
