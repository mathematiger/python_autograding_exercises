# Automatisch erzeugt aus lehrkraft/muster/3_013_testquoten.py - nicht von Hand ändern.
# vorlage-hash: 9c3d2459d43e23bd
# text-hash: d433713ae3e1f796
# thema: datenanalyse
# inhalt: numpy: Arrays, elementweise rechnen

def ist_nah(ergebnis, erwartet):
    """True, wenn ergebnis ein numpy-Array ist, das bis auf Rundungsfehler die Werte aus erwartet hat."""
    if not isinstance(ergebnis, np.ndarray) or ergebnis.shape != (len(erwartet),):
        return False
    for wert, soll in zip(ergebnis.tolist(), erwartet):
        # Relativ zur Größe, weil je nach Rechenweg (erst teilen, dann malnehmen) die letzten Stellen abweichen
        if abs(wert - soll) > 1e-9 * max(1, abs(soll)):
            return False
    return True


# erfolgsquoten: das Beispiel aus der Aufgabe
ergebnis = erfolgsquoten([40, 25, 8], [2, 0, 4])
assert ist_nah(ergebnis, [95.0, 100.0, 50.0]), (
    f"erfolgsquoten([40, 25, 8], [2, 0, 4]) ergibt {ergebnis!r}, erwartet war array([95., 100., 50.]).\n"
    "Tipp: Mit Listen kann man nicht elementweise rechnen; wandeln Sie sie zuerst mit np.array(...) um."
)

# erfolgsquoten liefert ein numpy-Array
assert isinstance(erfolgsquoten([10], [1]), np.ndarray), (
    f"erfolgsquoten([10], [1]) ergibt {erfolgsquoten([10], [1])!r}, erwartet war ein numpy-Array, kein {type(erfolgsquoten([10], [1])).__name__}."
)

# erfolgsquoten mit anderen Werten (nicht fest hinschreiben!)
for tests, fehlgeschlagen, erwartet in [
    ([3, 1000, 7], [1, 999, 7], [200 / 3, 0.1, 0.0]),
    ([1], [0], [100.0]),
    ([1], [1], [0.0]),
    ([10**6, 1], [1, 0], [99.9999, 100.0]),
]:
    ergebnis = erfolgsquoten(tests, fehlgeschlagen)
    assert ist_nah(ergebnis, erwartet), (
        f"erfolgsquoten({tests}, {fehlgeschlagen}) ergibt {ergebnis!r}, erwartet war ungefähr {erwartet}."
    )

# Ohne Module kommt ein leeres Array heraus
ergebnis = erfolgsquoten([], [])
assert isinstance(ergebnis, np.ndarray) and len(ergebnis) == 0, (
    f"erfolgsquoten([], []) ergibt {ergebnis!r}, erwartet war ein leeres numpy-Array."
)

# analyseaufwand: das Beispiel aus der Aufgabe
ergebnis = analyseaufwand([2, 0, 4], 45)
assert ist_nah(ergebnis, [1.5, 0.0, 3.0]), (
    f"analyseaufwand([2, 0, 4], 45) ergibt {ergebnis!r}, erwartet war array([1.5, 0., 3.]).\n"
    "Tipp: Fehler mal Minuten ergibt Minuten; durch 60 geteilt sind es Stunden. "
    "[2, 0, 4] * 45 hängt die Liste 45-mal aneinander, erst ein Array rechnet elementweise."
)

# analyseaufwand mit anderen Werten, auch mit 0 Minuten
for fehlgeschlagen, minuten, erwartet in [
    ([1, 3, 10], 20, [1 / 3, 1.0, 10 / 3]),
    ([5, 7], 0, [0.0, 0.0]),
    ([10**6], 600, [10**7]),
    ([], 30, []),
]:
    ergebnis = analyseaufwand(fehlgeschlagen, minuten)
    assert ist_nah(ergebnis, erwartet), (
        f"analyseaufwand({fehlgeschlagen}, {minuten}) ergibt {ergebnis!r}, erwartet war ungefähr {erwartet}."
    )

# Die Eingabelisten bleiben unverändert
tests = [40, 25, 8]
fehlgeschlagen = [2, 0, 4]
erfolgsquoten(tests, fehlgeschlagen)
analyseaufwand(fehlgeschlagen, 45)
assert (tests, fehlgeschlagen) == ([40, 25, 8], [2, 0, 4]), (
    f"Nach den Aufrufen sind die Listen {tests} und {fehlgeschlagen}, erwartet war, dass sie unverändert bleiben."
)

# 300 zufällige Testläufe, verglichen mit einer Rechnung über Listen
zufall = Zufall(3013)
for _ in range(300):
    anzahl = zufall.randint(0, 12)
    tests = [zufall.choice([zufall.randint(1, 20), zufall.randint(1, 10**6)]) for _ in range(anzahl)]
    fehlgeschlagen = [zufall.choice([0, anzahl_tests, zufall.randint(0, anzahl_tests)]) for anzahl_tests in tests]
    minuten = zufall.randint(0, 600)
    erwartet_quoten = [100 - 100 * fehler / gesamt for gesamt, fehler in zip(tests, fehlgeschlagen)]
    erwartet_aufwand = [fehler * minuten / 60 for fehler in fehlgeschlagen]
    ergebnis = erfolgsquoten(tests, fehlgeschlagen)
    assert ist_nah(ergebnis, erwartet_quoten), (
        f"erfolgsquoten({tests}, {fehlgeschlagen}) ergibt {ergebnis!r}, erwartet war ungefähr {erwartet_quoten}."
    )
    ergebnis = analyseaufwand(fehlgeschlagen, minuten)
    assert ist_nah(ergebnis, erwartet_aufwand), (
        f"analyseaufwand({fehlgeschlagen}, {minuten}) ergibt {ergebnis!r}, erwartet war ungefähr {erwartet_aufwand}."
    )

# An der oberen Grenze ohne Python-Schleife: 100 000 Module
tests = [10**6] * 50000 + [4] * 50000
fehlgeschlagen = [10**6] * 50000 + [1] * 50000
quoten, schritte_quoten = zaehle_schritte(erfolgsquoten, tests, fehlgeschlagen)
aufwand, schritte_aufwand = zaehle_schritte(analyseaufwand, fehlgeschlagen, 600)
assert len(quoten) == 100000 and quoten[0] == 0 and quoten[-1] == 75 and aufwand[0] == 10**7 and aufwand[-1] == 10, (
    "Bei 100 000 Modulen stimmen die Ergebnisse nicht: erfolgsquoten liefert am Anfang und Ende "
    f"{quoten[0]!r} und {quoten[-1]!r} (erwartet 0 und 75), analyseaufwand {aufwand[0]!r} und {aufwand[-1]!r} "
    "(erwartet 10000000 und 10)."
)
assert schritte_quoten <= 10 and schritte_aufwand <= 10, (
    f"Bei 100 000 Modulen brauchen erfolgsquoten und analyseaufwand {schritte_quoten} und {schritte_aufwand} "
    "ausgeführte Zeilen, erwartet waren je höchstens 10.\n"
    "Tipp: Rechnen Sie mit ganzen Arrays statt mit einer Schleife über die Module."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[95.0, 100.0, 50.0]\n[1.5, 0.0, 3.0]"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
