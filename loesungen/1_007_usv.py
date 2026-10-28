# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_007_usv.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_007_usv

"""Aufgabe 1_007 – USV-Laufzeit                                  Stufe 1 ★☆☆☆☆

Im Serverraum hängen die Server an einer USV, einer unterbrechungsfreien
Stromversorgung. Fällt der Strom aus, liefert ihr Akku noch eine Weile
Energie, damit die Server sauber herunterfahren können. Der Akku speichert
eine Energie in Wattstunden (Wh), die Server ziehen zusammen eine Leistung in
Watt (W). Das Programm fragt schon nach beiden Werten und berechnet die
Laufzeit in Minuten. Geben Sie die Laufzeit auf ganze Minuten gerundet aus und
in einer zweiten Zeile in Stunden mit einer Nachkommastelle. Bei Eingabe 1000
und 450 soll das Programm ausgeben:

    Die USV hält etwa 133 Minuten.
    Das sind etwa 2.2 Stunden.

Grenzen: Energie und Leistung sind ganze Zahlen zwischen 1 und 10 000.

Hintergrund: Bei Divisionen entstehen oft lange Kommazahlen wie
133.33333333333334. Die Funktion round rundet sie: round(133.33) ergibt die
ganze Zahl 133 (Typ int), round(2.2222, 1) ergibt die Kommazahl 2.2 (Typ
float) mit einer Nachkommastelle. Vorsicht bei int(...): int(85.71) schneidet
die Nachkommastellen einfach ab und ergibt 85, während round(85.71) richtig
auf 86 rundet.

Tipp: print("Die USV hält etwa", ..., "Minuten.") setzt zwischen die Teile
automatisch ein Leerzeichen. Eine Stunde hat 60 Minuten.
"""

energie = float(input("Energie des Akkus in Wh: "))
leistung = float(input("Leistung der Server in W: "))
minuten = energie / leistung * 60

print("Die USV hält etwa", round(minuten), "Minuten.")
print("Das sind etwa", round(minuten / 60, 1), "Stunden.")


# Idee: round(minuten) rundet auf eine ganze Zahl, round(minuten / 60, 1) rechnet erst in Stunden um und
# rundet dann auf eine Nachkommastelle. Beides kann direkt in print stehen.
# Anderer Weg: die gerundeten Werte erst in eigenen Variablen speichern und dann ausgeben, oder die
# Stunden als round(energie / leistung, 1) ausrechnen, das ist dieselbe Zahl.
# Typische Fehler: int(minuten) statt round(minuten) (schneidet nur ab: 85 statt 86), round(minuten, 0)
# (liefert 144.0 statt 144) oder erst runden und dann teilen: round(minuten) / 60 hat wieder viele
# Nachkommastellen.
