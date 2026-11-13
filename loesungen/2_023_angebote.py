# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_023_angebote.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_023_angebote

"""Aufgabe 2_023 – Angebote                                      Stufe 2 ★★☆☆☆

Für die neuen Notebooks der Schulungsabteilung hat der Einkauf Angebote
von mehreren Händlern eingeholt. Die Preise stehen in Cent in einer
Liste, in der Reihenfolge, in der die Angebote eingegangen sind:

    preise = [129900, 104950, 118000, 99900, 104950]

Diese Liste ist das Protokoll des Eingangs und darf nicht
durcheinandergeraten. Für die Entscheidung braucht der Einkauf aber zwei
sortierte Ansichten. Schreiben Sie zwei Funktionen:

- `guenstigste(preise, anzahl)` gibt eine neue Liste mit den anzahl
  niedrigsten Preisen zurück, aufsteigend sortiert. Die übergebene Liste
  bleibt unverändert.
- `absteigend_sortieren(preise)` sortiert die übergebene Liste selbst
  absteigend, den höchsten Preis zuerst, und gibt nichts zurück. Sie ist
  für die Arbeitskopie gedacht, die der Einkauf ausdrucken will.

    guenstigste(preise, 3)      →  [99900, 104950, 104950]
    preise                      →  [129900, 104950, 118000, 99900, 104950]  (unverändert)
    absteigend_sortieren(preise)
    preise                      →  [129900, 118000, 104950, 104950, 99900]

Benutzen Sie sorted und sort, keine eigene Sortierschleife.

Grenzen: preise hat 0 bis 100 000 Einträge, ganze Zahlen von 1 bis
10**7; derselbe Preis kann mehrmals vorkommen. anzahl ist eine ganze
Zahl von 0 bis len(preise).

Hintergrund: Python hat zwei Wege, eine Liste zu sortieren.
sorted(liste) (Aufgabe 1_031) baut eine neue, sortierte Liste und lässt
die alte, wie sie ist. liste.sort() sortiert dagegen die Liste selbst und gibt None
zurück; die alte Reihenfolge ist danach weg. Beide sortieren
aufsteigend, mit reverse=True absteigend:

    werte = [3, 1, 2]
    neu = sorted(werte, reverse=True)   # neu ist [3, 2, 1], werte bleibt [3, 1, 2]
    werte.sort()                        # werte ist jetzt [1, 2, 3]

Ein häufiger Fehler ist werte = werte.sort(): Danach ist werte None.
Wie in Aufgabe 2_019 sieht der Aufrufer jede Änderung, die eine Funktion
an einer übergebenen Liste macht; sort in einer Funktion verändert also
die Liste des Aufrufers, sorted nicht. Die ersten anzahl Elemente einer
Liste liefert liste[:anzahl] (Slicing wie in Aufgabe 2_018).
"""


def guenstigste(preise, anzahl):
    """Gibt die anzahl niedrigsten Preise aufsteigend in einer neuen Liste zurück."""
    return sorted(preise)[:anzahl]


def absteigend_sortieren(preise):
    """Sortiert die übergebene Liste selbst absteigend."""
    preise.sort(reverse=True)


preise = [129900, 104950, 118000, 99900, 104950]
print(guenstigste(preise, 3))
print(preise)
absteigend_sortieren(preise)
print(preise)


# Idee: guenstigste darf die Liste nicht ändern, also baut sorted(preise) eine neue, aufsteigend
# sortierte Liste, von der [:anzahl] die ersten anzahl Preise nimmt. absteigend_sortieren soll dagegen
# genau die übergebene Liste ändern: preise.sort(reverse=True) sortiert sie an Ort und Stelle.
#
# Anderer Weg: Für absteigend_sortieren geht auch preise.sort() und danach preise.reverse(). In
# guenstigste ginge außerhalb dieser Aufgabe auch eine Kopie, kopie = preise[:] (Aufgabe 2_018), und
# dann kopie.sort(); hier ist aber sorted verlangt, und die Tests prüfen das.
#
# Typische Fehler: in guenstigste preise.sort() (verändert das Eingangsprotokoll), return preise.sort()
# (gibt None zurück), in absteigend_sortieren preise = sorted(preise, reverse=True) (ändert nur die
# lokale Variable, der Aufrufer sieht nichts) oder reverse=True vergessen.
