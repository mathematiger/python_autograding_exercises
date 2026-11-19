# Automatisch erzeugt aus lehrkraft/muster/4_034_amortisation.py - nicht von Hand ändern.
# vorlage-hash: 0eea76491981954d
# text-hash: c0a2738c197d6dbb
# thema: kontrollfluss
# inhalt: Unendliche Generatoren

def erste_salden(investition, ersparnis, steigerung, anzahl):
    """Holt anzahl Paare aus salden; bricht ab, falls der Generator vorher endet."""
    folge = salden(investition, ersparnis, steigerung)
    paare = []
    for _ in range(anzahl):
        try:
            paare.append(next(folge))
        except StopIteration:
            paare.append("StopIteration")
            break
    return paare


def vergleich_salden(investition, ersparnis, steigerung, anzahl):
    """Vergleichslösung mit einer Formel statt einer laufenden Summe."""
    paare = []
    for jahr in range(1, anzahl + 1):
        gespart = jahr * ersparnis + steigerung * (jahr - 1) * jahr // 2
        paare.append((jahr, gespart - investition))
    return paare


def vergleich_jahr(investition, ersparnis, steigerung, laufzeit):
    """Vergleichslösung für amortisationsjahr mit einer einfachen Schleife."""
    for jahr, saldo in vergleich_salden(investition, ersparnis, steigerung, laufzeit):
        if saldo >= 0:
            return jahr
    return None


# salden liefert das erste Jahr
folge = salden(10000, 3000, 500)
assert hasattr(folge, "__next__"), (
    f"salden(10000, 3000, 500) ergibt {folge!r}, erwartet war ein Generator.\n"
    "Tipp: Schreiben Sie yield jahr, saldo statt return."
)

# Das Beispiel: die ersten drei Jahre
paare = erste_salden(10000, 3000, 500, 3)
assert paare == [(1, -7000), (2, -3500), (3, 500)], (
    f"Die ersten drei Werte von salden(10000, 3000, 500) sind {paare!r}, erwartet war "
    "[(1, -7000), (2, -3500), (3, 500)].\nTipp: Die Ersparnis wächst erst nach dem ersten Jahr um steigerung."
)

# salden ist unendlich: auch nach dem Amortisieren geht es weiter
paare = erste_salden(100, 60, 0, 6)
assert paare == vergleich_salden(100, 60, 0, 6), (
    f"Die ersten sechs Werte von salden(100, 60, 0) sind {paare!r}, erwartet war {vergleich_salden(100, 60, 0, 6)!r}.\n"
    "Tipp: Der Generator endet nie; schreiben Sie while True: um das yield."
)

# Ohne Ersparnis bleibt der Saldo bei der Investition
paare = erste_salden(500, 0, 0, 3)
assert paare == [(1, -500), (2, -500), (3, -500)], f"Die ersten drei Werte von salden(500, 0, 0) sind {paare!r}, erwartet war dreimal -500."

# Das Beispiel: amortisiert im dritten Jahr
ergebnis = amortisationsjahr(10000, 3000, 500, 15)
assert ergebnis == 3, f"amortisationsjahr(10000, 3000, 500, 15) ergibt {ergebnis!r}, erwartet war 3."

# Laufzeit zu kurz: None
ergebnis = amortisationsjahr(10000, 3000, 500, 2)
assert ergebnis is None, (
    f"amortisationsjahr(10000, 3000, 500, 2) ergibt {ergebnis!r}, erwartet war None (nach 2 Jahren ist der Saldo -3500).\n"
    "Tipp: Betrachten Sie nur die ersten laufzeit Jahre, etwa mit zip(range(laufzeit), ...)."
)

# Laufzeit genau bis zum Amortisationsjahr reicht
ergebnis = amortisationsjahr(10000, 3000, 500, 3)
assert ergebnis == 3, f"amortisationsjahr(10000, 3000, 500, 3) ergibt {ergebnis!r}, erwartet war 3 (das dritte Jahr gehört noch zur Laufzeit)."

# Saldo genau 0 zählt als amortisiert
ergebnis = amortisationsjahr(10000, 1000, 0, 15)
assert ergebnis == 10, f"amortisationsjahr(10000, 1000, 0, 15) ergibt {ergebnis!r}, erwartet war 10 (Saldo genau 0 zählt)."

# Ohne Investition ist die Anlage schon nach dem ersten Jahr amortisiert
ergebnis = amortisationsjahr(0, 0, 0, 5)
assert ergebnis == 1, f"amortisationsjahr(0, 0, 0, 5) ergibt {ergebnis!r}, erwartet war 1."

# Laufzeit 0: kein Jahr, also None
ergebnis = amortisationsjahr(0, 100, 0, 0)
assert ergebnis is None, f"amortisationsjahr(0, 100, 0, 0) ergibt {ergebnis!r}, erwartet war None (keine Jahre Laufzeit)."

# Nie amortisiert, obere Grenze der Laufzeit: None statt Endlosschleife
ergebnis = amortisationsjahr(10**9, 0, 0, 100000)
assert ergebnis is None, f"amortisationsjahr(10**9, 0, 0, 100000) ergibt {ergebnis!r}, erwartet war None."

# next mit Standardwert wird benutzt
assert verwendet("next"), "Suchen Sie das erste passende Jahr mit next(..., None) über salden."

# Früh amortisiert: der Rest der langen Laufzeit wird nicht berechnet
ergebnis, schritte = zaehle_schritte(amortisationsjahr, 100, 60, 0, 100000)
assert ergebnis == 2 and schritte <= 60, (
    f"amortisationsjahr(100, 60, 0, 100000) ergibt {ergebnis!r} nach {schritte} ausgeführten Zeilen; "
    "erwartet war 2 nach höchstens 60 Zeilen.\n"
    "Tipp: Hören Sie beim ersten Jahr mit Saldo ≥ 0 auf, statt alle 100 000 Jahre auszurechnen."
)

# Viele zufällige Anlagen
zufall = Zufall(4034)
for runde in range(300):
    investition = zufall.choice([0, zufall.randint(0, 10**4), zufall.randint(0, 10**9)])
    ersparnis = zufall.choice([0, zufall.randint(0, 3000), zufall.randint(0, 10**6)])
    steigerung = zufall.choice([0, zufall.randint(0, 100), zufall.randint(0, 10**4)])
    laufzeit = zufall.randint(0, 60)
    paare = erste_salden(investition, ersparnis, steigerung, 8)
    assert paare == vergleich_salden(investition, ersparnis, steigerung, 8), (
        f"Die ersten acht Werte von salden({investition}, {ersparnis}, {steigerung}) sind {paare!r}, "
        f"erwartet war {vergleich_salden(investition, ersparnis, steigerung, 8)!r}."
    )
    ergebnis = amortisationsjahr(investition, ersparnis, steigerung, laufzeit)
    erwartet = vergleich_jahr(investition, ersparnis, steigerung, laufzeit)
    assert ergebnis == erwartet, (
        f"amortisationsjahr({investition}, {ersparnis}, {steigerung}, {laufzeit}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Obere Grenze: große Investition, kleine Ersparnis, spät amortisiert
ergebnis = amortisationsjahr(10**9, 1, 1, 100000)
erwartet = vergleich_jahr(10**9, 1, 1, 100000)
assert ergebnis == erwartet, f"amortisationsjahr(10**9, 1, 1, 100000) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
