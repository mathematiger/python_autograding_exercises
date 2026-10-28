# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_002_verdoppeln.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_002_verdoppeln

"""Aufgabe 2_002 – Verdoppeln                                   Stufe 2 ★★☆☆☆

Vervollständigen Sie die Funktion `verdopple`. Sie bekommt eine Zahl und soll das
Doppelte davon zurückgeben (mit return, nicht mit print!).

    verdopple(21)  →  42

Grenzen: zahl ist eine ganze Zahl mit -10**9 ≤ zahl ≤ 10**9.
"""


def verdopple(zahl):
    return 2 * zahl


print(verdopple(21))


# Idee: Das Doppelte ist 2 * zahl. Die Funktion rechnet es aus und gibt es mit
# return an den Aufrufer zurück; erst das Programm unten gibt es mit print aus.
#
# Anderer Weg: zahl + zahl, auch über eine Hilfsvariable
# (ergebnis = zahl + zahl, dann return ergebnis).
#
# Typische Fehler: print statt return. Dann sieht man die Zahl zwar auf dem
# Bildschirm, aber die Funktion liefert None, und niemand kann mit dem Ergebnis
# weiterrechnen. Ebenso falsch ist eine Lösung, die nur für positive Zahlen
# stimmt, etwa mit einem if, das negative Zahlen unverändert zurückgibt.
