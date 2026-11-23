# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_055_scanbericht.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_055_scanbericht

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
    return f"{abteilung:<14}{dateien:>14,}{auffaellig / dateien:>9.2%}"


def bericht(abteilungen):
    """Gibt die Kopfzeile, eine Zeile je Abteilung und die Gesamtzeile als Liste zurück."""
    zeilen = [KOPF]
    summe_dateien = 0
    summe_auffaellig = 0
    for abteilung, dateien, auffaellig in abteilungen:
        zeilen.append(zeile(abteilung, dateien, auffaellig))
        summe_dateien += dateien
        summe_auffaellig += auffaellig
    zeilen.append(zeile("Gesamt", summe_dateien, summe_auffaellig))
    return zeilen


for text in bericht([("Vertrieb", 1234567, 1543), ("Labor", 48210, 1205)]):
    print(text)


# Idee: Ein einziger f-String erledigt die Zeile: {abteilung:<14} linksbündig, {dateien:>14,} rechtsbündig
# mit Tausendertrennzeichen, {auffaellig / dateien:>9.2%} rechtsbündig als Prozent mit zwei Stellen.
# bericht beginnt mit KOPF, hängt für jedes Tupel zeile(...) an, zählt dabei beide Summen mit und hängt
# am Ende zeile("Gesamt", summe_dateien, summe_auffaellig) an.
# Anderer Weg: den Prozentwert als f"{auffaellig / dateien * 100:.2f}%" bauen und mit rjust(9) auffüllen,
# oder die Summen nach der Schleife mit sum(...) über eine Comprehension bilden.
# Typische Fehler: selbst mal 100 rechnen und dann noch % benutzen (ergibt 12.50% statt 0.12%), Komma
# und Breite vertauschen (:,>14 füllt mit Kommas auf statt Trennzeichen zu setzen), die Breite ohne Kommas und Prozentzeichen ausrechnen,
# vorher mit round() runden, die Gesamtquote als Mittelwert der Quoten statt aus den Summen bilden.
# Laufzeit: zeile braucht konstant viele Schritte, bericht O(n) für n Abteilungen.
