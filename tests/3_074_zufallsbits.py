# Automatisch erzeugt aus lehrkraft/muster/3_074_zufallsbits.py - nicht von Hand ändern.
# vorlage-hash: 4d0a6fc4d576ca49
# text-hash: acdbe38a5c41a9d6
# thema: algorithmen
# inhalt: Galton-Brett simulieren

import itertools
import math


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def zaehlende_quelle(bits):
    """Gibt eine Bitquelle zurück, die die Bits wiederholt liefert, und eine Liste, deren Länge die Aufrufe zählt."""
    aufrufe = []
    naechste = itertools.cycle(bits)

    def bit():
        """Liefert das nächste Bit und merkt sich den Aufruf."""
        aufrufe.append(1)
        return next(naechste)

    return bit, aufrufe


def vergleich_galton(kugeln, reihen, bits):
    """Vergleichslösung: zerlegt die Bitfolge in Stücke der Länge reihen und zählt die Einsen."""
    faecher = [0] * (reihen + 1)
    for kugel in range(kugeln):
        faecher[sum(bits[kugel * reihen:(kugel + 1) * reihen])] += 1
    return faecher


def vergleich_erwartet(kugeln, reihen):
    """Vergleichslösung mit math.comb."""
    return [kugeln * math.comb(reihen, k) / 2**reihen for k in range(reihen + 1)]


def ungefaehr_liste(ergebnis, erwartet):
    """Prüft, ob ergebnis eine Liste von Zahlen ist, die bis auf Rundungsfehler gleich erwartet ist."""
    return (
        isinstance(ergebnis, list)
        and len(ergebnis) == len(erwartet)
        and all(isinstance(a, (int, float)) and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9) for a, b in zip(ergebnis, erwartet))
    )


def ungefaehr(a, b):
    """Prüft, ob a eine Zahl ist und bis auf Rundungsfehler gleich b."""
    return isinstance(a, (int, float)) and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


# galton: das Beispiel mit festen Bits
ergebnis = wert_von(galton, 2, 3, bits_aus([0, 1, 0, 1, 1, 1]))
assert ergebnis == [0, 1, 0, 1], (
    f"galton(2, 3, bits_aus([0, 1, 0, 1, 1, 1])) ergibt {ergebnis!r}, erwartet war [0, 1, 0, 1]: Die erste Kugel "
    "geht einmal nach rechts (0, 1, 0) und landet in Fach 1, die zweite dreimal (1, 1, 1) und landet in Fach 3.\n"
    "Tipp: Zählen Sie je Kugel die Einsen aus reihen Aufrufen von zufallsbit()."
)

