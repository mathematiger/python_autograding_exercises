# Automatisch erzeugt aus lehrkraft/muster/3_027_backlog_ordnen.py - nicht von Hand ändern.
# vorlage-hash: c3cf4114cc34cda2
# text-hash: 6421a3d2cba88ee2
# thema: funktionen
# inhalt: sorted mit key

BEISPIEL = [("Login", 1, 5), ("Export", 2, 3), ("Suche", 1, 3), ("Hilfe", 3, 1), ("Bericht", 2, 3)]

# nach_aufwand aus dem Beispiel: gleiche Punkte behalten ihre Reihenfolge
daten = list(BEISPIEL)
ergebnis = nach_aufwand(daten)
erwartet = [("Hilfe", 3, 1), ("Export", 2, 3), ("Suche", 1, 3), ("Bericht", 2, 3), ("Login", 1, 5)]
assert ergebnis == erwartet, (
    f"nach_aufwand(<Beispiel>) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Sortieren Sie nur nach den Punkten, key=lambda eintrag: eintrag[2]; sorted ist stabil und lässt "
    "Einträge mit gleich vielen Punkten in ihrer Reihenfolge. Ein zweites Kriterium würde sie umordnen."
)

# planungsreihenfolge aus dem Beispiel
ergebnis = planungsreihenfolge(daten)
erwartet = [("Suche", 1, 3), ("Login", 1, 5), ("Bericht", 2, 3), ("Export", 2, 3), ("Hilfe", 3, 1)]
assert ergebnis == erwartet, (
    f"planungsreihenfolge(<Beispiel>) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Der Schlüssel ist ein Tupel aus Priorität, Punkten und Titel, genau in dieser Reihenfolge."
)

# groesste_brocken aus dem Beispiel
ergebnis = groesste_brocken(daten, 3)
assert ergebnis == ["Login", "Bericht", "Export"], (
    f"groesste_brocken(<Beispiel>, 3) ergibt {ergebnis!r}, erwartet war ['Login', 'Bericht', 'Export'].\n"
    "Tipp: Die meisten Punkte zuerst, aber die Titel alphabetisch: key=lambda eintrag: (-eintrag[2], eintrag[0]). "
    "reverse=True würde auch die Titel umdrehen."
)

# backlog bleibt unverändert
assert daten == BEISPIEL, f"Nach den Aufrufen ist backlog {daten!r}, erwartet war unverändert {BEISPIEL!r}."

# Ergebnis ist eine neue Liste, auch wenn schon alles sortiert ist
daten = [("A", 1, 1), ("B", 1, 2)]
ergebnis = nach_aufwand(daten)
assert ergebnis == daten and ergebnis is not daten, (
    f"nach_aufwand({daten}) soll eine neue, gleiche Liste liefern; bekommen {ergebnis!r}"
    f"{' (die übergebene Liste selbst)' if ergebnis is daten else ''}."
)

# Doppelte Titel und Priorität entscheidet vor Punkten
daten = [("Fix", 2, 1), ("Fix", 1, 8), ("Abc", 1, 8), ("Zoo", 1, 2)]
ergebnis = planungsreihenfolge(daten)
erwartet = [("Zoo", 1, 2), ("Abc", 1, 8), ("Fix", 1, 8), ("Fix", 2, 1)]
assert ergebnis == erwartet, f"planungsreihenfolge({daten}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# groesste_brocken mit anzahl 0, mehr als vorhanden und doppelten Titeln
daten = [("Api", 1, 13), ("Db", 2, 40), ("Api", 3, 40)]
ergebnis = (groesste_brocken(daten, 0), groesste_brocken(daten, 5), groesste_brocken(daten, 2))
erwartet = ([], ["Api", "Db", "Api"], ["Api", "Db"])
assert ergebnis == erwartet, (
    f"groesste_brocken({daten}, …) mit anzahl 0, 5 und 2 ergibt {ergebnis!r}, erwartet war {erwartet!r}."
)

# Leeres Backlog
ergebnis = (nach_aufwand([]), planungsreihenfolge([]), groesste_brocken([], 3))
assert ergebnis == ([], [], []), f"Für ein leeres Backlog ergeben die drei Funktionen {ergebnis!r}, erwartet war ([], [], [])."

# Ränder: Punkte 1 und 100, Prioritäten 1 und 5
daten = [("Klein", 5, 1), ("Riesig", 5, 100), ("Dringend", 1, 100), ("Mini", 1, 1)]
ergebnis = (planungsreihenfolge(daten), groesste_brocken(daten, 2))
erwartet = ([("Mini", 1, 1), ("Dringend", 1, 100), ("Klein", 5, 1), ("Riesig", 5, 100)], ["Dringend", "Riesig"])
assert ergebnis == erwartet, f"Für {daten} ergeben planungsreihenfolge und groesste_brocken(…, 2) {ergebnis!r}, erwartet war {erwartet!r}."

