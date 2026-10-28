# Automatisch erzeugt aus lehrkraft/muster/3_002_binaere_suche.py - nicht von Hand ändern.
# vorlage-hash: ee10cd699339b8d9
# thema: algorithmen
# inhalt: Binäre Suche

# Element in der Mitte und daneben wird gefunden
for gesucht, erwartet in [(15, 2), (23, 3), (8, 1)]:
    ergebnis = binaere_suche([3, 8, 15, 23, 42], gesucht)
    assert ergebnis == erwartet, f"binaere_suche([3, 8, 15, 23, 42], {gesucht}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Erstes und letztes Element werden gefunden
for gesucht, erwartet in [(3, 0), (42, 4)]:
    ergebnis = binaere_suche([3, 8, 15, 23, 42], gesucht)
    assert ergebnis == erwartet, (
        f"binaere_suche([3, 8, 15, 23, 42], {gesucht}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Der Bereich reicht von 0 bis len(liste) - 1, und die Schleife läuft, solange links <= rechts."
    )

# Nicht vorhandene Werte ergeben -1, auch kleiner oder größer als alle
for gesucht in [10, 1, 50, 24]:
    ergebnis = binaere_suche([3, 8, 15, 23, 42], gesucht)
    assert ergebnis == -1, f"binaere_suche([3, 8, 15, 23, 42], {gesucht}) ergibt {ergebnis!r}, erwartet war -1."

# Leere Liste und Liste mit einem Element
for liste, gesucht, erwartet in [([], 5, -1), ([7], 7, 0), ([7], 3, -1), ([7], 9, -1)]:
    ergebnis = binaere_suche(liste, gesucht)
    assert ergebnis == erwartet, f"binaere_suche({liste}, {gesucht}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Jede Nummer in einer längeren Liste wird gefunden
regal = list(range(0, 300, 3))
for index in range(len(regal)):
    ergebnis = binaere_suche(regal, regal[index])
    assert ergebnis == index, f"In list(range(0, 300, 3)) ergibt die Suche nach {regal[index]} {ergebnis!r}, erwartet war {index}."


# Bei 1000 Einträgen reichen wenige Zugriffe (binäre statt linearer Suche)
messliste = Zaehlliste(list(range(1000)))
for gesucht in [0, 499, 998, 999, 1000, -1]:
    binaere_suche(messliste, gesucht)
assert messliste.lesezugriffe <= 6 * 25, (
    f"Für sechs Suchen in einer Liste mit 1000 Einträgen hat Ihre Funktion {messliste.lesezugriffe} Elemente angesehen, "
    "erlaubt sind höchstens 150 (etwa 20 pro Suche).\n"
    "Tipp: Halbieren Sie den Suchbereich in jedem Schritt, statt alle Elemente durchzugehen."
)

# Viele zufällige sortierte Listen, auch mit negativen Nummern (nicht fest hinschreiben!)
zufall = Zufall(3002)
for runde in range(600):
    liste = sorted(zufall.sample(range(-60, 60), runde // 30))
    gesucht = zufall.randint(-65, 65)
    erwartet = liste.index(gesucht) if gesucht in liste else -1
    ergebnis = binaere_suche(liste, gesucht)
    assert ergebnis == erwartet, f"binaere_suche({liste}, {gesucht}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Eine Million Nummern: Jede Suche kommt mit wenigen Zugriffen aus
messliste = Zaehlliste(range(-10**9, 10**9, 2000))
for gesucht, erwartet in [
    (-10**9, 0),
    (10**9 - 2000, 999999),
    (-10**9 + 2000 * 123456, 123456),
    (-10**9 + 1, -1),
    (10**9, -1),
]:
    vorher = messliste.lesezugriffe
    ergebnis = binaere_suche(messliste, gesucht)
    zugriffe = messliste.lesezugriffe - vorher
    assert ergebnis == erwartet and zugriffe <= 50, (
        f"In list(range(-10**9, 10**9, 2000)) mit einer Million Nummern ergibt die Suche nach {gesucht} "
        f"{ergebnis!r} nach {zugriffe} angesehenen Elementen; erwartet war {erwartet} nach höchstens 50.\n"
        "Tipp: Bei O(log n) reichen für eine Million Einträge etwa 20 Halbierungen des Suchbereichs."
    )
