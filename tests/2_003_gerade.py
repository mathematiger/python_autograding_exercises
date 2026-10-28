# Automatisch erzeugt aus lehrkraft/muster/2_003_gerade.py - nicht von Hand ändern.
# vorlage-hash: a10d635da8f3362a
# thema: kontrollfluss
# inhalt: if und Funktionen

# Gerade Zahlen und ungerade Zahlen werden richtig erkannt
for zahl, erwartet in [(4, True), (7, False), (0, True), (-3, False)]:
    ergebnis = ist_gerade(zahl)
    assert ergebnis == erwartet, f"ist_gerade({zahl}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Viele zufällige Zahlen werden richtig erkannt
zufall = Zufall(2003)
for _ in range(1000):
    zahl = zufall.randint(-10**9, 10**9)
    # Vergleichsrechnung ohne %: Eine gerade Zahl ändert sich nicht, wenn man sie halbiert und wieder verdoppelt.
    erwartet = zahl // 2 * 2 == zahl
    ergebnis = ist_gerade(zahl)
    assert ergebnis == erwartet, f"ist_gerade({zahl}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Die Ränder der Grenzen
for zahl, erwartet in [(10**9, True), (10**9 - 1, False), (-10**9, True), (-10**9 + 1, False)]:
    ergebnis = ist_gerade(zahl)
    assert ergebnis == erwartet, f"ist_gerade({zahl}) ergibt {ergebnis!r}, erwartet war {erwartet}."
