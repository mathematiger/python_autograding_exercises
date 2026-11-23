# Automatisch erzeugt aus lehrkraft/muster/3_061_hilfeseite.py - nicht von Hand ändern.
# vorlage-hash: 93488b19b1286108
# text-hash: 1a58adab3407dc6c
# thema: algorithmen
# inhalt: Sliding Window

KLICKS = [12, 40, 7, 3, 55, 21, 9, 30]


def wert_von(funktion, klicks, k):
    """Ruft funktion mit einer Kopie von klicks auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(list(klicks), k)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_summen(klicks, k):
    """Vergleichslösung: rechnet jede Fenstersumme neu aus (langsam, aber offensichtlich richtig)."""
    return [sum(klicks[start:start + k]) for start in range(len(klicks) - k + 1)]


def vergleich_beste(klicks, k):
    """Vergleichslösung für beste_position über max mit einem Schlüssel."""
    summen = vergleich_summen(klicks, k)
    if not summen:
        return None
    beste = max(range(len(summen)), key=lambda start: (summen[start], -start))
    return (beste, summen[beste])


def meldung(funktion, klicks, k, erwartet, hinweis=""):
    """Prüft funktion(klicks, k) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, klicks, k)
    gezeigt = klicks if len(klicks) <= 12 else f"<{len(klicks)} Einträge>"
    erwartet_kurz = erwartet if len(repr(erwartet)) <= 200 else f"<{len(erwartet)} Summen>"
    ergebnis_kurz = repr(ergebnis) if len(repr(ergebnis)) <= 200 else repr(ergebnis)[:150] + " …"
    text = f"{funktion.__name__}({gezeigt}, {k}) ergibt {ergebnis_kurz}, erwartet war {erwartet_kurz}.{hinweis}"
    return ergebnis == erwartet, text


def zugriffe(funktion, klicks, k):
    """Ruft funktion mit einer Zaehlliste auf; liefert (Ergebnis, Lesezugriffe)."""
    liste = Zaehlliste(klicks)
    try:
        ergebnis = funktion(liste, k)
    except Exception as fehler:
        ergebnis = f"{type(fehler).__name__}: {fehler}"
    return ergebnis, liste.lesezugriffe


# fenstersummen: das Beispiel
stimmt, text = meldung(fenstersummen, KLICKS, 3, [59, 50, 65, 79, 85, 60])
assert stimmt, text

# fenstersummen: eine andere Breite (nicht fest hinschreiben!)
stimmt, text = meldung(fenstersummen, KLICKS, 2, [52, 47, 10, 58, 76, 30, 39])
assert stimmt, text

# fenstersummen: das letzte Fenster endet mit dem letzten Eintrag
stimmt, text = meldung(
    fenstersummen, [1, 2, 3, 4], 2, [3, 5, 7],
    "\nTipp: Es gibt len(klicks) - k + 1 Fenster; das letzte beginnt bei len(klicks) - k.",
)
assert stimmt, text

# fenstersummen: Breite 1 ergibt die Einträge selbst
stimmt, text = meldung(fenstersummen, [5, 0, 7], 1, [5, 0, 7])
assert stimmt, text

# fenstersummen: ein Fenster über die ganze Liste
stimmt, text = meldung(fenstersummen, KLICKS, 8, [177])
assert stimmt, text

# fenstersummen: Liste kürzer als das Fenster
stimmt, text = meldung(
    fenstersummen, KLICKS, 9, [],
    "\nTipp: Ist len(klicks) < k, gibt es keinen vollen Bildschirm; geben Sie [] zurück.",
)
assert stimmt, text

# fenstersummen: leere Liste
stimmt, text = meldung(fenstersummen, [], 1, [])
assert stimmt, text

# fenstersummen: Einträge ohne Klicks
stimmt, text = meldung(fenstersummen, [0, 0, 0, 0], 3, [0, 0])
assert stimmt, text

# beste_position: das Beispiel
stimmt, text = meldung(beste_position, KLICKS, 3, (4, 85), "\nTipp: Rufen Sie fenstersummen auf und suchen Sie darin das Maximum.")
assert stimmt, text

