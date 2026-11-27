# Automatisch erzeugt aus lehrkraft/muster/2_047_ersatzteillager.py - nicht von Hand ändern.
# vorlage-hash: c04cf73c440bdca0
# text-hash: e9c5d7b03deae56a
# thema: algorithmen
# inhalt: Rekursion: Türme von Hanoi

def zuege_von(n, start="A", ziel="C", hilf="B"):
    """Ruft umlagern auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return umlagern(n, start, ziel, hilf)
    except RecursionError:
        return "RecursionError (fehlt die Abbruchbedingung für n == 0?)"
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def als_tupel(zuege):
    """Wandelt Züge, die als Liste [von, nach] geschrieben sind, in Tupel um; alles andere bleibt."""
    if not isinstance(zuege, list):
        return zuege
    return [tuple(zug) if isinstance(zug, list) else zug for zug in zuege]


def ergebnis_von(n, start="A", ziel="C", hilf="B"):
    """Ruft umlagern auf und vergleicht locker: Züge als Listen zählen wie Tupel."""
    return als_tupel(zuege_von(n, start, ziel, hilf))


def ohne_klammerart(ausgabe):
    """Macht eckige Klammern rund, damit Züge als Listen in der Ausgabe wie Tupel zählen."""
    return vergleichbar(ausgabe.replace("[", "(").replace("]", ")"))


def regelverstoss(n, zuege, start, ziel, hilf):
    """Spielt die Züge nach; gibt den ersten Verstoß als Text zurück, sonst None."""
    if not isinstance(zuege, list):
        return f"Das Ergebnis ist keine Liste, sondern {zuege!r}."
    faecher = {start: list(range(n, 0, -1)), ziel: [], hilf: []}
    for nummer, zug in enumerate(zuege, start=1):
        if not isinstance(zug, tuple) or len(zug) != 2 or zug[0] not in faecher or zug[1] not in faecher:
            return f"Zug {nummer} ist {zug!r}, erwartet war ein Tupel (von, nach) aus {start!r}, {ziel!r}, {hilf!r}."
        von, nach = zug
        if not faecher[von]:
            return f"Zug {nummer} {zug!r} nimmt einen Karton aus dem leeren Fach {von!r}."
        if faecher[nach] and faecher[nach][-1] < faecher[von][-1]:
            return f"Zug {nummer} {zug!r} legt einen größeren Karton auf einen kleineren."
        faecher[nach].append(faecher[von].pop())
    if faecher[ziel] != list(range(n, 0, -1)):
        return f"Nach allen Zügen liegen in {ziel!r} die Kartons {faecher[ziel]}, erwartet war {list(range(n, 0, -1))}."
    return None


def innere_aufrufe(n, start, ziel, hilf):
    """Gibt zurück, mit welchen Argumenten umlagern(n, …) sich mit n - 1 Kartons aufruft."""
    global umlagern
    original = umlagern
    innere = []

    def mitschreiben(n, start, ziel, hilf):
        """Merkt sich den inneren Aufruf und reicht ihn an die echte Funktion weiter."""
        innere.append((n, start, ziel, hilf))
        return original(n, start, ziel, hilf)

    umlagern = mitschreiben
    try:
        original(n, start, ziel, hilf)
    finally:
        umlagern = original
    return [argumente for argumente in innere if argumente[0] == n - 1]


# Ein einziger Karton: ein Zug von A nach C
ergebnis = ergebnis_von(1)
assert ergebnis == [("A", "C")], (
    f'umlagern(1, "A", "C", "B") ergibt {ergebnis!r}, erwartet war [("A", "C")].'
    + ("\nTipp: Geben Sie die Liste mit return zurück." if ergebnis is None else "")
)

# Zwei Kartons: drei Züge
ergebnis = ergebnis_von(2)
assert ergebnis == [("A", "B"), ("A", "C"), ("B", "C")], (
    f'umlagern(2, "A", "C", "B") ergibt {ergebnis!r}, erwartet war [("A", "B"), ("A", "C"), ("B", "C")].\n'
    "Tipp: Erst n - 1 Kartons von start nach hilf, dann einer von start nach ziel, dann n - 1 von hilf nach ziel."
)

# Drei Kartons: sieben Züge
ergebnis = ergebnis_von(3)
erwartet = [("A", "C"), ("A", "B"), ("C", "B"), ("A", "C"), ("B", "A"), ("B", "C"), ("A", "C")]
assert ergebnis == erwartet, f'umlagern(3, "A", "C", "B") ergibt {ergebnis!r}, erwartet war {erwartet!r}.'

# Null Kartons: keine Züge
ergebnis = ergebnis_von(0)
assert ergebnis == [], f'umlagern(0, "A", "C", "B") ergibt {ergebnis!r}, erwartet war [].'

# Andere Fächer: die Namen kommen aus den Parametern
ergebnis = ergebnis_von(2, "links", "rechts", "mitte")
erwartet = [("links", "mitte"), ("links", "rechts"), ("mitte", "rechts")]
assert ergebnis == erwartet, (
    f'umlagern(2, "links", "rechts", "mitte") ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    'Tipp: Schreiben Sie nicht "A", "B" oder "C" in die Funktion, sondern start, ziel und hilf.'
)

# Ziel und Hilfsfach vertauscht: dann landet der Stapel in B
ergebnis = ergebnis_von(3, "A", "B", "C")
verstoss = regelverstoss(3, ergebnis, "A", "B", "C")
assert verstoss is None, f'umlagern(3, "A", "B", "C") ergibt {ergebnis!r}.\n{verstoss}'

# Jeder Zug ist ein Tupel (von, nach)
zuege = zuege_von(2)
assert isinstance(zuege, list) and all(isinstance(zug, tuple) for zug in zuege), (
    f'umlagern(2, "A", "C", "B") ergibt {zuege!r}, erwartet war eine Liste von Tupeln: '
    '[("A", "B"), ("A", "C"), ("B", "C")].\n'
    "Tipp: Schreiben Sie einen Zug in runde Klammern, (start, ziel), nicht in eckige."
)

# Die Ausgabe des Programms
erwartet = "[('A', 'B'), ('A', 'C'), ('B', 'C')]\n7 Züge für 3 Kartons"
assert ohne_klammerart(AUSGABE) == ohne_klammerart(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Rekursiv: umlagern(3, …) ruft sich mit 2 Kartons zweimal auf
innere = innere_aufrufe(3, "A", "C", "B")
assert innere == [(2, "A", "B", "C"), (2, "B", "C", "A")], (
    f'umlagern(3, "A", "C", "B") ruft sich mit {innere!r} auf, erwartet war zuerst (2, "A", "B", "C") '
    'und dann (2, "B", "C", "A").\nTipp: Rufen Sie umlagern(n - 1, start, hilf, ziel) und umlagern(n - 1, hilf, ziel, start) auf.'
)

# Ohne Schleife
assert not verwendet("for") and not verwendet("while"), "Lösen Sie die Aufgabe rekursiv, ohne for und ohne while."

# Jede Kartonzahl von 0 bis 10 hält die Regeln ein und braucht 2**n - 1 Züge
for n in range(11):
    ergebnis = ergebnis_von(n, "Fach 1", "Fach 3", "Fach 2")
    verstoss = regelverstoss(n, ergebnis, "Fach 1", "Fach 3", "Fach 2")
    assert verstoss is None, f'umlagern({n}, "Fach 1", "Fach 3", "Fach 2"): {verstoss}'
    anzahl = len(ergebnis)
    assert anzahl == 2**n - 1, f"umlagern({n}, …) braucht {anzahl} Züge, erwartet waren 2**{n} - 1 = {2**n - 1}."

# Viele zufällige Fachnamen und Kartonzahlen
zufall = Zufall(2047)
for _ in range(30):
    namen = zufall.sample(["A", "B", "C", "oben", "unten", "Regal 7", "x"], 3)
    n = zufall.randint(0, 8)
    ergebnis = ergebnis_von(n, *namen)
    verstoss = regelverstoss(n, ergebnis, *namen)
    assert verstoss is None, f"umlagern({n}, {namen[0]!r}, {namen[1]!r}, {namen[2]!r}): {verstoss}"
    assert len(ergebnis) == 2**n - 1, f"umlagern({n}, …) braucht {len(ergebnis)} Züge, erwartet waren {2**n - 1}."

# Obere Grenze: 15 Kartons
ergebnis = ergebnis_von(15)
verstoss = regelverstoss(15, ergebnis, "A", "C", "B")
assert verstoss is None and len(ergebnis) == 2**15 - 1, (
    f'umlagern(15, "A", "C", "B"): {verstoss or f"{len(ergebnis)} Züge, erwartet waren 32767."}'
)
