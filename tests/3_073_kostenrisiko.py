# Automatisch erzeugt aus lehrkraft/muster/3_073_kostenrisiko.py - nicht von Hand ändern.
# vorlage-hash: aa72063622e8486a
# text-hash: c180140680655651
# thema: algorithmen
# inhalt: Monte-Carlo-Simulation, Pi schätzen

import math


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_pi(wuerfe, startwert):
    """Vergleichslösung: dieselbe Simulation mit eigenem Generator."""
    zufall = Zufall(startwert)
    treffer = 0
    for _ in range(wuerfe):
        x = zufall.random()
        y = zufall.random()
        treffer += x * x + y * y <= 1
    return 4 * treffer / wuerfe


def vergleich_kosten(zufall, positionen):
    """Vergleichslösung: ein Durchlauf mit dem Generator zufall."""
    return sum(zufall.uniform(von, bis) for von, bis in positionen)


def vergleich_ueberschreitung(positionen, budget, durchlaeufe, startwert):
    """Vergleichslösung: dieselbe Simulation mit eigenem Generator."""
    zufall = Zufall(startwert)
    zu_teuer = sum(1 for _ in range(durchlaeufe) if vergleich_kosten(zufall, positionen) > budget)
    return zu_teuer / durchlaeufe


def ungefaehr(a, b):
    """Prüft, ob a eine Zahl ist und bis auf Rundungsfehler gleich b."""
    return isinstance(a, (int, float)) and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


POSITIONEN = [(20000, 30000), (5000, 15000), (8000, 10000)]
TIPP_REIHENFOLGE = (
    "\nTipp: Ziehen Sie für jeden Wurf genau zwei Zahlen, erst x = random.random(), dann y = random.random(), "
    "und setzen Sie vorher random.seed(startwert)."
)

# schaetze_pi: das erste Beispiel aus der Aufgabe
ergebnis = wert_von(schaetze_pi, 1000, 3073)
assert ungefaehr(ergebnis, 3.124), f"schaetze_pi(1000, 3073) ergibt {ergebnis!r}, erwartet war 3.124." + TIPP_REIHENFOLGE

# schaetze_pi: andere Werte (nicht fest hinschreiben!)
ergebnis = wert_von(schaetze_pi, 500, 17)
erwartet = vergleich_pi(500, 17)
assert ungefaehr(ergebnis, erwartet), f"schaetze_pi(500, 17) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# schaetze_pi: das Ergebnis ist 4 · Treffer / wuerfe, nicht nur der Anteil
ergebnis = wert_von(schaetze_pi, 2000, 5)
erwartet = vergleich_pi(2000, 5)
assert ungefaehr(ergebnis, erwartet), f"schaetze_pi(2000, 5) ergibt {ergebnis!r}, erwartet war {erwartet!r}." + (
    "\nTipp: Das ist nur der Anteil der Treffer. Der Viertelkreis hat die Fläche π/4, also gehört der Faktor 4 dazu."
    if ungefaehr(ergebnis, erwartet / 4)
    else ""
)

# schaetze_pi: derselbe Startwert ergibt dasselbe Ergebnis
erstes = wert_von(schaetze_pi, 300, 42)
random.random()
zweites = wert_von(schaetze_pi, 300, 42)
assert erstes == zweites and ungefaehr(erstes, vergleich_pi(300, 42)), (
    f"Zweimal schaetze_pi(300, 42) ergibt {erstes!r} und {zweites!r}; erwartet war beide Male "
    f"{vergleich_pi(300, 42)!r}.\nTipp: Rufen Sie random.seed(startwert) am Anfang von schaetze_pi auf."
)

# schaetze_pi: ein einziger Wurf ergibt 4 oder 0
for startwert, erwartet in [(1, 4.0), (2, 0.0)]:
    ergebnis = wert_von(schaetze_pi, 1, startwert)
    assert ungefaehr(ergebnis, erwartet), f"schaetze_pi(1, {startwert}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# schaetze_pi: viele Würfe kommen nahe an π
