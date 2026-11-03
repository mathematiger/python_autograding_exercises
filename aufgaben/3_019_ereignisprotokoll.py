"""Aufgabe 3_019 – Ereignisprotokoll                             Stufe 3 ★★★☆☆

Eine Versicherung will wissen, wie ihre Schadensmeldungen tatsächlich
bearbeitet werden. Das Bearbeitungssystem schreibt dafür ein
Ereignisprotokoll: Jedes Mal, wenn an einem Fall ein Schritt erledigt
wird, kommt ein Tupel (fallnummer, schritt) dazu, in zeitlicher
Reihenfolge und für alle Fälle durcheinander.

    protokoll = [
        (101, "eingang"), (102, "eingang"), (101, "pruefung"),
        (103, "eingang"), (101, "abschluss"), (102, "pruefung"),
        (102, "rueckfrage"), (102, "pruefung"),
    ]

Schreiben Sie drei Funktionen, die jeweils eine Menge zurückgeben:

- `schritte(protokoll)` gibt alle verschiedenen Schritte zurück, die im
  Protokoll vorkommen.
- `faelle_mit(protokoll, schritt)` gibt die Nummern der Fälle zurück, an
  denen der Schritt mindestens einmal erledigt wurde.
- `offene_faelle(protokoll)` gibt die Nummern der Fälle zurück, die im
  Protokoll vorkommen, aber noch keinen Schritt "abschluss" haben.

    schritte(protokoll)                   →  {"eingang", "pruefung", "abschluss", "rueckfrage"}
    faelle_mit(protokoll, "pruefung")     →  {101, 102}
    offene_faelle(protokoll)              →  {102, 103}

Schreiben Sie alle drei Funktionen mit Set Comprehensions, ohne for-
oder while-Schleife als eigene Anweisung.

Grenzen: protokoll hat 0 bis 100 000 Einträge. Fallnummern sind ganze
Zahlen von 1 bis 10**9, Schritte nicht leere Texte aus Kleinbuchstaben.
Derselbe Schritt kann an einem Fall mehrmals vorkommen. schritt in
faelle_mit ist ein nicht leerer Text, der nicht im Protokoll vorkommen
muss. Das Protokoll bleibt unverändert.

Hintergrund: Eine Set Comprehension sieht aus wie eine List
Comprehension (Aufgabe 3_017), steht aber in geschweiften Klammern ohne
Doppelpunkt (mit Doppelpunkt wäre sie eine Dict Comprehension, Aufgabe
3_018). Sie baut eine Menge, also eine Sammlung ohne Reihenfolge, in der
jeder Wert nur einmal vorkommt; Doppelte fallen von selbst weg:

    orte = {kunde["ort"] for kunde in kunden}
    grosse = {nummer for nummer, betrag in rechnungen if betrag > 1000}

Mengen kann man wie in der Mathematik verknüpfen: a | b ist die
Vereinigung, a & b der Schnitt und a - b enthält alles aus a, was nicht
in b ist. Ob ein Wert in einer Menge liegt, prüft wert in menge im
Mittel in O(1), bei einer Liste braucht dasselbe O(n). Achtung: {} ist
ein leeres Dictionary, eine leere Menge schreibt man set().
"""


def schritte(protokoll):
    """Gibt die Menge aller Schritte im Protokoll zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def faelle_mit(protokoll, schritt):
    """Gibt die Menge der Fälle zurück, an denen schritt erledigt wurde."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def offene_faelle(protokoll):
    """Gibt die Menge der Fälle ohne Schritt "abschluss" zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokoll = [
    (101, "eingang"), (102, "eingang"), (101, "pruefung"),
    (103, "eingang"), (101, "abschluss"), (102, "pruefung"),
    (102, "rueckfrage"), (102, "pruefung"),
]
print(sorted(schritte(protokoll)))
print(sorted(faelle_mit(protokoll, "pruefung")))
print(sorted(offene_faelle(protokoll)))
