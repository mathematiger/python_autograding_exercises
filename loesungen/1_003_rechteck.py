# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_003_rechteck.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_003_rechteck

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

flaeche = breite * hoehe
umfang = 2 * (breite + hoehe)
print("Fläche:", flaeche)
print("Umfang:", umfang)


# Idee: Die Fläche ist Breite mal Höhe, der Umfang zweimal Breite plus zweimal Höhe. Rechnen Sie mit den
# Variablen breite und hoehe, dann stimmt das Programm für jeden Raum, den jemand eintippt.
# Anderer Weg: umfang = breite + hoehe + breite + hoehe oder 2 * breite + 2 * hoehe; alle drei Formeln
# ergeben dasselbe.
# Typische Fehler: 2 * breite + hoehe ohne Klammern (Punkt vor Strich: bei 4 und 3 nur 11), die Zahlen 12
# und 14 fest hinschreiben (stimmt nur für das Beispiel) oder print("Fläche:" + flaeche), das mit einem
# TypeError abbricht, weil + keinen Text mit einer Zahl verbindet.
