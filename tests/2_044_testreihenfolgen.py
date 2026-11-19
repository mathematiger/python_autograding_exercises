# Automatisch erzeugt aus lehrkraft/muster/2_044_testreihenfolgen.py - nicht von Hand ändern.
# vorlage-hash: 6c222be47e60dd29
# text-hash: da9116ead9957c97
# thema: algorithmen
# inhalt: Rekursion: Fakultät

def fakultaet(n):
    """Vergleichslösung mit einer Schleife, nur für die Tests."""
    produkt = 1
    for faktor in range(2, n + 1):
        produkt = produkt * faktor
    return produkt


# Drei Tests haben 6 Reihenfolgen
ergebnis = reihenfolgen(3)
assert ergebnis == 6, f"reihenfolgen(3) ergibt {ergebnis!r}, erwartet war 3 · 2 · 1 = 6."

# Vier Tests haben 24 Reihenfolgen (nicht fest hinschreiben!)
ergebnis = reihenfolgen(4)
assert ergebnis == 24, f"reihenfolgen(4) ergibt {ergebnis!r}, erwartet war 4 · 3 · 2 · 1 = 24."

# Ein Test hat eine Reihenfolge
ergebnis = reihenfolgen(1)
assert ergebnis == 1, f"reihenfolgen(1) ergibt {ergebnis!r}, erwartet war 1."

# Kein Test: genau eine, die leere Reihenfolge
try:
    ergebnis = reihenfolgen(0)
except RecursionError:
    ergebnis = "RecursionError"
assert ergebnis == 1, (
    f"reihenfolgen(0) ergibt {ergebnis!r}, erwartet war 1 (0! = 1).\n"
    "Tipp: Nehmen Sie n == 0 als Abbruchbedingung; bei n == 1 als einziger Bedingung ruft sich "
    "die Funktion für 0 endlos weiter auf."
)

# Zehn Tests
ergebnis = reihenfolgen(10)
assert ergebnis == 3628800, f"reihenfolgen(10) ergibt {ergebnis!r}, erwartet war 3628800."

# Ohne Schleife
assert not verwendet("for") and not verwendet("while"), (
    "Lösen Sie die Aufgabe rekursiv: reihenfolgen ruft sich selbst mit n - 1 auf, ohne for oder while."
)

# Ohne math.factorial
assert not verwendet("factorial"), "Berechnen Sie n! selbst rekursiv, nicht mit math.factorial."

# Alle Werte von 0 bis 60 der Reihe nach
for n in range(61):
    ergebnis = reihenfolgen(n)
    assert ergebnis == fakultaet(n), f"reihenfolgen({n}) ergibt {ergebnis!r}, erwartet war {fakultaet(n)}."

# Viele zufällige Werte
zufall = Zufall(2044)
for n in sorted(zufall.sample(range(301), 40)):
    ergebnis = reihenfolgen(n)
    assert ergebnis == fakultaet(n), f"reihenfolgen({n}) ergibt eine falsche Zahl (erwartet {fakultaet(n)})."

# Obere Grenze: 300 Tests
ergebnis = reihenfolgen(300)
assert ergebnis == fakultaet(300), (
    "reihenfolgen(300) ergibt eine falsche Zahl. Erwartet war eine Zahl mit "
    f"{len(str(fakultaet(300)))} Ziffern, bekommen: {str(ergebnis)[:30]}…"
)
