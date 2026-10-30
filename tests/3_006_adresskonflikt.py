# Automatisch erzeugt aus lehrkraft/muster/3_006_adresskonflikt.py - nicht von Hand ändern.
# vorlage-hash: ed9f3b2105b4d990
# text-hash: d7236702496cba15
# thema: algorithmen
# inhalt: Laufzeit und O-Notation

# Drei verschiedene Adressen brauchen paarweise 3 Vergleiche
ergebnis = vergleiche_paarweise(["10.0.0.1", "10.0.0.2", "10.0.0.3"])
assert ergebnis == 3, (
    f'vergleiche_paarweise(["10.0.0.1", "10.0.0.2", "10.0.0.3"]) ergibt {ergebnis!r}, erwartet war 3 '
    "(1. mit 2., 1. mit 3., 2. mit 3.).\n"
    "Tipp: Erhöhen Sie den Zähler in der inneren Schleife, direkt vor dem Vergleich."
)

# Ohne Konflikt werden alle Paare verglichen (nicht fest 3 hinschreiben!)
for anzahl, erwartet in [(2, 1), (4, 6), (5, 10), (1000, 499500)]:
    adressen = []
    for nummer in range(anzahl):
        adressen.append("192.168." + str(nummer // 256) + "." + str(nummer % 256))
    ergebnis = vergleiche_paarweise(adressen)
    assert ergebnis == erwartet, (
        f"vergleiche_paarweise mit {anzahl} verschiedenen Adressen ergibt {ergebnis!r}, erwartet war {erwartet}."
    )

# Beim ersten Konflikt ist Schluss
for adressen, erwartet in [
    (["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.1"], 3),
    (["10.0.0.7", "10.0.0.7", "10.0.0.8", "10.0.0.9"], 1),
    (["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.2"], 5),
    (["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.4"], 10),
]:
    ergebnis = vergleiche_paarweise(adressen)
    assert ergebnis == erwartet, (
        f"vergleiche_paarweise({adressen}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Wie konflikt_paarweise hört die Funktion beim ersten gleichen Paar auf und gibt dann "
        "die Zahl der Vergleiche bis dahin zurück, diesen einen mitgezählt."
    )

# Leere Liste und eine einzige Adresse: kein Vergleich
for adressen in [[], ["10.0.0.1"]]:
    ergebnis = vergleiche_paarweise(adressen)
    assert ergebnis == 0, f"vergleiche_paarweise({adressen}) ergibt {ergebnis!r}, erwartet war 0."

# Drei verschiedene sortierte Adressen brauchen 2 Nachbarvergleiche
ergebnis = vergleiche_nachbarn(["10.0.0.1", "10.0.0.2", "10.0.0.3"])
assert ergebnis == 2, (
    f'vergleiche_nachbarn(["10.0.0.1", "10.0.0.2", "10.0.0.3"]) ergibt {ergebnis!r}, erwartet war 2 '
    "(1. mit 2., 2. mit 3.).\n"
    "Tipp: Bei n Adressen gibt es n - 1 Nachbarpaare."
)

# Ohne Konflikt werden alle Nachbarn verglichen
for anzahl, erwartet in [(2, 1), (5, 4), (1000, 999)]:
    adressen = []
    for nummer in range(anzahl):
        adressen.append("192.168." + str(nummer // 256) + "." + str(nummer % 256))
    adressen.sort()
    ergebnis = vergleiche_nachbarn(adressen)
    assert ergebnis == erwartet, (
        f"vergleiche_nachbarn mit {anzahl} verschiedenen sortierten Adressen ergibt {ergebnis!r}, erwartet war {erwartet}."
    )

# Auch bei den Nachbarn ist beim ersten Konflikt Schluss
for sortiert, erwartet in [
    (["10.0.0.1", "10.0.0.1", "10.0.0.2"], 1),
    (["10.0.0.1", "10.0.0.2", "10.0.0.2", "10.0.0.3"], 2),
    (["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.4"], 4),
]:
    ergebnis = vergleiche_nachbarn(sortiert)
    assert ergebnis == erwartet, (
        f"vergleiche_nachbarn({sortiert}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Sobald zwei Nachbarn gleich sind, geben Sie die Zahl der Vergleiche bis dahin zurück."
    )

# Leere Liste und eine einzige Adresse: kein Nachbarvergleich
for sortiert in [[], ["10.0.0.1"]]:
    ergebnis = vergleiche_nachbarn(sortiert)
    assert ergebnis == 0, (
        f"vergleiche_nachbarn({sortiert}) ergibt {ergebnis!r}, erwartet war 0.\n"
        "Tipp: Ohne zweite Adresse gibt es keine Nachbarin; range(len(sortiert) - 1) ist dann leer."
    )


def erwartete_vergleiche(gleich):
    """Zählt die Vergleiche bis zum ersten True in der Liste der Vergleichsergebnisse."""
    if True in gleich:
        return gleich.index(True) + 1
    return len(gleich)


# Viele zufällige Adresslisten, oft mit Konflikt: paarweise (nicht fest hinschreiben!)
zufall = Zufall(3006)
for runde in range(300):
    adressen = ["10.0.0." + str(zufall.randint(1, 12)) for _ in range(runde // 15)]
    paare = [(i, j) for i in range(len(adressen)) for j in range(i + 1, len(adressen))]
    erwartet = erwartete_vergleiche([adressen[i] == adressen[j] for i, j in paare])
    ergebnis = vergleiche_paarweise(adressen)
    assert ergebnis == erwartet, f"vergleiche_paarweise({adressen}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Viele zufällige sortierte Adresslisten, oft mit Konflikt: Nachbarn
for runde in range(300):
    sortiert = sorted("10.0.0." + str(zufall.randint(1, 12)) for _ in range(runde // 15))
    erwartet = erwartete_vergleiche([links == rechts for links, rechts in zip(sortiert, sortiert[1:])])
    ergebnis = vergleiche_nachbarn(sortiert)
    assert ergebnis == erwartet, f"vergleiche_nachbarn({sortiert}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# 1000 Adressen mit einem Konflikt weit hinten
adressen = []
for nummer in range(1000):
    adressen.append("192.168." + str(nummer // 256) + "." + str(nummer % 256))
adressen[999] = adressen[600]
paare = [(i, j) for i in range(1000) for j in range(i + 1, 1000)]
erwartet_paarweise = erwartete_vergleiche([adressen[i] == adressen[j] for i, j in paare])
sortiert = sorted(adressen)
erwartet_nachbarn = erwartete_vergleiche([links == rechts for links, rechts in zip(sortiert, sortiert[1:])])
ergebnis = (vergleiche_paarweise(adressen), vergleiche_nachbarn(sortiert))
assert ergebnis == (erwartet_paarweise, erwartet_nachbarn), (
    f"Bei 1000 Adressen, von denen die letzte gleich der Adresse an Index 600 ist, ergeben vergleiche_paarweise "
    f"und vergleiche_nachbarn {ergebnis}, erwartet war ({erwartet_paarweise}, {erwartet_nachbarn})."
)


def o_notation(text):
    """Vereinheitlicht verschiedene Schreibweisen wie O(n^2), O(n**2) und O(n * n)."""
    text = str(text).lower().replace(" ", "")
    for quadrat in ["**2", "^2", "*n", "·n", "⋅n"]:
        text = text.replace(quadrat, "²")
    return text


# Paarweise wächst die Zahl der Vergleiche quadratisch
assert o_notation(LAUFZEIT_PAARWEISE) == "o(n²)", (
    f"LAUFZEIT_PAARWEISE ist {LAUFZEIT_PAARWEISE!r}. Das stimmt nicht.\n"
    "Tipp: Wie viele Vergleiche sind es bei doppelt so vielen Adressen? Siehe die Ausgabe des Programms und den Hintergrund."
)

# Mit Nachbarn wächst die Zahl der Vergleiche linear
assert o_notation(LAUFZEIT_NACHBARN) == "o(n)", (
    f"LAUFZEIT_NACHBARN ist {LAUFZEIT_NACHBARN!r}. Das stimmt nicht.\n"
    "Tipp: Bei n Adressen sind es höchstens n - 1 Vergleiche. Feste Summanden wie - 1 lässt man weg."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "100 Adressen: 4950 paarweise, 99 Nachbarn\n"
    "200 Adressen: 19900 paarweise, 199 Nachbarn\n"
    "400 Adressen: 79800 paarweise, 399 Nachbarn"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
