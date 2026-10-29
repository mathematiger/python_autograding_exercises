# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_003_rechteck.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_003_rechteck

"""Aufgabe 1_003 – Rechteck                                     Stufe 1 ★☆☆☆☆

Für den neuen Serverraum soll Bodenbelag bestellt und eine Fußleiste ringsum
angebracht werden. Der Raum ist ein Rechteck; seine Breite und Höhe (in Metern)
stehen schon im Programm. Berechnen Sie Fläche und Umfang des Rechtecks.
Speichern Sie sie in den Variablen flaeche und umfang und geben Sie sie danach
so aus:

    Fläche: 12
    Umfang: 14

Hintergrund: Mit flaeche = breite * hoehe rechnet Python die rechte Seite aus
und speichert das Ergebnis unter dem Namen links. Wie in der Mathematik gilt
Punkt vor Strich; was zuerst gerechnet werden soll, kommt in Klammern:
2 * (breite + hoehe). print kann mehrere Werte durch Kommas getrennt ausgeben
und setzt dazwischen ein Leerzeichen: print("Fläche:", flaeche).

Tipp: Rechnen Sie mit den Variablen breite und hoehe, nicht mit den Zahlen 4 und 3.
"""

breite = 4
hoehe = 3

flaeche = breite * hoehe
umfang = 2 * (breite + hoehe)
print("Fläche:", flaeche)
print("Umfang:", umfang)


# Idee: Die Fläche ist Breite mal Höhe, der Umfang zweimal Breite plus zweimal Höhe. Rechnen Sie mit den
# Variablen breite und hoehe, dann stimmt das Programm auch, wenn jemand die Maße oben ändert.
# Anderer Weg: umfang = breite + hoehe + breite + hoehe oder 2 * breite + 2 * hoehe; alle drei Formeln
# ergeben dasselbe.
# Typische Fehler: 2 * breite + hoehe ohne Klammern (Punkt vor Strich: das ist nur 11), die Zahlen 4 und 3
# fest hinschreiben oder print("Fläche:" + flaeche), das mit einem TypeError abbricht, weil + keinen Text
# mit einer Zahl verbindet.
