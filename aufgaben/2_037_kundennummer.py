"""Aufgabe 2_037 – Kundennummer                                  Stufe 2 ★★☆☆☆

Im Bestellformular eines Onlineshops tippen Firmenkunden ihre Kundennummer
ein. Damit ein Tippfehler auffällt, bevor die Bestellung beim falschen
Kunden landet, ist die letzte Ziffer jeder Kundennummer eine Prüfziffer:
die Quersumme aller anderen Ziffern, davon nur die letzte Stelle (also die
Quersumme % 10). Stimmt sie nicht, zeigt das Formular sofort einen Hinweis
neben dem Eingabefeld an.

Beispiel 48153: Die Ziffern vor der letzten sind 4, 8, 1 und 5, ihre
Quersumme ist 18, die Prüfziffer also 8. Die letzte Ziffer ist aber 3, die
Nummer ist falsch. Richtig wäre 48158.

Vervollständigen Sie zwei Funktionen:

- `quersumme(zahl)` gibt die Summe der Ziffern von zahl zurück.
- `ist_gueltig(nummer)` gibt True zurück, wenn die letzte Ziffer von
  nummer die Prüfziffer der übrigen Ziffern ist, sonst False. Benutzen Sie
  dafür quersumme.

    quersumme(48153)    →  21
    quersumme(7)        →  7
    quersumme(0)        →  0
    ist_gueltig(48158)  →  True
    ist_gueltig(48153)  →  False
    ist_gueltig(10)     →  False

Rechnen Sie nur mit // und %, ohne die Zahl mit str(...) in einen Text
umzuwandeln.

Grenzen: Für quersumme ist 0 ≤ zahl ≤ 10**18. Für ist_gueltig ist
10 ≤ nummer ≤ 10**12, die Nummer hat also mindestens zwei Ziffern.

Hintergrund: Die Ziffern einer ganzen Zahl bekommt man ohne Text mit zwei
Rechenzeichen aus Aufgabe 1_005: zahl % 10 ist die letzte Ziffer, und
zahl // 10 ist die Zahl ohne ihre letzte Ziffer. Bei 481 ist 481 % 10 = 1
und 481 // 10 = 48. Wiederholt man das in einer while-Schleife (Aufgabe
2_004), bis die Zahl 0 ist, kommt jede Ziffer genau einmal dran, von
hinten nach vorn:

    while zahl > 0:
        ziffer = zahl % 10
        ...
        zahl = zahl // 10

Bei zahl = 0 läuft die Schleife gar nicht; das passt, denn die Quersumme
von 0 ist 0.
"""


def quersumme(zahl):
    """Gibt die Summe der Ziffern von zahl zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ist_gueltig(nummer):
    """Prüft, ob die letzte Ziffer von nummer die Prüfziffer der übrigen Ziffern ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(quersumme(48153))
print(ist_gueltig(48158))
