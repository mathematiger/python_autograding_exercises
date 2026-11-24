# Automatisch erzeugt aus lehrkraft/muster/3_065_testumgebung.py - nicht von Hand ändern.
# vorlage-hash: 35fd1297d384582c
# text-hash: 79cdfcc8148f4300
# thema: algorithmen
# inhalt: Greedy: Termine ohne Überschneidung

import bisect

BEISPIEL = [("Kasse", 9, 12), ("Shop", 10, 11), ("Lager", 11, 14),
            ("Login", 12, 13), ("Suche", 13, 17), ("Bericht", 8, 18)]


def kurz(wert):
    """Kürzt lange Listen für Meldungen."""
    text = repr(wert)
    if len(text) <= 300:
        return text
    if isinstance(wert, list):
        return f"<Liste mit {len(wert)} Anträgen, beginnend mit {wert[:3]!r}>"
    return text[:200] + " …"


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def ueberschneidung_erwartet(a, b, erwartet, hinweis=""):
    """Prüft ueberschneiden(a, b); liefert (stimmt, Meldung)."""
    ergebnis = wert_von(ueberschneiden, a, b)
    return ergebnis == erwartet, f"ueberschneiden({a!r}, {b!r}) ergibt {ergebnis!r}, erwartet war {erwartet}.{hinweis}"


def beste_anzahl_alle_teilmengen(antraege):
    """Langsame Vergleichslösung: probiert alle Auswahlen aus und zählt die größte ohne Überschneidung."""
    beste = 0
    for maske in range(2 ** len(antraege)):
        auswahl = [antraege[i] for i in range(len(antraege)) if maske >> i & 1]
        passt = all(
            a[2] <= b[1] or b[2] <= a[1]
            for i, a in enumerate(auswahl)
            for b in auswahl[i + 1:]
        )
        if passt and len(auswahl) > beste:
            beste = len(auswahl)
    return beste


def beste_anzahl_rueckwaerts(antraege):
    """Vergleichslösung anders als gierig: nach Start sortiert, von hinten „nehmen oder auslassen“."""
    geordnet = sorted(antraege, key=lambda antrag: antrag[1])
    starts = [antrag[1] for antrag in geordnet]
    beste = [0] * (len(geordnet) + 1)
    for i in range(len(geordnet) - 1, -1, -1):
        naechster = bisect.bisect_left(starts, geordnet[i][2])
        beste[i] = max(beste[i + 1], 1 + beste[naechster])
    return beste[0]


def fehler_in_auswahl(antraege, ergebnis, beste):
    """Prüft, ob ergebnis eine gültige Auswahl mit beste Anträgen ist; liefert eine Beschreibung oder None."""
    aufruf = f"genehmigte({kurz(antraege)})"
    if not isinstance(ergebnis, list):
        hinweis = " (fehlt das return?)" if ergebnis is None else ""
        return f"{aufruf} ergibt {kurz(ergebnis)}, erwartet war eine Liste von Anträgen{hinweis}."
    vorhanden = set(antraege)
    for antrag in ergebnis:
        if antrag not in vorhanden:
            return f"{aufruf} enthält {antrag!r}, das ist keiner der Anträge."
    if len(set(ergebnis)) < len(ergebnis):
        return f"{aufruf} ergibt {kurz(ergebnis)}: Ein Antrag kommt mehrfach vor."
    for vorher, nachher in zip(ergebnis, ergebnis[1:]):
        if vorher[2] > nachher[2]:
            return (
                f"{aufruf} ergibt {kurz(ergebnis)}: {vorher!r} steht vor {nachher!r}, "
                "erwartet war die Reihenfolge nach der Endzeit."
            )
    for vorher, nachher in zip(ergebnis, ergebnis[1:]):
        if nachher[1] < vorher[2]:
            return f"{aufruf} ergibt {kurz(ergebnis)}: {vorher!r} und {nachher!r} überschneiden sich."
    if len(ergebnis) != beste:
        return (
            f"{aufruf} ergibt {kurz(ergebnis)} mit {len(ergebnis)} Anträgen, möglich sind {beste} ohne Überschneidung."
        )
    return None


