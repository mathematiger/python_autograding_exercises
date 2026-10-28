"""Aufgabe 2_012 – Übertragung                                   Stufe 2 ★★☆☆☆

Ein Systemhaus will seinen Kunden vorrechnen, wie lange das nächtliche
Backup über das Netz dauert. Die Bandbreite einer Leitung wird in Megabit
pro Sekunde (Mbit/s) angegeben, Dateigrößen aber in Megabyte (MB). Ein
Byte hat 8 Bit, also braucht eine Datei von 250 MB über eine Leitung mit
100 Mbit/s 250 * 8 / 100 = 20 Sekunden.

Ein Kollege hat dafür schon zwei Funktionen geschrieben, aber sie
funktionieren nicht:

    bandbreite = 100
    gesamt = 0

    def dauer(megabyte, mbit_pro_sekunde):
        return round(megabyte * 8 / bandbreite, 1)

    def gesamtdauer(dateien, mbit_pro_sekunde):
        for megabyte in dateien:
            gesamt = gesamt + megabyte * 8 / mbit_pro_sekunde
        return round(gesamt, 1)

dauer(250, 50) liefert 20.0 statt 40.0, und gesamtdauer bricht mit einem
UnboundLocalError ab. Finden Sie die beiden Fehler und schreiben Sie die
Funktionen richtig:

- `dauer(megabyte, mbit_pro_sekunde)` gibt die Übertragungsdauer einer
  Datei in Sekunden zurück, auf eine Nachkommastelle gerundet.
- `gesamtdauer(dateien, mbit_pro_sekunde)` bekommt eine Liste von
  Dateigrößen in MB und gibt die Dauer für alle zusammen zurück, ebenfalls
  auf eine Nachkommastelle gerundet. Eine leere Liste dauert 0 Sekunden.

    dauer(250, 100)                    →  20.0
    dauer(250, 50)                     →  40.0
    gesamtdauer([250, 125, 50], 100)   →  34.0

Beide Funktionen sollen nur mit ihren Parametern arbeiten. Sie müssen
jedes Mal dasselbe Ergebnis liefern, egal wie oft man sie aufruft.

Grenzen: Alle Werte sind ganze Zahlen. Jede Dateigröße liegt bei
0 ≤ megabyte ≤ 10**6, die Bandbreite bei 1 ≤ mbit_pro_sekunde ≤ 100 000, und
dateien hat 0 ≤ len(dateien) ≤ 1000 Einträge.

Hintergrund: Eine Variable, der man innerhalb einer Funktion einen Wert
zuweist, ist lokal: Sie entsteht beim Aufruf, gilt nur in dieser Funktion
und verschwindet danach wieder. Parameter sind ebenfalls lokale Variablen.
Variablen, die außerhalb jeder Funktion zugewiesen werden, sind global.
Eine Funktion kann globale Variablen lesen, wenn sie keine lokale mit
demselben Namen hat; das ist der erste Fehler des Kollegen: Er liest die
globale bandbreite statt seines Parameters, und so rechnet die Funktion
immer mit 100. Weist eine Funktion einer Variablen irgendwo einen Wert zu,
ist dieser Name in der ganzen Funktion lokal, auch vor der Zuweisung. In
gesamt = gesamt + ... ist gesamt deshalb lokal und hat beim ersten Lesen
noch keinen Wert; Python meldet einen UnboundLocalError. Die Lösung ist
nicht, die globale Variable zu benutzen, sondern eine lokale Variable in
der Funktion anzulegen, bevor die Schleife beginnt. Eine globale Summe
würde bei jedem Aufruf weiterwachsen.

Tipp: Eine Datei von 125 MB braucht bei 100 Mbit/s 10 Sekunden.
"""

bandbreite = 100
gesamt = 0


def dauer(megabyte, mbit_pro_sekunde):
    """Gibt die Übertragungsdauer einer Datei in Sekunden zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gesamtdauer(dateien, mbit_pro_sekunde):
    """Gibt die Übertragungsdauer aller Dateien zusammen in Sekunden zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print("250 MB bei 100 Mbit/s:", dauer(250, 100), "Sekunden")
print("250 MB bei 50 Mbit/s:", dauer(250, 50), "Sekunden")
print("Backup bei 100 Mbit/s:", gesamtdauer([250, 125, 50], 100), "Sekunden")
