# Automatisch erzeugt aus lehrkraft/muster/2_002_verdoppeln.py - nicht von Hand ändern.
# vorlage-hash: 38fe960c08ce63fe
# thema: funktionen
# inhalt: Funktionen mit return

# verdopple gibt etwas zurück
assert verdopple(3) is not None, "verdopple(3) gibt nichts zurück – haben Sie return vergessen oder print benutzt?"

# verdopple(3) ist 6
assert verdopple(3) == 6, f"verdopple(3) ergibt {verdopple(3)!r}, erwartet war 6."

# verdopple(-4) ist -8
assert verdopple(-4) == -8, f"verdopple(-4) ergibt {verdopple(-4)!r}, erwartet war -8."

# Viele zufällige Zahlen werden richtig verdoppelt
zufall = Zufall(2002)
for _ in range(1000):
    zahl = zufall.randint(-10**9, 10**9)
    ergebnis = verdopple(zahl)
    assert ergebnis == zahl + zahl, f"verdopple({zahl}) ergibt {ergebnis!r}, erwartet war {zahl + zahl}."

# Die Ränder der Grenzen: 0, -10**9 und 10**9
for zahl, erwartet in [(0, 0), (-10**9, -2 * 10**9), (10**9, 2 * 10**9)]:
    ergebnis = verdopple(zahl)
    assert ergebnis == erwartet, f"verdopple({zahl}) ergibt {ergebnis!r}, erwartet war {erwartet}."
