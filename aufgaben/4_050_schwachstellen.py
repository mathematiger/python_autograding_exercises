"""Aufgabe 4_050 – Schwachstellen                                Stufe 4 ★★★★☆

Ein Schwachstellen-Scanner prüft jede Nacht alle Server einer Firma auf
bekannte Sicherheitslücken, etwa veraltete Software mit einem
öffentlich bekannten Fehler. Jeder Fund bekommt einen Schweregrad:
niedrig, mittel, hoch oder kritisch. Die Funde, die noch nicht behoben
sind, kommen als DataFrame mit einer Zeile je Fund und den Spalten
system (Name des Servers), schweregrad und tage_offen (seit wie vielen
Tagen der Fund bekannt ist). Für die wöchentliche Besprechung mit der
IT-Sicherheit braucht es Kreuztabellen: eine Zeile je System, eine
Spalte je Schweregrad. Schreiben Sie mit pivot_table drei Funktionen,
die je einen neuen DataFrame zurückgeben:

- `anzahl_matrix(funde)`: in jeder Zelle die Zahl der Funde dieses
  Systems mit diesem Schweregrad, 0 wo es keinen gibt.
- `mittlere_dauer(funde)`: in jeder Zelle der Mittelwert von tage_offen,
  gerundet auf eine Nachkommastelle; wo es keinen Fund gibt, NaN.
- `mit_gesamt(funde)`: wie anzahl_matrix, dazu eine letzte Spalte und
  eine letzte Zeile namens "gesamt" mit den Summen.

In allen drei steht system im Index, alphabetisch sortiert (bei
mit_gesamt danach die Zeile "gesamt"). Die Spalten sind immer die vier
Schweregrade in der Reihenfolge niedrig, mittel, hoch, kritisch, auch
wenn einer davon gar nicht vorkommt (bei mit_gesamt danach "gesamt").
Die übergebene Tabelle bleibt unverändert. Benutzen Sie keine Schleife
über die Zeilen.

    funde = pd.DataFrame([
        {"system": "web01", "schweregrad": "hoch", "tage_offen": 12},
        {"system": "db01", "schweregrad": "kritisch", "tage_offen": 3},
        {"system": "web01", "schweregrad": "hoch", "tage_offen": 5},
        {"system": "web01", "schweregrad": "niedrig", "tage_offen": 40},
    ])
    anzahl_matrix(funde).to_dict("index")
        →  {"db01": {"niedrig": 0, "mittel": 0, "hoch": 0, "kritisch": 1},
            "web01": {"niedrig": 1, "mittel": 0, "hoch": 2, "kritisch": 0}}
    mittlere_dauer(funde).loc["web01", "hoch"]       →  8.5
    mit_gesamt(funde).loc["gesamt", "gesamt"]        →  4

Grenzen: 1 bis 20 000 Zeilen mit genau den drei Spalten oben. system
ist ein nicht leerer Text (nie "gesamt"), schweregrad einer der vier
Texte, tage_offen eine ganze Zahl von 0 bis 3650.

Hintergrund: Mit groupby und agg (Aufgabe 4_041) bekommt man eine Zeile
je Gruppe. Gruppiert man nach zwei Spalten, will man das Ergebnis oft
als Kreuztabelle sehen: die Werte der einen Spalte als Zeilen, die der
anderen als Spalten, wie in einer Pivot-Tabelle einer
Tabellenkalkulation. Das macht pivot_table:

    tabelle = df.pivot_table(
        index="raum",          # wird zu den Zeilen
        columns="tag",         # jeder Wert wird eine Spalte
        values="watt",         # diese Spalte wird zusammengefasst
        aggfunc="sum",         # womit: "count", "sum", "mean", "max" …
        fill_value=0,          # statt NaN, wo es keine Zeile gibt
    )
    tabelle.loc["A", "Mo"]     # eine Zelle lesen

Ohne fill_value steht in leeren Zellen NaN („not a number“, pandas'
Zeichen für einen fehlenden Wert). Mit margins=True kommen eine Zeile
und eine Spalte mit dem Gesamtergebnis dazu; margins_name="summe"
gibt ihnen einen Namen. Die Zeilen und Spalten sortiert pivot_table
alphabetisch, und es entstehen nur Spalten für Werte, die vorkommen.
Eine feste Reihenfolge, auch mit Spalten, die es noch nicht gibt,
erzwingt reindex:

    tabelle.reindex(columns=["Mo", "Di", "Mi"], fill_value=0)

Fehlende Spalten werden dabei mit fill_value aufgefüllt (ohne
fill_value mit NaN), Spalten, die nicht in der Liste stehen, fallen weg.
Zum Runden hat jeder DataFrame round(1), wie eine Spalte (Aufgabe
3_044). Der Index heißt nach der Spalte, aus der er stammt (hier
"raum"); das stört nicht.
"""

import pandas as pd

SCHWEREGRADE = ["niedrig", "mittel", "hoch", "kritisch"]


def anzahl_matrix(funde):
    """Gibt die Zahl der Funde je System und Schweregrad zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def mittlere_dauer(funde):
    """Gibt die mittlere Zahl offener Tage je System und Schweregrad zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def mit_gesamt(funde):
    """Gibt die Zahl der Funde je System und Schweregrad mit Summenzeile und -spalte zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


funde = pd.DataFrame(
    [
        {"system": "web01", "schweregrad": "hoch", "tage_offen": 12},
        {"system": "db01", "schweregrad": "kritisch", "tage_offen": 3},
        {"system": "web01", "schweregrad": "hoch", "tage_offen": 5},
        {"system": "web01", "schweregrad": "niedrig", "tage_offen": 40},
    ]
)
print(anzahl_matrix(funde).to_dict("index"))
print(mittlere_dauer(funde).loc["web01", "hoch"])
print(mit_gesamt(funde).loc["gesamt", "gesamt"])
