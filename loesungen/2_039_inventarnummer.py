# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_039_inventarnummer.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_039_inventarnummer

"""Aufgabe 2_039 – Inventarnummer                                Stufe 2 ★★☆☆☆

Im Rechenzentrum hat jeder Server, jeder Switch und jede USV (unterbrechungsfreie
Stromversorgung) eine Inventarnummer, die auf einem Aufkleber am Gehäuse steht.
Damit sich beim Abtippen kein Fehler einschleicht, hängt die Inventarverwaltung
eine Prüfziffer an: die Quersumme der Nummer (die Summe ihrer Ziffern), davon
nur die letzte Stelle. Schreiben Sie zwei Funktionen:

- `ziffern(nummer)` gibt die Liste der Ziffern von nummer zurück, von vorn nach
  hinten gelesen.
- `pruefziffer(nummer)` gibt die letzte Stelle der Quersumme zurück, also eine
  Zahl von 0 bis 9. Verwenden Sie dafür Ihre Funktion ziffern.

    ziffern(40715)      →  [4, 0, 7, 1, 5]
    pruefziffer(40715)  →  7        (4 + 0 + 7 + 1 + 5 = 17)
    ziffern(0)          →  [0]
    pruefziffer(0)      →  0

Rechnen Sie mit // und %, ohne die Zahl mit str(...) in einen Text umzuwandeln.

Grenzen: nummer ist eine ganze Zahl mit 0 ≤ nummer ≤ 10**18.

Hintergrund: Teilt man eine ganze Zahl mit // durch 10, fällt die letzte Ziffer
weg; der Rest mit % 10 ist genau diese letzte Ziffer (Aufgabe 1_005):

    40715 % 10   →  5
    40715 // 10  →  4071

Wiederholt man das in einer while-Schleife (Aufgabe 2_004), bis die Zahl 0 ist,
bekommt man alle Ziffern, allerdings von hinten nach vorn. Man fügt jede neue
Ziffer deshalb vorn an (liste.insert(0, ziffer)) oder dreht die Liste am Ende um
(liste.reverse()). Die Zahl 0 ist ein Sonderfall: Bei ihr endet die Schleife
sofort, sie hat aber trotzdem eine Ziffer.
"""


def ziffern(nummer):
    """Gibt die Ziffern von nummer als Liste zurück, von vorn nach hinten."""
    if nummer == 0:
        return [0]
    ergebnis = []
    while nummer > 0:
        ergebnis.insert(0, nummer % 10)
        nummer = nummer // 10
    return ergebnis


def pruefziffer(nummer):
    """Gibt die letzte Stelle der Quersumme von nummer zurück."""
    return sum(ziffern(nummer)) % 10


print(ziffern(40715))
print(pruefziffer(40715))


# Idee: nummer % 10 liefert die letzte Ziffer, nummer // 10 schneidet sie ab. In einer while-Schleife wird
# das wiederholt, bis nummer 0 ist; jede Ziffer kommt mit insert(0, …) vorn in die Liste, damit die
# Reihenfolge stimmt. Die 0 wird vorher gesondert behandelt. pruefziffer summiert die Liste und nimmt % 10.
#
# Anderer Weg: Die Ziffern mit append hinten anhängen und die Liste am Ende mit reverse() umdrehen, oder
# rekursiv: ziffern(nummer // 10) + [nummer % 10] für nummer >= 10. Mit Text ginge es als
# [int(z) for z in str(nummer)], das sollte hier aber gerade nicht benutzt werden.
#
# Typische Fehler: append ohne Umdrehen (Ziffern verkehrt herum), die 0 vergessen (leere Liste),
# nummer / 10 statt nummer // 10 (Kommazahlen, die Schleife endet erst nach über 300 Durchläufen mit
# Unsinn) oder in pruefziffer die ganze Quersumme statt ihrer letzten Stelle zurückgeben.
