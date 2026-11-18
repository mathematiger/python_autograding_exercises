"""Aufgabe 5_021 – Messreihe                                     Stufe 5 ★★★★★

Ein Temperatursensor in einem Kühlhaus schickt in festem Takt Messwerte an
einen kleinen Rechner (ein IoT-Gateway). Jede Messreihe hat einen
Startzeitpunkt (Sekunden seit Mitternacht), einen Takt in Sekunden und die
Liste der Werte; Wert Nummer i wurde also zum Zeitpunkt start + i · takt
gemessen. Die Auswertung soll mit einer Messreihe arbeiten können wie mit
einer Liste: len(reihe), reihe[-1], for wert in reihe, wert in reihe,
reihe.index(wert), reversed(reihe). Ein Ausschnitt wie reihe[10:20] oder
reihe[::2] soll aber keine nackte Liste liefern, sondern wieder eine
Messreihe mit passendem Startzeitpunkt und Takt, sonst gehen die Zeitpunkte
verloren. Vervollständigen Sie die Klasse `Messreihe`, die von
collections.abc.Sequence erbt:

- `__len__(self)` liefert die Anzahl der Werte.
- `__getitem__(self, index)`: Bei einer ganzen Zahl der Wert an dieser
  Stelle, auch mit negativem Index wie bei Listen; außerhalb ein IndexError.
  Bei einem Slice eine neue Messreihe mit den ausgewählten Werten, deren
  Startzeitpunkt der Zeitpunkt des ersten ausgewählten Werts ist und deren
  Takt takt · Schrittweite ist. Bei jedem anderen Typ ein TypeError.
- `zeitpunkt(self, i)` ist vorgegeben.

    reihe = Messreihe(start=3600, takt=60, werte=[4.1, 4.3, 4.0, 3.8, 4.2])
    len(reihe)              →  5
    reihe[-1]               →  4.2
    teil = reihe[1:5:2]
    teil.start, teil.takt, list(teil)   →  3660, 120, [4.3, 3.8]
    3.8 in reihe            →  True
    reihe.index(4.0)        →  2
    list(reversed(reihe))   →  [4.2, 3.8, 4.0, 4.3, 4.1]

Grenzen: 0 ≤ len(werte) ≤ 100 000, start und takt sind ganze Zahlen mit
0 ≤ start ≤ 10**6 und 1 ≤ takt ≤ 3600. Ein Index ist eine ganze Zahl (nicht
bool) mit -10**6 ≤ index ≤ 10**6, oder ein Slice mit beliebigen Grenzen
(auch negativ, auch außerhalb, auch None) und einer Schrittweite ungleich 0;
bei negativer Schrittweite ist der neue Takt negativ. Die übergebene Liste
werte darf sich später ändern, ohne dass sich die Messreihe ändert. Ein
einzelner Zugriff reihe[i] soll O(1) Schritte brauchen.

Hintergrund: Python kennt für Container keine festen Klassen, sondern
Protokolle: Wer __len__ und __getitem__ hat, kann mit len() und [] benutzt
werden. Der Ausdruck reihe[1:5:2] ruft reihe.__getitem__(slice(1, 5, 2))
auf; ein slice-Objekt hat die Attribute start, stop und step (jeweils
vielleicht None). Die Methode slice.indices(laenge) rechnet sie für eine
bestimmte Länge in drei ganze Zahlen um, wie Listen es tun, mit allen
Sonderfällen für None, negative Werte und Grenzen außerhalb:

    s = slice(None, None, -2)
    s.indices(5)                →  (4, -1, -2)
    list(range(*s.indices(5)))  →  [4, 2, 0]

range(*s.indices(n)) liefert also genau die ausgewählten Stellen, und
len(...) dieses range-Objekts ihre Anzahl. Negative ganze Zahlen als Index
behandelt man selbst: Für -len ≤ index < 0 ist die Stelle index + len.

Den Rest liefert das Modul collections.abc. Die abstrakte Basisklasse
Sequence verlangt nur __getitem__ und __len__ und baut daraus fertige
Methoden: __contains__ (für in), __iter__, __reversed__, index und count.
__contains__, __iter__, index und count rufen __getitem__ mit 0, 1, 2, …
auf, bis ein IndexError kommt (__reversed__ zählt mit len rückwärts);
darum ist der IndexError für Stellen außerhalb wichtig, sonst endet for
nie. Außerdem gilt isinstance(reihe, Sequence), was andere
Bibliotheken zur Erkennung nutzen:

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

    list(Quadrate(4)), 9 in Quadrate(4)   →  [0, 1, 4, 9], True

Ob ein Index eine ganze Zahl oder ein Slice ist, prüft man mit
isinstance(index, slice) und isinstance(index, int); bool ist eine
Unterklasse von int und muss mit isinstance(index, bool) eigens
ausgeschlossen werden.
"""

from collections.abc import Sequence


class Messreihe(Sequence):
    """Messwerte in festem Takt ab einem Startzeitpunkt, benutzbar wie eine Liste."""

    def __init__(self, start, takt, werte):
        self.start = start
        self.takt = takt
        self._werte = list(werte)

    def zeitpunkt(self, i):
        """Zeitpunkt in Sekunden, zu dem Wert Nummer i gemessen wurde."""
        return self.start + i * self.takt

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __getitem__(self, index):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __repr__(self):
        return f"Messreihe(start={self.start}, takt={self.takt}, werte={self._werte!r})"


reihe = Messreihe(start=3600, takt=60, werte=[4.1, 4.3, 4.0, 3.8, 4.2])
print(len(reihe), reihe[-1], reihe[1:5:2])