# galton: andere Bits (nicht fest hinschreiben!)
bits = [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
ergebnis = wert_von(galton, 3, 4, bits_aus(bits))
erwartet = vergleich_galton(3, 4, bits)
assert ergebnis == erwartet, f"galton(3, 4, bits_aus({bits})) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# galton: die Liste hat reihen + 1 Fächer
ergebnis = wert_von(galton, 1, 5, bits_aus([0] * 5))
assert ergebnis == [1, 0, 0, 0, 0, 0], (
    f"galton(1, 5, bits_aus([0, 0, 0, 0, 0])) ergibt {ergebnis!r}, erwartet war [1, 0, 0, 0, 0, 0].\n"
    "Tipp: Bei reihen Reihen gibt es reihen + 1 Fächer, von 0 (immer links) bis reihen (immer rechts)."
)

# galton: immer rechts landet im letzten Fach
ergebnis = wert_von(galton, 4, 3, bits_aus([1] * 12))
assert ergebnis == [0, 0, 0, 4], f"galton(4, 3, bits_aus([1] * 12)) ergibt {ergebnis!r}, erwartet war [0, 0, 0, 4]."

# galton: keine Kugeln
ergebnis = wert_von(galton, 0, 4, bits_aus([]))
assert ergebnis == [0, 0, 0, 0, 0], f"galton(0, 4, bits_aus([])) ergibt {ergebnis!r}, erwartet war [0, 0, 0, 0, 0]."

# galton: genau ein Aufruf von zufallsbit je Kugel und Reihe
quelle, aufrufe = zaehlende_quelle([1, 0, 0])
ergebnis = wert_von(galton, 7, 6, quelle)
assert len(aufrufe) == 42 and ergebnis == vergleich_galton(7, 6, [1, 0, 0] * 14), (
    f"galton(7, 6, …) ruft zufallsbit {len(aufrufe)}-mal auf und ergibt {ergebnis!r}; erwartet waren 42 Aufrufe "
    f"(7 Kugeln · 6 Reihen) und {vergleich_galton(7, 6, [1, 0, 0] * 14)!r}."
)

# galton: das Beispiel mit random
random.seed(3074)
ergebnis = wert_von(galton, 1024, 10, lambda: random.randint(0, 1))
assert ergebnis == [0, 11, 34, 129, 202, 268, 202, 130, 39, 9, 0], (
    f"Nach random.seed(3074) ergibt galton(1024, 10, lambda: random.randint(0, 1))\n{ergebnis!r},\nerwartet war\n"
    "[0, 11, 34, 129, 202, 268, 202, 130, 39, 9, 0].\nTipp: Rufen Sie zufallsbit Kugel für Kugel auf und ziehen Sie "
    "keine eigenen Zufallszahlen."
)

zufall = Zufall(3074)

# galton: viele zufällige Bitfolgen
for _ in range(100):
    kugeln, reihen = zufall.randint(0, 30), zufall.randint(1, 8)
    bits = [zufall.randint(0, 1) for _ in range(kugeln * reihen)]
    ergebnis = wert_von(galton, kugeln, reihen, bits_aus(bits))
    erwartet = vergleich_galton(kugeln, reihen, bits)
    assert ergebnis == erwartet, f"galton({kugeln}, {reihen}, bits_aus({bits})) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# erwartete_anzahlen: das Beispiel aus der Aufgabe
ergebnis = wert_von(erwartete_anzahlen, 16, 4)
assert ungefaehr_liste(ergebnis, [1, 4, 6, 4, 1]), (
    f"erwartete_anzahlen(16, 4) ergibt {ergebnis!r}, erwartet war [1.0, 4.0, 6.0, 4.0, 1.0].\n"
    "Tipp: Bauen Sie die Zeile 4 des Pascalschen Dreiecks [1, 4, 6, 4, 1] und rechnen Sie jeden Eintrag "
    "· kugeln / 2 hoch reihen."
)

# erwartete_anzahlen: andere Werte (nicht fest hinschreiben!)
ergebnis = wert_von(erwartete_anzahlen, 100, 3)
assert ungefaehr_liste(ergebnis, [12.5, 37.5, 37.5, 12.5]), (
    f"erwartete_anzahlen(100, 3) ergibt {ergebnis!r}, erwartet war [12.5, 37.5, 37.5, 12.5]."
)

# erwartete_anzahlen: eine Reihe teilt die Kugeln halb und halb
ergebnis = wert_von(erwartete_anzahlen, 10, 1)
assert ungefaehr_liste(ergebnis, [5, 5]), f"erwartete_anzahlen(10, 1) ergibt {ergebnis!r}, erwartet war [5.0, 5.0]."

# erwartete_anzahlen: keine Kugeln
ergebnis = wert_von(erwartete_anzahlen, 0, 2)
assert ungefaehr_liste(ergebnis, [0, 0, 0]), f"erwartete_anzahlen(0, 2) ergibt {ergebnis!r}, erwartet war [0.0, 0.0, 0.0]."

# erwartete_anzahlen: alle Reihen von 1 bis 30
for reihen in range(1, 31):
    ergebnis = wert_von(erwartete_anzahlen, 10_000, reihen)
    erwartet = vergleich_erwartet(10_000, reihen)
    assert ungefaehr_liste(ergebnis, erwartet), (
        f"erwartete_anzahlen(10000, {reihen}) ergibt {str(ergebnis)[:200]}, erwartet war {str(erwartet)[:200]}."
    )

# chi_quadrat: das Beispiel aus der Aufgabe
ergebnis = wert_von(chi_quadrat, [2, 3, 6, 4, 1], [1, 4, 6, 4, 1])
assert ungefaehr(ergebnis, 1.25), (
    f"chi_quadrat([2, 3, 6, 4, 1], [1, 4, 6, 4, 1]) ergibt {ergebnis!r}, erwartet war 1.25 "
    "(also (2-1)²/1 + (3-4)²/4 + 0 + 0 + 0).\nTipp: Quadrieren Sie die Differenz, bevor Sie durch erwartet teilen."
)

# chi_quadrat: andere Werte (nicht fest hinschreiben!)
ergebnis = wert_von(chi_quadrat, [10, 30, 10], [12.5, 25, 12.5])
assert ungefaehr(ergebnis, 2.0), f"chi_quadrat([10, 30, 10], [12.5, 25, 12.5]) ergibt {ergebnis!r}, erwartet war 2.0."

# chi_quadrat: gleiche Listen ergeben 0
ergebnis = wert_von(chi_quadrat, [1, 4, 6, 4, 1], [1.0, 4.0, 6.0, 4.0, 1.0])
assert ungefaehr(ergebnis, 0), f"chi_quadrat([1, 4, 6, 4, 1], [1.0, 4.0, 6.0, 4.0, 1.0]) ergibt {ergebnis!r}, erwartet war 0."

# chi_quadrat: ein einziges Fach
ergebnis = wert_von(chi_quadrat, [3], [5])
assert ungefaehr(ergebnis, 0.8), f"chi_quadrat([3], [5]) ergibt {ergebnis!r}, erwartet war 0.8."

# chi_quadrat: viele zufällige Listen
for _ in range(100):
    laenge = zufall.randint(1, 31)
    beobachtet = [zufall.randint(0, 100) for _ in range(laenge)]
    erwartet = [zufall.uniform(0.5, 100) for _ in range(laenge)]
    ergebnis = wert_von(chi_quadrat, beobachtet, erwartet)
    summe = math.fsum((b - e) ** 2 / e for b, e in zip(beobachtet, erwartet))
    assert ungefaehr(ergebnis, summe), f"chi_quadrat({beobachtet}, {erwartet}) ergibt {ergebnis!r}, erwartet war {summe!r}."

# verdaechtig: ein guter Generator besteht
random.seed(3074)
ergebnis = wert_von(verdaechtig, lambda: random.randint(0, 1), 1024, 10, 23.2)
assert ergebnis is False, (
    f"Nach random.seed(3074) ergibt verdaechtig(lambda: random.randint(0, 1), 1024, 10, 23.2) {ergebnis!r}, "
    "erwartet war False (χ² ist etwa 8.8)."
)

# verdaechtig: ein schiefer Generator fällt auf
random.seed(3074)
ergebnis = wert_von(verdaechtig, lambda: 1 if random.random() < 0.6 else 0, 1024, 10, 23.2)
assert ergebnis is True, (
    f"Ein Generator, der in 60 von 100 Fällen 1 liefert, ergibt verdaechtig(…, 1024, 10, 23.2) = {ergebnis!r}; "
    "erwartet war True (χ² ist fast 500)."
)

# verdaechtig: genau die erwarteten Anzahlen sind nicht verdächtig
ergebnis = wert_von(verdaechtig, bits_aus([0, 1, 1, 1, 0, 0, 1, 0]), 4, 2, 1.0)
assert ergebnis is False, (
    "Vier Kugeln mit zwei Reihen landen in den Fächern [1, 2, 1], genau wie erwartet, also χ² = 0. "
    f"verdaechtig(…, 4, 2, 1.0) ergibt {ergebnis!r}, erwartet war False."
)

# verdaechtig: genau auf der Grenze ist nicht verdächtig
ergebnis = wert_von(verdaechtig, bits_aus([1, 1, 1, 1, 0, 0, 1, 0]), 4, 2, 1.5)
assert ergebnis is False, (
    "Vier Kugeln mit zwei Reihen landen in den Fächern [1, 1, 2]; erwartet sind [1, 2, 1], also "
    f"χ² = 0 + 0.5 + 1 = 1.5. verdaechtig(…, 4, 2, 1.5) ergibt {ergebnis!r}, erwartet war False: Verdächtig ist "
    "nur, was größer als grenze ist."
)

# verdaechtig: knapp über der Grenze ist verdächtig
ergebnis = wert_von(verdaechtig, bits_aus([1, 1, 1, 1, 0, 0, 1, 0]), 4, 2, 1.4)
assert ergebnis is True, f"Bei χ² = 1.5 und grenze 1.4 ergibt verdaechtig {ergebnis!r}, erwartet war True."

# Obere Grenze: 10000 Kugeln durch 30 Reihen
quelle, aufrufe = zaehlende_quelle([zufall.randint(0, 1) for _ in range(997)])
ergebnis = wert_von(galton, 10_000, 30, quelle)
assert isinstance(ergebnis, list) and len(ergebnis) == 31 and sum(ergebnis) == 10_000 and len(aufrufe) == 300_000, (
    f"galton(10000, 30, …) ergibt {str(ergebnis)[:120]} mit {len(aufrufe)} Aufrufen von zufallsbit; erwartet waren "
    "31 Fächer mit zusammen 10000 Kugeln und 300000 Aufrufe."
)
