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

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"{anzahl} Ports eingegeben, davon {bekannte} Well-known-Ports.")
