# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_042_zeittabelle.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_042_zeittabelle

"""Aufgabe 1_042 – Zeittabelle                                   Stufe 1 ★☆☆☆☆

In einer Prozessanalyse wird geschätzt, wie lange ein Arbeitsschritt
insgesamt dauert: Gesamtzeit = Anzahl der Vorgänge mal Minuten pro
Vorgang. Damit die Teamleitung nicht jedes Mal rechnen muss, hängt eine
Tabelle an der Wand: Jede Zeile steht für eine Anzahl von Vorgängen
(1, 2, 3, …), jede Spalte für eine Dauer in Minuten pro Vorgang (1, 2,
3, …), und in jeder Zelle steht die Gesamtzeit.

Das Programm fragt schon nach der Zahl der Zeilen und der Spalten, und
die äußere Schleife geht die Zeilen durch. Ergänzen Sie die innere
Schleife, die in einer Zeile alle Gesamtzeiten nebeneinander ausgibt,
getrennt durch ein Leerzeichen. Bei 3 Zeilen und 4 Spalten:

    1 2 3 4
    2 4 6 8
    3 6 9 12

Grenzen: Zeilen und Spalten sind ganze Zahlen von 1 bis 12.

Hintergrund: Eine Schleife darf in einer anderen stehen. Die innere
Schleife läuft dann bei jedem Durchgang der äußeren einmal ganz durch:

    for a in range(1, 3):
        for b in range(1, 4):
            print(a, b)

gibt 1 1, 1 2, 1 3, 2 1, 2 2, 2 3 aus, je ein Paar pro Zeile. print
beginnt normalerweise nach jeder Ausgabe eine neue Zeile. Mit
print(wert, end=" ") setzt es stattdessen ein Leerzeichen dahinter, und
die nächste Ausgabe kommt in dieselbe Zeile. Ein print() ohne Werte
beendet die Zeile; das steht im Programm schon nach der inneren
Schleife.
"""

zeilen = int(input("Anzahl der Zeilen (Vorgänge): "))
spalten = int(input("Anzahl der Spalten (Minuten pro Vorgang): "))

for vorgaenge in range(1, zeilen + 1):
    for minuten in range(1, spalten + 1):
        print(vorgaenge * minuten, end=" ")
    print()


# Idee: Für jede Zeile (vorgaenge) läuft eine zweite Schleife über die Minuten von 1 bis spalten und
# gibt vorgaenge * minuten mit end=" " aus, damit alles in derselben Zeile bleibt. Das vorgegebene
# print() beendet danach die Zeile, und die äußere Schleife macht mit der nächsten weiter.
# Anderer Weg: Die Werte einer Zeile erst in einem Text sammeln (zeile = zeile + str(wert) + " ")
# und ihn nach der inneren Schleife mit einem einzigen print ausgeben.
# Typische Fehler: end=" " vergessen (dann steht jede Zahl in einer eigenen Zeile), range(spalten)
# statt range(1, spalten + 1) (dann beginnt jede Zeile mit 0 und die letzte Spalte fehlt), in der
# inneren Schleife bis zeilen statt bis spalten zählen oder das print() mit einrücken.
