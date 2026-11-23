# Automatisch erzeugt aus lehrkraft/muster/4_066_statustafel.py - nicht von Hand ändern.
# vorlage-hash: 0d7cee231f147c16
# text-hash: 980349f4630966b7
# thema: texte_zahlen
# inhalt: format_spec, Ausrichtung, Datum

from decimal import ROUND_HALF_EVEN, Decimal

ZEIT = datetime(2026, 11, 23, 9, 5)


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_ueberschrift(titel, breite):
    """Vergleichslösung: rechnet die Füllzeichen links und rechts von Hand aus."""
    rest = breite - len(titel) - 2
    links = rest // 2
    return "=" * links + " " + titel + " " + "=" * (rest - links)


def zweistellig(zahl):
    """Schreibt eine Zahl mit führender Null zweistellig."""
    return str(zahl).zfill(2)


def vergleich_zeile(zeitpunkt, host, cpu, aenderung):
    """Vergleichslösung mit zfill, ljust und rjust statt Formatangaben."""
    datum = f"{zweistellig(zeitpunkt.day)}.{zweistellig(zeitpunkt.month)}.{zeitpunkt.year}"
    uhrzeit = f"{zweistellig(zeitpunkt.hour)}:{zweistellig(zeitpunkt.minute)}"
    vorzeichen = "+" if aenderung >= 0 else "-"
    return (
        f"{datum} {uhrzeit} " + host.ljust(12, ".") + " " + str(round(cpu, 1)).rjust(6) + " % "
        + vorzeichen + str(abs(aenderung))
    )


def vergleich_spalte(werte, breite, stellen):
    """Vergleichslösung: rundet exakt mit Decimal und füllt mit rjust auf."""
    raster = Decimal(1).scaleb(-stellen)
    return [str(Decimal(wert).quantize(raster, rounding=ROUND_HALF_EVEN)).rjust(breite) for wert in werte]


def meldung(funktion, vergleich, *argumente, hinweis=""):
    """Vergleicht funktion mit vergleich; liefert (stimmt, Meldung) mit sichtbaren Rändern."""
    ergebnis = wert_von(funktion, *argumente)
    erwartet = vergleich(*argumente)
    gezeigt = ", ".join(repr(argument) for argument in argumente)
    text = f"{funktion.__name__}({gezeigt}) ergibt\n  {ergebnis!r}\nerwartet war\n  {erwartet!r}{hinweis}"
    return ergebnis == erwartet, text


# ueberschrift: der Titel steht mit Leerzeichen darin
ergebnis = wert_von(ueberschrift, "Rechenzentrum Nord", 36)
assert isinstance(ergebnis, str) and " Rechenzentrum Nord " in ergebnis, (
    f"ueberschrift('Rechenzentrum Nord', 36) ergibt {ergebnis!r}; darin fehlt ' Rechenzentrum Nord '."
)

# ueberschrift: das Beispiel
stimmt, text = meldung(
    ueberschrift, vergleich_ueberschrift, "Rechenzentrum Nord", 36,
    hinweis="\nTipp: Mit :=^36 wird zentriert und mit = aufgefüllt; das Leerzeichen gehört zum Text.",
)
assert stimmt, text

# ueberschrift: andere Breite aus einer Variablen (nicht fest hinschreiben!)
stimmt, text = meldung(
    ueberschrift, vergleich_ueberschrift, "Nord", 20,
    hinweis="\nTipp: Die Breite kommt aus der Variablen: {...:=^{breite}}.",
)
assert stimmt, text

# ueberschrift: ungerader Rest, das zusätzliche = rechts
stimmt, text = meldung(ueberschrift, vergleich_ueberschrift, "Süd", 12)
assert stimmt, text

# ueberschrift: genau so breit wie der Titel mit Leerzeichen
stimmt, text = meldung(ueberschrift, vergleich_ueberschrift, "Lager", 7)
assert stimmt, text

# statuszeile: Datum und Uhrzeit vorn
ergebnis = wert_von(statuszeile, ZEIT, "web01", 87.46, 3.2)
assert isinstance(ergebnis, str) and ergebnis.startswith("23.11.2026 09:05 "), (
    f"statuszeile(datetime(2026, 11, 23, 9, 5), ...) ergibt {ergebnis!r}; vorn erwartet war '23.11.2026 09:05 '.\n"
    "Tipp: f'{zeitpunkt:%d.%m.%Y %H:%M}' schreibt Tag, Monat, Jahr, Stunde und Minute mit führenden Nullen."
)

# statuszeile: der Host mit Punkten aufgefüllt
assert "web01....... " in ergebnis, (
    f"In {ergebnis!r} fehlt 'web01....... ' (der Host in 12 Zeichen mit Punkten).\n"
    "Tipp: Das Füllzeichen steht vor der Ausrichtung: {host:.<12}."
)

