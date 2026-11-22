"""Aufgabe 4_045 – Störungscodes                                 Stufe 4 ★★★★☆

Das Monitoring eines Rechenzentrums meldet jede Störung mit einer
laufenden Nummer, dem betroffenen Host und einem kurzen Code wie
"DSK01" oder "NET07". Was ein Code bedeutet, steht in einem eigenen
Katalog: die Ursache ("Hardware", "Netz", "Software", …) und die
Schwere von 1 (gering) bis 3 (kritisch). Für die monatliche
Fehleranalyse sollen beide Tabellen über den Code verknüpft werden.
Schreiben Sie mit merge drei Funktionen:

- `mit_ursache(stoerungen, katalog)` gibt einen DataFrame mit den
  Spalten id, host, code, ursache und schwere zurück: eine Zeile für
  jede Störung, deren Code im Katalog steht, in der Reihenfolge der
  Störungen.
- `ohne_eintrag(stoerungen, katalog)` gibt die Codes, die in den
  Störungen vorkommen, aber nicht im Katalog, als alphabetisch
  sortierte Liste ohne Doppelte zurück. Diese Codes muss jemand im
  Katalog nachtragen.
- `je_ursache(stoerungen, katalog)` gibt ein Dictionary zurück, das
  jeder Ursache die Zahl ihrer Störungen zuordnet. Störungen, deren
  Code nicht im Katalog steht, zählen unter "unbekannt". Ursachen ohne
  Störung kommen nicht vor.

Die übergebenen Tabellen bleiben unverändert.

    stoerungen = pd.DataFrame([
        {"id": 1, "host": "web01", "code": "NET07"},
        {"id": 2, "host": "db02", "code": "DSK01"},
        {"id": 3, "host": "web01", "code": "APP99"},
        {"id": 4, "host": "web02", "code": "NET07"},
    ])
    katalog = pd.DataFrame([
        {"code": "DSK01", "ursache": "Hardware", "schwere": 3},
        {"code": "NET07", "ursache": "Netz", "schwere": 2},
        {"code": "MEM02", "ursache": "Hardware", "schwere": 2},
    ])
    mit_ursache(stoerungen, katalog)["ursache"].tolist()
        →  ["Netz", "Hardware", "Netz"]
    ohne_eintrag(stoerungen, katalog)  →  ["APP99"]
    je_ursache(stoerungen, katalog)    →  {"Hardware": 1, "Netz": 2, "unbekannt": 1}

Grenzen: stoerungen hat 0 bis 50 000 Zeilen mit genau den Spalten id
(eindeutige ganze Zahl), host und code (nicht leere Texte). katalog hat
0 bis 1000 Zeilen mit genau den Spalten code, ursache und schwere; jeder
Code steht dort höchstens einmal, ursache ist ein nicht leerer Text
außer "unbekannt", schwere eine ganze Zahl von 1 bis 3. Beide Tabellen
können leer sein.

Hintergrund: In Aufgabe 4_041 wurden Zeilen einer Tabelle gruppiert.
Oft stehen die Angaben, die man braucht, aber in zwei Tabellen, die
über einen gemeinsamen Schlüssel zusammenhängen, wie Kundennummer oder
Code. merge verknüpft sie wie ein JOIN in SQL: Zu jeder Zeile links
sucht es die Zeilen rechts mit demselben Schlüssel und hängt deren
Spalten an.

    messungen.merge(geraete, on="seriennr")

Das Argument how bestimmt, was mit Zeilen ohne Partner passiert:

    how="inner"   nur Zeilen, deren Schlüssel in beiden Tabellen steht
                  (Standard; die Reihenfolge der linken Tabelle bleibt)
    how="left"    alle Zeilen der linken Tabelle; fehlt der Partner,
                  stehen in den neuen Spalten fehlende Werte (NaN)
    how="outer"   alle Zeilen beider Tabellen

Mit indicator=True kommt eine Spalte _merge dazu, die für jede Zeile
"both", "left_only" oder "right_only" enthält; damit findet man Zeilen
ohne Partner mit einer Maske (Aufgabe 3_041):

    alle = links.merge(rechts, on="nr", how="left", indicator=True)
    alle[alle["_merge"] == "left_only"]

Fehlende Werte ersetzt man mit fillna: spalte.fillna("leer") gibt eine
neue Spalte zurück, in der jedes NaN durch "leer" ersetzt ist. Eine
Ganzzahlspalte mit NaN wird übrigens zu Kommazahlen, weil NaN selbst
eine Kommazahl ist. Achtung: Steht ein Schlüssel rechts mehrfach,
bekommt jede passende linke Zeile mehrere Partner und kommt mehrfach
vor. Hier ist das ausgeschlossen, weil jeder Code nur einmal im
Katalog steht.

Tipp: unique() liefert die verschiedenen Werte einer Spalte,
sorted(...) macht daraus eine sortierte Liste; value_counts() zählt,
wie oft jeder Wert in einer Spalte vorkommt.
"""

import pandas as pd


def mit_ursache(stoerungen, katalog):
    """Gibt die Störungen mit Ursache und Schwere zurück, nur Codes aus dem Katalog."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ohne_eintrag(stoerungen, katalog):
    """Gibt die Codes ohne Katalogeintrag sortiert und ohne Doppelte zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def je_ursache(stoerungen, katalog):
    """Gibt die Zahl der Störungen je Ursache zurück, fehlende Codes als "unbekannt"."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


stoerungen = pd.DataFrame(
    [
        {"id": 1, "host": "web01", "code": "NET07"},
        {"id": 2, "host": "db02", "code": "DSK01"},
        {"id": 3, "host": "web01", "code": "APP99"},
        {"id": 4, "host": "web02", "code": "NET07"},
    ]
)
katalog = pd.DataFrame(
    [
        {"code": "DSK01", "ursache": "Hardware", "schwere": 3},
        {"code": "NET07", "ursache": "Netz", "schwere": 2},
        {"code": "MEM02", "ursache": "Hardware", "schwere": 2},
    ]
)
print(mit_ursache(stoerungen, katalog)["ursache"].tolist())
print(ohne_eintrag(stoerungen, katalog))
print(sorted(je_ursache(stoerungen, katalog).items()))
