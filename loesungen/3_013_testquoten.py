# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_013_testquoten.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_013_testquoten

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
    gesamt = np.array(tests)
    fehler = np.array(fehlgeschlagen)
    return (gesamt - fehler) / gesamt * 100


def analyseaufwand(fehlgeschlagen, minuten_pro_fehler):
    """Gibt den Aufwand für die Fehleranalyse je Modul in Stunden als numpy-Array zurück."""
    return np.array(fehlgeschlagen) * minuten_pro_fehler / 60


print(erfolgsquoten([40, 25, 8], [2, 0, 4]).tolist())
print(analyseaufwand([2, 0, 4], 45).tolist())


# Idee: np.array(...) macht aus jeder Liste ein Array. Dann rechnet (tests - fehlgeschlagen) / tests
# * 100 für alle Module zugleich: Die Rechenzeichen wirken Stelle für Stelle, die einzelne Zahl 100
# wird mit jedem Element verrechnet. Beim Aufwand genügt es, die Fehler in ein Array zu verwandeln;
# mal Minuten und durch 60 gerechnet ergibt es die Stunden.
#
# Anderer Weg: 100 - 100 * fehlgeschlagen / tests rechnet dasselbe. Mit einer Schleife,
# [(t - f) / t * 100 for t, f in zip(tests, fehlgeschlagen)], kommen die gleichen Zahlen heraus,
# aber jede Rechnung läuft dann als Python-Zeile, und das Ergebnis ist eine Liste statt eines Arrays.
#
# Typische Fehler: direkt mit den Listen rechnen (Liste minus Liste ist ein TypeError, Liste mal Zahl
# wiederholt die Liste), nur eine der beiden Listen umwandeln und dabei erst tests - fehlgeschlagen
# mit Listen rechnen, oder die Quote der fehlgeschlagenen statt der bestandenen Tests ausrechnen.
#
# Laufzeit: O(n) Rechenschritte für n Module; die macht numpy in C. In Python laufen nur zwei
# oder drei Zeilen, egal wie lang die Listen sind.
