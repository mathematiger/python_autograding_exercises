# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_005_wuerfel.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_005_wuerfel

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

Grenzen: anzahl ist eine ganze Zahl mit 0 ≤ anzahl ≤ 10**6.

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
    k = 0
    while k * k * k < anzahl:
        k = k + 1
    if k * k * k == anzahl:
        return k
    return -1


print(kantenlaenge(27))


# Idee: k beginnt bei 0 und wird erhöht, solange k * k * k kleiner als anzahl
# ist. Danach ist k die kleinste Zahl, deren Würfel mindestens anzahl Klötze
# braucht. Ist k * k * k genau anzahl, ist k die Kantenlänge, sonst geht es
# nicht auf.
#
# Anderer Weg: for k in range(anzahl + 1) mit return k, sobald k * k * k == anzahl
# ist, und return -1 nach der Schleife. Das ist auch richtig, probiert aber bei
# Zahlen, die keine Würfelzahl sind, alle k bis anzahl durch, statt beim ersten
# zu großen Würfel aufzuhören. Mit round(anzahl ** (1 / 3)) geht es ohne Raten,
# aber nur mit anschließender Probe, weil Kommazahlen ungenau sind.
#
# Typische Fehler: bei k = 1 statt 0 anfangen (dann ist kantenlaenge(0) falsch)
# oder nach der Schleife nicht prüfen, ob es genau passt.
