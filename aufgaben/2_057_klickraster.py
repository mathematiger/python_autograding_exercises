"""Aufgabe 2_057 – Klickraster                                   Stufe 2 ★★☆☆☆

Ein Team überarbeitet die Eingabemaske eines Bestellportals. Um zu
sehen, wohin die Leute klicken, legt es ein unsichtbares Raster über die
Seite und zählt für jedes Feld des Rasters die Klicks einer Woche. Das
Ergebnis ist eine Klickkarte (englisch Heatmap): eine Liste von Zeilen,
jede Zeile eine Liste mit der Klickzahl jedes Felds, Zeile 0 ganz oben,
Spalte 0 ganz links:

    raster = [
        [0, 3, 1, 0],    # Zeile 0: Kopfbereich
        [2, 9, 4, 0],    # Zeile 1: Formular
        [0, 1, 0, 5],    # Zeile 2: Fußbereich mit dem Knopf „Bestellen“
    ]

Für die Auswertung braucht das Team die Klicks je Zeile und je Spalte,
und für die Ansicht auf Tablets im Hochformat soll die Karte gekippt
werden: Aus jeder Spalte wird eine Zeile. Schreiben Sie drei Funktionen,
die je eine neue Liste zurückgeben und raster nicht verändern:

- `transponieren(raster)`: die gekippte Karte. Der Wert, der in raster
  in Zeile z und Spalte s steht, steht im Ergebnis in Zeile s und
  Spalte z. Aus 3 Zeilen mit je 4 Werten werden 4 Zeilen mit je 3 Werten.
- `zeilensummen(raster)`: die Summe jeder Zeile, von oben nach unten.
- `spaltensummen(raster)`: die Summe jeder Spalte, von links nach
  rechts. Benutzen Sie dafür die beiden Funktionen oben: Die Spalten von
  raster sind die Zeilen der gekippten Karte.

    transponieren(raster)   →  [[0, 2, 0], [3, 9, 1], [1, 4, 0], [0, 0, 5]]
    zeilensummen(raster)    →  [4, 15, 6]
    spaltensummen(raster)   →  [2, 13, 5, 5]

Grenzen: raster hat 1 bis 300 Zeilen, alle mit gleich vielen Werten, 1
bis 300 pro Zeile. Die Werte sind ganze Zahlen von 0 bis 10 000.

Hintergrund: Eine Liste von Listen, in der alle Zeilen gleich lang
sind, heißt Matrix. Wie man mit raster[z][s] auf einen Wert zugreift und
mit zwei Schleifen alle Werte durchläuft, kennen Sie aus Aufgabe 2_020.
Die Anzahl der Zeilen ist len(raster), die Anzahl der Spalten
len(raster[0]). Beim Transponieren baut man die neue Matrix Zeile für
Zeile auf; ihre Zeile s sammelt aus jeder alten Zeile den Wert an der
Stelle s, also gerade die alte Spalte s:

    tabelle = [[1, 2, 3], [4, 5, 6]]
    gekippt = []
    for s in range(len(tabelle[0])):      # eine neue Zeile je alter Spalte
        neue_zeile = []
        for z in range(len(tabelle)):
            neue_zeile.append(tabelle[z][s])
        gekippt.append(neue_zeile)
    gekippt   →  [[1, 4], [2, 5], [3, 6]]

Die äußere Schleife läuft hier über die Spalten, nicht über die Zeilen.
Für die Summe einer Zeile genügt sum(zeile) (Aufgabe 1_031). Wer einmal
transponieren kann, muss das Durchlaufen der Spalten nie wieder neu
schreiben: Jede Rechnung für Zeilen wird auf der gekippten Matrix zu
einer Rechnung für Spalten.
"""


def transponieren(raster):
    """Gibt die gekippte Matrix zurück: Zeilen werden zu Spalten."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zeilensummen(raster):
    """Gibt die Summe jeder Zeile als Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def spaltensummen(raster):
    """Gibt die Summe jeder Spalte als Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


raster = [
    [0, 3, 1, 0],
    [2, 9, 4, 0],
    [0, 1, 0, 5],
]
print(zeilensummen(raster))
print(spaltensummen(raster))
