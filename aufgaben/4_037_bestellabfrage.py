"""Aufgabe 4_037 – Bestellabfrage                                Stufe 4 ★★★★☆

Ein Versandhändler für Computerzubehör speichert seine Bestellungen in
einer Tabelle mit drei Spalten: der Bestellnummer, dem Namen des Kunden
und dem Betrag in Cent (ganze Zahlen, damit beim Addieren kein
Rundungsfehler entsteht). Die Tabelle kommt als pandas-DataFrame aus dem
Shopsystem. Die Abfragen dafür hat die Datenbankabteilung bisher in SQL
geschrieben, und so soll es bleiben: Schreiben Sie die drei Funktionen
mit DuckDB, also mit SQL direkt auf dem DataFrame. Jede gibt eine
gewöhnliche Python-Liste zurück.

- `bestellungen_von(bestellungen, kunde)` gibt die Bestellnummern des
  Kunden als Liste von ganzen Zahlen zurück, aufsteigend sortiert. Der
  Name kommt aus einem Suchfeld und kann jedes Zeichen enthalten, auch
  ein Apostroph wie in "O'Brien".
- `umsatz_je_kunde(bestellungen)` gibt für jeden Kunden ein Tupel
  (kunde, summe_cent, anzahl_bestellungen) zurück, sortiert nach der
  Summe absteigend, bei gleicher Summe nach dem Namen aufsteigend.
- `stammkunden(bestellungen, mindestanzahl)` gibt die Namen der Kunden
  mit mindestens mindestanzahl Bestellungen zurück, alphabetisch
  sortiert.

    bestellungen = pd.DataFrame({
        "bestellnummer": [1001, 1002, 1003, 1004, 1005],
        "kunde": ["Nowak", "Becker", "Nowak", "O'Brien", "Becker"],
        "betrag_cent": [4999, 12900, 1500, 7900, 2500],
    })
    bestellungen_von(bestellungen, "Nowak")   →  [1001, 1003]
    umsatz_je_kunde(bestellungen)  →  [("Becker", 15400, 2),
                                       ("O'Brien", 7900, 1),
                                       ("Nowak", 6499, 2)]
    stammkunden(bestellungen, 2)              →  ["Becker", "Nowak"]

Grenzen: 0 bis 100 000 Zeilen mit genau diesen drei Spalten.
bestellnummer ist eindeutig, eine ganze Zahl von 1 bis 10**9, kunde ein
nicht leerer Text mit beliebigen Zeichen, betrag_cent eine ganze Zahl
von 0 bis 10**7. kunde in bestellungen_von ist ein beliebiger Text, auch
einer, der in der Tabelle nicht vorkommt. 1 ≤ mindestanzahl ≤ 100 000.

Hintergrund: DuckDB ist eine Datenbank, die ohne eigenen Server in
Python läuft. Nach import duckdb führt duckdb.sql(abfrage) eine
SQL-Abfrage aus. Steht hinter FROM der Name einer Python-Variablen, die
einen DataFrame enthält (auch ein Parameter der Funktion), liest DuckDB
den DataFrame wie eine Tabelle; nichts wird kopiert oder gespeichert.
.fetchall() liefert das Ergebnis als Liste von Tupeln, ein Tupel je
Zeile, auch wenn nur eine Spalte ausgewählt wird:

    import duckdb

    def lauter_hosts(messungen):
        return duckdb.sql(
            "SELECT host, cpu FROM messungen WHERE cpu > 90 ORDER BY cpu DESC, host"
        ).fetchall()

    lauter_hosts(df)  →  [("db1", 97), ("web2", 93)]

Eine Abfrage hat die Form SELECT spalten FROM tabelle WHERE bedingung
ORDER BY spalten. ORDER BY sortiert aufsteigend, mit DESC hinter einer
Spalte absteigend. GROUP BY spalte fasst alle Zeilen mit demselben Wert
zu einer Zeile zusammen; SUM(spalte) und COUNT(*) rechnen dann je
Gruppe, und mit AS bekommt das Ergebnis einen Namen, den man in ORDER BY
benutzen kann. HAVING ist wie WHERE, prüft aber die fertigen Gruppen:

    SELECT host, COUNT(*) AS anzahl FROM messungen
    GROUP BY host HAVING COUNT(*) >= 3 ORDER BY host

Texte stehen in SQL in einfachen Anführungszeichen ('db1'). Einen Wert
aus Python darf man darum nie mit einem f-String in die Abfrage
schreiben: Ein Name wie O'Brien beendet den Text zu früh, und ein
böswillig gewählter Name könnte die Abfrage sogar umschreiben
(SQL-Injection). Stattdessen setzt man ein ? an die Stelle und gibt die
Werte als Liste mit; das geht mit duckdb.execute statt duckdb.sql:

    duckdb.execute("SELECT cpu FROM messungen WHERE host = ?", [name]).fetchall()

DuckDB setzt den Wert dann sicher ein, egal welche Zeichen er enthält.
"""

import duckdb
import pandas as pd


def bestellungen_von(bestellungen, kunde):
    """Gibt die Bestellnummern des Kunden aufsteigend sortiert zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def umsatz_je_kunde(bestellungen):
    """Gibt (kunde, summe_cent, anzahl_bestellungen) je Kunde zurück, größte Summe zuerst."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def stammkunden(bestellungen, mindestanzahl):
    """Gibt die Kunden mit mindestens mindestanzahl Bestellungen alphabetisch zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


bestellungen = pd.DataFrame(
    {
        "bestellnummer": [1001, 1002, 1003, 1004, 1005],
        "kunde": ["Nowak", "Becker", "Nowak", "O'Brien", "Becker"],
        "betrag_cent": [4999, 12900, 1500, 7900, 2500],
    }
)
print(bestellungen_von(bestellungen, "Nowak"))
print(umsatz_je_kunde(bestellungen))
print(stammkunden(bestellungen, 2))
