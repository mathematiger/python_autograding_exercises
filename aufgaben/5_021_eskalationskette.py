"""Aufgabe 5_021 – Eskalationskette                              Stufe 5 ★★★★★

Im IT-Support eines Dienstleisters wandert ein Ticket, das auf einer Stufe
nicht gelöst wird, eine Stufe weiter: vom Service-Desk zum Fachteam, von
dort zum Hersteller und so fort. Die Reihenfolge dieser Stufen heißt
Eskalationskette, und sie ist für jeden Kundenvertrag anders. Das
Ticketsystem soll sie wie eine Liste behandeln können (Index, Slices,
len, in, for, index, reversed), sie aber nicht verändern dürfen.

Vervollständigen Sie die Klasse `Eskalationskette`, eine Unterklasse von
collections.abc.Sequence:

- `__init__(self, stufen)` übernimmt die Namen der Stufen aus einem
  beliebigen Iterable, in dieser Reihenfolge. Spätere Änderungen an dem
  übergebenen Objekt wirken sich nicht auf die Kette aus.
- `__len__(self)` liefert die Zahl der Stufen.
- `__getitem__(self, index)` liefert bei einer ganzen Zahl den Namen der
  Stufe (negative Indizes zählen von hinten, außerhalb ein IndexError) und
  bei einem Slice eine neue Eskalationskette mit den ausgewählten Stufen.
- `__contains__(self, name)` prüft, ob es eine Stufe mit diesem Namen gibt,
  und zwar in O(1), ohne die Stufen nacheinander anzusehen.
- `__eq__(self, other)`: Zwei Ketten sind gleich, wenn sie dieselben Stufen
  in derselben Reihenfolge haben. Mit etwas anderem als einer
  Eskalationskette gibt __eq__ NotImplemented zurück.
- `__repr__(self)` liefert z. B. "Eskalationskette(['Service-Desk', 'Fachteam'])".
- `naechste(self, name)` gibt den Namen der Stufe nach name zurück, None
  nach der letzten Stufe und einen ValueError, wenn es name nicht gibt.

index, count, __iter__ und __reversed__ schreiben Sie nicht selbst, die
liefert Sequence.

    kette = Eskalationskette(["Service-Desk", "Fachteam", "Hersteller"])
    len(kette)                    →  3
    kette[-1]                     →  "Hersteller"
    kette[1:]                     →  Eskalationskette(['Fachteam', 'Hersteller'])
    "Fachteam" in kette           →  True
    kette.index("Hersteller")     →  2
    list(reversed(kette))         →  ['Hersteller', 'Fachteam', 'Service-Desk']
    kette.naechste("Fachteam")    →  "Hersteller"
    kette.naechste("Hersteller")  →  None

Grenzen: Eine Kette hat 0 bis 10**5 Stufen. Die Namen sind nicht leere
Texte und innerhalb einer Kette verschieden. Indizes sind ganze Zahlen
beliebiger Größe, Slices haben beliebigen Anfang, Ende und Schritt
(Schritt nicht 0). Bei in und naechste kann name auch ein Text sein, den es
in der Kette nicht gibt.

Hintergrund: Was eine Klasse zur Sequenz macht, ist ein Protokoll, keine
Abstammung: Python braucht nur __len__ und __getitem__ mit ganzen Zahlen ab
0. Daraus lässt sich alles andere ableiten, und genau das tut die
abstrakte Basisklasse collections.abc.Sequence (abc.ABC, Aufgabe 4_011).
Wer von ihr erbt, muss __getitem__ und __len__ schreiben und bekommt dafür
als Mixin-Methoden geschenkt:

    __contains__   x in s        sieht s[0], s[1], … der Reihe nach an
    __iter__       for x in s    ruft s[0], s[1], … bis zum IndexError
    __reversed__   reversed(s)   ruft s[len(s) - 1], …, s[0]
    index, count                 laufen ebenfalls über s[i]

Alle diese Methoden rufen nur __getitem__ und __len__ auf. Darum muss
__getitem__ bei einem zu großen Index einen IndexError auslösen: Daran
erkennt __iter__, dass es vorbei ist.

Bei s[1:3] oder s[::-1] bekommt __getitem__ statt einer Zahl ein
slice-Objekt mit den Attributen start, stop und step. Am einfachsten gibt
man es an eine eingebaute Sequenz weiter, die schon alle Sonderfälle
kennt, und verpackt das Ergebnis wieder in die eigene Klasse:

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Eskalationskette(self._stufen[index])
        return self._stufen[index]

Die Mixin-Methoden sind korrekt, aber nicht unbedingt schnell: Das
geerbte __contains__ braucht O(n) Aufrufe von __getitem__. Wer mehr über
seine Daten weiß, überschreibt es; hier sind die Namen verschieden, also
kann eine Menge (set) die Frage in O(1) beantworten. Gespeichert werden
die Stufen am besten in einem Tupel: Das ist unveränderlich, und eine
Änderung der übergebenen Liste erreicht die Kette nicht.

Und __eq__ liefert Sequence nicht mit (zwei Sequenzen verschiedener Typen
gelten in Python nicht als gleich, [1] == (1,) ist False). NotImplemented
als Rückgabe sagt Python, dass es die andere Seite fragen oder auf
Identität ausweichen soll (Aufgabe 5_019).
"""

from collections.abc import Sequence


class Eskalationskette(Sequence):
    """Unveränderliche Folge von Eskalationsstufen eines Supportvertrags."""

    def __init__(self, stufen):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __getitem__(self, index):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __contains__(self, name):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __eq__(self, other):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __repr__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def naechste(self, name):
        """Gibt die Stufe nach name zurück, None nach der letzten; ValueError, wenn es name nicht gibt."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kette = Eskalationskette(["Service-Desk", "Fachteam", "Hersteller"])
print(kette[1:])
print(kette.naechste("Fachteam"), kette.naechste("Hersteller"))
