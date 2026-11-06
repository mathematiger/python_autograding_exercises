"""Aufgabe 5_015 – Soll-Ist-Vergleich                            Stufe 5 ★★★★★

Die Buchhaltung eines Betriebs bearbeitet jede eingehende Rechnung in
festen Prozessschritten: erfassen, sachlich prüfen, freigeben, buchen.
Für jeden Schritt gibt es eine Sollzeit in Minuten, also die Zeit, die
er höchstens dauern soll. Das Rechnungsprogramm protokolliert für jeden
Vorgang (eine Rechnung) und jeden Schritt die tatsächliche Dauer, die
Istzeit. Ein Soll-Ist-Vergleich soll zeigen, welche Schritte ihre
Sollzeit am häufigsten reißen.

Die Auswertung soll später in eine bestehende Software eingebaut werden;
welche Bibliothek dort läuft, steht noch nicht fest. Darum schreiben Sie
dieselbe Auswertung dreimal: mit pandas, mit polars und mit SQL in
DuckDB. Jede der drei Fassungen verknüpft die Messungen über die Spalte
schritt mit den Sollzeiten und liefert je Schritt mit mindestens einer
Messung eine Zeile mit den Spalten

- `schritt`: der Name des Schritts,
- `anzahl`: wie viele Messungen es zu dem Schritt gibt,
- `schnitt`: der Durchschnitt der Istzeiten, als Kommazahl, nicht gerundet,
- `soll`: die Sollzeit des Schritts,
- `ueberschritten`: bei wie vielen Messungen die Istzeit größer als die
  Sollzeit war (genau die Sollzeit zählt nicht als überschritten),

sortiert nach ueberschritten absteigend, bei Gleichstand nach schritt
aufsteigend. Schritte, die nur in den Sollzeiten stehen, kommen nicht
vor.

- `auswertung_pandas(messungen, sollzeiten)` bekommt zwei pandas-
  DataFrames und gibt einen pandas-DataFrame mit genau diesen fünf
  Spalten in dieser Reihenfolge zurück (der Index ist egal). Die beiden
  übergebenen DataFrames bleiben unverändert.
- `auswertung_polars(messungen, sollzeiten)` bekommt zwei polars-
  DataFrames und gibt einen polars-DataFrame mit denselben Spalten
  zurück.
- `auswertung_sql(verbindung)` bekommt eine DuckDB-Verbindung, in der
  die Tabellen messungen und sollzeiten angelegt sind, und gibt das
  Ergebnis einer einzigen SQL-Abfrage als Liste von Tupeln zurück.

Die Messungen haben die Spalten vorgang, schritt und ist, die
Sollzeiten die Spalten schritt und soll. Die Funktionen als_pandas,
als_polars und als_duckdb im Code bauen diese Tabellen aus Listen.

    messungen = [(1, "erfassen", 4), (1, "pruefen", 25), (1, "freigeben", 90),
                 (1, "buchen", 3), (2, "erfassen", 7), (2, "pruefen", 15),
                 (2, "freigeben", 200), (2, "buchen", 2), (3, "erfassen", 5),
                 (3, "pruefen", 32), (3, "freigeben", 150)]
    sollzeiten = [("erfassen", 5), ("pruefen", 20), ("freigeben", 120),
                  ("buchen", 5), ("mahnen", 10)]
    auswertung_sql(als_duckdb(messungen, sollzeiten))
        →  [("freigeben", 3, 146.666…, 120, 2), ("pruefen", 3, 24.0, 20, 2),
            ("erfassen", 3, 5.333…, 5, 1), ("buchen", 2, 2.5, 5, 0)]
    auswertung_pandas(*als_pandas(messungen, sollzeiten))["schritt"].tolist()
        →  ["freigeben", "pruefen", "erfassen", "buchen"]
    auswertung_polars(*als_polars(messungen, sollzeiten)).rows()
        →  dieselben Tupel wie bei auswertung_sql

Benutzen Sie in jeder Funktion nur ihre eigene Bibliothek: in
auswertung_pandas weder polars noch DuckDB, in auswertung_polars weder
pandas noch DuckDB, und auswertung_sql rechnet ganz in SQL.

Grenzen: messungen hat 0 bis 100 000 Zeilen, sollzeiten 1 bis 1000.
vorgang ist eine ganze Zahl von 1 bis 10**9, schritt ein nicht leerer
Text aus Kleinbuchstaben und _, ist eine ganze Zahl von 0 bis 10**5,
soll eine ganze Zahl von 1 bis 10**5. In sollzeiten kommt jeder Schritt
genau einmal vor, und jeder Schritt aus messungen steht dort. Ein
Vorgang kann denselben Schritt mehrmals durchlaufen (etwa nach einer
Rückfrage); jede Zeile ist eine eigene Messung. Die Zeilen sind nicht
sortiert.

Hintergrund: Die drei Werkzeuge beschreiben Tabellenauswertungen auf
verschiedene Weise, aber die Bausteine sind immer dieselben: Tabellen
über einen Schlüssel verknüpfen (join), aus jeder Zeile etwas berechnen,
nach einer Spalte gruppieren und je Gruppe zusammenfassen (aggregieren),
zum Schluss sortieren. Wer diese Bausteine einmal kennt, kann zwischen
den Werkzeugen übersetzen.

pandas (Aufgabe 5_006) arbeitet Schritt für Schritt mit Methoden des
DataFrames. merge verknüpft zwei Tabellen; how="inner" (der Standard)
behält nur Zeilen, deren Schlüssel in beiden Tabellen vorkommt,
how="left" alle Zeilen der linken Tabelle. groupby(…).agg(…) fasst
zusammen; mit „benannten Aggregationen“ name=(spalte, funktion) legt man
die Namen der Ergebnisspalten gleich mit fest. as_index=False macht die
Gruppenspalte zu einer normalen Spalte statt zum Index:

    tabelle = auftraege.merge(kunden, on="kunde")
    tabelle["gross"] = tabelle["betrag"] > 1000      # Spalte aus True/False
    je_ort = tabelle.groupby("ort", as_index=False).agg(
        auftraege=("betrag", "size"),     # Anzahl Zeilen der Gruppe
        mittel=("betrag", "mean"),
        grosse=("gross", "sum"),          # True zählt als 1
    )
    je_ort.sort_values(["grosse", "ort"], ascending=[False, True])

Vorsicht: tabelle["gross"] = … ändert die Tabelle, auf der es steht.
Auf dem Ergebnis von merge ist das harmlos, weil merge eine neue Tabelle
liefert; auf einem übergebenen DataFrame verändert es die Daten der
aufrufenden Stelle. assign(gross=…) gibt stattdessen eine Kopie mit der
neuen Spalte zurück.

polars (Aufgabe 5_012) beschreibt Spalten mit Ausdrücken. Ein Ausdruck
wie pl.col("betrag") > 1000 kann direkt in agg stehen, eine Hilfsspalte
ist nicht nötig; .alias gibt dem Ergebnis einen Namen. pl.len() zählt
die Zeilen einer Gruppe, .first() nimmt den ersten Wert:

    (auftraege.join(kunden, on="kunde")              # Standard: how="inner"
        .group_by("ort")
        .agg(
            pl.len().alias("auftraege"),
            pl.col("betrag").mean().alias("mittel"),
            (pl.col("betrag") > 1000).sum().alias("grosse"),
        )
        .sort(["grosse", "ort"], descending=[True, False]))

Ein polars-DataFrame lässt sich nie an Ort und Stelle ändern; jede
Methode liefert einen neuen. Anders als pandas, das die Gruppen nach
dem Schlüssel sortiert, liefert group_by die Gruppen in beliebiger
Reihenfolge, die sich von Lauf zu Lauf ändern kann. Ohne sort am Ende
ist das Ergebnis also Glückssache.

In SQL steht die ganze Auswertung in einer Abfrage. DuckDB (Aufgabe
5_009) führt sie mit verbindung.execute(abfrage) aus, .fetchall()
liefert die Zeilen als Liste von Tupeln. JOIN … USING (spalte) verknüpft
über eine gleichnamige Spalte (wie inner bei pandas), LEFT JOIN behält
alle Zeilen der linken Tabelle. Jede Spalte im SELECT, die kein Aggregat
ist, muss im GROUP BY stehen. Eine Bedingung zählt man mit COUNT(*)
FILTER (WHERE …) oder mit SUM(CASE WHEN … THEN 1 ELSE 0 END):

    SELECT ort, COUNT(*) AS auftraege, AVG(betrag) AS mittel,
           COUNT(*) FILTER (WHERE betrag > 1000) AS grosse
    FROM auftraege JOIN kunden USING (kunde)
    GROUP BY ort
    ORDER BY grosse DESC, ort

Auch in SQL ist die Reihenfolge ohne ORDER BY nicht festgelegt. DESC
gilt nur für die Spalte, hinter der es steht; ort wird also aufsteigend
sortiert.

Die Ergebnisse vergleicht man über ihre Werte, nicht über print: bei
pandas df["spalte"].tolist() oder df.itertuples(index=False,
name=None), bei polars df.rows() oder df.to_dicts(), bei DuckDB
fetchall(). Die Zahlentypen unterscheiden sich dabei (numpy.int64, u32,
Python-int), die Werte nicht. Durchschnitte sind Kommazahlen; wer sie
vergleicht, lässt eine kleine Toleranz zu.
"""

