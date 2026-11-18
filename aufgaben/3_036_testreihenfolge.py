"""Aufgabe 3_036 – Reihenfolge im Usability-Test                 Stufe 3 ★★★☆☆

Ein Team hat drei Entwürfe für die Startseite einer App gebaut und lässt
sie in einem Usability-Test von Testpersonen ausprobieren. Wer einen
Entwurf als zweiten oder dritten sieht, kennt die App schon ein wenig und
kommt schneller zurecht. Damit dieser Lerneffekt nicht einen Entwurf
bevorzugt, bekommt jede Testperson die Entwürfe in einer anderen
Reihenfolge, und am Ende soll jede mögliche Reihenfolge gleich oft
vorgekommen sein. Dafür braucht das Team erst einmal die Liste aller
Reihenfolgen. Zwei Entwürfe sehen sich so ähnlich, dass sie nicht direkt
nacheinander gezeigt werden sollen.

- `alle_reihenfolgen(entwuerfe)` bekommt eine Liste von Namen und liefert
  eine Liste aller Reihenfolgen. Jede Reihenfolge ist eine Liste, die jeden
  Namen genau einmal enthält; jede Reihenfolge kommt genau einmal vor. In
  welcher Reihenfolge die Reihenfolgen in der Ergebnisliste stehen, ist
  egal.
- `ohne_nachbarn(entwuerfe, a, b)` liefert nur die Reihenfolgen, in denen a
  und b nicht direkt nebeneinander stehen (weder a vor b noch b vor a).
  Benutzen Sie dafür alle_reihenfolgen.

    alle_reihenfolgen(["Kacheln", "Liste"])
        →  [["Kacheln", "Liste"], ["Liste", "Kacheln"]]
    alle_reihenfolgen(["A", "B", "C"])
        →  [["A", "B", "C"], ["A", "C", "B"], ["B", "A", "C"],
            ["B", "C", "A"], ["C", "A", "B"], ["C", "B", "A"]]
    ohne_nachbarn(["A", "B", "C"], "A", "B")
        →  [["A", "C", "B"], ["B", "C", "A"]]

Lösen Sie alle_reihenfolgen rekursiv und ohne itertools.

Grenzen: 0 ≤ len(entwuerfe) ≤ 8, die Namen sind verschiedene, nicht leere
Texte. Für die leere Liste gibt es genau eine Reihenfolge, die leere:
alle_reihenfolgen([]) → [[]]. Bei ohne_nachbarn sind a und b zwei
verschiedene Namen aus entwuerfe. Bei n Entwürfen gibt es
n · (n - 1) · … · 1 Reihenfolgen, bei 8 also 40 320. Die Liste entwuerfe
darf nicht verändert werden.

Hintergrund: Eine Reihenfolge aller Elemente heißt Permutation. Man findet
alle rekursiv mit derselben Idee wie in Aufgabe 2_044 beim Zählen: Jedes
Element kann vorne stehen; dahinter folgt eine beliebige Reihenfolge der
übrigen Elemente. Die übrigen sind eine kürzere Liste, also dasselbe
Problem in klein. Die Abbruchbedingung ist die leere Liste mit ihrer
einzigen, leeren Reihenfolge.

    def alle_reihenfolgen(entwuerfe):
        if entwuerfe == []:
            return [[]]
        ergebnis = []
        for stelle in range(len(entwuerfe)):
            vorne = entwuerfe[stelle]
            rest = entwuerfe[:stelle] + entwuerfe[stelle + 1:]
            for hinten in alle_reihenfolgen(rest):
                ergebnis.append(...)       # vorne, dann hinten
        return ergebnis

Der Rest entsteht durch Slicing als neue Liste, so bleibt entwuerfe
unverändert. Bei n Elementen gibt es n Möglichkeiten für vorne und für
jede (n - 1)! Reihenfolgen des Rests, zusammen n!. Schneller als n! geht
es nicht, weil jede Reihenfolge einmal hingeschrieben werden muss; schon
bei 12 Elementen wären es fast eine halbe Milliarde. Rekursion mit Listen
kennen Sie aus Aufgabe 3_034, das Durchprobieren aller Möglichkeiten aus
Aufgabe 3_035.

Tipp: Zwei Listen hängt man mit + aneinander: [vorne] + hinten.
"""


def alle_reihenfolgen(entwuerfe):
    """Gibt alle Reihenfolgen der Entwürfe als Liste von Listen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ohne_nachbarn(entwuerfe, a, b):
    """Gibt alle Reihenfolgen zurück, in denen a und b nicht direkt nebeneinander stehen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(alle_reihenfolgen(["Kacheln", "Liste"]))
