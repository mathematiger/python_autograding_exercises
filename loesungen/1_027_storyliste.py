# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_027_storyliste.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_027_storyliste

"""Aufgabe 1_027 – Storyliste                                   Stufe 1 ★☆☆☆☆

Ein Entwicklungsteam plant seinen nächsten Sprint, also die nächsten
zwei Arbeitswochen. Wer im Team die Rolle Product Owner hat, entscheidet
über die Reihenfolge der Arbeit und hat fünf User Stories (kurze
Beschreibungen, was die Software können soll) ausgewählt und nach
Wichtigkeit sortiert:

    Login-Seite, Passwort vergessen, Profilbild, Suche, Export als PDF

Legen Sie in der Variablen stories eine Liste mit diesen fünf Texten
in genau dieser Reihenfolge an. Das Programm fragt dann nach einem
Platz in der Rangfolge, 1 ist die wichtigste Story. Ergänzen Sie eine
print-Zeile, die die Story auf diesem Platz und die Anzahl aller
Stories ausgibt. Bei Eingabe 2 soll das Programm ausgeben:

    Platz 2 von 5: Passwort vergessen

Grenzen: Der Platz ist eine ganze Zahl von 1 bis 5.

Hintergrund: Eine Liste fasst mehrere Werte unter einem Namen zusammen.
Man schreibt die Werte durch Kommas getrennt in eckige Klammern:
farben = ["rot", "grün", "blau"]. Wie bei den Zeichen eines Textes
(Aufgabe 1_011) holt farben[0] den ersten Wert, farben[1] den zweiten;
gezählt wird also ab 0. len(farben) gibt an, wie viele Werte in der
Liste stehen, hier 3.

Tipp: Der Platz beginnt bei 1, der Index bei 0. Für Platz 2 brauchen
Sie also stories[1].
"""

stories = ["Login-Seite", "Passwort vergessen", "Profilbild", "Suche", "Export als PDF"]

platz = int(input("Platz der Story (1 bis 5): "))

print(f"Platz {platz} von {len(stories)}: {stories[platz - 1]}")


# Idee: Die fünf Texte stehen in eckigen Klammern, durch Kommas getrennt, in der vorgegebenen
# Reihenfolge. Weil Python ab 0 zählt, der Platz aber ab 1, steht die Story auf Platz platz beim Index
# platz - 1. len(stories) liefert die Anzahl, hier 5.
# Anderer Weg: Erst index = platz - 1 und story = stories[index] in eigene Zeilen schreiben und dann
# print(f"Platz {platz} von {len(stories)}: {story}") ausgeben; das ist länger, aber leichter zu lesen.
# Typische Fehler: stories[platz] statt stories[platz - 1] (dann kommt die nächste Story heraus und bei
# Platz 5 ein IndexError), die Anzahl als feste 5 hinschreiben, die Texte ohne Anführungszeichen
# schreiben (NameError) oder einen Tippfehler in einem der Texte machen.
