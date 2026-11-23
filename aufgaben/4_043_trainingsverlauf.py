"""Aufgabe 4_043 – Trainingsverlauf                              Stufe 4 ★★★★☆

Ein Team trainiert ein Modell für maschinelles Lernen, das Fotos von
Bauteilen als „in Ordnung“ oder „defekt“ einordnen soll. Das Training
läuft in Epochen: In jeder Epoche sieht das Modell alle Trainingsbilder
einmal, danach wird gemessen, welcher Anteil der Prüfbilder richtig
erkannt wird (die Genauigkeit, in Prozent) und wie viele Sekunden die
Epoche gedauert hat. Die Genauigkeit schwankt; sie steigt nicht in
jeder Epoche. Schreiben Sie mit itertools.accumulate drei Funktionen:

- `trainingszeit(sekunden)` gibt für jede Epoche zurück, wie viele
  Sekunden das Training bis zu ihrem Ende insgesamt gedauert hat.
- `bestwerte(genauigkeiten)` gibt für jede Epoche die beste Genauigkeit
  zurück, die bis dahin erreicht wurde.
- `abbruch_nach(genauigkeiten, geduld)` gibt die Nummer der Epoche (ab
  1 gezählt) zurück, nach der das Training abgebrochen wird, oder None,
  wenn es bis zum Ende läuft. Abgebrochen wird nach der ersten Epoche e,
  für die der Bestwert nach e derselbe ist wie geduld Epochen vorher,
  nach Epoche e - geduld. Dann hat sich in den letzten geduld Epochen
  nichts verbessert (englisch „early stopping“). Vor Epoche geduld + 1
  wird nie abgebrochen. Eine gleich gute Genauigkeit zählt nicht als
  Verbesserung.

Alle drei geben Listen zurück bzw. eine Zahl, und die übergebenen
Listen bleiben unverändert.

    trainingszeit([30, 28, 31])                          →  [30, 58, 89]
    genauigkeiten = [61.0, 70.5, 68.2, 74.1, 73.9, 74.1, 72.0]
    bestwerte(genauigkeiten)
        →  [61.0, 70.5, 70.5, 74.1, 74.1, 74.1, 74.1]
    abbruch_nach(genauigkeiten, 2)                       →  6
    abbruch_nach(genauigkeiten, 4)                       →  None

Im Beispiel ist der Bestwert nach Epoche 6 (74.1) derselbe wie nach
Epoche 4, also bricht das Training mit geduld 2 nach Epoche 6 ab.

Grenzen: sekunden und genauigkeiten haben je 0 bis 100 000 Einträge;
sekunden sind ganze Zahlen von 1 bis 10 000, genauigkeiten Kommazahlen
von 0 bis 100. 1 ≤ geduld ≤ 1000. Ihre Lösung soll O(n) Schritte
brauchen.

Hintergrund: In Aufgabe 4_029 hat functools.reduce eine ganze Folge
mit einer Funktion zu einem einzigen Wert zusammengefasst, etwa die
Summe. itertools.accumulate tut dasselbe, liefert aber jeden
Zwischenstand, nicht nur den letzten. Ohne zweites Argument addiert es:

    from itertools import accumulate

    list(accumulate([3, 1, 4, 1]))         →  [3, 4, 8, 9]

Als zweites Argument nimmt accumulate eine Funktion mit zwei
Parametern: den bisherigen Zwischenstand und den nächsten Wert. Sie
gibt den neuen Zwischenstand zurück. Mit max entsteht so das laufende
Maximum, mit min das laufende Minimum, mit lambda a, b: a * b das
laufende Produkt:

    list(accumulate([3, 1, 4, 1], max))    →  [3, 3, 4, 4]
    list(accumulate([5, 2, 8], lambda bisher, neu: bisher * 10 + neu))
                                           →  [5, 52, 528]

Mit initial= beginnt die Folge mit einem Startwert, das Ergebnis ist
dann einen Wert länger: list(accumulate([3, 1], initial=100)) ergibt
[100, 103, 104]. Wie alle Werkzeuge aus itertools ist accumulate ein
lazy Iterator; list(...) holt alle Werte. Für eine leere Folge liefert
es nichts.

Hat man die laufenden Werte einmal in einer Liste, beantwortet ein
Blick an zwei Stellen, was sich zwischen ihnen getan hat. So muss man
nicht für jede Epoche wieder von vorn das Maximum suchen; das wäre
O(n²).
"""

from itertools import accumulate


def trainingszeit(sekunden):
    """Gibt für jede Epoche die bis dahin vergangenen Sekunden zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bestwerte(genauigkeiten):
    """Gibt für jede Epoche die beste bis dahin erreichte Genauigkeit zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def abbruch_nach(genauigkeiten, geduld):
    """Gibt die Epoche zurück, nach der das Training abbricht, oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(trainingszeit([30, 28, 31]))
genauigkeiten = [61.0, 70.5, 68.2, 74.1, 73.9, 74.1, 72.0]
print(bestwerte(genauigkeiten))
print(abbruch_nach(genauigkeiten, 2))
print(abbruch_nach(genauigkeiten, 4))
