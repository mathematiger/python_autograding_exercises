# Automatisch erzeugt aus lehrkraft/muster/4_035_tabreihenfolge.py - nicht von Hand ändern.
# vorlage-hash: 6d16759294dbfce9
# text-hash: d050582e4d37637d
# thema: kontrollfluss
# inhalt: __iter__ als Generator

import types


def beispielmaske():
    """Baut die Maske aus dem Beispiel der Aufgabe."""
    maske = Eingabemaske()
    maske.hinzufuegen("Name", 10)
    maske.hinzufuegen("Firma", 20, aktiv=False)
    maske.hinzufuegen("E-Mail", 30)
    maske.hinzufuegen("Absenden", 99)
    maske.hinzufuegen("Vorname", 10)
    return maske


def vergleich(felder):
    """Vergleichslösung: Namen der aktiven Felder aus [(name, position, aktiv), …] in Tabreihenfolge.

    Sortiert über (position, Einfügenummer) statt sich auf die Stabilität von sorted zu verlassen.
    """
    aktive = [(position, nummer, name) for nummer, (name, position, aktiv) in enumerate(felder) if aktiv]
    return [name for _, _, name in sorted(aktive)]


BEISPIEL = ["Name", "Vorname", "E-Mail", "Absenden"]

# Ein Durchlauf liefert die aktiven Felder in Tabreihenfolge
ergebnis = list(beispielmaske())
assert ergebnis == BEISPIEL, f"list(maske) ergibt im Beispiel {ergebnis!r}, erwartet war {BEISPIEL!r}."

# Nach Position sortiert (nicht fest hinschreiben!)
maske = Eingabemaske()
maske.hinzufuegen("PLZ", 50)
maske.hinzufuegen("Straße", 40)
maske.hinzufuegen("Ort", 60)
ergebnis = list(maske)
assert ergebnis == ["Straße", "PLZ", "Ort"], (
    f"Felder PLZ (50), Straße (40), Ort (60): list(maske) ergibt {ergebnis!r}, erwartet war ['Straße', 'PLZ', 'Ort']."
)

# Abgeschaltete Felder werden übersprungen
maske = Eingabemaske()
maske.hinzufuegen("A", 1)
maske.hinzufuegen("B", 2, aktiv=False)
maske.hinzufuegen("C", 3)
ergebnis = list(maske)
assert ergebnis == ["A", "C"], f"Feld B ist abgeschaltet: list(maske) ergibt {ergebnis!r}, erwartet war ['A', 'C']."

# Gleiche Position: das zuerst hinzugefügte Feld kommt zuerst
maske = Eingabemaske()
maske.hinzufuegen("Zweig", 5)
maske.hinzufuegen("Ast", 5)
maske.hinzufuegen("Blatt", 5)
ergebnis = list(maske)
assert ergebnis == ["Zweig", "Ast", "Blatt"], (
    f"Drei Felder mit Position 5, hinzugefügt als Zweig, Ast, Blatt: list(maske) ergibt {ergebnis!r}, "
    "erwartet war ['Zweig', 'Ast', 'Blatt'] (nicht alphabetisch).\nTipp: Sortieren Sie nur nach der Position."
)

# aktiv_setzen schaltet ein Feld ein
maske = beispielmaske()
maske.aktiv_setzen("Firma", True)
ergebnis = list(maske)
assert ergebnis == ["Name", "Vorname", "Firma", "E-Mail", "Absenden"], (
    f"Nach aktiv_setzen('Firma', True) ergibt list(maske) {ergebnis!r}, erwartet war "
    "['Name', 'Vorname', 'Firma', 'E-Mail', 'Absenden']."
)

# aktiv_setzen schaltet ein Feld ab
maske = beispielmaske()
maske.aktiv_setzen("E-Mail", False)
ergebnis = list(maske)
assert ergebnis == ["Name", "Vorname", "Absenden"], (
    f"Nach aktiv_setzen('E-Mail', False) ergibt list(maske) {ergebnis!r}, erwartet war ['Name', 'Vorname', 'Absenden']."
)

# rueckwaerts liefert die umgekehrte Reihenfolge
ergebnis = list(beispielmaske().rueckwaerts())
assert ergebnis == BEISPIEL[::-1], f"list(maske.rueckwaerts()) ergibt im Beispiel {ergebnis!r}, erwartet war {BEISPIEL[::-1]!r}."

# Eine leere Maske liefert nichts
ergebnis = (list(Eingabemaske()), list(Eingabemaske().rueckwaerts()))
assert ergebnis == ([], []), f"Eine leere Maske liefert vorwärts und rückwärts {ergebnis!r}, erwartet war ([], [])."

