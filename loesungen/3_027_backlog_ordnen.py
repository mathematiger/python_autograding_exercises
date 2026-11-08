# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_027_backlog_ordnen.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_027_backlog_ordnen

"""Aufgabe 3_027 – Backlog ordnen                                Stufe 3 ★★★☆☆

Ein Scrum-Team sammelt seine Arbeit im Product Backlog, einer Liste
von Einträgen, die das Team nach und nach umsetzt. Jeder Eintrag ist
ein Tupel (titel, prioritaet, punkte): prioritaet 1 ist am
wichtigsten, 2 weniger wichtig und so weiter, und die Story Points
punkte schätzen, wie aufwendig der Eintrag ist. Vor der Sprintplanung
will das Team das Backlog auf drei Arten geordnet sehen. Schreiben Sie
drei Funktionen, jede mit sorted und dem Parameter key, die jeweils
eine neue Liste zurückgeben:

- `nach_aufwand(backlog)`: die Einträge nach punkte aufsteigend. Haben
  zwei Einträge gleich viele Punkte, bleibt ihre Reihenfolge aus
  backlog erhalten.
- `planungsreihenfolge(backlog)`: die Einträge nach prioritaet
  aufsteigend, bei gleicher Priorität nach punkte aufsteigend (kleine
  Aufgaben zuerst) und wenn auch das gleich ist, nach titel
  alphabetisch.
- `groesste_brocken(backlog, anzahl)`: die Titel der anzahl Einträge
  mit den meisten Punkten, die meisten zuerst; bei gleich vielen
  Punkten alphabetisch nach Titel. Hat backlog weniger Einträge, kommen
  alle.

    backlog = [("Login", 1, 5), ("Export", 2, 3), ("Suche", 1, 3),
               ("Hilfe", 3, 1), ("Bericht", 2, 3)]
    nach_aufwand(backlog)
        →  [("Hilfe", 3, 1), ("Export", 2, 3), ("Suche", 1, 3),
            ("Bericht", 2, 3), ("Login", 1, 5)]
    planungsreihenfolge(backlog)
        →  [("Suche", 1, 3), ("Login", 1, 5), ("Bericht", 2, 3),
            ("Export", 2, 3), ("Hilfe", 3, 1)]
    groesste_brocken(backlog, 3)   →  ["Login", "Bericht", "Export"]

Grenzen: 0 ≤ len(backlog) ≤ 100 000. titel ist ein nicht leerer Text
aus Buchstaben ohne Umlaute und Leerzeichen; Titel dürfen doppelt
vorkommen. prioritaet ist eine ganze Zahl von 1 bis 5, punkte eine
ganze Zahl von 1 bis 100. anzahl ist eine ganze Zahl von 0 bis 100 000.
backlog bleibt unverändert. Ihre Lösung soll O(n log n) Schritte
brauchen.

Hintergrund: sorted(liste) vergleicht die Elemente selbst miteinander;
bei Tupeln heißt das erst nach dem ersten Element, bei Gleichstand nach
dem zweiten und so weiter (Aufgabe 2_024). Will man nach etwas anderem
sortieren, übergibt man mit key eine Funktion, die zu jedem Element
einen Sortierschlüssel liefert. sorted ruft sie für jedes Element
einmal auf und ordnet die Elemente nach diesen Schlüsseln; die
Elemente selbst bleiben, wie sie sind. Meist ist key ein
lambda-Ausdruck (Aufgabe 3_025):

    dateien = [("bild.png", 300), ("text.txt", 12), ("lied.mp3", 300)]
    sorted(dateien, key=lambda d: d[1])
        →  [("text.txt", 12), ("bild.png", 300), ("lied.mp3", 300)]
    sorted(["Ei", "Brot", "Apfel"], key=len)   →  ["Ei", "Brot", "Apfel"]

Für mehrere Kriterien liefert key ein Tupel, das dann Element für
Element verglichen wird: key=lambda d: (d[1], d[0]) sortiert nach Größe
und bei gleicher Größe nach Namen. Absteigend sortiert reverse=True
(Aufgabe 2_023), aber das dreht alle Kriterien um. Soll nur eines
absteigend sein, dreht man bei Zahlen das Vorzeichen um:
key=lambda d: (-d[1], d[0]) bringt die größten Dateien zuerst und bei
gleicher Größe die Namen trotzdem alphabetisch. sorted ist stabil:
Elemente mit gleichem Schlüssel behalten ihre Reihenfolge aus der
Eingabe; oben bleibt deshalb bild.png vor lied.mp3. sorted braucht
O(n log n) Vergleiche (wie Merge Sort, Aufgabe 3_005).
"""


def nach_aufwand(backlog):
    """Gibt die Einträge nach Story Points aufsteigend zurück, bei Gleichstand in der Eingabereihenfolge."""
    return sorted(backlog, key=lambda eintrag: eintrag[2])


def planungsreihenfolge(backlog):
    """Gibt die Einträge nach Priorität, dann Punkten, dann Titel geordnet zurück."""
    return sorted(backlog, key=lambda eintrag: (eintrag[1], eintrag[2], eintrag[0]))


def groesste_brocken(backlog, anzahl):
    """Gibt die Titel der anzahl Einträge mit den meisten Punkten zurück, bei Gleichstand alphabetisch."""
    geordnet = sorted(backlog, key=lambda eintrag: (-eintrag[2], eintrag[0]))
    return [eintrag[0] for eintrag in geordnet[:anzahl]]


backlog = [("Login", 1, 5), ("Export", 2, 3), ("Suche", 1, 3), ("Hilfe", 3, 1), ("Bericht", 2, 3)]
print(nach_aufwand(backlog))
print(planungsreihenfolge(backlog))
print(groesste_brocken(backlog, 3))


# Idee: Jede Funktion ist ein Aufruf von sorted mit dem passenden Schlüssel. nach_aufwand sortiert nur nach
# eintrag[2]; weil sorted stabil ist, bleiben gleich große Einträge in ihrer Reihenfolge. planungsreihenfolge
# nimmt das Tupel (prioritaet, punkte, titel), das Python Element für Element vergleicht. groesste_brocken
# braucht die Punkte absteigend, die Titel aber aufsteigend; dafür nimmt der Schlüssel -punkte. Danach
# schneidet [:anzahl] die ersten ab, und eine List Comprehension holt die Titel heraus.
#
# Anderer Weg: Mehrfach stabil sortieren, das unwichtigste Kriterium zuerst: erst nach Titel, dann nach Punkten
# mit reverse=True; die Stabilität hält die Titelreihenfolge fest. Statt lambda geht auch
# operator.itemgetter(1, 2, 0) (Stufe 4). Eine eigene Sortierschleife (Selection Sort) braucht O(n²).
#
# Typische Fehler: reverse=True in groesste_brocken (dann stehen auch die Titel rückwärts), in nach_aufwand
# zusätzlich nach Titel sortieren (dann geht die Eingabereihenfolge verloren), backlog.sort(...) benutzen
# (verändert das Backlog und gibt None zurück) oder die Reihenfolge im Schlüsseltupel vertauschen.
#
# Laufzeit: sorted braucht O(n log n) Vergleiche, der Schlüssel wird für jedes Element nur einmal berechnet;
# das Abschneiden und Herausholen der Titel kostet O(n).
