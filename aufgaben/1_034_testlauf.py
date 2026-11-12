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

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"{bestanden + fehlgeschlagen} Testfälle: {bestanden} bestanden, {fehlgeschlagen} fehlgeschlagen")
