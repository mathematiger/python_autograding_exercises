"""Aufgabe 5_015 – Ticketauswertung                             Stufe 5 ★★★★★

Der IT-Service eines Krankenhauses bekommt jeden Tag Hunderte Tickets:
Störungen und Anfragen zu Druckern, zum Netz, zu Arztbriefen in der
Software. Für jedes Ticket ist vereinbart, innerhalb wie vieler Minuten
es gelöst sein muss (die Frist aus dem Service-Level-Agreement, kurz
SLA). Jeden Monat soll ein Bericht zeigen, wie es in jeder Kategorie
lief. Drei Teams wollen ihn mit verschiedenen Werkzeugen erstellen:
das Controlling mit pandas, die Entwicklung mit polars, der Betrieb mit
SQL in seiner Datenbank. Damit die Zahlen sicher übereinstimmen,
schreiben Sie dieselbe Auswertung dreimal:

- `bericht_pandas(tickets, mindestens)` bekommt ein pandas-DataFrame,
- `bericht_polars(tickets, mindestens)` bekommt ein polars-DataFrame,
- `bericht_sql(verbindung, mindestens)` bekommt eine Verbindung zu
  DuckDB, in der die Tabelle tickets liegt.

Die Tickets haben die Spalten nummer, kategorie, status ("offen" oder
"geschlossen"), minuten (Dauer bis zur Lösung, bei offenen Tickets die
bisherige Dauer) und frist (in Minuten). Ausgewertet werden nur
geschlossene Tickets. Jede Funktion gibt für jede Kategorie mit
mindestens `mindestens` geschlossenen Tickets das Tupel (kategorie,
anzahl, schnitt, verstoesse) zurück: anzahl der geschlossenen
Tickets, schnitt der Durchschnitt ihrer minuten als Kommazahl (nicht
gerundet) und verstoesse die Anzahl der Tickets mit minuten größer als
frist. Das Ergebnis ist eine Liste, sortiert nach kategorie. Benutzen
Sie in jeder Funktion nur die jeweilige Bibliothek, keine for- oder
while-Schleife.

    nummer  kategorie  status       minuten  frist
    1       drucker    geschlossen  45       60
    2       netz       geschlossen  130     120
    3       drucker    geschlossen  75       60
    4       netz       offen        300     120
    5       software   geschlossen  20      240
    6       drucker    geschlossen  60       60

    bericht_pandas(tickets, 1)   →  [("drucker", 3, 60.0, 1), ("netz", 1, 130.0, 1), ("software", 1, 20.0, 0)]
    bericht_polars(tickets, 2)   →  [("drucker", 3, 60.0, 1)]

bericht_sql liefert dasselbe aus der Tabelle tickets.

Grenzen: 0 bis 10 000 Tickets mit verschiedenen Nummern. kategorie ist
ein nicht leerer Text aus Kleinbuchstaben, minuten und frist sind
ganze Zahlen von 0 bis 10**6. Genau die Frist einzuhalten ist kein
Verstoß. mindestens ist eine ganze Zahl von 1 bis 10 000. Die Zahlen in
den Tupeln dürfen Python-Zahlen oder Zahlen der Bibliothek sein
(numpy.int64 …), solange sie den richtigen Wert haben.

Hintergrund: Fast jede Auswertung einer Tabelle besteht aus denselben
Schritten: Zeilen auswählen, eine neue Spalte berechnen, nach einer
Spalte gruppieren, je Gruppe zusammenfassen, Gruppen auswählen,
sortieren. In SQL heißen sie WHERE, SELECT, GROUP BY, Aggregatfunktion,
HAVING und ORDER BY, und pandas (Aufgabe 5_006) und polars (Aufgabe
5_012) haben für jeden Schritt eine Methode. Am Beispiel „Anzahl und
größte Frist je status, nur Tickets mit frist über 30“:

    # pandas: Masken, groupby mit benannten Aggregationen
    gefiltert = tickets[tickets["frist"] > 30]
    ergebnis = gefiltert.groupby("status", as_index=False).agg(
        anzahl=("nummer", "size"), groesste=("frist", "max"))
    ergebnis = ergebnis[ergebnis["anzahl"] >= 2].sort_values("status")
    zeilen = list(ergebnis.itertuples(index=False, name=None))

    # polars: Ausdrücke mit pl.col, group_by und agg
    ergebnis = (tickets.filter(pl.col("frist") > 30)
                .group_by("status")
                .agg(pl.len().alias("anzahl"), pl.col("frist").max().alias("groesste"))
                .filter(pl.col("anzahl") >= 2)
                .sort("status"))
    zeilen = ergebnis.rows()

    # SQL in DuckDB: Werte aus Python als Parameter ?
    zeilen = verbindung.execute(
        "SELECT status, COUNT(*) AS anzahl, MAX(frist) AS groesste FROM tickets "
        "WHERE frist > 30 GROUP BY status HAVING COUNT(*) >= ? ORDER BY status",
        [2]).fetchall()

Die Unterschiede liegen im Detail. pandas legt die Gruppenspalte ohne
as_index=False in den Index und rechnet eine neue Spalte mit
tickets.assign(neu=…) oder tickets["neu"] = … aus. polars ändert nie
ein DataFrame, sondern baut aus Ausdrücken neue; die Reihenfolge der
Gruppen nach group_by ist zufällig, ohne sort also nicht verlässlich.
In SQL gilt WHERE für Zeilen vor dem Gruppieren und HAVING für Gruppen
danach. Einen Vergleich als Zahl zählt man überall gleich: Die Summe
über eine Spalte aus True und False ist die Anzahl der True, in pandas
(tickets["minuten"] > tickets["frist"]).sum(), in polars
(pl.col("minuten") > pl.col("frist")).sum(), in SQL
SUM(CASE WHEN minuten > frist THEN 1 ELSE 0 END) oder
COUNT(*) FILTER (WHERE minuten > frist). Den Durchschnitt liefern mean
bzw. AVG. Kommen in einer Tabelle keine passenden Zeilen vor, geben
alle drei eine leere Tabelle zurück.
"""

import io

import duckdb
import pandas as pd
import polars as pl


def bericht_pandas(tickets, mindestens):
    """Wertet die geschlossenen Tickets je Kategorie mit pandas aus."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bericht_polars(tickets, mindestens):
    """Wertet die geschlossenen Tickets je Kategorie mit polars aus."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bericht_sql(verbindung, mindestens):
    """Wertet die geschlossenen Tickets je Kategorie mit SQL in DuckDB aus."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


TICKETS_CSV = """nummer,kategorie,status,minuten,frist
1,drucker,geschlossen,45,60
2,netz,geschlossen,130,120
3,drucker,geschlossen,75,60
4,netz,offen,300,120
5,software,geschlossen,20,240
6,drucker,geschlossen,60,60
"""

tickets_pandas = pd.read_csv(io.StringIO(TICKETS_CSV))
tickets_polars = pl.read_csv(io.StringIO(TICKETS_CSV))
verbindung = duckdb.connect()
verbindung.execute("CREATE TABLE tickets AS SELECT * FROM tickets_pandas")
print(bericht_pandas(tickets_pandas, 1))
print(bericht_polars(tickets_polars, 2))
print(bericht_sql(verbindung, 1))
