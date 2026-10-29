# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_003_gerade.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_003_gerade

"""Aufgabe 2_003 – Gerade oder ungerade?                         Stufe 2 ★★☆☆☆

Auf einem Switch gehören die Ports mit gerader Nummer zum Verwaltungsnetz.
Vervollständigen Sie die Funktion ist_gerade. Die Funktion soll True
zurückgeben, wenn die Zahl gerade ist, sonst False.

    ist_gerade(4)  →  True
    ist_gerade(7)  →  False

Grenzen: zahl ist eine ganze Zahl mit -10**9 ≤ zahl ≤ 10**9, auch 0 und
negative Zahlen kommen vor.

Hintergrund: if bedingung: führt den eingerückten Block darunter nur aus, wenn
die Bedingung wahr ist. a == b vergleicht zwei Werte und liefert True oder
False (ein einzelnes = speichert dagegen einen Wert). Ein return beendet die
Funktion sofort; ein return dahinter gilt also für alle anderen Fälle. True und
False sind Wahrheitswerte, keine Texte, und stehen ohne Anführungszeichen.

Tipp: zahl % 2 ist der Rest beim Teilen durch 2.
"""


def ist_gerade(zahl):
    if zahl % 2 == 0:
        return True
    return False


for zahl in range(1, 5):
    print(zahl, ist_gerade(zahl))


# Idee: Eine Zahl ist gerade, wenn beim Teilen durch 2 kein Rest bleibt, also
# zahl % 2 == 0. Das if gibt in diesem Fall True zurück, sonst geht es weiter zum
# return False.
#
# Anderer Weg: Der Vergleich zahl % 2 == 0 ist schon True oder False, deshalb
# reicht return zahl % 2 == 0 ohne if. Das ist kürzer und in der Praxis üblich;
# hier soll aber das if geübt werden.
#
# Typische Fehler: zahl / 2 == 0 statt zahl % 2 == 0 prüft, ob die Zahl 0 ist,
# nicht ob sie gerade ist. Wer "True" in Anführungszeichen zurückgibt, liefert
# einen Text statt eines Wahrheitswerts. Negative Zahlen brauchen keinen
# Sonderfall: In Python ist -3 % 2 gleich 1 und -4 % 2 gleich 0.
