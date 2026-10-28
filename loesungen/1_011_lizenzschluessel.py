# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_011_lizenzschluessel.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_011_lizenzschluessel

"""Aufgabe 1_011 – Lizenzschlüssel                              Stufe 1 ★☆☆☆☆

Ein Betrieb kauft Lizenzen für ein Büroprogramm und trägt jeden
Lizenzschlüssel in eine Liste ein, um später zu zählen, wie viele Lizenzen
es gibt und welche davon noch gebraucht werden. Beim Eintragen schleichen
sich leicht Tippfehler ein. Ein Schlüssel des Herstellers ist leicht zu
prüfen: Das erste Zeichen gibt die Produktreihe an, das letzte die Edition
(S für Standard, P für Professional), und die Länge muss stimmen. Das
Programm fragt schon nach dem Schlüssel. Ergänzen Sie die drei Zeilen, die
die Länge, das erste und das letzte Zeichen in die Variablen anzahl, erstes
und letztes schreiben. Bei Eingabe B7K2-QX9M-41TP soll das Programm ausgeben:

    Der Schlüssel hat 14 Zeichen.
    Erstes Zeichen: B
    Letztes Zeichen: P

Grenzen: Der Schlüssel ist ein Text aus 1 bis 50 Zeichen; es kommen nur
Großbuchstaben, Ziffern und Bindestriche vor.

Hintergrund: len(text) liefert, wie viele Zeichen ein Text hat; auch
Bindestriche und Leerzeichen zählen mit. Ein einzelnes Zeichen holt man mit
eckigen Klammern und seiner Position, dem Index, heraus. Python beginnt dabei
bei 0 zu zählen: Bei text = "Lizenz" ist text[0] das "L" und text[1] das "i".
Das letzte Zeichen hat deshalb den Index len(text) - 1, hier text[5] mit dem
"z". text[6] gibt es nicht, das bricht mit einem IndexError ab.

Tipp: Sie haben die Länge schon in anzahl gespeichert und können sie für das
letzte Zeichen wiederverwenden.
"""

schluessel = input("Lizenzschlüssel: ")

anzahl = len(schluessel)
erstes = schluessel[0]
letztes = schluessel[anzahl - 1]

print("Der Schlüssel hat", anzahl, "Zeichen.")
print("Erstes Zeichen:", erstes)
print("Letztes Zeichen:", letztes)


# Idee: len(schluessel) liefert die Länge, schluessel[0] das erste Zeichen. Weil Python ab 0 zählt, hat
# das letzte Zeichen den Index anzahl - 1.
# Anderer Weg: schluessel[-1]; negative Indizes zählen von hinten (mehr dazu in Aufgabe 1_012).
# Typische Fehler: schluessel[1] für das erste Zeichen (das ist das zweite), schluessel[anzahl] für das
# letzte (IndexError, den Index gibt es nicht) oder ein fester Index wie schluessel[13], der nur bei
# Schlüsseln mit 14 Zeichen stimmt.
