"""Aufgabe 4_049 – GPU-Budget                                    Stufe 4 ★★★★☆

Ein Entwicklungsteam trainiert seine Modelle auf gemieteten
Grafikprozessoren (GPUs) bei einem Cloud-Anbieter. Abgerechnet wird
stundenweise, und der Preis einer Stunde schwankt mit der Nachfrage.
Die Geschäftsführung hat dem Team ein Budget bewilligt; vor jeder
Verlängerung will sie sehen, ob sich die Miete lohnt. Das
Abrechnungssystem liefert die Kosten jeder Stunde in Cent als
Iterator, der sich nur einmal durchlaufen lässt. Schreiben Sie mit dem
Modul itertools drei Funktionen:

- `stunden_bis_budget(kosten, budget)` gibt zurück, wie viele Stunden
  vom Anfang an die Summe der Kosten höchstens budget ist. kosten kann
  auch ein endloser Iterator sein (die Miete läuft weiter); lesen Sie
  darum nur so weit wie nötig.
- `kostenspruenge(kosten, grenze)` gibt die Liste der Stellen (die
  erste Stunde hat die Stelle 0) zurück, an denen eine Stunde um mehr
  als grenze teurer war als die Stunde davor.
- `kosten_je_tag(protokoll)` bekommt Tupel (datum, cent), die Einträge
  eines Tages stehen hintereinander. Die Funktion gibt die Liste der
  Tupel (datum, summe) zurück, ein Tupel je Tag in der Reihenfolge des
  Protokolls.

Benutzen Sie dafür accumulate und takewhile, pairwise und groupby.

    kosten = [120, 80, 300, 90, 450, 60]
    stunden_bis_budget(iter(kosten), 500)       →  3
    kostenspruenge(iter(kosten), 150)           →  [2, 4]
    kosten_je_tag(iter([("2026-11-02", 120), ("2026-11-02", 80),
                        ("2026-11-03", 300)]))
        →  [("2026-11-02", 200), ("2026-11-03", 300)]

Im ersten Beispiel kosten die ersten drei Stunden zusammen genau 500
Cent, mit der vierten wären es 590.

Grenzen: kosten liefert ganze Zahlen von 0 bis 100 000; ist der
Iterator endlos, wird das Budget irgendwann überschritten. Endliche
Iteratoren haben 0 bis 200 000 Werte. 0 ≤ budget ≤ 10**12,
0 ≤ grenze ≤ 100 000. protokoll hat 0 bis 200 000 Einträge, datum ist
ein Text der Form "JJJJ-MM-TT", cent wie bei kosten.

Hintergrund: Diese Übung verbindet die itertools-Werkzeuge der letzten
Aufgaben. accumulate (Aufgabe 4_043) liefert laufende Summen,
takewhile (Aufgabe 4_047) nimmt Werte, solange eine Bedingung gilt,
pairwise (Aufgabe 4_048) liefert jeden Wert mit seinem Nachfolger, und
groupby (Aufgabe 4_044) fasst aufeinanderfolgende Elemente mit
demselben Schlüssel zusammen:

    from itertools import accumulate, groupby, pairwise, takewhile

    list(accumulate([3, 4, 5]))                       →  [3, 7, 12]
    list(takewhile(lambda s: s <= 7, [3, 7, 12]))     →  [3, 7]
    list(pairwise([3, 4, 5]))                         →  [(3, 4), (4, 5)]
    for raum, gruppe in groupby([("A", 1), ("A", 2), ("B", 5)], key=lambda e: e[0]):
        print(raum, [wert for _, wert in gruppe])     # A [1, 2], dann B [5]

Weil alle lazy arbeiten, lassen sie sich hintereinanderschalten: Was
accumulate liefert, kann takewhile direkt weiterverarbeiten, ohne dass
eine Liste aller Summen entsteht. So hört die Rechnung auf, sobald das
Ergebnis feststeht, auch bei einem endlosen Iterator. Wie viele Werte
ein Iterator liefert, zählt sum(1 for _ in it); len gibt es bei einem
Iterator nicht.
"""

from itertools import accumulate, groupby, pairwise, takewhile


def stunden_bis_budget(kosten, budget):
    """Gibt die Zahl der Stunden zurück, die vom Anfang an ins Budget passen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kostenspruenge(kosten, grenze):
    """Gibt die Stellen zurück, an denen eine Stunde um mehr als grenze teurer war als die davor."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kosten_je_tag(protokoll):
    """Gibt die Liste der Tupel (datum, summe) zurück, eins je Tag."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kosten = [120, 80, 300, 90, 450, 60]
print(stunden_bis_budget(iter(kosten), 500))
print(kostenspruenge(iter(kosten), 150))
print(kosten_je_tag(iter([("2026-11-02", 120), ("2026-11-02", 80), ("2026-11-03", 300)])))
