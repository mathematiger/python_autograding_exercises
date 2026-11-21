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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(umlagern(2, "A", "C", "B"))
print(len(umlagern(3, "A", "C", "B")), "Züge für 3 Kartons")
