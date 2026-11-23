# Automatisch erzeugt aus lehrkraft/muster/4_040_moderationsplan.py - nicht von Hand ändern.
# vorlage-hash: ab188e21e2030a5d
# text-hash: 7b52b687fefe40dd
# thema: kontrollfluss
# inhalt: count, cycle, repeat, islice

def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def ersten(iterator, anzahl):
    """Holt höchstens anzahl Werte mit next; ein Fehler wird als Text zurückgegeben."""
    werte = []
    try:
        for _ in range(anzahl):
            werte.append(next(iterator))
    except StopIteration:
        werte.append("(Ende – StopIteration)")
    except Exception as fehler:
        werte.append(f"{type(fehler).__name__}: {fehler}")
    return werte


def vergleich_plan(team, erster_sprint, anzahl, tage):
    """Vergleichslösung mit Indexrechnung statt itertools."""
    plan = []
    tag = 0
    for sprint in range(anzahl):
        namen = []
        for _ in range(tage):
            namen.append(team[tag % len(team)])
            tag += 1
        plan.append((erster_sprint + sprint, namen))
    return plan


def vergleich_frei(belegt, start):
    """Vergleichslösung mit while."""
    nummer = start
    while nummer in belegt:
        nummer += 1
    return nummer


class Zaehlteam:
    """Eine Liste von Namen, die zählt, wie oft sie durchlaufen wird."""

    def __init__(self, namen):
        """Merkt sich die Namen."""
        self.namen = namen
        self.durchlaeufe = 0

    def __iter__(self):
        """Liefert die Namen und zählt den Durchlauf."""
        self.durchlaeufe += 1
        return iter(self.namen)

    def __len__(self):
        """Die Zahl der Namen."""
        return len(self.namen)

    def __getitem__(self, stelle):
        """Der Name an einer Stelle."""
        return self.namen[stelle]


TEAM = ["Ada", "Ben", "Cem"]

# rotation liefert die Namen reihum
reihe = wert_von(lambda: rotation(TEAM))
ergebnis = ersten(reihe, 4) if not isinstance(reihe, str) else reihe
assert ergebnis == ["Ada", "Ben", "Cem", "Ada"], (
    f"Vier next(...) auf rotation(['Ada', 'Ben', 'Cem']) ergeben {ergebnis!r}, erwartet war ['Ada', 'Ben', 'Cem', 'Ada'].\n"
    "Tipp: itertools.cycle(team) liefert die Namen immer wieder von vorn."
)

# rotation läuft ohne Ende weiter
reihe = wert_von(lambda: rotation(["Dana", "Emil"]))
ergebnis = ersten(reihe, 1001)[-1] if not isinstance(reihe, str) else reihe
assert ergebnis == "Dana", f"Der 1001. Name aus rotation(['Dana', 'Emil']) ist {ergebnis!r}, erwartet war 'Dana'."

# rotation mit nur einer Person
reihe = wert_von(lambda: rotation(["Fe"]))
ergebnis = ersten(reihe, 3) if not isinstance(reihe, str) else reihe
assert ergebnis == ["Fe", "Fe", "Fe"], f"Drei next(...) auf rotation(['Fe']) ergeben {ergebnis!r}, erwartet war ['Fe', 'Fe', 'Fe']."

# rotation benutzt itertools.cycle
assert verwendet("cycle"), "Benutzen Sie in rotation itertools.cycle."

# sprintplan im Beispiel
ergebnis = wert_von(lambda: sprintplan(TEAM, 41, 2, 2))
assert ergebnis == [(41, ["Ada", "Ben"]), (42, ["Cem", "Ada"])], (
    f"sprintplan(team, 41, 2, 2) ergibt {ergebnis!r}, erwartet war [(41, ['Ada', 'Ben']), (42, ['Cem', 'Ada'])].\n"
    "Tipp: Legen Sie die Rotation einmal vor der Schleife an; dann macht islice im nächsten Sprint dort weiter."
)

# sprintplan mit anderen Zahlen (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: sprintplan(["Ada", "Ben"], 7, 3, 3))
erwartet = [(7, ["Ada", "Ben", "Ada"]), (8, ["Ben", "Ada", "Ben"]), (9, ["Ada", "Ben", "Ada"])]
assert ergebnis == erwartet, f"sprintplan(['Ada', 'Ben'], 7, 3, 3) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# sprintplan mit null Sprints
ergebnis = wert_von(lambda: sprintplan(TEAM, 5, 0, 4))
assert ergebnis == [], f"sprintplan(team, 5, 0, 4) ergibt {ergebnis!r}, erwartet war []."

# sprintplan mit einem Tag pro Sprint und mit mehr Tagen als Personen
ergebnis = wert_von(lambda: [sprintplan(TEAM, 1, 4, 1), sprintplan(["Ada"], 1, 1, 5)])
erwartet = [[(1, ["Ada"]), (2, ["Ben"]), (3, ["Cem"]), (4, ["Ada"])], [(1, ["Ada"] * 5)]]
assert ergebnis == erwartet, f"sprintplan(team, 1, 4, 1) und sprintplan(['Ada'], 1, 1, 5) ergeben {ergebnis!r}, erwartet war {erwartet!r}."

# sprintplan benutzt islice und count
fehlt = [name for name in ["islice", "count"] if not verwendet(name)]
assert fehlt == [], f"Ihr Code verwendet {fehlt} nicht. Zählen Sie die Sprints mit count und nehmen Sie die Namen mit islice."

