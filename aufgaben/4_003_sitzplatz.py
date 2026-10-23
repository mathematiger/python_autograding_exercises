"""Aufgabe 4_003 – Kinoplätze                                    Stufe 4 ★★★★☆

Ein Kino verwaltet seine Reservierungen am Computer. Jeder Sitzplatz ist ein
Objekt der Klasse `Sitzplatz` mit Saal, Reihe und Platznummer. Die gebuchten
Plätze stehen in einer Menge, die Preise für besondere Plätze in einem
Dictionary. Das Problem: Ein neu erzeugtes Objekt Sitzplatz(1, "F", 7) wird
nicht als gebucht erkannt, obwohl derselbe Platz längst in der Menge steht.
So werden Plätze doppelt verkauft. Vervollständigen Sie die Klasse:

- `__eq__(self, other)` liefert True, wenn other ebenfalls ein Sitzplatz mit
  gleichem Saal, gleicher Reihe und gleicher Nummer ist, sonst False. Ist other
  gar kein Sitzplatz, gibt die Methode NotImplemented zurück.
- `__hash__(self)` liefert einen Hashwert, der für gleiche Sitzplätze gleich
  ist.

    gebucht = {Sitzplatz(1, "F", 7), Sitzplatz(1, "F", 8)}
    Sitzplatz(1, "F", 7) in gebucht     →  True
    Sitzplatz(2, "F", 7) in gebucht     →  False
    Sitzplatz(1, "F", 7) == (1, "F", 7) →  False

Hintergrund: Ohne eigene Methoden vergleicht == zwei Objekte nach ihrer
Identität: Zwei getrennt erzeugte Objekte sind verschieden, auch wenn alle
Attribute übereinstimmen. Mit __eq__ legt man fest, wann zwei Objekte als
gleich gelten. a == b ruft a.__eq__(b) auf; != ergibt Python automatisch als
Gegenteil. Weiß __eq__ mit dem anderen Objekt nichts anzufangen, gibt es den
besonderen Wert NotImplemented zurück (nicht False und keine Ausnahme). Dann
fragt Python noch die andere Seite und nimmt, wenn auch die nicht zuständig
ist, False:

    def __eq__(self, other):
        if not isinstance(other, Bruch):
            return NotImplemented
        return (self.zaehler, self.nenner) == (other.zaehler, other.nenner)

Mengen und Dictionaries finden ihre Elemente nicht durch Vergleichen mit
allen Einträgen, sondern über einen Hashwert: hash(objekt) ruft
objekt.__hash__() auf und liefert eine ganze Zahl, aus der die Menge direkt
die Stelle berechnet, an der sie nachsehen muss. Erst dort vergleicht sie mit
==. Daraus folgt die wichtigste Regel: Gleiche Objekte müssen den gleichen
Hashwert haben. Sonst sucht die Menge an der falschen Stelle und findet den
Platz nicht. Am einfachsten bildet man den Hash aus einem Tupel genau der
Attribute, die auch __eq__ vergleicht:

    def __hash__(self):
        return hash((self.zaehler, self.nenner))

Vorsicht: Definiert eine Klasse __eq__, aber kein __hash__, setzt Python
__hash__ auf None. Die Objekte lassen sich dann nicht mehr in Mengen legen
(TypeError: unhashable type). Und ein Objekt, das in einer Menge steckt, darf
seine Attribute nicht mehr ändern, sonst passt sein Hashwert nicht mehr zu
der Stelle, an der es liegt.

Tipp: Verschiedene Plätze dürfen zufällig denselben Hashwert haben; das ist
erlaubt, macht Mengen aber langsam. Mit dem Tupel-Hash passiert das kaum.
"""


class Sitzplatz:
    """Ein Sitzplatz im Kino, bestimmt durch Saal, Reihe und Nummer."""

    def __init__(self, saal, reihe, nummer):
        self.saal = saal
        self.reihe = reihe
        self.nummer = nummer

    def __repr__(self):
        """Gibt einen Python-Ausdruck zurück, der diesen Sitzplatz erzeugt."""
        return f"Sitzplatz({self.saal!r}, {self.reihe!r}, {self.nummer!r})"

    def __eq__(self, other):
        """Gibt zurück, ob other derselbe Sitzplatz ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __hash__(self):
        """Gibt einen Hashwert zurück, der für gleiche Sitzplätze gleich ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


gebucht = {Sitzplatz(1, "F", 7), Sitzplatz(1, "F", 8)}
print(Sitzplatz(1, "F", 7) in gebucht)
print(Sitzplatz(2, "F", 7) in gebucht)
