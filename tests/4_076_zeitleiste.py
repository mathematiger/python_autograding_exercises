# Automatisch erzeugt aus lehrkraft/muster/4_076_zeitleiste.py - nicht von Hand ändern.
# vorlage-hash: ac70ea2da34eb9fa
# text-hash: 9d6d1e4b811a6972
# thema: algorithmen
# inhalt: k Listen mit Heap mergen

from itertools import islice

BEISPIEL = {
    "san01": [("03:11:58", "Pfad zu hv01 ausgefallen"), ("03:12:09", "Sperre für web-01 an hv02 vergeben")],
    "hv02": [("03:12:07", "Herzschlag von hv01 fehlt"), ("03:12:09", "starte VM web-01 neu"), ("03:12:31", "VM web-01 läuft")],
    "hv03": [("03:12:08", "Herzschlag von hv01 fehlt")],
    "hv01": [],
}


def kopie(protokolle):
    """Kopiert die Protokolle, damit eine Lösung, die sie verändert, die Tests nicht verdirbt."""
    return {geraet: list(eintraege) for geraet, eintraege in protokolle.items()}


def leiste_von(protokolle):
    """Ruft zeitleiste mit einer Kopie auf und holt alle Einträge ab; ein Fehler wird als Text zurückgegeben."""
    try:
        return list(zeitleiste(kopie(protokolle)))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def fenster_von(protokolle, von, bis):
    """Ruft stoerungsfenster mit einer Kopie auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return stoerungsfenster(kopie(protokolle), von, bis)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich(protokolle):
    """Vergleichslösung: alles markieren und nach (Zeit, Gerätenummer, Position) sortieren, also anders als verlangt."""
    markiert = []
    for nummer, (geraet, eintraege) in enumerate(protokolle.items()):
        for position, (zeit, meldung) in enumerate(eintraege):
            markiert.append((zeit, nummer, position, geraet, meldung))
    return [(zeit, geraet, meldung) for zeit, _, _, geraet, meldung in sorted(markiert)]


def vergleich_fenster(protokolle, von, bis):
    """Vergleichslösung für stoerungsfenster über die ganze Zeitleiste."""
    return [eintrag for eintrag in vergleich(protokolle) if von <= eintrag[0] <= bis]


def abweichung(ergebnis, erwartet):
    """Beschreibt Länge und erste abweichende Stelle, damit lange Ergebnisse lesbar bleiben."""
    if not isinstance(ergebnis, list):
        return f"{str(ergebnis)[:200]!r} statt einer Liste mit {len(erwartet)} Einträgen"
    for stelle, (ihr, soll) in enumerate(zip(ergebnis, erwartet)):
        if ihr != soll:
            return f"{len(ergebnis)} statt {len(erwartet)} Einträgen, erste Abweichung an Stelle {stelle}: {ihr!r} statt {soll!r}"
    return f"{len(ergebnis)} statt {len(erwartet)} Einträgen"


def pruefe(protokolle, hinweis=""):
    """Vergleicht list(zeitleiste(...)) mit der Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = leiste_von(protokolle)
    erwartet = vergleich(protokolle)
    text = f"list(zeitleiste({protokolle}))\nergibt   {ergebnis!r}\nerwartet {erwartet}"
    return ergebnis == erwartet, text + hinweis