ergebnis = wert_von(schaetze_pi, 200_000, 2026)
assert ungefaehr(ergebnis, vergleich_pi(200_000, 2026)) and abs(ergebnis - math.pi) < 0.02, (
    f"schaetze_pi(200000, 2026) ergibt {ergebnis!r}, erwartet war {vergleich_pi(200_000, 2026)!r} "
    f"(π ist {math.pi:.5f})."
)

zufall = Zufall(3073)

# schaetze_pi: viele zufällige Startwerte
for _ in range(50):
    wuerfe, startwert = zufall.randint(1, 300), zufall.randint(-10**6, 10**6)
    ergebnis, erwartet = wert_von(schaetze_pi, wuerfe, startwert), vergleich_pi(wuerfe, startwert)
    assert ungefaehr(ergebnis, erwartet), (
        f"schaetze_pi({wuerfe}, {startwert}) ergibt {ergebnis!r}, erwartet war {erwartet!r}." + TIPP_REIHENFOLGE
    )

# gesamtkosten: das Beispiel aus der Aufgabe
random.seed(7)
ergebnis = wert_von(gesamtkosten, POSITIONEN)
erwartet = vergleich_kosten(Zufall(7), POSITIONEN)
assert ungefaehr(ergebnis, erwartet), (
    f"Nach random.seed(7) ergibt gesamtkosten({POSITIONEN}) {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Ziehen Sie für jede Position der Reihe nach genau einen Betrag mit random.uniform(von, bis)."
)

# gesamtkosten: setzt den Zufall nicht zurück, zwei Aufrufe ergeben verschiedene Beträge
random.seed(8)
erstes = wert_von(gesamtkosten, POSITIONEN)
zweites = wert_von(gesamtkosten, POSITIONEN)
vergleich = Zufall(8)
erwartet = (vergleich_kosten(vergleich, POSITIONEN), vergleich_kosten(vergleich, POSITIONEN))
assert ungefaehr(erstes, erwartet[0]) and ungefaehr(zweites, erwartet[1]), (
    f"Nach random.seed(8) ergeben zwei Aufrufe von gesamtkosten {erstes!r} und {zweites!r}; erwartet waren "
    f"{erwartet[0]!r} und {erwartet[1]!r}.\nTipp: gesamtkosten ruft random.seed nicht auf."
)

# gesamtkosten: andere Positionen
random.seed(9)
positionen = [(100, 200), (0, 50), (1000, 1000)]
ergebnis = wert_von(gesamtkosten, positionen)
erwartet = vergleich_kosten(Zufall(9), positionen)
assert ungefaehr(ergebnis, erwartet), f"Nach random.seed(9) ergibt gesamtkosten({positionen}) {ergebnis!r}, erwartet war {erwartet!r}."

# gesamtkosten: keine Positionen kosten nichts
ergebnis = wert_von(gesamtkosten, [])
assert ungefaehr(ergebnis, 0), f"gesamtkosten([]) ergibt {ergebnis!r}, erwartet war 0."

# ueberschreitung: das Beispiel aus der Aufgabe
ergebnis = wert_von(ueberschreitung, POSITIONEN, 50000, 10000, 3073)
assert ungefaehr(ergebnis, 0.0798), (
    f"ueberschreitung({POSITIONEN}, 50000, 10000, 3073) ergibt {ergebnis!r}, erwartet war 0.0798.\n"
    "Tipp: Erst random.seed(startwert), dann durchlaeufe-mal gesamtkosten(positionen) aufrufen und zählen, wie oft "
    "die Summe größer als budget ist; zum Schluss durch durchlaeufe teilen."
)

