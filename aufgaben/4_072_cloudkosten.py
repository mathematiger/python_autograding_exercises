"""Aufgabe 4_072 – Cloudkosten                                   Stufe 4 ★★★★☆

Ein Entwicklungsteam mietet für seine Tests virtuelle Maschinen (VMs)
bei einem Cloud-Anbieter. Abgerechnet wird jede angefangene Stunde, in
der eine VM läuft. Die Controllerin vermutet, dass viele Test-VMs auch
nachts und am Wochenende laufen, obwohl dann niemand testet, und will
wissen, ob sich eine automatische Abschaltung lohnt: Die Kernarbeitszeit
ist montags bis freitags von 07:00 bis 19:00 Uhr, alles andere gilt als
„außerhalb“. Der Anbieter liefert die Abrechnung als CSV-Text, eine
Zeile je VM und Stunde, mit dem Beginn der Stunde:

    zeitpunkt,vm,kosten_eur
    20.11.2026 08:00,test-01,0.40
    20.11.2026 13:00,test-02,0.85
    20.11.2026 20:00,test-01,0.40
    21.11.2026 10:00,test-02,0.85
    23.11.2026 06:00,test-02,0.85
    23.11.2026 07:00,test-01,0.40
    23.11.2026 18:00,test-02,0.85
    23.11.2026 19:00,test-01,0.40

Der 20.11.2026 ist ein Freitag, der 21. ein Samstag, der 23. ein Montag.
Schreiben Sie vier Funktionen mit pandas, alle ohne Python-Schleife:

- `lade(text)` liest den CSV-Text in einen DataFrame mit den Spalten
  zeitpunkt, vm und kosten_eur; zeitpunkt wird dabei ein Zeitpunkt
  (Datentyp datetime64), kein Text.
- `ausserhalb(abrechnung)` gibt eine Serie aus True und False zurück,
  eine je Zeile: True, wenn die Stunde am Samstag oder Sonntag liegt
  oder vor 07:00 oder ab 19:00 Uhr beginnt.
- `ausserhalb_kosten(abrechnung)` gibt die Summe der Kosten dieser
  Stunden zurück, auf Cent gerundet. Benutzen Sie dafür ausserhalb.
- `kosten_je_tag(abrechnung)` gibt eine Serie mit den Kosten je
  Kalendertag zurück, auf Cent gerundet, vom ersten bis zum letzten Tag
  der Abrechnung; der Index sind die Tage (jeweils 00:00 Uhr). Tage ohne
  eine einzige Zeile kommen mit 0 vor.

    abrechnung = lade(text)
    ausserhalb(abrechnung).tolist()
    →  [False, False, True, True, True, False, False, True]
    ausserhalb_kosten(abrechnung)       →  2.5
    kosten_je_tag(abrechnung)
    →  2026-11-20    1.65
       2026-11-21    0.85
       2026-11-22    0.00
       2026-11-23    2.50

Grenzen: Der Text beginnt mit der Kopfzeile oben, danach 0 bis 10 000
Zeilen, nicht unbedingt zeitlich sortiert. zeitpunkt hat genau die Form
TT.MM.JJJJ HH:MM mit gültigem Datum zwischen 2000 und 2099, vm ist ein
nicht leerer Name ohne Komma, kosten_eur eine Zahl von 0 bis 100 mit
höchstens zwei Nachkommastellen.

Hintergrund: Wie man einen CSV-Text mit pd.read_csv(io.StringIO(text))
liest, kennen Sie aus Aufgabe 3_053. Datumsangaben bleiben dabei Texte.
pd.to_datetime macht aus einer Spalte von Texten eine Spalte von
Zeitpunkten (pandas nennt sie Timestamp; sie verhalten sich wie datetime
aus Aufgabe 4_071). Geben Sie das Format immer mit an, mit denselben
Platzhaltern wie bei strptime: Ohne format rät pandas, und bei
"05.12.2026" rät es den 12. Mai.

    df["zeit"] = pd.to_datetime(df["zeit"], format="%d.%m.%Y %H:%M")

Wie .str bei Texten (Aufgabe 4_068) gibt es .dt für Zeitpunkte: Es
wendet eine Eigenschaft auf jeden Wert der Spalte an und liefert eine
neue Serie, ganz ohne Schleife.

    df["zeit"].dt.hour          # Stunde, 0 bis 23
    df["zeit"].dt.day_of_week     # Wochentag, 0 = Montag bis 6 = Sonntag
    df["zeit"].dt.date          # nur das Datum
    df["zeit"].dt.month         # Monat, 1 bis 12

Daraus baut man Masken wie in Aufgabe 3_041 und verknüpft sie mit | und &
(jede Bedingung in Klammern).

resample ist groupby (Aufgabe 4_041) für die Zeit: Es teilt die Zeilen
in gleich lange Zeitabschnitte, hier "D" für Tage ("W" für Wochen, "h"
für Stunden, "MS" für Monate), und fasst jeden Abschnitt zusammen. on=
nennt die Spalte mit den Zeitpunkten; danach wählt man die Spalte, die
zusammengefasst werden soll:

    df.resample("D", on="zeit")["menge"].sum()

Anders als groupby nach df["zeit"].dt.date legt resample jeden
Abschnitt zwischen dem ersten und dem letzten an, auch leere; deren
Summe ist 0. Der Index der Ergebnisserie sind die Anfänge der
Abschnitte. Gerundet wird eine Serie mit .round(2), eine einzelne Zahl
mit round(zahl, 2).
"""

import io

import pandas as pd

TEXT = """zeitpunkt,vm,kosten_eur
20.11.2026 08:00,test-01,0.40
20.11.2026 13:00,test-02,0.85
20.11.2026 20:00,test-01,0.40
21.11.2026 10:00,test-02,0.85
23.11.2026 06:00,test-02,0.85
23.11.2026 07:00,test-01,0.40
23.11.2026 18:00,test-02,0.85
23.11.2026 19:00,test-01,0.40
"""


def lade(text):
    """Liest die Abrechnung aus einem CSV-Text; zeitpunkt wird ein Zeitpunkt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ausserhalb(abrechnung):
    """Gibt für jede Zeile an, ob die Stunde am Wochenende oder außerhalb von 07:00 bis 19:00 liegt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ausserhalb_kosten(abrechnung):
    """Gibt die Kosten der Stunden außerhalb der Kernarbeitszeit zurück, auf Cent gerundet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kosten_je_tag(abrechnung):
    """Gibt die Kosten je Kalendertag zurück, auch für Tage ohne Zeilen, auf Cent gerundet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


abrechnung = lade(TEXT)
print(ausserhalb(abrechnung).tolist())
print(ausserhalb_kosten(abrechnung))
print(kosten_je_tag(abrechnung).tolist())
