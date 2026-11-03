"""Aufgabe 1_023 – Adressbereich                                 Stufe 1 ★☆☆☆☆

Im Büronetz 192.168.10.0 vergibt ein DHCP-Server den Geräten
automatisch ihre IP-Adressen. Er nimmt dafür nur Adressen aus einem
festgelegten Bereich, zum Beispiel von 192.168.10.20 bis 192.168.10.23;
die Adressen davor und danach sind für Drucker und Server reserviert.
Bevor der Bereich eingerichtet wird, soll ein Programm alle Adressen
darin auflisten. Es fragt schon nach der ersten und der letzten
Endnummer. Ergänzen Sie eine for-Schleife, die jede Adresse des Bereichs
in einer eigenen Zeile ausgibt, die letzte eingeschlossen. Bei den
Eingaben 20 und 23:

    192.168.10.20
    192.168.10.21
    192.168.10.22
    192.168.10.23
    4 Adressen im Bereich.

Grenzen: Die erste und die letzte Endnummer sind ganze Zahlen von 1 bis
254, und die erste ist nie größer als die letzte.

Hintergrund: range(a, b) liefert die ganzen Zahlen von a bis b - 1:
range(3, 6) liefert 3, 4 und 5. Die erste Zahl ist also dabei, die
zweite nicht mehr. Soll b selbst noch dabei sein, schreibt man
range(a, b + 1). range(n) aus Aufgabe 1_022 ist dasselbe wie
range(0, n).
"""

erste = int(input("Erste Endnummer: "))
letzte = int(input("Letzte Endnummer: "))

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"{letzte - erste + 1} Adressen im Bereich.")
