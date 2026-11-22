# Automatisch erzeugt aus lehrkraft/muster/5_033_projektplan.py - nicht von Hand ändern.
# vorlage-hash: f8be6c769baf1280
# text-hash: b1c1679b1a204142
# thema: funktionen
# inhalt: functools.cached_property

import functools

original_berechnung = berechne_endzeitpunkte
berechnungen = []


# Zählt mit, wie oft gerechnet wird; die Klasse findet diese Fassung, weil sie den Namen erst beim Aufruf nachschlägt
def berechne_endzeitpunkte(pakete):
    """Ruft die vorgegebene Berechnung auf und zählt den Aufruf."""
    berechnungen.append(dict(pakete))
    return original_berechnung(pakete)


def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def neuer_plan(pakete):
    """Legt einen Plan an und setzt den Zähler zurück; ein Fehler wird als Text zurückgegeben."""
    plan = wert_von(lambda: Projektplan(pakete))
    berechnungen.clear()
    return plan


BEISPIEL = {"Analyse": (5, []), "Entwurf": (3, ["Analyse"])}

# endzeitpunkte im Beispiel
plan = neuer_plan(BEISPIEL)
ergebnis = wert_von(lambda: plan.endzeitpunkte)
assert ergebnis == {"Analyse": 5, "Entwurf": 8}, (
    f"plan.endzeitpunkte ergibt {ergebnis!r}, erwartet war {{'Analyse': 5, 'Entwurf': 8}}.\n"
    "Tipp: Geben Sie berechne_endzeitpunkte(self.pakete) zurück."
)

# projektdauer im Beispiel
plan = neuer_plan(BEISPIEL)
ergebnis = wert_von(lambda: plan.projektdauer)
assert ergebnis == 8, f"plan.projektdauer ergibt {ergebnis!r}, erwartet war 8."

# projektdauer eines leeren Plans und eines anderen Plans (nicht fest hinschreiben!)
ergebnis = [wert_von(lambda: neuer_plan({}).projektdauer), wert_von(lambda: neuer_plan({"A": (2, []), "B": (9, [])}).projektdauer)]
assert ergebnis == [0, 9], f"projektdauer eines leeren Plans und von A (2 Tage) und B (9 Tage) ergibt {ergebnis!r}, erwartet war [0, 9]."

# endzeitpunkte ist eine functools.cached_property
art = type(Projektplan.__dict__.get("endzeitpunkte")).__name__
assert isinstance(Projektplan.__dict__.get("endzeitpunkte"), functools.cached_property), (
    f"Projektplan.endzeitpunkte ist ein {art}, erwartet war eine functools.cached_property.\n"
    "Tipp: Schreiben Sie @cached_property über die Methode."
)

# projektdauer ist eine functools.cached_property
art = type(Projektplan.__dict__.get("projektdauer")).__name__
assert isinstance(Projektplan.__dict__.get("projektdauer"), functools.cached_property), (
    f"Projektplan.projektdauer ist ein {art}, erwartet war eine functools.cached_property."
)

# Zweimal endzeitpunkte rechnet nur einmal
plan = neuer_plan(BEISPIEL)
wert_von(lambda: [plan.endzeitpunkte, plan.endzeitpunkte, plan.endzeitpunkte])
assert len(berechnungen) == 1, f"Dreimal plan.endzeitpunkte ruft berechne_endzeitpunkte {len(berechnungen)}-mal auf, erwartet war einmal."

# Der Konstruktor rechnet noch nichts aus
berechnungen.clear()
plan = wert_von(lambda: Projektplan(BEISPIEL))
anzahl = len(berechnungen)
berechnungen.clear()
assert anzahl == 0, (
    f"Projektplan(...) ruft berechne_endzeitpunkte schon {anzahl}-mal auf, erwartet war erst beim ersten Zugriff.\n"
    "Tipp: Rechnen Sie nicht in __init__; cached_property rechnet beim ersten Zugriff."
)

