# Automatisch erzeugt aus lehrkraft/muster/2_003_gerade.py - nicht von Hand ändern.
# vorlage-hash: 626fbab96c481c61
# text-hash: 4c98d7a3126b136f
# thema: kontrollfluss
# inhalt: if und Funktionen

def meldung(zahl, ergebnis, erwartet):
    """Baut die Fehlermeldung; bei einem Text statt eines Wahrheitswerts mit Tipp."""
    text = f"ist_gerade({zahl}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    if isinstance(ergebnis, str):
        text += "\nTipp: True und False sind Wahrheitswerte und stehen ohne Anführungszeichen."
    if ergebnis is None:
        text += "\nTipp: Die Funktion liefert None. Für ungerade Zahlen fehlt return False."
    return text


# Das Beispiel aus der Aufgabe: 4 ist gerade
ergebnis = ist_gerade(4)
if ergebnis == False:
    hinweis = "\nTipp: Gerade heißt: Beim Teilen durch 2 bleibt kein Rest, also zahl % 2 == 0 (nicht zahl / 2)."
else:
    hinweis = ""
assert ergebnis == True, meldung(4, ergebnis, True) + hinweis

# Das Beispiel aus der Aufgabe: 7 ist ungerade
ergebnis = ist_gerade(7)
assert ergebnis == False, meldung(7, ergebnis, False)

# 0 ist gerade
ergebnis = ist_gerade(0)
assert ergebnis == True, meldung(0, ergebnis, True)

# Negative Zahlen: -3 ist ungerade
ergebnis = ist_gerade(-3)
assert ergebnis == False, meldung(-3, ergebnis, False)

# Viele zufällige Zahlen werden richtig erkannt
zufall = Zufall(2003)
for _ in range(1000):
    zahl = zufall.randint(-10**9, 10**9)
    # Vergleichsrechnung ohne %: Eine gerade Zahl ändert sich nicht, wenn man sie halbiert und wieder verdoppelt.
    erwartet = zahl // 2 * 2 == zahl
    ergebnis = ist_gerade(zahl)
    assert ergebnis == erwartet, meldung(zahl, ergebnis, erwartet)

# ist_gerade liefert einen Wahrheitswert, keine Zahl und keinen Text
for zahl in [4, 7]:
    ergebnis = ist_gerade(zahl)
    if ergebnis is None:
        typ_tipp = "Tipp: Für ungerade Zahlen fehlt return False."
    else:
        typ_tipp = "Tipp: Ein Vergleich wie zahl % 2 == 0 liefert schon True oder False."
    assert type(ergebnis) is bool, (
        f"ist_gerade({zahl}) ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war True oder False.\n"
        + typ_tipp
    )

# Die Ränder der Grenzen
for zahl, erwartet in [(10**9, True), (10**9 - 1, False), (-10**9, True), (-10**9 + 1, False)]:
    ergebnis = ist_gerade(zahl)
    assert ergebnis == erwartet, meldung(zahl, ergebnis, erwartet)
