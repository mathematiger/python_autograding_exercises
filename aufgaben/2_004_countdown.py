"""Aufgabe 2_004 – Countdown                                    Stufe 2 ★★☆☆☆

Vor einem geplanten Neustart zählt der Server die Sekunden herunter, damit alle
Angemeldeten ihre Arbeit noch speichern können. Das Programm fragt, bei welcher
Zahl der Countdown beginnt. Geben Sie dann mit einer while-Schleife die Zahlen
rückwärts bis 1 aus und zum Schluss das Wort „Neustart!“. Bei Eingabe 3:

    3
    2
    1
    Neustart!

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

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
