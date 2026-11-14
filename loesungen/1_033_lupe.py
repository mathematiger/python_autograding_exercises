# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_033_lupe.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_033_lupe

"""Aufgabe 1_033 – Bildschirmlupe                               Stufe 1 ★☆☆☆☆

Eine Anwendung soll auch für Menschen mit eingeschränktem Sehvermögen gut
nutzbar sein. Dafür hat sie eine Bildschirmlupe: Sie startet bei 100 %, und
jeder Klick auf „Vergrößern“ erhöht den Zoom um 25 Prozentpunkte. Das
Programm fragt, welche Vergrößerung jemand mindestens braucht, und zeigt,
welche Zoomstufen die Lupe nacheinander durchläuft, bis diese Vergrößerung
erreicht oder überschritten ist. Ergänzen Sie eine while-Schleife, die bei
jedem Durchlauf den Zoom um 25 erhöht, die Klicks mitzählt und die neue
Zoomstufe ausgibt. Bei Eingabe 140:

    Zoom: 125 %
    Zoom: 150 %
    Fertig nach 2 Klicks: 150 %

Ist die gewünschte Vergrößerung schon erreicht (Eingabe 100), braucht es
keinen Klick:

    Fertig nach 0 Klicks: 100 %

Grenzen: Die Eingabe ist eine ganze Zahl von 100 bis 1000.

Hintergrund: Eine for-Schleife wiederholt etwas, wenn man vorher weiß, wie
oft. Hier weiß man das nicht, man weiß nur, wann Schluss ist. Dafür gibt es
while: Solange die Bedingung hinter while wahr ist, wird der eingerückte
Block wiederholt; vor jedem Durchlauf prüft Python die Bedingung neu.

    while zoom < ziel:
        zoom = zoom + 25

Ist die Bedingung schon am Anfang falsch, läuft der Block kein einziges Mal.
Im Block muss sich etwas ändern, das in der Bedingung vorkommt, sonst endet
die Schleife nie (die Prüfung bricht dann nach 5 Sekunden ab).
"""

ziel = int(input("Gewünschte Vergrößerung in Prozent: "))
zoom = 100
klicks = 0

while zoom < ziel:
    zoom = zoom + 25
    klicks = klicks + 1
    print(f"Zoom: {zoom} %")

print(f"Fertig nach {klicks} Klicks: {zoom} %")


# Idee: Solange zoom kleiner als das Ziel ist, wird noch ein Klick gebraucht. In der Schleife wird zoom
# um 25 erhöht, klicks um 1 erhöht und die neue Stufe ausgegeben. Ist das Ziel erreicht oder
# überschritten, wird die Bedingung falsch, und die vorgegebene Schlusszeile erscheint einmal.
# Anderer Weg: Die Zahl der Klicks lässt sich auch ausrechnen: (ziel - 100 + 24) // 25. Dann braucht man
# für die Zwischenzeilen aber trotzdem eine Schleife, etwa for klick in range(1, klicks + 1).
# Typische Fehler: while zoom <= ziel (bei Eingabe 150 ein Klick zu viel, Ende bei 175 %), zoom oder
# klicks in der Schleife nicht erhöhen (Endlosschleife) oder die Schlusszeile in die Schleife
# einrücken (dann steht sie nach jedem Klick da und bei Eingabe 100 gar nicht).
