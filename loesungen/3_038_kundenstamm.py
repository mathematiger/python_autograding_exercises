# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_038_kundenstamm.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_038_kundenstamm

"""Aufgabe 3_038 – Kundenstamm                                   Stufe 3 ★★★☆☆

Eine Firma führt ihre Kundendaten bisher als Liste von Dictionaries, so
wie sie aus der Schnittstelle des alten Systems kommen: ein Dictionary je
Kunde mit den Schlüsseln "kundennummer", "name", "ort", "email" und
"telefon". Für die Auswertungen der nächsten Wochen sollen die Daten in
eine Tabelle der Bibliothek pandas umziehen. Schreiben Sie drei kleine
Funktionen:

- `als_tabelle(datensaetze)` gibt einen DataFrame zurück, der für jeden
  Datensatz eine Zeile und für jeden Schlüssel eine Spalte hat, in der
  Reihenfolge der Datensätze.
- `adressliste(tabelle)` gibt einen neuen DataFrame zurück, der nur die
  Spalten "name" und "ort" enthält, in dieser Reihenfolge. Die
  übergebene Tabelle bleibt unverändert.
- `emails(tabelle)` gibt alle E-Mail-Adressen als gewöhnliche Python-Liste
  zurück, in der Reihenfolge der Zeilen.

    kunden = [
        {"kundennummer": 1001, "name": "Weber GmbH", "ort": "Kassel",
         "email": "info@weber.example", "telefon": "0561 1234"},
        {"kundennummer": 1002, "name": "Lindner KG", "ort": "Fulda",
         "email": "post@lindner.example", "telefon": "0661 9876"},
    ]
    tabelle = als_tabelle(kunden)
    list(tabelle.columns)  →  ["kundennummer", "name", "ort", "email", "telefon"]
    adressliste(tabelle)   →  DataFrame mit den Spalten name und ort
    emails(tabelle)        →  ["info@weber.example", "post@lindner.example"]

Grenzen: 1 ≤ len(datensaetze) ≤ 5000. Alle Datensätze haben genau die
fünf Schlüssel oben, in derselben Reihenfolge; kundennummer ist eine
ganze Zahl, alle anderen Werte sind Texte. Namen und E-Mail-Adressen
dürfen mehrfach vorkommen.

Hintergrund: In Aufgabe 2_032 war eine Tabelle eine Liste von
Dictionaries: eine Zeile je Dictionary, eine Spalte je Schlüssel. Die
Bibliothek pandas hat dafür einen eigenen Typ, den DataFrame. Er
entsteht direkt aus so einer Liste:

    import pandas as pd

    zeilen = [{"host": "web1", "cpu": 35}, {"host": "db1", "cpu": 80}]
    df = pd.DataFrame(zeilen)
    list(df.columns)    →  ["host", "cpu"]
    len(df)             →  2  (Zahl der Zeilen)

Eine einzelne Spalte holt man mit eckigen Klammern und ihrem Namen
heraus: df["cpu"] ist eine Series, eine Spalte mit Werten. Steht in den
Klammern eine Liste von Namen, kommt ein neuer DataFrame mit genau
diesen Spalten in dieser Reihenfolge heraus (darum die doppelten
Klammern):

    df[["cpu", "host"]]  →  DataFrame mit den Spalten cpu und host

Dabei bleibt df selbst, wie es war. Eine Series ist keine Liste; mit
df["cpu"].tolist() wird daraus eine gewöhnliche Liste [35, 80].
"""

import pandas as pd


def als_tabelle(datensaetze):
    """Gibt die Datensätze als DataFrame zurück, eine Zeile je Datensatz."""
    return pd.DataFrame(datensaetze)


def adressliste(tabelle):
    """Gibt einen neuen DataFrame mit den Spalten name und ort zurück."""
    return tabelle[["name", "ort"]]


def emails(tabelle):
    """Gibt die E-Mail-Adressen als Liste zurück."""
    return tabelle["email"].tolist()


kunden = [
    {"kundennummer": 1001, "name": "Weber GmbH", "ort": "Kassel", "email": "info@weber.example", "telefon": "0561 1234"},
    {"kundennummer": 1002, "name": "Lindner KG", "ort": "Fulda", "email": "post@lindner.example", "telefon": "0661 9876"},
]
tabelle = als_tabelle(kunden)
print(list(tabelle.columns))
print(emails(tabelle))


# Idee: pd.DataFrame(datensaetze) macht aus der Liste von Dictionaries direkt eine Tabelle, die Schlüssel
# werden die Spalten. tabelle[["name", "ort"]] wählt mit einer Liste von Spaltennamen einen neuen
# DataFrame aus und lässt die alte Tabelle stehen. tabelle["email"] ist eine einzelne Spalte (Series),
# .tolist() macht daraus eine Python-Liste.
# Anderer Weg: pd.DataFrame.from_records(datensaetze) baut dieselbe Tabelle. Statt tolist() geht
# list(tabelle["email"]); für adressliste geht auch tabelle.loc[:, ["name", "ort"]] oder
# tabelle.drop(columns=["kundennummer", "email", "telefon"]).
# Typische Fehler: tabelle["name", "ort"] mit einfachen Klammern (KeyError, pandas sucht eine Spalte
# mit dem Namen ("name", "ort")), Spalten mit del tabelle["email"] aus der übergebenen Tabelle löschen
# (dann fehlen sie danach überall) oder die Series zurückgeben statt einer Liste.
# Laufzeit: Alle drei Funktionen brauchen O(n) für n Zeilen; die Arbeit erledigt pandas in C, ohne
# Python-Schleife.
