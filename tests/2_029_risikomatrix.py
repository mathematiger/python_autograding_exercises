# Automatisch erzeugt aus lehrkraft/muster/2_029_risikomatrix.py - nicht von Hand ändern.
# vorlage-hash: d4df6d7f96dd7fad
# text-hash: 4cb723141056164e
# thema: datenstrukturen
# inhalt: Tupel als Dictionary-Schlüssel

# matrix aus dem Beispiel
BEISPIEL = [("Lieferverzug", 4, 3), ("Ausfall Admin", 2, 5), ("Budget überzogen", 4, 3), ("Datenverlust", 1, 5)]
ergebnis = matrix(BEISPIEL)
if isinstance(ergebnis, dict) and any(isinstance(schluessel, str) for schluessel in ergebnis):
    hinweis = "\nTipp: Die Schlüssel sind die Felder (wahrscheinlichkeit, schaden), nicht die Namen der Risiken."
elif isinstance(ergebnis, dict) and any(not isinstance(schluessel, tuple) for schluessel in ergebnis):
    hinweis = "\nTipp: Jeder Schlüssel ist ein Tupel aus zwei Zahlen: (wahrscheinlichkeit, schaden)."
else:
    hinweis = ""
assert ergebnis == {(4, 3): 2, (2, 5): 1, (1, 5): 1}, (
    f"matrix({BEISPIEL}) ergibt {ergebnis!r}, erwartet war {{(4, 3): 2, (2, 5): 1, (1, 5): 1}}.{hinweis}"
)

# kritische_felder findet die richtigen Felder (die Reihenfolge zählt hier noch nicht)
raster = {(4, 3): 2, (2, 5): 1, (1, 5): 1}
ergebnis = kritische_felder(raster, 10)
assert isinstance(ergebnis, list) and sorted(ergebnis) == [(2, 5), (4, 3)], (
    f"kritische_felder({raster}, 10) ergibt {ergebnis!r}, erwartet waren die Felder (2, 5) und (4, 3).\n"
    "Tipp: Die Risikozahl ist wahrscheinlichkeit * schaden; nehmen Sie die Felder mit Risikozahl >= grenze."
)

# kritische_felder aus dem Beispiel
raster = {(4, 3): 2, (2, 5): 1, (1, 5): 1}
ergebnis = kritische_felder(raster, 10)
assert ergebnis == [(2, 5), (4, 3)], (
    f"kritische_felder({raster}, 10) ergibt {ergebnis!r}, erwartet war [(2, 5), (4, 3)].\n"
    "Tipp: Die Risikozahl ist wahrscheinlichkeit * schaden; geben Sie die Felder sortiert zurück."
)

# Wahrscheinlichkeit und Schaden nicht vertauschen
ergebnis = matrix([("Virus", 2, 5), ("Brand", 5, 2), ("Virus", 2, 5)])
assert ergebnis == {(2, 5): 2, (5, 2): 1}, (
    f'matrix([("Virus", 2, 5), ("Brand", 5, 2), ("Virus", 2, 5)]) ergibt {ergebnis!r}, '
    "erwartet war {(2, 5): 2, (5, 2): 1}.\n"
    "Tipp: (2, 5) und (5, 2) sind verschiedene Felder: zuerst die Wahrscheinlichkeit, dann der Schaden."
)

# Genau die Grenze zählt als kritisch
raster = {(2, 4): 3, (3, 3): 1, (1, 1): 5, (5, 5): 1}
ergebnis = kritische_felder(raster, 8)
assert ergebnis == [(2, 4), (3, 3), (5, 5)], (
    f"kritische_felder({raster}, 8) ergibt {ergebnis!r}, erwartet war [(2, 4), (3, 3), (5, 5)].\n"
    "Tipp: Mindestens grenze heißt >= grenze; die Risikozahl 8 ist bei Grenze 8 schon kritisch."
)

# Unterer Rand der Grenze: 1 nimmt alle Felder
raster = {(5, 5): 1, (1, 1): 2, (3, 2): 1}
ergebnis = kritische_felder(raster, 1)
assert sorted(ergebnis) == [(1, 1), (3, 2), (5, 5)], (
    f"kritische_felder({raster}, 1) ergibt {ergebnis!r}, erwartet war [(1, 1), (3, 2), (5, 5)]."
)

# Oberer Rand der Grenze: 25 nimmt nur (5, 5)
ergebnis = kritische_felder(raster, 25)
assert sorted(ergebnis) == [(5, 5)], f"kritische_felder({raster}, 25) ergibt {ergebnis!r}, erwartet war [(5, 5)]."

