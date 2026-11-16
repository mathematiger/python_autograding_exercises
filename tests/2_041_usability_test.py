# Automatisch erzeugt aus lehrkraft/muster/2_041_usability_test.py - nicht von Hand ändern.
# vorlage-hash: 56f255f551368f10
# text-hash: f5430cc2e5045d38
# thema: datenanalyse
# inhalt: Summe je Kategorie

def beispiel():
    """Baut die Tabelle aus dem Beispiel neu."""
    return [
        {"person": "P1", "aufgabe": "Anmelden", "sekunden": 35, "fehlklicks": 1},
        {"person": "P1", "aufgabe": "Suchen", "sekunden": 80, "fehlklicks": 4},
        {"person": "P2", "aufgabe": "Anmelden", "sekunden": 25, "fehlklicks": 0},
        {"person": "P2", "aufgabe": "Suchen", "sekunden": 62, "fehlklicks": 2},
        {"person": "P3", "aufgabe": "Anmelden", "sekunden": 40, "fehlklicks": 0},
    ]


def summe_von_hand(tabelle, gruppe, spalte):
    """Vergleichslösung: erst alle Gruppen sammeln, dann je Gruppe die passenden Zeilen addieren."""
    gruppen = []
    for zeile in tabelle:
        if zeile[gruppe] not in gruppen:
            gruppen.append(zeile[gruppe])
    return {name: sum(zeile[spalte] for zeile in tabelle if zeile[gruppe] == name) for name in gruppen}


def anzahl_von_hand(tabelle, gruppe):
    """Vergleichslösung: zählt je Gruppe mit einer Liste der Werte."""
    werte = [zeile[gruppe] for zeile in tabelle]
    return {name: werte.count(name) for name in dict.fromkeys(werte)}


def reihenfolge_hinweis(ergebnis, erwartet):
    """Gibt einen Tipp, wenn nur die Reihenfolge der Schlüssel nicht stimmt."""
    if isinstance(ergebnis, dict) and ergebnis == erwartet and list(ergebnis) != list(erwartet):
        return "\nTipp: Die Schlüssel sollen in der Reihenfolge ihres ersten Vorkommens stehen; sortieren Sie nicht."
    return ""


# summe_je aus dem Beispiel
daten = beispiel()
ergebnis = summe_je(daten, "aufgabe", "sekunden")
erwartet = {"Anmelden": 100, "Suchen": 142}
assert ergebnis == erwartet, (
    f'summe_je(<Beispiel>, "aufgabe", "sekunden") ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Addieren Sie zeile[spalte] zur bisherigen Summe der Gruppe zeile[gruppe], nicht überschreiben."
)

# summe_je nach anderen Spalten (nicht fest hinschreiben!)
ergebnis = summe_je(daten, "person", "fehlklicks")
erwartet = {"P1": 5, "P2": 2, "P3": 0}
assert ergebnis == erwartet, (
    f'summe_je(<Beispiel>, "person", "fehlklicks") ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Auch eine Gruppe mit der Summe 0 gehört ins Dictionary."
)

# anzahl_je aus dem Beispiel
ergebnis = anzahl_je(daten, "aufgabe")
erwartet = {"Anmelden": 3, "Suchen": 2}
assert ergebnis == erwartet, f'anzahl_je(<Beispiel>, "aufgabe") ergibt {ergebnis!r}, erwartet war {erwartet!r}.'

# anzahl_je nach einer anderen Spalte
ergebnis = anzahl_je(daten, "person")
erwartet = {"P1": 2, "P2": 2, "P3": 1}
assert ergebnis == erwartet, f'anzahl_je(<Beispiel>, "person") ergibt {ergebnis!r}, erwartet war {erwartet!r}.'

# Die Schlüssel stehen in der Reihenfolge ihres ersten Vorkommens
daten = [
    {"aufgabe": "Suchen", "sekunden": 5},
    {"aufgabe": "Bezahlen", "sekunden": 7},
    {"aufgabe": "Anmelden", "sekunden": 1},
    {"aufgabe": "Bezahlen", "sekunden": 2},
]
ergebnis = summe_je(daten, "aufgabe", "sekunden")
erwartet = {"Suchen": 5, "Bezahlen": 9, "Anmelden": 1}
assert ergebnis == erwartet and list(ergebnis) == list(erwartet), (
    f"summe_je({daten}, 'aufgabe', 'sekunden') ergibt {ergebnis!r}, erwartet war {erwartet!r} "
    f"in dieser Reihenfolge.{reihenfolge_hinweis(ergebnis, erwartet)}"
)

# Die Reihenfolge gilt auch für anzahl_je
ergebnis = anzahl_je(daten, "aufgabe")
erwartet = {"Suchen": 1, "Bezahlen": 2, "Anmelden": 1}
assert ergebnis == erwartet and list(ergebnis) == list(erwartet), (
    f"anzahl_je({daten}, 'aufgabe') ergibt {ergebnis!r}, erwartet war {erwartet!r} "
    f"in dieser Reihenfolge.{reihenfolge_hinweis(ergebnis, erwartet)}"
)

# Die Tabelle bleibt unverändert
daten = beispiel()
summe_je(daten, "aufgabe", "sekunden")
anzahl_je(daten, "person")
assert daten == beispiel(), f"Nach den Aufrufen ist die Tabelle {daten!r}, erwartet war unverändert {beispiel()!r}."

