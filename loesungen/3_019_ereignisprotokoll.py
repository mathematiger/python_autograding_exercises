# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_019_ereignisprotokoll.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_019_ereignisprotokoll

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
    return {schritt for _, schritt in protokoll}


def faelle_mit(protokoll, schritt):
    """Gibt die Menge der Fälle zurück, an denen schritt erledigt wurde."""
    return {fall for fall, erledigt in protokoll if erledigt == schritt}


def offene_faelle(protokoll):
    """Gibt die Menge der Fälle ohne Schritt "abschluss" zurück."""
    alle = {fall for fall, _ in protokoll}
    return alle - faelle_mit(protokoll, "abschluss")


protokoll = [
    (101, "eingang"), (102, "eingang"), (101, "pruefung"),
    (103, "eingang"), (101, "abschluss"), (102, "pruefung"),
    (102, "rueckfrage"), (102, "pruefung"),
]
print(sorted(schritte(protokoll)))
print(sorted(faelle_mit(protokoll, "pruefung")))
print(sorted(offene_faelle(protokoll)))


# Idee: Jede Funktion ist im Kern eine Set Comprehension über die Tupel des Protokolls, die man gleich
# in fall, schritt auspackt. schritte sammelt nur den Schritt, faelle_mit nur den Fall, wenn der Schritt
# passt; doppelte Werte fallen in der Menge von selbst weg. offene_faelle bildet die Menge aller Fälle und
# zieht mit - die Menge der Fälle mit "abschluss" ab, die faelle_mit schon liefert.
#
# Anderer Weg: set([schritt for _, schritt in protokoll]) baut erst eine Liste und daraus die Menge;
# das rechnet richtig, braucht aber unnötig Speicher und besteht hier nicht, weil die Aufgabe Set
# Comprehensions verlangt. Für offene_faelle geht auch {fall for fall, _ in protokoll
# if fall not in abgeschlossen} mit abgeschlossen = faelle_mit(protokoll, "abschluss"). Naiv wäre, für
# jeden Fall das ganze Protokoll nach "abschluss" zu durchsuchen: O(n²), bei 100 000 Einträgen zu langsam.
#
# Typische Fehler: [ ] statt { } (Liste mit Doppelten), {} für die leere Menge (das ist ein Dictionary),
# alle Fälle mit einem anderen Schritt als "abschluss" für offen halten (Fall 101 hat auch "eingang") oder
# fall not in abgeschlossen mit einer Liste abgeschlossen prüfen (O(n) je Test; bei vielen
# abgeschlossenen Fällen wird das sehr langsam).
#
# Laufzeit: Jede Comprehension sieht jeden der n Einträge einmal an, Einfügen in eine Menge und die
# Differenz zweier Mengen kosten im Mittel O(1) je Element; zusammen O(n).
