# Automatisch erzeugt aus lehrkraft/muster/3_041_sprintauswahl.py - nicht von Hand ändern.
# vorlage-hash: 09cd3bea9296887a
# text-hash: fab6d849e9239bb8
# thema: datenanalyse
# inhalt: pandas: Masken, sort_values

import pandas as pd

SPALTEN = ["nummer", "titel", "punkte", "prioritaet", "status"]
BEISPIEL = [
    {"nummer": 11, "titel": "Login", "punkte": 5, "prioritaet": 1, "status": "erledigt"},
    {"nummer": 12, "titel": "Export", "punkte": 8, "prioritaet": 2, "status": "offen"},
    {"nummer": 13, "titel": "Suche", "punkte": 3, "prioritaet": 1, "status": "in Arbeit"},
    {"nummer": 14, "titel": "Hilfe", "punkte": 2, "prioritaet": 3, "status": "offen"},
    {"nummer": 15, "titel": "Import", "punkte": 13, "prioritaet": 2, "status": "offen"},
]


def tabelle(zeilen):
    """Baut einen DataFrame mit den fünf Spalten, auch wenn zeilen leer ist."""
    return pd.DataFrame(zeilen, columns=SPALTEN)


def erster_unterschied(ergebnis, erwartet):
    """Beschreibt die erste Stelle, an der sich zwei Nummernlisten unterscheiden."""
    if not isinstance(ergebnis, list):
        return f"Ergebnis: {ergebnis}"
    for stelle in range(min(len(ergebnis), len(erwartet))):
        if ergebnis[stelle] != erwartet[stelle]:
            return f"an Stelle {stelle} steht Nummer {ergebnis[stelle]}, erwartet war {erwartet[stelle]}"
    return f"{len(ergebnis)} Nummern statt {len(erwartet)}"


def nummern(ergebnis):
    """Die Nummern der Zeilen eines Ergebnisses; ist es kein DataFrame, eine Beschreibung."""
    if not isinstance(ergebnis, pd.DataFrame):
        return f"kein DataFrame, sondern {type(ergebnis).__name__}: {ergebnis!r}"
    if "nummer" not in ergebnis.columns:
        return f"ein DataFrame ohne Spalte nummer (Spalten: {list(ergebnis.columns)})"
    return ergebnis["nummer"].tolist()


def zeilen_von(ergebnis):
    """Alle Zeilen eines DataFrames als Liste von Dictionaries, ohne Index."""
    if not isinstance(ergebnis, pd.DataFrame):
        return f"kein DataFrame, sondern {type(ergebnis).__name__}"
    return ergebnis.to_dict("records")


def spaltenwerte_von(ergebnis):
    """Die Zeilen eines DataFrames als Dictionaries, nur mit den fünf Spalten; zusätzliche Spalten stören nicht."""
    if isinstance(ergebnis, pd.DataFrame) and set(SPALTEN) <= set(ergebnis.columns):
        return ergebnis[SPALTEN].to_dict("records")
    return zeilen_von(ergebnis)


def zufallsbacklog(zufall, anzahl):
    """Erzeugt anzahl zufällige Einträge mit eindeutigen Nummern in zufälliger Reihenfolge."""
    nummern_liste = zufall.sample(range(1, 10**6), anzahl)
    zeilen = []
    for nummer in nummern_liste:
        zeilen.append(
            {
                "nummer": nummer,
                "titel": zufall.choice(["Login", "Export", "Suche", "Hilfe", "Import"]),
                "punkte": zufall.choice([0, 1, 2, 3, 5, 8, 13, 100, zufall.randint(0, 100)]),
                "prioritaet": zufall.randint(1, 5),
                "status": zufall.choice(["offen", "in Arbeit", "erledigt"]),
            }
        )
    return zeilen


def vergleich_reihenfolge(zeilen):
    """Vergleichslösung ohne pandas: filtert und sortiert die Dictionaries mit sorted."""
    offen = [zeile for zeile in zeilen if zeile["status"] != "erledigt"]
    return [zeile["nummer"] for zeile in sorted(offen, key=lambda z: (z["prioritaet"], -z["punkte"], z["nummer"]))]


# nicht_erledigt im Beispiel
ergebnis = nicht_erledigt(tabelle(BEISPIEL))
assert nummern(ergebnis) == [12, 13, 14, 15], (
    f"nicht_erledigt(backlog) hat die Nummern {nummern(ergebnis)}, erwartet war [12, 13, 14, 15].\n"
    'Tipp: backlog[backlog["status"] != "erledigt"] behält die übrigen Zeilen.'
)

# nicht_erledigt behält alle Spalten und Werte
ergebnis = nicht_erledigt(tabelle(BEISPIEL))
assert zeilen_von(ergebnis) == BEISPIEL[1:], (
    f"nicht_erledigt(backlog) ergibt die Zeilen {zeilen_von(ergebnis)}, erwartet waren die Zeilen 12 bis 15 vollständig."
)

