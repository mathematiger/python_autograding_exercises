# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_034_testlauf.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_034_testlauf

"""Aufgabe 1_034 – Testlauf                                      Stufe 1 ★☆☆☆☆

Bevor eine neue Version einer Software ausgeliefert wird, spielt eine
Testerin die Testfälle aus dem Testplan von Hand durch. Nach jedem Testfall
tippt sie das Ergebnis ein: "ok", wenn sich das Programm wie beschrieben
verhalten hat, sonst "fehler". Ist sie fertig, tippt sie "stop". Danach
soll das Programm zusammenfassen, wie viele Testfälle bestanden haben und
wie viele nicht.

Der vorgegebene Code legt die beiden Zähler an, liest die erste Eingabe und
gibt am Ende die Zusammenfassung aus. Ergänzen Sie dazwischen eine
while-Schleife, die läuft, solange die Eingabe nicht "stop" ist. In jedem
Durchlauf zählt sie die Eingabe beim passenden Zähler mit und liest dann
mit input die nächste Eingabe.

Bei den Eingaben ok, ok, fehler, ok, stop:

    4 Testfälle: 3 bestanden, 1 fehlgeschlagen

Grenzen: Jede Eingabe ist genau "ok", "fehler" oder "stop". Vor dem "stop"
kommen 0 bis 200 Ergebnisse.

Hintergrund: Wie oft eine Schleife laufen muss, steht hier vorher nicht
fest; erst die Eingabe "stop" beendet sie. Dafür liest man die erste
Eingabe vor der Schleife und jede weitere am Ende des Blocks. So prüft die
Bedingung immer die gerade gelesene Eingabe:

    eingabe = input("Ergebnis: ")
    while eingabe != "stop":
        ...
        eingabe = input("Ergebnis: ")

Fehlt das input im Block, prüft die Schleife immer wieder dieselbe Eingabe
und läuft endlos. Wie eine while-Schleife arbeitet, steht in Aufgabe 1_033.
"""

bestanden = 0
fehlgeschlagen = 0
eingabe = input("Ergebnis (ok, fehler oder stop): ")

while eingabe != "stop":
    if eingabe == "ok":
        bestanden = bestanden + 1
    else:
        fehlgeschlagen = fehlgeschlagen + 1
    eingabe = input("Ergebnis (ok, fehler oder stop): ")

print(f"{bestanden + fehlgeschlagen} Testfälle: {bestanden} bestanden, {fehlgeschlagen} fehlgeschlagen")


# Idee: Die erste Eingabe liest schon der vorgegebene Code. Die Schleife läuft, solange sie nicht "stop"
# ist: Bei "ok" erhöht sie bestanden, sonst fehlgeschlagen, und als letzte Zeile im Block liest sie die
# nächste Eingabe. Kommt "stop", ist die Bedingung falsch, und darunter folgt die Zusammenfassung.
# Anderer Weg: statt else ein zweites if eingabe == "fehler". Oder nur bestanden und eine Variable
# gesamt zählen und fehlgeschlagen = gesamt - bestanden ausrechnen.
# Typische Fehler: das input im Block vergessen (Endlosschleife), das input an den Anfang des Blocks
# stellen (dann wird die erste Eingabe nie gezählt und "stop" als Fehler mitgezählt) oder die
# Bedingung als eingabe == "stop" schreiben (dann läuft die Schleife gar nicht).