# projektdauer benutzt die gespeicherten endzeitpunkte
plan = neuer_plan(BEISPIEL)
ergebnis = wert_von(lambda: [plan.endzeitpunkte, plan.projektdauer, plan.projektdauer])
assert ergebnis == [{"Analyse": 5, "Entwurf": 8}, 8, 8] and len(berechnungen) == 1, (
    f"plan.endzeitpunkte und zweimal plan.projektdauer ergeben {ergebnis!r} und rufen berechne_endzeitpunkte "
    f"{len(berechnungen)}-mal auf, erwartet war einmal.\nTipp: projektdauer nimmt max(self.endzeitpunkte.values(), default=0)."
)

# Der Wert liegt im __dict__ des Objekts
plan = neuer_plan(BEISPIEL)
wert_von(lambda: plan.projektdauer)
ergebnis = sorted(name for name in getattr(plan, "__dict__", {}) if name in ("endzeitpunkte", "projektdauer"))
assert ergebnis == ["endzeitpunkte", "projektdauer"], (
    f"Nach plan.projektdauer stehen im __dict__ des Plans die Einträge {ergebnis}, erwartet waren endzeitpunkte und projektdauer."
)

# Jedes Objekt hat seinen eigenen Zwischenspeicher
plan_a = neuer_plan({"A": (3, [])})
plan_b = neuer_plan({"B": (7, [])})
ergebnis = wert_von(lambda: [plan_a.projektdauer, plan_b.projektdauer, plan_a.projektdauer, plan_b.projektdauer])
assert ergebnis == [3, 7, 3, 7] and len(berechnungen) == 2, (
    f"Zwei Pläne, je zweimal projektdauer, ergeben {ergebnis!r} mit {len(berechnungen)} Berechnungen, "
    "erwartet war [3, 7, 3, 7] mit zwei Berechnungen."
)

# hinzufuegen: endzeitpunkte wird neu berechnet
plan = neuer_plan(BEISPIEL)
ergebnis = wert_von(lambda: [plan.endzeitpunkte, plan.hinzufuegen("Test", 4, ["Entwurf"]), plan.endzeitpunkte])
erwartet = [{"Analyse": 5, "Entwurf": 8}, None, {"Analyse": 5, "Entwurf": 8, "Test": 12}]
assert ergebnis == erwartet, (
    f"endzeitpunkte, hinzufuegen('Test', 4, ['Entwurf']) und wieder endzeitpunkte ergeben {ergebnis!r}, erwartet war {erwartet!r}.\n"
    'Tipp: Löschen Sie nach der Änderung den gespeicherten Wert, etwa mit self.__dict__.pop("endzeitpunkte", None).'
)

# hinzufuegen: auch projektdauer wird neu berechnet
plan = neuer_plan(BEISPIEL)
ergebnis = wert_von(lambda: [plan.projektdauer, plan.hinzufuegen("Test", 4, ["Entwurf"]), plan.projektdauer])
assert ergebnis == [8, None, 12], (
    f"projektdauer, hinzufuegen('Test', 4, ['Entwurf']) und wieder projektdauer ergeben {ergebnis!r}, erwartet war [8, None, 12].\n"
    "Tipp: Auch projektdauer ist gespeichert und muss vergessen werden."
)

# hinzufuegen, bevor je etwas abgefragt wurde
plan = neuer_plan(BEISPIEL)
ergebnis = wert_von(lambda: [plan.hinzufuegen("Doku", 2, []), plan.projektdauer, plan.endzeitpunkte["Doku"]])
assert ergebnis == [None, 8, 2], (
    f"hinzufuegen('Doku', 2, []) vor jedem Zugriff, dann projektdauer und endzeitpunkte['Doku'] ergeben {ergebnis!r}, "
    "erwartet war [None, 8, 2].\nTipp: del self.endzeitpunkte scheitert, wenn noch nichts gespeichert ist; pop(..., None) nicht."
)

