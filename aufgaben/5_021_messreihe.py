"""Aufgabe 5_021 – Messreihe als Sequenz                         Stufe 5 ★★★★★

Ein Temperatursensor in einem Kühlhaus schickt in festem Takt Messwerte an
ein Gateway, zum Beispiel alle 60 Sekunden. Statt zu jedem Wert eine
Uhrzeit zu speichern, merkt sich die Klasse `Messreihe` nur die Werte, den
Zeitpunkt der ersten Messung (start, in Sekunden seit Mitternacht) und den
Abstand zwischen zwei Messungen (takt). Die Messreihe soll sich wie eine
unveränderliche Liste benutzen lassen: Indizes, Slices, len, in, for,
index, count und reversed. Ein Slice soll wieder eine Messreihe sein, und
zwar mit passender Zeitachse. Vervollständigen Sie:

- `__init__(self, werte, start=0, takt=1)` speichert eine Kopie der Werte
  als Liste sowie start und takt.
- `__len__(self)` liefert die Anzahl der Werte.
- `__getitem__(self, index)`: Bei einer ganzen Zahl den Wert an dieser
  Stelle, auch mit negativem Index; außerhalb IndexError. Bei einem Slice
  eine neue Messreihe mit den ausgewählten Werten. Ihr start ist der
  Zeitpunkt des ersten ausgewählten Index, ihr takt ist takt mal die
  Schrittweite des Slices. Bei einem anderen Typ (Text, Kommazahl) einen
  TypeError.
- `__contains__(self, wert)` liefert, ob wert unter den Werten ist, und
  soll dafür nicht die ganze Liste durchsuchen (O(1) im Mittel).

Die Klasse erbt von collections.abc.Sequence; __iter__, index, count und
__reversed__ bekommt sie dadurch geschenkt.

    reihe = Messreihe([4.5, 4.8, 5.1, 6.0, 5.4], start=600, takt=60)
    len(reihe)          →  5
    reihe[1], reihe[-1] →  4.8, 5.4
    teil = reihe[1:4]   →  Messreihe([4.8, 5.1, 6.0], start=660, takt=60)
    reihe[::2]          →  Messreihe([4.5, 5.1, 5.4], start=600, takt=120)
    reihe[::-1]         →  Messreihe([5.4, 6.0, 5.1, 4.8, 4.5], start=840, takt=-60)
    6.0 in reihe        →  True
    reihe.index(5.1)    →  2
    reihe[7]            →  IndexError
    reihe["1"]          →  TypeError

Grenzen: werte ist eine Liste oder ein anderes Iterable mit 0 bis 100 000
ganzen Zahlen oder Kommazahlen (endlich, kein nan). start und takt sind
ganze Zahlen mit 0 ≤ start ≤ 86 400 und 1 ≤ takt ≤ 3600; bei Slices
entstehen auch negative takt und Zeitpunkte außerhalb davon. Slices dürfen
beliebige Grenzen und eine Schrittweite ungleich 0 haben, auch negative.
Bei einem leeren Ergebnis ist start beliebig, takt wie beschrieben. True
und False kommen als Index nicht vor. __contains__ darf beim Erzeugen O(n)
Vorarbeit leisten.

Hintergrund: Die eckigen Klammern sind in Python ein Protokoll. reihe[2]
ruft reihe.__getitem__(2) auf, reihe[1:4:2] ruft reihe.__getitem__ mit
einem slice-Objekt auf, das die drei Angaben als start, stop und step
enthält (fehlende als None). Ein eigener Typ muss deshalb unterscheiden,
was er bekommen hat:

    def __getitem__(self, index):
        if isinstance(index, slice):
            ...
        if isinstance(index, int):
            ...
        raise TypeError(...)

Die mühsame Rechnung mit negativen und zu großen Grenzen nimmt einem
range ab: range(len(self))[index] liefert für ein slice-Objekt wieder ein
range mit genau den ausgewählten Indizes, bereits normalisiert:

    range(5)[1:100]  →  range(1, 5)
    range(5)[::-1]   →  range(4, -1, -1)      (Indizes 4, 3, 2, 1, 0)
    r = range(5)[::2];  r.start, r.step  →  0, 2

Ebenso wirft range(len(self))[index] für eine ganze Zahl außerhalb einen
IndexError und rechnet negative Indizes um. Die Liste selbst kann ein
slice-Objekt ebenfalls direkt verarbeiten: self._werte[index].

collections.abc.Sequence ist eine abstrakte Basisklasse (Aufgabe 4_011).
Wer von ihr erbt, muss __getitem__ und __len__ schreiben und bekommt dafür
fertige Methoden: __iter__ ruft __getitem__(0), (1), … auf, bis ein
IndexError kommt; __contains__ geht diese Werte durch; dazu index, count und
__reversed__. Eine eigene Methode überschreibt die geerbte. Hier lohnt das
für __contains__: Die geerbte Fassung braucht O(n) Schritte, mit einer
Menge (set) der Werte, die man einmal im __init__ anlegt, ist es O(1). Das
geht, weil die Messreihe unveränderlich ist. Bei einer veränderlichen
Sequenz müsste man die Menge bei jeder Änderung nachführen.

isinstance(reihe, Sequence) ist durch das Erben True, ebenso wie für
list, tuple, str und range. Funktionen, die „irgendeine Sequenz“
erwarten, können so prüfen, ob sie Indizes und len benutzen dürfen.
"""

from collections.abc import Sequence


class Messreihe(Sequence):
    """Unveränderliche Messreihe mit gleichmäßigem Takt; Slices behalten die Zeitachse."""

    def __init__(self, werte, start=0, takt=1):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __getitem__(self, index):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __contains__(self, wert):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def zeitpunkt(self, index):
        """Zeitpunkt der Messung an der Stelle index in Sekunden."""
        return self.start + range(len(self))[index] * self.takt

    def __repr__(self):
        return f"Messreihe({list(self)!r}, start={self.start!r}, takt={self.takt!r})"


reihe = Messreihe([4.5, 4.8, 5.1, 6.0, 5.4], start=600, takt=60)
print(reihe[1:4])
print(6.0 in reihe, reihe.index(5.1))
