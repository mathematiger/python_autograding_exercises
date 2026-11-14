"""Aufgabe 5_021 – Zeitraster                                   Stufe 5 ★★★★★

Ein Temperatursensor in einer Kühlhalle sendet ab einem Startzeitpunkt in
festem Abstand einen Messwert, zum Beispiel alle 60 Sekunden. Die
Auswertungssoftware braucht oft die Liste der Zeitpunkte, zu denen ein
Wert kommen müsste, um Lücken zu finden. Bei einem Jahr im Sekundentakt
wären das über 31 Millionen Zahlen; die will niemand als Liste im Speicher
halten. Die Zeitpunkte lassen sich aber jederzeit ausrechnen: Der i-te ist
start + i · abstand.

Vervollständigen Sie die Klasse `Zeitraster(start, anzahl, abstand)`, die
sich wie eine unveränderliche Liste dieser Zeitpunkte verhält, ohne sie zu
speichern. Sie erbt von collections.abc.Sequence.

- `__init__` speichert start, anzahl und abstand unter diesen Namen. Ist
  anzahl negativ oder abstand 0, löst es einen ValueError aus.
- `__len__` liefert die Anzahl der Zeitpunkte.
- `__getitem__(index)` mit einer ganzen Zahl liefert den Zeitpunkt an
  dieser Stelle; negative Indizes zählen wie bei Listen von hinten. Liegt
  der Index außerhalb, löst es einen IndexError aus, ist er keine ganze
  Zahl (und kein Slice), einen TypeError.
- `__getitem__(slice)` liefert ein neues Zeitraster mit genau den
  Zeitpunkten, die list(raster)[slice] hätte, auch bei negativen oder
  fehlenden Grenzen und jeder Schrittweite außer 0.
- `__contains__(zeit)` liefert True, wenn zeit einer der Zeitpunkte ist,
  und zwar ausgerechnet, nicht durch Ausprobieren aller Stellen. Für Werte,
  die keine ganze Zahl (int) sind, liefert es False.

    raster = Zeitraster(1000, 5, 60)
    list(raster)          →  [1000, 1060, 1120, 1180, 1240]
    raster[-1]            →  1240
    raster[1:4]           →  Zeitraster(start=1060, anzahl=3, abstand=60)
    raster[::-2]          →  Zeitraster(start=1240, anzahl=3, abstand=-120)
    1120 in raster        →  True
    1121 in raster        →  False
    raster.index(1180)    →  3        (von Sequence geerbt)

Grenzen: start, anzahl und abstand sind ganze Zahlen mit
-10**12 ≤ start ≤ 10**12, 0 ≤ anzahl ≤ 10**12 und 1 ≤ |abstand| ≤ 10**6;
der Abstand darf negativ sein (dann laufen die Zeitpunkte rückwärts).
Indizes und Slice-Grenzen sind beliebige ganze Zahlen oder None. Ein
Zugriff mit einer Zahl, ein Slice und in sollen jeweils O(1) Schritte
brauchen, unabhängig von anzahl.

Hintergrund: Python fragt bei Operatoren nicht nach dem Typ, sondern nach
Methoden. len(x) ruft x.__len__() auf, x[3] ruft x.__getitem__(3) auf, und
3 in x ruft x.__contains__(3) auf. Wer diese Methoden schreibt, bekommt ein
Objekt, das sich wie eine Liste anfühlt.

Auch x[1:4:2] landet in __getitem__, nur bekommt die Methode dann ein
slice-Objekt mit den Attributen start, stop und step (jeweils None, wenn
weggelassen). Die Regeln für negative und zu große Grenzen muss man nicht
nachbauen: slice.indices(laenge) rechnet sie für eine Folge dieser Länge
in drei passende ganze Zahlen um, und range zählt ohne Liste, wie viele
Stellen das sind:

    teil = slice(None, None, -2)
    teil.indices(5)                       →  (4, -1, -2)
    len(range(*teil.indices(5)))          →  3      (Stellen 4, 2, 0)

collections.abc.Sequence ist eine abstrakte Basisklasse (Aufgabe 4_011): Sie
verlangt nur __getitem__ und __len__ und liefert daraus fertig __iter__,
__reversed__, index, count und __contains__ dazu.

    from collections.abc import Sequence

    class Quadrate(Sequence):
        def __init__(self, n):
            self.n = n
        def __len__(self):
            return self.n
        def __getitem__(self, i):
            if not 0 <= i < self.n:
                raise IndexError(i)
            return i * i

    list(Quadrate(4))       →  [0, 1, 4, 9]
    9 in Quadrate(4)        →  True

Das geerbte __iter__ ruft __getitem__(0), __getitem__(1), … auf, bis ein
IndexError kommt; ohne IndexError läuft for endlos. Das geerbte
__contains__ geht genauso alle Elemente durch, das ist O(n). Weil man hier
ausrechnen kann, ob eine Zahl dazugehört, überschreibt man es mit einer
schnellen eigenen Version, so wie range es auch tut.
"""

from collections.abc import Sequence


class Zeitraster(Sequence):
    """Die Zeitpunkte start, start + abstand, … (anzahl Stück), ohne sie zu speichern."""

    def __init__(self, start, anzahl, abstand):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __getitem__(self, index):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __contains__(self, zeit):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __repr__(self):
        return f"Zeitraster(start={self.start}, anzahl={self.anzahl}, abstand={self.abstand})"


raster = Zeitraster(1000, 5, 60)
print(list(raster), raster[1:4], 1120 in raster)
