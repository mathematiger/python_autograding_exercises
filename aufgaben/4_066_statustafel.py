"""Aufgabe 4_066 – Statustafel                                   Stufe 4 ★★★★☆

In der Leitwarte eines Rechenzentrums hängt ein großer Bildschirm, auf
dem das Monitoring jede Minute den Zustand der Server zeigt. Das
Anzeigeprogramm kann nur reinen Text in einer Schrift mit fester
Zeichenbreite darstellen, deshalb muss jede Zeile genau ausgerichtet
sein:

    ======== Rechenzentrum Nord ========
    23.11.2026 09:05 web01.......   87.5 % +3.2
    23.11.2026 09:05 db-backup...    4.0 % -12.0

Schreiben Sie drei Funktionen, die Text zurückgeben:

- `ueberschrift(titel, breite)`: der Titel mit je einem Leerzeichen
  davor und dahinter, zentriert in einer Zeile der Länge breite und
  links und rechts mit "=" aufgefüllt. Bleibt eine ungerade Zahl von
  Zeichen übrig, steht das zusätzliche "=" rechts.
- `statuszeile(zeitpunkt, host, cpu, aenderung)`: der Zeitpunkt (ein
  datetime-Objekt) als TT.MM.JJJJ HH:MM, ein Leerzeichen, der Hostname
  linksbündig in 12 Zeichen mit Punkten aufgefüllt, ein Leerzeichen, die
  CPU-Last in Prozent rechtsbündig in 6 Zeichen mit einer
  Nachkommastelle, " % ", und die Änderung zur letzten Minute mit
  Vorzeichen (+ oder -) und einer Nachkommastelle.
- `wertespalte(werte, breite, stellen)`: eine Liste, in der jeder Wert
  rechtsbündig in breite Zeichen mit stellen Nachkommastellen steht.

    ueberschrift("Rechenzentrum Nord", 36)
    →  "======== Rechenzentrum Nord ========"
    statuszeile(datetime(2026, 11, 23, 9, 5), "web01", 87.46, 3.2)
    →  "23.11.2026 09:05 web01.......   87.5 % +3.2"
    wertespalte([3.14159, 42, -0.5], 8, 2)
    →  ["    3.14", "   42.00", "   -0.50"]

Benutzen Sie dafür Formatangaben in f-Strings oder format(), nicht
ljust, rjust, center oder strftime.

Grenzen: titel hat 1 bis 40 Zeichen, len(titel) + 2 ≤ breite ≤ 80. Der
Zeitpunkt liegt zwischen den Jahren 1000 und 9999. host hat 1 bis 12
Zeichen, cpu ist eine Kommazahl von 0 bis 100, aenderung eine Kommazahl
von -100 bis 100 mit höchstens einer Nachkommastelle (nicht -0.0). Bei
wertespalte sind die Werte ganze oder Kommazahlen von -10**6 bis 10**6,
es gibt 0 bis 10 000 davon, 1 ≤ breite ≤ 20 und 0 ≤ stellen ≤ 6.

Hintergrund: Was hinter dem Doppelpunkt eines f-Strings steht, heißt
Formatangabe (englisch format_spec). Breite, Ausrichtung mit < und >,
Nachkommastellen (Aufgabe 2_016) und Tausendertrennzeichen (Aufgabe
3_055) kennen Sie. Der vollständige Aufbau ist

    [[füllzeichen]ausrichtung][vorzeichen][breite][,][.stellen][typ]

    f"{'ab':*^8}"      →  "***ab***"    ^ zentriert, * füllt auf
    f"{'ab':.<6}"      →  "ab...."      ein Füllzeichen braucht eine Ausrichtung
    f"{7:+}"           →  "+7"          + zeigt das Vorzeichen immer
    f"{-7:+}"          →  "-7"
    f"{42:05d}"        →  "00042"       0 vor der Breite füllt mit Nullen

Bei ^ und einer ungeraden Zahl von Füllzeichen kommt das zusätzliche
rechts hin: f"{'ab':*^7}" ist "**ab***". Breite und Stellen dürfen
selbst wieder aus Variablen kommen, dafür schachtelt man geschweifte
Klammern in der Formatangabe:

    breite = 8
    stellen = 2
    f"{3.14159:>{breite}.{stellen}f}"   →  "    3.14"

Dasselbe kann die eingebaute Funktion format(wert, formatangabe), der
man die Angabe als Text gibt: format(3.14159, ">8.2f"). Eigene Klassen
bestimmen mit __format__ selbst, was ihre Formatangabe bedeutet, und
genau das tut datetime: Hinter dem Doppelpunkt stehen dort Platzhalter
mit %, die durch Teile des Zeitpunkts ersetzt werden, %d Tag, %m Monat,
%Y vierstelliges Jahr, %H Stunde (00 bis 23), %M Minute, jeweils mit
führender Null:

    from datetime import datetime
    zeit = datetime(2026, 3, 7, 8, 4)
    f"{zeit:%d.%m.%Y}"      →  "07.03.2026"
    f"{zeit:%H:%M Uhr}"     →  "08:04 Uhr"

Rechnen mit Datum und Zeit kommt in einer späteren Aufgabe.
"""

from datetime import datetime


def ueberschrift(titel, breite):
    """Gibt den Titel zentriert und mit "=" aufgefüllt in einer Zeile der Länge breite zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def statuszeile(zeitpunkt, host, cpu, aenderung):
    """Gibt eine Zeile der Statustafel mit Zeitpunkt, Host, CPU-Last und Änderung zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def wertespalte(werte, breite, stellen):
    """Gibt jeden Wert rechtsbündig in breite Zeichen mit stellen Nachkommastellen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(ueberschrift("Rechenzentrum Nord", 36))
print(statuszeile(datetime(2026, 11, 23, 9, 5), "web01", 87.46, 3.2))
print(statuszeile(datetime(2026, 11, 23, 9, 5), "db-backup", 4.0, -12.0))
print(wertespalte([3.14159, 42, -0.5], 8, 2))