# nicht_erledigt: "in Arbeit" zählt als nicht erledigt (nicht nur "offen" behalten!)
zeilen = [
    {"nummer": 1, "titel": "A", "punkte": 1, "prioritaet": 1, "status": "in Arbeit"},
    {"nummer": 2, "titel": "B", "punkte": 2, "prioritaet": 1, "status": "erledigt"},
    {"nummer": 3, "titel": "C", "punkte": 3, "prioritaet": 1, "status": "in Arbeit"},
]
ergebnis = nicht_erledigt(tabelle(zeilen))
assert nummern(ergebnis) == [1, 3], (
    f"Bei zwei Einträgen \"in Arbeit\" und einem \"erledigt\" ergibt nicht_erledigt die Nummern {nummern(ergebnis)}, "
    "erwartet war [1, 3]."
)

# nicht_erledigt, wenn alles erledigt ist
ergebnis = nicht_erledigt(tabelle([{**zeile, "status": "erledigt"} for zeile in BEISPIEL]))
assert nummern(ergebnis) == [], f"Sind alle Einträge erledigt, ergibt nicht_erledigt die Nummern {nummern(ergebnis)}, erwartet war []."

# grosse_brocken im Beispiel
ergebnis = grosse_brocken(tabelle(BEISPIEL), 5)
assert nummern(ergebnis) == [12, 15], (
    f"grosse_brocken(backlog, 5) hat die Nummern {nummern(ergebnis)}, erwartet war [12, 15] "
    "(Nummer 11 hat zwar 5 Punkte, ist aber erledigt).\n"
    "Tipp: Verknüpfen Sie beide Masken mit & und setzen Sie jeden Vergleich in Klammern."
)

# grosse_brocken: genau mindestens Story Points zählen mit
ergebnis = grosse_brocken(tabelle(BEISPIEL), 8)
assert nummern(ergebnis) == [12, 15], (
    f"grosse_brocken(backlog, 8) hat die Nummern {nummern(ergebnis)}, erwartet war [12, 15] (8 Punkte sind mindestens 8)."
)

# grosse_brocken mit einer anderen Grenze (nicht fest hinschreiben!)
ergebnis = grosse_brocken(tabelle(BEISPIEL), 3)
assert nummern(ergebnis) == [12, 13, 15], f"grosse_brocken(backlog, 3) hat die Nummern {nummern(ergebnis)}, erwartet war [12, 13, 15]."

# grosse_brocken mit der Grenze 0: alle nicht erledigten
ergebnis = grosse_brocken(tabelle(BEISPIEL), 0)
assert nummern(ergebnis) == [12, 13, 14, 15], f"grosse_brocken(backlog, 0) hat die Nummern {nummern(ergebnis)}, erwartet war [12, 13, 14, 15]."

# grosse_brocken behält alle Spalten und Werte
ergebnis = grosse_brocken(tabelle(BEISPIEL), 5)
assert spaltenwerte_von(ergebnis) == [BEISPIEL[1], BEISPIEL[4]], (
    f"grosse_brocken(backlog, 5) ergibt die Zeilen {zeilen_von(ergebnis)}, erwartet waren die Zeilen 12 und 15 vollständig."
)

# planungsreihenfolge im Beispiel
ergebnis = planungsreihenfolge(tabelle(BEISPIEL))
assert nummern(ergebnis) == [13, 15, 12, 14], (
    f"planungsreihenfolge(backlog) hat die Nummern {nummern(ergebnis)}, erwartet war [13, 15, 12, 14].\n"
    "Tipp: Erst die erledigten Einträge entfernen, dann mit sort_values sortieren."
)

# planungsreihenfolge behält alle Spalten und Werte
ergebnis = planungsreihenfolge(tabelle(BEISPIEL))
assert spaltenwerte_von(ergebnis) == [BEISPIEL[2], BEISPIEL[4], BEISPIEL[1], BEISPIEL[3]], (
    f"planungsreihenfolge(backlog) ergibt die Zeilen {zeilen_von(ergebnis)}, erwartet waren die Zeilen 13, 15, 12 "
    "und 14 vollständig."
)

# planungsreihenfolge: bei gleicher Priorität die größere Schätzung zuerst
zeilen = [
    {"nummer": 1, "titel": "A", "punkte": 2, "prioritaet": 2, "status": "offen"},
    {"nummer": 2, "titel": "B", "punkte": 8, "prioritaet": 2, "status": "offen"},
    {"nummer": 3, "titel": "C", "punkte": 5, "prioritaet": 2, "status": "offen"},
]
ergebnis = planungsreihenfolge(tabelle(zeilen))
assert nummern(ergebnis) == [2, 3, 1], (
    f"Bei gleicher Priorität und 2, 8 und 5 Punkten ergibt planungsreihenfolge {nummern(ergebnis)}, erwartet war [2, 3, 1].\n"
    "Tipp: ascending=[True, False, True] sortiert die zweite Spalte absteigend."
)

