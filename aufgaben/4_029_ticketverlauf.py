"""Aufgabe 4_029 – Ticketverlauf                                 Stufe 4 ★★★★☆

Das Ticketsystem eines IT-Supports speichert zu jedem Ticket nicht den
aktuellen Zustand, sondern nur den Verlauf: eine Liste von Ereignissen in der
Reihenfolge, in der sie passiert sind. Die Eskalationsstufe gibt an, wer das
Ticket bearbeitet: 1 ist der First-Level-Support an der Hotline, 2 die
Fachabteilung, 3 der Hersteller; 0 heißt gelöst. Wie ein einzelnes Ereignis
die Stufe ändert, legt die vorgegebene Funktion `wende_an(stufe, ereignis)`
fest. Außerdem melden mehrere Standorte am Monatsende, wie viele Tickets sie
je Kategorie hatten, und die Zentrale braucht die Summen. Schreiben Sie mit
functools.reduce zwei Funktionen:

- `endstufe(ereignisse, start=1)` gibt die Stufe zurück, die sich ergibt,
  wenn man die Ereignisse nacheinander mit wende_an auf start anwendet. Ohne
  Ereignisse ist das start.
- `zusammenfuehren(zaehlungen)` bekommt eine Liste von Dictionaries
  kategorie → anzahl und gibt ein neues Dictionary mit der Summe je Kategorie
  zurück. Die Kategorien stehen in der Reihenfolge, in der sie zum ersten Mal
  vorkommen. Die übergebenen Dictionaries bleiben unverändert; bei leerer
  Liste kommt ein leeres Dictionary zurück.

    endstufe(["eskalieren", "eskalieren", "zurueckstufen"])   →  2
    endstufe(["loesen", "wiedereroeffnen"], start=3)         →  1
    endstufe([])                                             →  1
    zusammenfuehren([{"Drucker": 4, "Netz": 2}, {"Netz": 5, "Konto": 1}])
        →  {"Drucker": 4, "Netz": 7, "Konto": 1}

Grenzen: ereignisse hat 0 bis 100 000 Einträge, jeder ist einer der vier
Texte, die wende_an kennt; 0 ≤ start ≤ 3. zaehlungen hat 0 bis 2000
Dictionaries mit je 0 bis 20 Einträgen; insgesamt gibt es höchstens 50
verschiedene Kategorien, jede Anzahl ist eine ganze Zahl von 0 bis 10**6.
Benutzen Sie reduce in beiden Funktionen.

Hintergrund: Viele Auswertungen folgen demselben Muster: Man beginnt mit
einem Anfangswert und verrechnet die Elemente einer Folge der Reihe nach mit
dem bisherigen Ergebnis. Eine for-Schleife mit einer Variablen ergebnis tut
das, functools.reduce(funktion, folge, anfang) fasst es in einem Aufruf
zusammen. funktion bekommt zwei Argumente, das bisherige Ergebnis und das
nächste Element, und liefert das neue Ergebnis:

    from functools import reduce

    reduce(lambda summe, x: summe + x, [3, 5, 2], 0)
    # rechnet ((0 + 3) + 5) + 2  →  10

    def laengeres(bisher, wort):
        return wort if len(wort) > len(bisher) else bisher

    reduce(laengeres, ["Netz", "Drucker", "VPN"], "")   →  "Drucker"

Den Anfangswert sollte man fast immer angeben. Ohne ihn nimmt reduce das
erste Element als Anfang; bei einer leeren Folge gibt es dann einen
TypeError, und bei Dictionaries arbeitet die Funktion direkt mit dem ersten
übergebenen Objekt weiter. Verändert sie es, etwa mit bisher[k] += anzahl,
ist danach die Zählung des ersten Standorts verfälscht. Eine saubere
Verrechnungsfunktion baut darum ein neues Ergebnis, statt das alte zu
verändern; dict(bisher) legt eine Kopie an. Wenn die Verrechnung mehr als
einen Ausdruck braucht, schreibt man sie als eigene Funktion mit def statt
als lambda.
"""

from functools import reduce


def wende_an(stufe, ereignis):
    """Gibt die Eskalationsstufe nach einem Ereignis zurück (0 gelöst, 1 bis 3 offen)."""
    if ereignis == "loesen":
        return 0
    if ereignis == "wiedereroeffnen":
        return 1 if stufe == 0 else stufe
    if stufe == 0:
        return 0  # Ein gelöstes Ticket wird erst wiedereröffnet, bevor es eskaliert.
    if ereignis == "eskalieren":
        return min(stufe + 1, 3)
    if ereignis == "zurueckstufen":
        return max(stufe - 1, 1)
    raise ValueError(f"Unbekanntes Ereignis: {ereignis!r}")


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def endstufe(ereignisse, start=1):
    """Gibt die Eskalationsstufe nach allen Ereignissen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zusammenfuehren(zaehlungen):
    """Gibt ein neues Dictionary mit der Summe je Kategorie über alle Zählungen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(endstufe(["eskalieren", "eskalieren", "zurueckstufen"]))
print(zusammenfuehren([{"Drucker": 4, "Netz": 2}, {"Netz": 5, "Konto": 1}]))
