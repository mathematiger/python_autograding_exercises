"""Aufgabe 3_013 – Testquoten                                     Stufe 3 ★★★☆☆

Ein Softwareprojekt besteht aus vielen Modulen, und zu jedem Modul gibt
es automatische Tests. Nach jedem Testlauf meldet das Testwerkzeug für
jedes Modul, wie viele Tests es hat und wie viele davon fehlgeschlagen
sind. Das Qualitätsteam will daraus zwei Kennzahlen je Modul berechnen:

- die Erfolgsquote, also den Anteil der bestandenen Tests in Prozent,
- den Analyseaufwand in Stunden: Jeder fehlgeschlagene Test braucht im
  Mittel minuten_pro_fehler Minuten, bis die Ursache gefunden ist.

Weil große Projekte Zehntausende Module haben, sollen die Rechnungen
mit numpy-Arrays laufen, ohne Python-Schleife. Schreiben Sie:

- `erfolgsquoten(tests, fehlgeschlagen)`: bekommt zwei gleich lange
  Python-Listen und gibt ein numpy-Array mit den Erfolgsquoten in Prozent
  zurück, (tests - fehlgeschlagen) / tests * 100 für jedes Modul.
- `analyseaufwand(fehlgeschlagen, minuten_pro_fehler)`: bekommt eine
  Python-Liste und eine Zahl und gibt ein numpy-Array mit dem Aufwand in
  Stunden je Modul zurück.

    erfolgsquoten([40, 25, 8], [2, 0, 4])   →  array([ 95., 100.,  50.])
    analyseaufwand([2, 0, 4], 45)           →  array([1.5, 0. , 3. ])

Grenzen: 0 ≤ len(tests) = len(fehlgeschlagen) ≤ 100 000. Alle Einträge
sind ganze Zahlen mit 1 ≤ tests[i] ≤ 10**6 und
0 ≤ fehlgeschlagen[i] ≤ tests[i]; 0 ≤ minuten_pro_fehler ≤ 600 ist eine
ganze Zahl. Die Zahl der ausgeführten Python-Zeilen soll nicht mit der
Länge der Listen wachsen.

Hintergrund: numpy ist eine Bibliothek für das Rechnen mit vielen Zahlen
auf einmal. Ihr wichtigster Typ ist das Array, eine Folge von Zahlen
gleichen Typs. Man legt es aus einer Liste an:

    import numpy as np
    a = np.array([40, 25, 8])
    b = np.array([2, 0, 4])

Rechenzeichen zwischen zwei gleich langen Arrays wirken elementweise,
also Stelle für Stelle: a - b ist array([38, 25, 4]), a * b ist
array([80, 0, 32]). Steht auf einer Seite eine einzelne Zahl, wird sie
mit jedem Element verrechnet: b * 30 ist array([60, 0, 120]), a / 4 ist
array([10. , 6.25, 2. ]). Mit Listen geht das nicht: [40, 25] - [2, 0]
ist ein TypeError, und [2, 0] * 3 hängt die Liste dreimal aneinander.

Der Vorteil: Die Schleife über alle Elemente läuft in numpy, in schnellem
C-Code, statt Zeile für Zeile in Python; bei 100 000 Zahlen ist das oft
hundertmal schneller. Mit .tolist() wird aus einem Array wieder eine
Liste, mit len(a) bekommt man die Länge, und print zeigt ein Array ohne
Kommas, etwa [ 95. 100.  50.].
"""

import numpy as np


def erfolgsquoten(tests, fehlgeschlagen):
    """Gibt die Anteile der bestandenen Tests je Modul in Prozent als numpy-Array zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def analyseaufwand(fehlgeschlagen, minuten_pro_fehler):
    """Gibt den Aufwand für die Fehleranalyse je Modul in Stunden als numpy-Array zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(erfolgsquoten([40, 25, 8], [2, 0, 4]).tolist())
print(analyseaufwand([2, 0, 4], 45).tolist())