import duckdb
import pandas as pd
import polars as pl


def als_pandas(messungen, sollzeiten):
    """Baut aus den Listen die beiden pandas-DataFrames (messungen, sollzeiten)."""
    tabelle = pd.DataFrame(messungen, columns=["vorgang", "schritt", "ist"])
    soll = pd.DataFrame(sollzeiten, columns=["schritt", "soll"])
    return (
        tabelle.astype({"vorgang": "int64", "schritt": "object", "ist": "int64"}),
        soll.astype({"schritt": "object", "soll": "int64"}),
    )


def als_polars(messungen, sollzeiten):
    """Baut aus den Listen die beiden polars-DataFrames (messungen, sollzeiten)."""
    tabelle = pl.DataFrame(messungen, schema={"vorgang": pl.Int64, "schritt": pl.String, "ist": pl.Int64}, orient="row")
    soll = pl.DataFrame(sollzeiten, schema={"schritt": pl.String, "soll": pl.Int64}, orient="row")
    return tabelle, soll


def als_duckdb(messungen, sollzeiten):
    """Gibt eine neue DuckDB-Verbindung mit den Tabellen messungen und sollzeiten zurück."""
    verbindung = duckdb.connect()
    verbindung.execute("CREATE TABLE messungen (vorgang BIGINT, schritt VARCHAR, ist BIGINT)")
    verbindung.execute("CREATE TABLE sollzeiten (schritt VARCHAR, soll BIGINT)")
    verbindung.executemany("INSERT INTO messungen VALUES (?, ?, ?)", messungen)
    verbindung.executemany("INSERT INTO sollzeiten VALUES (?, ?)", sollzeiten)
    return verbindung


