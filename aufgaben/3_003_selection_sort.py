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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


zeiten = [14.2, 12.8, 15.0, 12.1]
sortiere(zeiten)
print(zeiten)
