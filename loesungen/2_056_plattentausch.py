# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_056_plattentausch.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_056_plattentausch

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
    ergebnis = []
    for nummer, stunden in platten:
        if nummer not in defekte:
            ergebnis.append((nummer, stunden))
    return ergebnis


def zusammenfuehren(regal_a, regal_b):
    """Gibt eine neue, nach Stunden sortierte Liste mit allen Paaren beider Listen zurück."""
    ergebnis = []
    i = 0
    j = 0
    while i < len(regal_a) and j < len(regal_b):
        if regal_a[i][1] <= regal_b[j][1]:
            ergebnis.append(regal_a[i])
            i += 1
        else:
            ergebnis.append(regal_b[j])
            j += 1
    while i < len(regal_a):
        ergebnis.append(regal_a[i])
        i += 1
    while j < len(regal_b):
        ergebnis.append(regal_b[j])
        j += 1
    return ergebnis


def erste_ab(platten, grenze):
    """Gibt die Position des ersten Paars mit mindestens grenze Stunden zurück, sonst -1."""
    for position in range(len(platten)):
        if platten[position][1] >= grenze:
            return position
    return -1


def tauschliste(regal_a, regal_b, defekte, grenze):
    """Gibt alle nicht defekten Platten mit mindestens grenze Stunden zurück, aufsteigend nach Stunden."""
    alle = zusammenfuehren(ohne_defekte(regal_a, defekte), ohne_defekte(regal_b, defekte))
    position = erste_ab(alle, grenze)
    if position == -1:
        return []
    return alle[position:]


regal_a = [("A7", 1200), ("A2", 30500), ("A9", 41000)]
regal_b = [("B4", 800), ("B1", 35000), ("B3", 52000)]
print(tauschliste(regal_a, regal_b, ["B1"], 30000))


# Idee: Jede Teilaufgabe bekommt ihre eigene Funktion. ohne_defekte baut eine neue Liste und hängt nur
# Paare an, deren Nummer nicht in defekte steht; zusammenfuehren läuft mit zwei Stellen i und j durch
# beide Listen (bei Gleichstand regal_a zuerst, also <=); erste_ab sucht von vorn die erste Position mit
# stunden >= grenze. tauschliste entfernt erst die Defekten in beiden Regalen, führt zusammen und gibt
# ab der gefundenen Position alles zurück, denn in der sortierten Liste liegen dahinter nur gleiche oder größere Werte.
# Anderer Weg: zuerst zusammenführen und dann die Defekten entfernen. Naiv wäre, jede Platte von
# regal_b an die passende Stelle einzusortieren; das braucht bis zu n · m Vergleiche.
# Typische Fehler: > statt >= bei der Grenze, -1 von erste_ab direkt in alle[-1:] stecken (liefert das
# letzte Paar statt einer leeren Liste), mit remove aus den übergebenen Listen löschen, < statt <= beim
# Zusammenführen (bei Gleichstand käme Regal B zuerst).
