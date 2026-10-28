# Automatisch erzeugt aus lehrkraft/muster/2_012_uebertragung.py - nicht von Hand ändern.
# vorlage-hash: af8c51a49c4da964
# thema: funktionen
# inhalt: Lokale und globale Variablen

# Das Beispiel aus der Aufgabe: 250 MB bei 100 Mbit/s
ergebnis = dauer(250, 100)
assert ergebnis == 20.0, f"dauer(250, 100) ergibt {ergebnis!r}, erwartet war 20.0."

# Andere Bandbreiten werden berücksichtigt
for megabyte, mbit, erwartet in [(250, 50, 40.0), (1000, 1000, 8.0), (100, 16, 50.0), (10, 3, 26.7), (0, 100, 0.0)]:
    ergebnis = dauer(megabyte, mbit)
    if ergebnis == round(megabyte * 8 / 100, 1) and mbit != 100:
        hinweis = "\nTipp: Ihre Funktion rechnet immer mit 100 Mbit/s. Benutzen Sie den Parameter mbit_pro_sekunde."
    else:
        hinweis = ""
    assert ergebnis == erwartet, f"dauer({megabyte}, {mbit}) ergibt {ergebnis!r}, erwartet war {erwartet}.{hinweis}"

# Die globale Variable bandbreite spielt keine Rolle
bandbreite = 1
ergebnis = dauer(250, 100)
bandbreite = 100
assert ergebnis == 20.0, (
    f"Wenn die globale Variable bandbreite 1 ist, ergibt dauer(250, 100) {ergebnis!r}, erwartet war 20.0.\n"
    "Tipp: Die Funktion soll nur mit ihren Parametern rechnen, nicht mit globalen Variablen."
)

# Das Beispiel aus der Aufgabe: drei Dateien bei 100 Mbit/s
ergebnis = gesamtdauer([250, 125, 50], 100)
assert ergebnis == 34.0, f"gesamtdauer([250, 125, 50], 100) ergibt {ergebnis!r}, erwartet war 34.0."

# Weitere Backups (nicht fest hinschreiben!)
for dateien, mbit, erwartet in [([500, 500], 1000, 8.0), ([10, 20, 30, 40], 16, 50.0), ([1, 2, 3], 4, 12.0), ([250], 50, 40.0), ([10], 3, 26.7)]:
    ergebnis = gesamtdauer(dateien, mbit)
    assert ergebnis == erwartet, f"gesamtdauer({dateien}, {mbit}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Eine leere Liste dauert 0 Sekunden
ergebnis = gesamtdauer([], 100)
assert ergebnis == 0, f"gesamtdauer([], 100) ergibt {ergebnis!r}, erwartet war 0."

# Mehrere Aufrufe hintereinander liefern jedes Mal dasselbe
ergebnisse = [gesamtdauer([250, 125, 50], 100) for _ in range(3)]
assert ergebnisse == [34.0, 34.0, 34.0], (
    f"Dreimal gesamtdauer([250, 125, 50], 100) hintereinander ergibt {ergebnisse!r}, erwartet war jedes Mal 34.0.\n"
    "Tipp: Eine globale Summe wächst bei jedem Aufruf weiter. Legen Sie die Summe als lokale Variable "
    "in der Funktion an, vor der Schleife."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "250 MB bei 100 Mbit/s: 20.0 Sekunden\n250 MB bei 50 Mbit/s: 40.0 Sekunden\nBackup bei 100 Mbit/s: 34.0 Sekunden"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