# Nur abgeschaltete Felder: auch nichts
maske = Eingabemaske()
maske.hinzufuegen("A", 1, aktiv=False)
ergebnis = list(maske)
assert ergebnis == [], f"Eine Maske mit nur einem abgeschalteten Feld liefert {ergebnis!r}, erwartet war []."

# __iter__ ist eine Generatormethode
durchlauf = iter(beispielmaske())
assert isinstance(durchlauf, types.GeneratorType), (
    f"iter(maske) ergibt ein Objekt vom Typ {type(durchlauf).__name__}, erwartet war ein Generator.\n"
    "Tipp: Schreiben Sie __iter__ mit yield, dann liefert jeder Aufruf einen neuen Generator."
)

# rueckwaerts ist eine Generatormethode
durchlauf = beispielmaske().rueckwaerts()
assert isinstance(durchlauf, types.GeneratorType), (
    f"maske.rueckwaerts() ergibt ein Objekt vom Typ {type(durchlauf).__name__}, erwartet war ein Generator."
)

# Zweimal durchlaufen liefert zweimal dasselbe
maske = beispielmaske()
ergebnis = [list(maske), list(maske)]
assert ergebnis == [BEISPIEL, BEISPIEL], f"Zweimal list(maske) ergibt {ergebnis!r}, erwartet war zweimal {BEISPIEL!r}."

# Verschachtelt durchlaufen: jeder Durchlauf ist unabhängig
maske = Eingabemaske()
maske.hinzufuegen("A", 1)
maske.hinzufuegen("B", 2)
ergebnis = [(a, b) for a in maske for b in maske]
erwartet = [("A", "A"), ("A", "B"), ("B", "A"), ("B", "B")]
assert ergebnis == erwartet, (
    f"[(a, b) for a in maske for b in maske] ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: __iter__ darf keinen gemeinsamen Zähler auf self benutzen."
)

# Ein Durchlauf nach einer Änderung sieht das neue Feld
maske = beispielmaske()
vorher = list(maske)
maske.hinzufuegen("Telefon", 35)
nachher = list(maske)
assert (vorher, nachher) == (BEISPIEL, ["Name", "Vorname", "E-Mail", "Telefon", "Absenden"]), (
    f"Vor und nach hinzufuegen('Telefon', 35) ergibt list(maske) {vorher!r} und {nachher!r}, erwartet war "
    f"{BEISPIEL!r} und ['Name', 'Vorname', 'E-Mail', 'Telefon', 'Absenden']."
)

# Die Ausgabe des Programms
erwartet_ausgabe = f"{BEISPIEL}\n{BEISPIEL[::-1]}"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet_ausgabe), f"Erwartete Ausgabe:\n{erwartet_ausgabe}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Masken
zufall = Zufall(4035)
for runde in range(300):
    felder = []
    maske = Eingabemaske()
    for nummer in range(zufall.randint(0, 8)):
        position = zufall.choice([zufall.randint(0, 3), zufall.randint(0, 10**6)])
        aktiv = zufall.random() < 0.7
        felder.append([f"F{nummer}", position, aktiv])
        maske.hinzufuegen(f"F{nummer}", position, aktiv=aktiv)
    aufrufe = [f"hinzufuegen{tuple(feld)}" for feld in felder]
    for _ in range(zufall.randint(0, 3)):
        if felder:
            feld = zufall.choice(felder)
            feld[2] = zufall.random() < 0.5
            maske.aktiv_setzen(feld[0], feld[2])
            aufrufe.append(f"aktiv_setzen({feld[0]!r}, {feld[2]})")
    erwartet = vergleich(felder)
    ergebnis = (list(maske), list(maske.rueckwaerts()))
    assert ergebnis == (erwartet, erwartet[::-1]), (
        f"Nach {', '.join(aufrufe)}:\n  vorwärts und rückwärts erwartet {erwartet!r}, {erwartet[::-1]!r}\n"
        f"  bekommen {ergebnis[0]!r}, {ergebnis[1]!r}"
    )

# Obere Grenze: 2000 Felder, die Hälfte abgeschaltet
felder = [(f"Feld{nummer}", zufall.randint(0, 10**6), nummer % 2 == 0) for nummer in range(2000)]
maske = Eingabemaske()
for name, position, aktiv in felder:
    maske.hinzufuegen(name, position, aktiv=aktiv)
ergebnis = list(maske)
assert ergebnis == vergleich(felder), (
    f"Bei 2000 Feldern ergibt list(maske) {len(ergebnis)} Namen, die ersten {ergebnis[:3]!r}; erwartet waren 1000, "
    f"die ersten {vergleich(felder)[:3]!r}."
)
