# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_027_meilensteine.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_027_meilensteine

"""Aufgabe 1_027 – Meilensteine                                  Stufe 1 ★☆☆☆☆

Ein Projekt wird mit Meilensteinen geplant: wichtigen Zwischenzielen,
an denen man prüft, ob das Projekt noch im Plan liegt, etwa „Kickoff“
oder „Prototyp fertig“. Die Projektleiterin tippt die Meilensteine in
ihrer Reihenfolge ein, durch Semikolons getrennt, und dann die Nummer
des Meilensteins, der als Nächstes ansteht. Der vorgegebene Code macht
aus der Eingabe eine Liste meilensteine und holt schon den ersten
Meilenstein heraus. Ergänzen Sie drei Zeilen: anzahl soll die Anzahl
der Meilensteine sein, naechster der Meilenstein mit der eingegebenen
Nummer (gezählt ab 1) und letzter der letzte Meilenstein. Bei den
Eingaben Kickoff;Anforderungen;Prototyp;Abnahme und 3:

    Der Plan hat 4 Meilensteine.
    Erster: Kickoff, letzter: Abnahme
    Als Nächstes: Meilenstein 3, Prototyp

Grenzen: Es gibt 2 bis 20 Meilensteine, jeder Name ist ein nicht leerer
Text ohne Semikolon. Die Nummer ist eine ganze Zahl von 1 bis zur
Anzahl der Meilensteine.

Hintergrund: Eine Liste fasst mehrere Werte in einer Reihenfolge
zusammen. Man schreibt sie in eckigen Klammern, etwa phasen =
["Planung", "Umsetzung", "Abnahme"]; die vorgegebene Zeile mit
split(";") baut eine solche Liste aus dem eingetippten Text. Wie bei
den Zeichen eines Textes (Aufgaben 1_011 und 1_012) holt phasen[0] das erste
Element, phasen[1] das zweite und phasen[-1] das letzte. len(phasen)
liefert die Anzahl der Elemente, hier 3. Das letzte Element hat also
den Index len(phasen) - 1, nicht len(phasen).
"""

eingabe = input("Meilensteine, durch Semikolon getrennt: ")
meilensteine = eingabe.split(";")
nummer = int(input("Nummer des nächsten Meilensteins: "))
erster = meilensteine[0]

anzahl = len(meilensteine)
naechster = meilensteine[nummer - 1]
letzter = meilensteine[-1]

print(f"Der Plan hat {anzahl} Meilensteine.")
print(f"Erster: {erster}, letzter: {letzter}")
print(f"Als Nächstes: Meilenstein {nummer}, {naechster}")


# Idee: len(meilensteine) zählt die Elemente der Liste. Weil die Liste ab 0 zählt, die Nummer aber ab 1,
# steht Meilenstein Nummer nummer unter dem Index nummer - 1. Der Index -1 holt das letzte Element.
# Anderer Weg: letzter = meilensteine[anzahl - 1] holt dasselbe Element über die Anzahl, denn bei anzahl
# Elementen ist anzahl - 1 der größte Index.
# Typische Fehler: meilensteine[nummer] (dann kommt der Meilenstein danach heraus, beim letzten bricht das
# Programm mit IndexError ab), meilensteine[anzahl] für den letzten (ebenfalls IndexError) oder die Anzahl
# fest als 4 hinschreiben, weil das Beispiel vier Meilensteine hat.