# sorted wird benutzt
assert verwendet("sorted"), "Benutzen Sie in allen drei Funktionen sorted mit dem Parameter key."


# Vergleichslösungen ohne key: Einfügen von Hand, stabil
def einfuegen_sortiert(eintraege, kommt_vor):
    """Sortiert stabil durch Einfügen; kommt_vor(a, b) sagt, ob a echt vor b gehört."""
    ergebnis = []
    for eintrag in eintraege:
        stelle = len(ergebnis)
        while stelle > 0 and kommt_vor(eintrag, ergebnis[stelle - 1]):
            stelle -= 1
        ergebnis.insert(stelle, eintrag)
    return ergebnis


def vor_im_plan(a, b):
    """Priorität, dann Punkte, dann Titel."""
    if a[1] != b[1]:
        return a[1] < b[1]
    if a[2] != b[2]:
        return a[2] < b[2]
    return a[0] < b[0]


def vor_bei_brocken(a, b):
    """Mehr Punkte zuerst, dann Titel."""
    if a[2] != b[2]:
        return a[2] > b[2]
    return a[0] < b[0]


# 300 zufällige Backlogs
zufall = Zufall(3027)
TITEL = ["Login", "Export", "Suche", "Hilfe", "Bericht", "Import", "Rechte", "Cache"]
for _ in range(300):
    daten = [(zufall.choice(TITEL), zufall.randint(1, 5), zufall.randint(1, 8)) for _ in range(zufall.randint(0, 9))]
    vorher = list(daten)
    anzahl = zufall.randint(0, 10)
    ergebnis = nach_aufwand(daten)
    erwartet = einfuegen_sortiert(vorher, lambda a, b: a[2] < b[2])
    assert ergebnis == erwartet, f"nach_aufwand({vorher}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    ergebnis = planungsreihenfolge(daten)
    erwartet = einfuegen_sortiert(vorher, vor_im_plan)
    assert ergebnis == erwartet, f"planungsreihenfolge({vorher}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    ergebnis = groesste_brocken(daten, anzahl)
    erwartet = [eintrag[0] for eintrag in einfuegen_sortiert(vorher, vor_bei_brocken)][:anzahl]
    assert ergebnis == erwartet, f"groesste_brocken({vorher}, {anzahl}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    assert daten == vorher, f"backlog wurde verändert: vorher {vorher}, nachher {daten!r}."

# Laufzeit: 500 Einträge brauchen höchstens O(n log n) Schritte
daten = [(f"T{(nummer * 7919) % 500}", nummer % 5 + 1, (nummer * 31) % 100 + 1) for nummer in range(500)]
_, schritte = zaehle_schritte(planungsreihenfolge, daten)
assert schritte < 20000, (
    f"planungsreihenfolge mit 500 Einträgen braucht {schritte} Schritte, erwartet waren O(n log n), hier weit unter "
    "20 000.\nTipp: Sortieren Sie mit sorted(backlog, key=…) statt mit einer eigenen Schleife."
)

# Obere Grenze: 100 000 Einträge
daten = [(f"T{(nummer * 7919) % 100000}", nummer % 5 + 1, (nummer * 31) % 100 + 1) for nummer in range(100000)]
ergebnis = (planungsreihenfolge(daten)[:2], groesste_brocken(daten, 100000)[:2], nach_aufwand(daten)[:2])
erwartet = (
    einfuegen_sortiert([e for e in daten if e[1] == 1 and e[2] == 1], vor_im_plan)[:2],
    [e[0] for e in einfuegen_sortiert([e for e in daten if e[2] == 100], vor_bei_brocken)][:2],
    [e for e in daten if e[2] == 1][:2],
)
assert ergebnis == erwartet, (
    f"Bei 100 000 Einträgen beginnen planungsreihenfolge, groesste_brocken und nach_aufwand mit {ergebnis!r}, "
    f"erwartet war {erwartet!r}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "[('Hilfe', 3, 1), ('Export', 2, 3), ('Suche', 1, 3), ('Bericht', 2, 3), ('Login', 1, 5)]\n"
    "[('Suche', 1, 3), ('Login', 1, 5), ('Bericht', 2, 3), ('Export', 2, 3), ('Hilfe', 3, 1)]\n"
    "['Login', 'Bericht', 'Export']"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
