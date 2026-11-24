# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_057_klickraster.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_057_klickraster

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
    gekippt = []
    for s in range(len(raster[0])):
        neue_zeile = []
        for z in range(len(raster)):
            neue_zeile.append(raster[z][s])
        gekippt.append(neue_zeile)
    return gekippt


def zeilensummen(raster):
    """Gibt die Summe jeder Zeile als Liste zurück."""
    summen = []
    for zeile in raster:
        summen.append(sum(zeile))
    return summen


def spaltensummen(raster):
    """Gibt die Summe jeder Spalte als Liste zurück."""
    return zeilensummen(transponieren(raster))


raster = [
    [0, 3, 1, 0],
    [2, 9, 4, 0],
    [0, 1, 0, 5],
]
print(zeilensummen(raster))
print(spaltensummen(raster))


# Idee: transponieren baut für jede Spalte s von raster (range(len(raster[0]))) eine neue Zeile auf, in
# die aus jeder alten Zeile z der Wert raster[z][s] kommt. zeilensummen hängt sum(zeile) für jede Zeile
# an. spaltensummen ist dann nur noch zeilensummen(transponieren(raster)), weil die Spalten von raster die
# Zeilen der gekippten Matrix sind.
# Anderer Weg (Ausblick): list(map(list, zip(*raster))) transponiert in einer Zeile: zip(*raster)
# übergibt die Zeilen einzeln an zip und liefert die Spalten als Tupel (zip kennen Sie aus Aufgabe 2_022,
# das Entpacken mit * aus Aufgabe 4_018, map aus Aufgabe 3_026). Spaltensummen gehen auch
# ohne Kippen mit einer Liste summen = [0] * len(raster[0]), zu der man jede Zeile Stelle für Stelle addiert.
# Typische Fehler: die Schleifen vertauschen (dann kommt bei nicht quadratischen Matrizen ein IndexError
# oder die alte Matrix zurück), range(len(raster)) für die Spalten nehmen, in die alte Matrix
# hineinschreiben, statt eine neue aufzubauen.
