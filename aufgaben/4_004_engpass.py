"""Aufgabe 4_004 – Engpass im Prozess                            Stufe 4 ★★★★☆

Eine Versandabteilung will ihren Ablauf beschleunigen. Jede Bestellung läuft
durch mehrere Prozessschritte (Erfassen, Prüfen, Verpacken …), und für jeden
Schritt wurde die mittlere Bearbeitungsdauer in Minuten gemessen. Der Schritt
mit der längsten Dauer ist der Engpass: Er bestimmt, wie viele Bestellungen
pro Tag durchkommen, also lohnt es sich, dort zuerst zu verbessern. Damit man
die Schritte mit sorted(...), min(...) und max(...) auswerten kann, sollen
Objekte der Klasse `Prozessschritt` vergleichbar werden. Vervollständigen Sie
die Klasse:

- Ein Schritt ist kleiner als ein anderer, wenn seine Dauer kürzer ist. Bei
  gleicher Dauer entscheidet der Name in alphabetischer Reihenfolge.
- `__eq__(self, other)` liefert True bei gleichem Namen und gleicher Dauer.
- `__lt__(self, other)` liefert True, wenn self kleiner als other ist.
- Beide geben NotImplemented zurück, wenn other kein Prozessschritt ist.
- Die übrigen Vergleiche <=, > und >= erzeugen Sie mit dem Dekorator
  functools.total_ordering, statt sie selbst zu schreiben.

    schritte = [Prozessschritt("Prüfen", 12), Prozessschritt("Erfassen", 5),
                Prozessschritt("Verpacken", 12), Prozessschritt("Versenden", 8)]
    sorted(schritte)  →  [Prozessschritt('Erfassen', 5), Prozessschritt('Versenden', 8),
                          Prozessschritt('Prüfen', 12), Prozessschritt('Verpacken', 12)]
    max(schritte)     →  Prozessschritt('Verpacken', 12)
    Prozessschritt("Erfassen", 5) < 5  →  TypeError

Hintergrund: sorted, min und max vergleichen die Elemente mit <. Für eigene
Klassen weiß Python nicht, was „kleiner“ heißen soll; ohne Hilfe gibt es
einen TypeError. Wie == die Methode __eq__ aufruft (Aufgabe 4_003), ruft a < b
die Methode a.__lt__(b) auf („less than“). Die anderen Vergleiche haben
eigene Methoden: __le__ für <=, __gt__ für > und __ge__ für >=. Alle vier
selbst zu schreiben ist mühsam und fehleranfällig. Der Klassen-Dekorator
total_ordering aus dem Modul functools ergänzt die fehlenden, wenn die Klasse
__eq__ und eine der vier definiert:

    import functools

    @functools.total_ordering
    class Version:
        def __init__(self, haupt, neben):
            self.haupt = haupt
            self.neben = neben

        def __eq__(self, other):
            if not isinstance(other, Version):
                return NotImplemented
            return (self.haupt, self.neben) == (other.haupt, other.neben)

        def __lt__(self, other):
            if not isinstance(other, Version):
                return NotImplemented
            return (self.haupt, self.neben) < (other.haupt, other.neben)

    Version(2, 1) >= Version(1, 9)  →  True   (von total_ordering erzeugt)

Der Trick mit den Tupeln: Python vergleicht Tupel elementweise von links. Ist
das erste Element verschieden, entscheidet es; sonst entscheidet das zweite.
So bekommt man eine Reihenfolge nach mehreren Kriterien geschenkt. Gibt __lt__
für fremde Typen NotImplemented zurück, fragt Python die andere Seite und
löst, wenn auch die nicht zuständig ist, einen TypeError aus. Das ist richtig
so: Ob ein Prozessschritt kleiner als 5 ist, lässt sich nicht sinnvoll sagen.
Wichtig ist, dass __eq__ und __lt__ zueinander passen: Zwei Objekte, die
gleich sind, dürfen nicht zugleich kleiner sein.

Tipp: Ein Dekorator steht mit @ davor in der Zeile direkt über class; in der
Vorlage ist das die Zeile mit pass über der Klasse. Die Zeile import
functools steht schon oben im Programm.
"""

import functools


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
class Prozessschritt:
    """Ein Schritt eines Ablaufs mit Name und mittlerer Dauer in Minuten."""

    def __init__(self, name, dauer):
        """Speichert Name und Dauer."""
        self.name = name
        self.dauer = dauer

    def __repr__(self):
        """Gibt einen Python-Ausdruck zurück, der diesen Schritt erzeugt."""
        return f"Prozessschritt({self.name!r}, {self.dauer!r})"

    def __eq__(self, other):
        """Gibt zurück, ob other derselbe Schritt mit derselben Dauer ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __lt__(self, other):
        """Gibt zurück, ob dieser Schritt kürzer ist (bei gleicher Dauer: Name früher im Alphabet)."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


schritte = [
    Prozessschritt("Prüfen", 12),
    Prozessschritt("Erfassen", 5),
    Prozessschritt("Verpacken", 12),
    Prozessschritt("Versenden", 8),
]
print(sorted(schritte))
print("Engpass:", max(schritte))