# beste_position: eine andere Breite
stimmt, text = meldung(beste_position, KLICKS, 2, (4, 76))
assert stimmt, text

# beste_position: der beste Bildschirm ist der erste
stimmt, text = meldung(beste_position, [90, 10, 1, 1, 2], 2, (0, 100))
assert stimmt, text

# beste_position: der beste Bildschirm ist der letzte
stimmt, text = meldung(beste_position, [1, 1, 2, 10, 90], 2, (3, 100))
assert stimmt, text

# beste_position: bei Gleichstand die kleinste Startposition
stimmt, text = meldung(
    beste_position, [5, 1, 5, 1, 5], 2, (0, 6),
    "\nTipp: Übernehmen Sie nur echt größere Summen (> statt >=).",
)
assert stimmt, text

# beste_position: alle Einträge ohne Klicks
stimmt, text = meldung(beste_position, [0, 0, 0], 2, (0, 0))
assert stimmt, text

# beste_position: kein Bildschirm ganz gefüllt
stimmt, text = meldung(beste_position, KLICKS, 9, None, "\nTipp: Ist fenstersummen leer, geben Sie None zurück.")
assert stimmt, text

# beste_position: leere Liste
stimmt, text = meldung(beste_position, [], 3, None)
assert stimmt, text

# Die Ausgabe des Programms
erwartet = "[59, 50, 65, 79, 85, 60]\n(4, 85)"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Hilfeseiten
zufall = Zufall(3061)
for _ in range(400):
    klicks = [zufall.randint(0, zufall.choice([3, 100, 1000000])) for _ in range(zufall.randint(0, 12))]
    k = zufall.randint(1, 14)
    stimmt, text = meldung(fenstersummen, klicks, k, vergleich_summen(klicks, k))
    assert stimmt, text
    stimmt, text = meldung(beste_position, klicks, k, vergleich_beste(klicks, k))
    assert stimmt, text

# Laufzeit: fenstersummen braucht O(n) Zugriffe, auch bei breitem Fenster
klicks = [zufall.randint(0, 1000) for _ in range(4000)]
ergebnis, anzahl = zugriffe(fenstersummen, klicks, 1000)
assert ergebnis == vergleich_summen(klicks, 1000) and anzahl <= 3 * len(klicks) + 10, (
    f"fenstersummen für 4000 Einträge und k = 1000 braucht {anzahl} Zugriffe auf klicks, erlaubt sind "
    f"{3 * len(klicks) + 10} (O(n)); jede Summe neu auszurechnen kostet etwa drei Millionen.\n"
    "Tipp: Rückt das Fenster weiter, addieren Sie den neuen Eintrag und ziehen den herausgefallenen ab."
)

# Laufzeit: beste_position braucht O(n) Zugriffe
ergebnis, anzahl = zugriffe(beste_position, klicks, 1000)
assert ergebnis == vergleich_beste(klicks, 1000) and anzahl <= 3 * len(klicks) + 10, (
    f"beste_position für 4000 Einträge und k = 1000 ergibt {ergebnis!r} (erwartet {vergleich_beste(klicks, 1000)}) "
    f"mit {anzahl} Zugriffen auf klicks; erlaubt sind {3 * len(klicks) + 10}."
)

# Obere Grenze: 100 000 Einträge, k = 50 000
klicks = [zufall.randint(0, 1000000) for _ in range(100000)]
ergebnis = wert_von(beste_position, klicks, 50000)
summe = sum(klicks[:50000])
beste = (0, summe)
for neu in range(50000, 100000):
    summe = summe + klicks[neu] - klicks[neu - 50000]
    if summe > beste[1]:
        beste = (neu - 49999, summe)
assert ergebnis == beste, f"beste_position(<100000 Einträge>, 50000) ergibt {ergebnis!r}, erwartet war {beste}."

# Obere Grenze: k = 100 000 bei 100 000 Einträgen
stimmt, text = meldung(fenstersummen, klicks, 100000, [sum(klicks)])
assert stimmt, text
