# Automatisch erzeugt aus lehrkraft/muster/3_033_ablaufvarianten.py - nicht von Hand ändern.
# vorlage-hash: 349f2c9264f694f3
# text-hash: ba404c26b5441492
# thema: algorithmen
# inhalt: Memoisierung mit Dictionary

def ablaeufe_vergleich(n):
    """Vergleichslösung mit einer Schleife: immer die letzten beiden Werte merken."""
    vorletzter, letzter = 1, 1
    for _ in range(n - 1):
        vorletzter, letzter = letzter, vorletzter + letzter
    return letzter


def meldung(n, ergebnis):
    """Baut die Fehlermeldung mit Eingabe, Ergebnis und erwartetem Wert."""
    return f"ablaeufe({n}) ergibt {ergebnis!r}, erwartet war {ablaeufe_vergleich(n)}."


# Das Beispiel aus der Aufgabe: 4 Schritte, 5 Abläufe
ergebnis = ablaeufe(4)
assert ergebnis == 5, meldung(4, ergebnis) + "\nTipp: ablaeufe(n) = ablaeufe(n - 1) + ablaeufe(n - 2)."

# Ein anderer Wert: 10 Schritte, 89 Abläufe (nicht fest hinschreiben!)
ergebnis = ablaeufe(10)
assert ergebnis == 89, meldung(10, ergebnis)

# Kleine Werte: 1, 2 und 3 Schritte
for n in [1, 2, 3]:
    ergebnis = ablaeufe(n)
    assert ergebnis == ablaeufe_vergleich(n), meldung(n, ergebnis) + "\nTipp: ablaeufe(0) und ablaeufe(1) sind beide 1."

# Kein Schritt: genau ein Ablauf (nichts tun)
ergebnis = ablaeufe(0)
assert ergebnis == 1, meldung(0, ergebnis)

# Hilfen für die nächsten Tests: Aufrufe über den Namen ablaeufe mitschreiben
aufrufe = []
echte_ablaeufe = ablaeufe


def ablaeufe_mitschreiben(n):
    """Merkt sich den Aufruf und rechnet mit der Lösung weiter."""
    aufrufe.append(n)
    return echte_ablaeufe(n)


def zaehle_rekursive_aufrufe(n):
    """Leert bekannt, ruft ablaeufe(n) auf und liefert die Liste der Aufrufe über den Namen ablaeufe."""
    global ablaeufe
    bekannt.clear()
    aufrufe.clear()
    ablaeufe = ablaeufe_mitschreiben
    try:
        echte_ablaeufe(n)
    finally:
        ablaeufe = echte_ablaeufe
    return list(aufrufe)


# ablaeufe arbeitet rekursiv: ablaeufe(6) ruft ablaeufe wieder auf
rekursiv = zaehle_rekursive_aufrufe(6)
assert len(rekursiv) > 0, (
    "ablaeufe(6) ruft ablaeufe nicht wieder auf. Die Aufgabe verlangt eine rekursive Lösung: "
    "ablaeufe(n) = ablaeufe(n - 1) + ablaeufe(n - 2)."
)

# Teilergebnisse landen im Dictionary bekannt
bekannt.clear()
ergebnis = ablaeufe(20)
assert ergebnis == 10946 and bekannt.get(15) == 987 and bekannt.get(19) == 6765, (
    f"Nach ablaeufe(20) (Ergebnis {ergebnis!r}, erwartet 10946) sollen im Dictionary bekannt die "
    f"Teilergebnisse stehen, z. B. bekannt[15] = 987 und bekannt[19] = 6765; gefunden: "
    f"bekannt[15] = {bekannt.get(15)!r}, bekannt[19] = {bekannt.get(19)!r}.\n"
    "Tipp: Tragen Sie jedes berechnete Ergebnis mit bekannt[n] = ergebnis ein, bevor Sie es zurückgeben."
)

# Jeder Wert wird nur einmal berechnet: ablaeufe(25) braucht nur wenige rekursive Aufrufe
rekursiv = zaehle_rekursive_aufrufe(25)
assert len(rekursiv) <= 3 * 25, (
    f"ablaeufe(25) mit leerem bekannt ruft sich {len(rekursiv)}-mal selbst auf; mit Memoisierung reichen "
    "etwa 2 · 25 = 50 Aufrufe.\n"
    "Tipp: Schauen Sie am Anfang der Funktion mit if n in bekannt nach, ob das Ergebnis schon da ist, und "
    "geben Sie es dann sofort zurück."
)

# Ein schon bekannter Wert wird nur nachgeschlagen
bekannt.clear()
ablaeufe(30)
ergebnis, schritte = zaehle_schritte(ablaeufe, 30)
assert ergebnis == 1346269 and schritte <= 10, (
    f"Ein zweiter Aufruf ablaeufe(30) ergibt {ergebnis!r} (erwartet 1346269) und braucht {schritte} Schritte; "
    "weil das Ergebnis schon in bekannt steht, sollten wenige Schritte reichen (höchstens 10)."
)

# Alle Werte von 0 bis 90, auch mit leerem Dictionary vorher
for n in range(91):
    bekannt.clear()
    ergebnis = ablaeufe(n)
    assert ergebnis == ablaeufe_vergleich(n), meldung(n, ergebnis)

# 200 zufällige Werte, das Dictionary bleibt dazwischen gefüllt
zufall = Zufall(3033)
bekannt.clear()
for _ in range(200):
    n = zufall.randint(0, 400)
    ergebnis = ablaeufe(n)
    assert ergebnis == ablaeufe_vergleich(n), meldung(n, ergebnis)

# Obere Grenze: 500 Schritte mit leerem Dictionary, in O(n) Schritten
bekannt.clear()
ergebnis, schritte = zaehle_schritte(ablaeufe, 500)
assert ergebnis == ablaeufe_vergleich(500) and schritte <= 20 * 500, (
    f"ablaeufe(500) mit leerem bekannt ergibt {'den richtigen Wert' if ergebnis == ablaeufe_vergleich(500) else repr(ergebnis)} "
    f"in {schritte} Schritten; erwartet waren höchstens {20 * 500} Schritte (O(n))."
)
