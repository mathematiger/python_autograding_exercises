"""Aufgabe 4_077 – Qualitätsstufen                               Stufe 4 ★★★★☆

Ein Datenteam prüft jede Nacht die Kundendatenbank eines Versandhändlers.
Für jeden Datensatz berechnet ein Prüfprogramm einen Qualitätswert von 0
bis 100: den Anteil der Felder in Prozent, die gefüllt sind und das
richtige Format haben (Postleitzahl mit fünf Ziffern, gültige
E-Mail-Adresse …). Damit die Fachabteilung den Wert schnell lesen kann,
wird er in Stufen übersetzt, ähnlich wie Punkte in Noten. Die Grenzen
stehen aufsteigend sortiert in einer Liste, die Stufen in einer zweiten,
die genau ein Element mehr hat:

    GRENZEN = [50, 70, 85, 95]
    STUFEN = ["E", "D", "C", "B", "A"]

Unter 50 ist die Stufe "E", ab 50 (einschließlich) "D", ab 70 "C", ab 85
"B" und ab 95 "A". Ein Wert genau auf einer Grenze gehört also schon zur
höheren Stufe. Außerdem führt das Team eine aufsteigend sortierte Liste
aller Qualitätswerte der Nacht und will daraus fragen können, wie viele
Datensätze in einem Bereich liegen. Schreiben Sie drei Funktionen und
benutzen Sie dafür das Modul bisect:

- `stufe(wert, grenzen, stufen)` gibt die Stufe zu einem Qualitätswert
  zurück.
- `fuege_ein(werte, wert)` fügt wert so in die sortierte Liste werte ein,
  dass sie sortiert bleibt, und zwar hinter allen gleichen Werten. Die
  Funktion verändert werte selbst und gibt die Position zurück, an der
  wert jetzt steht.
- `anzahl_im_bereich(werte, von, bis)` gibt zurück, wie viele Werte der
  sortierten Liste werte im Bereich von ≤ wert < bis liegen (bis gehört
  nicht mehr dazu, wie bei range). werte bleibt unverändert.

    stufe(72.5, GRENZEN, STUFEN)    →  "C"
    stufe(85, GRENZEN, STUFEN)      →  "B"
    werte = [40, 55, 70, 70, 88, 97]
    fuege_ein(werte, 70)            →  4
    werte                           →  [40, 55, 70, 70, 70, 88, 97]
    anzahl_im_bereich(werte, 50, 85)  →  4

Grenzen: grenzen ist streng aufsteigend sortiert mit 0 ≤ len(grenzen) ≤
1000, stufen ist eine Liste von Texten mit len(stufen) == len(grenzen) + 1.
Alle Werte und Grenzen sind ganze Zahlen oder Kommazahlen von 0 bis 100.
werte ist aufsteigend sortiert, darf gleiche Werte enthalten und leer
sein, 0 ≤ len(werte) ≤ 100 000. Bei anzahl_im_bereich gilt von ≤ bis.
stufe und anzahl_im_bereich sollen O(log n) Zugriffe auf ihre Liste
brauchen, nicht jedes Element ansehen.

Hintergrund: In Aufgabe 3_002 haben Sie die binäre Suche von Hand
geschrieben: Bereich halbieren, bis die Stelle gefunden ist. Das Modul
bisect der Standardbibliothek erledigt genau das, ohne dass man sich um
die Grenzen der Schleife kümmern muss. Es sucht in einer sortierten
Liste die Einfügeposition eines Werts, also den Index, an dem der Wert
stehen müsste, damit die Liste sortiert bleibt:

    import bisect

    liste = [10, 20, 20, 30]
    bisect.bisect_left(liste, 20)    →  1   (vor den gleichen Werten)
    bisect.bisect_right(liste, 20)   →  3   (hinter den gleichen Werten)
    bisect.bisect_left(liste, 25)    →  3   (ist der Wert nicht da, sind beide gleich)
    bisect.bisect(liste, 20)         →  3   (bisect ist dasselbe wie bisect_right)

Der Unterschied zwischen left und right zählt nur, wenn der Wert schon
in der Liste steht, und genau dieser Fall entscheidet bei Grenzen.
bisect_right(grenzen, wert) zählt, wie viele Grenzen kleiner oder gleich
wert sind; das ist bei „ab 50 einschließlich“ genau der Index der Stufe:

    grenzen = [60, 80]
    namen = ["niedrig", "mittel", "hoch"]
    namen[bisect.bisect_right(grenzen, 80)]   →  "hoch"
    namen[bisect.bisect_left(grenzen, 80)]    →  "mittel"   (80 zählte noch zu „mittel“)

Ebenso zählt bisect_left(liste, x), wie viele Werte kleiner als x sind.
Die Differenz zweier solcher Zahlen ist die Anzahl der Werte in einem
Bereich, ohne die Liste durchzugehen. Zum Einfügen gibt es
bisect.insort_left und bisect.insort_right (kurz insort): Sie suchen die
Position und rufen dann liste.insert auf.

    bisect.insort(liste, 20)         # liste ist jetzt [10, 20, 20, 20, 30]

Das Suchen braucht nur O(log n) Vergleiche. Das Einfügen selbst kostet
trotzdem O(n), weil insert alle Elemente dahinter um einen Platz
verschiebt; für eine Liste, die oft gelesen und selten geändert wird,
ist das in Ordnung. Statt bei jedem neuen Wert liste.append und
liste.sort() aufzurufen, ist insort trotzdem die bessere Wahl. Seit
Python 3.10 nehmen alle bisect-Funktionen auch ein key-Argument wie
sorted (Aufgabe 3_027), etwa um Tupel nach ihrem zweiten Element zu
durchsuchen; hier brauchen Sie es nicht.

Tipp: Die Position für fuege_ein liefert bisect_right, bevor Sie
einfügen.
"""

import bisect


def stufe(wert, grenzen, stufen):
    """Gibt die Stufe zu wert zurück; ein Wert genau auf einer Grenze gehört zur höheren Stufe."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def fuege_ein(werte, wert):
    """Fügt wert sortiert hinter gleichen Werten in werte ein und gibt seine Position zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def anzahl_im_bereich(werte, von, bis):
    """Gibt zurück, wie viele Werte der sortierten Liste im Bereich von ≤ wert < bis liegen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


GRENZEN = [50, 70, 85, 95]
STUFEN = ["E", "D", "C", "B", "A"]

werte = [40, 55, 70, 70, 88, 97]
print(stufe(72.5, GRENZEN, STUFEN))
print(fuege_ein(werte, 70), werte)
print(anzahl_im_bereich(werte, 50, 85))
