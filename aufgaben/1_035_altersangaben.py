"""Aufgabe 1_035 – Altersangaben                                 Stufe 1 ★☆☆☆☆

Ein Sportverein zieht seine Mitgliederdaten in eine neue Datenbank um.
In der alten Kartei fehlt bei vielen Mitgliedern das Alter, deshalb
tippt eine Mitarbeiterin die Angaben von den Papierbögen nach. Dabei
schleichen sich Fehler ein: Ein Alter unter 0 oder über 120 Jahren
kann nicht stimmen. Solche Angaben sollen nicht in die Datenbank,
sondern werden gezählt und später von Hand geprüft. Wie viele Angaben
es werden, weiß sie vorher nicht; wenn sie fertig ist, tippt sie stop.
Das Programm legt drei Variablen an, liest die erste Eingabe und gibt
am Ende das Ergebnis aus. Ergänzen Sie dazwischen eine while-Schleife,
die läuft, solange die Eingabe nicht "stop" ist: Sie wandelt die
Eingabe in eine ganze Zahl um und prüft sie. Liegt das Alter von 0
bis 120 (beide Grenzen gehören dazu), wird gueltig um 1 erhöht und
das Alter zu summe addiert, sonst wird ungueltig um 1 erhöht. Dann
liest die Schleife die nächste Eingabe mit derselben Frage wie oben.
Bei den Eingaben 34, 250, 17, -3, 52 und stop:

    3 gültige Angaben, Durchschnittsalter: 34.3 Jahre
    2 Angaben zur Prüfung zurückgestellt.

Sind gar keine Angaben gültig, steht in der ersten Zeile:

    Keine gültigen Angaben.

Grenzen: Es gibt 0 bis 100 Angaben, jede ist eine ganze Zahl von -999
bis 999. Danach kommt immer genau stop, in Kleinbuchstaben.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. Die
while-Schleife mit einer input-Zeile vor der Schleife und einer als
letzte Zeile im Block kennen Sie aus Aufgabe 1_034. In den Block
gehört diesmal ein if/else (Aufgabe 1_018), das mit and zwei
Vergleiche verknüpft (Aufgabe 1_020): alter >= 0 and alter <= 120 ist
nur wahr, wenn beide Vergleiche stimmen. Zähler und Summe wachsen wie
in Aufgabe 1_025 mit gueltig = gueltig + 1. Achten Sie auf die
Einrückung: Was nur für gültige Angaben gilt, steht eingerückt unter
dem if, die input-Zeile aber unter keinem der beiden Zweige, denn die
nächste Eingabe wird in jedem Fall gelesen.
"""

gueltig = 0
ungueltig = 0
summe = 0
eingabe = input("Alter (stop zum Beenden): ")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

if gueltig == 0:
    print("Keine gültigen Angaben.")
else:
    print(f"{gueltig} gültige Angaben, Durchschnittsalter: {summe / gueltig:.1f} Jahre")
print(f"{ungueltig} Angaben zur Prüfung zurückgestellt.")
