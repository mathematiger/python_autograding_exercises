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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def grosse_brocken(backlog, mindestens):
    """Gibt die nicht erledigten Einträge mit mindestens so vielen Story Points zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def planungsreihenfolge(backlog):
    """Gibt die nicht erledigten Einträge nach Priorität, Schätzung und Nummer sortiert zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


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
