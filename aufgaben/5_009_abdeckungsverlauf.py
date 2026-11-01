"""Aufgabe 5_009 – Abdeckungsverlauf                               Stufe 5 ★★★★★

Ein Team entwickelt eine größere Software aus mehreren Modulen. Bei
jedem Build, also jedem automatischen Übersetzen und Testen nach einer
Änderung, misst der Buildserver die Testabdeckung jedes Moduls: wie viel
Prozent der Codezeilen die automatischen Tests ausführen. Die Messwerte
liegen als pandas-DataFrame mit den Spalten modul (Text), build (ganze
Zahl, je Modul aufsteigend vergeben) und abdeckung (ganze Zahl in
Prozent) vor, ungeordnet. Die Qualitätssicherung will drei Auswertungen,
alle in SQL mit DuckDB:

- `gleitender_schnitt(builds)`: Zu jeder Zeile den Durchschnitt der
  Abdeckung dieses Builds und der bis zu zwei vorangehenden Builds
  desselben Moduls (beim ersten Build eines Moduls nur er selbst, beim
  zweiten die ersten beiden). Ergebnis: Liste von Tupeln
  (modul, build, schnitt), sortiert nach modul und build; schnitt ist
  eine Kommazahl, nicht gerundet.
- `rueckschritte(builds)`: Alle Builds, deren Abdeckung kleiner ist als
  beim vorangehenden Build desselben Moduls. Ergebnis: Liste von Tupeln
  (modul, build, vorher, jetzt), sortiert nach modul und build.
- `neuester_stand(builds)`: Zu jedem Modul der Build mit der größten
  Nummer. Ergebnis: Liste von Tupeln (modul, build, abdeckung), sortiert
  nach modul.

    builds = pd.DataFrame({
        "modul":     ["api", "api", "ui", "api", "ui", "api"],
        "build":     [1, 2, 1, 3, 4, 7],
        "abdeckung": [60, 70, 40, 65, 45, 80],
    })
    gleitender_schnitt(builds)
        →  [("api", 1, 60.0), ("api", 2, 65.0), ("api", 3, 65.0),
            ("api", 7, 71.666…), ("ui", 1, 40.0), ("ui", 4, 42.5)]
    rueckschritte(builds)   →  [("api", 3, 70, 65)]
    neuester_stand(builds)  →  [("api", 7, 80), ("ui", 4, 45)]

„Vorangehend“ heißt: mit der nächstkleineren Buildnummer desselben
Moduls; Lücken in den Nummern zählen nicht.

Grenzen: builds hat 0 bis 100 000 Zeilen. modul besteht aus 1 bis 20
Kleinbuchstaben, Ziffern und _, build ist eine ganze Zahl von 1 bis
10**6 und innerhalb eines Moduls eindeutig, abdeckung eine ganze Zahl von
0 bis 100. Die Zahl der ausgeführten Python-Zeilen soll nicht mit der
Zahl der Zeilen wachsen; die Arbeit macht DuckDB.

Hintergrund: GROUP BY fasst die Zeilen einer Gruppe zu einer einzigen
Ergebniszeile zusammen. Oft will man aber jede Zeile behalten und ihr
etwas aus ihrer Umgebung dazuschreiben: den Wert der vorigen Zeile, einen
laufenden Durchschnitt, ihren Rang. Das leisten Fensterfunktionen. Hinter
der Funktion steht OVER mit der Beschreibung des Fensters:

    SELECT modul, build,
           AVG(abdeckung) OVER (PARTITION BY modul ORDER BY build
                                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS schnitt
    FROM builds

PARTITION BY modul teilt die Zeilen in Gruppen wie GROUP BY, aber ohne sie
zusammenzufassen: Jede Zeile sieht nur ihre eigene Gruppe. ORDER BY build
ordnet die Zeilen innerhalb der Gruppe. Der Rahmen ROWS BETWEEN 2
PRECEDING AND CURRENT ROW sagt, welche Zeilen in die Rechnung eingehen:
die aktuelle und bis zu zwei davor. Ohne Rahmenangabe nimmt eine
Aggregatfunktion mit ORDER BY alles vom Anfang der Gruppe bis zur
aktuellen Zeile, also eine laufende Summe oder einen laufenden
Durchschnitt.

Einige Funktionen gibt es nur als Fensterfunktion:

    LAG(abdeckung) OVER (PARTITION BY modul ORDER BY build)    Wert der vorigen Zeile, NULL bei der ersten
    LEAD(abdeckung) OVER (…)                                  Wert der nächsten Zeile
    ROW_NUMBER() OVER (PARTITION BY modul ORDER BY build DESC) 1, 2, 3 … je Gruppe
    RANK() OVER (ORDER BY abdeckung DESC)                      Rang, Gleichstand teilt sich den Rang

Fensterfunktionen werden nach WHERE berechnet; darum kann man in WHERE
nicht nach ihnen filtern. Entweder rechnet man sie in einer Unterabfrage
(oder mit WITH name AS (…)) aus und filtert außen, oder man benutzt
DuckDBs QUALIFY, das nach den Fensterfunktionen filtert:

    SELECT modul, build FROM builds
    QUALIFY ROW_NUMBER() OVER (PARTITION BY modul ORDER BY build DESC) = 1

Einen DataFrame macht man DuckDB so bekannt; die Hilfsfunktion abfrage im
Code tut genau das, Sie müssen ihr nur noch die SQL-Abfrage geben:

    verbindung = duckdb.connect()
    verbindung.register("builds", builds)
    zeilen = verbindung.execute("SELECT … FROM builds ORDER BY modul").fetchall()

fetchall() liefert eine Liste von Tupeln mit gewöhnlichen Python-Werten.
Eine Reihenfolge gibt es in SQL nur mit ORDER BY; ohne sie darf DuckDB
die Zeilen in beliebiger Reihenfolge liefern.
"""

import duckdb
import pandas as pd


# Eine Verbindung für alle Abfragen: duckdb.connect() kostet bei jedem Aufruf einige Millisekunden.
VERBINDUNG = duckdb.connect()


def abfrage(builds, sql):
    """Führt sql mit dem DataFrame builds als Tabelle builds aus und gibt alle Zeilen als Tupel zurück."""
    VERBINDUNG.register("builds", builds)
    return VERBINDUNG.execute(sql).fetchall()


def gleitender_schnitt(builds):
    """Gibt (modul, build, schnitt) mit dem Schnitt über diesen und bis zu zwei vorige Builds zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def rueckschritte(builds):
    """Gibt (modul, build, vorher, jetzt) für alle Builds mit gesunkener Abdeckung zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def neuester_stand(builds):
    """Gibt zu jedem Modul (modul, build, abdeckung) seines neuesten Builds zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


builds = pd.DataFrame(
    {
        "modul": ["api", "api", "ui", "api", "ui", "api"],
        "build": [1, 2, 1, 3, 4, 7],
        "abdeckung": [60, 70, 40, 65, 45, 80],
    }
)
print([(modul, build, round(schnitt, 2)) for modul, build, schnitt in gleitender_schnitt(builds)])
print(rueckschritte(builds))
print(neuester_stand(builds))
