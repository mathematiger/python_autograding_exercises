# Automatisch erzeugt aus lehrkraft/muster/2_020_sensorraster.py - nicht von Hand ändern.
# vorlage-hash: a9e5d58c4dd1b4fe
# text-hash: 1757b6674ec5e6f2
# thema: datenstrukturen
# inhalt: Listen von Listen

messungen = [
    [21, 22, 35],
    [21, 23, 41],
    [20, 22, 38],
]

# werte_von aus dem Beispiel
ergebnis = werte_von(messungen, 2)
assert ergebnis == [35, 41, 38], (
    f"werte_von(messungen, 2) ergibt {ergebnis!r}, erwartet war [35, 41, 38].\n"
    "Tipp: Nehmen Sie aus jeder Zeile den Wert an der Stelle sensor, also zeile[sensor]."
)

# Andere Sensoren (nicht fest hinschreiben!)
for sensor, erwartet in [(0, [21, 21, 20]), (1, [22, 23, 22])]:
    ergebnis = werte_von(messungen, sensor)
    assert ergebnis == erwartet, (
        f"werte_von(messungen, {sensor}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: messungen[sensor] ist eine Zeile (eine Messrunde), keine Spalte."
    )

# Eine Tabelle mit nur einer Zeile und eine mit nur einer Spalte
for tabelle, sensor, erwartet in [([[5, -50, 150]], 1, [-50]), ([[7], [8], [9], [10]], 0, [7, 8, 9, 10])]:
    ergebnis = werte_von(tabelle, sensor)
    assert ergebnis == erwartet, f"werte_von({tabelle}, {sensor}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# werte_von lässt die Tabelle unverändert
tabelle = [[1, 2], [3, 4]]
werte_von(tabelle, 1)
assert tabelle == [[1, 2], [3, 4]], f"Nach werte_von([[1, 2], [3, 4]], 1) ist die Tabelle {tabelle!r}, sie soll unverändert sein."

# ueberschreitungen aus dem Beispiel
ergebnis = ueberschreitungen(messungen, 36)
assert ergebnis == [(1, 2), (2, 2)], (
    f"ueberschreitungen(messungen, 36) ergibt {ergebnis!r}, erwartet war [(1, 2), (2, 2)].\n"
    "Tipp: Jedes Tupel ist (runde, sensor), also zuerst die Zeilennummer, dann die Spaltennummer."
)

# Lesereihenfolge und Grenzwert selbst
ergebnis = ueberschreitungen(messungen, 22)
erwartet = [(0, 2), (1, 1), (1, 2), (2, 2)]
assert ergebnis == erwartet, (
    f"ueberschreitungen(messungen, 22) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: Genau 22 ist nicht größer als 22. Die äußere Schleife geht über die Runden, die innere über die Sensoren."
)

# Keine Überschreitung und alle Werte darüber
for grenze, erwartet in [(150, []), (41, []), (-50, [(r, s) for r in range(3) for s in range(3)])]:
    ergebnis = ueberschreitungen(messungen, grenze)
    assert ergebnis == erwartet, f"ueberschreitungen(messungen, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Negative Werte und eine nicht quadratische Tabelle
tabelle = [[-10, -20, -30, -40], [-5, -45, -50, -1]]
ergebnis = ueberschreitungen(tabelle, -25)
erwartet = [(0, 0), (0, 1), (1, 0), (1, 3)]
assert ergebnis == erwartet, (
    f"ueberschreitungen({tabelle}, -25) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: Die Zeilen haben hier 4 Werte, es gibt aber nur 2 Zeilen; nehmen Sie len(messungen) und len(messungen[runde])."
)


# Vergleichslösung: über alle Positionen mit divmod
def ueberschreitungen_von_hand(tabelle, grenze):
    """Geht alle Positionen als laufende Nummer durch und rechnet runde und sensor daraus aus."""
    breite = len(tabelle[0])
    gefunden = []
    for nummer in range(len(tabelle) * breite):
        runde, sensor = divmod(nummer, breite)
        if tabelle[runde][sensor] > grenze:
            gefunden.append((runde, sensor))
    return gefunden


# 300 zufällige Tabellen
zufall = Zufall(2020)
for _ in range(300):
    zeilen = zufall.randint(1, 6)
    spalten = zufall.randint(1, 6)
    tabelle = [[zufall.randint(-50, 150) for _ in range(spalten)] for _ in range(zeilen)]
    grenze = zufall.randint(-50, 150)
    sensor = zufall.randrange(spalten)
    erwartet = [zeile[sensor] for zeile in tabelle]
    ergebnis = werte_von(tabelle, sensor)
    assert ergebnis == erwartet, f"werte_von({tabelle}, {sensor}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    erwartet = ueberschreitungen_von_hand(tabelle, grenze)
    ergebnis = ueberschreitungen(tabelle, grenze)
    assert ergebnis == erwartet, f"ueberschreitungen({tabelle}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# An der oberen Grenze: 1000 Runden mit je 100 Sensoren
gross = [[(runde * 7 + sensor * 3) % 201 - 50 for sensor in range(100)] for runde in range(1000)]
spalte = werte_von(gross, 99)
stellen = ueberschreitungen(gross, 148)
erwartet = ueberschreitungen_von_hand(gross, 148)
assert len(spalte) == 1000 and spalte[:3] == [46, 53, 60] and stellen == erwartet, (
    f"Bei 1000 Runden mit je 100 Sensoren liefert werte_von(…, 99) {len(spalte)} Werte, beginnend mit {spalte[:3]}, "
    f"und ueberschreitungen(…, 148) {len(stellen)} Stellen, die ersten {stellen[:2]}; erwartet waren 1000 Werte, "
    f"beginnend mit [46, 53, 60], und {len(erwartet)} Stellen in Lesereihenfolge, die ersten {erwartet[:2]}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[35, 41, 38]\n[(1, 2), (2, 2)]"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
