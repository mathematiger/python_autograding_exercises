"""Aufgabe 4_031 – Anmeldeversuche                               Stufe 4 ★★★★☆

Das Sicherheitsteam eines Unternehmens wertet jeden Morgen aus, wie
oft sich die Konten am Vortag angemeldet haben. Viele fehlgeschlagene
Anmeldungen können bedeuten, dass jemand Passwörter durchprobiert
(ein Brute-Force-Angriff). Die Zahlen liegen als polars-DataFrame vor,
eine Zeile je Konto:

    benutzer   fehlversuche  erfolge  admin
    "abauer"              1        4  False
    "root"                9        1  True
    "ckaya"               6        2  False
    "dlang"               3        0  True
    "emeyer"              7        8  False

Vervollständigen Sie drei Funktionen, die je einen neuen DataFrame
bzw. eine Liste zurückgeben:

- `auffaellige(konten, grenze)`: nur die Zeilen mit mindestens grenze
  Fehlversuchen und davon nur die Spalten benutzer und fehlversuche,
  in der ursprünglichen Reihenfolge der Zeilen.
- `mit_quote(konten)`: alle Spalten und dahinter eine neue Spalte
  quote mit dem Anteil der Fehlversuche an allen Versuchen,
  fehlversuche / (fehlversuche + erfolge), als Kommazahl.
- `zu_sperren(konten)`: die Namen der Konten, die vorsorglich gesperrt
  werden, als Liste in alphabetischer Reihenfolge. Gesperrt wird, wenn
  die quote über 0.5 liegt und es mindestens 5 Fehlversuche gab, oder
  wenn es ein Admin-Konto mit mindestens 3 Fehlversuchen ist. Benutzen
  Sie dafür mit_quote.

    auffaellige(konten, 6)["benutzer"].to_list()   →  ["root", "ckaya", "emeyer"]
    mit_quote(konten)["quote"].to_list()           →  [0.2, 0.9, 0.75, 1.0, 0.4666…]
    zu_sperren(konten)                             →  ["ckaya", "dlang", "root"]

Arbeiten Sie mit Ausdrücken von polars (select, filter, with_columns,
pl.col), nicht mit einer Schleife über die Zeilen.

Grenzen: Der DataFrame hat 0 bis 100 000 Zeilen und immer die Spalten
benutzer (Text, ohne Wiederholung), fehlversuche und erfolge (ganze
Zahlen von 0 bis 10**6, in jeder Zeile zusammen mindestens 1) und
admin (True oder False). grenze ist eine ganze Zahl von 0 bis 10**6.

Hintergrund: polars ist eine Bibliothek für Tabellen, ähnlich wie
pandas, aber in Rust geschrieben und auf viele Prozessorkerne
ausgelegt. Ein DataFrame ist eine Tabelle mit benannten Spalten, in
der jede Spalte einen festen Datentyp hat. Man erzeugt ihn zum Beispiel
aus einer Liste von Dictionaries, wie in Aufgabe 2_032:

    import polars as pl
    df = pl.DataFrame([{"name": "a", "wert": 3}, {"name": "b", "wert": 8}])

Das Besondere an polars sind Ausdrücke. pl.col("wert") steht für „die
Spalte wert“, noch ohne konkrete Daten. Mit Ausdrücken kann man
rechnen und vergleichen wie mit Zahlen; das Ergebnis ist wieder ein
Ausdruck, der für jede Zeile gilt (wie bei den Arrays von numpy,
Aufgabe 3_013): pl.col("wert") * 2, pl.col("wert") > 5. Erst eine
Methode des DataFrames wendet sie auf die Daten an:

    df.select("name", "wert")                 # nur diese Spalten
    df.filter(pl.col("wert") > 5)             # nur die Zeilen, für die es wahr ist
    df.with_columns((pl.col("wert") * 2).alias("doppelt"))   # neue Spalte
    df.sort("name")                           # Zeilen ordnen
    df["name"].to_list()                      # eine Spalte als Python-Liste

alias gibt einer berechneten Spalte ihren Namen. Bedingungen verknüpft
man mit & (und), | (oder) und ~ (nicht), nicht mit and und or, weil
die für einzelne Wahrheitswerte gedacht sind. Weil & und | stärker
binden als > und ==, gehört jeder Vergleich in Klammern:

    df.filter((pl.col("wert") > 2) & (pl.col("name") != "b"))

Alle Methoden geben einen neuen DataFrame zurück und lassen den alten
unverändert; deshalb kann man sie hintereinanderschreiben:
df.filter(…).select(…). Weil polars die Ausdrücke selbst ausführt,
statt Python Zeile für Zeile rechnen zu lassen, ist das auch bei
Millionen Zeilen schnell.
"""

import polars as pl


def auffaellige(konten, grenze):
    """Gibt benutzer und fehlversuche der Konten mit mindestens grenze Fehlversuchen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def mit_quote(konten):
    """Gibt die Tabelle mit der zusätzlichen Spalte quote zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zu_sperren(konten):
    """Gibt die Namen der Konten, die gesperrt werden, alphabetisch geordnet zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


konten = pl.DataFrame(
    [
        {"benutzer": "abauer", "fehlversuche": 1, "erfolge": 4, "admin": False},
        {"benutzer": "root", "fehlversuche": 9, "erfolge": 1, "admin": True},
        {"benutzer": "ckaya", "fehlversuche": 6, "erfolge": 2, "admin": False},
        {"benutzer": "dlang", "fehlversuche": 3, "erfolge": 0, "admin": True},
        {"benutzer": "emeyer", "fehlversuche": 7, "erfolge": 8, "admin": False},
    ]
)
print(auffaellige(konten, 6)["benutzer"].to_list())
print(zu_sperren(konten))
