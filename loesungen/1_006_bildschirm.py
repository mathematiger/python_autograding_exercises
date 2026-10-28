# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_006_bildschirm.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_006_bildschirm

"""Aufgabe 1_006 – Bildschirmdiagonale                           Stufe 1 ★☆☆☆☆

Im Elektromarkt steht bei jedem Fernseher nur die Diagonale, zum Beispiel
„50 Zoll“. Sie wollen aber wissen, ob ein Gerät in Ihr Regal passt, und haben
Breite und Höhe des Bildschirms in Zentimetern gemessen. Das Programm fragt
schon nach beiden Werten. Berechnen Sie daraus die Diagonale mit dem Satz des
Pythagoras und geben Sie sie aus. Bei Eingabe 80 und 60 soll das Programm
ausgeben:

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

diagonale = math.sqrt(breite ** 2 + hoehe ** 2)
print("Die Diagonale ist", diagonale, "cm lang.")


# Idee: Beide Seiten mit ** 2 quadrieren, die Quadrate addieren und aus der Summe mit math.sqrt die
# Wurzel ziehen.
# Andere Wege: breite * breite statt breite ** 2, (breite ** 2 + hoehe ** 2) ** 0.5 statt math.sqrt,
# oder math.hypot(breite, hoehe), das genau diese Rechnung schon fertig mitbringt.
# Typische Fehler: die Wurzel aus jeder Seite einzeln ziehen (math.sqrt(breite) + math.sqrt(hoehe)),
# breite * 2 statt breite ** 2 (das ist das Doppelte, nicht das Quadrat) oder ** 1/2 ohne Klammern:
# x ** 1 / 2 ist die Hälfte von x, nicht die Wurzel.
