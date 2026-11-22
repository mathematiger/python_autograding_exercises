# Automatisch erzeugt aus lehrkraft/muster/3_045_kachelraster.py - nicht von Hand ändern.
# vorlage-hash: 90cd59c9a39448e4
# text-hash: 1e64ca9c327ee674
# thema: programmaufbau
# inhalt: math, statistics, random nutzen

import random


def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_zeilen(kacheln, breite, kachelbreite):
    """Vergleichslösung: zählt Zeilen, bis alle Kacheln untergebracht sind (ganzzahlig)."""
    je_zeile = breite // kachelbreite
    return (kacheln + je_zeile - 1) // je_zeile


def vergleich_bericht(breiten):
    """Vergleichslösung: zählt mit einem Dictionary und sortiert für den Median."""
    anzahl = {}
    for wert in breiten:
        anzahl[wert] = anzahl.get(wert, 0) + 1
    haeufigste = breiten[0]
    for wert in breiten:
        if anzahl[wert] > anzahl[haeufigste]:
            haeufigste = wert
    sortiert = sorted(breiten)
    mitte = len(sortiert) // 2
    if len(sortiert) % 2 == 1:
        return (haeufigste, sortiert[mitte])
    return (haeufigste, (sortiert[mitte - 1] + sortiert[mitte]) / 2)


def vergleich_gruppen(personen, startwert):
    """Vergleichslösung: mischt wie verlangt und teilt mit (n + 1) // 2."""
    gemischt = personen[:]
    random.Random(startwert).shuffle(gemischt)
    mitte = (len(gemischt) + 1) // 2
    return (gemischt[:mitte], gemischt[mitte:])


def als_listen(ergebnis):
    """Macht aus einem Tupel zweier Folgen ein Tupel zweier Listen; anderes bleibt, wie es ist."""
    if isinstance(ergebnis, tuple) and len(ergebnis) == 2 and all(isinstance(teil, (list, tuple)) for teil in ergebnis):
        return (list(ergebnis[0]), list(ergebnis[1]))
    return ergebnis


NAMEN = ["Ada", "Ben", "Cem", "Dana", "Eli"]

# zeilen_im_raster im Beispiel
ergebnis = wert_von(lambda: zeilen_im_raster(10, 1000, 300))
assert ergebnis == 4, (
    f"zeilen_im_raster(10, 1000, 300) ergibt {ergebnis!r}, erwartet war 4 (3 Kacheln je Zeile, die vierte Zeile ist angefangen).\n"
    "Tipp: math.ceil(kacheln / je_zeile) rundet auf."
)

# zeilen_im_raster, wenn die Kacheln genau aufgehen (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: [zeilen_im_raster(12, 1000, 250), zeilen_im_raster(9, 900, 300)])
assert ergebnis == [3, 3], (
    f"zeilen_im_raster(12, 1000, 250) und zeilen_im_raster(9, 900, 300) ergeben {ergebnis!r}, erwartet war [3, 3].\n"
    "Tipp: Geht die Teilung auf, gibt es keine angefangene Zeile."
)

# zeilen_im_raster: nur ganze Kacheln passen in eine Zeile
ergebnis = wert_von(lambda: zeilen_im_raster(7, 1000, 400))
assert ergebnis == 4, (
    f"zeilen_im_raster(7, 1000, 400) ergibt {ergebnis!r}, erwartet war 4 (nur 2 ganze Kacheln je Zeile).\n"
    "Tipp: Teilen Sie die Breite mit //, nicht mit /."
)

# zeilen_im_raster ohne Kacheln und mit einer Kachel je Zeile
ergebnis = wert_von(lambda: [zeilen_im_raster(0, 1000, 300), zeilen_im_raster(5, 500, 500), zeilen_im_raster(1, 10000, 1)])
assert ergebnis == [0, 5, 1], f"zeilen_im_raster(0, 1000, 300), (5, 500, 500) und (1, 10000, 1) ergeben {ergebnis!r}, erwartet war [0, 5, 1]."

# zeilen_im_raster benutzt math.ceil
assert verwendet("ceil"), "Benutzen Sie in zeilen_im_raster math.ceil, wie verlangt."

