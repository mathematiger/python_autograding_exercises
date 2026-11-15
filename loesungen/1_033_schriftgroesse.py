# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_033_schriftgroesse.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_033_schriftgroesse

"""Aufgabe 1_033 – Schriftgröße                                  Stufe 1 ★☆☆☆☆

Eine Webanwendung soll auch für Menschen mit einer Sehschwäche gut
lesbar sein. Dafür gibt es oben rechts die Taste „A+“: Jeder Klick
vergrößert die Schrift um 2 Pixel. Die Vorgabe für die Barrierefreiheit
lautet, dass die Schrift mindestens 24 Pixel groß sein soll. Das
Programm fragt nach der aktuellen Schriftgröße, legt einen Zähler an
und gibt am Ende aus, wie viele Klicks nötig waren. Ergänzen Sie
dazwischen eine while-Schleife, die so lange auf „A+“ klickt, wie die
Schrift kleiner als 24 Pixel ist: Bei jedem Klick wächst groesse um 2,
klicks um 1, und das Programm gibt eine Zeile wie „Klick 1: 20 Pixel“
aus. Bei Eingabe 18:

    Klick 1: 20 Pixel
    Klick 2: 22 Pixel
    Klick 3: 24 Pixel
    Nach 3 Klicks ist die Schrift 24 Pixel groß.

Ist die Schrift schon groß genug, wird nicht geklickt. Bei Eingabe 30:

    Nach 0 Klicks ist die Schrift 30 Pixel groß.

Grenzen: Die Schriftgröße ist eine ganze Zahl von 8 bis 40.

Hintergrund: Eine for-Schleife (Aufgabe 1_022) wiederholt etwas eine
feste Anzahl von Malen. Weiß man vorher nicht, wie oft, nimmt man eine
while-Schleife: Sie wiederholt ihren eingerückten Block, solange die
Bedingung dahinter wahr ist, und prüft sie vor jedem Durchlauf neu.
Ist sie schon beim ersten Mal falsch, läuft der Block kein einziges
Mal. Damit die Schleife endet, muss der Block etwas ändern, das in der
Bedingung vorkommt:

    while groesse < 24:
        groesse = groesse + 2

Fehlt die zweite Zeile, läuft die Schleife endlos; die Prüfung bricht
dann nach 5 Sekunden ab.
"""

groesse = int(input("Aktuelle Schriftgröße in Pixel: "))
klicks = 0

while groesse < 24:
    groesse = groesse + 2
    klicks = klicks + 1
    print(f"Klick {klicks}: {groesse} Pixel")

print(f"Nach {klicks} Klicks ist die Schrift {groesse} Pixel groß.")


# Idee: Die Bedingung groesse < 24 beschreibt, wann noch geklickt werden muss. Im Block wird die Schrift um
# 2 vergrößert, der Zähler um 1 erhöht und die Zeile ausgegeben. Sobald groesse 24 oder mehr ist, endet die
# Schleife, und der vorgegebene Code gibt das Ergebnis aus.
# Anderer Weg: Die Anzahl der Klicks ausrechnen, (24 - groesse + 1) // 2 bei Größen unter 24, und dann eine
# for-Schleife laufen lassen. Das ist umständlicher und leicht falsch, weil man an ungerade Größen und an
# Größen über 24 denken muss; die while-Schleife erledigt das von selbst.
# Typische Fehler: groesse <= 24 statt groesse < 24 (bei genau 24 wird noch einmal geklickt), groesse = groesse + 2
# vergessen (Endlosschleife), print vor dem Erhöhen (dann steht „Klick 0: 18 Pixel“ da) oder klicks nicht
# erhöhen (dann steht am Ende „Nach 0 Klicks“).
