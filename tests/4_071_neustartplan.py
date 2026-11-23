# Automatisch erzeugt aus lehrkraft/muster/4_071_neustartplan.py - nicht von Hand ändern.
# vorlage-hash: edeb4dbe5edeb7d3
# text-hash: 2fd9c5f705b9175f
# thema: texte_zahlen
# inhalt: datetime und timedelta, Fristen

JETZT = datetime(2026, 11, 23, 9, 0)
STARTZEITEN = {
    "web01": "02.11.2026 14:30",
    "db01": "28.10.2026 03:15",
    "mail": "20.11.2026 22:00",
    "backup": "06.11.2026 02:00",
}


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_fenster(gestartet):
    """Vergleichslösung: geht von der Frist aus Tag für Tag zurück, bis ein Sonntag 02:00 nicht danach liegt."""
    frist = gestartet + timedelta(days=30)
    for zurueck in range(8):
        tag = frist - timedelta(days=zurueck)
        fenster = datetime(tag.year, tag.month, tag.day, 2, 0)
        if fenster.weekday() == 6 and fenster <= frist:
            return fenster
    return None


def vergleich_text(dauer):
    """Vergleichslösung für als_text über die Gesamtzahl der Minuten."""
    minuten = int(dauer.total_seconds()) // 60
    return f"{minuten // 1440} d {minuten % 1440 // 60:02d}:{minuten % 60:02d}"


def vergleich_faellig(startzeiten, jetzt):
    """Vergleichslösung für faellig, ohne strptime."""
    termine = []
    for name, text in startzeiten.items():
        tag, monat, rest = text.split(".")
        jahr, uhrzeit = rest.split(" ")
        stunde, minute = uhrzeit.split(":")
        termin = vergleich_fenster(datetime(int(jahr), int(monat), int(tag), int(stunde), int(minute)))
        if termin < jetzt + timedelta(days=7):
            termine.append((termin, name))
    return [name for termin, name in sorted(termine)]


def zufallszeit(zufall):
    """Erzeugt einen zufälligen Zeitpunkt auf die Minute genau zwischen 2000 und 2098."""
    beginn = datetime(2000, 1, 1)
    return beginn + timedelta(minutes=zufall.randint(0, 99 * 365 * 1440))


