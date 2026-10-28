# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_001_suche.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_001_suche

"""Aufgabe 3_001 – Lineare Suche                                 Stufe 3 ★★★☆☆

In einer Bibliothek stehen die Buchnummern der Regalreihe in einer Liste, in der
Reihenfolge, wie die Bücher im Regal stehen. Vervollständigen Sie die Funktion
`finde`, die die Position (den Index) einer gesuchten Buchnummer liefert. Steht
das Buch nicht im Regal, soll -1 zurückkommen. Kommt die Nummer mehrmals vor,
zählt das erste Vorkommen.

    finde([41, 7, 23, 7], 23)  →  2
    finde([41, 7, 23, 7], 7)   →  1
    finde([41, 7, 23, 7], 99)  →  -1
    finde([], 5)               →  -1

Benutzen Sie dafür eine Schleife und nicht die fertige Methode liste.index(...).

Grenzen: 0 ≤ len(liste) ≤ 10 000. Die Buchnummern und gesucht sind ganze
Zahlen von 0 bis 999 999 (die Funktion soll aber auch mit Texten
funktionieren). Die Liste ist nicht sortiert, und dieselbe Nummer darf
mehrmals vorkommen. Ihre Lösung soll jedes Element höchstens einmal
ansehen, also O(n) Schritte brauchen, und beim ersten Treffer aufhören.

Hintergrund: Das hier ist die lineare Suche, der einfachste Suchalgorithmus:
Man geht die Liste von vorn nach hinten durch und vergleicht jedes Element mit
dem gesuchten Wert. Sobald es passt, ist man fertig und gibt den Index zurück.
Ist man am Ende angekommen, ohne etwas zu finden, gibt es den Wert nicht. Im
schlechtesten Fall schaut man sich alle n Elemente an; man sagt, die Suche hat
die Laufzeit O(n), sie wächst linear mit der Länge der Liste. Bei sortierten
Listen geht es schneller, das kommt in einer späteren Aufgabe.

Tipp: for index in range(len(liste)) liefert nacheinander alle Indizes. Ein
return innerhalb der Schleife beendet die Funktion sofort.
"""


def finde(liste, gesucht):
    """Gibt den Index des ersten Vorkommens von gesucht zurück, sonst -1."""
    for index in range(len(liste)):
        if liste[index] == gesucht:
            return index
    return -1


print(finde([41, 7, 23, 7], 23))


# Idee: Gehen Sie die Indizes von vorn nach hinten durch und vergleichen Sie jedes Element mit
# dem gesuchten Wert. Beim ersten Treffer geben Sie sofort den Index zurück. Erst wenn die
# Schleife ganz durchgelaufen ist, steht fest, dass der Wert fehlt; dann kommt -1 zurück.
#
# Anderer Weg: for index, element in enumerate(liste) liefert Index und Element zugleich.
# Mit fertigen Mitteln ginge es als liste.index(gesucht) if gesucht in liste else -1; das sieht
# die Liste aber bis zu zweimal durch und war hier nicht erlaubt.
#
# Typische Fehler: return -1 in einem else-Zweig innerhalb der Schleife (dann wird nur das erste
# Element angesehen) oder ohne return weiterlaufen und so das letzte statt des ersten
# Vorkommens liefern.
#
# Laufzeit: O(n). Im schlechtesten Fall (Wert fehlt oder steht ganz hinten) wird jedes der
# n Elemente genau einmal verglichen.
