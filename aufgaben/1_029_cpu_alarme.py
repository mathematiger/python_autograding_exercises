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

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
for wert in messwerte:
    zahl = int(wert)
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"Alarme über {schwelle} %: {alarme}")
print(f"Das sind {len(alarme)} von {len(messwerte)} Messwerten.")