def meldung(funktion, argumente, erwartet, hinweis=""):
    """Prüft funktion(*argumente) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, *argumente)
    gezeigt = ", ".join(repr(argument) for argument in argumente)
    if len(gezeigt) > 300:
        gezeigt = f"<{len(argumente[0])} Server>, {argumente[1]!r}"
    text = f"{funktion.__name__}({gezeigt})\nergibt   {ergebnis!r}\nerwartet {erwartet!r}{hinweis}"
    return ergebnis == erwartet, text


# lies_zeit: das Beispiel
stimmt, text = meldung(
    lies_zeit, ["02.11.2026 14:30"], datetime(2026, 11, 2, 14, 30),
    '\nTipp: datetime.strptime(text, "%d.%m.%Y %H:%M").',
)
assert stimmt, text

# lies_zeit: ein anderer Zeitpunkt (nicht fest hinschreiben!)
stimmt, text = meldung(lies_zeit, ["29.02.2028 00:05"], datetime(2028, 2, 29, 0, 5))
assert stimmt, text

# lies_zeit: ein ungültiges Datum ergibt einen ValueError
try:
    lies_zeit("31.04.2026 10:00")
    fehlerart = "kein Fehler"
except Exception as fehler:
    fehlerart = type(fehler).__name__
assert fehlerart == "ValueError", (
    f'lies_zeit("31.04.2026 10:00") ergibt {fehlerart}, erwartet war ein ValueError, denn der April hat 30 Tage.'
)

# laufzeit: das Beispiel
stimmt, text = meldung(
    laufzeit, [datetime(2026, 11, 2, 14, 30), JETZT], timedelta(days=20, hours=18, minutes=30),
    "\nTipp: Zwei datetime-Objekte kann man voneinander abziehen: jetzt - gestartet.",
)
assert stimmt, text

# laufzeit: über den Jahreswechsel
stimmt, text = meldung(laufzeit, [datetime(2026, 12, 30, 22, 0), datetime(2027, 1, 2, 3, 0)], timedelta(days=2, hours=5))
assert stimmt, text

# laufzeit: gerade erst gestartet
stimmt, text = meldung(laufzeit, [JETZT, JETZT], timedelta(0))
assert stimmt, text

# als_text: das Beispiel, Inhalt
ergebnis = wert_von(als_text, timedelta(days=20, hours=18, minutes=30))
assert isinstance(ergebnis, str) and vergleichbar(ergebnis).replace(":", "") == vergleichbar("20 d 18 30"), (
    f"als_text(timedelta(days=20, hours=18, minutes=30)) ergibt {ergebnis!r}, erwartet war '20 d 18:30'.\n"
    "Tipp: dauer.days sind die ganzen Tage; Stunden und Minuten stecken in dauer.seconds."
)

# als_text: das Beispiel, genaue Form
stimmt, text = meldung(als_text, [timedelta(days=20, hours=18, minutes=30)], "20 d 18:30")
assert stimmt, text

# als_text: Stunden und Minuten zweistellig
stimmt, text = meldung(
    als_text, [timedelta(days=3, hours=4, minutes=5)], "3 d 04:05",
    "\nTipp: {stunden:02d} schreibt eine Zahl mit mindestens zwei Stellen, vorn mit 0 aufgefüllt.",
)
assert stimmt, text

# als_text: Sekunden fallen weg
stimmt, text = meldung(
    als_text, [timedelta(hours=1, minutes=59, seconds=59)], "0 d 01:59",
    "\nTipp: Runden Sie nicht, sondern teilen Sie ganzzahlig mit //.",
)
assert stimmt, text

# als_text: mehr als 24 Stunden werden zu Tagen
stimmt, text = meldung(
    als_text, [timedelta(hours=50)], "2 d 02:00",
    "\nTipp: dauer.seconds enthält nur den Rest unter einem Tag; die ganzen Tage stehen in dauer.days.",
)
assert stimmt, text

# als_text: keine Laufzeit
stimmt, text = meldung(als_text, [timedelta(0)], "0 d 00:00")
assert stimmt, text

# spaetester_neustart: das Beispiel
stimmt, text = meldung(
    spaetester_neustart, [datetime(2026, 11, 2, 14, 30)], datetime(2026, 11, 29, 2, 0),
    "\nTipp: Die Frist ist gestartet + timedelta(days=30); gehen Sie von dort zum letzten Sonntag zurück.",
)
assert stimmt, text

# spaetester_neustart: ein anderer Start
stimmt, text = meldung(spaetester_neustart, [datetime(2026, 10, 28, 3, 15)], datetime(2026, 11, 22, 2, 0))
assert stimmt, text

# spaetester_neustart: Frist genau Sonntag 02:00
stimmt, text = meldung(
    spaetester_neustart, [datetime(2026, 11, 6, 2, 0)], datetime(2026, 12, 6, 2, 0),
    "\nTipp: Fällt die Frist genau auf den Beginn eines Wartungsfensters, zählt dieses Fenster noch.",
)
assert stimmt, text

# spaetester_neustart: Frist sonntags kurz vor 02:00
stimmt, text = meldung(
    spaetester_neustart, [datetime(2026, 11, 6, 1, 59)], datetime(2026, 11, 29, 2, 0),
    "\nTipp: Liegt das Fenster am Tag der Frist nach der Frist, ist es eine Woche früher.",
)
assert stimmt, text

# spaetester_neustart: Frist sonntags nach 02:00
stimmt, text = meldung(spaetester_neustart, [datetime(2026, 11, 6, 23, 0)], datetime(2026, 12, 6, 2, 0))
assert stimmt, text

# spaetester_neustart: Frist an einem Samstag
stimmt, text = meldung(spaetester_neustart, [datetime(2026, 11, 5, 12, 0)], datetime(2026, 11, 29, 2, 0))
assert stimmt, text

# spaetester_neustart: Sekunden beim Start spielen keine Rolle
stimmt, text = meldung(spaetester_neustart, [datetime(2026, 11, 2, 14, 30, 17)], datetime(2026, 11, 29, 2, 0))
assert stimmt, text

# spaetester_neustart: über den Jahreswechsel
stimmt, text = meldung(spaetester_neustart, [datetime(2027, 12, 20, 8, 0)], datetime(2028, 1, 16, 2, 0))
assert stimmt, text

# spaetester_neustart: über den 29. Februar
stimmt, text = meldung(spaetester_neustart, [datetime(2028, 2, 1, 8, 0)], datetime(2028, 2, 27, 2, 0))
assert stimmt, text

# faellig: das Beispiel
stimmt, text = meldung(
    faellig, [dict(STARTZEITEN), JETZT], ["db01", "web01"],
    "\nTipp: Sammeln Sie Paare (termin, name) und sortieren Sie sie; Tupel werden Element für Element verglichen.",
)
assert stimmt, text

# faellig: eine Woche später sind mehr Server dran
stimmt, text = meldung(faellig, [dict(STARTZEITEN), JETZT + timedelta(days=7)], ["db01", "web01", "backup"])
assert stimmt, text

# faellig: genau an der Grenze zählt nicht mehr
stimmt, text = meldung(
    faellig, [{"a": "06.11.2026 02:00"}, datetime(2026, 11, 29, 2, 0)], [],
    "\nTipp: Gesucht sind Termine vor jetzt + 7 Tage (<, nicht <=).",
)
assert stimmt, text

# faellig: bei gleichem Termin nach dem Namen
stimmt, text = meldung(
    faellig, [{"zeta": "02.11.2026 14:30", "alpha": "03.11.2026 08:00"}, JETZT], ["alpha", "zeta"],
)
assert stimmt, text

# faellig: keine Server
stimmt, text = meldung(faellig, [{}, JETZT], [])
assert stimmt, text

# Die Ausgabe des Programms
erwartet = "20 d 18:30\n2026-11-29 02:00:00\n['db01', 'web01']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Startzeiten
zufall = Zufall(4071)
for _ in range(400):
    gestartet = zufallszeit(zufall)
    stimmt, text = meldung(spaetester_neustart, [gestartet], vergleich_fenster(gestartet))
    assert stimmt, text
    dauer = timedelta(seconds=zufall.randint(0, 36500 * 86400))
    stimmt, text = meldung(als_text, [dauer], vergleich_text(dauer))
    assert stimmt, text

# Viele zufällige Serverlisten
for _ in range(100):
    jetzt = datetime(2026, 11, 23, 9, 0) + timedelta(minutes=zufall.randint(0, 100000))
    startzeiten = {}
    for nummer in range(zufall.randint(0, 6)):
        start = jetzt - timedelta(minutes=zufall.randint(0, 40 * 1440))
        startzeiten[f"srv{nummer:02d}"] = f"{start:%d.%m.%Y %H:%M}"
    stimmt, text = meldung(faellig, [startzeiten, jetzt], vergleich_faellig(startzeiten, jetzt))
    assert stimmt, text

# Obere Grenze: 10 000 Server
startzeiten = {}
for nummer in range(10000):
    start = JETZT - timedelta(minutes=zufall.randint(0, 40 * 1440))
    startzeiten[f"srv{nummer:05d}"] = f"{start:%d.%m.%Y %H:%M}"
stimmt, text = meldung(faellig, [startzeiten, JETZT], vergleich_faellig(startzeiten, JETZT))
assert stimmt, text.split("\n")[0][:300]

# Obere Grenze: die längste Laufzeit
stimmt, text = meldung(als_text, [timedelta(days=36500, hours=23, minutes=59, seconds=59)], "36500 d 23:59")
assert stimmt, text
