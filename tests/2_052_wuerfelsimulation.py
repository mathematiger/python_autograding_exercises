# Automatisch erzeugt aus lehrkraft/muster/2_052_wuerfelsimulation.py - nicht von Hand ändern.
# vorlage-hash: d2ef20caf9c2781f
# text-hash: 8190d03c45d1921c
# thema: algorithmen
# inhalt: Würfel simulieren, Augensumme

import random


def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def mit_startzahl(startzahl, aufruf):
    """Setzt random.seed(startzahl) und führt dann den Aufruf aus."""
    random.seed(startzahl)
    return wert_von(aufruf)


def vergleich_wurf(anzahl):
    """Vergleichslösung: zieht die Würfel als Liste und addiert sie."""
    augen = [random.randint(1, 6) for _ in range(anzahl)]
    return sum(augen)


def vergleich_verteilung(wuerfe, anzahl):
    """Vergleichslösung: erst alle Würfe sammeln, dann jede Summe mit count zählen."""
    summen = [vergleich_wurf(anzahl) for _ in range(wuerfe)]
    return {summe: summen.count(summe) for summe in range(anzahl, 6 * anzahl + 1)}


def vergleich_haeufigste(zaehler):
    """Vergleichslösung: größte Anzahl, dann die kleinste Summe mit dieser Anzahl."""
    groesste = max(zaehler.values())
    return min(summe for summe in zaehler if zaehler[summe] == groesste)


# wurf(1) liefert eine Augenzahl von 1 bis 6
ergebnisse = [mit_startzahl(startzahl, lambda: wurf(1)) for startzahl in range(200)]
falsch = [wert for wert in ergebnisse if wert not in [1, 2, 3, 4, 5, 6]]
assert falsch == [], f"wurf(1) ergibt unter anderem {falsch[:5]}, erwartet war jedes Mal eine Zahl von 1 bis 6."

# wurf(1) liefert alle sechs Augenzahlen, nicht immer dieselbe
assert sorted(set(ergebnisse)) == [1, 2, 3, 4, 5, 6], (
    f"wurf(1) ergibt bei 200 Startzahlen nur {sorted(set(ergebnisse))}, erwartet waren alle Augenzahlen von 1 bis 6.\n"
    "Tipp: random.randint(1, 6) würfelt einen Würfel."
)

# wurf(2) liefert Augensummen von 2 bis 12
ergebnisse = [mit_startzahl(startzahl, lambda: wurf(2)) for startzahl in range(300)]
falsch = [wert for wert in ergebnisse if wert not in range(2, 13)]
assert falsch == [] and 2 in ergebnisse and 12 in ergebnisse, (
    f"wurf(2) ergibt bei 300 Startzahlen die Werte {sorted(set(map(str, ergebnisse)))}, erwartet waren Augensummen von 2 bis 12.\n"
    "Tipp: Würfeln Sie in einer Schleife anzahl-mal und addieren Sie die Augen."
)

# wurf im Beispiel: nach random.seed(2052) ergibt wurf(2) 9
ergebnis = mit_startzahl(2052, lambda: wurf(2))
assert ergebnis == 9, (
    f"Nach random.seed(2052) ergibt wurf(2) {ergebnis!r}, erwartet war 9.\n"
    "Tipp: Benutzen Sie für jeden Würfel genau einmal random.randint(1, 6) und kein random.seed in der Funktion."
)

# wurf zieht je Würfel genau eine Zahl, auch bei anderen Startzahlen und Anzahlen
for startzahl, anzahl in [(1, 2), (7, 3), (42, 5), (99, 10)]:
    ergebnis = mit_startzahl(startzahl, lambda: wurf(anzahl))
    erwartet = mit_startzahl(startzahl, lambda: vergleich_wurf(anzahl))
    assert ergebnis == erwartet, (
        f"Nach random.seed({startzahl}) ergibt wurf({anzahl}) {ergebnis!r}, erwartet war {erwartet}.\n"
        f"Tipp: Rufen Sie random.randint(1, 6) genau {anzahl}-mal auf."
    )

# verteilung enthält jede mögliche Augensumme als Schlüssel, auch ohne Würfe
ergebnis = wert_von(lambda: verteilung(0, 2))
erwartet = {summe: 0 for summe in range(2, 13)}
assert ergebnis == erwartet, (
    f"verteilung(0, 2) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: Tragen Sie vor dem Würfeln jede Summe von anzahl bis 6 * anzahl mit 0 ein."
)

# verteilung zählt genau wuerfe Würfe
ergebnis = mit_startzahl(3, lambda: verteilung(500, 3))
gesamt = sum(ergebnis.values()) if isinstance(ergebnis, dict) else ergebnis
assert gesamt == 500, f"Die Anzahlen von verteilung(500, 3) ergeben zusammen {gesamt!r}, erwartet war 500."

