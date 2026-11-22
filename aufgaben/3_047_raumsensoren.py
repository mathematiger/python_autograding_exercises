"""Aufgabe 3_047 – Raumsensoren                                  Stufe 3 ★★★☆☆

In einem Bürogebäude hängt in jedem Raum ein Funksensor, der jede
Viertelstunde Temperatur (°C) und Luftfeuchte (%) an die
Gebäudesteuerung schickt. Funk ist unzuverlässig: Manchmal kommt ein
Wert nicht an, und bei neu angemeldeten Sensoren ist der Raum noch nicht
eingetragen. Die Gebäudesteuerung liefert die letzte Runde als Tabelle
mit den Spalten sensor, raum, temperatur und feuchte; was fehlt, ist
leer (in pandas NaN oder None). Schreiben Sie drei Funktionen:

- `luecken(messungen)` gibt ein Dictionary Spaltenname → Anzahl der
  fehlenden Werte zurück, für alle Spalten in ihrer Reihenfolge, auch
  für die ohne Lücke (dann 0).
- `vollstaendige(messungen)` gibt eine neue Tabelle mit den Zeilen
  zurück, in denen kein einziger Wert fehlt, in ihrer Reihenfolge.
- `aufgefuellt(messungen)` gibt eine neue Tabelle mit allen Zeilen
  zurück, in der ein fehlender Raum durch "unbekannt" und eine fehlende
  Temperatur durch den Mittelwert der vorhandenen Temperaturen ersetzt
  ist, gerundet auf eine Nachkommastelle. Fehlende Luftfeuchten bleiben
  leer, denn für sie soll der Sensor neu messen.

Die übergebene Tabelle bleibt unverändert.

    messungen = pd.DataFrame([
        {"sensor": "T-01", "raum": "Labor", "temperatur": 21.5, "feuchte": 40.0},
        {"sensor": "T-02", "raum": None, "temperatur": 23.0, "feuchte": 55.0},
        {"sensor": "T-03", "raum": "Lager", "temperatur": None, "feuchte": 61.0},
        {"sensor": "T-04", "raum": "Büro", "temperatur": 19.0, "feuchte": None},
        {"sensor": "T-05", "raum": "Flur", "temperatur": 20.1, "feuchte": 45.0},
    ])
    luecken(messungen)                          →  {"sensor": 0, "raum": 1, "temperatur": 1, "feuchte": 1}
    vollstaendige(messungen)["sensor"].tolist() →  ["T-01", "T-05"]
    aufgefuellt(messungen)["raum"].tolist()     →  ["Labor", "unbekannt", "Lager", "Büro", "Flur"]
    aufgefuellt(messungen)["temperatur"].tolist()  →  [21.5, 23.0, 20.9, 19.0, 20.1]

Grenzen: 0 bis 10 000 Zeilen mit genau den vier Spalten oben, auch eine
leere Tabelle ist möglich. sensor fehlt nie. raum ist ein nicht leerer
Text oder fehlt, temperatur eine Kommazahl von -40 bis 60, feuchte eine
von 0 bis 100, beide oder eine von ihnen können fehlen. Fehlt eine
Temperatur, gibt es in der Tabelle mindestens eine vorhandene.

Hintergrund: Wie man Spalten auswählt, filtert und auf einer Kopie neue
Spalten berechnet, steht in den Aufgaben 3_038, 3_041 und 3_044. Einen
fehlenden Wert speichert pandas in einer Zahlenspalte als NaN („not a
number“), in einer Textspalte oft als None. Mit == findet man ihn nicht,
denn NaN ist nicht einmal sich selbst gleich. Dafür gibt es isna(): Es
liefert True für jeden fehlenden Wert und False sonst, für eine Spalte
oder eine ganze Tabelle. Weil True als 1 zählt, zählt sum() die Lücken:

    df["preis"].isna()          # True/False je Zeile
    df["preis"].isna().sum()    # Anzahl der Lücken in der Spalte
    df.isna().sum()             # eine Series: Spaltenname → Anzahl

dropna() gibt eine neue Tabelle ohne die Zeilen zurück, in denen
irgendein Wert fehlt; mit dropna(subset=["preis"]) zählt nur diese
Spalte. fillna(wert) gibt eine neue Spalte zurück, in der jede Lücke
durch wert ersetzt ist:

    neu = df.copy()
    neu["ort"] = neu["ort"].fillna("ohne Ort")
    neu["preis"] = neu["preis"].fillna(0)

Rechenfunktionen wie mean() (Mittelwert), sum() oder max() übergehen
fehlende Werte: Der Mittelwert von 1, NaN und 3 ist 2. Eine Series
verhält sich wie ein Dictionary: for name, anzahl in reihe.items():
liefert Paare. pandas zählt mit eigenen Zahlentypen; int(anzahl) macht
daraus eine gewöhnliche Python-Zahl.
"""

import pandas as pd


def luecken(messungen):
    """Gibt ein Dictionary Spaltenname → Anzahl fehlender Werte zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def vollstaendige(messungen):
    """Gibt eine neue Tabelle nur mit den Zeilen ohne fehlenden Wert zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def aufgefuellt(messungen):
    """Gibt eine neue Tabelle mit aufgefülltem Raum und aufgefüllter Temperatur zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


messungen = pd.DataFrame(
    [
        {"sensor": "T-01", "raum": "Labor", "temperatur": 21.5, "feuchte": 40.0},
        {"sensor": "T-02", "raum": None, "temperatur": 23.0, "feuchte": 55.0},
        {"sensor": "T-03", "raum": "Lager", "temperatur": None, "feuchte": 61.0},
        {"sensor": "T-04", "raum": "Büro", "temperatur": 19.0, "feuchte": None},
        {"sensor": "T-05", "raum": "Flur", "temperatur": 20.1, "feuchte": 45.0},
    ]
)
print(luecken(messungen))
print(vollstaendige(messungen)["sensor"].tolist())
print(aufgefuellt(messungen)["raum"].tolist())
print(aufgefuellt(messungen)["temperatur"].tolist())
