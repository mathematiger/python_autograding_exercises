r"""Aufgabe 3_053 – Kühltransport                                 Stufe 3 ★★★☆☆

Eine Spedition fährt tiefgekühlte Lebensmittel aus. In jedem Laderaum
hängt ein Datenlogger, ein kleines Gerät, das alle 15 Minuten die
Temperatur misst und meldet, ob die Tür offen ist. Am Ziel lädt der
Fahrer die Daten über Funk auf ein Gateway, das sie als CSV-Text
weitergibt. Das Gateway ist auf deutsche Tabellenkalkulationen
eingestellt: Die Felder sind durch Semikolons getrennt, Kommazahlen
haben ein Komma, und die Nummer des Loggers hat immer fünf Ziffern,
auch mit Nullen vorn. tuer ist 1 für offen und 0 für zu:

    logger;zeit;temperatur;tuer
    00731;08:00;-18,5;0
    00731;08:15;-12,0;1
    04120;08:00;-19,25;0

Schreiben Sie zwei Funktionen:

- `lade_messungen(text)` liest den CSV-Text mit pandas ein und gibt den
  DataFrame zurück. logger bleibt Text mit den Nullen vorn, zeit bleibt
  Text, temperatur wird eine Kommazahl und tuer eine ganze Zahl.
- `kompakt(messungen)` gibt eine neue Tabelle mit denselben Spalten und
  Werten zurück, in der aber temperatur den Datentyp float32 und tuer
  den Datentyp bool hat. Das Gateway hat wenig Speicher, und beide Typen
  brauchen weniger Platz. Die übergebene Tabelle bleibt unverändert.

    df = lade_messungen(text)
    df["logger"].tolist()                   →  ["00731", "00731", "04120"]
    df["temperatur"].tolist()               →  [-18.5, -12.0, -19.25]
    kompakt(df)["tuer"].tolist()            →  [False, True, False]
    str(kompakt(df)["temperatur"].dtype)    →  "float32"

Grenzen: Der Text beginnt mit genau dieser Kopfzeile, danach kommen 0 bis
10 000 Zeilen, durch "\n" getrennt. logger besteht aus fünf Ziffern,
zeit hat die Form HH:MM, temperatur ist eine Kommazahl von -40 bis 30
mit höchstens zwei Nachkommastellen, tuer ist 0 oder 1.

Hintergrund: Einen DataFrame aus einer Liste von Dictionaries kennen Sie
aus Aufgabe 3_038. Meist kommen Tabellen aber als CSV, und dann liest
pd.read_csv sie ein. Statt eines Dateinamens nimmt es auch einen Text,
den io.StringIO wie eine Datei lesbar macht (Aufgabe 3_051). Dabei rät
pandas für jede Spalte den Datentyp: ganze Zahlen werden int64,
Kommazahlen float64, Texte object (ab pandas 3 str). df.dtypes zeigt,
was herauskam. Das Raten geht schief, wenn eine Spalte wie eine Zahl
aussieht, aber keine ist: Aus der Postleitzahl 01067 wird die Zahl
1067. Mit dtype legen Sie den Typ einzelner Spalten selbst fest; sep
und decimal sagen, welches Zeichen Felder trennt und welches vor den
Nachkommastellen steht:

    import io
    import pandas as pd

    text = "plz;ort;flaeche\n01067;Dresden;328,3\n"
    df = pd.read_csv(io.StringIO(text), sep=";", decimal=",", dtype={"plz": str})
    df["plz"].tolist()          # ['01067']
    df["flaeche"].tolist()      # [328.3]

Den Typ einer fertigen Spalte ändert astype; es gibt eine neue Spalte
zurück, beim DataFrame mit einem Dictionary Spalte → Typ eine neue
Tabelle: df.astype({"flaeche": "float32"}). Ein float32 braucht 4 statt
8 Byte, ist dafür nur auf etwa 7 Stellen genau. astype(bool) macht aus
0 False und aus jeder anderen Zahl True.
"""

import io

import pandas as pd


def lade_messungen(text):
    """Liest den CSV-Text des Gateways als DataFrame ein, logger als Text."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kompakt(messungen):
    """Gibt eine neue Tabelle mit temperatur als float32 und tuer als bool zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


text = "logger;zeit;temperatur;tuer\n00731;08:00;-18,5;0\n00731;08:15;-12,0;1\n04120;08:00;-19,25;0\n"
messungen = lade_messungen(text)
print(messungen["logger"].tolist())
print(messungen["temperatur"].tolist())
print(kompakt(messungen)["tuer"].tolist())
