"""Aufgabe 3_036 – Menüreihenfolge                               Stufe 3 ★★★☆☆

Eine App bekommt ein neues Hauptmenü mit wenigen Einträgen. Bei einem
Usability-Test sollen Testpersonen das Menü in jeder möglichen
Reihenfolge der Einträge ausprobieren; danach wertet das Team aus, in
welcher Reihenfolge die Aufgaben am schnellsten erledigt wurden. Dafür
braucht es eine Liste aller Reihenfolgen, also aller Permutationen.

Vervollständigen Sie die rekursive Funktion `alle_reihenfolgen(eintraege)`.
Sie gibt eine Liste zurück, in der jede Reihenfolge der Einträge genau
einmal als Liste vorkommt. Die Reihenfolgen sollen so geordnet sein:
zuerst alle, die mit dem ersten Eintrag beginnen, dann alle mit dem
zweiten Eintrag vorn und so weiter; innerhalb dieser Gruppen gilt für
den Rest dieselbe Regel.

    alle_reihenfolgen(["Start", "Suche", "Profil"])
    →  [["Start", "Suche", "Profil"], ["Start", "Profil", "Suche"],
        ["Suche", "Start", "Profil"], ["Suche", "Profil", "Start"],
        ["Profil", "Start", "Suche"], ["Profil", "Suche", "Start"]]
    alle_reihenfolgen(["Start"])   →  [["Start"]]
    alle_reihenfolgen([])          →  [[]]      (genau eine Reihenfolge: die leere)

Benutzen Sie dafür nicht itertools.permutations. Die übergebene Liste
darf nicht verändert werden.

Grenzen: 0 ≤ len(eintraege) ≤ 7. Die Einträge sind verschiedene Texte
(keine Doppelten). Bei n Einträgen gibt es n! Reihenfolgen, bei 7 also
5040.

Hintergrund: In Aufgabe 3_035 haben Sie alle Teilmengen rekursiv
erzeugt: Für jedes Element gibt es zwei Möglichkeiten, dabei oder nicht.
Bei Permutationen fragt man stattdessen: Welcher Eintrag kommt an die
erste Stelle? Jeder kommt in Frage. Hat man ihn gewählt, bleibt eine
kleinere Aufgabe derselben Art übrig: alle Reihenfolgen der übrigen
Einträge. Vor jede davon setzt man den gewählten Eintrag:

    für jeden Index i:
        erster = eintraege[i]
        rest = eintraege[:i] + eintraege[i + 1:]     # alle außer dem i-ten
        für jede Reihenfolge r in alle_reihenfolgen(rest):
            [erster] + r ist eine Reihenfolge

Die Abbruchbedingung ist die leere Liste: Sie hat genau eine
Reihenfolge, die leere Liste []. Mit [[]] als Ergebnis funktioniert dann
auch ein einzelner Eintrag von selbst: [erster] + [] ergibt [erster].
Gäbe die leere Liste dagegen [] zurück (keine Reihenfolge), käme aus der
Rekursion nie etwas heraus.
"""


def alle_reihenfolgen(eintraege):
    """Gibt alle Reihenfolgen der Einträge als Liste von Listen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(alle_reihenfolgen(["Start", "Suche", "Profil"]))
