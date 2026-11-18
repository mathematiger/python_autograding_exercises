"""Aufgabe 4_033 – Bandrotation                                  Stufe 4 ★★★★☆

Im Rechenzentrum eines Dienstleisters wird jede Nacht eine Sicherung der
Kundenserver auf ein Magnetband geschrieben. Die Bänder werden reihum
benutzt (Rotation): Bei den Bändern "A", "B" und "C" bekommt Tag 1 Band
A, Tag 2 Band B, Tag 3 Band C, Tag 4 wieder Band A und so weiter. Ein
Sicherungsplan beschreibt so eine Rotation über eine Anzahl von Tagen.

Den Plan durchlaufen verschiedene Programmteile, oft auch gleichzeitig:
Der Bericht geht ihn Tag für Tag durch, und für jeden Tag sucht eine
zweite, innere Schleife über denselben Plan alle Tage mit demselben
Band. Mit einem Iterator wie in Aufgabe 4_032 geht das nicht, denn der
ist nach einem Durchlauf verbraucht, und zwei Schleifen über denselben
Iterator stören sich. Der Plan soll darum ein Iterable sein, das bei
jedem Durchlauf einen frischen Iterator liefert. Vervollständigen Sie
die beiden Klassen:

- `Sicherungsplan(baender, tage)` merkt sich die Liste der Bänder und die
  Anzahl der Tage. `__iter__` gibt bei jedem Aufruf einen neuen
  `PlanIterator` für diesen Plan zurück.
- `PlanIterator(plan)` merkt sich den Plan und den zuletzt gelieferten
  Tag (am Anfang 0). `__next__` liefert das Paar (tag, band) für den
  nächsten Tag, beginnend mit (1, erstes Band), und löst nach dem
  letzten Tag StopIteration aus, auch bei jedem weiteren Aufruf.
  `__iter__` gibt den Iterator selbst zurück.

    plan = Sicherungsplan(["A", "B", "C"], 5)
    list(plan)     →  [(1, "A"), (2, "B"), (3, "C"), (4, "A"), (5, "B")]
    list(plan)     →  dasselbe noch einmal
    zeiger = iter(plan)
    next(zeiger)   →  (1, "A")
    next(zeiger)   →  (2, "B")
    next(iter(plan))  →  (1, "A")     (ein neuer Iterator beginnt vorn)

Schreiben Sie beide Klassen mit __iter__ und __next__ von Hand, ohne
yield. Der Iterator berechnet das Band erst, wenn der Tag abgeholt wird,
und legt keine Liste aller Tage an.

Grenzen: 1 ≤ len(baender) ≤ 100, die Bänder sind nicht leere Texte.
tage ist eine ganze Zahl mit 0 ≤ tage ≤ 10**12; so lange Pläne durchläuft
niemand ganz, aber die ersten Tage müssen sofort kommen. Ein vollständig
durchlaufener Plan hat höchstens 10 000 Tage. Die Liste baender wird
nicht verändert.

Hintergrund: Python unterscheidet zwei Rollen.

- Ein Iterable ist alles, worüber man mit for laufen kann: Listen,
  Texte, Dictionaries, range(...). Es hat eine Methode __iter__, die
  einen Iterator liefert. Das Iterable selbst merkt sich keinen
  Fortschritt.
- Ein Iterator ist das Lesezeichen für einen einzelnen Durchlauf. Er hat
  __next__, das den nächsten Wert liefert und sich merkt, wie weit er
  ist, und __iter__, das ihn selbst zurückgibt.

Eine for-Schleife ruft zu Beginn iter(...) auf das Iterable auf und holt
sich so einen neuen Iterator. Darum kann man eine Liste beliebig oft und
sogar verschachtelt durchlaufen, einen Iterator aber nur einmal:

    zahlen = [1, 2]
    iter(zahlen) is iter(zahlen)       →  False  (jedes Mal ein neuer)
    paare = [(a, b) for a in zahlen for b in zahlen]   # 4 Paare

    zeiger = iter(zahlen)
    zeiger is iter(zeiger)             →  True   (ein Iterator gibt sich selbst)
    [(a, b) for a in zeiger for b in zeiger]           # nur [(1, 2)]

Im zweiten Fall verbraucht die innere Schleife den einzigen Iterator,
und die äußere hat danach nichts mehr. Eigene Klassen trennen deshalb
die beiden Rollen: Die Klasse mit den Daten (hier der Plan) ist das
Iterable; ihr __iter__ erzeugt jedes Mal ein neues Objekt einer zweiten
Klasse, die den Fortschritt hält:

    class Strecke:
        def __init__(self, laenge):
            self.laenge = laenge

        def __iter__(self):
            return StreckenIterator(self)       # jedes Mal ein neuer

    class StreckenIterator:
        def __init__(self, strecke):
            self.strecke = strecke
            self.position = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.position >= self.strecke.laenge:
                raise StopIteration
            self.position += 1
            return self.position

So eine Klasse verhält sich wie range: Sie ist klein, rechnet jeden Wert
erst bei Bedarf aus und lässt sich beliebig oft durchlaufen. Dass man
__iter__ auch als Generatormethode mit yield schreiben kann, zeigt eine
spätere Aufgabe.

Tipp: Das Band für Tag t ist baender[(t - 1) % len(baender)].
"""


class Sicherungsplan:
    """Rotation der Sicherungsbänder über eine Anzahl von Tagen; beliebig oft durchlaufbar."""

    def __init__(self, baender, tage):
        """Merkt sich die Bänder und die Anzahl der Tage."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        """Gibt bei jedem Aufruf einen neuen Iterator über die Tage zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class PlanIterator:
    """Ein einzelner Durchlauf durch einen Sicherungsplan."""

    def __init__(self, plan):
        """Merkt sich den Plan; noch kein Tag ist geliefert."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        """Ein Iterator gibt sich selbst zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __next__(self):
        """Liefert (tag, band) für den nächsten Tag oder löst StopIteration aus."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


plan = Sicherungsplan(["A", "B", "C"], 5)
print(list(plan))
print(list(plan))
