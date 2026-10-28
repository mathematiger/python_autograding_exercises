# Automatisch erzeugt aus lehrkraft/muster/2_005_wuerfel.py - nicht von Hand ändern.
# vorlage-hash: ec0ff9c294bcdae2
# thema: algorithmen
# inhalt: Raten und Prüfen

# 27 Klötze ergeben einen Würfel mit Kantenlänge 3
assert kantenlaenge(27) == 3, f"kantenlaenge(27) ergibt {kantenlaenge(27)!r}, erwartet war 3."

# Weitere Würfelzahlen (nicht fest 3 hinschreiben!)
for anzahl, erwartet in [(1, 1), (8, 2), (64, 4), (1000, 10), (1000000, 100)]:
    ergebnis = kantenlaenge(anzahl)
    assert ergebnis == erwartet, f"kantenlaenge({anzahl}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Geht es nicht auf, kommt -1 heraus
for anzahl in [2, 9, 26, 28, 30, 999]:
    ergebnis = kantenlaenge(anzahl)
    assert ergebnis == -1, (
        f"kantenlaenge({anzahl}) ergibt {ergebnis!r}, erwartet war -1, weil {anzahl} keine Würfelzahl ist.\n"
        "Tipp: Prüfen Sie nach der Schleife, ob k * k * k genau gleich anzahl ist."
    )

# Null Klötze ergeben Kantenlänge 0
assert kantenlaenge(0) == 0, (
    f"kantenlaenge(0) ergibt {kantenlaenge(0)!r}, erwartet war 0 (0 * 0 * 0 = 0).\n"
    "Tipp: Fangen Sie beim Raten mit k = 0 an."
)

# Es wird mit einer Schleife geraten
assert verwendet("while") or verwendet("for"), "Raten Sie die Kantenlänge mit einer Schleife."
