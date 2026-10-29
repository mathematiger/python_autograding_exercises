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
    """Gibt True zurück, wenn zahl gerade ist, sonst False."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


for zahl in range(1, 5):
    print(zahl, ist_gerade(zahl))