def pruefe_genehmigte(antraege, beste, hinweis=""):
    """Ruft genehmigte mit einer Kopie auf und prüft das Ergebnis; liefert eine Beschreibung oder None."""
    ergebnis = wert_von(genehmigte, list(antraege))
    fehler = fehler_in_auswahl(antraege, ergebnis, beste)
    if fehler is None:
        return None
    return fehler + hinweis


# ueberschneiden: das Beispiel mit Überschneidung
stimmt, text = ueberschneidung_erwartet(("Kasse", 9, 12), ("Lager", 11, 14), True)
assert stimmt, text

# ueberschneiden: getrennte Fenster überschneiden sich nicht
stimmt, text = ueberschneidung_erwartet(("Shop", 10, 11), ("Suche", 13, 17), False)
assert stimmt, text

# ueberschneiden: die Reihenfolge von a und b ist egal
stimmt, text = ueberschneidung_erwartet(("Suche", 13, 17), ("Shop", 10, 11), False)
assert stimmt, text

# ueberschneiden: endet eins, wenn das andere beginnt, passt es (das Beispiel)
stimmt, text = ueberschneidung_erwartet(
    ("Kasse", 9, 12), ("Login", 12, 13), False,
    "\nTipp: ende gehört nicht mehr zum Fenster; ein Fenster bis 12 Uhr und eins ab 12 Uhr passen hintereinander.",
)
assert stimmt, text

# ueberschneiden: angrenzend auch in umgekehrter Reihenfolge
stimmt, text = ueberschneidung_erwartet(("Login", 12, 13), ("Kasse", 9, 12), False)
assert stimmt, text

# ueberschneiden: ein Fenster liegt ganz im anderen
stimmt, text = ueberschneidung_erwartet(
    ("Bericht", 8, 18), ("Login", 12, 13), True,
    "\nTipp: Zwei Fenster überschneiden sich, wenn jedes beginnt, bevor das andere endet.",
)
assert stimmt, text

# ueberschneiden: das kleine Fenster zuerst, das große umschließt es
stimmt, text = ueberschneidung_erwartet(("Login", 12, 13), ("Bericht", 8, 18), True)
assert stimmt, text

# ueberschneiden: gleiche Zeiten
stimmt, text = ueberschneidung_erwartet(("Kasse", 9, 12), ("Shop", 9, 12), True)
assert stimmt, text

# genehmigte: das Beispiel
fehler = pruefe_genehmigte(BEISPIEL, 3)
assert fehler is None, fehler

# genehmigte: andere Anträge (nicht fest hinschreiben!)
fehler = pruefe_genehmigte([("A", 1, 3), ("B", 2, 5), ("C", 4, 7), ("D", 6, 9), ("E", 8, 10)], 3)
assert fehler is None, fehler

# genehmigte: die Reihenfolge der Eingabe ist beliebig
fehler = pruefe_genehmigte(
    [("Spät", 20, 22), ("Lang", 0, 30), ("Früh", 1, 3), ("Mitte", 10, 12)], 3,
    "\nTipp: Sortieren Sie die Anträge zuerst nach ihrer Endzeit.",
)
assert fehler is None, fehler

# genehmigte: Fenster direkt hintereinander werden alle genehmigt
fehler = pruefe_genehmigte(
    [("C", 4, 6), ("A", 0, 2), ("D", 6, 9), ("B", 2, 4)], 4,
    "\nTipp: Ein Fenster darf genau dann beginnen, wenn das vorige endet.",
)
assert fehler is None, fehler

# genehmigte: „kürzestes Fenster zuerst“ reicht nicht
fehler = pruefe_genehmigte(
    [("A", 0, 10), ("B", 9, 12), ("C", 11, 20)], 2,
    "\nTipp: Das kürzeste Fenster (9, 12) blockiert beide anderen. Sortieren Sie nach der Endzeit, nicht nach der Länge.",
)
assert fehler is None, fehler

# genehmigte: „frühester Start zuerst“ reicht nicht
fehler = pruefe_genehmigte(
    [("Nacht", 0, 100), ("B", 1, 2), ("C", 3, 4)], 2,
    "\nTipp: Das Fenster, das zuerst beginnt, blockiert hier alle anderen. Sortieren Sie nach der Endzeit.",
)
assert fehler is None, fehler

