# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_044_speicherprognose.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_044_speicherprognose

"""Aufgabe 3_044 – Speicherprognose                              Stufe 3 ★★★☆☆

Im Rechenzentrum liegen die Daten der virtuellen Maschinen auf
Speicher-Volumes, Bereichen fester Größe in einem Speichersystem. Läuft
ein Volume voll, stürzen die Maschinen darauf ab. Das Betriebsteam
bekommt jeden Morgen eine Tabelle mit den Spalten volume (Name),
kapazitaet_gb (Größe), belegt_gb (davon belegt) und wachstum_gb (so viel
kommt im Schnitt pro Tag dazu). Schreiben Sie zwei Funktionen, die
jeweils eine neue Tabelle mit zusätzlichen Spalten zurückgeben:

- `mit_belegung(volumes)` ergänzt die Spalten frei_gb (Kapazität minus
  Belegung) und belegung (belegt_gb in Prozent der Kapazität, gerundet
  auf eine Nachkommastelle).
- `mit_prognose(volumes)` ergänzt dieselben beiden Spalten und dahinter
  tage_bis_voll (wie viele volle Tage der freie Platz beim jetzigen
  Wachstum noch reicht: frei_gb ganzzahlig geteilt durch wachstum_gb)
  und kritisch (True, wenn belegung mindestens 80 ist oder tage_bis_voll
  kleiner als 14, sonst False).

Die neuen Spalten stehen hinter den alten, in der genannten
Reihenfolge; die Zeilen behalten ihre Reihenfolge. Die übergebene
Tabelle bleibt unverändert. Rechnen Sie mit ganzen Spalten, ohne
Schleife über die Zeilen.

    volumes = pd.DataFrame([
        {"volume": "vol-a", "kapazitaet_gb": 1000, "belegt_gb": 850, "wachstum_gb": 2},
        {"volume": "vol-b", "kapazitaet_gb": 2000, "belegt_gb": 500, "wachstum_gb": 120},
        {"volume": "vol-c", "kapazitaet_gb": 3000, "belegt_gb": 1000, "wachstum_gb": 10},
    ])
    mit_belegung(volumes)["belegung"].tolist()        →  [85.0, 25.0, 33.3]
    mit_prognose(volumes)["tage_bis_voll"].tolist()   →  [75, 12, 200]
    mit_prognose(volumes)["kritisch"].tolist()        →  [True, True, False]

Grenzen: 0 bis 10 000 Zeilen mit genau den vier Spalten oben, auch
eine leere Tabelle mit diesen Spalten ist möglich. kapazitaet_gb ist
eine ganze Zahl von 1 bis 100 000, belegt_gb eine ganze Zahl von 0 bis
kapazitaet_gb, wachstum_gb eine ganze Zahl von 1 bis 1000.

Hintergrund: Wie man Spalten auswählt und mit Masken filtert, steht in
den Aufgaben 3_038 und 3_041. Rechnet man mit einer ganzen Spalte, gilt
die Rechnung für jede Zeile einzeln, und es kommt wieder eine Spalte
(Series) heraus. Mit zwei Spalten wird Zeile für Zeile gerechnet:

    df["netto"] - df["rabatt"]          # für jede Zeile netto minus rabatt
    df["anteil"].round(1)               # jede Zahl auf eine Stelle gerundet
    df["cpu"] >= 80                     # True oder False je Zeile

Weist man so eine Series einem neuen Spaltennamen zu, hängt pandas die
Spalte hinten an. Das verändert allerdings genau die Tabelle, in die
man schreibt. Soll das Original bleiben, wie es war, arbeitet man auf
einer Kopie:

    neu = df.copy()
    neu["brutto"] = neu["netto"] * 1.19
    neu["teuer"] = (neu["brutto"] > 100) | (neu["menge"] > 5)

Ohne copy() zeigt neu = df nur auf dieselbe Tabelle (wie bei Listen in
Aufgabe 2_018), und jede neue Spalte landete auch im Original. Eine neue
Spalte darf schon auf einer anderen neuen aufbauen, wenn sie danach
berechnet wird. Schleifen über die Zeilen braucht man dafür nicht;
pandas rechnet ganze Spalten auf einmal und viel schneller.
"""

import pandas as pd


def mit_belegung(volumes):
    """Gibt eine neue Tabelle mit den Spalten frei_gb und belegung zurück."""
    neu = volumes.copy()
    neu["frei_gb"] = neu["kapazitaet_gb"] - neu["belegt_gb"]
    neu["belegung"] = (neu["belegt_gb"] / neu["kapazitaet_gb"] * 100).round(1)
    return neu


def mit_prognose(volumes):
    """Gibt eine neue Tabelle mit Belegung, Tagen bis voll und der Spalte kritisch zurück."""
    neu = mit_belegung(volumes)
    neu["tage_bis_voll"] = neu["frei_gb"] // neu["wachstum_gb"]
    neu["kritisch"] = (neu["belegung"] >= 80) | (neu["tage_bis_voll"] < 14)
    return neu


volumes = pd.DataFrame(
    [
        {"volume": "vol-a", "kapazitaet_gb": 1000, "belegt_gb": 850, "wachstum_gb": 2},
        {"volume": "vol-b", "kapazitaet_gb": 2000, "belegt_gb": 500, "wachstum_gb": 120},
        {"volume": "vol-c", "kapazitaet_gb": 3000, "belegt_gb": 1000, "wachstum_gb": 10},
    ]
)
print(mit_belegung(volumes)["belegung"].tolist())
print(mit_prognose(volumes)["tage_bis_voll"].tolist())
print(mit_prognose(volumes)["kritisch"].tolist())


# Idee: Erst mit volumes.copy() eine Kopie anlegen, dann jede neue Spalte als Rechnung mit ganzen
# Spalten zuweisen: Differenz, Quotient mal 100 mit .round(1), Ganzzahldivision mit // und für
# kritisch zwei Masken mit | verknüpft. mit_prognose ruft mit_belegung auf und baut darauf auf, so
# steht die Rechnung für frei_gb und belegung nur einmal im Code.
# Anderer Weg: volumes.assign(frei_gb=..., belegung=...) gibt ohne copy() eine neue Tabelle zurück;
# spätere Spalten können dort mit lambda df: df["frei_gb"] // df["wachstum_gb"] auf frühere
# zugreifen. Eine Schleife über die Zeilen mit iterrows oder apply rechnet dasselbe, ist aber viel
# langsamer und hier ausgeschlossen.
# Typische Fehler: ohne copy() in die übergebene Tabelle schreiben, / statt // (dann 12.5 statt 12
# Tage), round(belegung) ohne Stellen (rundet auf ganze Zahlen), and/or statt |/& oder fehlende
# Klammern um die Vergleiche, > 80 statt >= 80 und <= 14 statt < 14.
# Laufzeit: O(n) für n Zeilen; jede Spaltenrechnung geht einmal über alle Zeilen.
