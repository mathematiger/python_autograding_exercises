"""Aufgabe 1_018 – Bewässerung                                   Stufe 1 ★☆☆☆☆

Auf dem Dach eines Bürogebäudes wachsen Pflanzen, die ein kleiner
Mikrocontroller automatisch gießt. Ein Sensor in der Erde misst die
Bodenfeuchte in Prozent (0 heißt ganz trocken, 100 ganz nass). Der
Controller entscheidet nach jeder Messung, ob das Wasserventil, ein
Aktor, geöffnet oder geschlossen wird: Liegt die Feuchte unter dem
Grenzwert 30, öffnet er das Ventil, sonst schließt er es.

Das Programm fragt schon nach der gemessenen Feuchte. Ergänzen Sie die
Entscheidung: Ist die Feuchte kleiner als grenzwert, soll „Ventil: offen“
ausgegeben werden, sonst „Ventil: zu“. Bei Eingabe 25:

    Feuchte: 25 Prozent
    Ventil: offen
    Nächste Messung in 10 Minuten.

Bei Eingabe 45:

    Feuchte: 45 Prozent
    Ventil: zu
    Nächste Messung in 10 Minuten.

Grenzen: Die Feuchte ist eine ganze Zahl von 0 bis 100.

Hintergrund: Mit else bekommt ein if einen zweiten Fall: Der Block unter
if läuft, wenn die Bedingung wahr ist, der Block unter else, wenn sie
falsch ist. Es läuft also immer genau einer der beiden Blöcke. else steht
genauso weit links wie das zugehörige if und hat keine eigene Bedingung,
nur einen Doppelpunkt:

    if punkte >= 50:
        print("bestanden")
    else:
        print("nicht bestanden")
"""

grenzwert = 30
feuchte = int(input("Bodenfeuchte in Prozent: "))
print("Feuchte:", feuchte, "Prozent")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print("Nächste Messung in 10 Minuten.")
