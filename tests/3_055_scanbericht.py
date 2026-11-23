# Automatisch erzeugt aus lehrkraft/muster/3_055_scanbericht.py - nicht von Hand ändern.
# vorlage-hash: c53e98c6e3368632
# text-hash: a99cff90a720b02c
# thema: texte_zahlen
# inhalt: Tausendertrennzeichen und Prozent

BEISPIEL = [("Vertrieb", 1234567, 1543), ("Labor", 48210, 1205)]


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def mit_trennzeichen(zahl):
    """Vergleichslösung für die Tausendertrennung: setzt die Kommas von Hand von rechts."""
    ziffern = str(zahl)
    gruppen = []
    while len(ziffern) > 3:
        gruppen.insert(0, ziffern[-3:])
        ziffern = ziffern[:-3]
    gruppen.insert(0, ziffern)
    return ",".join(gruppen)


def vergleich_zeile(abteilung, dateien, auffaellig):
    """Vergleichslösung: füllt die Spalten mit ljust und rjust statt mit einem Format."""
    prozent = f"{auffaellig / dateien * 100:.2f}%"
    return abteilung.ljust(14) + mit_trennzeichen(dateien).rjust(14) + prozent.rjust(9)


def meldung_zeile(abteilung, dateien, auffaellig, hinweis=""):
    """Vergleicht zeile mit der Vergleichslösung; liefert (stimmt, Meldung) mit sichtbaren Rändern."""
    ergebnis = wert_von(zeile, abteilung, dateien, auffaellig)
    erwartet = vergleich_zeile(abteilung, dateien, auffaellig)
    text = f"zeile({abteilung!r}, {dateien}, {auffaellig}) ergibt\n  {ergebnis!r}\nerwartet war\n  {erwartet!r}{hinweis}"
    return ergebnis == erwartet, text


def eindeutig(dateien, auffaellig):
    """True, wenn beide Rechenwege für den Prozentwert gleich runden (keine Grenzfälle der Gleitkommazahl)."""
    return f"{auffaellig / dateien * 100:.2f}" == f"{auffaellig * 100 / dateien:.2f}"


# Die Zahl der Dateien erscheint mit Tausendertrennzeichen
ergebnis = wert_von(zeile, "Vertrieb", 1234567, 1543)
assert isinstance(ergebnis, str) and "1,234,567" in ergebnis, (
    f"zeile('Vertrieb', 1234567, 1543) ergibt {ergebnis!r}; darin fehlt '1,234,567'.\n"
    "Tipp: Ein Komma hinter dem Doppelpunkt setzt die Tausendertrennzeichen: f'{dateien:,}'."
)

# Der Anteil erscheint als Prozentwert mit zwei Nachkommastellen
assert "0.12%" in ergebnis, (
    f"zeile('Vertrieb', 1234567, 1543) ergibt {ergebnis!r}; darin fehlt '0.12%' (1543 / 1234567 = 0.00125).\n"
    "Tipp: f'{anteil:.2%}' nimmt den Anteil mal 100 und hängt das Prozentzeichen an."
)

# Die Zeile beginnt mit der Abteilung und ist 37 Zeichen lang
assert ergebnis.startswith("Vertrieb ") and len(ergebnis) == 37, (
    f"zeile('Vertrieb', 1234567, 1543) ergibt {ergebnis!r} mit {len(ergebnis)} Zeichen; "
    "erwartet waren 14 + 14 + 9 = 37 Zeichen, vorn die Abteilung.\n"
    "Tipp: Geben Sie jeder Spalte ihre Breite: :<14, :>14, und :>9."
)

# Das Beispiel Zeichen für Zeichen
stimmt, text = meldung_zeile("Vertrieb", 1234567, 1543, "\nTipp: Die Breite steht vor dem Komma: :>14,")
assert stimmt, text

# Eine zweite Abteilung (nicht fest hinschreiben!)
stimmt, text = meldung_zeile("Labor", 48210, 1205)
assert stimmt, text

# Kleine Zahlen ohne Trennzeichen, ab 1000 mit
for dateien in [7, 999, 1000]:
    stimmt, text = meldung_zeile("Empfang", dateien, 0)
    assert stimmt, text

# Ohne Befund ist der Anteil 0.00%
stimmt, text = meldung_zeile("Einkauf", 52000, 0)
assert stimmt, text

