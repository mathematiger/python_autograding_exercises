"""Aufgabe 1_024 – Rack belegen                                  Stufe 1 ★☆☆☆☆

Im Rechenzentrum werden Server in Racks eingebaut, hohe Schränke mit
genormten Einschüben. Die Höhe eines Racks wird in Höheneinheiten (HE)
gemessen; die HE sind von unten nach oben durchnummeriert, die unterste
ist HE 1. Ein neues Rack soll mit Servern gefüllt werden, die jeweils
zwei HE hoch sind. Für die Dokumentation entsteht vorher ein
Belegungsplan, der von oben nach unten gelesen wird, so wie man vor dem
Rack steht. (Eingebaut wird später von unten nach oben, schwere Geräte
zuerst, damit das Rack nicht kopflastig wird.) Das Programm fragt schon
nach der Höhe des Racks. Ergänzen Sie eine for-Schleife, die von oben
nach unten für jeden Server ausgibt, welche beiden HE er belegt, die
untere zuerst. Bei Eingabe 6:

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

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"{hoehe // 2} Server passen in das Rack.")
