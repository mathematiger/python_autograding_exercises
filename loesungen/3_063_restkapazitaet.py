# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_063_restkapazitaet.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_063_restkapazitaet

"""Aufgabe 3_063 – Restkapazität                                 Stufe 3 ★★★☆☆

Ein Entwicklungsteam arbeitet mit einem Kanban-Board. Neben den großen
Aufgaben führt es eine Liste kleiner Aufräumarbeiten (Abhängigkeit
aktualisieren, Warnung beseitigen, Test ergänzen), jede mit ihrem
geschätzten Aufwand in Minuten. Die Liste ist nicht sortiert, sondern
steht in der Reihenfolge, in der die Einträge angelegt wurden, der
älteste vorn. Fällt für eine Entwicklerin ein Termin aus, hat sie frei
Minuten übrig. Sie will dann genau zwei Einträge der Liste erledigen,
die diese Zeit zusammen genau füllen. Schreiben Sie zwei Funktionen:

- `paar_fuer(aufwaende, frei)` gibt ein Paar (i, j) von Positionen mit
  i < j zurück, für das aufwaende[i] + aufwaende[j] == frei ist, oder
  None, wenn es keins gibt. Gibt es mehrere, soll das Paar herauskommen,
  das beim Durchgehen der Liste von vorn als erstes vollständig ist:
  j so klein wie möglich und dazu der früheste passende Partner i.
- `anzahl_paare(aufwaende, frei)` gibt zurück, wie viele Paare (i, j)
  mit i < j es gibt, für die aufwaende[i] + aufwaende[j] == frei ist.
  Damit sieht die Teamleitung im Daily, wie viel Auswahl es gibt.

    aufwaende = [90, 240, 45, 120, 300, 75, 120, 165]
    paar_fuer(aufwaende, 165)      →  (2, 3)    (45 + 120)
    paar_fuer(aufwaende, 240)      →  (3, 6)    (120 + 120)
    paar_fuer(aufwaende, 500)      →  None
    anzahl_paare(aufwaende, 165)   →  3         ((2, 3), (0, 5), (2, 6))

Bei frei = 165 passen auch (0, 5) und (2, 6); vollständig ist aber
zuerst (2, 3), denn schon an Position 3 hat man mit 45 und 120 ein
passendes Paar gesehen. Zwei Einträge dürfen gleich viel Aufwand haben,
ein Eintrag darf aber nicht mit sich selbst gepaart werden.

Grenzen: aufwaende hat 0 bis 100 000 Einträge, ganze Zahlen von 1 bis
100 000, nicht sortiert, Doppelte möglich. frei ist eine ganze Zahl von
1 bis 200 000. Beide Funktionen sollen O(n) Schritte brauchen, also
höchstens einige Zugriffe auf aufwaende je Eintrag.

Hintergrund: Naiv probiert man mit zwei verschachtelten Schleifen jedes
Paar, das sind O(n²) Schritte (Aufgabe 3_006). In Aufgabe 3_060 ging es
schneller, weil die Liste sortiert war: zwei Zeiger, O(n). Hier ist sie
unsortiert, und Sortieren würde O(n log n) kosten und die Positionen
durcheinanderbringen. Es geht aber in einem einzigen Durchgang ohne
Sortieren: Steht man bei einem Wert x, braucht man als Partner genau
frei - x, und man fragt nur, ob dieser Wert schon weiter vorn
vorkam. Dazu merkt man sich die bisher gesehenen Werte in einer Menge
(Aufgabe 2_028):

    gesehen = set()
    for wert in werte:
        if frei - wert in gesehen:
            ...                    # Paar gefunden
        gesehen.add(wert)

Die Frage frei - wert in gesehen kostet bei einer Menge im Mittel O(1)
(Aufgabe 3_019): Python rechnet aus dem Wert direkt aus, an welcher
Stelle er gespeichert sein müsste, und schaut nur dort nach. Dieselbe
Frage an die Liste, frei - wert in werte, geht dagegen alle Einträge
durch, und man ist wieder bei O(n²). Weil erst gefragt und danach
hinzugefügt wird, paart sich ein Wert nie mit sich selbst. Braucht man
mehr als ja oder nein, nimmt man statt der Menge ein Dictionary: für die
Positionen eines, das jeden Wert auf seine Position abbildet, für die
Anzahl eines, das wie in Aufgabe 2_025 zählt, wie oft jeder Wert schon
vorkam. Man tauscht also Speicher gegen Zeit.
"""


def paar_fuer(aufwaende, frei):
    """Gibt das zuerst vollständige Paar (i, j) mit aufwaende[i] + aufwaende[j] == frei zurück, oder None."""
    erste_position = {}
    for j in range(len(aufwaende)):
        wert = aufwaende[j]
        partner = frei - wert
        if partner in erste_position:
            return (erste_position[partner], j)
        if wert not in erste_position:
            erste_position[wert] = j
    return None


def anzahl_paare(aufwaende, frei):
    """Gibt die Anzahl der Paare i < j mit aufwaende[i] + aufwaende[j] == frei zurück."""
    bisher = {}
    anzahl = 0
    for wert in aufwaende:
        partner = frei - wert
        if partner in bisher:
            anzahl += bisher[partner]
        if wert in bisher:
            bisher[wert] += 1
        else:
            bisher[wert] = 1
    return anzahl


aufwaende = [90, 240, 45, 120, 300, 75, 120, 165]
print(paar_fuer(aufwaende, 165))
print(anzahl_paare(aufwaende, 165))


# Idee: Gehen Sie die Liste einmal von vorn durch. Für den Eintrag an Position j ist der passende
# Partner frei - aufwaende[j]. paar_fuer merkt sich in einem Dictionary zu jedem Aufwand die Position,
# an der er zum ersten Mal vorkam; ist der Partner schon darin, ist (erste Position des Partners, j)
# das zuerst vollständige Paar. anzahl_paare zählt stattdessen, wie oft jeder Aufwand schon vorkam,
# und addiert bei jedem Eintrag die Anzahl seiner früheren Partner. Erst fragen, dann eintragen,
# sonst paart sich ein Eintrag mit sich selbst.
# Anderer Weg: Naiv zwei verschachtelte Schleifen über alle Paare, O(n²). Oder die Paare (Aufwand,
# Position) sortieren und mit zwei Zeigern wie in Aufgabe 3_060 suchen: O(n log n), und das zuerst
# vollständige Paar zu finden wird mühsam. Für die Anzahl kann man auch erst alle Häufigkeiten zählen
# und dann für jeden Wert w häufigkeit[w] · häufigkeit[frei - w] addieren; gleiche Partner
# (w == frei - w) zählen dann k · (k - 1) / 2-mal, und jedes Paar darf nur einmal zählen.
# Typische Fehler: den eigenen Eintrag vor der Frage eintragen, die Position eines Doppelten
# überschreiben (dann kommt der späteste statt des frühesten Partners heraus), frei - wert in aufwaende
# auf der Liste fragen (wieder O(n²)), bei der Anzahl nur 1 statt der Zahl früherer Partner addieren.
# Laufzeit: O(n), denn jeder Eintrag wird einmal gelesen, und Nachschlagen und Eintragen im
# Dictionary kosten im Mittel O(1).