# Keine Risiken: leeres Dictionary
ergebnis = matrix([])
assert ergebnis == {}, f"matrix([]) ergibt {ergebnis!r}, erwartet war {{}}."

# Keine Risiken: keine kritischen Felder
ergebnis = kritische_felder({}, 5)
assert ergebnis == [], f"kritische_felder({{}}, 5) ergibt {ergebnis!r}, erwartet war []."

# Kein Feld ist kritisch
raster = {(1, 2): 4, (2, 2): 1}
ergebnis = kritische_felder(raster, 20)
assert ergebnis == [], f"kritische_felder({raster}, 20) ergibt {ergebnis!r}, erwartet war []."

# Die Liste risiken bleibt unverändert
risiken = [("A", 1, 2), ("B", 3, 4)]
matrix(risiken)
assert risiken == [("A", 1, 2), ("B", 3, 4)], f"Nach matrix(...) ist risiken {risiken!r}, erwartet war unverändert."


# Vergleichslösung: alle 25 Felder durchgehen und jeweils zählen
def matrix_von_hand(risiken):
    """Zählt für jedes der 25 Felder alle passenden Risiken einzeln."""
    raster = {}
    for wahrscheinlichkeit in range(1, 6):
        for schaden in range(1, 6):
            anzahl = 0
            for risiko in risiken:
                if risiko[1] == wahrscheinlichkeit and risiko[2] == schaden:
                    anzahl += 1
            if anzahl > 0:
                raster[(wahrscheinlichkeit, schaden)] = anzahl
    return raster


def kritisch_von_hand(raster, grenze):
    """Geht die 25 Felder in sortierter Reihenfolge durch."""
    felder = []
    for wahrscheinlichkeit in range(1, 6):
        for schaden in range(1, 6):
            if (wahrscheinlichkeit, schaden) in raster and wahrscheinlichkeit * schaden >= grenze:
                felder.append((wahrscheinlichkeit, schaden))
    return felder


# 300 zufällige Risikolisten für matrix
zufall = Zufall(2029)
NAMEN = ["Lieferverzug", "Ausfall Admin", "Budget", "Datenverlust", "Scope Creep", "Lizenz", "Hackerangriff"]
for _ in range(300):
    risiken = []
    for _ in range(zufall.randint(0, 12)):
        risiken.append((zufall.choice(NAMEN), zufall.randint(1, 5), zufall.randint(1, 5)))
    grenze = zufall.randint(1, 25)
    raster = matrix(risiken)
    erwartet = matrix_von_hand(risiken)
    assert raster == erwartet, f"matrix({risiken}) ergibt {raster!r}, erwartet war {erwartet!r}."

# 300 zufällige Raster für kritische_felder
zufall = Zufall(2029)
for _ in range(300):
    risiken = []
    for _ in range(zufall.randint(0, 12)):
        risiken.append((zufall.choice(NAMEN), zufall.randint(1, 5), zufall.randint(1, 5)))
    grenze = zufall.randint(1, 25)
    sortiert = matrix_von_hand(risiken)
    erwartet = {}
    # Schlüssel in umgekehrter Reihenfolge eintragen, damit vergessenes Sortieren auffällt
    for feld in reversed(list(sortiert)):
        erwartet[feld] = sortiert[feld]
    ergebnis = kritische_felder(erwartet, grenze)
    erwartet_kritisch = kritisch_von_hand(erwartet, grenze)
    assert ergebnis == erwartet_kritisch, (
        f"kritische_felder({erwartet}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet_kritisch!r}."
    )

# Obere Grenze: 10 000 Risiken, jedes Feld 400-mal belegt
risiken = []
for nummer in range(10000):
    risiken.append((f"Risiko {nummer}", nummer % 5 + 1, nummer // 5 % 5 + 1))
raster = matrix(risiken)
erwartet = {}
for wahrscheinlichkeit in range(1, 6):
    for schaden in range(1, 6):
        erwartet[(wahrscheinlichkeit, schaden)] = 400
assert raster == erwartet, (
    f"Bei 10 000 Risiken, die alle 25 Felder je 400-mal belegen, ergibt matrix ein Dictionary mit "
    f"{len(raster) if isinstance(raster, dict) else raster!r} Einträgen, erwartet waren 25 Felder mit je 400."
)

# Obere Grenze: kritische Felder bei voll belegtem Raster
ergebnis = kritische_felder(raster, 15)
assert ergebnis == [(3, 5), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)], (
    f"kritische_felder(<alle 25 Felder>, 15) ergibt {ergebnis!r}, erwartet war "
    "[(3, 5), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "{(4, 3): 2, (2, 5): 1, (1, 5): 1}\n[(2, 5), (4, 3)]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
