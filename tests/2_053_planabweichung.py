# Automatisch erzeugt aus lehrkraft/muster/2_053_planabweichung.py - nicht von Hand ändern.
# vorlage-hash: f8ef7a8755f47063
# text-hash: 657f377aa7200d12
# thema: algorithmen
# inhalt: Maximum und Minimum mit Position

def wert_von(funktion, abweichungen):
    """Ruft die Funktion mit einer Kopie der Liste auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(list(abweichungen))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_bester(abweichungen):
    """Vergleichslösung: größter Wert mit max, dann von hinten die erste Stelle mit diesem Wert."""
    groesste = max(abweichungen)
    for stelle in range(len(abweichungen) - 1, -1, -1):
        if abweichungen[stelle] == groesste:
            return (groesste, stelle + 1)


def vergleich_schlechtester(abweichungen):
    """Vergleichslösung: kleinster Wert mit min, Stelle mit index."""
    kleinste = min(abweichungen)
    return (kleinste, abweichungen.index(kleinste) + 1)


def als_tupel(ergebnis):
    """Macht aus einer Liste mit zwei Werten ein Tupel, damit nur der eigene Formtest die Liste bemängelt."""
    if isinstance(ergebnis, list) and len(ergebnis) == 2:
        return tuple(ergebnis)
    return ergebnis


def pruefe_bester(abweichungen, hinweis=""):
    """Vergleicht bester_sprint mit der Vergleichslösung und liefert (stimmt, Meldung)."""
    ergebnis = als_tupel(wert_von(bester_sprint, abweichungen))
    erwartet = vergleich_bester(abweichungen)
    text = f"bester_sprint({abweichungen}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    return ergebnis == erwartet, text + hinweis


def pruefe_schlechtester(abweichungen, hinweis=""):
    """Vergleicht schlechtester_sprint mit der Vergleichslösung und liefert (stimmt, Meldung)."""
    ergebnis = als_tupel(wert_von(schlechtester_sprint, abweichungen))
    erwartet = vergleich_schlechtester(abweichungen)
    text = f"schlechtester_sprint({abweichungen}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    return ergebnis == erwartet, text + hinweis


# bester_sprint im Beispiel: die größte Abweichung ist 4
ergebnis = als_tupel(wert_von(bester_sprint, [-3, 4, -8, 4, 0]))
assert isinstance(ergebnis, tuple) and len(ergebnis) == 2 and ergebnis[0] == 4, (
    f"bester_sprint([-3, 4, -8, 4, 0]) ergibt {ergebnis!r}, erwartet waren zwei Werte, deren erster 4 ist.\n"
    "Tipp: Geben Sie mit return (groesster, nummer) beide Werte als Tupel zurück."
)

# bester_sprint gibt ein Tupel zurück
ergebnis = wert_von(bester_sprint, [-3, 4, -8, 4, 0])
assert isinstance(ergebnis, tuple), (
    f"bester_sprint([-3, 4, -8, 4, 0]) ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war ein Tupel.\n"
    "Tipp: return (groesster, nummer) mit runden Klammern."
)

# bester_sprint mit einem anderen Verlauf, ohne Gleichstand (nicht fest hinschreiben!)
stimmt, text = pruefe_bester([2, 7, 1, 5], "\nTipp: Sprint 1 ist abweichungen[0]; zählen Sie mit enumerate(abweichungen, start=1).")
assert stimmt, text

# bester_sprint im Beispiel: bei Gleichstand zählt der letzte Sprint, also 4
stimmt, text = pruefe_bester([-3, 4, -8, 4, 0], "\nTipp: Mit >= statt > ersetzt jeder spätere gleich große Wert den gemerkten.")
assert stimmt, text

# bester_sprint: die größte Abweichung im ersten Sprint
stimmt, text = pruefe_bester([9, 3, -1, 8], "\nTipp: Beginnen Sie mit dem ersten Eintrag und der Nummer 1.")
assert stimmt, text

# bester_sprint: die größte Abweichung im letzten Sprint
stimmt, text = pruefe_bester([1, 2, 3, 10])
assert stimmt, text

# bester_sprint: alle Abweichungen negativ (Beispiel aus dem Aufgabentext)
stimmt, text = pruefe_bester([-5, -2, -7], "\nTipp: Mit dem Startwert 0 findet man keinen größeren Wert; beginnen Sie mit abweichungen[0].")
assert stimmt, text

# bester_sprint: nur ein Sprint
stimmt, text = pruefe_bester([-12])
assert stimmt, text

# bester_sprint: alle gleich, also der letzte Sprint
stimmt, text = pruefe_bester([0, 0, 0, 0])
assert stimmt, text

# schlechtester_sprint im Beispiel
stimmt, text = pruefe_schlechtester([-3, 4, -8, 4, 0], "\nTipp: Für das Minimum drehen Sie den Vergleich um.")
assert stimmt, text

# schlechtester_sprint mit einem anderen Verlauf (nicht fest hinschreiben!)
stimmt, text = pruefe_schlechtester([5, 2, 9, 3])
assert stimmt, text

# schlechtester_sprint: bei Gleichstand zählt der erste Sprint
stimmt, text = pruefe_schlechtester([4, -6, 1, -6, -6], "\nTipp: Mit < statt <= bleibt der erste gleich kleine Wert stehen.")
assert stimmt, text

# schlechtester_sprint: die kleinste Abweichung im ersten Sprint
stimmt, text = pruefe_schlechtester([-9, 0, 3])
assert stimmt, text

# schlechtester_sprint: die kleinste Abweichung im letzten Sprint
stimmt, text = pruefe_schlechtester([3, 0, -1, -9])
assert stimmt, text

# schlechtester_sprint: alle Abweichungen positiv
stimmt, text = pruefe_schlechtester([7, 3, 12], "\nTipp: Mit dem Startwert 0 findet man keinen kleineren Wert; beginnen Sie mit abweichungen[0].")
assert stimmt, text

# schlechtester_sprint: nur ein Sprint
stimmt, text = pruefe_schlechtester([1000])
assert stimmt, text

# Ohne max(), min(), sorted(), sort() und index()
verboten = [name for name in ["max", "min", "sorted", "sort", "index"] if verwendet(name)]
assert verboten == [], (
    f"Ihr Code verwendet {verboten}. Suchen Sie das Maximum und das Minimum selbst in einer Schleife."
)

# Die Ausgabe des Programms
erwartet = "(4, 4)\n(-8, 3)\n(-2, 2)"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# bester_sprint: viele zufällige Verläufe, auch mit vielen gleichen Werten
zufall = Zufall(2053)
verlaeufe = []
for runde in range(300):
    spanne = zufall.choice([2, 10, 1000])
    verlaeufe.append([zufall.randint(-spanne, spanne) for _ in range(zufall.randint(1, 12))])
for abweichungen in verlaeufe:
    stimmt, text = pruefe_bester(abweichungen)
    assert stimmt, text

# schlechtester_sprint: dieselben zufälligen Verläufe
for abweichungen in verlaeufe:
    stimmt, text = pruefe_schlechtester(abweichungen)
    assert stimmt, text

# Obere Grenze: 100 000 Sprints
abweichungen = [zufall.randint(-1000, 1000) for _ in range(100000)]
abweichungen[31337] = 1000
abweichungen[77777] = 1000
abweichungen[123] = -1000
abweichungen[99999] = -1000
assert als_tupel(wert_von(bester_sprint, abweichungen)) == vergleich_bester(abweichungen), (
    f"Bei 100 000 Sprints ergibt bester_sprint {wert_von(bester_sprint, abweichungen)!r}, erwartet war {vergleich_bester(abweichungen)}."
)
# Obere Grenze: schlechtester_sprint bei 100 000 Sprints
assert als_tupel(wert_von(schlechtester_sprint, abweichungen)) == vergleich_schlechtester(abweichungen), (
    f"Bei 100 000 Sprints ergibt schlechtester_sprint {wert_von(schlechtester_sprint, abweichungen)!r}, "
    f"erwartet war {vergleich_schlechtester(abweichungen)}."
)
