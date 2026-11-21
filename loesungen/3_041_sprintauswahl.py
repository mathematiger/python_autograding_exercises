# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_041_sprintauswahl.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_041_sprintauswahl

"""Aufgabe 3_041 – Sprintauswahl                                 Stufe 3 ★★★☆☆

Ein agiles Team sammelt alle Anforderungen im Product Backlog. Jeder
Eintrag hat eine Nummer, einen Titel, eine Schätzung in Story Points
(wie aufwendig er ist), eine Priorität von 1 (am wichtigsten) bis 5 und
einen Status: "offen", "in Arbeit" oder "erledigt". Vor jeder
Sprintplanung, also vor dem Festlegen der Arbeit für die nächsten zwei
Wochen, will das Team das Backlog als pandas-DataFrame auswerten.
Schreiben Sie drei Funktionen:

- `nicht_erledigt(backlog)` gibt einen DataFrame mit allen Einträgen
  zurück, deren Status nicht "erledigt" ist, in der ursprünglichen
  Reihenfolge.
- `grosse_brocken(backlog, mindestens)` gibt die nicht erledigten
  Einträge mit mindestens so vielen Story Points zurück, in der
  ursprünglichen Reihenfolge.
- `planungsreihenfolge(backlog)` gibt die nicht erledigten Einträge
  sortiert zurück: zuerst nach Priorität (1 zuerst), bei gleicher
  Priorität die größeren Schätzungen zuerst, bei gleicher Priorität und
  Schätzung nach Nummer aufsteigend.

Die übergebene Tabelle bleibt jedes Mal unverändert. Welchen Index die
zurückgegebenen Zeilen haben, ist egal.

    backlog = pd.DataFrame([
        {"nummer": 11, "titel": "Login", "punkte": 5, "prioritaet": 1, "status": "erledigt"},
        {"nummer": 12, "titel": "Export", "punkte": 8, "prioritaet": 2, "status": "offen"},
        {"nummer": 13, "titel": "Suche", "punkte": 3, "prioritaet": 1, "status": "in Arbeit"},
        {"nummer": 14, "titel": "Hilfe", "punkte": 2, "prioritaet": 3, "status": "offen"},
        {"nummer": 15, "titel": "Import", "punkte": 13, "prioritaet": 2, "status": "offen"},
    ])
    nicht_erledigt(backlog)["nummer"].tolist()       →  [12, 13, 14, 15]
    grosse_brocken(backlog, 5)["nummer"].tolist()    →  [12, 15]
    planungsreihenfolge(backlog)["nummer"].tolist()  →  [13, 15, 12, 14]

Grenzen: Das Backlog hat 0 bis 10 000 Zeilen und genau die Spalten
nummer, titel, punkte, prioritaet und status. nummer ist eindeutig,
punkte ist eine ganze Zahl von 0 bis 100, prioritaet eine von 1 bis 5,
status einer der drei Texte oben; mindestens ist eine ganze Zahl von 0
bis 100. Auch eine leere Tabelle mit diesen Spalten ist möglich.

Hintergrund: Wie man einen DataFrame anlegt und Spalten auswählt, steht
in Aufgabe 3_038. Ein Vergleich mit einer ganzen Spalte ergibt keine
einzelne Zahl, sondern für jede Zeile True oder False, eine sogenannte
Maske. Setzt man die Maske in eckige Klammern, bleiben nur die Zeilen
mit True übrig, in der alten Reihenfolge; die Tabelle selbst bleibt,
wie sie war:

    maske = df["cpu"] > 50          # z. B. [False, True, True]
    df[maske]                       # nur die Zeilen mit cpu über 50
    df[df["host"] != "db1"]         # alles außer db1

Masken verknüpft man mit & (und), | (oder) und ~ (nicht), nicht mit
and, or und not; jeder Vergleich braucht dann eigene Klammern:

    df[(df["cpu"] > 50) & (df["host"] != "db1")]

Sortiert wird mit sort_values. by nennt die Spalte oder eine Liste von
Spalten, ascending sagt je Spalte, ob aufsteigend (True) oder absteigend
(False). Auch sort_values gibt eine neue Tabelle zurück:

    df.sort_values(by=["raum", "cpu"], ascending=[True, False])
"""

import pandas as pd


def nicht_erledigt(backlog):
    """Gibt die Einträge zurück, deren Status nicht "erledigt" ist."""
    return backlog[backlog["status"] != "erledigt"]


def grosse_brocken(backlog, mindestens):
    """Gibt die nicht erledigten Einträge mit mindestens so vielen Story Points zurück."""
    return backlog[(backlog["status"] != "erledigt") & (backlog["punkte"] >= mindestens)]


def planungsreihenfolge(backlog):
    """Gibt die nicht erledigten Einträge nach Priorität, Schätzung und Nummer sortiert zurück."""
    offen = nicht_erledigt(backlog)
    return offen.sort_values(by=["prioritaet", "punkte", "nummer"], ascending=[True, False, True])


backlog = pd.DataFrame(
    [
        {"nummer": 11, "titel": "Login", "punkte": 5, "prioritaet": 1, "status": "erledigt"},
        {"nummer": 12, "titel": "Export", "punkte": 8, "prioritaet": 2, "status": "offen"},
        {"nummer": 13, "titel": "Suche", "punkte": 3, "prioritaet": 1, "status": "in Arbeit"},
        {"nummer": 14, "titel": "Hilfe", "punkte": 2, "prioritaet": 3, "status": "offen"},
        {"nummer": 15, "titel": "Import", "punkte": 13, "prioritaet": 2, "status": "offen"},
    ]
)
print(nicht_erledigt(backlog)["nummer"].tolist())
print(grosse_brocken(backlog, 5)["nummer"].tolist())
print(planungsreihenfolge(backlog)["nummer"].tolist())


# Idee: backlog["status"] != "erledigt" ist eine Maske, backlog[maske] behält nur die passenden
# Zeilen. Für grosse_brocken kommt mit & eine zweite Maske backlog["punkte"] >= mindestens dazu, jeder
# Vergleich in eigenen Klammern. planungsreihenfolge filtert erst (mit nicht_erledigt) und sortiert
# dann mit sort_values nach drei Spalten, die zweite absteigend.
# Anderer Weg: backlog.query('status != "erledigt" and punkte >= @mindestens') schreibt die Bedingung
# als Text; ~backlog["status"].eq("erledigt") oder backlog["status"].isin(["offen", "in Arbeit"])
# bilden dieselbe Maske. Statt drei Spalten auf einmal kann man auch nacheinander stabil sortieren
# (kind="stable"), dann aber zuerst nach nummer und zuletzt nach prioritaet.
# Typische Fehler: and statt & (ValueError: The truth value of a Series is ambiguous), fehlende
# Klammern um die Vergleiche, nur status == "offen" behalten (dann fehlt "in Arbeit"), > statt >=,
# ascending=False für alle Spalten oder sort_values(..., inplace=True) auf der übergebenen Tabelle.
# Laufzeit: Filtern O(n), Sortieren O(n log n).
