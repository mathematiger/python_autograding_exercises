# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_032_ticketbewertung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_032_ticketbewertung

"""Aufgabe 1_032 – Ticketbewertung                               Stufe 1 ★☆☆☆☆

Nach jedem gelösten Ticket bittet der IT-Support die Kundin oder den
Kunden um eine Bewertung von 1 (sehr unzufrieden) bis 5 (sehr
zufrieden). Die Teamleitung will am Ende der Woche wissen, wie der
Durchschnitt aussieht und bei welchen Tickets sie nachfassen muss:
bei allen mit einer Bewertung von 1 oder 2. Die Tickets der Woche
sind in der Reihenfolge der Eingabe ab 1 nummeriert. Der vorgegebene
Code liest die Bewertungen als Texte in die Liste teile und gibt am
Ende das Ergebnis aus. Ergänzen Sie dazwischen:

- eine Liste bewertungen mit den Bewertungen als Zahlen (mit append),
- eine Liste nachfassen mit den Nummern der Tickets, deren Bewertung
  höchstens 2 ist, in der Reihenfolge der Tickets,
- die Variable durchschnitt mit dem Durchschnitt aller Bewertungen.

Bei der Eingabe 5,2,4,1,5,3:

    6 Bewertungen, Durchschnitt: 3.33
    Schlechteste: 1, beste: 5
    Nachfassen bei Ticket: [2, 4]

Grenzen: Es gibt 1 bis 50 Bewertungen, jede ist eine ganze Zahl von 1
bis 5.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. Eine Liste
baut man auf, indem man vor der Schleife eine leere Liste anlegt und
in der Schleife mit append anhängt (Aufgabe 1_029). Mit for über eine
Liste (Aufgabe 1_028) bekommt man jedes Element, aber nicht seine
Stelle; die Ticketnummer erhält man mit for stelle in range(len(liste))
(Aufgaben 1_022 und 1_027): Element Nummer stelle + 1 ist liste[stelle],
denn die Liste zählt ab 0. Den Durchschnitt liefern sum und len
(Aufgabe 1_031): Summe geteilt durch Anzahl.
"""

eingabe = input("Bewertungen von 1 bis 5, durch Kommas getrennt: ")
teile = eingabe.split(",")

bewertungen = []
for teil in teile:
    bewertungen.append(int(teil))
nachfassen = []
for stelle in range(len(bewertungen)):
    if bewertungen[stelle] <= 2:
        nachfassen.append(stelle + 1)
durchschnitt = sum(bewertungen) / len(bewertungen)

print(f"{len(bewertungen)} Bewertungen, Durchschnitt: {durchschnitt:.2f}")
print(f"Schlechteste: {min(bewertungen)}, beste: {max(bewertungen)}")
print(f"Nachfassen bei Ticket: {nachfassen}")


# Idee: Erst eine leere Liste bewertungen anlegen und in einer for-Schleife über teile jede Bewertung mit
# int(teil) umwandeln und anhängen. Dann eine zweite Schleife über die Stellen mit range(len(bewertungen)):
# Ist bewertungen[stelle] höchstens 2, kommt stelle + 1 in die Liste nachfassen. Der Durchschnitt ist
# sum(bewertungen) / len(bewertungen).
# Anderer Weg: Beides in einer einzigen Schleife über range(len(teile)): umwandeln, anhängen und gleich
# prüfen. Oder eine eigene Zählvariable nummer, die in der Schleife über die Bewertungen mitzählt.
# Typische Fehler: stelle statt stelle + 1 anhängen (alle Nummern um eins zu klein), < 2 statt <= 2
# (Bewertung 2 fehlt), die Bewertung statt der Ticketnummer anhängen oder teil statt int(teil) anhängen
# (dann sind es Texte, und schon der Vergleich <= 2 bricht mit TypeError ab).
