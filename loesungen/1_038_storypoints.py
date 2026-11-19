# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_038_storypoints.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_038_storypoints

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

def stunden(punkte):
    """Schätzt die Arbeitsstunden für eine User Story mit so vielen Story Points."""
    return punkte * 6 + 2


story_a = int(input("Story Points der Story A: "))
story_b = int(input("Story Points der Story B: "))

print(f"Story A: {stunden(story_a)} Stunden")
print(f"Story B: {stunden(story_b)} Stunden")
print(f"Zusammen: {stunden(story_a) + stunden(story_b)} Stunden")


# Idee: Die Funktion rechnet mit dem Parameter punkte die Faustregel aus und gibt das Ergebnis mit
# return zurück. Das vorgegebene Programm setzt die Aufrufe in die f-Strings ein und addiert zwei
# Aufrufe für die Summe; das geht nur, weil die Funktion einen Wert liefert.
# Anderer Weg: Man kann das Ergebnis erst in einer Variablen ablegen, etwa ergebnis = punkte * 6 + 2,
# und dann return ergebnis schreiben. Das ist eine Zeile mehr, aber beim Lesen manchmal klarer.
# Typische Fehler: print statt return (dann steht "Story A: None Stunden" da, und die Summe bricht mit
# einem TypeError ab), die 2 Stunden für das Review vergessen oder (punkte + 2) * 6 rechnen.
