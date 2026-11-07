"""Aufgabe 5_018 – Löschfristen                                  Stufe 5 ★★★★★

Ein Onlinehändler speichert personenbezogene Daten: Bewerbungen,
Rechnungen, Newsletter-Anmeldungen und mehr. Nach der
Datenschutz-Grundverordnung dürfen solche Daten nur so lange gespeichert
werden, wie es einen Grund dafür gibt; für jede Kategorie legt das
Unternehmen deshalb eine Löschfrist in Tagen fest (für Rechnungen gilt
zum Beispiel eine gesetzliche Aufbewahrungspflicht von zehn Jahren).
Die Datenschutzbeauftragte möchte zu einem Stichtag wissen, welche
Datensätze gelöscht werden müssen. Der Export aus der Datenbank ist
allerdings unsauber: Kategorien mit Leerzeichen und in gemischter
Schreibweise, ungültige Datumsangaben und doppelte Datensätze.
Schreiben Sie die Auswertung mit pandas in fünf Funktionen. Die
übergebenen DataFrames bleiben jeweils unverändert.

- `bereinige(roh)` bekommt die Tabelle aus lade(ROHDATEN) mit den
  Spalten id, kategorie, erstellt und kunde (alle außer id als Text) und
  gibt eine neue Tabelle mit denselben Spalten und dem Index 0, 1, 2, …
  zurück: kategorie ohne Leerzeichen am Rand und in Kleinbuchstaben,
  erstellt als Datum (datetime64). Zeilen, deren erstellt kein gültiges
  Datum der Form JJJJ-MM-TT ist, fallen weg. Danach bleibt von
  mehreren Zeilen mit derselben id nur die erste.
- `loeschtermine(daten, fristen)` verknüpft die bereinigten Daten über
  kategorie mit der Tabelle fristen (Spalten kategorie und frist_tage)
  und ergänzt die Spalte loeschen_ab = erstellt + frist_tage Tage.
  Datensätze, deren Kategorie keine Frist hat, fallen weg.
- `faellige(daten, fristen, stichtag)` gibt die Datensätze mit
  loeschen_ab <= stichtag zurück, mit den Spalten id, kategorie und
  loeschen_ab, sortiert nach loeschen_ab, bei Gleichstand nach id.
- `ohne_frist(daten, fristen)` gibt die sortierte Liste der ids zurück,
  deren Kategorie keine Löschfrist hat. Diese Fälle muss jemand klären,
  denn ohne Frist würden die Daten nie gelöscht.
- `bericht(daten, fristen, stichtag)` gibt je Kategorie mit Frist und
  mindestens einem Datensatz eine Zeile mit den Spalten kategorie,
  datensaetze (Anzahl) und faellig (davon fällig) zurück, sortiert nach
  faellig absteigend, bei Gleichstand nach kategorie.

Bei faellige und bericht ist der Index egal. Mit den Daten im Code und
dem Stichtag 2025-01-01:

    daten = bereinige(lade(ROHDATEN))
    daten["id"].tolist()                       →  [1, 2, 4, 5, 6]
    daten["kategorie"].tolist()                →  ["bewerbung", "rechnung", "newsletter",
                                                   "chatprotokoll", "bewerbung"]
    faellige(daten, fristen, stichtag)["id"].tolist()   →  [4, 1]
    ohne_frist(daten, fristen)                 →  [5]
    bericht(daten, fristen, stichtag).values.tolist()
        →  [["bewerbung", 2, 1], ["newsletter", 1, 1], ["rechnung", 1, 0]]

Grenzen: roh hat 0 bis 100 000 Zeilen. id ist eine ganze Zahl von 1
bis 10**9. kategorie ist ein Text aus Buchstaben ohne Umlaute, der
nach dem Entfernen der Leerzeichen am Rand nicht leer ist. erstellt ist
ein gültiges Datum JJJJ-MM-TT zwischen 1990-01-01 und 2030-12-31 oder ein
beliebiger anderer Text oder leer. kunde ist ein nicht leerer Text.
fristen hat 1 bis 100 Zeilen mit verschiedenen Kategorien in
Kleinbuchstaben, frist_tage ist eine ganze Zahl von 0 bis 36 500.
stichtag ist ein pd.Timestamp. Benutzen Sie keine Schleife über die
Zeilen.

Hintergrund: Ein kleines Datenprojekt hat fast immer dieselben drei
Schritte: bereinigen, verknüpfen, auswerten. Wer sie in getrennte
Funktionen legt, kann jeden Schritt einzeln testen und später
austauschen. Verknüpfen (merge), Gruppieren mit benannten Aggregationen
(groupby(…).agg(…)), assign und sort_values kennen Sie aus Aufgabe
5_015; dass man ganze Spalten auf einmal bearbeitet statt Zeile für
Zeile, aus Aufgabe 5_006. Neu sind einige Werkzeuge fürs Bereinigen.

read_csv liest eine Tabelle aus einem Text, wenn man ihn in
io.StringIO verpackt; dtype legt die Typen der Spalten fest, hier
bleibt erstellt ein Text, damit man das Umwandeln selbst steuert.
Textspalten haben unter .str die Methoden von Texten, angewendet auf
jede Zelle: spalte.str.strip().str.lower() entfernt die Leerzeichen am
Rand und macht alles klein.

pd.to_datetime(spalte, format="%Y-%m-%d", errors="coerce") wandelt
Texte in Daten um; was nicht zum Format passt, etwa "2023-02-30", wird
mit errors="coerce" zu NaT („not a time“), dem fehlenden Wert für
Daten, statt einen Fehler auszulösen. Fehlende Werte findet isna(), und
dropna(subset=["spalte"]) entfernt die Zeilen, in denen diese Spalte
fehlt. drop_duplicates(subset="id", keep="first") behält von gleichen
ids die erste Zeile, reset_index(drop=True) nummeriert danach neu:

    tabelle = pd.DataFrame({"tag": ["2024-01-31", "gestern", "2024-02-30"]})
    pd.to_datetime(tabelle["tag"], format="%Y-%m-%d", errors="coerce").isna().tolist()
        →  [False, True, True]

Mit Daten kann man rechnen: Ein Datum plus eine Zeitspanne ist wieder
ein Datum, und pd.to_timedelta(spalte, unit="D") macht aus einer
Spalte mit Zahlen eine Spalte mit so vielen Tagen. Daten vergleicht man
mit <, <= und so weiter, auch mit einem einzelnen pd.Timestamp:

    beginn = pd.to_datetime(pd.Series(["2024-12-30"]))
    (beginn + pd.to_timedelta(pd.Series([3]), unit="D")).dt.strftime("%Y-%m-%d").tolist()
        →  ["2025-01-02"]
    (beginn <= pd.Timestamp("2025-01-01")).tolist()   →  [True]

spalte.isin(werte) liefert für jede Zelle True oder False, je nachdem,
ob ihr Wert unter werte vorkommt; ~ dreht eine solche Maske um. Beim
merge entscheidet how, welche Zeilen bleiben: "inner" behält nur
Schlüssel, die in beiden Tabellen stehen, "left" alle Zeilen der linken
Tabelle (fehlende Werte werden NaN).
"""

