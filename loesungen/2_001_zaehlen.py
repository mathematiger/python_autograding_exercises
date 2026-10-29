# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_001_zaehlen.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_001_zaehlen

"""Aufgabe 2_001 – Zählen                                       Stufe 2 ★★☆☆☆

Im Serverraum stehen fünf Racks, die für eine Beschriftungsliste von 1 bis 5
durchnummeriert werden. Geben Sie mit einer for-Schleife die Zahlen von 1 bis 5
untereinander aus:

    1
    2
    3
    4
    5

Hintergrund: for zahl in range(a, b): nimmt nacheinander die Zahlen a, a + 1,
… bis b - 1 in die Variable zahl und führt jedes Mal den eingerückten Block
darunter aus. Die obere Grenze b gehört nicht dazu. Hinter der Kopfzeile steht
ein Doppelpunkt, und der Block darunter ist eingerückt.

Tipp: range(1, 6) liefert die Zahlen 1, 2, 3, 4, 5.
"""

for zahl in range(1, 6):
    print(zahl)


# Idee: range(1, 6) liefert die Zahlen 1 bis 5; die for-Schleife nimmt sie
# nacheinander in die Variable zahl, und print gibt jede in einer eigenen Zeile aus.
#
# Anderer Weg: eine while-Schleife mit einem Zähler, der bei 1 beginnt und nach
# jeder Ausgabe um 1 wächst (zahl = zahl + 1), solange zahl <= 5 ist. Das ist
# länger und man kann das Hochzählen vergessen; dann läuft die Schleife endlos.
#
# Typische Fehler: range(5) gibt 0 bis 4 aus, range(1, 5) nur 1 bis 4, denn die
# obere Grenze gehört nicht dazu. print(zahl) muss eingerückt unter der
# for-Zeile stehen, sonst meldet Python einen IndentationError.
