# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_014_usability.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_014_usability

"""Aufgabe 3_014 – Usability-Test                                 Stufe 3 ★★★☆☆

Bevor ein neues Bestellformular online geht, testet das Team es mit
echten Nutzerinnen und Nutzern: Jede Testperson soll eine Bestellung
aufgeben, und die Software misst, wie viele Sekunden sie dafür braucht
und ob sie es am Ende geschafft hat. Wer lange braucht oder aufgibt, ist
irgendwo im Formular hängen geblieben. Die Messwerte liegen als zwei
gleich lange numpy-Arrays vor: zeiten (ganze Sekunden) und erfolgreich
(True oder False für jede Testperson).

Schreiben Sie drei Auswertungsfunktionen, alle ohne Python-Schleife:

- `anzahl_ueber(zeiten, grenze)`: wie viele Testpersonen mehr als
  grenze Sekunden gebraucht haben, als ganze Zahl.
- `mittel_erfolgreich(zeiten, erfolgreich)`: die mittlere Zeit derer,
  die es geschafft haben; None, wenn es niemand geschafft hat.
- `laengste_erfolgreich(zeiten, erfolgreich)`: die längste Zeit, die
  eine erfolgreiche Testperson gebraucht hat; None, wenn es niemand
  geschafft hat.

    zeiten = np.array([95, 240, 61, 180, 300])
    erfolgreich = np.array([True, False, True, True, False])
    anzahl_ueber(zeiten, 120)                    →  3
    mittel_erfolgreich(zeiten, erfolgreich)      →  112.0
    laengste_erfolgreich(zeiten, erfolgreich)    →  180

Grenzen: zeiten ist ein Array ganzer Zahlen (dtype int64) mit
1 ≤ zeiten[i] ≤ 3600, erfolgreich ein gleich langes Array mit dtype bool;
beide haben 0 bis 100 000 Einträge. 0 ≤ grenze ≤ 3600 ist eine ganze
Zahl. Die Zahl der ausgeführten Python-Zeilen soll nicht mit der Länge
der Arrays wachsen.

Hintergrund: Ein Vergleich zwischen einem Array und einer Zahl wirkt wie
das Rechnen elementweise (Aufgabe 3_013) und liefert ein Array aus True
und False, eine Maske:

    a = np.array([5, 12, 8, 20])
    maske = a > 10          →  array([False,  True, False,  True])

Mit einer Maske in eckigen Klammern wählt man die Elemente aus, bei
denen True steht: a[maske] ist array([12, 20]). Die Maske muss genauso
lang sein wie das Array. Masken verknüpft man mit & (und), | (oder)
und ~ (nicht), etwa a[(a > 6) & (a < 15)], mit Klammern um jeden
Vergleich.

Arrays haben fertige Auswertungen: a.sum(), a.mean() (Mittelwert),
a.max() und a.min(). Bei einer Maske zählt maske.sum() die True-Werte,
weil True als 1 und False als 0 gerechnet wird. Vorsicht bei leeren
Arrays: np.array([]).max() ist ein ValueError, und mean() liefert nan
(„not a number“) mit einer Warnung. Prüfen Sie darum vorher, ob etwas
ausgewählt wurde, etwa mit len(auswahl) == 0.
"""

import numpy as np


def anzahl_ueber(zeiten, grenze):
    """Gibt zurück, wie viele Zeiten größer als grenze sind."""
    return int((zeiten > grenze).sum())


def mittel_erfolgreich(zeiten, erfolgreich):
    """Gibt die mittlere Zeit der erfolgreichen Testpersonen zurück, None ohne Erfolge."""
    auswahl = zeiten[erfolgreich]
    if len(auswahl) == 0:
        return None
    return float(auswahl.mean())


def laengste_erfolgreich(zeiten, erfolgreich):
    """Gibt die längste Zeit einer erfolgreichen Testperson zurück, None ohne Erfolge."""
    auswahl = zeiten[erfolgreich]
    if len(auswahl) == 0:
        return None
    return int(auswahl.max())


zeiten = np.array([95, 240, 61, 180, 300])
erfolgreich = np.array([True, False, True, True, False])
print(anzahl_ueber(zeiten, 120))
print(mittel_erfolgreich(zeiten, erfolgreich))
print(laengste_erfolgreich(zeiten, erfolgreich))


# Idee: zeiten > grenze ist eine Maske, und ihre Summe zählt die True-Werte. Für die beiden anderen
# Auswertungen wählt zeiten[erfolgreich] nur die Zeiten der erfolgreichen Testpersonen aus. Ist diese
# Auswahl leer, kommt None zurück; sonst liefern .mean() und .max() Mittelwert und Maximum. int(...)
# und float(...) machen aus den numpy-Zahlen gewöhnliche Python-Zahlen.
#
# Anderer Weg: np.count_nonzero(zeiten > grenze) zählt ebenfalls, und erfolgreich.any() prüft, ob es
# mindestens einen Erfolg gibt. Mit einer Schleife über zip(zeiten, erfolgreich) kommt dasselbe heraus,
# aber jede Testperson kostet dann eine Python-Zeile.
#
# Typische Fehler: >= statt > (Zeiten genau an der Grenze zählen mit), zeiten.mean() statt
# zeiten[erfolgreich].mean() (dann zählen die Abbrecher mit), and statt & beim Verknüpfen von Masken
# (ValueError) oder max() auf einer leeren Auswahl (ValueError).
#
# Laufzeit: O(n) für n Testpersonen; Maske, Auswahl, Summe, Mittelwert und Maximum berechnet numpy
# in C, in Python laufen nur wenige Zeilen.