# planungsreihenfolge: bei gleicher Priorität und Schätzung nach Nummer
zeilen = [
    {"nummer": 30, "titel": "A", "punkte": 3, "prioritaet": 4, "status": "offen"},
    {"nummer": 10, "titel": "B", "punkte": 3, "prioritaet": 4, "status": "in Arbeit"},
    {"nummer": 20, "titel": "C", "punkte": 3, "prioritaet": 4, "status": "offen"},
]
ergebnis = planungsreihenfolge(tabelle(zeilen))
assert nummern(ergebnis) == [10, 20, 30], (
    f"Bei gleicher Priorität und Schätzung ergibt planungsreihenfolge {nummern(ergebnis)}, erwartet war [10, 20, 30]."
)

# planungsreihenfolge lässt erledigte Einträge weg
zeilen = [
    {"nummer": 1, "titel": "A", "punkte": 3, "prioritaet": 1, "status": "erledigt"},
    {"nummer": 2, "titel": "B", "punkte": 3, "prioritaet": 5, "status": "offen"},
]
ergebnis = planungsreihenfolge(tabelle(zeilen))
assert nummern(ergebnis) == [2], f"planungsreihenfolge mit einem erledigten Eintrag 1 ergibt {nummern(ergebnis)}, erwartet war [2]."

# Die übergebene Tabelle bleibt unverändert
backlog_test = tabelle(BEISPIEL)
nicht_erledigt(backlog_test)
grosse_brocken(backlog_test, 5)
planungsreihenfolge(backlog_test)
assert zeilen_von(backlog_test) == BEISPIEL and list(backlog_test.index) == [0, 1, 2, 3, 4], (
    f"Nach den drei Aufrufen enthält das Backlog {zeilen_von(backlog_test)}; erwartet war das unveränderte Beispiel.\n"
    "Tipp: Masken und sort_values liefern neue Tabellen; inplace=True oder del verändern das Original."
)

# nicht_erledigt mit einer leeren Tabelle
ergebnis = nummern(nicht_erledigt(tabelle([])))
assert ergebnis == [], f"Mit einem leeren Backlog ergibt nicht_erledigt {ergebnis}, erwartet war eine leere Tabelle."

# grosse_brocken mit einer leeren Tabelle
ergebnis = nummern(grosse_brocken(tabelle([]), 3))
assert ergebnis == [], f"Mit einem leeren Backlog ergibt grosse_brocken {ergebnis}, erwartet war eine leere Tabelle."

# planungsreihenfolge mit einer leeren Tabelle
ergebnis = nummern(planungsreihenfolge(tabelle([])))
assert ergebnis == [], f"Mit einem leeren Backlog ergibt planungsreihenfolge {ergebnis}, erwartet war eine leere Tabelle."

# Die Ausgabe des Programms
erwartet = "[12, 13, 14, 15]\n[12, 15]\n[13, 15, 12, 14]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Backlogs
zufall = Zufall(3041)
for _ in range(60):
    zeilen = zufallsbacklog(zufall, zufall.randint(0, 15))
    mindestens = zufall.randint(0, 100)
    erwartet_offen = [z["nummer"] for z in zeilen if z["status"] != "erledigt"]
    erwartet_gross = [z["nummer"] for z in zeilen if z["status"] != "erledigt" and z["punkte"] >= mindestens]
    ergebnis = [nummern(nicht_erledigt(tabelle(zeilen))), nummern(grosse_brocken(tabelle(zeilen), mindestens))]
    assert ergebnis == [erwartet_offen, erwartet_gross], (
        f"Beim Backlog {zeilen} und mindestens = {mindestens} ergeben nicht_erledigt und grosse_brocken {ergebnis}, "
        f"erwartet war {[erwartet_offen, erwartet_gross]}."
    )
    ergebnis = nummern(planungsreihenfolge(tabelle(zeilen)))
    assert ergebnis == vergleich_reihenfolge(zeilen), (
        f"Beim Backlog {zeilen} ergibt planungsreihenfolge {ergebnis}, erwartet war {vergleich_reihenfolge(zeilen)}."
    )

# Obere Grenze: 10 000 Zeilen
zeilen = zufallsbacklog(zufall, 10000)
ergebnis = nummern(planungsreihenfolge(tabelle(zeilen)))
erwartet = vergleich_reihenfolge(zeilen)
assert ergebnis == erwartet, (
    f"Bei 10 000 Zeilen stimmt die Reihenfolge von planungsreihenfolge nicht: {erster_unterschied(ergebnis, erwartet)}."
)

# Obere Grenze: grosse_brocken mit 10 000 Zeilen
ergebnis = nummern(grosse_brocken(tabelle(zeilen), 50))
erwartet = [z["nummer"] for z in zeilen if z["status"] != "erledigt" and z["punkte"] >= 50]
assert ergebnis == erwartet, (
    f"Bei 10 000 Zeilen stimmt das Ergebnis von grosse_brocken(backlog, 50) nicht: {erster_unterschied(ergebnis, erwartet)}."
)
