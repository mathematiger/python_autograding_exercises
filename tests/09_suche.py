# Automatisch erzeugt aus lehrkraft/muster/09_suche.py - nicht von Hand ändern.
# vorlage-hash: f604efe87fbd81db

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
