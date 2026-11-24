# Automatisch erzeugt aus lehrkraft/muster/2_057_klickraster.py - nicht von Hand ändern.
# vorlage-hash: 4ac30f0de811de42
# text-hash: 1bc82eb6fc09e3b2
# thema: datenstrukturen
# inhalt: Matrix transponieren, Summen

import copy

RASTER = [[0, 3, 1, 0], [2, 9, 4, 0], [0, 1, 0, 5]]


def wert_von(funktion, raster):
    """Ruft funktion mit einer Kopie von raster auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(copy.deepcopy(raster))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_kippen(raster):
    """Vergleichslösung: liest jeden Wert über seine neue Position ab."""
    return [[raster[z][s] for z in range(len(raster))] for s in range(len(raster[0]))]


def meldung(funktion, raster, erwartet, hinweis=""):
    """Prüft funktion(raster) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, raster)
    gezeigt = raster if len(raster) * len(raster[0]) <= 30 else f"<{len(raster)} × {len(raster[0])} Werte>"
    text = f"{funktion.__name__}({gezeigt})\nergibt   {ergebnis!r}\nerwartet {erwartet}{hinweis}"
    return zeilen_als_listen(ergebnis) == erwartet, text


def zeilen_als_listen(ergebnis):
    """Macht aus Zeilen als Tupel Listen, damit erst der eigene Test die Form der Zeilen prüft."""
    if isinstance(ergebnis, list) and all(isinstance(zeile, tuple) for zeile in ergebnis) and ergebnis:
        return [list(zeile) for zeile in ergebnis]
    return ergebnis


def zufallsraster(zufall, zeilen, spalten):
    """Erzeugt eine Matrix mit zufälligen Klickzahlen."""
    return [[zufall.randint(0, 10000) for _ in range(spalten)] for _ in range(zeilen)]


# transponieren: das Beispiel
stimmt, text = meldung(
    transponieren, RASTER, [[0, 2, 0], [3, 9, 1], [1, 4, 0], [0, 0, 5]],
    "\nTipp: Die äußere Schleife läuft über die Spalten von raster, die innere über die Zeilen.",
)
assert stimmt, text

# transponieren: eine quadratische Matrix (nicht fest hinschreiben!)
stimmt, text = meldung(transponieren, [[1, 2], [3, 4]], [[1, 3], [2, 4]])
assert stimmt, text

# transponieren: 2 Zeilen mit je 3 Werten werden 3 Zeilen mit je 2 Werten
stimmt, text = meldung(
    transponieren, [[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]],
    "\nTipp: Das Ergebnis hat so viele Zeilen, wie raster Spalten hat: len(raster[0]).",
)
assert stimmt, text

# transponieren: eine einzige Zeile wird eine einzige Spalte
stimmt, text = meldung(transponieren, [[7, 8, 9]], [[7], [8], [9]])
assert stimmt, text

# transponieren: eine einzige Spalte wird eine einzige Zeile
stimmt, text = meldung(transponieren, [[7], [8], [9]], [[7, 8, 9]])
assert stimmt, text

# transponieren: ein einziger Wert
stimmt, text = meldung(transponieren, [[0]], [[0]])
assert stimmt, text

# transponieren: jede Zeile des Ergebnisses ist eine Liste
ergebnis = wert_von(transponieren, [[1, 2, 3], [4, 5, 6]])
assert ergebnis == [[1, 4], [2, 5], [3, 6]], (
    f"transponieren([[1, 2, 3], [4, 5, 6]]) ergibt {ergebnis!r}, erwartet war die Liste von Listen "
    "[[1, 4], [2, 5], [3, 6]].\nTipp: zip liefert die Zeilen als Tupel; list(...) macht aus jedem eine Liste."
)

# transponieren verändert raster nicht
raster = copy.deepcopy(RASTER)
try:
    transponieren(raster)
except Exception:
    pass
assert raster == RASTER, f"Nach transponieren(raster) ist raster {raster}; es sollte unverändert bleiben."

# zeilensummen: das Beispiel
stimmt, text = meldung(zeilensummen, RASTER, [4, 15, 6])
assert stimmt, text

# zeilensummen: andere Werte
stimmt, text = meldung(zeilensummen, [[1, 2, 3], [4, 5, 6]], [6, 15])
assert stimmt, text

# zeilensummen: eine einzige Spalte
stimmt, text = meldung(zeilensummen, [[7], [0], [9]], [7, 0, 9])
assert stimmt, text

# spaltensummen: das Beispiel
stimmt, text = meldung(
    spaltensummen, RASTER, [2, 13, 5, 5],
    "\nTipp: Die Spaltensummen von raster sind die Zeilensummen von transponieren(raster).",
)
assert stimmt, text

# spaltensummen: andere Werte
stimmt, text = meldung(spaltensummen, [[1, 2, 3], [4, 5, 6]], [5, 7, 9])
assert stimmt, text

# spaltensummen: eine einzige Zeile
stimmt, text = meldung(spaltensummen, [[7, 0, 9]], [7, 0, 9])
assert stimmt, text

# spaltensummen verändert raster nicht
raster = copy.deepcopy(RASTER)
try:
    spaltensummen(raster)
except Exception:
    pass
assert raster == RASTER, f"Nach spaltensummen(raster) ist raster {raster}; es sollte unverändert bleiben."

# spaltensummen benutzt transponieren
aufrufe = []
eigenes_transponieren = transponieren


def transponieren(raster):
    """Zählt die Aufrufe und reicht sie an die eigene Funktion weiter."""
    aufrufe.append(1)
    return eigenes_transponieren(raster)


try:
    spaltensummen(copy.deepcopy(RASTER))
except Exception:
    pass
transponieren = eigenes_transponieren
assert aufrufe, "spaltensummen ruft transponieren nicht auf. Benutzen Sie zeilensummen(transponieren(raster))."

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar("[4, 15, 6]\n[2, 13, 5, 5]"), (
    f"Erwartete Ausgabe:\n[4, 15, 6]\n[2, 13, 5, 5]\nIhr Programm:\n{AUSGABE}"
)

# Viele zufällige Klickkarten
zufall = Zufall(2057)
for _ in range(300):
    raster = zufallsraster(zufall, zufall.randint(1, 6), zufall.randint(1, 6))
    gekippt = vergleich_kippen(raster)
    stimmt, text = meldung(transponieren, raster, gekippt)
    assert stimmt, text
    stimmt, text = meldung(zeilensummen, raster, [sum(zeile) for zeile in raster])
    assert stimmt, text
    stimmt, text = meldung(spaltensummen, raster, [sum(zeile) for zeile in gekippt])
    assert stimmt, text

# Obere Grenze: 300 × 300 Felder
raster = zufallsraster(zufall, 300, 300)
gekippt = vergleich_kippen(raster)
assert zeilen_als_listen(wert_von(transponieren, raster)) == gekippt, "Bei 300 × 300 Feldern stimmt transponieren nicht."

# Obere Grenze: spaltensummen bei 300 × 300 Feldern
assert zeilen_als_listen(wert_von(spaltensummen, raster)) == [sum(zeile) for zeile in gekippt], (
    "Bei 300 × 300 Feldern stimmt spaltensummen nicht."
)
