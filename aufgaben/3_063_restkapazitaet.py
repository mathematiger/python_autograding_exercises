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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def anzahl_paare(aufwaende, frei):
    """Gibt die Anzahl der Paare i < j mit aufwaende[i] + aufwaende[j] == frei zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


aufwaende = [90, 240, 45, 120, 300, 75, 120, 165]
print(paar_fuer(aufwaende, 165))
print(anzahl_paare(aufwaende, 165))
