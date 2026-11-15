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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def pruefziffer(nummer):
    """Gibt die letzte Stelle der Quersumme von nummer zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(ziffern(40715))
print(pruefziffer(40715))
