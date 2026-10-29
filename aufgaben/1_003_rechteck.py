"""Aufgabe 1_003 – Rechteck                                     Stufe 1 ★☆☆☆☆

Für den neuen Serverraum soll Bodenbelag bestellt und eine Fußleiste ringsum
angebracht werden. Der Raum ist ein Rechteck; das Programm fragt schon nach
seiner Breite und Höhe (in Metern). Berechnen Sie Fläche und Umfang des
Rechtecks. Speichern Sie sie in den Variablen flaeche und umfang und geben Sie
sie danach aus. Bei den Eingaben 4 und 3 soll das Programm ausgeben:

    Fläche: 12
    Umfang: 14

Grenzen: Breite und Höhe sind ganze Zahlen von 1 bis 1000.

Hintergrund: Mit flaeche = breite * hoehe rechnet Python die rechte Seite aus
und speichert das Ergebnis unter dem Namen links. Wie in der Mathematik gilt
Punkt vor Strich; was zuerst gerechnet werden soll, kommt in Klammern:
2 * (breite + hoehe). print kann mehrere Werte durch Kommas getrennt ausgeben
und setzt dazwischen ein Leerzeichen: print("Fläche:", flaeche). Das int(...)
um das input(...) im vorgegebenen Code macht aus dem eingetippten Text eine
ganze Zahl, mit der man rechnen kann (mehr dazu in Aufgabe 1_004).

Tipp: Rechnen Sie mit den Variablen breite und hoehe, nicht mit den Zahlen 4 und 3.
"""

breite = int(input("Breite in Metern: "))
hoehe = int(input("Höhe in Metern: "))

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
