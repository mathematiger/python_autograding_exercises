"""Aufgabe 2_002 – Verdoppeln                                   Stufe 2 ★★☆☆☆

Auf einem gespiegelten Speicher (RAID 1) liegt jede Datei auf zwei Platten
und belegt deshalb doppelt so viel Platz. Vervollständigen Sie die Funktion
verdopple. Die Funktion bekommt eine Zahl, etwa die Dateigröße, und soll das
Doppelte davon zurückgeben (mit return, nicht mit print!).

    verdopple(21)  →  42

Grenzen: zahl ist eine ganze Zahl mit -10**9 ≤ zahl ≤ 10**9. Die Funktion
soll für jede ganze Zahl funktionieren, nicht nur für Dateigrößen.

Hintergrund: Eine Funktion ist ein benannter Block. Die Zeile
def verdopple(zahl): legt sie an, mit ihrem Namen und dem Parameter in
Klammern; der eingerückte Block darunter ist ihr Rumpf. Man ruft sie mit
verdopple(21) auf; der Wert in der Klammer landet im Parameter zahl. return
gibt das Ergebnis an die Stelle des Aufrufs zurück und beendet die Funktion.
Dort kann man es speichern, damit weiterrechnen oder ausgeben. Benutzt die
Funktion print statt return, zeigt sie den Wert nur an und liefert None,
den Wert für „nichts“.
"""


def verdopple(zahl):
    """Gibt das Doppelte von zahl zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(verdopple(21))
