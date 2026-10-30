# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_018_bewaesserung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_018_bewaesserung

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

if feuchte < grenzwert:
    print("Ventil: offen")
else:
    print("Ventil: zu")

print("Nächste Messung in 10 Minuten.")


# Idee: if feuchte < grenzwert: entscheidet zwischen den beiden Fällen. Darunter eingerückt steht
# print("Ventil: offen"), unter else: steht print("Ventil: zu"). Es läuft immer genau einer der
# beiden Blöcke.
# Anderer Weg: die Bedingung umdrehen, also if feuchte >= grenzwert: zuerst „Ventil: zu“ und unter
# else „Ventil: offen“. Statt grenzwert kann auch direkt 30 dastehen; mit der Variablen muss man
# den Wert aber nur an einer Stelle ändern.
# Typische Fehler: <= statt < (dann öffnet das Ventil schon bei genau 30 Prozent), else mit einer
# eigenen Bedingung (else feuchte >= 30: ist ein SyntaxError) oder else weiter einrücken als if.