# breitenbericht im Beispiel
ergebnis = wert_von(lambda: breitenbericht([1920, 1366, 1920, 390, 1536]))
assert ergebnis == (1920, 1536), (
    f"breitenbericht([1920, 1366, 1920, 390, 1536]) ergibt {ergebnis!r}, erwartet war (1920, 1536).\n"
    "Tipp: return (statistics.mode(breiten), statistics.median(breiten))."
)

# breitenbericht mit einer anderen häufigsten Breite (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: breitenbericht([390, 1440, 390, 2560, 390, 1440, 800]))
assert ergebnis == (390, 800), f"breitenbericht([390, 1440, 390, 2560, 390, 1440, 800]) ergibt {ergebnis!r}, erwartet war (390, 800)."

# breitenbericht: Median bei gerader Anzahl ist der Mittelwert der beiden mittleren
ergebnis = wert_von(lambda: breitenbericht([1280, 1920, 1366, 1920]))
assert ergebnis == (1920, 1643), (
    f"breitenbericht([1280, 1920, 1366, 1920]) ergibt {ergebnis!r}, erwartet war (1920, 1643.0).\n"
    "Tipp: Bei gerader Anzahl liegt der Median zwischen den beiden mittleren Werten der sortierten Liste."
)

# breitenbericht: bei Gleichstand zählt die Breite, die zuerst vorkommt
ergebnis = wert_von(lambda: breitenbericht([1536, 1920, 1920, 1536, 390]))
assert ergebnis == (1536, 1536), (
    f"breitenbericht([1536, 1920, 1920, 1536, 390]) ergibt {ergebnis!r}, erwartet war (1536, 1536).\n"
    "Tipp: statistics.mode nimmt bei Gleichstand den Wert, der zuerst vorkommt; max oder sorted entscheiden anders."
)

# breitenbericht mit nur einem Besuch
ergebnis = wert_von(lambda: breitenbericht([1024]))
assert ergebnis == (1024, 1024), f"breitenbericht([1024]) ergibt {ergebnis!r}, erwartet war (1024, 1024)."

# breitenbericht verändert die Liste nicht
breiten = [1920, 1366, 1920, 390, 1536]
wert_von(lambda: breitenbericht(breiten))
assert breiten == [1920, 1366, 1920, 390, 1536], f"breitenbericht hat die übergebene Liste verändert: {breiten}."

# breitenbericht benutzt statistics.mode und statistics.median
assert verwendet("mode") and verwendet("median"), "Benutzen Sie in breitenbericht statistics.mode und statistics.median, wie verlangt."

# ab_gruppen im Beispiel
ergebnis = als_listen(wert_von(lambda: ab_gruppen(list(NAMEN), 3)))
assert ergebnis == (["Ada", "Cem", "Dana"], ["Eli", "Ben"]), (
    f"ab_gruppen({NAMEN}, 3) ergibt {ergebnis!r}, erwartet war (['Ada', 'Cem', 'Dana'], ['Eli', 'Ben']).\n"
    "Tipp: gemischt = list(personen), dann random.Random(startwert).shuffle(gemischt)."
)

# ab_gruppen: beide Gruppen zusammen enthalten alle Personen genau einmal
ergebnis = als_listen(wert_von(lambda: ab_gruppen(list(NAMEN), 11)))
assert isinstance(ergebnis, tuple) and sorted(ergebnis[0] + ergebnis[1]) == sorted(NAMEN), (
    f"ab_gruppen({NAMEN}, 11) ergibt {ergebnis!r}; erwartet waren zwei Gruppen, die zusammen alle fünf Namen genau einmal enthalten."
)

# ab_gruppen: Gruppe A hat bei ungerader Zahl eine Person mehr
assert [len(ergebnis[0]), len(ergebnis[1])] == [3, 2], (
    f"Bei fünf Personen haben die Gruppen {len(ergebnis[0])} und {len(ergebnis[1])} Personen, erwartet war 3 und 2.\n"
    "Tipp: math.ceil(len(gemischt) / 2) ist die Größe von Gruppe A."
)

