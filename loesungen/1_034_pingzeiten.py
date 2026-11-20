# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_034_pingzeiten.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_034_pingzeiten

"""Aufgabe 1_034 – Pingzeiten                                    Stufe 1 ★☆☆☆☆

Eine Netzwerktechnikerin misst, wie schnell ein Server antwortet. Mit
dem Befehl ping schickt sie ein kleines Paket an den Server und liest
ab, wie viele Millisekunden (ms) die Antwort braucht. Sie misst
mehrmals und tippt jede Zeit in das Programm ein; wie viele Messungen
es werden, weiß sie vorher nicht. Wenn sie fertig ist, tippt sie stop.
Das Programm legt zwei Variablen an, liest die erste Eingabe und gibt
am Ende das Ergebnis aus. Ergänzen Sie dazwischen eine while-Schleife,
die läuft, solange die Eingabe nicht "stop" ist: Sie zählt in anzahl
die Messungen, addiert in summe alle Zeiten und liest dann die nächste
Eingabe mit derselben Frage wie oben. Bei den Eingaben 23, 41, 18 und
stop:

    3 Messungen, Durchschnitt: 27.3 ms

Tippt sie gleich stop, gibt das Programm aus:

    Keine Messungen.

Grenzen: Es gibt 0 bis 100 Messungen, jede ist eine ganze Zahl von 0
bis 2000. Danach kommt immer genau stop, in Kleinbuchstaben.

Hintergrund: Eine while-Schleife (Aufgabe 1_033) eignet sich, wenn man
vorher nicht weiß, wie oft sich etwas wiederholt. Bei Eingaben bis zu
einem Endwort braucht man zwei input-Zeilen: eine vor der Schleife für
die erste Eingabe und eine als letzte Zeile im Block für die nächste.
So prüft die Bedingung jede Eingabe, bevor damit gerechnet wird, und
das Wort stop wird nie mit int(...) umgewandelt:

    eingabe = input("Wert: ")
    while eingabe != "stop":
        ...                     # mit eingabe arbeiten
        eingabe = input("Wert: ")

Fehlt die input-Zeile im Block, ändert sich eingabe nie, und die
Schleife läuft endlos.
"""

anzahl = 0
summe = 0
eingabe = input("Pingzeit in ms (stop zum Beenden): ")

while eingabe != "stop":
    anzahl = anzahl + 1
    summe = summe + int(eingabe)
    eingabe = input("Pingzeit in ms (stop zum Beenden): ")

if anzahl == 0:
    print("Keine Messungen.")
else:
    print(f"{anzahl} Messungen, Durchschnitt: {summe / anzahl:.1f} ms")


# Idee: Die erste Eingabe liest der vorgegebene Code. Die Bedingung eingabe != "stop" prüft sie; ist sie
# eine Zahl, wird anzahl um 1 erhöht, int(eingabe) zu summe addiert und als letzte Zeile im Block die
# nächste Eingabe gelesen. Dann prüft die Bedingung diese, und so weiter, bis stop kommt.
# Anderer Weg: while True: mit einem input am Anfang des Blocks und if eingabe == "stop": break (break
# beendet die Schleife sofort, mehr dazu in Aufgabe 2_007). Dann
# braucht man nur eine input-Zeile, muss aber die erste Eingabe vor der Schleife selbst verarbeiten,
# weil der vorgegebene Code sie schon gelesen hat.
# Typische Fehler: die input-Zeile im Block vergessen (Endlosschleife), sie an den Anfang des Blocks
# stellen (dann wird die erste Zeit übersprungen und int("stop") bricht ab) oder summe = int(eingabe)
# statt summe = summe + int(eingabe) (dann zählt nur die letzte Zeit).
