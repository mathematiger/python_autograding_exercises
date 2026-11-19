"""Aufgabe 4_033 – Bandrotation                                  Stufe 4 ★★★★☆

Ein Rechenzentrum sichert jede Nacht auf Bandkassetten. Die Bänder
werden reihum benutzt: am ersten Tag das erste Band, am zweiten das
zweite und so weiter; nach dem letzten Band ist wieder das erste dran,
dessen alte Sicherung dann überschrieben wird. Ein Rotationsplan legt
fest, welche Bänder es gibt und für wie viele Tage geplant wird.

Der Plan wird an mehreren Stellen gleichzeitig durchlaufen: Das
Wochenblatt für die Operatoren geht ihn von vorn bis hinten durch, eine
Prüfung vergleicht ihn mit sich selbst um einen Tag versetzt, und ein
Bericht durchläuft ihn danach noch einmal. Darum darf der Plan kein
Iterator sein, der nach einem Durchlauf leer ist, sondern ein Iterable:
Jeder Durchlauf bekommt einen eigenen, frischen Iterator.

Vervollständigen Sie die beiden Klassen:

- `Rotationsplan(baender, tage)` merkt sich die Liste der Bänder und die
  Zahl der Tage. `__iter__(self)` gibt bei jedem Aufruf einen neuen
  `PlanIterator` für diesen Plan zurück.
- `PlanIterator(plan)` merkt sich den Plan und den nächsten Tag (am
  Anfang Tag 1). `__iter__(self)` gibt sich selbst zurück. `__next__(self)`
  gibt das Paar (tag, band) des nächsten Tags zurück und rückt einen Tag
  weiter; nach dem letzten Tag löst es StopIteration aus, auch bei jedem
  weiteren Aufruf.

    plan = Rotationsplan(["Band A", "Band B", "Band C"], 4)
    list(plan)  →  [(1, "Band A"), (2, "Band B"), (3, "Band C"), (4, "Band A")]
    list(plan)  →  dasselbe noch einmal
    iterator = iter(plan)
    next(iterator)   →  (1, "Band A")
    next(iterator)   →  (2, "Band B")
    next(iter(plan)) →  (1, "Band A")     (ein neuer Iterator beginnt vorn)

Schreiben Sie __next__ von Hand, ohne yield und ohne vorab eine Liste
aller Tage anzulegen: Jedes Paar wird erst berechnet, wenn es abgeholt
wird.

Grenzen: 1 ≤ len(baender) ≤ 100, die Bänder sind Texte. tage ist eine
ganze Zahl mit 0 ≤ tage ≤ 100 000. Beliebig viele Iteratoren desselben
Plans können gleichzeitig unterwegs sein.

Hintergrund: In Aufgabe 4_032 war die Klasse selbst ein Iterator:
__iter__ gab self zurück, und nach einem Durchlauf war sie verbraucht.
Python unterscheidet zwei Rollen:

- Ein Iterable ist etwas, das man durchlaufen kann. Es hat eine Methode
  __iter__, die einen Iterator liefert. Listen, Texte, Dictionaries und
  range sind Iterables.
- Ein Iterator ist ein Lesezeichen in einem Durchlauf. Er hat __next__
  (nächster Wert oder StopIteration) und ein __iter__, das self
  zurückgibt.

for x in daten ruft zuerst iter(daten) auf, also daten.__iter__(). Bei
einer Liste entsteht dabei jedes Mal ein neuer Listen-Iterator, darum
kann man eine Liste beliebig oft und sogar verschachtelt durchlaufen:

    zahlen = [1, 2]
    [(a, b) for a in zahlen for b in zahlen]   →  [(1, 1), (1, 2), (2, 1), (2, 2)]
    iter(zahlen) is iter(zahlen)               →  False
    it = iter(zahlen)
    iter(it) is it                             →  True

Eine eigene Klasse wird zum Iterable, indem ihr __iter__ ein neues
Iterator-Objekt einer zweiten Klasse zurückgibt. Die Daten liegen im
Iterable; der Iterator hält nur einen Verweis darauf und seine eigene
Position:

    class Zimmer:
        def __init__(self, namen):
            self.namen = namen

        def __iter__(self):
            return ZimmerIterator(self)

    class ZimmerIterator:
        def __init__(self, zimmer):
            self.zimmer = zimmer
            self.position = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.position >= len(self.zimmer.namen):
                raise StopIteration
            name = self.zimmer.namen[self.position]
            self.position += 1
            return name

Gäbe Zimmer.__iter__ stattdessen self zurück und speicherte die Position
im Zimmer selbst, liefe der zweite Durchlauf leer, und zwei verschachtelte
Schleifen störten sich gegenseitig. Welches Band an Tag t dran ist, liefert
der Rest beim Teilen (Aufgabe 1_009): baender[(t - 1) % len(baender)].
"""


class Rotationsplan:
    """Plan, welches Band an welchem Tag benutzt wird; beliebig oft durchlaufbar."""

    def __init__(self, baender, tage):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class PlanIterator:
    """Ein Durchlauf durch einen Rotationsplan, Tag für Tag."""

    def __init__(self, plan):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __next__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


plan = Rotationsplan(["Band A", "Band B", "Band C"], 4)
print(list(plan))
