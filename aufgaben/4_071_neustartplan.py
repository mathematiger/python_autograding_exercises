"""Aufgabe 4_071 – Neustartplan                                  Stufe 4 ★★★★☆

Ein Hosting-Anbieter betreibt in seinem Rechenzentrum Server für viele
Kunden. Sicherheitsupdates für den Betriebssystemkern wirken erst nach
einem Neustart, deshalb ist mit den Kunden vereinbart: Kein Server
läuft länger als 30 Tage ohne Neustart. Neu gestartet wird nur im
Wartungsfenster, und das beginnt jeden Sonntag um 02:00 Uhr. Das
Monitoring meldet für jeden Server, wann er zuletzt gestartet wurde,
als Text in der Form TT.MM.JJJJ HH:MM. Daraus soll das Betriebsteam
jeden Montag sehen, welche Server in der kommenden Woche drankommen.

Schreiben Sie fünf Funktionen mit dem Modul datetime:

- `lies_zeit(text)` macht aus einem Text wie "02.11.2026 14:30" ein
  datetime-Objekt.
- `laufzeit(gestartet, jetzt)` gibt als timedelta zurück, wie lange der
  Server seit gestartet läuft.
- `als_text(dauer)` schreibt ein timedelta als "T d HH:MM": die ganzen
  Tage, ein Leerzeichen, ein d, ein Leerzeichen, dann Stunden und
  Minuten zweistellig. Sekunden fallen weg.
- `spaetester_neustart(gestartet)` gibt den Beginn des letzten
  Wartungsfensters (Sonntag 02:00) zurück, der nicht später als 30 Tage
  nach gestartet liegt. Fällt die Frist genau auf Sonntag 02:00, ist
  das schon das gesuchte Fenster.
- `faellig(startzeiten, jetzt)` bekommt ein Dictionary Servername →
  Startzeit als Text und gibt die Namen der Server zurück, deren
  spätester Neustart vor jetzt + 7 Tage liegt (auch die schon
  überfälligen), geordnet nach diesem Zeitpunkt, bei Gleichstand nach
  dem Namen.

    gestartet = lies_zeit("02.11.2026 14:30")      # ein Montag
    jetzt = datetime(2026, 11, 23, 9, 0)
    als_text(laufzeit(gestartet, jetzt))           →  "20 d 18:30"
    spaetester_neustart(gestartet)                 →  datetime(2026, 11, 29, 2, 0)
    startzeiten = {"web01": "02.11.2026 14:30", "db01": "28.10.2026 03:15",
                   "mail": "20.11.2026 22:00", "backup": "06.11.2026 02:00"}
    faellig(startzeiten, jetzt)                    →  ["db01", "web01"]

Die Frist von web01 endet am Mittwoch, 02.12.2026, 14:30; das letzte
Wartungsfenster davor ist Sonntag, 29.11. Bei backup endet sie genau am
Sonntag, 06.12., um 02:00, das ist nach dem 30.11. um 09:00.

Grenzen: Alle Zeiten liegen zwischen 2000 und 2099 und sind Ortszeit
ohne Zeitzone; die Sommerzeit spielt keine Rolle. Die Texte haben genau
die Form TT.MM.JJJJ HH:MM mit gültigem Datum. gestartet liegt nicht
nach jetzt, also ist eine Laufzeit nie negativ; sie ist höchstens
36 500 Tage lang und darf Sekunden enthalten. startzeiten hat 0 bis
10 000 Einträge.

Hintergrund: In Aufgabe 3_054 haben Sie ein Datum noch von Hand zerlegt
und geprüft, in Aufgabe 4_066 ein datetime-Objekt im f-String
formatiert. Das Modul datetime kann aber auch rechnen. Ein datetime ist
ein Zeitpunkt, ein timedelta eine Zeitspanne. Zieht man zwei
Zeitpunkte voneinander ab, erhält man eine Zeitspanne; zählt man eine
Zeitspanne zu einem Zeitpunkt hinzu, erhält man wieder einen Zeitpunkt.
Monatslängen, Schaltjahre (Aufgabe 2_051) und Jahreswechsel erledigt
datetime dabei selbst:

    from datetime import datetime, timedelta

    beginn = datetime(2026, 12, 30, 22, 0)
    ende = beginn + timedelta(days=2, hours=5)    →  datetime(2027, 1, 2, 3, 0)
    spanne = ende - beginn                        →  timedelta(days=2, seconds=18000)
    spanne.days, spanne.seconds                   →  (2, 18000)
    spanne.total_seconds()                        →  190800.0
    ende > beginn                                 →  True

Ein timedelta speichert intern nur Tage, Sekunden (0 bis 86 399) und
Mikrosekunden; Stunden und Minuten rechnet man aus spanne.seconds mit
// und % (Aufgabe 1_005) heraus. Zeitpunkte lassen sich mit <, > und
sorted vergleichen wie Zahlen.

Aus einem Text macht datetime.strptime(text, format) einen Zeitpunkt;
das Format benutzt dieselben Platzhalter wie beim Ausgeben, %d Tag, %m
Monat, %Y Jahr mit vier Stellen, %H Stunde, %M Minute. Ein falsches
Datum wie der 31.04. ergibt einen ValueError:

    datetime.strptime("07.03.2026 08:04", "%d.%m.%Y %H:%M")
    →  datetime(2026, 3, 7, 8, 4)

Für Wochentage gibt zeit.weekday() eine Zahl von 0 (Montag) bis 6
(Sonntag) zurück. zeit.replace(hour=2, minute=0) gibt eine Kopie mit
geänderten Feldern zurück; datetime-Objekte selbst sind unveränderlich.
Um vom Tag x zum letzten Sonntag zu kommen, zieht man so viele Tage ab,
wie seit Sonntag vergangen sind: (x.weekday() + 1) % 7. Wer das
Wartungsfenster auf diesem Sonntag nimmt, muss noch prüfen, ob es nicht
nach der Frist liegt; dann ist es eine Woche früher.
"""

from datetime import datetime, timedelta

HOECHSTE_LAUFZEIT = timedelta(days=30)
VORLAUF = timedelta(days=7)


def lies_zeit(text):
    """Wandelt einen Text der Form TT.MM.JJJJ HH:MM in ein datetime um."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def laufzeit(gestartet, jetzt):
    """Gibt die Zeitspanne von gestartet bis jetzt zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def als_text(dauer):
    """Schreibt eine Zeitspanne als "T d HH:MM"."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def spaetester_neustart(gestartet):
    """Gibt den Beginn des letzten Wartungsfensters (Sonntag 02:00) bis zur Frist zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def faellig(startzeiten, jetzt):
    """Gibt die Server zurück, die vor jetzt + VORLAUF neu gestartet werden müssen, nach Zeitpunkt geordnet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


jetzt = datetime(2026, 11, 23, 9, 0)
gestartet = lies_zeit("02.11.2026 14:30")
print(als_text(laufzeit(gestartet, jetzt)))
print(spaetester_neustart(gestartet))
startzeiten = {
    "web01": "02.11.2026 14:30",
    "db01": "28.10.2026 03:15",
    "mail": "20.11.2026 22:00",
    "backup": "06.11.2026 02:00",
}
print(faellig(startzeiten, jetzt))