# dauer_aendern im Beispiel
plan = neuer_plan(BEISPIEL)
ergebnis = wert_von(lambda: [plan.hinzufuegen("Test", 4, ["Entwurf"]), plan.projektdauer, plan.dauer_aendern("Analyse", 7), plan.endzeitpunkte["Test"]])
assert ergebnis == [None, 12, None, 14], (
    f"hinzufuegen, projektdauer, dauer_aendern('Analyse', 7) und endzeitpunkte['Test'] ergeben {ergebnis!r}, "
    "erwartet war [None, 12, None, 14]."
)

# dauer_aendern: auch projektdauer wird neu berechnet und die Vorgänger bleiben
plan = neuer_plan({"A": (1, []), "B": (1, ["A"])})
ergebnis = wert_von(lambda: [plan.projektdauer, plan.dauer_aendern("B", 10), plan.projektdauer, plan.dauer_aendern("A", 0), plan.projektdauer])
assert ergebnis == [2, None, 11, None, 10], (
    f"projektdauer, dauer_aendern('B', 10), projektdauer, dauer_aendern('A', 0), projektdauer ergeben {ergebnis!r}, "
    "erwartet war [2, None, 11, None, 10]."
)

# Nach einer Änderung wird genau einmal neu gerechnet
plan = neuer_plan(BEISPIEL)
wert_von(lambda: [plan.projektdauer, plan.dauer_aendern("Entwurf", 4), plan.projektdauer, plan.endzeitpunkte, plan.projektdauer])
assert len(berechnungen) == 2, (
    f"projektdauer, dauer_aendern, dann dreimal Abfragen rufen berechne_endzeitpunkte {len(berechnungen)}-mal auf, "
    "erwartet war zweimal (einmal vor und einmal nach der Änderung)."
)

# Die Ausgabe des Programms
erwartet = "{'Analyse': 5, 'Entwurf': 8}\n8\n12\n14"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Pläne und Änderungen
zufall = Zufall(5033)
for _ in range(100):
    pakete = {}
    plan = neuer_plan({})
    aenderungen = 0
    for schritt in range(zufall.randint(1, 15)):
        if pakete and zufall.random() < 0.3:
            name = zufall.choice(sorted(pakete))
            dauer = zufall.randint(0, 1000)
            pakete[name] = (dauer, pakete[name][1])
            wert_von(lambda: plan.dauer_aendern(name, dauer))
        else:
            name = f"P{schritt}"
            vorgaenger = zufall.sample(sorted(pakete), zufall.randint(0, min(3, len(pakete))))
            pakete[name] = (zufall.randint(0, 1000), vorgaenger)
            wert_von(lambda: plan.hinzufuegen(name, pakete[name][0], vorgaenger))
        aenderungen += 1
        ergebnis = wert_von(lambda: [plan.projektdauer, plan.endzeitpunkte, plan.projektdauer])
        erwartet_ende = original_berechnung(pakete)
        erwartet = [max(erwartet_ende.values(), default=0), erwartet_ende, max(erwartet_ende.values(), default=0)]
        assert ergebnis == erwartet, f"Nach den Änderungen bis zu {name} ergeben projektdauer und endzeitpunkte {ergebnis!r}, erwartet war {erwartet!r}."
    assert len(berechnungen) == aenderungen, (
        f"Bei {aenderungen} Änderungen mit je drei Abfragen danach wurde {len(berechnungen)}-mal gerechnet, erwartet war {aenderungen}-mal."
    )

# Obere Grenze: 2000 Pakete in einer Kette, oft abgefragt
pakete = {"P0": (1, [])}
for nummer in range(1, 2000):
    pakete[f"P{nummer}"] = (1, [f"P{nummer - 1}"])
plan = neuer_plan(pakete)
ergebnis = wert_von(lambda: [plan.projektdauer for _ in range(1000)])
assert ergebnis == [2000] * 1000 and len(berechnungen) == 1, (
    f"Bei 2000 Paketen in einer Kette und 1000 Abfragen von projektdauer wurde {len(berechnungen)}-mal gerechnet "
    f"(Ergebnis zuerst {ergebnis[:1] if isinstance(ergebnis, list) else ergebnis!r}), erwartet war 2000 und eine Berechnung."
)
