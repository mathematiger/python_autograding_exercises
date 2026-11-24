# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_047_ersatzteillager.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_047_ersatzteillager

"""Aufgabe 2_047 – Ersatzteillager                               Stufe 2 ★★☆☆☆

Im Ersatzteillager des IT-Supports liegen Netzteile in Kartons
unterschiedlicher Größe auf einem Stapel, der größte unten, der
kleinste oben. Der Stapel soll vom Regalfach A ins Fach C umziehen; Fach
B darf dabei als Zwischenablage dienen. Weil die Kartons empfindlich
sind, gelten zwei Regeln: Man trägt immer nur einen Karton, und nie darf
ein größerer Karton auf einem kleineren liegen. Das ist genau das Rätsel
„Türme von Hanoi“, mit dem die Vorlesung MIT 6.0001 (Lecture 6) die
Rekursion vorführt.

Vervollständigen Sie die Funktion `umlagern(n, start, ziel, hilf)`. Sie
gibt die Liste aller Züge zurück, mit denen n Kartons vom Fach start ins
Fach ziel kommen; ein Zug ist ein Tupel (von, nach). Schreiben Sie sie
rekursiv, ohne for und ohne while:

- Bei 0 Kartons ist nichts zu tun: die leere Liste.
- Sonst legt man erst die oberen n - 1 Kartons von start nach hilf
  (über ziel), dann trägt man den größten Karton von start nach ziel,
  zuletzt legt man die n - 1 Kartons von hilf nach ziel (über start).

    umlagern(1, "A", "C", "B")  →  [("A", "C")]
    umlagern(2, "A", "C", "B")  →  [("A", "B"), ("A", "C"), ("B", "C")]
    len(umlagern(3, "A", "C", "B"))  →  7
    umlagern(0, "A", "C", "B")  →  []

Grenzen: 0 ≤ n ≤ 15. start, ziel und hilf sind drei verschiedene, nicht
leere Texte.

Hintergrund: Eine rekursive Funktion ruft sich selbst mit einem
kleineren Problem auf, bis sie bei einem Fall ankommt, dessen Antwort
sie direkt kennt (Aufgabe 2_044). Hier ruft sie sich sogar zweimal auf,
jedes Mal mit einem Karton weniger, und baut aus den beiden Teillisten
und dem einen Zug dazwischen die ganze Liste. Listen verbindet man mit
+, und ein Tupel aus zwei Werten schreibt man in runde Klammern:

    erste = [("A", "B")]
    zweite = [("B", "C")]
    erste + [("A", "C")] + zweite  →  [("A", "B"), ("A", "C"), ("B", "C")]

Man muss sich die einzelnen Züge nicht selbst ausdenken: Es genügt, sich
darauf zu verlassen, dass der Aufruf für n - 1 Kartons schon richtig
arbeitet. Weil jeder Karton mehr die Zahl der Züge verdoppelt (plus
einen), braucht man für n Kartons 2**n - 1 Züge.
"""


def umlagern(n, start, ziel, hilf):
    """Gibt die Liste der Züge (von, nach) zurück, die n Kartons von start nach ziel bringen."""
    if n == 0:
        return []
    davor = umlagern(n - 1, start, hilf, ziel)
    danach = umlagern(n - 1, hilf, ziel, start)
    return davor + [(start, ziel)] + danach


print(umlagern(2, "A", "C", "B"))
print(len(umlagern(3, "A", "C", "B")), "Züge für 3 Kartons")


# Idee: Bei 0 Kartons ist die Liste leer (Abbruchbedingung). Sonst verlässt man sich auf zwei
# Aufrufe mit n - 1 Kartons: Der erste schafft die oberen n - 1 Kartons von start nach hilf, dann
# kommt der Zug (start, ziel) für den größten Karton, und der zweite Aufruf holt die n - 1 Kartons
# von hilf nach ziel. Die drei Teile werden mit + zu einer Liste verbunden.
# Anderer Weg: Als Abbruchbedingung n == 1 mit dem einzigen Zug [(start, ziel)], dann aber n == 0
# zusätzlich abfangen; oder die Züge der inneren Aufrufe mit extend an eine Liste anhängen, statt
# drei Listen mit + zu verbinden.
# Typische Fehler: in den inneren Aufrufen ziel und hilf nicht vertauschen (dann landen die oberen
# Kartons am falschen Ort), feste Namen "A", "B", "C" statt der Parameter, nur n == 1 als
# Abbruchbedingung (dann läuft n == 0 in einen RecursionError) oder das Ergebnis der inneren
# Aufrufe nicht verwenden.
# Laufzeit: 2**n - 1 Züge, also exponentiell; jeder Karton mehr verdoppelt die Zahl der Züge. Weil +
# die Teillisten jedes Mal kopiert, sind es insgesamt etwa n · 2**n kopierte Züge; bei n ≤ 15 spielt
# das keine Rolle.
