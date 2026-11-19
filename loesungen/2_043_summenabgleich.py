# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_043_summenabgleich.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_043_summenabgleich

"""Aufgabe 2_043 – Summenabgleich                                Stufe 2 ★★☆☆☆

Ein Onlinehändler zieht jede Nacht die Bestellungen aus der Datenbank in
ein Auswertungssystem um. Danach prüft ein Skript die Datenqualität: Zu
jeder Bestellung sind die Preise der einzelnen Positionen gespeichert und
zusätzlich der Gesamtbetrag. Passt beides nicht zusammen, ist beim Umzug
etwas schiefgegangen. Bisher meldet das Skript aber auch bei vielen
richtigen Bestellungen einen Fehler, denn es vergleicht mit ==.

Vervollständigen Sie die Funktion `summe_passt(positionen, gesamt)`. Sie
gibt True zurück, wenn die Summe der Positionen und der Gesamtbetrag
weniger als TOLERANZ (0.001 Euro) voneinander abweichen, egal in welche
Richtung, sonst False.

    summe_passt([0.1, 0.2], 0.3)        →  True    (obwohl 0.1 + 0.2 == 0.3 False ist)
    summe_passt([19.99, 5.01], 25.0)    →  True
    summe_passt([10.0, 5.5], 15.6)      →  False
    summe_passt([], 0)                  →  True

Grenzen: 0 ≤ len(positionen) ≤ 10 000. Jeder Preis und der Gesamtbetrag
sind Zahlen (int oder float) von 0 bis 100 000 mit höchstens zwei
Nachkommastellen. Zwei verschiedene Beträge unterscheiden sich darum um
mindestens 0.01 Euro.

Hintergrund: Kommazahlen (float) speichert der Rechner im Zweiersystem,
und dort haben Zahlen wie 0.1 so wenig eine endliche Darstellung wie
1/3 im Zehnersystem (0.333…). Gespeichert wird die nächstgelegene Zahl,
die passt; der kleine Rest fällt beim Rechnen manchmal auf:

    0.1 + 0.2           →  0.30000000000000004
    0.1 + 0.2 == 0.3    →  False

Kommazahlen vergleicht man deshalb nie mit ==, sondern fragt, ob ihr
Abstand kleiner als eine kleine Schranke ist, oft epsilon genannt (hier
TOLERANZ). Den Abstand liefert abs(a - b), der Betrag des Unterschieds,
egal welche Zahl größer ist:

    abs(0.1 + 0.2 - 0.3) < 0.001    →  True
"""

TOLERANZ = 0.001


def summe_passt(positionen, gesamt):
    """Prüft, ob die Summe der Positionen bis auf TOLERANZ gleich dem Gesamtbetrag ist."""
    summe = 0
    for preis in positionen:
        summe = summe + preis
    return abs(summe - gesamt) < TOLERANZ


print(summe_passt([0.1, 0.2], 0.3))


# Idee: Die Preise in einer Schleife aufsummieren und dann den Abstand zwischen Summe und
# Gesamtbetrag mit abs(summe - gesamt) bilden. Ist er kleiner als TOLERANZ, gelten beide als gleich.
# Der Vergleich liefert schon True oder False und kann direkt mit return zurückgegeben werden.
# Anderer Weg: return abs(sum(positionen) - gesamt) < TOLERANZ mit der eingebauten Funktion sum.
# Bei Geldbeträgen kann man auch in Cent rechnen: round(preis * 100) macht aus jedem Preis eine
# ganze Zahl, und ganze Zahlen darf man mit == vergleichen. Später lernen Sie das Modul decimal
# kennen, das Dezimalzahlen exakt speichert.
# Typische Fehler: mit == vergleichen; abs vergessen (dann passt jeder zu große Gesamtbetrag,
# weil summe - gesamt negativ und damit kleiner als TOLERANZ ist); if ...: return True ohne ein
# return False für den anderen Fall (dann kommt None zurück).