def auswertung_pandas(messungen, sollzeiten):
    """Soll-Ist-Vergleich je Schritt mit pandas; gibt einen pandas-DataFrame zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auswertung_polars(messungen, sollzeiten):
    """Soll-Ist-Vergleich je Schritt mit polars; gibt einen polars-DataFrame zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auswertung_sql(verbindung):
    """Soll-Ist-Vergleich je Schritt mit SQL in DuckDB; gibt eine Liste von Tupeln zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


messungen = [
    (1, "erfassen", 4), (1, "pruefen", 25), (1, "freigeben", 90), (1, "buchen", 3),
    (2, "erfassen", 7), (2, "pruefen", 15), (2, "freigeben", 200), (2, "buchen", 2),
    (3, "erfassen", 5), (3, "pruefen", 32), (3, "freigeben", 150),
]
sollzeiten = [("erfassen", 5), ("pruefen", 20), ("freigeben", 120), ("buchen", 5), ("mahnen", 10)]
for schritt, anzahl, schnitt, soll, ueberschritten in auswertung_sql(als_duckdb(messungen, sollzeiten)):
    print(f"{schritt:<10} {anzahl:>3} {schnitt:>8.1f} {soll:>5} {ueberschritten:>3}")
print(auswertung_pandas(*als_pandas(messungen, sollzeiten))["schritt"].tolist())
print(auswertung_polars(*als_polars(messungen, sollzeiten))["ueberschritten"].to_list())
