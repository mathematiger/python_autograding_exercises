"""Aufgabe 3_001 – Lineare Suche                                 Stufe 3 ★★★☆☆

In einer Bibliothek stehen die Buchnummern der Regalreihe in einer Liste, in der
Reihenfolge, wie die Bücher im Regal stehen. Vervollständigen Sie die Funktion
`finde`, die die Position (den Index) einer gesuchten Buchnummer liefert. Steht
das Buch nicht im Regal, soll -1 zurückkommen. Kommt die Nummer mehrmals vor,
zählt das erste Vorkommen.

    finde([41, 7, 23, 7], 23)  →  2
    finde([41, 7, 23, 7], 7)   →  1
    finde([41, 7, 23, 7], 99)  →  -1
    finde([], 5)               →  -1

Benutzen Sie dafür eine Schleife und nicht die fertige Methode liste.index(...).

Hintergrund: Das hier ist die lineare Suche, der einfachste Suchalgorithmus:
Man geht die Liste von vorn nach hinten durch und vergleicht jedes Element mit
dem gesuchten Wert. Sobald es passt, ist man fertig und gibt den Index zurück.
Ist man am Ende angekommen, ohne etwas zu finden, gibt es den Wert nicht. Im
schlechtesten Fall schaut man sich alle n Elemente an; man sagt, die Suche hat
die Laufzeit O(n), sie wächst linear mit der Länge der Liste. Bei sortierten
Listen geht es schneller, das kommt in einer späteren Aufgabe.

Tipp: for index in range(len(liste)) liefert nacheinander alle Indizes. Ein
return innerhalb der Schleife beendet die Funktion sofort.
"""


def finde(liste, gesucht):
    """Gibt den Index des ersten Vorkommens von gesucht zurück, sonst -1."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(finde([41, 7, 23, 7], 23))
