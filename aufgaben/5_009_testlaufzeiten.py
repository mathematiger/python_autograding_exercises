"""Aufgabe 5_009 – Testlaufzeiten                                Stufe 5 ★★★★★

Ein Entwicklungsteam lässt bei jedem Build, also bei jedem automatischen
Übersetzen und Testen der Software, alle automatisierten Tests laufen.
Der Build-Server schreibt für jeden Test eine Zeile: die Nummer des
Builds, das Modul, zu dem der Test gehört, den Namen des Tests und wie
viele Millisekunden er gebraucht hat. Langsame Tests bremsen das ganze
Team, darum soll eine kleine Auswertung zeigen, wo es hakt. Die Daten
liegen als pandas-DataFrame vor; ausgewertet wird mit SQL in DuckDB.
Schreiben Sie drei Funktionen, die jeweils eine Abfrage mit einer
Fensterfunktion ausführen und das Ergebnis als Liste von Tupeln
zurückgeben:

- `langsamste_tests(laeufe, build, k)` gibt für den Build mit der Nummer
  build in jedem Modul die k langsamsten Tests zurück, als Tupel (modul,
  test, dauer_ms, platz). Platz 1 ist der langsamste Test des Moduls;
  brauchen zwei Tests gleich lange, kommt der mit dem alphabetisch
  kleineren Namen zuerst, die Plätze sind also immer 1, 2, 3, …
  Sortiert nach modul, dann platz. Gibt es den Build nicht, ist die
  Liste leer.
- `veraenderungen(laeufe)` gibt für jede Zeile das Tupel (modul, test,
  build, dauer_ms, differenz) zurück. differenz ist dauer_ms minus die
  Dauer desselben Tests (gleiches Modul, gleicher Name) im
  vorangehenden Build, in dem er lief, beim ersten Lauf des Tests None.
  Sortiert nach modul, test, build.
- `gesamtdauer(laeufe)` gibt für jeden Build das Tupel (build, summe,
  schnitt) zurück: summe ist die Dauer aller Tests des Builds, schnitt
  der Durchschnitt von summe über diesen und die bis zu zwei
  vorangehenden Builds (gleitender Durchschnitt; am Anfang über weniger
  Builds), als Kommazahl, nicht gerundet. Sortiert nach build.

    laeufe = pd.DataFrame({
        "build":    [101, 101, 101, 101, 102, 102, 102, 102, 103, 103],
        "modul":    ["login", "login", "login", "suche", "login", "login", "login", "suche", "login", "suche"],
        "test":     ["passwort", "sperre", "token", "volltext", "passwort", "sperre", "token", "volltext",
                     "passwort", "volltext"],
        "dauer_ms": [120, 340, 80, 900, 130, 310, 130, 1250, 125, 1100],
    })
    langsamste_tests(laeufe, 102, 2)
        →  [("login", "sperre", 310, 1), ("login", "passwort", 130, 2), ("suche", "volltext", 1250, 1)]
    veraenderungen(laeufe)[:3]
        →  [("login", "passwort", 101, 120, None), ("login", "passwort", 102, 130, 10),
            ("login", "passwort", 103, 125, -5)]
    gesamtdauer(laeufe)
        →  [(101, 1440, 1440.0), (102, 1820, 1630.0), (103, 1225, 1495.0)]

Benutzen Sie für die Auswertung SQL in DuckDB, nicht pandas.

Grenzen: laeufe hat 1 bis 10 000 Zeilen und die Spalten build (ganze
Zahlen von 1 bis 10**6), modul und test (nicht leere Texte aus
Kleinbuchstaben und _) und dauer_ms (ganze Zahlen von 0 bis 10**7).
Jede Kombination aus build, modul und test kommt höchstens einmal vor.
Die Builds sind nicht unbedingt lückenlos nummeriert, die Zeilen nicht
sortiert, und ein Test muss nicht in jedem Build laufen. build in
langsamste_tests ist eine ganze Zahl von 1 bis 10**6, k eine ganze Zahl
von 1 bis 100.

Hintergrund: DuckDB ist eine Datenbank, die ohne Server im eigenen
Python-Prozess läuft und SQL direkt auf DataFrames ausführen kann. Nach
import duckdb führt duckdb.sql(abfrage) eine Abfrage aus; steht in der
Abfrage hinter FROM der Name einer Python-Variablen, die ein DataFrame
enthält, liest DuckDB dieses DataFrame wie eine Tabelle. .fetchall()
liefert das Ergebnis als Liste von Tupeln, eine Zeile pro Tupel; ein
NULL aus SQL wird dabei zu None. Werte aus Python setzt man nicht mit
f-Strings in den SQL-Text, sondern als Parameter: ein ? im Text, die
Werte in einer Liste dazu, und zwar mit duckdb.execute(abfrage, werte)
statt duckdb.sql(abfrage).

    def teure_builds(laeufe, grenze):
        return duckdb.execute(
            "SELECT build, SUM(dauer_ms) FROM laeufe GROUP BY build HAVING SUM(dauer_ms) > ? ORDER BY build",
            [grenze],
        ).fetchall()

GROUP BY fasst die Zeilen einer Gruppe zu einer einzigen Zeile zusammen.
Eine Fensterfunktion rechnet dagegen für jede Zeile einen Wert aus,
indem sie auf ein „Fenster“ benachbarter Zeilen schaut; die Zeilen
bleiben alle erhalten. Das Fenster beschreibt OVER (…):

    SELECT modul, test, dauer_ms,
           ROW_NUMBER() OVER (PARTITION BY modul ORDER BY dauer_ms DESC) AS platz
    FROM laeufe

PARTITION BY modul teilt die Zeilen in Gruppen, ein Fenster pro Modul;
ORDER BY legt die Reihenfolge innerhalb des Fensters fest. ROW_NUMBER()
nummeriert die Zeilen jedes Fensters 1, 2, 3, … durch. RANK() gibt
gleichen Werten denselben Platz und lässt danach Plätze aus (1, 1, 3),
DENSE_RANK() lässt keine aus (1, 1, 2). Soll die Reihenfolge bei
Gleichstand eindeutig sein, gibt man hinter ORDER BY eine zweite Spalte
an. Weil Fensterfunktionen erst nach WHERE ausgewertet werden, kann man
nicht direkt WHERE platz <= 3 schreiben; man legt die Abfrage in eine
Unterabfrage oder schreibt dafür QUALIFY platz <= 3 (eine Erweiterung
von DuckDB).

LAG(spalte) OVER (PARTITION BY … ORDER BY …) liefert den Wert der
Spalte aus der vorigen Zeile desselben Fensters, in der ersten Zeile
NULL; LEAD(spalte) den aus der nächsten. Jede Rechnung mit NULL ergibt
wieder NULL: dauer_ms - LAG(dauer_ms) OVER (…) ist in der ersten Zeile
NULL, ohne dass man diesen Fall eigens behandeln muss. Damit lassen sich Zeilen mit
ihrem Vorgänger vergleichen, ohne die Tabelle mit sich selbst zu
verknüpfen. Aggregatfunktionen wie SUM und AVG können ebenfalls als
Fensterfunktion laufen. Mit einem Rahmen schaut das Fenster nur auf
einige Zeilen rund um die aktuelle:

    AVG(wert) OVER (ORDER BY tag ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

ist der Durchschnitt über die aktuelle und die zwei vorigen Zeilen, ein
gleitender Durchschnitt. Fensterfunktionen werden nach GROUP BY
berechnet; darum darf in ihnen auch ein Aggregat stehen, etwa
AVG(SUM(dauer_ms)) OVER (ORDER BY build …) in einer Abfrage mit GROUP BY
build.
"""

import duckdb
import pandas as pd


def langsamste_tests(laeufe, build, k):
    """Gibt je Modul die k langsamsten Tests des Builds als (modul, test, dauer_ms, platz) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def veraenderungen(laeufe):
    """Gibt jeden Lauf als (modul, test, build, dauer_ms, differenz zum vorigen Lauf des Tests) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gesamtdauer(laeufe):
    """Gibt je Build (build, summe, gleitender Durchschnitt der Summe über drei Builds) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


laeufe = pd.DataFrame(
    {
        "build": [101, 101, 101, 101, 102, 102, 102, 102, 103, 103],
        "modul": ["login", "login", "login", "suche", "login", "login", "login", "suche", "login", "suche"],
        "test": ["passwort", "sperre", "token", "volltext", "passwort", "sperre", "token", "volltext", "passwort", "volltext"],
        "dauer_ms": [120, 340, 80, 900, 130, 310, 130, 1250, 125, 1100],
    }
)
print(langsamste_tests(laeufe, 102, 2))
print(veraenderungen(laeufe)[:3])
print(gesamtdauer(laeufe))
