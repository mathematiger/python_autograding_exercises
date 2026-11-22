"""Aufgabe 4_057 – Abnahme                                       Stufe 4 ★★★★☆

Ein Softwarehaus liefert einer Stadtverwaltung ein neues
Terminbuchungssystem. Im Lastenheft stehen alle Anforderungen, jede mit
einer Kennung, einer Art und einer Priorität. Funktionale Anforderungen
beschreiben, was das System tut („Termin stornieren“), nicht
funktionale, wie gut es das tut („Seite lädt in unter 2 Sekunden“). Die
Priorität ist "muss", "soll" oder "kann". Vor der Abnahme, der
offiziellen Übergabe an den Kunden, laufen Testfälle; jeder gehört zu
genau einer Anforderung und ist bestanden oder nicht:

    anforderungen                       tests
    id   art               prioritaet   anforderung  testfall  bestanden
    A1   funktional        muss         A1           T1        True
    A2   funktional        soll         A1           T2        True
    A3   nicht funktional  muss         A2           T3        False
    A4   nicht funktional  kann         A2           T4        True
    A5   funktional        kann         A3           T5        False
                                        A5           T6        True
                                        A9           T7        True

Schreiben Sie mit polars drei Funktionen, die beide Tabellen bekommen
und einen neuen DataFrame zurückgeben:

- `status_je_anforderung(anforderungen, tests)`: je Anforderung eine
  Zeile mit den Spalten id, art, prioritaet, tests (Anzahl ihrer
  Testfälle), bestanden (Anzahl der bestandenen) und status: "offen",
  wenn es keinen Testfall gibt, "erfüllt", wenn alle bestanden sind,
  sonst "verfehlt". Sortiert nach id. Testfälle zu Kennungen, die nicht
  im Lastenheft stehen (A9), zählen nicht.
- `abnahmebericht(anforderungen, tests)`: je art eine Zeile mit den
  Spalten art, anzahl (Anforderungen), erfuellt (davon erfüllt) und
  quote (erfuellt / anzahl in Prozent, auf eine Nachkommastelle
  gerundet), sortiert nach art.
- `blockierende(anforderungen, tests)`: die Spalten id und status aller
  Muss-Anforderungen, die nicht erfüllt sind, sortiert nach id. Solange
  es welche gibt, nimmt der Kunde nicht ab.

    status_je_anforderung(anforderungen, tests)["status"].to_list()
        →  ["erfüllt", "verfehlt", "verfehlt", "offen", "erfüllt"]
    abnahmebericht(anforderungen, tests).to_dicts()
        →  [{"art": "funktional", "anzahl": 3, "erfuellt": 2, "quote": 66.7},
            {"art": "nicht funktional", "anzahl": 2, "erfuellt": 0, "quote": 0.0}]
    blockierende(anforderungen, tests).to_dicts()
        →  [{"id": "A3", "status": "verfehlt"}]

Grenzen: anforderungen hat 0 bis 1000 Zeilen, jede id kommt höchstens
einmal vor; art ist "funktional" oder "nicht funktional". tests hat 0
bis 10 000 Zeilen, bestanden ist True oder False. Die Spalten haben
immer die Namen und Typen wie oben, auch bei leeren Tabellen.

Hintergrund: In Aufgabe 4_031 haben Sie mit polars gefiltert und
Spalten berechnet; in Aufgabe 4_041 und 4_045 haben Sie mit pandas
gruppiert und verknüpft. In polars heißt das group_by und join:

    import polars as pl

    je_ort = bestellungen.group_by("ort").agg(
        pl.len().alias("anzahl"),                   # Zeilen je Gruppe
        pl.col("betrag").sum().alias("umsatz"),
        (pl.col("betrag") > 100).sum().alias("gross"),   # True zählt als 1
    )
    mit_ort = kunden.join(je_ort, on="ort", how="left")

group_by(spalte).agg(…) bildet je Wert der Spalte eine Gruppe und
fasst jede Gruppe mit den Ausdrücken in agg zu einer Zeile zusammen.
Die Reihenfolge der Gruppen ist dabei zufällig; darum sortiert man
danach mit sort(spalte) oder schreibt group_by(spalte,
maintain_order=True). join verknüpft zwei Tabellen über einen Schlüssel:
on="spalte", wenn er in beiden gleich heißt, sonst left_on=… und
right_on=…. how="inner" (Standard) behält nur Zeilen mit Partner in
beiden Tabellen, how="left" alle Zeilen der linken; fehlt dort der
Partner, stehen in den neuen Spalten null, die man mit
pl.col("x").fill_null(0) ersetzt. Fallunterscheidungen schreibt man als
Ausdruck mit pl.when:

    pl.when(pl.col("umsatz") > 1000).then(pl.lit("A"))
      .when(pl.col("umsatz") > 100).then(pl.lit("B"))
      .otherwise(pl.lit("C")).alias("klasse")

Die erste zutreffende Bedingung zählt, wie bei if/elif/else.
pl.lit("A") ist ein fester Wert als Ausdruck. Eine Division zweier
Spalten mit / ergibt eine Kommazahl, .round(1) rundet sie.
"""

import polars as pl


def status_je_anforderung(anforderungen, tests):
    """Gibt je Anforderung die Zahl der Tests, der bestandenen und den Status zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def abnahmebericht(anforderungen, tests):
    """Gibt je Art die Zahl der Anforderungen, der erfüllten und die Quote in Prozent zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def blockierende(anforderungen, tests):
    """Gibt id und status der Muss-Anforderungen zurück, die nicht erfüllt sind."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


anforderungen = pl.DataFrame(
    {
        "id": ["A1", "A2", "A3", "A4", "A5"],
        "art": ["funktional", "funktional", "nicht funktional", "nicht funktional", "funktional"],
        "prioritaet": ["muss", "soll", "muss", "kann", "kann"],
    }
)
tests = pl.DataFrame(
    {
        "anforderung": ["A1", "A1", "A2", "A2", "A3", "A5", "A9"],
        "testfall": ["T1", "T2", "T3", "T4", "T5", "T6", "T7"],
        "bestanden": [True, True, False, True, False, True, True],
    }
)
print(status_je_anforderung(anforderungen, tests)["status"].to_list())
print(abnahmebericht(anforderungen, tests).to_dicts())
print(blockierende(anforderungen, tests).to_dicts())
