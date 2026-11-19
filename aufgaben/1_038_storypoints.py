"""Aufgabe 1_038 – Story Points                                  Stufe 1 ★☆☆☆☆

Ein Entwicklungsteam schätzt den Aufwand seiner User Stories (kleine,
abgeschlossene Anforderungen) in Story Points. Für die Sprintplanung
rechnet es sie mit einer Faustregel in Arbeitsstunden um: 6 Stunden je
Story Point und zusätzlich 2 Stunden für das Review jeder Story.

Schreiben Sie oben im Programm eine eigene Funktion stunden mit einem
Parameter punkte, die die geschätzten Stunden mit return zurückgibt.
Das Programm darunter ist vorgegeben: Es fragt nach den Story Points
zweier Stories und gibt die Stunden jeder Story und beider zusammen aus.
Bei den Eingaben 3 und 5:

    Story A: 20 Stunden
    Story B: 32 Stunden
    Zusammen: 52 Stunden

Grenzen: Beide Eingaben sind ganze Zahlen von 0 bis 100.

Hintergrund: Eine Funktion legen Sie mit def fest (Aufgabe 1_037). Soll
sie ein Ergebnis liefern, mit dem man weiterrechnen kann, schreiben Sie
return und dahinter den Wert. return beendet die Funktion, und der Aufruf
steht dann für diesen Wert:

    def doppelt(zahl):
        return zahl * 2

    ergebnis = doppelt(4) + 1       # ergebnis ist 9

Ein print in der Funktion würde den Wert nur anzeigen; der Aufruf lieferte
dann None, und mit None kann man nicht rechnen.
"""

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


story_a = int(input("Story Points der Story A: "))
story_b = int(input("Story Points der Story B: "))

print(f"Story A: {stunden(story_a)} Stunden")
print(f"Story B: {stunden(story_b)} Stunden")
print(f"Zusammen: {stunden(story_a) + stunden(story_b)} Stunden")
