"""Aufgabe 3_009 – RAID-Kapazität                                Stufe 3 ★★★☆☆

Ein Server im Rechenzentrum speichert seine Daten nicht auf einer
einzelnen Festplatte, sondern auf mehreren, die zu einem RAID verbunden
sind. Je nach RAID-Level wird ein Teil des Platzes für Kopien oder
Prüfdaten verwendet, damit beim Ausfall einer Platte nichts verloren geht.
Wie viel Platz nutzbar bleibt, hängt vom Level, der Zahl der Platten und
ihrer Größe in Terabyte (TB) ab; alle Platten sind gleich groß:

    Level   nutzbare Kapazität          mindestens
    0       anzahl * groesse            2 Platten
    1       groesse                     2 Platten
    5       (anzahl - 1) * groesse      3 Platten
    6       (anzahl - 2) * groesse      4 Platten

Ein Planungswerkzeug soll die nutzbare Kapazität ausrechnen. Bei falschen
Angaben darf es aber kein Ergebnis liefern, das niemand bemerkt, etwa 0 TB
für ein RAID 6 mit zwei Platten. Schreiben Sie die Funktion
`nutzkapazitaet(level, anzahl, groesse)`, die zuerst ihre Vorbedingungen
prüft und bei einem Verstoß einen ValueError auslöst:

- Ist das Level nicht 0, 1, 5 oder 6, lautet die Meldung zum Beispiel
  "Unbekanntes RAID-Level: 3".
- Sind es zu wenige Platten für das Level, nennt die Meldung die
  Mindestzahl, zum Beispiel "RAID 6 braucht mindestens 4 Platten".
- Ist die Größe 0 oder negativ, lautet sie "Die Plattengröße muss positiv
  sein".

Sind alle Angaben in Ordnung, gibt die Funktion die nutzbare Kapazität in
TB zurück.

    nutzkapazitaet(5, 4, 8)    →  24
    nutzkapazitaet(1, 2, 4)    →  4
    nutzkapazitaet(6, 2, 8)    →  ValueError: RAID 6 braucht mindestens 4 Platten
    nutzkapazitaet(3, 4, 8)    →  ValueError: Unbekanntes RAID-Level: 3

Grenzen: level und anzahl sind ganze Zahlen mit -10 ≤ level ≤ 10 und
0 ≤ anzahl ≤ 100; groesse ist eine ganze Zahl oder Kommazahl mit
-100 ≤ groesse ≤ 100. Welche Meldung kommt, wenn mehrere Angaben falsch
sind, legt die Aufgabe nur für Level und Anzahl fest: das Level zuerst.

Hintergrund: Bisher haben Sie Ausnahmen nur abgefangen (Aufgaben 3_007
und 3_008). Mit raise löst man selbst eine aus:

    if anzahl < 0:
        raise ValueError("Die Anzahl darf nicht negativ sein")

raise beendet die Funktion sofort, so wie return, aber ohne
Rückgabewert: Der Aufrufer bekommt die Ausnahme und muss sie mit
try/except behandeln, sonst bricht das Programm ab. Der Text in den
Klammern ist die Fehlermeldung; man kommt im except-Block mit
except ValueError as fehler und str(fehler) an ihn heran. Eine Funktion,
die ihre Vorbedingungen gleich am Anfang prüft, meldet einen Fehler dort,
wo er entsteht, statt mit falschen Werten weiterzurechnen. ValueError ist
die passende Ausnahme, wenn ein Argument den richtigen Typ, aber einen
unzulässigen Wert hat. Eine gute Meldung sagt, welcher Wert falsch war
oder welcher richtig wäre, damit man den Fehler ohne Rätselraten findet.

Tipp: Ein Dictionary von Level zur Mindestzahl der Platten erspart viele
if-Abfragen. Prüfen Sie das Level vor der Anzahl.
"""


def nutzkapazitaet(level, anzahl, groesse):
    """Gibt die nutzbare Kapazität eines RAID in TB zurück; löst bei unzulässigen Angaben ValueError aus."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


for level, anzahl, groesse in [(5, 4, 8), (1, 2, 4), (6, 2, 8), (3, 4, 8)]:
    try:
        print(f"RAID {level} mit {anzahl} x {groesse} TB:", nutzkapazitaet(level, anzahl, groesse), "TB")
    except ValueError as fehler:
        print(f"RAID {level} mit {anzahl} x {groesse} TB: Fehler –", fehler)
