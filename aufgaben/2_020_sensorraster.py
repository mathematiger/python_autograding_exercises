"""Aufgabe 2_020 – Sensorraster                                  Stufe 2 ★★☆☆☆

In einer Lagerhalle hängen mehrere Temperatursensoren, die ihre Werte
über das Netz an einen kleinen Rechner schicken. Der Rechner speichert
die Messungen als Tabelle: eine Liste von Zeilen, jede Zeile eine Liste
mit einem Wert pro Sensor. Zeile 0 ist die erste Messrunde, Spalte 0
der erste Sensor:

    messungen = [
        [21, 22, 35],    # Runde 0: Sensor 0, 1 und 2
        [21, 23, 41],    # Runde 1
        [20, 22, 38],    # Runde 2
    ]

Sensor 2 hängt offenbar neben einer Heizung. Schreiben Sie zwei
Funktionen:

- `werte_von(messungen, sensor)` gibt alle Werte des Sensors mit der
  Nummer sensor als Liste zurück, in der Reihenfolge der Runden.
- `ueberschreitungen(messungen, grenze)` gibt alle Stellen zurück, an
  denen ein Wert größer als grenze ist, als Liste von Tupeln
  (runde, sensor). Die Reihenfolge ist die beim Lesen der Tabelle: Runde
  0 von links nach rechts, dann Runde 1 und so weiter.

    werte_von(messungen, 2)            →  [35, 41, 38]
    werte_von(messungen, 0)            →  [21, 21, 20]
    ueberschreitungen(messungen, 36)   →  [(1, 2), (2, 2)]
    ueberschreitungen(messungen, 22)   →  [(0, 2), (1, 1), (1, 2), (2, 2)]

Grenzen: messungen hat 1 bis 1000 Zeilen, alle mit gleich vielen
Werten, 1 bis 100 pro Zeile. Die Werte und grenze sind ganze Zahlen von
-50 bis 150. 0 ≤ sensor < Anzahl der Werte pro Zeile.

Hintergrund: Die Elemente einer Liste können selbst Listen sein. Mit
einem Index bekommt man eine ganze Zeile, mit einem zweiten Index daraus
einen Wert:

    messungen[1]       →  [21, 23, 41]
    messungen[1][2]    →  41
    len(messungen)     →  3           Anzahl der Zeilen
    len(messungen[0])  →  3           Anzahl der Werte pro Zeile

Eine Spalte gibt es nicht als eigenes Objekt; man sammelt sie, indem man
aus jeder Zeile denselben Index nimmt. Um alle Werte mit ihrer Position
zu durchlaufen, schachtelt man zwei Schleifen: Die äußere geht über die
Zeilennummern, die innere über die Spaltennummern.
"""


def werte_von(messungen, sensor):
    """Gibt die Werte des Sensors sensor aus allen Runden als Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ueberschreitungen(messungen, grenze):
    """Gibt alle Stellen (runde, sensor) mit einem Wert über grenze in Lesereihenfolge zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


messungen = [
    [21, 22, 35],
    [21, 23, 41],
    [20, 22, 38],
]
print(werte_von(messungen, 2))
print(ueberschreitungen(messungen, 36))
