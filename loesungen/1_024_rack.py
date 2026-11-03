# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_024_rack.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_024_rack

"""Aufgabe 1_024 – Rack belegen                                  Stufe 1 ★☆☆☆☆

Im Rechenzentrum werden Server in Racks eingebaut, hohe Schränke mit
genormten Einschüben. Die Höhe eines Racks wird in Höheneinheiten (HE)
gemessen; die HE sind von unten nach oben durchnummeriert, die unterste
ist HE 1. Ein neues Rack soll mit Servern gefüllt werden, die jeweils
zwei HE hoch sind. Eingebaut wird von oben nach unten, damit unten Platz
für die schwere USV bleibt. Das Programm fragt schon nach der Höhe des
Racks. Ergänzen Sie eine for-Schleife, die von oben nach unten für jeden
Server ausgibt, welche beiden HE er belegt, die untere zuerst. Bei
Eingabe 6:

    Server in HE 5 und 6
    Server in HE 3 und 4
    Server in HE 1 und 2
    3 Server passen in das Rack.

Bei einer ungeraden Höhe bleibt unten eine HE frei. Bei Eingabe 7:

    Server in HE 6 und 7
    Server in HE 4 und 5
    Server in HE 2 und 3
    3 Server passen in das Rack.

Grenzen: Die Höhe ist eine ganze Zahl von 2 bis 48.

Hintergrund: range kann eine dritte Zahl bekommen, die Schrittweite:
range(a, b, schritt) beginnt bei a und zählt immer um schritt weiter,
solange b noch nicht erreicht ist. range(1, 10, 3) liefert 1, 4 und 7.
Mit einer negativen Schrittweite zählt range rückwärts, dann muss a
größer als b sein: range(10, 0, -2) liefert 10, 8, 6, 4 und 2. Wie
immer ist b selbst nicht mehr dabei.
"""

hoehe = int(input("Höhe des Racks in HE: "))

for unten in range(hoehe - 1, 0, -2):
    print(f"Server in HE {unten} und {unten + 1}")

print(f"{hoehe // 2} Server passen in das Rack.")


# Idee: Die Schleifenvariable ist die untere HE jedes Servers. Der oberste Server belegt hoehe - 1 und
# hoehe, der nächste zwei HE tiefer. range(hoehe - 1, 0, -2) zählt also von hoehe - 1 in Zweierschritten
# rückwärts, solange die Zahl noch größer als 0 ist. Bei ungerader Höhe endet sie bei 2, HE 1 bleibt frei.
# Anderer Weg: Die obere HE laufen lassen, range(hoehe, 1, -2), und unten - 1 ausgeben. Oder vorwärts
# zählen, range(hoehe // 2), und die HE ausrechnen: hoehe - 1 - 2 * nummer.
# Typische Fehler: range(hoehe, 0, -2) als untere HE (dann ragt der oberste Server über das Rack hinaus),
# Ende -1 statt 0 (dann kommt bei ungerader Höhe ein Server in HE 0 und 1 dazu) oder vorwärts mit
# range(1, hoehe, 2) zählen (falsche Reihenfolge, bei ungerader Höhe bleibt oben statt unten frei).
