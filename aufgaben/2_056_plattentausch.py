"""Aufgabe 2_056 – Plattentausch                                  Stufe 2 ★★☆☆☆

Im Rechenzentrum stehen zwei Speicherregale voller Festplatten. Jede
Festplatte zählt ihre Betriebsstunden; ab einer bestimmten Zahl von
Stunden fallen Platten deutlich häufiger aus, deshalb tauscht das Team
sie vorher vorsorglich aus. Jedes Regal liefert eine Liste aus Paaren
(seriennummer, stunden), aufsteigend nach Betriebsstunden sortiert:

    regal_a = [("A7", 1200), ("A2", 30500), ("A9", 41000)]
    regal_b = [("B4", 800), ("B1", 35000), ("B3", 52000)]

Einige Platten sind schon ausgefallen; für sie ist der Ersatz längst
bestellt, sie gehören nicht mehr in die Planung:

    defekte = ["B1"]

Schreiben Sie vier Funktionen, die je eine neue Liste oder eine Zahl
zurückgeben und die übergebenen Listen nicht verändern:

- `ohne_defekte(platten, defekte)`: alle Paare aus platten, deren
  Seriennummer nicht in defekte steht, in ihrer Reihenfolge.
- `zusammenfuehren(regal_a, regal_b)`: alle Paare beider Listen,
  aufsteigend nach Stunden; bei gleichen Stunden kommt das Paar aus
  regal_a zuerst, und innerhalb einer Liste bleibt die Reihenfolge.
- `erste_ab(platten, grenze)`: die Position des ersten Paars mit
  mindestens grenze Stunden in der sortierten Liste platten, oder -1,
  wenn es keins gibt.
- `tauschliste(regal_a, regal_b, defekte, grenze)`: alle Platten beider
  Regale, die nicht defekt sind und mindestens grenze Stunden haben,
  aufsteigend nach Stunden. Benutzen Sie dafür die drei Funktionen oben.

    ohne_defekte(regal_b, defekte)     →  [("B4", 800), ("B3", 52000)]
    erste_ab(regal_a, 30000)           →  1
    tauschliste(regal_a, regal_b, defekte, 30000)
    →  [("A2", 30500), ("A9", 41000), ("B3", 52000)]

Benutzen Sie weder sort() noch sorted().

Grenzen: Jedes Regal hat 0 bis 20 000 Paare, aufsteigend nach Stunden
sortiert. Die Seriennummern sind verschiedene, nicht leere Texte, die
Stunden ganze Zahlen von 0 bis 100 000, gleiche kommen vor. defekte hat
0 bis 10 Seriennummern, auch solche, die in keinem Regal stehen.
grenze ist eine ganze Zahl von 0 bis 100 000. tauschliste soll höchstens
etwa 30 · (Länge von regal_a + Länge von regal_b) Schritte brauchen.

Hintergrund: Diese Übung setzt drei Listen-Algorithmen zusammen, die
Sie einzeln kennen. Entfernen: eine neue Liste anlegen und nur die
Paare anhängen, die bleiben sollen, wie in Aufgabe 2_054; ob eine
Seriennummer in defekte steht, sagt nummer in defekte. Zusammenführen:
zwei Stellen i und j und eine while-Schleife, die immer das kleinere der
beiden vordersten Paare übernimmt, wie in Aufgabe 2_055. Suchen: die
Liste von vorn durchgehen und beim ersten Treffer seine Position
zurückgeben, wie bei der Suche nach dem Maximum in Aufgabe 2_053, nur
dass man hier sofort aufhören darf. Weil die zusammengeführte Liste
sortiert ist, stehen alle Platten ab dieser Position auf oder über der Grenze,
und liste[position:] (Slicing, Aufgabe 2_018) liefert sie auf einmal.
Wer jede Aufgabe einmal in einer eigenen Funktion löst, kann sie danach
wie Bausteine verbinden und jeden Baustein für sich prüfen.
"""


def ohne_defekte(platten, defekte):
    """Gibt eine neue Liste ohne die Paare zurück, deren Seriennummer in defekte steht."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zusammenfuehren(regal_a, regal_b):
    """Gibt eine neue, nach Stunden sortierte Liste mit allen Paaren beider Listen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def erste_ab(platten, grenze):
    """Gibt die Position des ersten Paars mit mindestens grenze Stunden zurück, sonst -1."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def tauschliste(regal_a, regal_b, defekte, grenze):
    """Gibt alle nicht defekten Platten mit mindestens grenze Stunden zurück, aufsteigend nach Stunden."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


regal_a = [("A7", 1200), ("A2", 30500), ("A9", 41000)]
regal_b = [("B4", 800), ("B1", 35000), ("B3", 52000)]
print(tauschliste(regal_a, regal_b, ["B1"], 30000))
