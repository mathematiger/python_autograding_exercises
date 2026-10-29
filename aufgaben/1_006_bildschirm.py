"""Aufgabe 1_006 – Bildschirmdiagonale                           Stufe 1 ★☆☆☆☆

Bei Bildschirmen und Fernsehern steht im Datenblatt nur die Diagonale, meist in
Zoll, zum Beispiel „50 Zoll“ (1 Zoll sind 2,54 cm, 50 Zoll also 127 cm). Sie
wollen einen vorhandenen Bildschirm mit den Angeboten vergleichen und haben
Breite und Höhe seiner Bildfläche (ohne Rahmen) in Zentimetern gemessen. Das
Programm fragt schon nach beiden Werten. Berechnen Sie daraus die Diagonale in
Zentimetern mit dem Satz des Pythagoras und geben Sie sie ungerundet aus. Bei
Eingabe 80 und 60 soll das Programm ausgeben:

    Die Diagonale ist 100.0 cm lang.

Die Formel: Diagonale = Wurzel aus (Breite² + Höhe²)

Grenzen: Breite und Höhe sind Zahlen zwischen 1 und 1000 mit höchstens einer
Nachkommastelle, zum Beispiel 80, 2.5 oder 121.7.

Hintergrund: Der Operator ** rechnet „hoch“: 3 ** 2 ergibt 9, 2 ** 10 ergibt
1024. Für die Wurzel gibt es die Funktion sqrt (englisch „square root“) im
Modul math. Ein Modul ist eine Sammlung fertiger Funktionen, die man erst mit
import math laden muss; danach ruft man sie mit dem Modulnamen und einem Punkt
auf: math.sqrt(9) ergibt 3.0. Die Zeile import math steht schon oben im
Programm.

Tipp: print("Die Diagonale ist", diagonale, "cm lang.") setzt zwischen die
Teile automatisch ein Leerzeichen.
"""

import math

breite = float(input("Breite in cm: "))
hoehe = float(input("Höhe in cm: "))

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
