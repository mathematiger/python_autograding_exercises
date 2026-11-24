# Automatisch erzeugt aus lehrkraft/muster/3_064_replikatverzug.py - nicht von Hand ändern.
# vorlage-hash: 73199043217e81e6
# text-hash: 219c77695eef963f
# thema: algorithmen
# inhalt: Intervalle zusammenführen

MELDUNGEN = [(300, 420), (60, 180), (400, 500), (150, 200), (500, 560), (900, 960)]


def wert_von(funktion, zeitraeume):
    """Ruft funktion mit einer Kopie der Liste auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(list(zeitraeume))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def als_tupel(ergebnis):
    """Macht aus Einträgen, die Listen sind, Tupel, damit der Inhalt unabhängig von der Form verglichen wird."""
    if not isinstance(ergebnis, list):
        return ergebnis
    return [tuple(eintrag) if isinstance(eintrag, (list, tuple)) else eintrag for eintrag in ergebnis]


def kurz(wert):
    """Kürzt lange Listen für Meldungen."""
    text = repr(wert)
    if len(text) <= 200:
        return text
    if isinstance(wert, list):
        return f"<Liste mit {len(wert)} Einträgen>"
    return text[:150] + " …"


def pruefe_zusammenfuehren(zeitraeume, erwartet, hinweis=""):
    """Prüft den Inhalt von zusammenfuehren(zeitraeume); liefert (stimmt, Meldung)."""
    ergebnis = als_tupel(wert_von(zusammenfuehren, zeitraeume))
    text = f"zusammenfuehren({kurz(zeitraeume)}) ergibt {kurz(ergebnis)}, erwartet war {kurz(erwartet)}.{hinweis}"
    return ergebnis == erwartet, text


def pruefe_gesamtdauer(zeitraeume, erwartet, hinweis=""):
    """Prüft gesamtdauer(zeitraeume); liefert (stimmt, Meldung)."""
    ergebnis = wert_von(gesamtdauer, zeitraeume)
    text = f"gesamtdauer({kurz(zeitraeume)}) ergibt {kurz(ergebnis)}, erwartet war {erwartet}.{hinweis}"
    return ergebnis == erwartet, text


def vergleich(zeitraeume):
    """Vergleichslösung: markiert jede belegte Sekunde und liest zusammenhängende Läufe ab (langsam, aber offensichtlich richtig)."""
    belegt = set()
    for start, ende in zeitraeume:
        belegt.update(range(start, ende))
    ergebnis = []
    for sekunde in sorted(belegt):
        if ergebnis and ergebnis[-1][1] == sekunde:
            ergebnis[-1] = (ergebnis[-1][0], sekunde + 1)
        else:
            ergebnis.append((sekunde, sekunde + 1))
    return ergebnis


def zerlegte_bloecke(zufall, anzahl_bloecke):
    """Erzeugt getrennte Blöcke und zerlegt jeden in zehn sich überlappende oder berührende Teile; liefert (teile, bloecke)."""
    bloecke = []
    teile = []
    ende = 0
    for _ in range(anzahl_bloecke):
        start = ende + zufall.randint(1, 100)
        ende = start + zufall.randint(20, 150)
        bloecke.append((start, ende))
        schnitte = [start] + sorted(zufall.sample(range(start + 1, ende), 4)) + [ende]
        for links, rechts in zip(schnitte, schnitte[1:]):
            teile.append((links, rechts))
        for _ in range(5):
            von = zufall.randint(start, ende - 1)
            teile.append((von, zufall.randint(von + 1, ende)))
    zufall.shuffle(teile)
    return teile, bloecke


# zusammenfuehren: das Beispiel
stimmt, text = pruefe_zusammenfuehren(
    MELDUNGEN, [(60, 200), (300, 560), (900, 960)],
    "\nTipp: Sortieren Sie zuerst mit sorted und vergleichen Sie dann jeden Zeitraum mit dem letzten Eintrag "
    "des Ergebnisses. Zeiträume, die sich nur berühren wie (400, 500) und (500, 560), gehören zusammen (<=).",
)
assert stimmt, text

# zusammenfuehren: andere Meldungen (nicht fest hinschreiben!)
stimmt, text = pruefe_zusammenfuehren([(40, 70), (10, 50), (80, 90)], [(10, 70), (80, 90)])
assert stimmt, text

# zusammenfuehren: getrennte Zeiträume kommen nur geordnet zurück
stimmt, text = pruefe_zusammenfuehren(
    [(700, 710), (100, 120), (400, 450)], [(100, 120), (400, 450), (700, 710)],
    "\nTipp: Ohne Überschneidung wird nichts verschmolzen, aber das Ergebnis ist nach start geordnet.",
)
assert stimmt, text

# zusammenfuehren: eine Sekunde Abstand trennt zwei Zeiträume
stimmt, text = pruefe_zusammenfuehren(
    [(10, 20), (21, 30)], [(10, 20), (21, 30)],
    "\nTipp: (10, 20) umfasst die Sekunden 10 bis 19; Sekunde 20 ist frei, also bleiben beide getrennt.",
)
assert stimmt, text

# zusammenfuehren: sich berührende Zeiträume (ende == start) werden einer
stimmt, text = pruefe_zusammenfuehren(
    [(21, 30), (10, 21)], [(10, 30)],
    "\nTipp: Endet ein Zeitraum genau dort, wo der nächste beginnt, gehören beide zusammen; vergleichen Sie mit <=.",
)
assert stimmt, text

# zusammenfuehren: ein Zeitraum liegt ganz in einem anderen
stimmt, text = pruefe_zusammenfuehren(
    [(100, 500), (200, 300)], [(100, 500)],
    "\nTipp: Das neue Ende ist das größere der beiden Enden (max), nicht einfach das Ende des neuen Zeitraums.",
)
assert stimmt, text

# zusammenfuehren: eine Kette, in der jeder den vorigen verlängert
stimmt, text = pruefe_zusammenfuehren(
    [(50, 90), (10, 40), (30, 60), (85, 100)], [(10, 100)],
    "\nTipp: Vergleichen Sie mit dem Ende des schon verlängerten letzten Eintrags, nicht mit dem ursprünglichen.",
)
assert stimmt, text

# zusammenfuehren: derselbe Zeitraum mehrfach gemeldet
stimmt, text = pruefe_zusammenfuehren([(5, 9), (5, 9), (5, 9)], [(5, 9)])
assert stimmt, text

# zusammenfuehren: gleicher Beginn, verschiedenes Ende
stimmt, text = pruefe_zusammenfuehren([(0, 30), (0, 10), (0, 20)], [(0, 30)])
assert stimmt, text

# zusammenfuehren: ein einziger Zeitraum
stimmt, text = pruefe_zusammenfuehren([(2678399, 2678400)], [(2678399, 2678400)])
assert stimmt, text

# zusammenfuehren: keine Meldungen
stimmt, text = pruefe_zusammenfuehren([], [], "\nTipp: Ohne Meldungen ist das Ergebnis die leere Liste.")
assert stimmt, text

# zusammenfuehren: die Einträge des Ergebnisses sind Tupel
ergebnis = wert_von(zusammenfuehren, MELDUNGEN)
assert isinstance(ergebnis, list) and all(isinstance(eintrag, tuple) for eintrag in ergebnis), (
    f"zusammenfuehren(meldungen) ergibt {kurz(ergebnis)}; erwartet war eine Liste von Tupeln wie (60, 200).\n"
    "Tipp: Hängen Sie (start, ende) an, nicht [start, ende]."
)

# zusammenfuehren: die übergebene Liste bleibt unverändert
zeitraeume = list(MELDUNGEN)
try:
    zusammenfuehren(zeitraeume)
except Exception:
    pass
assert zeitraeume == MELDUNGEN, (
    f"Nach zusammenfuehren(meldungen) steht in meldungen {zeitraeume}, erwartet war die ursprüngliche Liste "
    f"{MELDUNGEN}.\nTipp: zeitraeume.sort() ändert die Liste selbst; sorted(zeitraeume) liefert eine neue."
)

# gesamtdauer: das Beispiel
stimmt, text = pruefe_gesamtdauer(MELDUNGEN, 460, "\nTipp: Summieren Sie ende - start über die zusammengeführten Zeiträume.")
assert stimmt, text

# gesamtdauer: überschneidende Sekunden zählen nur einmal
stimmt, text = pruefe_gesamtdauer(
    [(40, 70), (10, 50), (80, 90)], 70,
    "\nTipp: (10, 50) und (40, 70) teilen sich die Sekunden 40 bis 49; zusammen decken sie nur die 60 Sekunden von 10 bis 69 ab.",
)
assert stimmt, text

# gesamtdauer: ein einzelner Zeitraum
stimmt, text = pruefe_gesamtdauer([(0, 2678400)], 2678400)
assert stimmt, text

# gesamtdauer: keine Meldungen
stimmt, text = pruefe_gesamtdauer([], 0)
assert stimmt, text

# gesamtdauer benutzt zusammenfuehren
aufrufe = []
eigenes_zusammenfuehren = zusammenfuehren


def zusammenfuehren(zeitraeume):
    """Zählt die Aufrufe und reicht sie an die eigene Funktion weiter."""
    aufrufe.append(len(zeitraeume))
    return eigenes_zusammenfuehren(zeitraeume)


try:
    gesamtdauer(list(MELDUNGEN))
except Exception:
    pass
zusammenfuehren = eigenes_zusammenfuehren
assert len(aufrufe) == 1, (
    f"gesamtdauer hat zusammenfuehren {len(aufrufe)}-mal aufgerufen; erwartet war genau einmal.\n"
    "Tipp: Führen Sie die Zeiträume mit zusammenfuehren zusammen und addieren Sie dann ihre Dauern."
)

# Die Ausgabe des Programms
erwartet = "[(60, 200), (300, 560), (900, 960)]\n460"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Meldungen
zufall = Zufall(3064)
for _ in range(400):
    zeitraeume = []
    for _ in range(zufall.randint(0, 12)):
        start = zufall.randint(0, 40)
        zeitraeume.append((start, start + zufall.randint(1, 8)))
    erwartet = vergleich(zeitraeume)
    stimmt, text = pruefe_zusammenfuehren(zeitraeume, erwartet)
    assert stimmt, text
    dauer = sum(ende - start for start, ende in erwartet)
    stimmt, text = pruefe_gesamtdauer(zeitraeume, dauer)
    assert stimmt, text

# Laufzeit: Vorbereitung, je 100 und 400 getrennte Zeiträume in gemischter Reihenfolge
laufzeitproben = []
for anzahl in [100, 400]:
    zeitraeume = [(10 * nummer, 10 * nummer + 5) for nummer in range(anzahl)]
    zufall.shuffle(zeitraeume)
    try:
        ergebnis, gezaehlt = zaehle_schritte(zusammenfuehren, list(zeitraeume))
    except Exception as fehler:
        ergebnis, gezaehlt = f"{type(fehler).__name__}: {fehler}", 0
    laufzeitproben.append((anzahl, sorted(zeitraeume), als_tupel(ergebnis), gezaehlt))

# Laufzeit: viele getrennte Zeiträume kommen geordnet zurück
for anzahl, erwartet, ergebnis, _ in laufzeitproben:
    assert ergebnis == erwartet, (
        f"zusammenfuehren für {anzahl} getrennte Zeiträume (0, 5), (10, 15), … in gemischter Reihenfolge ergibt "
        f"{kurz(ergebnis)}, erwartet waren dieselben Zeiträume geordnet."
    )

# Laufzeit: die Schritte wachsen wie n · log n, nicht wie n²
schritte_klein = max(laufzeitproben[0][3], 1)
schritte_gross = laufzeitproben[1][3]
assert schritte_gross <= 7 * schritte_klein, (
    f"zusammenfuehren braucht für 100 getrennte Zeiträume {schritte_klein} Schritte, für viermal so viele "
    f"{schritte_gross}, also {schritte_gross / schritte_klein:.1f}-mal so viele. Bei O(n log n) wären es etwa "
    "4- bis 5-mal so viele, bei O(n²) 16-mal.\n"
    "Tipp: Vergleichen Sie nicht jedes Paar, sondern sortieren Sie einmal mit sorted und gehen Sie dann "
    "einmal durch, wobei Sie jeden Zeitraum nur mit dem letzten Eintrag des Ergebnisses vergleichen."
)

# Obere Grenze: 100 000 Meldungen aus 10 000 getrennten Zeiträumen
teile, bloecke = zerlegte_bloecke(zufall, 10000)
ergebnis = als_tupel(wert_von(zusammenfuehren, teile))
abweichung = "?"
if isinstance(ergebnis, list):
    for index in range(min(len(ergebnis), len(bloecke))):
        if ergebnis[index] != bloecke[index]:
            abweichung = f"Eintrag {index} ist {ergebnis[index]!r}, erwartet war {bloecke[index]!r}"
            break
    else:
        abweichung = f"{len(ergebnis)} Einträge, erwartet waren {len(bloecke)}"
assert ergebnis == bloecke, (
    f"Bei 100 000 Meldungen, die 10 000 getrennte Zeiträume bilden, stimmt zusammenfuehren nicht: {abweichung}."
)

# Obere Grenze: gesamtdauer für 100 000 Meldungen
dauer = sum(ende - start for start, ende in bloecke)
stimmt, text = pruefe_gesamtdauer(teile, dauer)
assert stimmt, text
