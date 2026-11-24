# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_065_testumgebung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_065_testumgebung

"""Aufgabe 3_065 – Testumgebung                                  Stufe 3 ★★★☆☆

Eine Softwarefirma hat genau eine Lasttestumgebung: einen Servercluster,
der wie das echte System aufgebaut ist und auf dem ein Team prüft, ob
seine Software auch Tausende gleichzeitige Nutzer verkraftet. Weil ein
Lasttest den ganzen Cluster auslastet, darf immer nur ein Team darauf
arbeiten. Die Teams beantragen deshalb Zeitfenster. Für die nächste Woche
liegen mehr Anträge vor, als hineinpassen, und die Leitung möchte
möglichst viele davon genehmigen; ein Antrag wird ganz oder gar nicht
genehmigt.

Ein Antrag ist ein Tupel (team, start, ende) mit den Zeitpunkten in
Stunden ab Montag 0 Uhr. Das Fenster beginnt bei start und endet bei
ende, ende selbst gehört nicht mehr dazu (wie bei range). Endet ein
Fenster um 12 Uhr, darf das nächste also um 12 Uhr beginnen. Schreiben
Sie zwei Funktionen:

- `ueberschneiden(a, b)` gibt True zurück, wenn sich die Fenster der
  Anträge a und b überschneiden, sonst False.
- `genehmigte(antraege)` gibt eine Liste mit möglichst vielen Anträgen
  aus antraege zurück, von denen sich keine zwei überschneiden, geordnet
  nach ihrer Endzeit. Die Liste antraege selbst soll unverändert bleiben.

    ueberschneiden(("Kasse", 9, 12), ("Lager", 11, 14))   →  True
    ueberschneiden(("Kasse", 9, 12), ("Login", 12, 13))   →  False
    antraege = [("Kasse", 9, 12), ("Shop", 10, 11), ("Lager", 11, 14),
                ("Login", 12, 13), ("Suche", 13, 17), ("Bericht", 8, 18)]
    genehmigte(antraege)
        →  [("Shop", 10, 11), ("Login", 12, 13), ("Suche", 13, 17)]

Oft gibt es mehrere gleich gute Auswahlen; im Beispiel wäre auch
[("Kasse", 9, 12), ("Login", 12, 13), ("Suche", 13, 17)] richtig. Es
zählt nur, dass es so viele Anträge wie möglich sind.

Grenzen: 0 ≤ len(antraege) ≤ 100 000. Die Teamnamen sind verschiedene,
nicht leere Texte; start und ende sind ganze Zahlen mit
0 ≤ start < ende ≤ 10**9. Die Anträge stehen in beliebiger Reihenfolge,
und viele Fenster dürfen dieselbe Start- oder Endzeit haben.
genehmigte soll O(n log n) Schritte brauchen.

Hintergrund: Ein Greedy-Verfahren („gierig“) baut eine Lösung Schritt für
Schritt auf, nimmt bei jedem Schritt das, was im Moment am besten
aussieht, und nimmt diese Entscheidung nie wieder zurück. Das ist
schnell, aber nur bei manchen Aufgaben richtig, und es kommt darauf an,
was „am besten“ heißt. Hier gilt: Nehmen Sie immer den Antrag, der am
frühesten endet und sich nicht mit dem zuletzt genehmigten überschneidet.
Dafür sortieren Sie die Anträge nach ihrer Endzeit (sorted mit key,
Aufgabe 3_027) und gehen sie einmal durch. Wie in Aufgabe 3_064 werden
die Zeiträume also erst sortiert und dann einmal durchgegangen, dort aber
nach dem Start; hier ist die Endzeit entscheidend.

Warum das die meisten Anträge liefert: Nehmen Sie irgendeine beste
Auswahl. Ihr erster Antrag endet nicht früher als der Antrag g mit der
frühesten Endzeit überhaupt. Tauscht man ihn gegen g aus, überschneidet
sich weiterhin nichts, und es sind gleich viele. Also gibt es eine beste
Auswahl, die mit g beginnt, und für den Rest bleibt dieselbe Aufgabe mit
allen Anträgen, die nicht vor dem Ende von g beginnen. Dort wiederholt
sich das Argument Schritt für Schritt. Naheliegende andere Regeln
scheitern: „das kürzeste Fenster zuerst“ nimmt bei (0, 10), (9, 12),
(11, 20) nur das kurze (9, 12), das beide anderen blockiert, statt
(0, 10) und (11, 20). „Der früheste Start zuerst“ nimmt bei (0, 100),
(1, 2), (3, 4) nur das lange Fenster statt der beiden kurzen. Alle
Auswahlen durchzuprobieren (Aufgabe 3_035) wäre richtig, kostet bei
n Anträgen aber 2**n Versuche.

Tipp: Merken Sie sich den zuletzt genehmigten Antrag. Ein neuer passt,
wenn er sich nicht mit ihm überschneidet; mit früheren kann er sich dann
auch nicht überschneiden, weil die alle noch früher enden.
"""


def ueberschneiden(a, b):
    """Gibt True zurück, wenn sich die Zeitfenster der Anträge a und b überschneiden."""
    _, start_a, ende_a = a
    _, start_b, ende_b = b
    return start_a < ende_b and start_b < ende_a


def genehmigte(antraege):
    """Gibt möglichst viele Anträge ohne Überschneidung zurück, nach Endzeit geordnet."""
    auswahl = []
    for antrag in sorted(antraege, key=lambda antrag: antrag[2]):
        if not auswahl or not ueberschneiden(auswahl[-1], antrag):
            auswahl.append(antrag)
    return auswahl


antraege = [("Kasse", 9, 12), ("Shop", 10, 11), ("Lager", 11, 14),
            ("Login", 12, 13), ("Suche", 13, 17), ("Bericht", 8, 18)]
print(ueberschneiden(("Kasse", 9, 12), ("Lager", 11, 14)))
print(genehmigte(antraege))


# Idee: Sortieren Sie die Anträge nach der Endzeit und gehen Sie sie einmal durch. Ein Antrag wird
# genehmigt, wenn noch keiner genehmigt ist oder er sich nicht mit dem zuletzt genehmigten
# überschneidet. ueberschneiden prüft, ob jedes Fenster beginnt, bevor das andere endet; weil ende
# nicht dazugehört, steht dort < und nicht <=.
# Anderer Weg: Statt des letzten Antrags merkt man sich nur dessen Endzeit (letztes_ende = 0, ein
# Antrag passt bei start >= letztes_ende). Naiv probiert man alle 2**n Auswahlen durch (Aufgabe 3_035);
# das ist richtig, aber schon bei 40 Anträgen hoffnungslos. Gleich gut wäre gierig von hinten: nach
# Startzeit absteigend sortieren und immer den spätesten Start nehmen.
# Typische Fehler: nach Länge oder nach Startzeit sortieren (Gegenbeispiele im Hintergrund), mit dem
# Vorgänger in der sortierten Liste statt mit dem zuletzt genehmigten vergleichen, <= statt < in
# ueberschneiden (dann passen angrenzende Fenster nicht mehr), antraege.sort() verändert die Eingabe.
# Laufzeit: Das Sortieren kostet O(n log n), der Durchgang danach O(n), zusammen O(n log n).