# verteilung im Beispiel
ergebnis = mit_startzahl(2052, lambda: (wurf(2), verteilung(5, 1)))
erwartet = (9, {1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 2})
assert ergebnis == erwartet, (
    f"Nach random.seed(2052) ergeben wurf(2) und verteilung(5, 1) {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: verteilung soll für jeden Wurf wurf(anzahl) aufrufen."
)

# verteilung mit anderen Startzahlen (nicht fest hinschreiben!)
for startzahl, wuerfe, anzahl in [(10, 20, 2), (11, 50, 4)]:
    ergebnis = mit_startzahl(startzahl, lambda: verteilung(wuerfe, anzahl))
    erwartet = mit_startzahl(startzahl, lambda: vergleich_verteilung(wuerfe, anzahl))
    assert ergebnis == erwartet, f"Nach random.seed({startzahl}) ergibt verteilung({wuerfe}, {anzahl}) {ergebnis!r}, erwartet war {erwartet}."

# haeufigste im Beispiel: Gleichstand, die kleinere Summe gewinnt
ergebnis = wert_von(lambda: haeufigste({2: 1, 3: 4, 4: 4}))
assert ergebnis == 3, (
    f"haeufigste({{2: 1, 3: 4, 4: 4}}) ergibt {ergebnis!r}, erwartet war 3.\n"
    "Tipp: Gesucht ist der Schlüssel mit dem größten Wert, nicht der größte Wert selbst."
)

# haeufigste ohne Gleichstand
ergebnis = wert_von(lambda: haeufigste({1: 3, 2: 0, 3: 1, 4: 7, 5: 2, 6: 7}))
assert ergebnis == 4, f"haeufigste({{1: 3, 2: 0, 3: 1, 4: 7, 5: 2, 6: 7}}) ergibt {ergebnis!r}, erwartet war 4."

# haeufigste: die häufigste Summe steht ganz am Anfang oder ganz am Ende
ergebnis = wert_von(lambda: [haeufigste({2: 9, 3: 1, 4: 5}), haeufigste({3: 0, 4: 2, 5: 8})])
assert ergebnis == [2, 5], f"haeufigste({{2: 9, 3: 1, 4: 5}}) und haeufigste({{3: 0, 4: 2, 5: 8}}) ergeben {ergebnis!r}, erwartet war [2, 5]."

# haeufigste ohne Würfe: alle 0, also die kleinste Summe
ergebnis = wert_von(lambda: haeufigste({summe: 0 for summe in range(3, 19)}))
assert ergebnis == 3, f"haeufigste für 3 Würfel ohne einen Wurf ergibt {ergebnis!r}, erwartet war 3 (Gleichstand bei 0)."

# Die Simulation zeigt einen fairen Würfel: bei 18 000 Würfen mit zwei Würfeln fällt die 7 am häufigsten
ergebnis = mit_startzahl(77, lambda: verteilung(18000, 2))
assert isinstance(ergebnis, dict) and 2700 <= ergebnis.get(7, 0) <= 3300 and ergebnis.get(2, 0) <= 650, (
    f"verteilung(18000, 2) ergibt {ergebnis!r}; erwartet war die 7 etwa 3000-mal und die 2 etwa 500-mal."
)
# haeufigste der Simulation ist die 7
assert wert_von(lambda: haeufigste(ergebnis)) == 7, f"haeufigste(verteilung(18000, 2)) ergibt {wert_von(lambda: haeufigste(ergebnis))!r}, erwartet war 7."

# Die Ausgabe des Programms
erwartet = "9\n{1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 2}\n3"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Startzahlen, Würfe und Anzahlen
zufall = Zufall(2052)
for _ in range(150):
    startzahl = zufall.randint(0, 10**6)
    wuerfe = zufall.randint(0, 40)
    anzahl = zufall.randint(1, 10)
    ergebnis = mit_startzahl(startzahl, lambda: verteilung(wuerfe, anzahl))
    erwartet = mit_startzahl(startzahl, lambda: vergleich_verteilung(wuerfe, anzahl))
    assert ergebnis == erwartet, f"Nach random.seed({startzahl}) ergibt verteilung({wuerfe}, {anzahl}) {ergebnis!r}, erwartet war {erwartet}."
    ergebnis = wert_von(lambda: haeufigste(erwartet))
    assert ergebnis == vergleich_haeufigste(erwartet), f"haeufigste({erwartet}) ergibt {ergebnis!r}, erwartet war {vergleich_haeufigste(erwartet)}."

# Obere Grenze: 20 000 Würfe mit 10 Würfeln
ergebnis = mit_startzahl(20000, lambda: verteilung(20000, 10))
erwartet = mit_startzahl(20000, lambda: vergleich_verteilung(20000, 10))
assert ergebnis == erwartet, "Bei 20 000 Würfen mit 10 Würfeln stimmt verteilung nicht mit der Vergleichslösung überein."
# Obere Grenze: haeufigste bei 20 000 Würfen mit 10 Würfeln
assert wert_von(lambda: haeufigste(ergebnis)) == vergleich_haeufigste(erwartet), "Bei 20 000 Würfen mit 10 Würfeln stimmt haeufigste nicht."
