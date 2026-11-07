# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_029_cpu_alarme.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_029_cpu_alarme

"""Aufgabe 1_029 – CPU-Alarme                                    Stufe 1 ★☆☆☆☆

Ein Überwachungsprogramm (Monitoring) misst jede Minute die Auslastung
des Prozessors (CPU) eines Servers in Prozent. Liegt ein Messwert über
einem Schwellwert, soll er in einer Alarmliste landen, damit die
Administratorin sofort sieht, welche Werte zu hoch waren. Das Programm
fragt nach den Messwerten, durch Kommas getrennt, und nach dem
Schwellwert. Ergänzen Sie zwei Stellen: Legen Sie vor der Schleife eine
leere Liste alarme an. Hängen Sie in der Schleife jede zahl, die größer
als der Schwellwert ist, mit append an alarme an. Ein Wert, der genau
gleich dem Schwellwert ist, löst keinen Alarm aus. Bei den Eingaben
45,91,78,85,80,97,60 und 80:

    Alarme über 80 %: [91, 85, 97]
    Das sind 3 von 7 Messwerten.

Grenzen: Es gibt 1 bis 30 Messwerte, jeder ist eine ganze Zahl von 0
bis 100. Der Schwellwert ist eine ganze Zahl von 0 bis 100.

Hintergrund: Oft weiß man vorher nicht, wie viele Elemente eine Liste
bekommt. Dann legt man zuerst eine leere Liste an, liste = [], und
hängt in einer Schleife mit liste.append(wert) jeweils einen Wert
hinten an. append ist eine Methode der Liste: Sie wird mit einem Punkt
hinter dem Namen der Liste aufgerufen und verändert genau diese Liste.
Nach werte = [] und werte.append(4) und werte.append(7) ist werte
gleich [4, 7]. Die leere Liste muss vor der Schleife stehen; stünde
sie in der Schleife, finge die Liste bei jedem Durchlauf wieder leer
an.
"""

eingabe = input("Messwerte in Prozent, durch Kommas getrennt: ")
messwerte = eingabe.split(",")
schwelle = int(input("Schwellwert in Prozent: "))

alarme = []
for wert in messwerte:
    zahl = int(wert)
    if zahl > schwelle:
        alarme.append(zahl)

print(f"Alarme über {schwelle} %: {alarme}")
print(f"Das sind {len(alarme)} von {len(messwerte)} Messwerten.")


# Idee: alarme = [] legt vor der Schleife eine leere Liste an. In der Schleife prüft ein if, ob zahl größer
# als schwelle ist, und alarme.append(zahl) hängt den Wert dann hinten an. So steht am Ende jeder zu hohe
# Wert genau einmal in der Liste, in der Reihenfolge der Messung.
# Anderer Weg: alarme = alarme + [zahl] hängt ebenfalls an, baut dabei aber jedes Mal eine neue Liste.
# append verändert die vorhandene Liste und ist der übliche Weg.
# Typische Fehler: alarme = [] in die Schleife schreiben (dann bleibt nur der letzte Wert übrig), >= statt >
# (dann löst auch der Schwellwert selbst Alarm aus), wert statt zahl anhängen (dann stehen Texte wie '91'
# in der Liste) oder alarme = alarme.append(zahl) (append gibt nichts zurück, danach ist alarme None).
