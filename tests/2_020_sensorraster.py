# Automatisch erzeugt aus lehrkraft/muster/2_020_sensorraster.py - nicht von Hand ändern.
# vorlage-hash: a9e5d58c4dd1b4fe
# text-hash: 3e69d549c20de1ef
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



def als_tupel(stellen):
    """Macht aus Einträgen, die Listen sind, Tupel, damit erst der Inhalt und später die Form geprüft wird."""
    if not isinstance(stellen, list):
        return stellen
    return [tuple(stelle) if isinstance(stelle, list) else stelle for stelle in stellen]


# ueberschreitungen aus dem Beispiel (ob Tupel oder Liste, zählt hier noch nicht)
ergebnis = ueberschreitungen(messungen, 36)
assert als_tupel(ergebnis) == [(1, 2), (2, 2)], (
    f"ueberschreitungen(messungen, 36) ergibt {ergebnis!r}, erwartet war [(1, 2), (2, 2)].\n"
    "Tipp: Jedes Tupel ist (runde, sensor), also zuerst die Zeilennummer, dann die Spaltennummer."
)

# Jede Stelle ist ein Tupel (runde, sensor)
ergebnis = ueberschreitungen(messungen, 36)
assert ergebnis == [(1, 2), (2, 2)], (
    f"ueberschreitungen(messungen, 36) ergibt {ergebnis!r}, erwartet war [(1, 2), (2, 2)].\n"
    "Tipp: Jede Stelle soll ein Tupel sein, keine Liste: stellen.append((runde, sensor)) mit doppelten runden Klammern."
)

# Genau der Grenzwert ist keine Überschreitung
ergebnis = ueberschreitungen(messungen, 38)
assert als_tupel(ergebnis) == [(1, 2)], (
    f"ueberschreitungen(messungen, 38) ergibt {ergebnis!r}, erwartet war [(1, 2)].\n"
    "Tipp: Genau 38 ist nicht größer als 38; vergleichen Sie mit > statt mit >=."
)

# Die Stellen kommen in Lesereihenfolge: erst ganz Runde 0, dann Runde 1
tabelle = [[9, 9], [9, 0]]
ergebnis = ueberschreitungen(tabelle, 5)
erwartet = [(0, 0), (0, 1), (1, 0)]
if isinstance(ergebnis, list) and sorted(als_tupel(ergebnis)) == erwartet:
    hinweis = (
        "\nTipp: Die Stellen stimmen, nur die Reihenfolge nicht. "
        "Die äußere Schleife geht über die Runden, die innere über die Sensoren."
    )
else:
    hinweis = ""
assert als_tupel(ergebnis) == erwartet, f"ueberschreitungen({tabelle}, 5) ergibt {ergebnis!r}, erwartet war {erwartet}.{hinweis}"

# Das zweite Beispiel aus der Aufgabe
ergebnis = ueberschreitungen(messungen, 22)
erwartet = [(0, 2), (1, 1), (1, 2), (2, 2)]
assert als_tupel(ergebnis) == erwartet, (
    f"ueberschreitungen(messungen, 22) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: Genau 22 ist nicht größer als 22. Die äußere Schleife geht über die Runden, die innere über die Sensoren."
)

# Keine Überschreitung und alle Werte darüber
for grenze, erwartet in [(150, []), (41, []), (-50, [(r, s) for r in range(3) for s in range(3)])]:
    ergebnis = ueberschreitungen(messungen, grenze)
    assert als_tupel(ergebnis) == erwartet, f"ueberschreitungen(messungen, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Negative Werte und eine nicht quadratische Tabelle
tabelle = [[-10, -20, -30, -40], [-5, -45, -50, -1]]
ergebnis = ueberschreitungen(tabelle, -25)
erwartet = [(0, 0), (0, 1), (1, 0), (1, 3)]
assert als_tupel(ergebnis) == erwartet, (
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


# 300 zufällige Tabellen für werte_von
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

# 300 zufällige Tabellen für ueberschreitungen
zufall = Zufall(2020)
for _ in range(300):
    zeilen = zufall.randint(1, 6)
    spalten = zufall.randint(1, 6)
    tabelle = [[zufall.randint(-50, 150) for _ in range(spalten)] for _ in range(zeilen)]
    grenze = zufall.randint(-50, 150)
    sensor = zufall.randrange(spalten)
    erwartet = ueberschreitungen_von_hand(tabelle, grenze)
    ergebnis = ueberschreitungen(tabelle, grenze)
    assert als_tupel(ergebnis) == erwartet, f"ueberschreitungen({tabelle}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# An der oberen Grenze: werte_von bei 1000 Runden mit je 100 Sensoren
gross = [[(runde * 7 + sensor * 3) % 201 - 50 for sensor in range(100)] for runde in range(1000)]
spalte = werte_von(gross, 99)
assert len(spalte) == 1000 and spalte[:3] == [46, 53, 60], (
    f"Bei 1000 Runden mit je 100 Sensoren liefert werte_von(…, 99) {len(spalte)} Werte, beginnend mit {spalte[:3]}; "
    "erwartet waren 1000 Werte, beginnend mit [46, 53, 60]."
)

# An der oberen Grenze: ueberschreitungen bei 1000 Runden mit je 100 Sensoren
stellen = ueberschreitungen(gross, 148)
erwartet = ueberschreitungen_von_hand(gross, 148)
assert als_tupel(stellen) == erwartet, (
    f"Bei 1000 Runden mit je 100 Sensoren liefert ueberschreitungen(…, 148) {len(stellen)} Stellen, "
    f"die ersten {stellen[:2]}; erwartet waren {len(erwartet)} Stellen in Lesereihenfolge, die ersten {erwartet[:2]}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[35, 41, 38]\n[(1, 2), (2, 2)]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
