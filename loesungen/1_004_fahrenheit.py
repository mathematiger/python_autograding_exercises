# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_004_fahrenheit.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_004_fahrenheit

"""Aufgabe 1_004 – Fahrenheit                                    Stufe 1 ★☆☆☆☆

Eine Freundin aus den USA fragt, wie warm es bei Ihnen ist. Sie kennt aber nur
Grad Fahrenheit. Das Programm fragt schon nach der Temperatur in Celsius.
Rechnen Sie sie um und geben Sie das Ergebnis aus. Bei Eingabe 25 soll das
Programm ausgeben:

    Das sind 77.0 Grad Fahrenheit.

Die Formel: Fahrenheit = Celsius * 9 / 5 + 32

Grenzen: Die Temperatur ist eine Zahl zwischen -50 und 50 mit höchstens einer
Nachkommastelle, zum Beispiel 25, -3.5 oder 36.5.

Hintergrund: input() liefert immer einen Text, auch wenn man eine Zahl eintippt.
Mit "25" kann Python nicht rechnen. Deshalb wandelt float("25") den Text in
die Kommazahl 25.0 um (int("25") würde die ganze Zahl 25 liefern). Erst dann
kann man mit * und + rechnen.

Tipp: print("Das sind", fahrenheit, "Grad Fahrenheit.") setzt zwischen die
Teile automatisch ein Leerzeichen.
"""

eingabe = input("Temperatur in Celsius: ")

celsius = float(eingabe)
fahrenheit = celsius * 9 / 5 + 32
print("Das sind", fahrenheit, "Grad Fahrenheit.")


# Idee: Den Text aus input() mit float(...) in eine Kommazahl umwandeln, die Formel ausrechnen und das
# Ergebnis mit print zwischen die beiden Textteile setzen.
# Anderer Weg: celsius * 1.8 + 32 rechnet dasselbe, weil 9 / 5 genau 1.8 ist. Kommazahlen speichert der
# Rechner aber nur ungefähr, darum steht dann manchmal 20.299999999999997 statt 20.3 da; das ist auch richtig.
# Typische Fehler: mit dem Text eingabe statt mit der Zahl rechnen (TypeError), int(...) statt float(...)
# (36.5 lässt sich nicht umwandeln) oder Klammern falsch setzen: celsius * 9 / (5 + 32) ist etwas anderes.
