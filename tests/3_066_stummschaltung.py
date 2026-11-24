# Automatisch erzeugt aus lehrkraft/muster/3_066_stummschaltung.py - nicht von Hand ändern.
# vorlage-hash: 29cf3d975a2207d0
# text-hash: 767db08dea1a52b9
# thema: algorithmen
# inhalt: Greedy: Wechselgeld und Gegenbeispiel

STANDARD = [60, 30, 10, 5, 1]


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def als_dict(ergebnis):
    """Macht aus einer Liste von Paaren (stufe, anzahl) ein Dictionary ohne Nullen; sonst None."""
    if not isinstance(ergebnis, (list, tuple)):
        return None
    inhalt = {}
    for paar in ergebnis:
        if not isinstance(paar, (list, tuple)) or len(paar) != 2:
            return None
        stufe, anzahl = paar
        if anzahl != 0:
            inhalt[stufe] = inhalt.get(stufe, 0) + anzahl
    return inhalt


def bereinigt(ergebnis):
    """Macht aus einer Liste von Paaren eine Liste von Tupeln ohne Anzahl 0; anderes bleibt, wie es ist."""
    if not isinstance(ergebnis, list):
        return ergebnis
    paare = []
    for paar in ergebnis:
        if not isinstance(paar, (list, tuple)) or len(paar) != 2:
            return ergebnis
        if paar[1] != 0:
            paare.append(tuple(paar))
    return paare


def gierig_von_hand(minuten, stufen):
    """Langsame Vergleichslösung: zieht immer wieder die größte passende Stufe einzeln ab."""
    zaehler = {}
    rest = minuten
    while rest > 0:
        groesste = max(stufe for stufe in stufen if stufe <= rest)
        zaehler[groesste] = zaehler.get(groesste, 0) + 1
        rest = rest - groesste
    return [(stufe, zaehler[stufe]) for stufe in sorted(zaehler, reverse=True)]


def gegenbeispiel_von_hand(stufen, bis):
    """Vergleichslösung: eigene gierige Stückelung gegen eine eigene Tabelle der besten Klickzahlen."""
    beste = [0] + [None] * bis
    for d in range(1, bis + 1):
        beste[d] = min(beste[d - stufe] + 1 for stufe in stufen if stufe <= d)
        rest, klicks = d, 0
        for stufe in sorted(stufen, reverse=True):
            klicks, rest = klicks + rest // stufe, rest % stufe
        if klicks > beste[d]:
            return d
    return None


def meldung_gierig(minuten, stufen, ergebnis, erwartet, tipp=""):
    """Baut die Meldung für einen falschen Wert von gierig."""
    text = f"gierig({minuten}, {stufen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    if ergebnis is None:
        text = text + "\nTipp: Geben Sie die Liste mit return zurück."
    elif tipp:
        text = text + "\nTipp: " + tipp
    return text


def inhalt_stimmt(minuten, stufen, erwartet, tipp=""):
    """Prüft locker, ob gierig die richtigen Anzahlen liefert (Reihenfolge egal); liefert (stimmt, Meldung)."""
    ergebnis = wert_von(gierig, minuten, list(stufen))
    stimmt = als_dict(ergebnis) == dict(erwartet)
    return stimmt, meldung_gierig(minuten, stufen, ergebnis, erwartet, tipp)


def meldung_gegenbeispiel(stufen, bis, ergebnis, erwartet, tipp=""):
    """Baut die Meldung für einen falschen Wert von gegenbeispiel."""
    text = f"gegenbeispiel({stufen}, {bis}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    if tipp:
        text = text + "\nTipp: " + tipp
    return text


# gierig: das Beispiel mit 75 Minuten (Anzahlen stimmen)
stimmt, text = inhalt_stimmt(75, STANDARD, [(60, 1), (10, 1), (5, 1)])
assert stimmt, text

# gierig: 137 Minuten, eine Stufe mehrmals (nicht fest hinschreiben!)
stimmt, text = inhalt_stimmt(
    137, STANDARD, [(60, 2), (10, 1), (5, 1), (1, 2)],
    "Nehmen Sie jede Stufe so oft, wie sie in den Rest passt: 137 // 60 ist 2.",
)
assert stimmt, text

