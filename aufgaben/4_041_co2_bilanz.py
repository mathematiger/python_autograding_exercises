"""Aufgabe 4_041 – CO₂-Bilanz                                    Stufe 4 ★★★★☆

Ein Unternehmen mit mehreren Standorten will für seinen
Nachhaltigkeitsbericht wissen, wie viel Strom seine IT-Geräte
verbrauchen und wie viel CO₂ dabei entsteht. Aus der Inventarliste kommt
ein DataFrame mit einer Zeile je Gerät und den Spalten inventar
(eindeutige Nummer), standort, typ (etwa "Notebook" oder "Drucker"),
kwh_jahr (geschätzter Verbrauch in Kilowattstunden pro Jahr) und alter
(in Jahren). Schreiben Sie mit groupby und agg drei Funktionen, die je
einen neuen DataFrame zurückgeben:

- `verbrauch_je_standort(geraete)` hat eine Zeile je Standort mit den
  Spalten standort, anzahl (Zahl der Geräte) und kwh (Summe von
  kwh_jahr), sortiert nach standort.
- `co2_bilanz(geraete, gramm_pro_kwh)` hat dieselben Spalten und
  dahinter co2_kg: kwh mal gramm_pro_kwh, geteilt durch 1000, gerundet
  auf eine Nachkommastelle. Sortiert nach co2_kg absteigend, bei
  Gleichstand nach standort.
- `typen_uebersicht(geraete)` hat eine Zeile je Typ mit den Spalten
  typ, anzahl, kwh_mittel (Mittelwert von kwh_jahr, gerundet auf eine
  Nachkommastelle) und aeltestes (größtes alter), sortiert nach typ.

standort und typ sind normale Spalten, nicht der Index; welchen Index
die Ergebnisse haben, ist egal. Die übergebene Tabelle bleibt
unverändert. Benutzen Sie keine Schleife über die Zeilen oder Gruppen.

    geraete = pd.DataFrame([
        {"inventar": 1, "standort": "Kiel", "typ": "Notebook", "kwh_jahr": 40, "alter": 2},
        {"inventar": 2, "standort": "Kiel", "typ": "Drucker", "kwh_jahr": 150, "alter": 6},
        {"inventar": 3, "standort": "Bonn", "typ": "Notebook", "kwh_jahr": 35, "alter": 4},
        {"inventar": 4, "standort": "Kiel", "typ": "Notebook", "kwh_jahr": 45, "alter": 1},
    ])
    verbrauch_je_standort(geraete).to_dict("records")
        →  [{"standort": "Bonn", "anzahl": 1, "kwh": 35},
            {"standort": "Kiel", "anzahl": 3, "kwh": 235}]
    co2_bilanz(geraete, 380)["co2_kg"].tolist()          →  [89.3, 13.3]
    typen_uebersicht(geraete)["kwh_mittel"].tolist()     →  [150.0, 40.0]

Grenzen: 0 bis 20 000 Zeilen mit genau den fünf Spalten oben, auch eine
leere Tabelle mit diesen Spalten ist möglich. standort und typ sind
nicht leere Texte, kwh_jahr ist eine ganze Zahl von 0 bis 5000, alter
eine von 0 bis 20; gramm_pro_kwh ist eine ganze Zahl von 0 bis 1000.

Hintergrund: In Aufgabe 4_037 haben Sie mit SQL gruppiert: GROUP BY
fasst alle Zeilen mit gleichem Wert zusammen, und COUNT, SUM oder AVG
machen aus jeder Gruppe eine Zahl. pandas kann das selbst, nach dem
Muster „aufteilen, berechnen, zusammensetzen“:

    df.groupby("raum")                     # teilt in eine Gruppe je Raum
    df.groupby("raum")["watt"].sum()       # eine Summe je Raum

Das Ergebnis ist nach dem Gruppenschlüssel sortiert, und der Schlüssel
wird zum Index. Mehrere Kennzahlen auf einmal berechnet agg. Am
lesbarsten ist die benannte Form: Jedes Argument ist eine neue Spalte,
und das Tupel sagt, welche Spalte womit zusammengefasst wird:

    df.groupby("raum").agg(
        geraete=("watt", "count"),         # Zahl der Werte in der Gruppe
        summe=("watt", "sum"),
        mittel=("watt", "mean"),
        groesste=("watt", "max"),
    )

Weitere Namen sind "min", "median", "first" und "nunique" (Zahl der
verschiedenen Werte). Danach steht raum im Index, nicht in einer
Spalte. reset_index() macht daraus wieder eine gewöhnliche Spalte
(oder man schreibt gleich groupby("raum", as_index=False)):

    ergebnis = df.groupby("raum").agg(summe=("watt", "sum")).reset_index()
    ergebnis.to_dict("records")  →  [{"raum": "A", "summe": 300}, ...]

Mit dem Ergebnis geht es wie mit jeder Tabelle weiter: neue Spalten
berechnen (Aufgabe 3_044) und mit sort_values sortieren (Aufgabe
3_041). groupby verändert die ursprüngliche Tabelle nicht.
"""

import pandas as pd


def verbrauch_je_standort(geraete):
    """Gibt je Standort die Zahl der Geräte und den Verbrauch zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def co2_bilanz(geraete, gramm_pro_kwh):
    """Gibt je Standort Anzahl, Verbrauch und CO₂ in kg zurück, die größten zuerst."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def typen_uebersicht(geraete):
    """Gibt je Typ Anzahl, mittleren Verbrauch und das höchste Alter zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


geraete = pd.DataFrame(
    [
        {"inventar": 1, "standort": "Kiel", "typ": "Notebook", "kwh_jahr": 40, "alter": 2},
        {"inventar": 2, "standort": "Kiel", "typ": "Drucker", "kwh_jahr": 150, "alter": 6},
        {"inventar": 3, "standort": "Bonn", "typ": "Notebook", "kwh_jahr": 35, "alter": 4},
        {"inventar": 4, "standort": "Kiel", "typ": "Notebook", "kwh_jahr": 45, "alter": 1},
    ]
)
print(verbrauch_je_standort(geraete).to_dict("records"))
print(co2_bilanz(geraete, 380)["co2_kg"].tolist())
print(typen_uebersicht(geraete)["kwh_mittel"].tolist())
