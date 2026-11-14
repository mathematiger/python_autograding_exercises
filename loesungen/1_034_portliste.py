# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_034_portliste.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_034_portliste

"""Aufgabe 1_034 – Portliste                                    Stufe 1 ★☆☆☆☆

Ein Netzwerkadministrator geht die Firewall-Regeln eines Servers durch und
tippt die freigegebenen Ports einzeln ein. Wie viele es werden, weiß er
vorher nicht; ist er fertig, gibt er stop ein. Das Programm soll zählen,
wie viele Ports eingegeben wurden und wie viele davon sogenannte
Well-known-Ports sind: Das sind die Ports 0 bis 1023, auf denen
Standarddienste wie HTTP (80) oder SSH (22) laufen.

Der vorgegebene Code liest die erste Eingabe und gibt am Ende das Ergebnis
aus. Ergänzen Sie dazwischen eine while-Schleife, die läuft, solange die
Eingabe nicht stop ist: Sie wandelt die Eingabe in eine Zahl um, zählt
anzahl und, falls der Port unter 1024 liegt, auch bekannte hoch, und liest
dann die nächste Eingabe. Bei den Eingaben 22, 443, 8080, 3306 und stop:

    4 Ports eingegeben, davon 2 Well-known-Ports.

Grenzen: Es werden 0 bis 50 Ports eingegeben, jeder ist eine ganze Zahl von
0 bis 65535. Danach kommt genau einmal stop (kleingeschrieben).

Hintergrund: Bei einer Eingabeschleife steht input() zweimal im Programm:
einmal vor der Schleife, damit die Bedingung beim ersten Mal etwas zu
prüfen hat, und einmal als letzte Zeile im Schleifenblock, damit die
Bedingung danach die neue Eingabe prüft:

    eingabe = input("Port: ")
    while eingabe != "stop":
        ...
        eingabe = input("Port: ")

Fehlt das zweite input(), prüft die Schleife immer wieder dieselbe Eingabe
und endet nie. Ist schon die erste Eingabe stop, läuft der Block kein
einziges Mal. Die while-Schleife kennen Sie aus Aufgabe 1_033.
"""

anzahl = 0
bekannte = 0
eingabe = input("Port (oder stop): ")

while eingabe != "stop":
    port = int(eingabe)
    anzahl = anzahl + 1
    if port < 1024:
        bekannte = bekannte + 1
    eingabe = input("Port (oder stop): ")

print(f"{anzahl} Ports eingegeben, davon {bekannte} Well-known-Ports.")


# Idee: Die Schleife läuft, solange eingabe nicht "stop" ist. Im Block wird die Eingabe mit int(...)
# umgewandelt, anzahl um 1 erhöht und bei port < 1024 auch bekannte. Die letzte Zeile im Block liest mit
# input(...) die nächste Eingabe; danach prüft while die Bedingung mit dieser neuen Eingabe.
# Anderer Weg: while True: mit eingabe = input(...) als erster Zeile und if eingabe == "stop": break.
# Dann braucht man input() nur einmal, aber die vorgegebene erste Eingabe müsste anders verarbeitet werden.
# Typische Fehler: das zweite input() vergessen (Endlosschleife), es an den Anfang des Blocks stellen
# (dann wird die erste Eingabe übersprungen und int("stop") bricht ab), port <= 1024 statt port < 1024
# oder anzahl nur bei den Well-known-Ports hochzählen.