# gierig: 59 Minuten, jede kleinere Stufe kommt dran
stimmt, text = inhalt_stimmt(59, STANDARD, [(30, 1), (10, 2), (5, 1), (1, 4)])
assert stimmt, text

# gierig: Liste von Tupeln, von der größten Stufe zur kleinsten
ergebnis = wert_von(gierig, 137, list(STANDARD))
assert ergebnis == [(60, 2), (10, 1), (5, 1), (1, 2)], meldung_gierig(
    137, STANDARD, ergebnis, [(60, 2), (10, 1), (5, 1), (1, 2)],
    "Geben Sie eine Liste von Tupeln (stufe, anzahl) zurück, die größte Stufe zuerst.",
)

# gierig: Stufen, die nicht geklickt werden, fehlen in der Liste
ergebnis = wert_von(gierig, 120, list(STANDARD))
assert ergebnis == [(60, 2)], meldung_gierig(
    120, STANDARD, ergebnis, [(60, 2)], "Hängen Sie ein Tupel nur an, wenn die Anzahl größer als 0 ist."
)

# gierig: die Stufen dürfen in beliebiger Reihenfolge kommen
ergebnis = wert_von(gierig, 75, [5, 60, 1, 30, 10])
assert bereinigt(ergebnis) == [(60, 1), (10, 1), (5, 1)], meldung_gierig(
    75, [5, 60, 1, 30, 10], ergebnis, [(60, 1), (10, 1), (5, 1)],
    "Sortieren Sie die Stufen zuerst absteigend: sorted(stufen, reverse=True).",
)

# gierig: die Liste stufen bleibt unverändert
eingabe = [5, 60, 1, 30, 10]
wert_von(gierig, 75, eingabe)
assert eingabe == [5, 60, 1, 30, 10], (
    f"gierig hat die übergebene Liste stufen verändert, sie ist jetzt {eingabe!r}.\n"
    "Tipp: sorted(stufen, reverse=True) liefert eine neue Liste, stufen.sort() ändert die alte."
)

# gierig: bei nicht passenden Stufen bleibt es gierig (das Beispiel mit 25, 15, 1)
ergebnis = wert_von(gierig, 30, [25, 15, 1])
assert bereinigt(ergebnis) == [(25, 1), (1, 5)], meldung_gierig(
    30, [25, 15, 1], ergebnis, [(25, 1), (1, 5)],
    "gierig soll immer die größte passende Stufe nehmen, auch wenn das nicht die wenigsten Klicks sind.",
)

# gierig: nur die Stufe 1
ergebnis = wert_von(gierig, 7, [1])
assert bereinigt(ergebnis) == [(1, 7)], meldung_gierig(7, [1], ergebnis, [(1, 7)])

# gierig: 0 Minuten brauchen keinen Klick
ergebnis = wert_von(gierig, 0, list(STANDARD))
assert bereinigt(ergebnis) == [], meldung_gierig(0, STANDARD, ergebnis, [], "Bei 0 Minuten wird keine Stufe geklickt: [].")

# gierig: genau eine Stufe
ergebnis = wert_von(gierig, 1000, [1000, 1])
assert bereinigt(ergebnis) == [(1000, 1)], meldung_gierig(1000, [1000, 1], ergebnis, [(1000, 1)])

# gierig: 300 zufällige Fälle, verglichen mit einzelnem Abziehen
zufall = Zufall(3066)
for _ in range(300):
    stufen = zufall.sample(range(2, 60), zufall.randint(0, 6)) + [1]
    zufall.shuffle(stufen)
    minuten = zufall.randint(0, 500)
    erwartet = gierig_von_hand(minuten, stufen)
    ergebnis = wert_von(gierig, minuten, list(stufen))
    assert bereinigt(ergebnis) == erwartet, meldung_gierig(minuten, stufen, ergebnis, erwartet)

# gierig: Laufzeit hängt nicht von der Zahl der Minuten ab
ergebnis_klein, schritte_klein = zaehle_schritte(gierig, 10_000, [60, 1])
ergebnis_gross, schritte_gross = zaehle_schritte(gierig, 40_000, [60, 1])
assert bereinigt(ergebnis_gross) == [(60, 666), (1, 40)] and schritte_gross <= 2 * max(schritte_klein, 1) + 10, (
    f"gierig(10000, [60, 1]) braucht {schritte_klein} Schritte, gierig(40000, [60, 1]) {schritte_gross}. "
    "Die Zahl der Schritte soll nicht mit minuten wachsen.\n"
    "Tipp: anzahl = rest // stufe und rest = rest % stufe statt rest = rest - stufe in einer Schleife."
)

