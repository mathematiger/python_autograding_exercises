# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_012_seriennummer.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_012_seriennummer

"""Aufgabe 1_012 – Seriennummer                                  Stufe 1 ★☆☆☆☆

In einer Fabrikhalle hängen viele kleine Sensoren, die Temperatur,
Luftfeuchte oder Bewegung messen und ihre Werte über das Netz melden. Jeder
Sensor hat eine Seriennummer wie TH-2024-4711-EU: vorn zwei Buchstaben für
den Gerätetyp (TH steht für Temperatur und Feuchte), dann das Baujahr, dann
die laufende Nummer und hinten zwei Buchstaben für die Region, für die das
Gerät zugelassen ist. Die laufende Nummer ist unterschiedlich lang, je
nachdem, wie viele Geräte schon gebaut wurden.

Das Programm fragt schon nach der Seriennummer und holt den Gerätetyp
heraus. Ergänzen Sie die drei Zeilen, die das Baujahr, die laufende Nummer
und die Region in die Variablen jahr, laufnummer und region schreiben. Bei
Eingabe TH-2024-4711-EU soll das Programm ausgeben:

    Gerätetyp: TH
    Baujahr: 2024
    Laufende Nummer: 4711
    Region: EU

Grenzen: Die Seriennummer hat immer die Form TT-JJJJ-N-RR: zwei Großbuchstaben,
ein Bindestrich, vier Ziffern, ein Bindestrich, die laufende Nummer aus 1 bis
10 Ziffern, ein Bindestrich und zwei Großbuchstaben.

Hintergrund: Mit text[a:b] schneidet man ein Stück aus einem Text heraus,
von Index a bis vor Index b; das nennt man Slicing. Bei text = "Sensor" ist
text[1:4] das Stück "ens". Lässt man a weg, beginnt das Stück am Anfang,
lässt man b weg, geht es bis zum Ende: text[:2] ist "Se", text[3:] ist
"sor". Negative Indizes zählen von hinten: text[-1] ist das letzte Zeichen
"r", text[-3:] sind die letzten drei Zeichen "sor", und text[1:-1] ist
alles außer dem ersten und dem letzten Zeichen, "enso". So kommt man an das
Ende eines Textes, ohne seine Länge zu kennen.

Tipp: Zählen Sie die Positionen bei TH-2024-4711-EU ab. Die laufende Nummer
beginnt immer am selben Index, endet aber immer drei Zeichen vor dem Ende.
"""

nummer = input("Seriennummer: ")
typ = nummer[:2]

jahr = nummer[3:7]
laufnummer = nummer[8:-3]
region = nummer[-2:]

print("Gerätetyp:", typ)
print("Baujahr:", jahr)
print("Laufende Nummer:", laufnummer)
print("Region:", region)


# Idee: Das Baujahr steht immer an den Indizes 3 bis 6, also nummer[3:7]. Die laufende Nummer beginnt
# immer bei Index 8, ist aber unterschiedlich lang; ihr Ende zählt man darum von hinten: nummer[8:-3]
# hört vor dem Bindestrich vor der Region auf. Die Region sind die letzten zwei Zeichen, nummer[-2:].
# Anderer Weg: nummer[len(nummer) - 2:] für die Region und nummer[8:len(nummer) - 3] für die laufende
# Nummer; das rechnet dieselben Indizes von vorn aus.
# Typische Fehler: feste Indizes wie nummer[8:12] und nummer[13:15], die nur bei vierstelligen laufenden
# Nummern stimmen, oder ein Slice, das den Bindestrich mitnimmt (nummer[7:-3] oder nummer[8:-2]).
