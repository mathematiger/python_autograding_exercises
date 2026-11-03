"""Aufgabe 5_012 – Kundenimport                                   Stufe 5 ★★★★★

Ein Versandhändler stellt sein Warenwirtschaftssystem um. Die
Kundendaten kommen als CSV-Export aus dem alten System, mit typischen
Mängeln: Manche Kunden haben keine E-Mail-Adresse, manche Adressen
haben Großbuchstaben oder Leerzeichen am Rand, und manche Kunden wurden
früher doppelt angelegt, mit derselben E-Mail-Adresse unter zwei
Kundennummern.

    kunden_nr,name,email,ort
    1001,Ada Berg, Ada.Berg@Example.org ,Bonn
    1002,Bo Lang,,Jena
    1003,Cem Koch,cem@example.org,Bonn
    1004,Ada Berg,ada.berg@example.org,Bonn

Der Export ist im echten Betrieb mehrere Gigabyte groß. Deshalb soll
die Bereinigung mit polars im Lazy-Modus laufen: Die Funktionen
beschreiben nur, was zu tun ist, und erst ganz am Ende wird einmal
gerechnet. Vervollständigen Sie drei Funktionen:

- `lade(csv_text)` gibt einen LazyFrame zurück, der den CSV-Text mit
  pl.scan_csv liest (den Text vorher mit io.BytesIO(csv_text.encode())
  in ein Datei-Objekt verpacken). Die Funktion liest dabei noch nichts.
- `bereinigt(kunden)` bekommt einen LazyFrame mit den Spalten kunden_nr,
  name, email und ort und gibt einen LazyFrame zurück, in dem
  1. die Zeilen ohne E-Mail-Adresse fehlen (leeres Feld, also null),
  2. die E-Mail-Adressen ohne Leerzeichen am Rand und in
     Kleinbuchstaben stehen,
  3. von mehreren Zeilen mit derselben (bereinigten) Adresse nur die
     mit der kleinsten Kundennummer übrig ist,
  4. die Zeilen nach kunden_nr aufsteigend sortiert sind.
  Die Funktion darf nicht collect() aufrufen.
- `kunden_je_ort(kunden)` bekommt einen LazyFrame wie bereinigt und gibt
  eine Liste von Tupeln (ort, anzahl) zurück: wie viele bereinigte
  Kunden es je Ort gibt, nach anzahl absteigend, bei gleicher Anzahl
  nach ort aufsteigend. Sie benutzt bereinigt und ruft genau einmal
  collect() auf.

    kunden = lade(csv_text)
    bereinigt(kunden).collect()["email"].to_list()
        →  ["ada.berg@example.org", "cem@example.org"]
    bereinigt(kunden).collect()["kunden_nr"].to_list()
        →  [1001, 1003]
    kunden_je_ort(kunden)
        →  [("Bonn", 2)]

Grenzen: Der LazyFrame hat 0 bis 100 000 Zeilen. kunden_nr sind ganze
Zahlen von 1 bis 10**9 ohne Wiederholung, name und ort nicht leere
Texte, email ein Text mit 1 bis 100 Zeichen oder null. Die Zeilen sind
nicht sortiert. Der CSV-Text in lade hat immer die Kopfzeile
kunden_nr,name,email,ort.

Hintergrund: polars ist eine Bibliothek für Tabellen wie pandas, aber
mit einer eigenen Sprache aus Ausdrücken: pl.col("preis") steht für eine
Spalte, und Methoden darauf beschreiben, was mit ihr geschehen soll.

    df.filter(pl.col("preis") > 100)                         # Zeilen auswählen
    df.with_columns(pl.col("name").str.to_uppercase())       # Spalte ersetzen
    df.group_by("ort").agg(pl.len().alias("anzahl"))         # gruppieren und zählen
    df.sort(["anzahl", "ort"], descending=[True, False])     # nach zwei Spalten sortieren
    df.unique(subset="email", keep="first", maintain_order=True)   # Dubletten entfernen

with_columns ersetzt eine Spalte, wenn der Ausdruck denselben Namen hat
(hier "name"), sonst kommt eine neue hinzu. .is_not_null() ist wahr für
Zeilen mit Wert, .str.strip_chars() entfernt Leerzeichen am Rand.
unique mit keep="first" behält von gleichen Werten die erste Zeile,
maintain_order=True die Reihenfolge; die erste Zeile ist also nur dann
die mit der kleinsten Nummer, wenn man vorher sortiert hat.

Ein DataFrame (pl.DataFrame) rechnet jede dieser Zeilen sofort aus.
Ein LazyFrame (pl.LazyFrame) kennt dieselben Methoden, rechnet aber
nichts aus: Jede Methode liefert einen neuen LazyFrame, der sich nur
merkt, was zu tun ist, einen Abfrageplan. Erst .collect() führt den Plan
aus und liefert einen DataFrame. pl.scan_csv(quelle) ist die Lazy-Form
von pl.read_csv; df.lazy() macht aus einem DataFrame einen LazyFrame.

    plan = pl.scan_csv(quelle).filter(pl.col("ort") == "Bonn").select("name")
    print(plan.explain())     # zeigt den Plan, noch ohne zu rechnen
    ergebnis = plan.collect()

Der Vorteil: Bevor polars rechnet, sieht es den ganzen Plan und
optimiert ihn. explain() zeigt das: Beim Lesen der Datei steht dort zum
Beispiel PROJECT 2/4 COLUMNS und SELECTION: col("ort") == "Bonn", das
heißt, polars liest nur die zwei nötigen Spalten und filtert schon beim
Lesen (Projection und Predicate Pushdown), statt erst alles in den
Speicher zu holen. Jedes collect() führt den Plan komplett neu aus; wer
zwischendurch collect() aufruft, verschenkt die Optimierung und liest
die Daten mehrmals. Nach collect() sind Tabellen gewöhnliche DataFrames:
df["spalte"].to_list() gibt eine Spalte als Liste, df.rows() alle
Zeilen als Liste von Tupeln.
"""

import io

import polars as pl


def lade(csv_text):
    """Gibt einen LazyFrame zurück, der den CSV-Text liest."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bereinigt(kunden):
    """Gibt einen LazyFrame ohne fehlende E-Mails, mit bereinigten Adressen und ohne Dubletten zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kunden_je_ort(kunden):
    """Gibt (ort, anzahl) der bereinigten Kunden zurück, die meisten zuerst."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


csv_text = """kunden_nr,name,email,ort
1001,Ada Berg, Ada.Berg@Example.org ,Bonn
1002,Bo Lang,,Jena
1003,Cem Koch,cem@example.org,Bonn
1004,Ada Berg,ada.berg@example.org,Bonn
"""
kunden = lade(csv_text)
print(bereinigt(kunden).collect()["email"].to_list())
print(bereinigt(kunden).collect()["kunden_nr"].to_list())
print(kunden_je_ort(kunden))
