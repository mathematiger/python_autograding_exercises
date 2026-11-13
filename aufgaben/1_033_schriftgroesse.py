"""Aufgabe 1_033 – Schriftgröße                                  Stufe 1 ★☆☆☆☆

In einer Eingabemaske hat jede Schaltfläche eine feste Breite in Pixeln.
Ist die Beschriftung zu lang, soll die Schrift so lange kleiner werden,
bis der Text hineinpasst. Die Maske beginnt mit Schriftgröße 24. Ein
Text ist ungefähr so breit wie Anzahl der Zeichen mal Schriftgröße
geteilt durch 2 (ganzzahlig mit //). Der vorgegebene Code liest die
Anzahl der Zeichen und die Breite der Schaltfläche ein und gibt am Ende
das Ergebnis aus. Ergänzen Sie dazwischen eine while-Schleife, die die
Schriftgröße um 1 verkleinert, solange der Text breiter ist als die
Schaltfläche. Passt der Text schon, bleibt es bei 24. Bei 20 Zeichen
und einer Breite von 150 Pixeln:

    Schriftgröße: 15, Textbreite: 150 Pixel

Grenzen: Die Anzahl der Zeichen ist eine ganze Zahl von 1 bis 100, die
Breite eine ganze Zahl von der Anzahl der Zeichen bis 2000. Genau so
breit wie die Schaltfläche darf der Text sein.

Hintergrund: Eine for-Schleife über range(n) läuft eine feste Anzahl von
Malen (Aufgabe 1_022). Oft weiß man aber vorher nicht, wie oft etwas
wiederholt werden muss, sondern nur, wann Schluss ist. Dafür gibt es die
while-Schleife: Sie wiederholt ihren eingerückten Block, solange die
Bedingung dahinter wahr ist, und prüft sie vor jedem Durchlauf neu.

    while zahl > 10:
        zahl = zahl - 3

Im Block muss sich etwas ändern, das in der Bedingung vorkommt, sonst
wird sie nie falsch und die Schleife läuft endlos (die Prüfung bricht
dann nach 5 Sekunden ab). Ist die Bedingung schon am Anfang falsch, läuft
der Block kein einziges Mal.
"""

zeichen = int(input("Anzahl der Zeichen: "))
breite = int(input("Breite der Schaltfläche in Pixeln: "))
schriftgroesse = 24

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"Schriftgröße: {schriftgroesse}, Textbreite: {zeichen * schriftgroesse // 2} Pixel")
