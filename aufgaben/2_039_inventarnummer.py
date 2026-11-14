"""Aufgabe 2_039 – Inventarnummer                               Stufe 2 ★★☆☆☆

Im Rechenzentrum klebt auf jedem Server ein Etikett mit einer
Inventarnummer. Damit Tippfehler beim Erfassen auffallen, ist die letzte
Ziffer eine Prüfziffer: Sie ist die letzte Ziffer der Quersumme aller
übrigen Ziffern. Bei der Nummer 47125 sind die übrigen Ziffern 4, 7, 1, 2;
ihre Quersumme ist 14, also muss die Prüfziffer 4 sein, und 47125 ist
falsch erfasst. Richtig wäre 47124.

Schreiben Sie zwei Funktionen:

- `quersumme(zahl)` liefert die Summe der Ziffern von zahl.
- `nummer_gueltig(nummer)` liefert True, wenn die letzte Ziffer von nummer
  die richtige Prüfziffer für die übrigen Ziffern ist, sonst False.
  Benutzen Sie dafür quersumme.

    quersumme(4712)         →  14
    quersumme(0)            →  0
    nummer_gueltig(47124)   →  True
    nummer_gueltig(47125)   →  False

Rechnen Sie nur mit Zahlen: ohne str(), ohne Umwandlung in Text.

Grenzen: 0 ≤ zahl ≤ 10**18 und 10 ≤ nummer ≤ 10**18, beides ganze Zahlen.

Hintergrund: Die Ziffern einer Zahl bekommt man mit // und % (Aufgabe 1_005):
zahl % 10 ist die letzte Ziffer, zahl // 10 ist die Zahl ohne ihre letzte
Ziffer. Wiederholt man das, bis die Zahl 0 ist, kommt jede Ziffer einmal
dran, von hinten nach vorn:

    4712 % 10 = 2     4712 // 10 = 471
     471 % 10 = 1      471 // 10 = 47
      47 % 10 = 7       47 // 10 = 4
       4 % 10 = 4        4 // 10 = 0   → fertig

Wie oft das passiert, weiß man vorher nicht; darum passt eine while-Schleife
(Aufgabe 2_004) mit der Bedingung zahl > 0.
"""


def quersumme(zahl):
    """Liefert die Summe der Ziffern von zahl."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def nummer_gueltig(nummer):
    """Prüft, ob die letzte Ziffer von nummer die Prüfziffer der übrigen Ziffern ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(quersumme(4712))
print(nummer_gueltig(47124))
