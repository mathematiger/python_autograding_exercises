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


def selbstaufrufe(n):
    """Ruft reihenfolgen(n) auf und gibt die Liste der Werte zurück, mit denen sich die Funktion selbst aufruft."""
    global reihenfolgen
    original = reihenfolgen
    aufrufe = []

    def mitzaehlen(wert):
        """Merkt sich den Wert eines Selbstaufrufs und rechnet mit der Funktion der SuS weiter."""
        aufrufe.append(wert)
        return original(wert)

    # Die Selbstaufrufe suchen reihenfolgen im gemeinsamen Namensraum und landen so in mitzaehlen
    reihenfolgen = mitzaehlen
    try:
        original(n)
    finally:
        reihenfolgen = original
    return aufrufe


def kurz(zahl):
    """Kürzt eine lange Zahl für Fehlermeldungen auf ihre ersten Ziffern und nennt die Anzahl der Ziffern."""
    text = repr(zahl)
    if len(text) <= 30:
        return text
    return f"{text[:30]}… ({len(text)} Ziffern)"


# Drei Tests haben 6 Reihenfolgen
try:
    ergebnis = reihenfolgen(3)
    tipp = ""
except TypeError as fehler:
    if "NoneType" not in str(fehler):
        raise
    ergebnis = f"TypeError: {fehler}"
    tipp = "\nTipp: Ein Aufruf gibt None zurück; steht vor n * reihenfolgen(n - 1) ein return?"
assert ergebnis == 6, f"reihenfolgen(3) ergibt {ergebnis!r}, erwartet war 3 · 2 · 1 = 6.{tipp}"

# Vier Tests haben 24 Reihenfolgen (nicht fest hinschreiben!)
ergebnis = reihenfolgen(4)
assert ergebnis == 24, f"reihenfolgen(4) ergibt {ergebnis!r}, erwartet war 4 · 3 · 2 · 1 = 24."

# Ein Test hat eine Reihenfolge
ergebnis = reihenfolgen(1)
assert ergebnis == 1, f"reihenfolgen(1) ergibt {ergebnis!r}, erwartet war 1." + (
    "\nTipp: Ein Aufruf gibt None zurück; steht vor jedem Ergebnis ein return?" if ergebnis is None else ""
)

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

# reihenfolgen ruft sich selbst auf
aufrufe = selbstaufrufe(5)
assert len(aufrufe) >= 3, (
    f"reihenfolgen(5) ruft sich {len(aufrufe)}-mal selbst auf, erwartet war mindestens 3-mal "
    "(reihenfolgen(4), reihenfolgen(3), …).\n"
    "Tipp: Lösen Sie die Aufgabe rekursiv: Geben Sie n * reihenfolgen(n - 1) zurück."
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
    assert ergebnis == fakultaet(n), f"reihenfolgen({n}) ergibt {kurz(ergebnis)}, erwartet war {kurz(fakultaet(n))}."

# Obere Grenze: 300 Tests
ergebnis = reihenfolgen(300)
assert ergebnis == fakultaet(300), (
    "reihenfolgen(300) ergibt eine falsche Zahl. Erwartet war eine Zahl mit "
    f"{len(str(fakultaet(300)))} Ziffern, bekommen: {str(ergebnis)[:30]}…"
)