# ueberschreitung: andere Werte (nicht fest hinschreiben!)
ergebnis = wert_von(ueberschreitung, POSITIONEN, 45000, 2000, 11)
erwartet = vergleich_ueberschreitung(POSITIONEN, 45000, 2000, 11)
assert ungefaehr(ergebnis, erwartet), f"ueberschreitung({POSITIONEN}, 45000, 2000, 11) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# ueberschreitung: das Ergebnis ist ein Anteil von 0 bis 1, keine Anzahl
ergebnis = wert_von(ueberschreitung, POSITIONEN, 40000, 1000, 12)
erwartet = vergleich_ueberschreitung(POSITIONEN, 40000, 1000, 12)
assert ungefaehr(ergebnis, erwartet), (
    f"ueberschreitung({POSITIONEN}, 40000, 1000, 12) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    + ("\nTipp: Teilen Sie die Anzahl durch durchlaeufe." if ungefaehr(ergebnis, erwartet * 1000) else "")
)

# ueberschreitung: genau das Budget ist keine Überschreitung
ergebnis = wert_von(ueberschreitung, [(1000, 1000), (500, 500)], 1500, 10, 1)
assert ungefaehr(ergebnis, 0), (
    f"ueberschreitung([(1000, 1000), (500, 500)], 1500, 10, 1) ergibt {ergebnis!r}, erwartet war 0: Die Kosten "
    "sind immer genau 1500, das Budget wird also nie überschritten.\nTipp: Zählen Sie nur Summen, die größer als "
    "budget sind."
)

# ueberschreitung: immer über dem Budget ergibt 1
ergebnis = wert_von(ueberschreitung, [(10, 20)], 5, 50, 1)
assert ungefaehr(ergebnis, 1), f"ueberschreitung([(10, 20)], 5, 50, 1) ergibt {ergebnis!r}, erwartet war 1."

# ueberschreitung: ohne Positionen wird ein Budget von 0 nie überschritten
ergebnis = wert_von(ueberschreitung, [], 0, 20, 1)
assert ungefaehr(ergebnis, 0), f"ueberschreitung([], 0, 20, 1) ergibt {ergebnis!r}, erwartet war 0."

# ueberschreitung: benutzt gesamtkosten und setzt den Startwert nur einmal
ergebnis = wert_von(ueberschreitung, POSITIONEN, 48000, 300, 99)
erwartet = vergleich_ueberschreitung(POSITIONEN, 48000, 300, 99)
assert ungefaehr(ergebnis, erwartet), (
    f"ueberschreitung({POSITIONEN}, 48000, 300, 99) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: random.seed(startwert) gehört einmal an den Anfang, nicht in die Schleife; sonst ist jeder Durchlauf gleich."
)

# ueberschreitung: viele zufällige Projekte
for _ in range(60):
    positionen = []
    for _ in range(zufall.randint(0, 6)):
        von = zufall.randint(0, 10**4)
        positionen.append((von, von + zufall.randint(0, 10**4)))
    budget = zufall.randint(0, 3 * 10**4)
    durchlaeufe, startwert = zufall.randint(1, 100), zufall.randint(0, 10**6)
    ergebnis = wert_von(ueberschreitung, positionen, budget, durchlaeufe, startwert)
    erwartet = vergleich_ueberschreitung(positionen, budget, durchlaeufe, startwert)
    assert ungefaehr(ergebnis, erwartet), (
        f"ueberschreitung({positionen}, {budget}, {durchlaeufe}, {startwert}) ergibt {ergebnis!r}, "
        f"erwartet war {erwartet!r}."
    )

# Obere Grenze: 20000 Durchläufe mit 20 Positionen
positionen = [(10**6 * k, 10**6 * k + 10**6) for k in range(20)]
ergebnis = wert_von(ueberschreitung, positionen, 200_000_000, 20_000, 7)
erwartet = vergleich_ueberschreitung(positionen, 200_000_000, 20_000, 7)
assert ungefaehr(ergebnis, erwartet), (
    f"ueberschreitung mit 20 Positionen und 20000 Durchläufen ergibt {ergebnis!r}, erwartet war {erwartet!r}."
)