# Jeder Aufruf liefert ein neues Dictionary
erstes = summe_je([{"g": "a", "w": 1}], "g", "w")
zweites = summe_je([{"g": "b", "w": 2}], "g", "w")
assert erstes == {"a": 1} and zweites == {"b": 2}, (
    f"Zwei Aufrufe von summe_je mit verschiedenen Tabellen ergeben {erstes!r} und {zweites!r}, "
    "erwartet waren {'a': 1} und {'b': 2}.\nTipp: Legen Sie das Dictionary in der Funktion neu an, nicht außerhalb."
)

# Leere Tabelle: summe_je liefert ein leeres Dictionary
ergebnis = summe_je([], "aufgabe", "sekunden")
assert ergebnis == {}, f'summe_je([], "aufgabe", "sekunden") ergibt {ergebnis!r}, erwartet war {{}}.'

# Leere Tabelle: anzahl_je liefert ein leeres Dictionary
ergebnis = anzahl_je([], "aufgabe")
assert ergebnis == {}, f'anzahl_je([], "aufgabe") ergibt {ergebnis!r}, erwartet war {{}}.'

# Groß- und Kleinschreibung zählt
daten = [{"aufgabe": "Suchen", "sekunden": 3}, {"aufgabe": "suchen", "sekunden": 4}]
ergebnis = summe_je(daten, "aufgabe", "sekunden")
assert ergebnis == {"Suchen": 3, "suchen": 4}, (
    f"summe_je({daten}, 'aufgabe', 'sekunden') ergibt {ergebnis!r}, erwartet war {{'Suchen': 3, 'suchen': 4}}."
)

# Ränder der Werte: 0 und 10**6
daten = [{"aufgabe": "A", "sekunden": 10**6}, {"aufgabe": "A", "sekunden": 0}, {"aufgabe": "B", "sekunden": 0}]
ergebnis = summe_je(daten, "aufgabe", "sekunden")
assert ergebnis == {"A": 10**6, "B": 0}, (
    f"summe_je({daten}, 'aufgabe', 'sekunden') ergibt {ergebnis!r}, erwartet war {{'A': {10**6}, 'B': 0}}."
)

# 300 zufällige Tabellen für summe_je
zufall = Zufall(2041)
AUFGABEN = ["Anmelden", "Suchen", "Bezahlen", "Abmelden", "Profil"]
PERSONEN = ["P1", "P2", "P3", "P4"]


def zufallstabelle():
    """Baut eine zufällige kleine Tabelle."""
    return [
        {"person": zufall.choice(PERSONEN), "aufgabe": zufall.choice(AUFGABEN),
         "sekunden": zufall.randint(0, 300), "fehlklicks": zufall.randint(0, 5)}
        for _ in range(zufall.randint(0, 10))
    ]


for _ in range(300):
    daten = zufallstabelle()
    vorher = repr(daten)
    gruppe = zufall.choice(["person", "aufgabe"])
    spalte = zufall.choice(["sekunden", "fehlklicks"])
    ergebnis = summe_je(daten, gruppe, spalte)
    erwartet = summe_von_hand(daten, gruppe, spalte)
    assert ergebnis == erwartet and list(ergebnis) == list(erwartet), (
        f"summe_je({daten}, {gruppe!r}, {spalte!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
        f"{reihenfolge_hinweis(ergebnis, erwartet)}"
    )
    assert repr(daten) == vorher, f"Die Tabelle wurde verändert: vorher {vorher}, nachher {daten!r}."

# 300 zufällige Tabellen für anzahl_je
for _ in range(300):
    daten = zufallstabelle()
    gruppe = zufall.choice(["person", "aufgabe"])
    ergebnis = anzahl_je(daten, gruppe)
    erwartet = anzahl_von_hand(daten, gruppe)
    assert ergebnis == erwartet and list(ergebnis) == list(erwartet), (
        f"anzahl_je({daten}, {gruppe!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
        f"{reihenfolge_hinweis(ergebnis, erwartet)}"
    )

# Obere Grenze: 100 000 Zeilen mit 50 000 verschiedenen Personen, nur ein Durchlauf
daten = [{"person": f"P{nummer // 2}", "sekunden": nummer % 1000} for nummer in range(100000)]
ergebnis, schritte = zaehle_schritte(summe_je, daten, "person", "sekunden")
assert len(ergebnis) == 50000 and ergebnis["P0"] == 1 and ergebnis["P49999"] == 1997 and schritte <= 600000, (
    f"Bei 100 000 Zeilen mit 50 000 Personen ergibt summe_je {len(ergebnis)} Gruppen nach {schritte} Schritten; "
    "erwartet waren 50 000 Gruppen (P0 mit 1, P49999 mit 1997) und höchstens etwa 6 Schritte je Zeile.\n"
    "Tipp: Gehen Sie die Tabelle nur einmal durch und schlagen Sie die Gruppe im Dictionary nach."
)

# Obere Grenze: anzahl_je bei 100 000 Zeilen
ergebnis, schritte = zaehle_schritte(anzahl_je, daten, "person")
assert len(ergebnis) == 50000 and set(ergebnis.values()) == {2} and schritte <= 600000, (
    f"Bei 100 000 Zeilen mit 50 000 Personen ergibt anzahl_je {len(ergebnis)} Gruppen nach {schritte} Schritten; "
    "erwartet waren 50 000 Gruppen mit je 2 Zeilen und höchstens etwa 6 Schritte je Zeile."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Anmelden: im Schnitt 33.3 Sekunden\nSuchen: im Schnitt 71.0 Sekunden"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