# ab_gruppen mit anderem Startwert (nicht fest hinschreiben!)
ergebnis = als_listen(wert_von(lambda: ab_gruppen(list(NAMEN), 11)))
erwartet = vergleich_gruppen(list(NAMEN), 11)
assert ergebnis == erwartet, f"ab_gruppen({NAMEN}, 11) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# ab_gruppen mit gerader Zahl
personen = ["Fe", "Gil", "Hao", "Ida", "Jo", "Kai"]
ergebnis = als_listen(wert_von(lambda: ab_gruppen(list(personen), 2052)))
erwartet = vergleich_gruppen(personen, 2052)
assert ergebnis == erwartet, f"ab_gruppen({personen}, 2052) ergibt {ergebnis!r}, erwartet war {erwartet!r} (je drei Personen)."

# ab_gruppen verändert die übergebene Liste nicht
personen = list(NAMEN)
wert_von(lambda: ab_gruppen(personen, 3))
assert personen == NAMEN, f"ab_gruppen hat die übergebene Liste verändert: {personen}. Mischen Sie eine Kopie."

# ab_gruppen benutzt den globalen Zufall nicht
random.seed(1)
vorher = random.random()
random.seed(1)
wert_von(lambda: ab_gruppen(list(NAMEN), 3))
assert random.random() == vorher, (
    "ab_gruppen verändert die Zahlenfolge des Moduls random. Benutzen Sie random.Random(startwert) statt random.seed oder random.shuffle."
)

# ab_gruppen ohne und mit einer Person
ergebnis = [als_listen(wert_von(lambda: ab_gruppen([], 5))), als_listen(wert_von(lambda: ab_gruppen(["Ada"], 5)))]
assert ergebnis == [([], []), (["Ada"], [])], f"ab_gruppen([], 5) und ab_gruppen(['Ada'], 5) ergeben {ergebnis!r}, erwartet war [([], []), (['Ada'], [])]."

# Die Ausgabe des Programms
erwartet = "4\n(1920, 1536)\n(['Ada', 'Cem', 'Dana'], ['Eli', 'Ben'])"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Eingaben
zufall = Zufall(3045)
for _ in range(300):
    kachelbreite = zufall.randint(1, 3000)
    breite = zufall.randint(kachelbreite, 10000)
    kacheln = zufall.randint(0, 1000)
    ergebnis = wert_von(lambda: zeilen_im_raster(kacheln, breite, kachelbreite))
    erwartet = vergleich_zeilen(kacheln, breite, kachelbreite)
    assert ergebnis == erwartet, f"zeilen_im_raster({kacheln}, {breite}, {kachelbreite}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    breiten = [zufall.choice([360, 390, 1366, 1536, 1920, 2560, zufall.randint(240, 7680)]) for _ in range(zufall.randint(1, 12))]
    ergebnis = wert_von(lambda: breitenbericht(list(breiten)))
    assert ergebnis == vergleich_bericht(breiten), f"breitenbericht({breiten}) ergibt {ergebnis!r}, erwartet war {vergleich_bericht(breiten)}."
    personen = [f"P{nummer}" for nummer in range(zufall.randint(0, 9))]
    startwert = zufall.randint(0, 10**9)
    ergebnis = als_listen(wert_von(lambda: ab_gruppen(list(personen), startwert)))
    erwartet = vergleich_gruppen(personen, startwert)
    assert ergebnis == erwartet, f"ab_gruppen({personen}, {startwert}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Obere Grenze: eine Million Kacheln
ergebnis = wert_von(lambda: [zeilen_im_raster(10**6, 10000, 1), zeilen_im_raster(10**6, 10000, 7), zeilen_im_raster(999999, 10000, 10000)])
assert ergebnis == [100, vergleich_zeilen(10**6, 10000, 7), 999999], f"zeilen_im_raster an der oberen Grenze ergibt {ergebnis!r}."
# Obere Grenze: 100 000 Besuche
breiten = [zufall.randint(240, 7680) for _ in range(100000)]
ergebnis = wert_von(lambda: breitenbericht(breiten))
assert ergebnis == vergleich_bericht(breiten), f"breitenbericht mit 100 000 Breiten ergibt {ergebnis!r}, erwartet war {vergleich_bericht(breiten)}."
# Obere Grenze: 10 000 Personen
personen = [f"P{nummer}" for nummer in range(10000)]
ergebnis = als_listen(wert_von(lambda: ab_gruppen(personen, 10**9)))
assert ergebnis == vergleich_gruppen(personen, 10**9), "ab_gruppen mit 10 000 Personen stimmt nicht mit der Vergleichslösung überein."