import io

import pandas as pd

ROHDATEN = """id,kategorie,erstellt,kunde
1, Bewerbung ,2024-03-01,K-17
2,rechnung,2015-12-31,K-03
2,Rechnung,2016-01-05,K-03
3,Newsletter,2023-02-30,K-11
4,NEWSLETTER,2022-06-15,K-11
5,Chatprotokoll,2024-01-10,K-08
6,bewerbung,2024-11-20,K-21
"""

FRISTEN = """kategorie,frist_tage
bewerbung,180
rechnung,3650
newsletter,730
"""

SPALTENTYPEN = {"id": "int64", "frist_tage": "int64", "kategorie": str, "erstellt": str, "kunde": str}


def lade(text):
    """Liest eine CSV-Tabelle aus text; id und frist_tage werden Zahlen, alle anderen Spalten bleiben Texte."""
    return pd.read_csv(io.StringIO(text), dtype=SPALTENTYPEN)


def bereinige(roh):
    """Vereinheitlicht die Kategorien, wandelt erstellt in Daten um und entfernt ungültige und doppelte Zeilen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def loeschtermine(daten, fristen):
    """Verknüpft daten mit fristen und ergänzt loeschen_ab; Datensätze ohne Frist fallen weg."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def faellige(daten, fristen, stichtag):
    """Gibt id, kategorie und loeschen_ab der Datensätze zurück, die zum stichtag gelöscht werden müssen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ohne_frist(daten, fristen):
    """Gibt die sortierten ids der Datensätze zurück, für deren Kategorie keine Löschfrist festgelegt ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bericht(daten, fristen, stichtag):
    """Gibt je Kategorie mit Frist die Anzahl der Datensätze und der fälligen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


daten = bereinige(lade(ROHDATEN))
fristen = lade(FRISTEN)
stichtag = pd.Timestamp("2025-01-01")
print(daten["id"].tolist())
print(faellige(daten, fristen, stichtag)["id"].tolist())
print(ohne_frist(daten, fristen))
print(bericht(daten, fristen, stichtag).values.tolist())
