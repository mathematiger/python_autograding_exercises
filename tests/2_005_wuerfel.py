# Automatisch erzeugt aus lehrkraft/muster/2_005_wuerfel.py - nicht von Hand ändern.
# vorlage-hash: 046588e3d957c8c3
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

# Viele zufällige Anzahlen, Würfelzahlen und knapp daneben
zufall = Zufall(2005)
wuerfelzahlen = {k * k * k: k for k in range(101)}
for durchlauf in range(200):
    if durchlauf % 2 == 0:
        anzahl = zufall.randint(0, 10**4)
    else:
        anzahl = max(zufall.randint(0, 21) ** 3 + zufall.randint(-1, 1), 0)
    erwartet = wuerfelzahlen.get(anzahl, -1)
    ergebnis = kantenlaenge(anzahl)
    assert ergebnis == erwartet, f"kantenlaenge({anzahl}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Die obere Grenze 10**6 und knapp darunter
for anzahl, erwartet in [(10**6, 100), (10**6 - 1, -1), (99**3, 99), (99**3 + 1, -1)]:
    ergebnis = kantenlaenge(anzahl)
    assert ergebnis == erwartet, f"kantenlaenge({anzahl}) ergibt {ergebnis!r}, erwartet war {erwartet}."
