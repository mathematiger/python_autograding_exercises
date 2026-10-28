"""Aufgabe 2_003 – Gerade oder ungerade?                         Stufe 2 ★★☆☆☆

Vervollständigen Sie die Funktion `ist_gerade`. Sie soll True zurückgeben, wenn die
Zahl gerade ist, sonst False.

    ist_gerade(4)  →  True
    ist_gerade(7)  →  False

Grenzen: zahl ist eine ganze Zahl mit -10**9 ≤ zahl ≤ 10**9, auch 0 und
negative Zahlen kommen vor.

Tipp: zahl % 2 ist der Rest beim Teilen durch 2.
"""


def ist_gerade(zahl):
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


for zahl in range(1, 5):
    print(zahl, ist_gerade(zahl))
