"""Aufgabe 4_031 – Anmeldeprotokoll                              Stufe 4 ★★★★☆

Der VPN-Zugang einer Firma schreibt für jedes Benutzerkonto und jede
Stunde, in der jemand versucht hat, sich anzumelden, eine Zeile ins
Protokoll: den Benutzernamen, die Stunde (0 bis 23) und die Zahl der
fehlgeschlagenen Anmeldeversuche in dieser Stunde. Viele Fehlversuche
mitten in der Nacht deuten auf einen Angriff hin, bei dem jemand
Passwörter durchprobiert (Brute Force). Das Sicherheitsteam möchte das
Protokoll mit polars auswerten. Vervollständigen Sie drei Funktionen;
jede bekommt einen polars-DataFrame mit den Spalten benutzer, stunde und
fehlversuche:

- `mit_nachtmarke(protokoll)` gibt den DataFrame mit einer zusätzlichen
  letzten Spalte nachts zurück: True, wenn die Stunde vor 6 oder ab 22
  liegt (also 22, 23, 0, 1, …, 5), sonst False. Die übrigen Spalten und
  die Reihenfolge der Zeilen bleiben, wie sie sind.
- `verdaechtig(protokoll, schwelle)` gibt einen DataFrame mit genau den
  Spalten benutzer und fehlversuche (in dieser Reihenfolge) zurück, und
  zwar nur mit den Zeilen, die nachts liegen und mindestens schwelle
  Fehlversuche haben, in der ursprünglichen Reihenfolge.
- `kennzahlen(protokoll)` gibt einen DataFrame mit genau einer Zeile
  und den Spalten summe (alle Fehlversuche zusammen), hoechstwert (der
  größte Wert in fehlversuche) und betroffen (Anzahl der Zeilen mit
  mindestens einem Fehlversuch) zurück.

    protokoll = pl.DataFrame({
        "benutzer": ["anna", "ben", "anna", "cem"],
        "stunde": [3, 10, 23, 5],
        "fehlversuche": [40, 2, 0, 12],
    })
    mit_nachtmarke(protokoll)["nachts"].to_list()  →  [True, False, True, True]
    verdaechtig(protokoll, 10).to_dicts()
        →  [{"benutzer": "anna", "fehlversuche": 40},
            {"benutzer": "cem", "fehlversuche": 12}]
    kennzahlen(protokoll).to_dicts()
        →  [{"summe": 54, "hoechstwert": 40, "betroffen": 3}]

Benutzen Sie die Ausdrücke von polars (pl.col …), keine Schleife über
die Zeilen.

Grenzen: Das Protokoll hat 0 bis 100 000 Zeilen. benutzer ist ein nicht
leerer Text, stunde eine ganze Zahl von 0 bis 23, fehlversuche eine
ganze Zahl von 0 bis 10 000 (Spaltentypen String, Int64, Int64). schwelle
ist eine ganze Zahl von 0 bis 10 000. Bei einem leeren Protokoll ist
summe 0, betroffen 0 und hoechstwert None (es gibt keinen größten
Wert), so wie polars es von selbst liefert. Der übergebene DataFrame
darf nicht verändert werden.

Hintergrund: polars ist eine Bibliothek für Tabellen, ähnlich wie pandas
(Aufgabe 3_038) (Aufgabe 3_013 zeigt die verwandte Idee „rechnen ohne
Schleife“ mit numpy). Eine Tabelle heißt DataFrame und besteht aus Spalten
mit festem Typ. Man baut sie zum Beispiel aus einem Dictionary von Listen:

    import polars as pl

    df = pl.DataFrame({"name": ["a", "b", "c"], "preis": [5, 120, 80]})

Das Besondere an polars sind Ausdrücke: pl.col("preis") rechnet nicht
sofort, sondern beschreibt „die Spalte preis“. Mit Operatoren und
Methoden baut man daraus größere Beschreibungen, etwa pl.col("preis") *
2, pl.col("preis") > 100 oder pl.col("preis").sum(). Bedingungen
verknüpft man mit & (und), | (oder) und ~ (nicht), nicht mit and/or/not,
und setzt jede Bedingung in Klammern, weil & und | stärker binden als <:

    (pl.col("preis") > 10) & (pl.col("preis") < 100)

Ein Ausdruck wird erst in einer der drei Grundmethoden ausgewertet. Jede
gibt einen neuen DataFrame zurück und lässt den alten unverändert:

    df.filter(pl.col("preis") > 50)                 # nur Zeilen, für die der Ausdruck True ist
    df.with_columns((pl.col("preis") * 1.19).alias("brutto"))   # Spalte hinzufügen
    df.select("name", "preis")                       # nur diese Spalten, in dieser Reihenfolge
    df.select(pl.col("preis").max().alias("teuerste"))           # Ausdruck als Ergebnis

with_columns hängt eine Spalte an oder ersetzt eine gleichnamige;
.alias("name") gibt dem Ergebnis eines Ausdrucks seinen Spaltennamen
(ohne alias hieße es wie die Ausgangsspalte). select mit Ausdrücken
wie .sum() oder .max() fasst eine Spalte zu einem Wert zusammen, das
Ergebnis ist ein DataFrame mit einer Zeile. Eine Spalte aus True und
False lässt sich ebenfalls summieren: True zählt als 1. Die Methoden
lassen sich verketten, df.filter(...).select(...), und weil sie den
alten DataFrame nicht ändern, muss man das Ergebnis zurückgeben oder
einer Variablen zuweisen.

Zum Ansehen der Ergebnisse: df["preis"].to_list() liefert eine Spalte als
Liste, df.to_dicts() alle Zeilen als Liste von Dictionaries, df.columns
die Spaltennamen.

Tipp: Die Funktion verdaechtig kann mit_nachtmarke benutzen und danach
filtern und auswählen.
"""

import polars as pl


def mit_nachtmarke(protokoll):
    """Gibt das Protokoll mit der zusätzlichen Spalte nachts (True vor 6 und ab 22 Uhr) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def verdaechtig(protokoll, schwelle):
    """Gibt benutzer und fehlversuche der nächtlichen Zeilen mit mindestens schwelle Fehlversuchen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kennzahlen(protokoll):
    """Gibt einen DataFrame mit einer Zeile und den Spalten summe, hoechstwert und betroffen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokoll = pl.DataFrame({
    "benutzer": ["anna", "ben", "anna", "cem"],
    "stunde": [3, 10, 23, 5],
    "fehlversuche": [40, 2, 0, 12],
})
print(verdaechtig(protokoll, 10).to_dicts())
