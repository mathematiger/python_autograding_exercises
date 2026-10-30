# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_003_selection_sort.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_003_selection_sort

"""Aufgabe 3_003 – Siegerliste                                   Stufe 3 ★★★☆☆

Beim Sportfest werden die Zeiten im 100-m-Lauf in Sekunden notiert, in der
Reihenfolge, in der die Läuferinnen und Läufer gestartet sind. Für die
Siegerehrung soll die Liste aufsteigend sortiert werden, die schnellste Zeit
zuerst. Vervollständigen Sie die Funktion `sortiere`, die die Liste mit
Selection Sort sortiert. Die Funktion verändert die übergebene Liste selbst
(„an Ort und Stelle“) und gibt nichts zurück.

    zeiten = [14.2, 12.8, 15.0, 12.1]
    sortiere(zeiten)
    print(zeiten)  →  [12.1, 12.8, 14.2, 15.0]

Benutzen Sie dafür Schleifen und nicht die fertigen Werkzeuge sorted(...) oder
liste.sort().

Grenzen: 0 ≤ len(liste) ≤ 1000. Die Zeiten sind ganze Zahlen oder
Kommazahlen von 0 bis 1000; gleiche Zeiten dürfen mehrmals vorkommen.
Selection Sort braucht O(n²) Vergleiche, soll aber höchstens einmal pro
Runde tauschen, also höchstens n Tausche machen.

Hintergrund: Selection Sort („Sortieren durch Auswählen“, Jena-Skript Teil 3)
teilt die Liste gedanklich in einen fertigen Teil vorn und einen unsortierten
Rest dahinter. Am Anfang ist der fertige Teil leer. In jeder Runde sucht man
im Rest das kleinste Element und tauscht es an die erste Stelle des Rests;
damit wächst der fertige Teil um ein Element:

    [14.2, 12.8, 15.0, 12.1]   kleinstes im Rest ab Index 0: 12.1 → tauschen mit Index 0
    [12.1, 12.8, 15.0, 14.2]   kleinstes im Rest ab Index 1: 12.8 → bleibt
    [12.1, 12.8, 15.0, 14.2]   kleinstes im Rest ab Index 2: 14.2 → tauschen mit Index 2
    [12.1, 12.8, 14.2, 15.0]   fertig

Für Runde i (i = 0, 1, …, len(liste) - 2) läuft eine innere Schleife über die
Indizes i + 1 bis zum Ende und merkt sich den Index des kleinsten Elements.
Zwei Elemente tauscht man in Python so:

    liste[i], liste[k] = liste[k], liste[i]

Selection Sort tauscht höchstens einmal pro Runde, braucht aber für das Suchen
etwa n * n / 2 Vergleiche; die Laufzeit ist O(n²). Für die Siegerliste eines
Sportfests ist das schnell genug, für Millionen Einträge nicht.

Tipp: Suchen Sie den Index des Minimums, nicht nur seinen Wert. Sonst wissen
Sie nicht, womit Sie tauschen müssen.
"""


def sortiere(liste):
    """Sortiert liste an Ort und Stelle aufsteigend mit Selection Sort."""
    for i in range(len(liste) - 1):
        kleinster = i
        for k in range(i + 1, len(liste)):
            if liste[k] < liste[kleinster]:
                kleinster = k
        liste[i], liste[kleinster] = liste[kleinster], liste[i]


zeiten = [14.2, 12.8, 15.0, 12.1]
sortiere(zeiten)
print(zeiten)


# Idee: In Runde i suchen Sie im unsortierten Rest ab Index i den Index des kleinsten Elements
# und tauschen dieses Element an die Stelle i. Nach Runde i stehen die i + 1 kleinsten Zeiten
# vorn in der richtigen Reihenfolge; nach len(liste) - 1 Runden ist die Liste sortiert.
#
# Anderer Weg: Insertion Sort nimmt nacheinander jedes Element und schiebt es im sortierten
# Teil vorn an die passende Stelle; auch das braucht O(n²) Schritte, ist aber bei fast
# sortierten Listen schnell. Bubble Sort (Aufgabe 3_004) tauscht Nachbarn, dafür viel öfter.
#
# Typische Fehler: bei jedem kleineren Element sofort tauschen statt nur den Index zu merken
# (sortiert auch, tauscht aber bis zu n² / 2-mal), die innere Schleife nur bis len(liste) - 1
# laufen lassen, oder eine neue Liste zurückgeben statt die alte zu verändern.
#
# Laufzeit: O(n²). Runde i vergleicht n - 1 - i Elemente, zusammen etwa n² / 2 Vergleiche,
# egal wie die Liste vorher aussieht; getauscht wird höchstens n - 1-mal.
