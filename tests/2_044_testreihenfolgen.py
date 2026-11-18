# Automatisch erzeugt aus lehrkraft/muster/2_044_testreihenfolgen.py - nicht von Hand ändern.
# vorlage-hash: 15759e915b387f89
# text-hash: 35d25f72cf56cfc8
# thema: algorithmen
# inhalt: Rekursion: Fakultät

def fakultaet_mit_schleife(n):
    """Vergleichslösung mit einer Schleife statt Rekursion."""
    ergebnis = 1
    for faktor in range(2, n + 1):
        ergebnis = ergebnis * faktor
    return ergebnis


def rekursive_aufrufe(n):
    """Ruft reihenfolgen(n) auf und liefert die Argumente der Aufrufe, die die Funktion dabei von sich selbst macht."""
    global reihenfolgen
    original = reihenfolgen
    argumente = []

    def mitzaehlen(m):
        """Merkt sich das Argument eines inneren Aufrufs und rechnet wie das Original."""
        argumente.append(m)
        return original(m)

    reihenfolgen = mitzaehlen
    try:
        original(n)
    finally:
        reihenfolgen = original
    return argumente


# Drei Tests haben sechs Reihenfolgen
ergebnis = reihenfolgen(3)
assert ergebnis == 6, f"reihenfolgen(3) ergibt {ergebnis!r}, erwartet war 6 (3 · 2 · 1)."

# Fünf Tests haben 120 Reihenfolgen (nicht fest hinschreiben!)
ergebnis = reihenfolgen(5)
assert ergebnis == 120, f"reihenfolgen(5) ergibt {ergebnis!r}, erwartet war 120 (5 · 4 · 3 · 2 · 1)."

# Weitere Werte
for n, erwartet in [(2, 2), (4, 24), (7, 5040), (10, 3628800)]:
    ergebnis = reihenfolgen(n)
    assert ergebnis == erwartet, f"reihenfolgen({n}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ein Test hat genau eine Reihenfolge
ergebnis = reihenfolgen(1)
assert ergebnis == 1, f"reihenfolgen(1) ergibt {ergebnis!r}, erwartet war 1."

# Kein Test: genau eine, die leere Reihenfolge
try:
    ergebnis = reihenfolgen(0)
except RecursionError:
    ergebnis = "RecursionError"
assert ergebnis == 1, (
    f"reihenfolgen(0) ergibt {ergebnis!r}, erwartet war 1 (0! = 1).\n"
    "Tipp: Die Abbruchbedingung muss schon bei n == 0 greifen und 1 zurückgeben."
)

# reihenfolgen ruft sich selbst mit n - 1 auf
argumente = rekursive_aufrufe(5)
assert len(argumente) > 0 and argumente[0] == 4, (
    f"Beim Aufruf reihenfolgen(5) ruft sich die Funktion "
    + (f"mit diesen Argumenten auf: {argumente}." if argumente else "kein einziges Mal selbst auf.")
    + " Erwartet war als Erstes reihenfolgen(4).\n"
    "Tipp: Lösen Sie die Aufgabe rekursiv: return n * reihenfolgen(n - 1), keine Schleife und kein math.factorial."
)

# Keine Schleife
assert not verwendet("for") and not verwendet("while"), (
    "Ihre Lösung benutzt eine Schleife. Lösen Sie die Aufgabe rekursiv, ohne for und while."
)

# Alle n von 0 bis 60, verglichen mit einer Schleife
for n in range(61):
    erwartet = fakultaet_mit_schleife(n)
    ergebnis = reihenfolgen(n)
    assert ergebnis == erwartet, f"reihenfolgen({n}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Viele zufällige n bis zur oberen Grenze
zufall = Zufall(2044)
for n in sorted(zufall.sample(range(61, 501), 20)):
    erwartet = fakultaet_mit_schleife(n)
    ergebnis = reihenfolgen(n)
    assert ergebnis == erwartet, (
        f"reihenfolgen({n}) ist falsch: erwartet war eine Zahl mit {len(str(erwartet))} Ziffern, die mit "
        f"{str(erwartet)[:10]}… beginnt; bekommen {str(ergebnis)[:20]!r}…"
    )

# Obere Grenze: 500 Tests
erwartet = fakultaet_mit_schleife(500)
ergebnis = reihenfolgen(500)
assert ergebnis == erwartet, (
    f"reihenfolgen(500) ist falsch: erwartet war eine Zahl mit 1135 Ziffern, bekommen {str(ergebnis)[:20]!r}…\n"
    "Tipp: Rechnen Sie mit ganzen Zahlen (*), nicht mit / oder float."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("6 120"), f'Erwartete Ausgabe: "6 120" – Ihr Programm: "{AUSGABE}"'
