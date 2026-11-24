# Automatisch erzeugt aus lehrkraft/muster/5_051_funkprofil.py - nicht von Hand ändern.
# vorlage-hash: bd5e94c4feacd318
# text-hash: 91cb878e9e48326e
# thema: klassen
# inhalt: Deskriptoren in dataclasses

def versuche(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(*argumente), None
    except Exception as ausnahme:
        return None, ausnahme


def setze(objekt, name, wert):
    """Weist objekt.name = wert zu; liefert die Ausnahme oder None."""
    try:
        setattr(objekt, name, wert)
    except Exception as ausnahme:
        return ausnahme
    return None


def beschreibe(ausnahme):
    """Beschreibt eine Ausnahme kurz für Meldungen."""
    if ausnahme is None:
        return "keine Ausnahme"
    return f"{type(ausnahme).__name__}: {ausnahme}"


def werte(ap):
    """Liefert die drei Bereich-Felder eines Accesspoints als Tupel; bei einem Fehler dessen Beschreibung."""
    try:
        return (ap.kanal, ap.sendeleistung, ap.max_geraete)
    except Exception as ausnahme:
        return beschreibe(ausnahme)


TIPP_STANDARD = (
    "\nTipp: @dataclass holt den Standardwert mit getattr(Accesspoint, 'sendeleistung'), also über "
    "__get__(None, Accesspoint). Geben Sie bei objekt None den Standardwert zurück, nicht den Deskriptor."
)

# erlaubt: Werte im Bereich und an seinen Grenzen
bereich = Bereich(1, 13)
ergebnisse = [versuche(bereich.erlaubt, wert)[0] for wert in [6, 1, 13]]
assert ergebnisse == [True, True, True], (
    f"Bereich(1, 13).erlaubt(6), (1) und (13) ergeben {ergebnisse}, erwartet [True, True, True] "
    "(die Grenzen gehören dazu)."
)

# erlaubt: Werte außerhalb des Bereichs
ergebnisse = [versuche(bereich.erlaubt, wert)[0] for wert in [0, 14, -5]]
assert ergebnisse == [False, False, False], (
    f"Bereich(1, 13).erlaubt(0), (14) und (-5) ergeben {ergebnisse}, erwartet [False, False, False]."
)

# erlaubt: nur ganze Zahlen, kein bool, keine Kommazahl, kein Text, nicht None
ergebnisse = [versuche(bereich.erlaubt, wert)[0] for wert in [True, 6.0, "6", None]]
assert ergebnisse == [False, False, False, False], (
    f"Bereich(1, 13).erlaubt(True), (6.0), ('6') und (None) ergeben {ergebnisse}, erwartet viermal False.\n"
    "Tipp: Prüfen Sie zuerst isinstance(wert, int) und schließen Sie bool aus (True ist auch ein int); "
    "vergleichen Sie erst danach, sonst stürzt '6' < 1 ab."
)

# Accesspoint("Flur-OG2", 6) aus der Aufgabe: kanal gesetzt, die anderen Felder mit Standardwert
ap, fehler = versuche(Accesspoint, "Flur-OG2", 6)
assert fehler is None and werte(ap) == (6, 17, 64), (
    "Accesspoint('Flur-OG2', 6) soll kanal=6, sendeleistung=17 und max_geraete=64 ergeben; "
    + (f"bekommen: {beschreibe(fehler)}." if fehler else f"bekommen: {werte(ap)!r}.")
    + TIPP_STANDARD
)

# Alle Felder angegeben
ap, fehler = versuche(Accesspoint, "Treppenhaus", 1, 20, 250)
assert fehler is None and werte(ap) == (1, 20, 250), (
    "Accesspoint('Treppenhaus', 1, 20, 250) soll kanal=1, sendeleistung=20 und max_geraete=250 ergeben; "
    + (f"bekommen: {beschreibe(fehler)}." if fehler else f"bekommen: {werte(ap)!r}.")
)

# Spätere Zuweisung eines erlaubten Werts wirkt
ap = Accesspoint("Flur-OG2", 6)
fehler = setze(ap, "kanal", 11)
assert fehler is None and werte(ap) == (11, 17, 64), (
    f"Nach ap.kanal = 11 erwartet kanal=11, bekommen: {beschreibe(fehler) if fehler else werte(ap)!r}."
)

# Jedes Objekt hat seine eigenen Werte (nicht im Deskriptor speichern)
a = Accesspoint("A", 1)
b = Accesspoint("B", 13, 5, 10)
assert (werte(a), werte(b)) == ((1, 17, 64), (13, 5, 10)), (
    f"Zwei Accesspoints teilen sich Werte: a ergibt {werte(a)!r}, b ergibt {werte(b)!r}, erwartet (1, 17, 64) "
    "und (13, 5, 10).\nTipp: Speichern Sie den Wert im Objekt (objekt), nicht in self."
)

# repr der Datenklasse zeigt die Werte
text = repr(Accesspoint("Flur-OG2", 6))
assert text == "Accesspoint(name='Flur-OG2', kanal=6, sendeleistung=17, max_geraete=64)", (
    f"repr(Accesspoint('Flur-OG2', 6)) ergibt {text!r}, erwartet war "
    "\"Accesspoint(name='Flur-OG2', kanal=6, sendeleistung=17, max_geraete=64)\"."
)

# == der Datenklasse vergleicht die Werte
gleich = Accesspoint("A", 6) == Accesspoint("A", 6, 17, 64)
verschieden = Accesspoint("A", 6) == Accesspoint("A", 7)
assert gleich and not verschieden, (
    f"Accesspoint('A', 6) == Accesspoint('A', 6, 17, 64) ergibt {gleich}, erwartet True; "
    f"Accesspoint('A', 6) == Accesspoint('A', 7) ergibt {verschieden}, erwartet False."
)

# Zugriff über die Klasse liefert den Standardwert
assert (Accesspoint.sendeleistung, Accesspoint.max_geraete) == (17, 64), (
    f"Accesspoint.sendeleistung und Accesspoint.max_geraete ergeben {Accesspoint.sendeleistung!r} und "
    f"{Accesspoint.max_geraete!r}, erwartet 17 und 64." + TIPP_STANDARD
)

# Zuweisung außerhalb des Bereichs: ValueError
ap = Accesspoint("Flur-OG2", 6)
fehler = setze(ap, "kanal", 14)
assert isinstance(fehler, ValueError), f"ap.kanal = 14 soll einen ValueError auslösen, bekommen: {beschreibe(fehler)}."

# Die Meldung nennt den Feldnamen
ap = Accesspoint("Flur-OG2", 6)
fehler = setze(ap, "max_geraete", 251)
assert isinstance(fehler, ValueError) and vergleichbar("max_geraete") in vergleichbar(str(fehler)), (
    f"ap.max_geraete = 251 soll einen ValueError mit 'max_geraete' in der Meldung auslösen, bekommen: "
    f"{beschreibe(fehler)}.\nTipp: Den Feldnamen bekommt der Deskriptor in __set_name__."
)

# Die Meldung nennt beide Grenzen
fehler = setze(Accesspoint("Flur-OG2", 6), "sendeleistung", 0)
assert isinstance(fehler, ValueError) and "1" in str(fehler) and "20" in str(fehler), (
    f"ap.sendeleistung = 0 soll einen ValueError auslösen, dessen Meldung die Grenzen 1 und 20 nennt, "
    f"bekommen: {beschreibe(fehler)}."
)

# Nach einem abgelehnten Wert bleibt der alte
ap = Accesspoint("Flur-OG2", 6)
setze(ap, "kanal", 0)
assert werte(ap) == (6, 17, 64), (
    f"Nach dem abgelehnten ap.kanal = 0 erwartet kanal=6, bekommen: {werte(ap)!r}.\n"
    "Tipp: Erst prüfen, dann speichern."
)

# Die Grenzen selbst sind erlaubt, knapp daneben nicht
ap = Accesspoint("Flur-OG2", 6)
ergebnisse = []
for wert in [1, 13, 0, 14]:
    ergebnisse.append(setze(ap, "kanal", wert) is None)
assert ergebnisse == [True, True, False, False], (
    "kanal = 1, 13, 0, 14: erwartet erlaubt, erlaubt, ValueError, ValueError (von 1 bis 13 einschließlich); "
    f"erlaubt war: {ergebnisse}."
)

# Auch der Konstruktor prüft
_, fehler = versuche(Accesspoint, "Lager", 6, 25)
assert isinstance(fehler, ValueError), (
    f"Accesspoint('Lager', 6, 25) soll einen ValueError auslösen (sendeleistung 25 > 20), bekommen: "
    f"{beschreibe(fehler)}."
)

# kanal ist ein Pflichtfeld: ohne kanal ein TypeError
_, fehler = versuche(Accesspoint, "Lager")
assert isinstance(fehler, TypeError), (
    f"Accesspoint('Lager') soll wie bei jedem Pflichtfeld einen TypeError auslösen, bekommen: {beschreibe(fehler)}.\n"
    "Tipp: Ohne Standardwert muss __get__(None, Accesspoint) einen AttributeError auslösen; dann gibt @dataclass "
    "dem Feld keinen Standardwert."
)

# Kommazahlen, bool, Texte und None sind keine erlaubten Werte
ap = Accesspoint("Flur-OG2", 6)
falsch_angenommen = []
for wert in [6.0, True, "6", None]:
    fehler = setze(ap, "kanal", wert)
    if not isinstance(fehler, ValueError):
        falsch_angenommen.append(f"{wert!r} → {beschreibe(fehler)}")
assert falsch_angenommen == [] and werte(ap) == (6, 17, 64), (
    "kanal = 6.0, True, '6' und None sollen je einen ValueError auslösen und kanal bei 6 lassen; nicht so bei: "
    f"{'; '.join(falsch_angenommen) or 'Wert danach ' + repr(werte(ap))}.\n"
    "Tipp: Prüfen Sie zuerst isinstance(wert, int) und schließen Sie bool aus (True ist auch ein int)."
)

# Ein Standardwert außerhalb des Bereichs wird schon beim Anlegen abgelehnt
_, fehler = versuche(Bereich, 1, 13, 14)
_, fehler_unten = versuche(Bereich, 1, 13, 0)
assert isinstance(fehler, ValueError) and isinstance(fehler_unten, ValueError), (
    f"Bereich(1, 13, standard=14) und Bereich(1, 13, standard=0) sollen einen ValueError auslösen, bekommen: "
    f"{beschreibe(fehler)} und {beschreibe(fehler_unten)}."
)

# Standardwerte an den Grenzen sind erlaubt
_, fehler = versuche(Bereich, 1, 13, 1)
_, fehler_oben = versuche(Bereich, 1, 13, 13)
assert fehler is None and fehler_oben is None, (
    f"Bereich(1, 13, standard=1) und Bereich(1, 13, standard=13) sind erlaubt, bekommen: "
    f"{beschreibe(fehler)} und {beschreibe(fehler_oben)}."
)

# Derselbe Deskriptor funktioniert in einer anderen Datenklasse mit negativen Grenzen
try:
    @dataclass
    class Funkmessung:
        signal: int = Bereich(-100, -30)
        rauschen: int = Bereich(-120, -50, standard=-95)

    m = Funkmessung(-67)
    messwerte = (m.signal, m.rauschen)
    fehler = setze(m, "signal", -20)
    meldung = beschreibe(fehler)
    ergebnis = messwerte == (-67, -95) and isinstance(fehler, ValueError) and vergleichbar("signal") in vergleichbar(meldung)
except Exception as ausnahme:
    ergebnis, messwerte, meldung = False, None, beschreibe(ausnahme)
assert ergebnis, (
    "In einer zweiten Datenklasse mit signal = Bereich(-100, -30) und rauschen = Bereich(-120, -50, standard=-95) "
    f"erwartet Funkmessung(-67) → (-67, -95) und bei signal = -20 ein ValueError mit 'signal'; bekommen: "
    f"{messwerte!r}, {meldung}."
)

# Viele zufällige Zuweisungen an mehrere Accesspoints, verglichen mit dem erwarteten Stand
zufall = Zufall(5051)
grenzen = {"kanal": (1, 13), "sendeleistung": (1, 20), "max_geraete": (1, 250)}
geraete = [Accesspoint(f"AP{nummer}", 1) for nummer in range(4)]
erwartet = [{"kanal": 1, "sendeleistung": 17, "max_geraete": 64} for _ in range(4)]
schritte = []
fehlerfall = None
for _ in range(2000):
    nummer = zufall.randrange(4)
    name = zufall.choice(list(grenzen))
    unten, oben = grenzen[name]
    wert = zufall.choice([
        zufall.randint(unten - 2, oben + 2),
        zufall.randint(-10**18, 10**18),
        zufall.choice([float(unten), True, False, "5", None, 2.5]),
    ])
    schritte = (schritte + [f"ap{nummer}.{name} = {wert!r}"])[-4:]
    gueltig = type(wert) is int and unten <= wert <= oben
    fehler = setze(geraete[nummer], name, wert)
    if gueltig:
        erwartet[nummer][name] = wert
    bekommen = [{feld: getattr(ap, feld) for feld in grenzen} for ap in geraete]
    if (fehler is None) != gueltig or (fehler is not None and not isinstance(fehler, ValueError)) or bekommen != erwartet:
        fehlerfall = (schritte, gueltig, beschreibe(fehler), erwartet[nummer], bekommen[nummer])
        break
assert fehlerfall is None, (
    f"Nach den letzten Zuweisungen {'; '.join(fehlerfall[0])} (ap0 bis ap3 sind vier Accesspoints):\n"
    f"  beim letzten Schritt erwartet {'keine Ausnahme' if fehlerfall[1] else 'ein ValueError'}, bekommen: "
    f"{fehlerfall[2]}\n  Werte erwartet {fehlerfall[3]}\n  bekommen       {fehlerfall[4]}"
)

# Obere Grenze: riesige Zahlen und 10 000 Accesspoints
_, fehler = versuche(Accesspoint, "Riese", 10**18)
liste = [Accesspoint(f"AP{nummer}", nummer % 13 + 1, nummer % 20 + 1) for nummer in range(10000)]
stimmt = all(ap.kanal == nummer % 13 + 1 and ap.sendeleistung == nummer % 20 + 1 for nummer, ap in enumerate(liste))
assert isinstance(fehler, ValueError) and stimmt, (
    f"Accesspoint('Riese', 10**18) soll einen ValueError auslösen (bekommen: {beschreibe(fehler)}), und 10 000 "
    f"Accesspoints sollen je ihre eigenen Werte behalten (stimmt: {stimmt})."
)

# Die Ausgabe des Programms stimmt
assert AUSGABE.strip() == "Accesspoint(name='Flur-OG2', kanal=6, sendeleistung=17, max_geraete=64)", (
    "Erwartete Ausgabe: Accesspoint(name='Flur-OG2', kanal=6, sendeleistung=17, max_geraete=64) – "
    f"Ihr Programm: {AUSGABE!r}"
)