# Alle Dateien auffällig ergibt 100.00%
stimmt, text = meldung_zeile("Testlabor", 12, 12, "\nTipp: Rechnen Sie nicht selbst mal 100; das macht % schon.")
assert stimmt, text

# Gerundet wird beim Formatieren, nicht abgeschnitten
stimmt, text = meldung_zeile("Recht", 3, 2, "\nTipp: 2 / 3 ergibt 66.67%, nicht 66.66%.")
assert stimmt, text

# Abteilungsname mit genau 14 Zeichen
stimmt, text = meldung_zeile("Instandhaltung", 1, 1)
assert stimmt, text

# Obere Grenze: eine Milliarde Dateien
stimmt, text = meldung_zeile("Archiv", 10**9, 1)
assert stimmt, text

# bericht: Kopfzeile, zwei Abteilungen und Gesamt
ergebnis = wert_von(bericht, BEISPIEL)
erwartet = [KOPF, vergleich_zeile(*BEISPIEL[0]), vergleich_zeile(*BEISPIEL[1]), vergleich_zeile("Gesamt", 1282777, 2748)]
assert isinstance(ergebnis, list) and len(ergebnis) == 4, (
    f"bericht(...) ergibt {ergebnis!r}, erwartet war eine Liste mit 4 Zeilen: Kopf, Vertrieb, Labor, Gesamt."
)

# bericht: die Zeilen stimmen
assert ergebnis == erwartet, (
    "bericht(...) ergibt\n  " + "\n  ".join(repr(text) for text in ergebnis) + "\nerwartet war\n  "
    + "\n  ".join(repr(text) for text in erwartet)
    + "\nTipp: Die Gesamtzeile hat die Summe der Dateien und die Summe der Befunde; ihr Anteil ist 2748 / 1282777."
)

# bericht: eine einzige Abteilung
ergebnis = wert_von(bericht, [("Labor", 48210, 1205)])
erwartet = [KOPF, vergleich_zeile("Labor", 48210, 1205), vergleich_zeile("Gesamt", 48210, 1205)]
assert ergebnis == erwartet, f"bericht([('Labor', 48210, 1205)]) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Die Ausgabe des Programms
erwartet = "\n".join([KOPF, vergleich_zeile(*BEISPIEL[0]), vergleich_zeile(*BEISPIEL[1]), vergleich_zeile("Gesamt", 1282777, 2748)])
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Zeilen
zufall = Zufall(3055)
geprueft = 0
while geprueft < 2000:
    dateien = zufall.choice([zufall.randint(1, 2000), zufall.randint(1, 10**6), zufall.randint(1, 10**9)])
    auffaellig = zufall.choice([0, dateien, zufall.randint(0, dateien), zufall.randint(0, min(dateien, 50))])
    if eindeutig(dateien, auffaellig):
        name = "".join(zufall.choice("abcdefghij") for _ in range(zufall.randint(1, 14)))
        stimmt, text = meldung_zeile(name, dateien, auffaellig)
        assert stimmt, text
        geprueft += 1

# Viele zufällige Berichte
for _ in range(100):
    abteilungen = []
    for nummer in range(zufall.randint(1, 6)):
        dateien = zufall.randint(1, 10**6)
        abteilungen.append((f"Abt{nummer}", dateien, zufall.randint(0, dateien)))
    summe = sum(eintrag[1] for eintrag in abteilungen)
    befunde = sum(eintrag[2] for eintrag in abteilungen)
    if not eindeutig(summe, befunde) or not all(eindeutig(e[1], e[2]) for e in abteilungen):
        continue
    erwartet = [KOPF] + [vergleich_zeile(*eintrag) for eintrag in abteilungen] + [vergleich_zeile("Gesamt", summe, befunde)]
    ergebnis = wert_von(bericht, abteilungen)
    assert ergebnis == erwartet, f"bericht({abteilungen}) ergibt\n{ergebnis!r}\nerwartet war\n{erwartet}"

# Obere Grenze: 1000 Abteilungen
abteilungen = [(f"Abt{nummer}", 1000000, nummer) for nummer in range(1000)]
ergebnis = wert_von(bericht, abteilungen)
assert isinstance(ergebnis, list) and len(ergebnis) == 1002 and ergebnis[-1] == vergleich_zeile("Gesamt", 10**9, 499500), (
    "Bei 1000 Abteilungen stimmt der Bericht nicht; erwartet waren 1002 Zeilen und als letzte\n  "
    + repr(vergleich_zeile("Gesamt", 10**9, 499500))
)
