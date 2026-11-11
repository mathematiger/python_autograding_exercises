"""Aufgabe 3_031 – Abfrageversuche                               Stufe 3 ★★★☆☆

Eine Webanwendung holt ihre Daten aus einer Datenbank, die auf einem
anderen Server läuft. Meistens klappt jede Abfrage sofort. Ab und zu ist
aber das Netz kurz überlastet oder die Datenbank startet gerade neu. Dann
scheitert die Abfrage mit einem TimeoutError oder einem ConnectionError,
obwohl sie einen Augenblick später geklappt hätte. Solche vorübergehenden
Fehler soll die Anwendung nicht sofort melden, sondern die Abfrage noch
einmal versuchen. Andere Fehler, etwa ein Tippfehler in der Abfrage
(ValueError) oder eine fehlende Spalte (KeyError), gehen durch einen neuen
Versuch nicht weg; sie sollen sofort beim Aufrufer ankommen.

Schreiben Sie die Funktion `mit_wiederholung(abfrage, versuche, protokoll)`.
abfrage ist eine Funktion ohne Parameter, die ihr Ergebnis zurückgibt oder
eine Ausnahme auslöst; mit_wiederholung bekommt sie als Argument und ruft
sie mit abfrage() auf (Funktionen als Argumente, Aufgabe 3_028). versuche
ist die Zahl der Aufrufe, die höchstens erlaubt sind, protokoll eine Liste.

- mit_wiederholung ruft abfrage auf und gibt deren Ergebnis zurück, sobald
  ein Aufruf klappt.
- Scheitert ein Aufruf mit einem TimeoutError oder einem ConnectionError
  (auch einer Art darunter, etwa ConnectionRefusedError), hängt sie den
  Text "Versuch <k>: <Meldung der Ausnahme>" an protokoll an; k zählt die
  Aufrufe ab 1. Dann versucht sie es noch einmal, solange noch Versuche
  übrig sind.
- Scheitert auch der letzte erlaubte Versuch, gibt sie auf: Nach dem
  Eintrag ins Protokoll reicht sie genau die Ausnahme dieses letzten
  Versuchs an den Aufrufer weiter, unverändert.
- Jede andere Ausnahme reicht sie sofort weiter, ohne neuen Versuch und
  ohne Eintrag ins Protokoll.

    protokoll = []
    mit_wiederholung(lies_kunden, 3, protokoll)   →  ["Ada", "Ben"]
    protokoll   →  ["Versuch 1: keine Antwort nach 5 s"]

lies_kunden steht unten im Code: Beim ersten Aufruf löst sie
TimeoutError("keine Antwort nach 5 s") aus, beim zweiten liefert sie die
Liste ["Ada", "Ben"].

Grenzen: 1 ≤ versuche ≤ 10. protokoll kann schon Einträge haben; neue
kommen ans Ende. abfrage gibt einen beliebigen Wert zurück, auch [], 0
oder None, oder löst eine Ausnahme mit einer kurzen Meldung aus.

Hintergrund: Manchmal will man auf einen Fehler reagieren, etwa ihn
protokollieren, kann ihn aber nicht beheben. Dann fängt man die Ausnahme
ab, tut, was nötig ist, und reicht sie mit einem bloßen raise weiter:

    try:
        daten = lies_datei()
    except FileNotFoundError as ausnahme:
        protokoll.append("Datei fehlt: " + str(ausnahme))
        raise

raise ohne Argument löst im except-Block genau die Ausnahme noch einmal
aus, die gerade behandelt wird: dasselbe Objekt mit derselben Art,
derselben Meldung und demselben Traceback (Aufgabe 3_016). Für den
Aufrufer sieht es so aus, als hätte man sie nie abgefangen. raise
TimeoutError(str(ausnahme)) wäre dagegen eine neue Ausnahme: Aus einem
ConnectionResetError würde so ein TimeoutError, und der Traceback meldete
zwei Fehler ("During handling of the above exception, another exception
occurred"), als wäre im except-Block selbst etwas schiefgegangen.

TimeoutError und ConnectionError gehören beide zu OSError (Aufgabe 3_030),
aber nicht jeder OSError geht von selbst wieder weg: Eine fehlende Datei
(FileNotFoundError) fehlt auch beim zweiten Versuch. Fangen Sie deshalb
genau diese beiden Arten ab, in einem except mit Tupel (Aufgabe 2_035).
Auch ein Verbindungsfehler kann bleiben, etwa bei einem falschen Port;
deshalb ist die Zahl der Versuche begrenzt.

Zwei Dinge machen echte Programme zusätzlich. Sie warten zwischen zwei
Versuchen kurz, oft jedes Mal doppelt so lange wie zuvor; ohne Pause wären
bei einem Neustart der Datenbank alle Versuche nach Sekundenbruchteilen
verbraucht. Das entfällt hier, damit die Tests schnell bleiben. Und sie
wiederholen so nur Abfragen, die bloß lesen: Bei einer Buchung weiß man
nach einem Timeout nicht, ob sie schon ausgeführt wurde, und ein zweiter
Versuch bucht womöglich doppelt.

Tipp: Eine for-Schleife über die Versuchsnummern 1 bis versuche; im
try-Block steht return abfrage(). Im except-Block schreiben Sie ins
Protokoll und prüfen, ob es der letzte Versuch war.
"""

bisherige_aufrufe = []


def lies_kunden():
    """Fragt die Kundentabelle ab; beim ersten Aufruf antwortet die Datenbank nicht."""
    bisherige_aufrufe.append("lies_kunden")
    if len(bisherige_aufrufe) == 1:
        raise TimeoutError("keine Antwort nach 5 s")
    return ["Ada", "Ben"]


def mit_wiederholung(abfrage, versuche, protokoll):
    """Ruft abfrage auf und wiederholt den Aufruf bei vorübergehenden Fehlern, höchstens versuche-mal."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kundenprotokoll = []
print(mit_wiederholung(lies_kunden, 3, kundenprotokoll))
print(kundenprotokoll)
