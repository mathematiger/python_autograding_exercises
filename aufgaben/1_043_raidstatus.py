"""Aufgabe 1_043 – RAID-Status                                   Stufe 1 ★☆☆☆☆

Die Server im Rechenzentrum speichern ihre Daten auf mehreren
Festplatten im RAID-Verbund: Fällt eine Platte aus, sind die Daten noch
auf den anderen vorhanden, aber die kaputte Platte muss schnell getauscht
werden. Der Server meldet den Zustand des Verbunds als kurzen Text, ein
Zeichen pro Platte: U heißt „läuft“ (englisch up), ein Unterstrich _
heißt „ausgefallen“. Der Text UU_U_U gehört also zu einem Verbund aus
sechs Platten, von denen zwei ausgefallen sind.

Das Programm fragt schon nach dem Status-Text, geht ihn mit einer
for-Schleife Zeichen für Zeichen durch und gibt am Ende die Zahlen aus.
Ergänzen Sie in der Schleife den Zähler für die ausgefallenen Platten.
Bei Eingabe UU_U_U soll das Programm ausgeben:

    Platten: 6
    Ausgefallen: 2
    Laufen: 4

Benutzen Sie dafür die Schleife und nicht die fertige Methode count().

Grenzen: Der Status-Text hat 1 bis 30 Zeichen und besteht nur aus U und _.

Hintergrund: Eine for-Schleife kann nicht nur über range oder eine
Liste laufen, sondern auch über einen Text. Die Schleifenvariable ist
dann in jedem Durchgang ein einzelnes Zeichen, von vorn nach hinten:

    for zeichen in "U_U":
        print(zeichen)

gibt nacheinander U, _ und U aus, jedes in einer eigenen Zeile. Mit
einem Zähler, der vor der Schleife bei 0 beginnt und in der Schleife
unter einer Bedingung um 1 wächst (Aufgabe 1_025), zählt man so
bestimmte Zeichen.
"""

status = input("RAID-Status: ")
ausgefallen = 0

for zeichen in status:
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print("Platten:", len(status))
print("Ausgefallen:", ausgefallen)
print("Laufen:", len(status) - ausgefallen)
