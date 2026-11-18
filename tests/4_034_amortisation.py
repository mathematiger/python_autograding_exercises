# Automatisch erzeugt aus lehrkraft/muster/4_034_amortisation.py - nicht von Hand ändern.
# vorlage-hash: 5e68ed5f7c6e6db2
# text-hash: 5062ee485fdbf3dc
# thema: kontrollfluss
# inhalt: Unendliche Generatoren

import inspect


def staende_von_hand(investition, ersparnis, zuwachs, anzahl):
    """Vergleichslösung: die ersten anzahl Stände mit der Summenformel statt Schritt für Schritt."""
    ergebnis = []
    for jahr in range(1, anzahl + 1):
        # Ersparnisse der Jahre 1 bis jahr: jahr · ersparnis + zuwachs · (0 + 1 + … + (jahr - 1))
        ergebnis.append(jahr * ersparnis + zuwachs * jahr * (jahr - 1) // 2 - investition)
    return ergebnis


def amortisation_von_hand(investition, ersparnis, zuwachs, laufzeit):
    """Vergleichslösung: geht die Jahre einzeln mit der Summenformel durch."""
    for jahr in range(1, laufzeit + 1):
        if jahr * ersparnis + zuwachs * jahr * (jahr - 1) // 2 >= investition:
            return jahr
    return None


def erste_staende(investition, ersparnis, zuwachs, anzahl):
    """Holt die ersten anzahl Werte aus staende(...); liefert (Werte, Ausnahme oder None)."""
    werte = []
    try:
        folge = staende(investition, ersparnis, zuwachs)
        for _ in range(anzahl):
            werte.append(next(folge))
    except Exception as ausnahme:
        return werte, ausnahme
    return werte, None


# staende: der erste Stand ist Ersparnis minus Investition
werte, fehler = erste_staende(10000, 3000, 500, 1)
assert fehler is None and werte == [-7000], (
    f"Der erste Wert von staende(10000, 3000, 500) ist {werte[0] if werte else fehler!r}, erwartet war -7000.\n"
    "Tipp: Ohne yield liefert der Aufruf keinen Generator, und next(...) meldet „object is not an iterator“."
)

# staende: die ersten vier Stände aus dem Beispiel
werte, fehler = erste_staende(10000, 3000, 500, 4)
assert fehler is None and werte == [-7000, -3500, 500, 5000], (
    f"Die ersten vier Werte von staende(10000, 3000, 500) sind {werte}"
    + (f", dann {type(fehler).__name__}: {fehler}" if fehler else "")
    + ", erwartet waren [-7000, -3500, 500, 5000].\n"
    "Tipp: Jedes Jahr kommt die Ersparnis dazu, und danach wächst die Ersparnis um zuwachs."
)

# staende: andere Werte, ohne Zuwachs (nicht fest hinschreiben!)
werte, fehler = erste_staende(500, 200, 0, 3)
assert fehler is None and werte == [-300, -100, 100], (
    f"Die ersten drei Werte von staende(500, 200, 0) sind {werte}, erwartet waren [-300, -100, 100]."
)

# staende: der Generator geht über den Nullpunkt hinaus weiter
werte, fehler = erste_staende(0, 10, 5, 4)
assert fehler is None and werte == [10, 25, 45, 70], (
    f"Die ersten vier Werte von staende(0, 10, 5) sind {werte}"
    + (f", dann {type(fehler).__name__}: {fehler}" if fehler else "")
    + ", erwartet waren [10, 25, 45, 70].\nTipp: Der Generator ist unendlich; er hört nicht auf, wenn der Stand 0 erreicht."
)

# staende ist eine Generatorfunktion
assert inspect.isgeneratorfunction(staende), (
    "staende ist keine Generatorfunktion. Benutzen Sie yield, statt eine Liste zurückzugeben."
)

# staende ist unendlich: 100 000 Stände ohne Ende
werte, fehler = erste_staende(10**9, 0, 1, 100_000)
erwartet_letzter = staende_von_hand(10**9, 0, 1, 100_000)[-1]
assert fehler is None and len(werte) == 100_000 and werte[-1] == erwartet_letzter, (
    f"Aus staende(10**9, 0, 1) kamen {len(werte)} Werte"
    + (f", dann {type(fehler).__name__}: {fehler}" if fehler else "")
    + f"; erwartet waren 100 000 Werte, der letzte {erwartet_letzter}.\n"
    "Tipp: Eine Schleife while True: … yield … endet nie; der Generator hört nie von selbst auf."
)

# amortisation: das Beispiel, nach drei Jahren
ergebnis = amortisation(10000, 3000, 500, 10)
assert ergebnis == 3, f"amortisation(10000, 3000, 500, 10) ergibt {ergebnis!r}, erwartet war 3."

# amortisation: andere Werte (nicht fest hinschreiben!)
ergebnis = amortisation(5000, 1000, 0, 20)
assert ergebnis == 5, f"amortisation(5000, 1000, 0, 20) ergibt {ergebnis!r}, erwartet war 5."

# amortisation: genau 0 zählt schon als amortisiert
ergebnis = amortisation(3000, 1000, 0, 10)
assert ergebnis == 3, (
    f"amortisation(3000, 1000, 0, 10) ergibt {ergebnis!r}, erwartet war 3 (nach drei Jahren ist der Stand "
    "genau 0).\nTipp: Gefragt ist ein Stand von mindestens 0, also >= 0."
)

# amortisation: nach der Laufzeit ist es zu spät
ergebnis = amortisation(10000, 3000, 500, 2)
assert ergebnis is None, (
    f"amortisation(10000, 3000, 500, 2) ergibt {ergebnis!r}, erwartet war None (amortisiert erst in Jahr 3)."
)

# amortisation: genau im letzten Jahr der Laufzeit zählt noch
ergebnis = amortisation(10000, 3000, 500, 3)
assert ergebnis == 3, f"amortisation(10000, 3000, 500, 3) ergibt {ergebnis!r}, erwartet war 3 (das letzte Jahr zählt mit)."

# amortisation: ohne Investition schon im ersten Jahr
ergebnis = amortisation(0, 0, 0, 5)
assert ergebnis == 1, f"amortisation(0, 0, 0, 5) ergibt {ergebnis!r}, erwartet war 1."

# amortisation: ohne Ersparnis nie
ergebnis = amortisation(1, 0, 0, 100)
assert ergebnis is None, f"amortisation(1, 0, 0, 100) ergibt {ergebnis!r}, erwartet war None."

# amortisation: Laufzeit 1
ergebnisse = (amortisation(100, 100, 0, 1), amortisation(100, 99, 50, 1))
assert ergebnisse == (1, None), (
    f"amortisation(100, 100, 0, 1) und amortisation(100, 99, 50, 1) ergeben {ergebnisse}, erwartet war (1, None)."
)

# amortisation hört im ersten passenden Jahr auf
ergebnis, schritte = zaehle_schritte(amortisation, 100, 50, 0, 100_000)
assert ergebnis == 2 and schritte <= 200, (
    f"amortisation(100, 50, 0, 100000) ergibt {ergebnis!r} nach {schritte} ausgeführten Zeilen; erwartet war 2 "
    "nach wenigen Zeilen (höchstens 200).\n"
    "Tipp: Holen Sie die Stände einzeln (for oder next) und hören Sie beim ersten passenden Jahr auf, statt "
    "erst eine Liste aller Jahre der Laufzeit anzulegen."
)

# Viele zufällige Investitionen
zufall = Zufall(4034)
for runde in range(400):
    investition = zufall.choice([0, zufall.randint(0, 10_000), zufall.randint(0, 10**9)])
    ersparnis = zufall.choice([0, zufall.randint(0, 3000), zufall.randint(0, 10**6)])
    zuwachs = zufall.choice([0, zufall.randint(0, 500), zufall.randint(0, 10**5)])
    laufzeit = zufall.randint(1, 60)
    werte, fehler = erste_staende(investition, ersparnis, zuwachs, 8)
    erwartet = staende_von_hand(investition, ersparnis, zuwachs, 8)
    assert fehler is None and werte == erwartet, (
        f"Die ersten acht Werte von staende({investition}, {ersparnis}, {zuwachs}) sind {werte}, erwartet war {erwartet}."
    )
    ergebnis = amortisation(investition, ersparnis, zuwachs, laufzeit)
    erwartet = amortisation_von_hand(investition, ersparnis, zuwachs, laufzeit)
    assert ergebnis == erwartet, (
        f"amortisation({investition}, {ersparnis}, {zuwachs}, {laufzeit}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Obere Grenze: größte Investition, kleinste Ersparnis, längste Laufzeit
for argumente in [(10**9, 0, 1, 10**5), (10**9, 0, 0, 10**5), (10**9, 10**6, 10**5, 10**5)]:
    ergebnis = amortisation(*argumente)
    erwartet = amortisation_von_hand(*argumente)
    assert ergebnis == erwartet, f"amortisation{argumente} ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("-7000 -3500 500 5000\n3 None"), (
    f"Erwartete Ausgabe:\n-7000 -3500 500 5000\n3 None\nIhr Programm:\n{AUSGABE}"
)