# genehmigte: ein neuer Antrag wird mit dem zuletzt genehmigten verglichen
fehler = pruefe_genehmigte(
    [("A", 0, 4), ("B", 1, 5), ("C", 3, 6), ("D", 5, 8)], 2,
    "\nTipp: Vergleichen Sie jeden Antrag mit dem zuletzt genehmigten, nicht mit dem davor in der sortierten Liste.",
)
assert fehler is None, fehler

# genehmigte: alle Fenster überschneiden sich, nur eins wird genehmigt
fehler = pruefe_genehmigte([("A", 5, 9), ("B", 0, 10), ("C", 6, 8), ("D", 7, 12)], 1)
assert fehler is None, fehler

# genehmigte: ein Fenster ab Montag 0 Uhr
fehler = pruefe_genehmigte(
    [("Null", 0, 1), ("B", 1, 3)], 2,
    "\nTipp: Startzeit 0 ist erlaubt; vergleichen Sie mit dem zuletzt genehmigten Antrag, nicht mit einer Startzahl.",
)
assert fehler is None, fehler

# genehmigte: ein einziger Antrag
fehler = pruefe_genehmigte([("Kasse", 9, 12)], 1)
assert fehler is None, fehler

# genehmigte: keine Anträge
fehler = pruefe_genehmigte([], 0, "\nTipp: Ohne Anträge ist das Ergebnis die leere Liste [].")
assert fehler is None, fehler

# genehmigte: dieselbe Endzeit bei mehreren Anträgen
fehler = pruefe_genehmigte([("A", 2, 5), ("B", 0, 5), ("C", 4, 5), ("D", 5, 6), ("E", 1, 6)], 2)
assert fehler is None, fehler

# genehmigte: die Liste antraege bleibt unverändert
eingabe = list(BEISPIEL)
wert_von(genehmigte, eingabe)
assert eingabe == BEISPIEL, (
    f"genehmigte hat die übergebene Liste verändert, sie ist jetzt {eingabe!r}.\n"
    "Tipp: sorted(antraege, key=...) liefert eine neue Liste, antraege.sort() ändert die alte."
)

# Viele zufällige Anträge, verglichen mit dem Durchprobieren aller Auswahlen
zufall = Zufall(3065)
for runde in range(300):
    antraege = []
    for nummer in range(zufall.randint(0, 8)):
        start = zufall.randint(0, 15)
        antraege.append((f"T{nummer}", start, start + zufall.randint(1, 6)))
    fehler = pruefe_genehmigte(antraege, beste_anzahl_alle_teilmengen(antraege))
    assert fehler is None, fehler

# Laufzeit: genehmigte vergleicht nicht jeden Antrag mit allen genehmigten
proben = []
for anzahl in [100, 400]:
    antraege = [(f"T{nummer}", 2 * nummer, 2 * nummer + 2) for nummer in range(anzahl)]
    zufall.shuffle(antraege)
    ergebnis, schritte = zaehle_schritte(genehmigte, list(antraege))
    proben.append((fehler_in_auswahl(antraege, ergebnis, anzahl), max(schritte, 1)))
fehler = proben[0][0] or proben[1][0]
schritte_klein = proben[0][1]
schritte_gross = proben[1][1]
assert fehler is None and schritte_gross <= 7 * schritte_klein, fehler or (
    f"genehmigte braucht für 100 Anträge direkt hintereinander {schritte_klein} Schritte, für viermal so viele "
    f"{schritte_gross}, also {schritte_gross / schritte_klein:.1f}-mal so viele. Bei O(n log n) wären es etwa "
    "4- bis 5-mal so viele, bei O(n²) 16-mal.\n"
    "Tipp: Nach dem Sortieren genügt der Vergleich mit dem zuletzt genehmigten Antrag, nicht mit allen."
)

# Obere Grenze: 100 000 Anträge
antraege = []
for nummer in range(100000):
    start = zufall.randint(0, 10**9 - 1)
    antraege.append((f"T{nummer}", start, min(10**9, start + zufall.randint(1, 10**5))))
fehler = pruefe_genehmigte(antraege, beste_anzahl_rueckwaerts(antraege))
assert fehler is None, fehler
