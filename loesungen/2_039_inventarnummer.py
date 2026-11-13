# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_039_inventarnummer.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_039_inventarnummer

"""Aufgabe 2_039 – Inventarnummer                                Stufe 2 ★★☆☆☆

Jeder Server im Rechenzentrum trägt ein Etikett mit einer Inventarnummer.
Damit ein Zahlendreher beim Abtippen auffällt, ist die letzte Ziffer eine
Prüfziffer: Sie ist die letzte Ziffer der Quersumme aller übrigen Ziffern.
Die Quersumme ist die Summe aller Ziffern einer Zahl. Bei der Nummer 47113
ist die Quersumme von 4711 gleich 4 + 7 + 1 + 1 = 13, die Prüfziffer also 3.

Vervollständigen Sie zwei Funktionen:

- `quersumme(zahl)` liefert die Summe der Ziffern von zahl.
- `pruefziffer_stimmt(nummer)` liefert True, wenn die letzte Ziffer von
  nummer die Prüfziffer der übrigen Ziffern ist, sonst False. Benutzen
  Sie dafür quersumme.

    quersumme(4711)              →  13
    quersumme(0)                 →  0
    pruefziffer_stimmt(47113)    →  True
    pruefziffer_stimmt(47118)    →  False

Rechnen Sie nur mit // und %, ohne die Zahl mit str(...) in einen Text
umzuwandeln.

Grenzen: zahl ist eine ganze Zahl mit 0 ≤ zahl ≤ 10**18, nummer eine ganze
Zahl mit 10 ≤ nummer ≤ 10**18.

Hintergrund: Mit // und % kommt man an die Ziffern einer Zahl heran, ohne
sie in einen Text zu verwandeln (Aufgabe 1_005). Im Zehnersystem ist zahl %
10 der Rest beim Teilen durch 10, also genau die letzte Ziffer, und zahl //
10 ist die Zahl ohne ihre letzte Ziffer:

    4711 % 10   →  1
    4711 // 10  →  471

Wiederholt man das in einer while-Schleife (Aufgabe 2_004), bis die Zahl 0
geworden ist, bekommt man alle Ziffern von hinten nach vorn: 1, 1, 7, 4.
Die Schleife läuft so oft, wie die Zahl Ziffern hat. Für 0 läuft sie gar
nicht, und das passt: Die Quersumme von 0 ist 0.
"""


def quersumme(zahl):
    """Summe der Ziffern von zahl."""
    summe = 0
    while zahl > 0:
        summe = summe + zahl % 10
        zahl = zahl // 10
    return summe


def pruefziffer_stimmt(nummer):
    """True, wenn die letzte Ziffer von nummer die letzte Ziffer der Quersumme der übrigen Ziffern ist."""
    return nummer % 10 == quersumme(nummer // 10) % 10


print(quersumme(4711))
print(pruefziffer_stimmt(47113))


# Idee: In einer while-Schleife, solange zahl > 0 ist, die letzte Ziffer zahl % 10 zur Summe addieren und
# sie mit zahl = zahl // 10 abschneiden. Für die Prüfziffer ist nummer % 10 die letzte Ziffer und
# nummer // 10 der Rest der Nummer; die beiden passen, wenn nummer % 10 == quersumme(nummer // 10) % 10.
# Anderer Weg: divmod(zahl, 10) liefert Rest und Ganzzahlquotient auf einmal. Oder rekursiv:
# quersumme(zahl) = zahl % 10 + quersumme(zahl // 10), mit 0 als Abbruch. Über den Text ginge es mit
# sum(int(z) for z in str(zahl)), das war hier nicht erlaubt.
# Typische Fehler: zahl / 10 statt zahl // 10 (Kommazahlen, die Schleife endet erst sehr spät), die
# Prüfziffer in die Quersumme einrechnen oder die ganze Quersumme statt ihrer letzten Ziffer vergleichen.