# gegenbeispiel: Stufen 4, 3, 1 – bei 6 Minuten reicht gierig nicht
ergebnis = wert_von(gegenbeispiel, [4, 3, 1], 20)
assert ergebnis == 6, meldung_gegenbeispiel(
    [4, 3, 1], 20, ergebnis, 6, "Gierig: 4 + 1 + 1 sind drei Klicks, wenigste_klicks findet zwei (3 + 3)."
)

# gegenbeispiel: das Beispiel mit 25, 15, 1 (nicht fest hinschreiben!)
ergebnis = wert_von(gegenbeispiel, [25, 15, 1], 100)
assert ergebnis == 30, meldung_gegenbeispiel(
    [25, 15, 1], 100, ergebnis, 30,
    "Zählen Sie für jedes d die Klicks der gierigen Stückelung (Summe der Anzahlen) und vergleichen Sie mit "
    "wenigste_klicks(bis, stufen)[d]. Gesucht ist das kleinste solche d. Rufen Sie wenigste_klicks nur einmal "
    "vor der Schleife auf, sonst dauert es bei großem bis zu lange.",
)

# gegenbeispiel: bei 60, 30, 10, 5, 1 ist gierig immer am besten
ergebnis = wert_von(gegenbeispiel, list(STANDARD), 1000)
assert ergebnis is None, meldung_gegenbeispiel(
    STANDARD, 1000, ergebnis, None, "Gibt es kein d, bei dem gierig schlechter ist, geben Sie None zurück."
)

# gegenbeispiel: bis gehört noch dazu
ergebnis = wert_von(gegenbeispiel, [25, 15, 1], 30)
assert ergebnis == 30, meldung_gegenbeispiel(
    [25, 15, 1], 30, ergebnis, 30, "Prüfen Sie alle d von 1 bis einschließlich bis: range(1, bis + 1)."
)

# gegenbeispiel: liegt das erste Gegenbeispiel hinter bis, gibt es keins
ergebnis = wert_von(gegenbeispiel, [25, 15, 1], 29)
assert ergebnis is None, meldung_gegenbeispiel([25, 15, 1], 29, ergebnis, None)

# gegenbeispiel: nur die Stufe 1, bis = 1
ergebnis = wert_von(gegenbeispiel, [1], 1)
assert ergebnis is None, meldung_gegenbeispiel([1], 1, ergebnis, None)

# gegenbeispiel: unsortierte Stufen (1, 7, 10: 14 = 7 + 7)
ergebnis = wert_von(gegenbeispiel, [1, 10, 7], 50)
assert ergebnis == 14, meldung_gegenbeispiel([1, 10, 7], 50, ergebnis, 14)

# gegenbeispiel: 300 zufällige Stufen, verglichen mit einer eigenen Rechnung
for _ in range(300):
    stufen = zufall.sample(range(2, 30), zufall.randint(0, 4)) + [1]
    zufall.shuffle(stufen)
    bis = zufall.randint(1, 80)
    erwartet = gegenbeispiel_von_hand(stufen, bis)
    ergebnis = wert_von(gegenbeispiel, list(stufen), bis)
    assert ergebnis == erwartet, meldung_gegenbeispiel(stufen, bis, ergebnis, erwartet)

# Obere Grenze: gierig mit 10**9 Minuten
ergebnis = wert_von(gierig, 10**9, [7, 1000, 1, 999])
erwartet = [(1000, 1_000_000)]
assert bereinigt(ergebnis) == erwartet, meldung_gierig(10**9, [7, 1000, 1, 999], ergebnis, erwartet)

# Obere Grenze: gegenbeispiel mit bis = 10 000 und zehn Stufen ohne Gegenbeispiel
stufen = [1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
ergebnis = wert_von(gegenbeispiel, list(stufen), 10_000)
assert ergebnis is None, meldung_gegenbeispiel(stufen, 10_000, ergebnis, None)
