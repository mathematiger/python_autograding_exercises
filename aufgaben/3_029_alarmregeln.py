"""Aufgabe 3_029 – Alarmregeln                                   Stufe 3 ★★★☆☆

Ein Monitoring-System löst einen Alarm aus, sobald ein Messwert eines
Servers eine Schwelle über- oder unterschreitet. Welche Schwellen gelten,
schreibt das Betriebsteam in eine Regeldatei, eine Regel pro Zeile:

    cpu > 90
    temperatur > 75.5
    festplatte < 10

Jede Regel besteht aus drei Teilen, durch Leerzeichen getrennt: der
Messgröße, dem Vergleich (> oder <) und dem Schwellwert. Messgrößen sind
cpu und ram (Auslastung in Prozent), festplatte (freier Platz in Prozent)
und temperatur (in °C). "festplatte < 10" heißt also: Alarm, wenn weniger
als 10 Prozent des Plattenplatzes frei sind.

Bisher bricht das Einlesen beim ersten Tippfehler ab. Wer die Datei
pflegt, findet deshalb bei jedem Neustart nur einen Fehler. Künftig soll
das Einlesen die ganze Datei prüfen und alle Fehler auf einmal melden,
jeweils mit der Zeilennummer. Schreiben Sie zwei Funktionen:

- `lies_regel(zeile)` zerlegt eine Zeile mit split() und gibt ein Tupel
  (messgroesse, vergleich, schwellwert) zurück, den Schwellwert mit
  float(...) umgewandelt. Ist die Zeile fehlerhaft, löst sie einen
  ValueError aus. Sie prüft in dieser Reihenfolge:
  1. Liefert split() nicht genau drei Teile, lautet die Meldung
     "Erwartet: Messgröße Vergleich Schwellwert".
  2. Ist die Messgröße unbekannt, lautet sie zum Beispiel
     "Unbekannte Messgröße: gpu".
  3. Ist der Vergleich unbekannt, lautet sie zum Beispiel
     "Unbekannter Vergleich: >=".
  4. Ist der Schwellwert keine Zahl, löst float(...) selbst einen
     ValueError mit eigener Meldung aus. lies_regel prüft das nicht
     vorher und fängt diesen Fehler nicht ab, sondern lässt ihn durch.
- `lies_regeln(zeilen)` übergibt jede nicht leere Zeile an lies_regel und
  gibt ein Tupel (regeln, meldungen) zurück: die Liste der Tupel aller
  richtigen Regeln und eine Liste mit einer Meldung für jede fehlerhafte
  Zeile, in der Form "Zeile <nummer>: <Meldung des ValueError>", beide in
  der Reihenfolge der Zeilen. Die Zeilen zählen ab 1. Zeilen, die leer
  sind oder nur aus Leerzeichen bestehen, werden übersprungen, zählen bei
  der Zeilennummer aber mit. Fangen Sie nur den ValueError ab: Jede andere
  Ausnahme wäre ein Programmierfehler und soll weiterhin auffallen.

    lies_regel("cpu > 90")         →  ("cpu", ">", 90.0)
    lies_regel("gpu > 90")         →  ValueError: Unbekannte Messgröße: gpu
    lies_regel("cpu > neunzig")    →  ValueError: could not convert string to float: 'neunzig'
    lies_regeln(["cpu > 90", "", "ram >= 80", "temperatur > 75.5", "festplatte <"])
        →  ([("cpu", ">", 90.0), ("temperatur", ">", 75.5)],
            ["Zeile 3: Unbekannter Vergleich: >=",
             "Zeile 5: Erwartet: Messgröße Vergleich Schwellwert"])

Grenzen: 0 ≤ len(zeilen) ≤ 10 000, jede Zeile ist ein Text mit höchstens
50 Zeichen; als Leerraum kommen nur Leerzeichen vor, keine Tabulatoren.
Lässt sich ein Schwellwert umwandeln, liegt er zwischen -1000 und 1000;
Texte wie "nan", "inf" oder "1e3" kommen nicht vor.

Hintergrund: Eine Ausnahme, die eine Funktion nicht abfängt, verschwindet
nicht. Sie beendet die Funktion sofort und taucht beim Aufrufer wieder
auf, genau an der Stelle, an der er die Funktion aufgerufen hat. Fängt
auch er sie nicht ab, wandert sie weiter nach oben, bis das Programm
abbricht; diesen Weg zeigt der Traceback (Aufgabe 3_016). Man muss also
entscheiden, wo man eine Ausnahme abfängt, und zwar dort, wo man weiß,
wie es weitergeht. In Aufgabe 3_007 konnte die Hilfsfunktion das selbst:
Ein unbrauchbarer Wert wurde einfach None. Hier nicht: lies_regel sieht
nur eine Zeile und weiß weder ihre Nummer noch, ob das Einlesen
weiterlaufen soll. Deshalb meldet lies_regel Fehler nur, mit raise
(Aufgabe 3_009) oder indem sie den Fehler von float(...) durchlässt, und
fängt selbst nichts ab. lies_regeln kennt die Zeilennummer, fängt den
Fehler ab und sammelt die Meldungen. Wie in Aufgabe 3_009 kurz erwähnt,
kommt man mit except ... as name an die Ausnahme selbst heran, und
str(name) liefert ihre Meldung:

    def lies_prozent(text):
        wert = float(text)     # ValueError, wenn text keine Zahl ist
        if wert < 0 or wert > 100:
            raise ValueError("Kein Prozentwert: " + text)
        return wert

    try:
        anteil = lies_prozent("120")
    except ValueError as ausnahme:
        print("Abgelehnt:", str(ausnahme))     # Abgelehnt: Kein Prozentwert: 120

Mit lies_prozent("viel") käme der ValueError von float(...) in denselben
except-Block, und es erschiene "Abgelehnt: could not convert string to
float: 'viel'". Der Name hinter as gilt nur innerhalb des except-Blocks;
danach löscht Python ihn, auch wenn vorher eine andere Variable so hieß.
Nennen Sie ihn deshalb nicht so wie Ihre Liste der Meldungen.

Tipp: Die bekannten Messgrößen und Vergleiche stehen schon in den Tupeln
MESSGROESSEN und VERGLEICHE im Code. enumerate(zeilen, 1) liefert die
Zeilennummern ab 1 gleich mit (Aufgabe 2_021).
"""

MESSGROESSEN = ("cpu", "ram", "festplatte", "temperatur")
VERGLEICHE = (">", "<")


def lies_regel(zeile):
    """Zerlegt eine Regelzeile in das Tupel (messgroesse, vergleich, schwellwert)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def lies_regeln(zeilen):
    """Liest alle Regelzeilen und gibt das Tupel (regeln, meldungen) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


regeldatei = ["cpu > 90", "", "ram >= 80", "temperatur > 75.5", "festplatte <"]
gelesene_regeln, fehlermeldungen = lies_regeln(regeldatei)
print(len(gelesene_regeln), "Regeln gelesen")
for meldung in fehlermeldungen:
    print(meldung)
