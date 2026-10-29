# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_004_countdown.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_004_countdown

"""Aufgabe 2_004 – Countdown                                    Stufe 2 ★★☆☆☆

Beim Raketenstart zählt die Kontrolle rückwärts. Das Programm fragt, bei welcher
Zahl der Countdown beginnt. Geben Sie dann mit einer while-Schleife die Zahlen
rückwärts bis 1 aus und zum Schluss das Wort „Start!“. Bei Eingabe 3:

    3
    2
    1
    Start!

Grenzen: Die Eingabe ist eine ganze Zahl mit 0 ≤ zahl ≤ 1000.

Hintergrund: Eine while-Schleife wiederholt ihren Block, solange die Bedingung
dahinter wahr ist. Vor jedem Durchlauf wird die Bedingung neu geprüft. Damit
die Schleife irgendwann endet, muss sich im Block etwas ändern, das in der
Bedingung vorkommt, hier die Zahl:

    while zahl > 0:
        ...
        zahl = zahl - 1

Vergisst man die letzte Zeile, läuft die Schleife endlos. Die Prüfung bricht
dann nach 5 Sekunden ab.
"""

zahl = int(input("Countdown ab: "))

while zahl > 0:
    print(zahl)
    zahl = zahl - 1
print("Start!")


# Idee: Die Zahl aus der Eingabe ist zugleich der Zähler. Solange sie größer als
# 0 ist, wird sie ausgegeben und um 1 verkleinert; ist sie bei 0 angekommen,
# endet die Schleife, und darunter steht einmal print("Start!").
#
# Anderer Weg: for rest in range(zahl, 0, -1): print(rest) zählt ebenfalls rückwärts bis 1.
# Das ist kürzer, aber hier soll die while-Schleife geübt werden.
#
# Typische Fehler: zahl = zahl - 1 vergessen (Endlosschleife), while zahl >= 0
# (gibt zusätzlich 0 aus) oder print("Start!") in die Schleife einrücken (dann
# steht es nach jeder Zahl). Bei Eingabe 0 darf nur Start! erscheinen.
