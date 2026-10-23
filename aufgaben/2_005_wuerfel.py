"""Aufgabe 2_005 – Bauklotz-Würfel                              Stufe 2 ★★☆☆☆

Ein Kindergarten hat eine Kiste voller gleich großer Bauklötze. Die Kinder
wollen daraus einen großen, vollen Würfel bauen, ohne dass ein Klotz übrig
bleibt. Ein Würfel mit Kantenlänge 3 braucht 3 * 3 * 3 = 27 Klötze.
Vervollständigen Sie die Funktion `kantenlaenge`, die zu einer Anzahl von
Klötzen die Kantenlänge des Würfels liefert. Geht es nicht auf, soll -1
zurückkommen.

    kantenlaenge(27)  →  3
    kantenlaenge(64)  →  4
    kantenlaenge(30)  →  -1
    kantenlaenge(0)   →  0

Hintergrund: Für viele Fragen gibt es keine fertige Formel, aber man kann die
Antwort raten und prüfen („guess and check“, MIT 6.0001 Lecture 3). Man
probiert der Reihe nach k = 0, 1, 2, … und hört beim ersten k auf, das die
gesuchte Eigenschaft hat. Hier ist das die kleinste Zahl k mit
k * k * k >= anzahl. Danach prüft man, ob es genau passt (k * k * k == anzahl)
oder ob man schon darüber hinaus ist. Weil man bei 0 anfängt und in Einerschritten
zählt, findet man garantiert die kleinste passende Zahl.

Tipp: Eine while-Schleife mit der Bedingung k * k * k < anzahl zählt k so lange
hoch, bis der Würfel groß genug ist.
"""


def kantenlaenge(anzahl):
    """Gibt die Kantenlänge des Würfels aus anzahl Klötzen zurück, sonst -1."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(kantenlaenge(27))
