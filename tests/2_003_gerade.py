# Automatisch erzeugt aus lehrkraft/muster/2_003_gerade.py - nicht von Hand ändern.
# vorlage-hash: 4900cb5dd2b1e196

# Gerade Zahlen und ungerade Zahlen werden richtig erkannt
for zahl, erwartet in [(4, True), (7, False), (0, True), (-3, False)]:
    ergebnis = ist_gerade(zahl)
    assert ergebnis == erwartet, f"ist_gerade({zahl}) ergibt {ergebnis!r}, erwartet war {erwartet}."
