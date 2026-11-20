"""Aufgabe 1_035 – Altersangaben                                 Stufe 1 ★☆☆☆☆

Eine Firma übernimmt ihre alte Kundenkartei in eine neue Datenbank.
Bevor die Altersangaben eingespielt werden, prüft eine Mitarbeiterin
die Datenqualität: Ein Alter ist nur gültig, wenn es von 0 bis 120
Jahre reicht. Alles andere (zum Beispiel 130 oder -2) ist ein Tippfehler
in der alten Kartei. Sie tippt die Werte nacheinander in das Programm,
am Ende tippt sie stop. Das Programm legt drei Zähler an, liest die
erste Eingabe und gibt am Ende das Ergebnis aus. Ergänzen Sie
dazwischen eine while-Schleife, die läuft, solange die Eingabe nicht
"stop" ist. Sie wandelt die Eingabe in eine Zahl um und prüft sie:

- Ist das Alter gültig, erhöht sie gueltig um 1 und addiert das Alter
  zu summe.
- Sonst erhöht sie ungueltig um 1 und gibt sofort eine Zeile wie
  „Ungültiger Wert: 130“ aus.

Danach liest sie die nächste Eingabe mit derselben Frage wie oben. Bei
den Eingaben 34, 130, 51, -2, 27 und stop:

    Ungültiger Wert: 130
    Ungültiger Wert: -2
    Gültig: 3, ungültig: 2
    Durchschnittsalter: 37.3 Jahre

Gibt es keinen gültigen Wert, fehlt die letzte Zeile.

Grenzen: Es gibt 0 bis 100 Werte, jeder ist eine ganze Zahl von -999
bis 999. Danach kommt immer genau stop, in Kleinbuchstaben.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. Die Eingaben
bis zum Endwort liest eine while-Schleife mit zwei input-Zeilen, eine
vor der Schleife und eine als letzte Zeile im Block (Aufgabe 1_034).
Im Block wandeln Sie die Eingabe mit int(...) in eine Zahl um (Aufgabe
1_004).
In der Schleife entscheidet if/else (Aufgabe 1_018), was mit dem Wert
passiert; ob er in einem Bereich liegt, prüfen zwei Vergleiche, die
mit and verknüpft sind (Aufgaben 1_016 und 1_020):

    if alter >= 0 and alter <= 120:

Die Zähler wachsen wie in Aufgabe 1_025 mit gueltig = gueltig + 1.
"""

gueltig = 0
ungueltig = 0
summe = 0
eingabe = input("Alter (stop zum Beenden): ")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"Gültig: {gueltig}, ungültig: {ungueltig}")
if gueltig > 0:
    print(f"Durchschnittsalter: {summe / gueltig:.1f} Jahre")
