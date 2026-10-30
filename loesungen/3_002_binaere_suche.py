# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_002_binaere_suche.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_002_binaere_suche

"""Aufgabe 3_002 – Binäre Suche                                 Stufe 3 ★★★☆☆

Die Bibliothek aus Aufgabe 3_001 hat aufgeräumt: Im Magazin stehen jetzt
Hunderttausende Bücher, und ihre Nummern sind aufsteigend sortiert. Jede
Nummer kommt höchstens einmal vor. Die lineare Suche ist dafür zu langsam.
Vervollständigen Sie die Funktion `binaere_suche`, die den Index einer
gesuchten Nummer in der sortierten Liste liefert, oder -1, wenn es sie nicht
gibt.

    binaere_suche([3, 8, 15, 23, 42], 23)  →  3
    binaere_suche([3, 8, 15, 23, 42], 3)   →  0
    binaere_suche([3, 8, 15, 23, 42], 10)  →  -1
    binaere_suche([], 5)                   →  -1

Die Funktion darf sich höchstens etwa 20 Elemente einer Liste mit 1000
Einträgen ansehen; eine Schleife über alle Elemente, `in` oder liste.index(...)
sind deshalb nicht erlaubt.

Grenzen: 0 ≤ len(liste) ≤ 1 000 000. Die Nummern und gesucht sind ganze
Zahlen von -10**9 bis 10**9. Die Liste ist echt aufsteigend sortiert, jede
Nummer kommt also höchstens einmal vor. Ihre Lösung soll O(log n) Schritte
brauchen.

Hintergrund: Die binäre Suche nutzt aus, dass die Liste sortiert ist (MIT 6.0001
Lecture 12). Man merkt sich einen Bereich von Index `links` bis Index `rechts`,
in dem der gesuchte Wert noch liegen kann; am Anfang ist das die ganze Liste.
Dann schaut man in die Mitte `mitte = (links + rechts) // 2`:

- Ist liste[mitte] der gesuchte Wert, ist man fertig.
- Ist liste[mitte] kleiner, kann der Wert nur rechts davon liegen: links = mitte + 1.
- Ist liste[mitte] größer, kann er nur links davon liegen: rechts = mitte - 1.

Das wiederholt man, solange links <= rechts gilt. Wird der Bereich leer, gibt
es den Wert nicht. Jeder Schritt halbiert den Bereich: Bei 1000 Elementen ist
man nach höchstens 10 Schritten fertig, bei einer Million nach 20. Man sagt,
die Laufzeit ist O(log n), sie wächst mit dem Logarithmus der Länge. Die
lineare Suche aus Aufgabe 3_001 braucht im schlechtesten Fall n Schritte, also
O(n).

Tipp: Die häufigsten Fehler sind rechts = len(liste) statt len(liste) - 1 und
links = mitte statt mitte + 1; das zweite führt zu einer Endlosschleife.
"""


def binaere_suche(liste, gesucht):
    """Gibt den Index von gesucht in der sortierten liste zurück, sonst -1."""
    links = 0
    rechts = len(liste) - 1
    while links <= rechts:
        mitte = (links + rechts) // 2
        if liste[mitte] == gesucht:
            return mitte
        if liste[mitte] < gesucht:
            links = mitte + 1
        else:
            rechts = mitte - 1
    return -1


print(binaere_suche([3, 8, 15, 23, 42], 23))


# Idee: Merken Sie sich mit links und rechts den Bereich, in dem der Wert noch liegen kann, und
# schauen Sie in dessen Mitte. Je nach Vergleich ist der Wert gefunden, oder Sie verwerfen die
# linke oder die rechte Hälfte samt Mitte. Wird der Bereich leer (links > rechts), fehlt der Wert.
#
# Anderer Weg: rekursiv, mit links und rechts als zusätzlichen Parametern. Der naive Weg ist die
# lineare Suche aus Aufgabe 3_001 mit O(n) Schritten; bei einer Million Einträgen sind das bis zu
# eine Million Vergleiche statt etwa 20.
#
# Typische Fehler: rechts = len(liste) statt len(liste) - 1 (Zugriff hinter das Ende),
# while links < rechts (bleibt zuletzt ein Element übrig, links == rechts, wird es nie angesehen)
# und links = mitte
# statt mitte + 1 (der Bereich schrumpft nicht mehr, Endlosschleife).
#
# Laufzeit: O(log n). Jeder Durchlauf halbiert den Bereich, nach etwa log₂(n) Durchläufen ist
# er leer.