# kapazitaeten im Beispiel
ergebnis = wert_von(lambda: kapazitaeten(TEAM, 30))
assert ergebnis == {"Ada": 30, "Ben": 30, "Cem": 30}, f"kapazitaeten(team, 30) ergibt {ergebnis!r}, erwartet war {{'Ada': 30, 'Ben': 30, 'Cem': 30}}."

# kapazitaeten mit anderen Werten und mit 0 Stunden
ergebnis = wert_von(lambda: [kapazitaeten(["Dana"], 12), kapazitaeten(["X", "Y"], 0)])
assert ergebnis == [{"Dana": 12}, {"X": 0, "Y": 0}], f"kapazitaeten(['Dana'], 12) und kapazitaeten(['X', 'Y'], 0) ergeben {ergebnis!r}, erwartet war [{{'Dana': 12}}, {{'X': 0, 'Y': 0}}]."

# kapazitaeten benutzt itertools.repeat
assert verwendet("repeat"), "Benutzen Sie in kapazitaeten itertools.repeat, etwa mit zip(team, repeat(stunden))."

# naechste_freie_nummer im Beispiel
ergebnis = wert_von(lambda: naechste_freie_nummer({7, 8, 10}, 7))
assert ergebnis == 9, f"naechste_freie_nummer({{7, 8, 10}}, 7) ergibt {ergebnis!r}, erwartet war 9."

# naechste_freie_nummer: start selbst ist frei, und eine leere Menge
ergebnis = wert_von(lambda: [naechste_freie_nummer({1, 2, 3}, 5), naechste_freie_nummer(set(), 0), naechste_freie_nummer({0}, 0)])
assert ergebnis == [5, 0, 1], (
    f"naechste_freie_nummer({{1, 2, 3}}, 5), (set(), 0) und ({{0}}, 0) ergeben {ergebnis!r}, erwartet war [5, 0, 1]."
)

# naechste_freie_nummer: belegte Zahlen unter start zählen nicht
ergebnis = wert_von(lambda: naechste_freie_nummer({1, 2, 3, 4, 5}, 3))
assert ergebnis == 6, f"naechste_freie_nummer({{1, 2, 3, 4, 5}}, 3) ergibt {ergebnis!r}, erwartet war 6."

# Die Ausgabe des Programms
erwartet = "['Ada', 'Ben', 'Cem', 'Ada']\n[(41, ['Ada', 'Ben']), (42, ['Cem', 'Ada'])]\n{'Ada': 30, 'Ben': 30, 'Cem': 30}\n9"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# sprintplan geht die Teamliste nicht für jeden Sprint neu durch
zaehlteam = Zaehlteam(["Ada", "Ben", "Cem"])
ergebnis = wert_von(lambda: sprintplan(zaehlteam, 1, 50, 2))
assert zaehlteam.durchlaeufe <= 1, (
    f"sprintplan für 50 Sprints durchläuft die Teamliste {zaehlteam.durchlaeufe}-mal; erwartet war höchstens einmal "
    "(cycle merkt sich die Namen selbst).\nTipp: Rufen Sie rotation(team) nur einmal auf, vor der Schleife."
)

# Viele zufällige Pläne und Nummern
zufall = Zufall(4040)
for runde in range(200):
    team = [f"P{nummer}" for nummer in range(zufall.randint(1, 6))]
    zufall.shuffle(team)
    erster, anzahl, tage = zufall.randint(1, 10**6), zufall.randint(0, 6), zufall.randint(1, 7)
    ergebnis = wert_von(lambda: sprintplan(team, erster, anzahl, tage))
    erwartet = vergleich_plan(team, erster, anzahl, tage)
    assert ergebnis == erwartet, f"sprintplan({team}, {erster}, {anzahl}, {tage}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    stunden = zufall.randint(0, 40)
    ergebnis = wert_von(lambda: kapazitaeten(team, stunden))
    assert ergebnis == {name: stunden for name in team}, f"kapazitaeten({team}, {stunden}) ergibt {ergebnis!r}, erwartet war {dict.fromkeys(team, stunden)!r}."
    start = zufall.randint(0, 30)
    belegt = set(zufall.sample(range(40), zufall.randint(0, 35)))
    ergebnis = wert_von(lambda: naechste_freie_nummer(belegt, start))
    assert ergebnis == vergleich_frei(belegt, start), (
        f"naechste_freie_nummer({sorted(belegt)}, {start}) ergibt {ergebnis!r}, erwartet war {vergleich_frei(belegt, start)}."
    )

# Obere Grenze: 1000 Sprints mit je 20 Tagen und 20 Personen
team = [f"P{nummer:02d}" for nummer in range(20)]
ergebnis = wert_von(lambda: sprintplan(team, 10**6, 1000, 20))
erwartet = vergleich_plan(team, 10**6, 1000, 20)
assert ergebnis == erwartet, (
    f"sprintplan mit 20 Personen, 1000 Sprints und 20 Tagen weicht ab; erwartet waren 1000 Sprints ab {10**6}."
    if isinstance(ergebnis, list) else f"sprintplan mit 20 Personen, 1000 Sprints und 20 Tagen ergibt {ergebnis!r}."
)

# Obere Grenze: 100 000 belegte Nummern ab einer großen Startzahl
start = 10**9 - 100000
belegt = set(range(start, 10**9))
ergebnis = wert_von(lambda: naechste_freie_nummer(belegt, start))
assert ergebnis == 10**9, f"Bei 100 000 belegten Nummern ab {start} ergibt naechste_freie_nummer {ergebnis!r}, erwartet war {10**9}."
