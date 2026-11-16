# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_035_altersangaben.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_035_altersangaben

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

while eingabe != "stop":
    alter = int(eingabe)
    if alter >= 0 and alter <= 120:
        gueltig = gueltig + 1
        summe = summe + alter
    else:
        ungueltig = ungueltig + 1
    eingabe = input("Alter (stop zum Beenden): ")

if gueltig == 0:
    print("Keine gültigen Angaben.")
else:
    print(f"{gueltig} gültige Angaben, Durchschnittsalter: {summe / gueltig:.1f} Jahre")
print(f"{ungueltig} Angaben zur Prüfung zurückgestellt.")


# Idee: Die Bedingung eingabe != "stop" prüft jede Eingabe, bevor damit gerechnet wird. Im Block wird die
# Eingabe mit int(...) umgewandelt; ein if/else mit alter >= 0 and alter <= 120 entscheidet, ob gueltig und
# summe wachsen oder ungueltig. Als letzte Zeile, außerhalb von if und else, wird die nächste Eingabe gelesen.
# Anderer Weg: Python erlaubt verkettete Vergleiche, 0 <= alter <= 120 bedeutet dasselbe wie die beiden
# Vergleiche mit and. Statt else geht auch ein zweites if mit alter < 0 or alter > 120; dann muss man aber
# darauf achten, dass die beiden Bedingungen genau das Gegenteil voneinander sind.
# Typische Fehler: die input-Zeile in den if-Zweig einrücken (nach der ersten ungültigen Angabe läuft die
# Schleife endlos), alter > 0 statt alter >= 0 (ein Neugeborenes zählt als Fehler), auch ungültige Angaben
# zu summe addieren oder die Eingabe vor der Bedingung umwandeln (dann bricht int("stop") ab).