def pruefe_fenster(protokolle, von, bis, hinweis=""):
    """Vergleicht stoerungsfenster mit der Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = fenster_von(protokolle, von, bis)
    erwartet = vergleich_fenster(protokolle, von, bis)
    text = f"stoerungsfenster({protokolle}, {von!r}, {bis!r})\nergibt   {ergebnis!r}\nerwartet {erwartet}"
    return ergebnis == erwartet, text + hinweis


def zeit(sekunden):
    """Macht aus Sekunden seit Mitternacht einen Zeitstempel HH:MM:SS."""
    return f"{sekunden // 3600:02d}:{sekunden // 60 % 60:02d}:{sekunden % 60:02d}"


def zufallsprotokolle(zufall, geraete, eintraege, spanne):
    """Erzeugt bis zu geraete Protokolle mit zusammen eintraege Einträgen und Zeiten aus spanne Sekunden ab 03:00:00."""
    namen = [f"g{nummer:03d}" for nummer in range(geraete)]
    zufall.shuffle(namen)
    zeiten = {name: [] for name in namen}
    for _ in range(eintraege if namen else 0):
        zeiten[zufall.choice(namen)].append(10800 + zufall.randrange(spanne))
    protokolle = {}
    for name in namen:
        protokolle[name] = [(zeit(sekunde), f"m{name}-{stelle}") for stelle, sekunde in enumerate(sorted(zeiten[name]))]
    return protokolle


def als_zaehllisten(protokolle):
    """Macht aus jedem Protokoll eine Zaehlliste, die ihre Lesezugriffe zählt."""
    return {geraet: Zaehlliste(eintraege) for geraet, eintraege in protokolle.items()}


def gelesen(zaehlprotokolle):
    """Summe der Lesezugriffe auf alle Zaehllisten."""
    return sum(liste.lesezugriffe for liste in zaehlprotokolle.values())


# zeitleiste: im Beispiel kommen alle sechs Einträge heraus
ergebnis = leiste_von(BEISPIEL)
assert isinstance(ergebnis, list) and len(ergebnis) == 6, (
    f"list(zeitleiste(protokolle)) ergibt {ergebnis!r}, erwartet war eine Liste mit 6 Einträgen.\n"
    "Tipp: Legen Sie nach jedem heappop den nächsten Eintrag desselben Protokolls in den Heap."
)

# zeitleiste: im Beispiel sind die Zeitstempel aufsteigend
zeiten = [eintrag[0] for eintrag in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert zeiten == ["03:11:58", "03:12:07", "03:12:08", "03:12:09", "03:12:09", "03:12:31"], (
    f"Die Zeitstempel der Zeitleiste sind {zeiten}, erwartet war\n"
    "['03:11:58', '03:12:07', '03:12:08', '03:12:09', '03:12:09', '03:12:31'].\n"
    "Tipp: Das erste Element der Tupel im Heap ist der Zeitstempel, danach die Gerätenummer."
)

# zeitleiste: das Beispiel vollständig, san01 vor hv02 bei 03:12:09
stimmt, text = pruefe(
    BEISPIEL,
    "\nTipp: Jeder Eintrag ist ein Tripel (zeitstempel, gerät, meldung). Bei gleichem Zeitstempel kommt san01 "
    "zuerst, weil es im Dictionary vor hv02 steht.",
)
assert stimmt, text

# zeitleiste: andere Protokolle (nicht fest hinschreiben!)
stimmt, text = pruefe(
    {
        "fw01": [("22:00:00", "Regel 17 geändert"), ("22:05:10", "Verbindung zu db01 verworfen")],
        "db01": [("21:59:59", "Sicherung beendet"), ("22:05:11", "Zeitüberschreitung bei app01")],
        "app01": [("22:05:12", "Datenbank nicht erreichbar")],
    }
)
assert stimmt, text

# zeitleiste: gleicher Zeitstempel, Reihenfolge wie im Dictionary statt alphabetisch
stimmt, text = pruefe(
    {"web02": [("08:00:00", "A")], "db01": [("08:00:00", "B")], "app03": [("08:00:00", "C")]},
    "\nTipp: Legen Sie (zeitstempel, gerätenummer, position) in den Heap, mit der Nummer aus "
    "enumerate(protokolle) statt des Namens.",
)
assert stimmt, text

# zeitleiste: gleicher Zeitstempel in einem Protokoll, Reihenfolge bleibt
stimmt, text = pruefe(
    {"hv01": [("09:00:00", "zweiter Versuch"), ("09:00:00", "VM gestartet"), ("09:00:00", "Abbruch")]},
    "\nTipp: Liegt im Tupel nach Zeitstempel und Gerätenummer die Meldung statt der Position, kommen gleich alte "
    "Meldungen alphabetisch heraus.",
)
assert stimmt, text

# zeitleiste: nur ein Gerät
stimmt, text = pruefe({"nas01": [("01:00:00", "Scrub begonnen"), ("01:30:00", "Scrub beendet")]})
assert stimmt, text

# zeitleiste: leere Protokolle vorn, in der Mitte und hinten
stimmt, text = pruefe(
    {"a": [], "b": [("10:00:00", "x"), ("10:00:02", "y")], "c": [], "d": [("10:00:01", "z")], "e": []},
    "\nTipp: Ein leeres Protokoll bekommt keinen Eintrag im Heap.",
)
assert stimmt, text

# zeitleiste: kein Gerät
stimmt, text = pruefe({})
assert stimmt, text

# zeitleiste: alle Protokolle leer
stimmt, text = pruefe({"hv01": [], "hv02": []})
assert stimmt, text

# zeitleiste: Zeitstempel am Rand des Tages
stimmt, text = pruefe({"a": [("00:00:00", "Mitternacht"), ("23:59:59", "Tagesende")], "b": [("12:00:00", "Mittag")]})
assert stimmt, text

# Die übergebenen Protokolle bleiben unverändert
protokolle = kopie(BEISPIEL)
try:
    list(zeitleiste(protokolle))
    stoerungsfenster(protokolle, "03:12:00", "03:12:10")
except Exception:
    pass
assert protokolle == BEISPIEL, (
    f"Nach zeitleiste und stoerungsfenster sind die Protokolle {protokolle};\nsie sollten unverändert bleiben.\n"
    "Tipp: Merken Sie sich im Heap die Position, statt mit pop Einträge zu entfernen."
)

# zeitleiste ist ein Generator
try:
    ergebnis = zeitleiste(kopie(BEISPIEL))
    ist_iterator = iter(ergebnis) is ergebnis
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
    ist_iterator = False
assert ist_iterator, (
    f"zeitleiste(protokolle) gibt {type(ergebnis).__name__} zurück, erwartet war ein Generator.\n"
    "Tipp: Schreiben Sie yield statt append und return."
)

# Mit einem Heap aus heapq, ohne sort, sorted und heapq.merge
verboten = [name for name in ["sort", "sorted", "merge"] if verwendet(name)]
mit_heap = verwendet("heappop") or verwendet("heapreplace") or verwendet("heappushpop")
assert verboten == [] and mit_heap, (
    f"Ihr Code verwendet {verboten if verboten else 'kein heappop'}. Führen Sie die Protokolle mit heapq.heappush "
    "und heapq.heappop zusammen; sort, sorted und heapq.merge sind hier nicht erlaubt."
)

# zeitleiste liest nur, was gebraucht wird
zufall = Zufall(4076)
zaehlprotokolle = als_zaehllisten(zufallsprotokolle(zufall, 4, 4000, 3600))
try:
    erste = list(islice(zeitleiste(zaehlprotokolle), 3))
    fehler = None
except Exception as ausnahme:
    erste = []
    fehler = f"{type(ausnahme).__name__}: {ausnahme}"
assert fehler is None and gelesen(zaehlprotokolle) <= 2 * 3 + 2 * 4, (
    f"Für die ersten 3 Einträge aus 4 Protokollen mit zusammen 4000 Einträgen hat zeitleiste "
    f"{gelesen(zaehlprotokolle)} Einträge gelesen{f' (Fehler: {fehler})' if fehler else ''}; erlaubt sind "
    "2 · 3 + 2 · 4 = 14.\nTipp: Legen Sie anfangs nur den ersten Eintrag jedes Protokolls in den Heap und "
    "lesen Sie den nächsten erst nach dem heappop."
)

# stoerungsfenster: das Beispiel
ergebnis = fenster_von(BEISPIEL, "03:12:08", "03:12:09")
erwartet = vergleich_fenster(BEISPIEL, "03:12:08", "03:12:09")
assert ergebnis == erwartet, (
    f'stoerungsfenster(protokolle, "03:12:08", "03:12:09") ergibt\n{ergebnis!r},\nerwartet war\n{erwartet}.\n'
    "Tipp: von und bis gehören beide zum Fenster, die Reihenfolge ist die der Zeitleiste."
)

# stoerungsfenster: ein anderes Fenster
stimmt, text = pruefe_fenster(BEISPIEL, "03:12:00", "03:12:30")
assert stimmt, text

# stoerungsfenster: von und bis gehören dazu
stimmt, text = pruefe_fenster(BEISPIEL, "03:11:58", "03:12:31")
assert stimmt, text

# stoerungsfenster: ein Fenster aus einem einzigen Zeitpunkt
stimmt, text = pruefe_fenster(BEISPIEL, "03:12:09", "03:12:09")
assert stimmt, text

# stoerungsfenster: nichts im Fenster
stimmt, text = pruefe_fenster(BEISPIEL, "03:12:10", "03:12:30")
assert stimmt, text

# stoerungsfenster: das Fenster liegt vor allen Einträgen
stimmt, text = pruefe_fenster(BEISPIEL, "00:00:00", "03:00:00")
assert stimmt, text

# stoerungsfenster: das Fenster liegt nach allen Einträgen
stimmt, text = pruefe_fenster(BEISPIEL, "04:00:00", "23:59:59")
assert stimmt, text

# stoerungsfenster: ohne Geräte
stimmt, text = pruefe_fenster({}, "00:00:00", "23:59:59")
assert stimmt, text

# stoerungsfenster hört nach bis auf
protokolle = zufallsprotokolle(zufall, 4, 4000, 36000)
zaehlprotokolle = als_zaehllisten(protokolle)
bis = "03:01:00"
noetig = len([eintrag for eintrag in vergleich(protokolle) if eintrag[0] <= bis])
try:
    ergebnis = stoerungsfenster(zaehlprotokolle, "03:00:30", bis)
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert isinstance(ergebnis, list) and gelesen(zaehlprotokolle) <= 2 * noetig + 2 * 4, (
    f"Bis {bis} gibt es {noetig} von 4000 Einträgen, stoerungsfenster hat aber {gelesen(zaehlprotokolle)} gelesen"
    f"{'' if isinstance(ergebnis, list) else f' (Fehler: {ergebnis})'}; "
    f"erlaubt sind 2 · {noetig} + 2 · 4 = {2 * noetig + 8}.\n"
    "Tipp: Gehen Sie mit for durch zeitleiste(protokolle) und brechen Sie mit break ab, sobald ein Zeitstempel "
    "nach bis kommt."
)

# Die Ausgabe des Programms
erwartet = "\n".join(str(eintrag) for eintrag in vergleich(BEISPIEL))
erwartet += "\n" + str(vergleich_fenster(BEISPIEL, "03:12:08", "03:12:09"))
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Protokolle
for _ in range(300):
    protokolle = zufallsprotokolle(zufall, zufall.randint(0, 6), zufall.randint(0, 15), zufall.choice([3, 10, 100]))
    stimmt, text = pruefe(protokolle)
    assert stimmt, text
    von = zeit(10800 + zufall.randrange(12))
    bis = zeit(10800 + zufall.randrange(12) + 3)
    if von <= bis:
        stimmt, text = pruefe_fenster(protokolle, von, bis)
        assert stimmt, text

# Laufzeit: jeder Eintrag wird höchstens zweimal gelesen
protokolle = zufallsprotokolle(zufall, 100, 2000, 3600)
zaehlprotokolle = als_zaehllisten(protokolle)
try:
    ergebnis = list(zeitleiste(zaehlprotokolle))
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert isinstance(ergebnis, list) and gelesen(zaehlprotokolle) <= 2 * 2000, (
    f"Für 100 Geräte mit zusammen 2000 Einträgen hat zeitleiste {gelesen(zaehlprotokolle)} Einträge gelesen"
    f"{'' if isinstance(ergebnis, list) else f' (Fehler: {ergebnis})'}, erlaubt sind 2 · 2000 = 4000.\n"
    "Tipp: Suchen Sie nicht jedes Mal den kleinsten Kopf unter allen Protokollen, sondern holen Sie ihn mit heappop aus dem Heap."
)

# Laufzeit: O(N log k) Schritte statt O(N · k)
try:
    _, schritte = zaehle_schritte(lambda: list(zeitleiste(protokolle)))
except Exception as fehler:
    schritte = f"(Abbruch: {type(fehler).__name__}: {fehler})"
assert isinstance(schritte, int) and schritte <= 10 * (2000 + 100), (
    f"Für 100 Geräte mit zusammen 2000 Einträgen braucht zeitleiste {schritte} Schritte, erlaubt sind "
    "10 · (2000 + 100) = 21000.\nTipp: Mit einem Heap kostet jeder Eintrag nur ein heappop und ein heappush; "
    "wer die 100 Köpfe jedes Mal durchsucht oder die Protokolle paarweise zusammenführt, braucht das "
    "Hundertfache."
)

# Obere Grenze: 1000 Geräte mit zusammen 100 000 Einträgen
protokolle = zufallsprotokolle(zufall, 1000, 100000, 86400 - 10800)
ergebnis = leiste_von(protokolle)
erwartet = vergleich(protokolle)
assert ergebnis == erwartet, f"Bei 1000 Geräten und 100 000 Einträgen ergibt zeitleiste {abweichung(ergebnis, erwartet)}."