# statuszeile: CPU-Last rechtsbündig mit einer Nachkommastelle
assert "   87.5 % " in ergebnis, (
    f"In {ergebnis!r} fehlt '   87.5 % ' (87.46 rechtsbündig in 6 Zeichen mit einer Nachkommastelle)."
)

# statuszeile: das Beispiel mit Vorzeichen
stimmt, text = meldung(
    statuszeile, vergleich_zeile, ZEIT, "web01", 87.46, 3.2,
    hinweis="\nTipp: Mit + in der Formatangabe ({aenderung:+.1f}) steht auch vor positiven Zahlen ein Vorzeichen.",
)
assert stimmt, text

# statuszeile: negative Änderung und anderer Host
stimmt, text = meldung(statuszeile, vergleich_zeile, ZEIT, "db-backup", 4.0, -12.0)
assert stimmt, text

# statuszeile: Änderung 0 bekommt ein Plus
stimmt, text = meldung(statuszeile, vergleich_zeile, datetime(2027, 1, 2, 0, 0), "mail", 0.0, 0.0)
assert stimmt, text

# statuszeile: Höchstwerte 100 % und Hostname mit 12 Zeichen
stimmt, text = meldung(statuszeile, vergleich_zeile, datetime(2026, 12, 31, 23, 59), "monitoring01", 100.0, -100.0)
assert stimmt, text

# wertespalte: das Beispiel
ergebnis = wert_von(wertespalte, [3.14159, 42, -0.5], 8, 2)
assert ergebnis == ["    3.14", "   42.00", "   -0.50"], (
    f"wertespalte([3.14159, 42, -0.5], 8, 2) ergibt {ergebnis!r}, erwartet war ['    3.14', '   42.00', '   -0.50'].\n"
    "Tipp: Breite und Stellen aus Variablen: f'{wert:>{breite}.{stellen}f}'."
)

# wertespalte: andere Breite und Stellen
stimmt, text = meldung(wertespalte, vergleich_spalte, [1.5, 2.25], 5, 1)
assert stimmt, text

# wertespalte: keine Nachkommastellen
stimmt, text = meldung(wertespalte, vergleich_spalte, [7, 12.4, 99.6], 4, 0)
assert stimmt, text

# wertespalte: Breite kleiner als die Zahl, dann wird nichts abgeschnitten
stimmt, text = meldung(wertespalte, vergleich_spalte, [123456.789], 3, 2)
assert stimmt, text

# wertespalte: leere Liste
stimmt, text = meldung(wertespalte, vergleich_spalte, [], 8, 2)
assert stimmt, text

# Ohne ljust, rjust, center und strftime
verboten = [name for name in ["ljust", "rjust", "center", "strftime"] if verwendet(name)]
assert verboten == [], f"Ihr Code verwendet {verboten}. Lösen Sie die Aufgabe mit Formatangaben."

# Die Ausgabe des Programms
erwartet = "\n".join([
    vergleich_ueberschrift("Rechenzentrum Nord", 36),
    vergleich_zeile(ZEIT, "web01", 87.46, 3.2),
    vergleich_zeile(ZEIT, "db-backup", 4.0, -12.0),
    str(vergleich_spalte([3.14159, 42, -0.5], 8, 2)),
])
assert AUSGABE.strip() == erwartet, f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Überschriften
zufall = Zufall(4066)
for _ in range(500):
    titel = "".join(zufall.choice("abc XYZ-") for _ in range(zufall.randint(1, 40)))
    stimmt, text = meldung(ueberschrift, vergleich_ueberschrift, titel, zufall.randint(len(titel) + 2, 80))
    assert stimmt, text

# Viele zufällige Statuszeilen
for _ in range(500):
    zeitpunkt = datetime(
        zufall.randint(1000, 9999), zufall.randint(1, 12), zufall.randint(1, 28), zufall.randint(0, 23), zufall.randint(0, 59)
    )
    host = "".join(zufall.choice("abc01-") for _ in range(zufall.randint(1, 12)))
    cpu = zufall.randint(0, 10000) / 100
    aenderung = zufall.randint(-1000, 1000) / 10
    if aenderung == 0:
        aenderung = 0.0
    stimmt, text = meldung(statuszeile, vergleich_zeile, zeitpunkt, host, cpu, aenderung)
    assert stimmt, text

# Viele zufällige Spalten
for _ in range(300):
    stellen = zufall.randint(0, 6)
    werte = [zufall.choice([zufall.randint(-10**6, 10**6), zufall.randint(-10**6, 10**6) / 8]) for _ in range(zufall.randint(0, 5))]
    stimmt, text = meldung(wertespalte, vergleich_spalte, werte, zufall.randint(1, 20), stellen)
    assert stimmt, text

# Obere Grenze: 10 000 Werte
werte = [nummer / 4 - 1000 for nummer in range(10000)]
assert wert_von(wertespalte, werte, 20, 6) == vergleich_spalte(werte, 20, 6), "Bei 10 000 Werten stimmt wertespalte nicht."
