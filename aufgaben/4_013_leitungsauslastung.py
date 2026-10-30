"""Aufgabe 4_013 – Leitungsauslastung                            Stufe 4 ★★★★☆

Ein Unternehmen verbindet seine Standorte über gemietete Leitungen, und
jede Leitung hat eine feste Bandbreite in Mbit/s. Das Netzwerk-Monitoring
misst für jede Leitung und jede Stunde den mittleren Datenverkehr, auch in
Mbit/s. Die Messungen stehen in einem zweidimensionalen numpy-Array
verkehr: Zeile i gehört zu Leitung i, Spalte s zu Stunde s. Die
Bandbreiten stehen in einem eindimensionalen Array bandbreite, Eintrag i
für Leitung i.

Schreiben Sie vier Auswertungen, alle ohne Python-Schleife:

- `spitzen(verkehr)`: für jede Leitung den höchsten Verkehr über alle
  Stunden, als Array mit einem Eintrag pro Leitung.
- `stundenmittel(verkehr)`: für jede Stunde den mittleren Verkehr über
  alle Leitungen, als Array mit einem Eintrag pro Stunde.
- `auslastung(verkehr, bandbreite)`: ein Array derselben Form wie
  verkehr mit der Auslastung in Prozent, verkehr[i, s] / bandbreite[i]
  * 100.
- `ueberlastet(verkehr, bandbreite, schwelle)`: die Nummern der
  Leitungen, deren Auslastung in mindestens einer Stunde über schwelle
  Prozent lag, aufsteigend als Python-Liste.

    verkehr = np.array([[200, 850, 400],     # Leitung 0
                        [ 90, 100,  95]])    # Leitung 1
    bandbreite = np.array([1000, 100])
    spitzen(verkehr)                       →  array([850, 100])
    stundenmittel(verkehr)                 →  array([145. , 475. , 247.5])
    auslastung(verkehr, bandbreite)        →  array([[ 20.,  85.,  40.],
                                                     [ 90., 100.,  95.]])
    ueberlastet(verkehr, bandbreite, 90)   →  [1]
    ueberlastet(verkehr, bandbreite, 80)   →  [0, 1]

Grenzen: verkehr hat die Form (n, h) mit 1 ≤ n ≤ 1000 Leitungen und
1 ≤ h ≤ 168 Stunden (eine Woche), ganze Zahlen (dtype int64) von 0 bis
10**5. bandbreite hat die Form (n,) mit ganzen Zahlen von 1 bis 10**5;
der Verkehr darf über der Bandbreite liegen (dann staut sich etwas).
schwelle ist eine ganze Zahl von 0 bis 1000. Die Zahl der ausgeführten
Python-Zeilen soll nicht mit n oder h wachsen.

Hintergrund: Ein zweidimensionales Array hat zwei Achsen. Achse 0 läuft
die Zeilen hinunter, Achse 1 die Spalten entlang. Auswertungen wie sum,
mean, max oder any nehmen ein Argument axis, das sagt, welche Achse
dabei verschwindet:

    a = np.array([[1, 2, 3],
                  [4, 5, 6]])     # a.shape ist (2, 3)
    a.sum()            →  21                    alles zusammen
    a.sum(axis=0)      →  array([5, 7, 9])      Achse 0 fällt weg: je Spalte
    a.sum(axis=1)      →  array([ 6, 15])       Achse 1 fällt weg: je Zeile

Merkregel: Bei axis=0 wird über die Zeilen hinweg zusammengefasst, und
es bleibt eine Zahl pro Spalte übrig; bei axis=1 eine Zahl pro Zeile.

Rechnet man zwei Arrays verschiedener Form miteinander, gleicht numpy
die Formen nach festen Regeln an; das heißt Broadcasting. Die Formen
werden von hinten verglichen. Zwei Längen passen, wenn sie gleich sind
oder eine davon 1 ist; eine Achse der Länge 1 wird gedanklich so oft
wiederholt, wie nötig. Fehlt einem Array vorne eine Achse, zählt sie
als Länge 1:

    a + np.array([10, 20, 30])     # (2, 3) und (3,): passt, je Spalte
    →  array([[11, 22, 33],
              [14, 25, 36]])
    a + np.array([100, 200])       # (2, 3) und (2,): 3 gegen 2, ValueError

Soll ein Wert pro Zeile verrechnet werden, braucht das zweite Array die
Form (2, 1), eine Spalte. Die bekommt man mit [:, np.newaxis] (kurz
[:, None]) oder reshape(-1, 1):

    zeilenwerte = np.array([100, 200])
    zeilenwerte[:, np.newaxis].shape   →  (2, 1)
    a + zeilenwerte[:, np.newaxis]
    →  array([[101, 102, 103],
              [204, 205, 206]])

Gefährlich ist der Fall, in dem die Formen zufällig zusammenpassen: Bei
einem quadratischen Array der Form (3, 3) rechnet a + b mit b der Form
(3,) ohne Fehlermeldung, aber je Spalte statt je Zeile.

Um zu prüfen, ob in einer Zeile irgendwo True steht, gibt es
maske.any(axis=1); np.flatnonzero(werte) liefert die Positionen aller
Einträge, die nicht 0 oder False sind.
"""

import numpy as np


def spitzen(verkehr):
    """Gibt für jede Leitung den höchsten Verkehr über alle Stunden zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def stundenmittel(verkehr):
    """Gibt für jede Stunde den mittleren Verkehr über alle Leitungen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auslastung(verkehr, bandbreite):
    """Gibt die Auslastung jeder Leitung in jeder Stunde in Prozent zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ueberlastet(verkehr, bandbreite, schwelle):
    """Gibt die Nummern der Leitungen zurück, die in mindestens einer Stunde über schwelle Prozent lagen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


verkehr = np.array([[200, 850, 400], [90, 100, 95]])
bandbreite = np.array([1000, 100])
print(spitzen(verkehr).tolist())
print(stundenmittel(verkehr).tolist())
print(auslastung(verkehr, bandbreite).tolist())
print(ueberlastet(verkehr, bandbreite, 90))
