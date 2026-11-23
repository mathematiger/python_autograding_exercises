"""Aufgabe 3_055 – Scanbericht                                   Stufe 3 ★★★☆☆

Jede Nacht durchsucht ein Virenscanner die Dateiablagen aller
Abteilungen. Er zählt, wie viele Dateien er geprüft hat und wie viele
davon auffällig waren, also möglicherweise Schadsoftware enthalten. Am
Morgen geht ein Bericht an das Sicherheitsteam der Konzernmutter in
Dublin. Das Team liest viele Berichte und erwartet die englische
Schreibweise: Komma als Tausendertrennzeichen, Punkt vor den
Nachkommastellen.

    Abteilung            Dateien   Befund
    Vertrieb           1,234,567    0.12%
    Labor                 48,210    2.50%
    Gesamt             1,282,777    0.21%

Schreiben Sie zwei Funktionen, die Text zurückgeben, ohne ihn
auszugeben:

- `zeile(abteilung, dateien, auffaellig)`: eine Zeile des Berichts. Die
  Abteilung steht linksbündig in einer Spalte der Breite 14, die Zahl
  der Dateien rechtsbündig mit Tausendertrennzeichen in einer Spalte
  der Breite 14 und der Anteil auffällig / dateien rechtsbündig als
  Prozentwert mit zwei Nachkommastellen in einer Spalte der Breite 9.
- `bericht(abteilungen)`: alle Zeilen des Berichts als Liste. Zuerst
  die Kopfzeile KOPF (vorgegeben), dann eine Zeile je Abteilung in der
  Reihenfolge der Liste, zuletzt die Zeile "Gesamt" mit den Summen
  beider Zahlen. abteilungen ist eine Liste von Tupeln
  (abteilung, dateien, auffaellig).

    zeile("Vertrieb", 1234567, 1543)  →  "Vertrieb           1,234,567    0.12%"
    zeile("Labor", 48210, 1205)       →  "Labor                 48,210    2.50%"

Grenzen: abteilung ist ein Text aus 1 bis 14 Zeichen, nicht "Gesamt".
dateien und auffaellig sind ganze Zahlen mit 1 ≤ dateien ≤ 10**9 und
0 ≤ auffaellig ≤ dateien. abteilungen hat 1 bis 1000 Einträge, die
Summe aller Dateien ist höchstens 10**9.

Hintergrund: Breiten mit < und > kennen Sie aus Aufgabe 2_016. Hinter
dem Doppelpunkt eines f-Strings kann noch mehr stehen. Ein Komma vor
dem Typ setzt Tausendertrennzeichen, ein % statt f nimmt den Wert mal
100, hängt das Prozentzeichen an und rundet auf die angegebene Zahl
von Nachkommastellen:

    f"{1234567:,}"         →  "1,234,567"
    f"{0.0425:.1%}"        →  "4.2%"
    f"[{9876:>8,}]"        →  "[   9,876]"
    f"[{0.5:>8.2%}]"       →  "[  50.00%]"

Die Reihenfolge ist immer Ausrichtung, Breite, Komma, Punkt mit
Nachkommastellen, Typ; die Breite zählt dabei alle Zeichen, auch die
Kommas und das Prozentzeichen. Für einen deutschen Bericht ersetzt
man hinterher die Zeichen: f"{1234567:,}".replace(",", ".") ergibt
"1.234.567". Rechnen Sie den Anteil nicht selbst in Prozent um und
runden nicht vorher mit round(): Das übernimmt % beim Formatieren.

Tipp: Bauen Sie bericht mit zeile auf, dann stimmen alle Spalten
automatisch überein.
"""

KOPF = "Abteilung            Dateien   Befund"


def zeile(abteilung, dateien, auffaellig):
    """Gibt eine Berichtszeile mit Tausendertrennzeichen und Prozentwert zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bericht(abteilungen):
    """Gibt die Kopfzeile, eine Zeile je Abteilung und die Gesamtzeile als Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


for text in bericht([("Vertrieb", 1234567, 1543), ("Labor", 48210, 1205)]):
    print(text)
