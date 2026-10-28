# Automatisch erzeugt aus lehrkraft/muster/3_001_suche.py - nicht von Hand ändern.
# vorlage-hash: b11625cd0b936867
# thema: algorithmen
# inhalt: Lineare Suche

# Element in der Mitte wird gefunden
assert finde([41, 7, 23, 7], 23) == 2, f"finde([41, 7, 23, 7], 23) ergibt {finde([41, 7, 23, 7], 23)!r}, erwartet war 2."

# Erstes Vorkommen zählt
assert finde([41, 7, 23, 7], 7) == 1, (
    f"finde([41, 7, 23, 7], 7) ergibt {finde([41, 7, 23, 7], 7)!r}, erwartet war 1 (das erste Vorkommen)."
)

# Element am Anfang und am Ende
for liste, gesucht, erwartet in [([5, 6, 7], 5, 0), ([5, 6, 7], 7, 2)]:
    ergebnis = finde(liste, gesucht)
    assert ergebnis == erwartet, f"finde({liste}, {gesucht}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Nicht vorhanden ergibt -1
assert finde([41, 7, 23, 7], 99) == -1, (
    f"finde([41, 7, 23, 7], 99) ergibt {finde([41, 7, 23, 7], 99)!r}, erwartet war -1.\n"
    "Tipp: Das return -1 gehört hinter die Schleife, nicht in sie hinein."
)

# Leere Liste ergibt -1
assert finde([], 5) == -1, f"finde([], 5) ergibt {finde([], 5)!r}, erwartet war -1."

# Funktioniert auch mit Texten
assert finde(["a", "b"], "b") == 1, f'finde(["a", "b"], "b") ergibt {finde(["a", "b"], "b")!r}, erwartet war 1.'

# Eine Schleife wird benutzt, nicht liste.index
assert verwendet("for") or verwendet("while"), "Suchen Sie mit einer Schleife, nicht mit liste.index(...)."

# Viele zufällige Regale, auch mit doppelten Nummern (nicht fest hinschreiben!)
zufall = Zufall(3001)
for runde in range(500):
    liste = [zufall.randint(0, 9) for _ in range(runde // 25)]
    gesucht = zufall.randint(0, 11)
    erwartet = liste.index(gesucht) if gesucht in liste else -1
    ergebnis = finde(liste, gesucht)
    assert ergebnis == erwartet, f"finde({liste}, {gesucht}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ein volles Regal mit 10 000 Büchern (Nummern 19998, 19996, …, 0)
regal = list(range(19998, -1, -2))
for gesucht, erwartet in [(19998, 0), (10000, 4999), (0, 9999), (7, -1), (999999, -1)]:
    ergebnis = finde(regal, gesucht)
    assert ergebnis == erwartet, (
        f"In list(range(19998, -1, -2)) ergibt finde(..., {gesucht}) {ergebnis!r}, erwartet war {erwartet}."
    )

# Beim ersten Treffer ist Schluss
messliste = Zaehlliste(range(10000))
ergebnis = finde(messliste, 20)
assert ergebnis == 20 and messliste.lesezugriffe <= 50, (
    f"Die Suche nach 20 in einer Liste mit den Zahlen 0 bis 9999 ergibt {ergebnis!r} und hat "
    f"{messliste.lesezugriffe} Elemente angesehen; erwartet waren 20 und nur wenige angesehene Elemente (21 genügen).\n"
    "Tipp: Geben Sie den Index mit return zurück, sobald Sie ihn gefunden haben, statt weiterzusuchen."
)
