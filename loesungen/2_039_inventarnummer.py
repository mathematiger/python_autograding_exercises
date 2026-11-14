# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_039_inventarnummer.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_039_inventarnummer

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
    summe = 0
    while zahl > 0:
        summe = summe + zahl % 10
        zahl = zahl // 10
    return summe


def nummer_gueltig(nummer):
    """Prüft, ob die letzte Ziffer von nummer die Prüfziffer der übrigen Ziffern ist."""
    pruefziffer = nummer % 10
    rest = nummer // 10
    return quersumme(rest) % 10 == pruefziffer


print(quersumme(4712))
print(nummer_gueltig(47124))


# Idee: In quersumme die letzte Ziffer mit zahl % 10 abschneiden und addieren, dann mit zahl // 10
# ohne sie weitermachen, bis zahl 0 ist. In nummer_gueltig ist nummer % 10 die Prüfziffer und
# nummer // 10 der Rest; die Nummer ist gültig, wenn quersumme(rest) % 10 die Prüfziffer ergibt.
# Anderer Weg: sum(int(ziffer) for ziffer in str(zahl)) rechnet über den Text, war hier aber nicht erlaubt.
# Oder rekursiv: quersumme(zahl) = zahl % 10 + quersumme(zahl // 10), mit quersumme(0) = 0.
# Typische Fehler: while zahl % 10 > 0 (hört bei der ersten 0 auf, quersumme(10500) gibt 0),
# zahl / 10 statt zahl // 10 (Kommazahlen, die Schleife läuft sehr lange und rechnet falsch),
# die ganze Quersumme statt ihrer letzten Ziffer mit der Prüfziffer vergleichen.
