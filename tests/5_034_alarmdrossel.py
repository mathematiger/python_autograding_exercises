# Automatisch erzeugt aus lehrkraft/muster/5_034_alarmdrossel.py - nicht von Hand ändern.
# vorlage-hash: 2b315ffb4203a294
# text-hash: b0d08f5ddb13f086
# thema: funktionen
# inhalt: Methoden-Dekorator, Zustand je Objekt

def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


class Testfehler(Exception):
    """Eine Ausnahme, die nur im Test vorkommt."""


def baue_klasse():
    """Baut eine Testklasse mit zwei verschieden stark gedrosselten Methoden; ein Fehler wird als Text zurückgegeben."""
    try:

        class Kanal:
            """Ein Alarmkanal für die Tests."""

            def __init__(self, server):
                """Merkt sich den Server und legt die Liste der Ereignisse an."""
                self.server = server
                self.ereignisse = []

            @drosseln(2)
            def sms(self, text, *, prioritaet="normal"):
                """Schickt eine SMS."""
                self.ereignisse.append(("sms", text, prioritaet))
                return len(self.ereignisse)

            @drosseln(1)
            def anruf(self, nummer):
                """Ruft die Bereitschaft an; die Nummer 0 gibt es nicht."""
                if nummer == 0:
                    raise Testfehler("keine gültige Nummer")
                self.ereignisse.append(("anruf", nummer))
                return "verbunden"

            @drosseln(0)
            def pager(self):
                """Ist abgeschaltet."""
                self.ereignisse.append(("pager",))
                return "piep"

    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"
    return Kanal


def baue_unhashbar():
    """Baut eine unhashbare Klasse mit __eq__ und ohne __hash__; ein Fehler wird als Text zurückgegeben."""
    try:

        class Messpunkt:
            """Zwei Messpunkte sind gleich, wenn sie gleich heißen."""

            def __init__(self, name):
                """Merkt sich den Namen."""
                self.name = name
                self.meldungen = 0

            def __eq__(self, anderer):
                """Vergleicht über den Namen."""
                return isinstance(anderer, Messpunkt) and anderer.name == self.name

            @drosseln(1)
            def melde(self):
                """Meldet einmal."""
                self.meldungen += 1
                return self.meldungen

    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"
    return Messpunkt


Kanal = baue_klasse()
Messpunkt = baue_unhashbar()

# Die Methode läuft und gibt ihr Ergebnis zurück
web = Kanal("web01")
ergebnis = wert_von(lambda: web.sms("CPU 98 %"))
assert ergebnis == 1 and web.ereignisse == [("sms", "CPU 98 %", "normal")], (
    f"Der erste Aufruf von sms ergibt {ergebnis!r} und die Ereignisse {web.ereignisse!r}, erwartet war 1 und eine SMS.\n"
    "Tipp: drosseln(maximal) gibt einen Dekorator zurück, der Dekorator die Hülle, die Hülle ruft methode(self, *args, **kwargs) auf."
)

# Bis maximal läuft die Methode, danach gibt sie None zurück
ergebnis = [wert_von(lambda: web.sms("CPU 99 %")), wert_von(lambda: web.sms("CPU 99 %")), wert_von(lambda: web.sms("CPU 100 %"))]
assert ergebnis == [2, None, None] and len(web.ereignisse) == 2, (
    f"Der zweite bis vierte Aufruf von sms ergeben {ergebnis!r} bei {len(web.ereignisse)} gesendeten SMS, erwartet war [2, None, None] bei 2.\n"
    "Tipp: Ab maximal ausgeführten Aufrufen wird die Methode nicht mehr aufgerufen."
)

# Schlüsselwortargumente kommen an (eigene Klasse, damit nur das geprüft wird)
kanal = baue_klasse()("vpn")
wert_von(lambda: kanal.sms("Tunnel weg", prioritaet="hoch"))
assert kanal.ereignisse == [("sms", "Tunnel weg", "hoch")], f"sms('Tunnel weg', prioritaet='hoch') ergibt die Ereignisse {kanal.ereignisse!r}."

# Ein anderes Objekt hat eigene Zähler
db = Kanal("db01")
ergebnis = [wert_von(lambda: db.sms("Platte voll")), wert_von(lambda: db.sms("Platte voll")), wert_von(lambda: db.sms("x"))]
assert ergebnis == [1, 2, None], (
    f"Nachdem web01 gedrosselt ist, ergeben drei Aufrufe von sms bei db01 {ergebnis!r}, erwartet war [1, 2, None].\n"
    "Tipp: Ein Zähler im Closure des Dekorators gilt für alle Objekte; legen Sie ihn in self.__dict__ ab."
)

# Jede Methode hat eigene Zähler und ihr eigenes maximal
kanal = Kanal("mail")
ergebnis = [wert_von(lambda: kanal.sms("a")), wert_von(lambda: kanal.anruf(110)), wert_von(lambda: kanal.anruf(110)), wert_von(lambda: kanal.sms("b"))]
assert ergebnis == [1, "verbunden", None, 3], (
    f"sms, anruf, anruf, sms ergeben {ergebnis!r}, erwartet war [1, 'verbunden', None, 3] (anruf darf einmal, sms zweimal).\n"
    "Tipp: Führen Sie die Zähler je Methode, etwa unter methode.__name__."
)

# maximal 0: die Methode läuft nie
kanal = Kanal("alt")
ergebnis = [wert_von(lambda: kanal.pager()), wert_von(lambda: kanal.pager())]
assert ergebnis == [None, None] and kanal.ereignisse == [], f"Mit drosseln(0) ergibt pager {ergebnis!r} und die Ereignisse {kanal.ereignisse!r}, erwartet war nie ausgeführt."

# Der Zustand liegt im Attribut _drossel des Objekts
assert "_drossel" in vars(web), (
    f"Nach den Aufrufen hat web01 die Attribute {sorted(vars(web))}, erwartet war auch _drossel.\n"
    'Tipp: self.__dict__.setdefault("_drossel", {}).'
)

# unterdrueckt zählt die unterdrückten Aufrufe je Objekt und Methode
ergebnis = wert_von(lambda: [unterdrueckt(web, "sms"), unterdrueckt(db, "sms"), unterdrueckt(web, "anruf"), unterdrueckt(Kanal("neu"), "sms")])
assert ergebnis == [2, 1, 0, 0], (
    f"unterdrueckt für web01/sms, db01/sms, web01/anruf und ein neues Objekt ergibt {ergebnis!r}, erwartet war [2, 1, 0, 0]."
)

# freigeben setzt die Zähler eines Objekts zurück
freigeben(web)
ergebnis = [wert_von(lambda: unterdrueckt(web, "sms")), wert_von(lambda: web.sms("CPU 97 %")), wert_von(lambda: web.sms("CPU 96 %"))]
assert ergebnis == [0, 3, 4], (
    f"Nach freigeben(web) ergeben unterdrueckt und zwei Aufrufe von sms {ergebnis!r}, erwartet war [0, 3, 4].\n"
    "Tipp: Löschen Sie den Eintrag _drossel des Objekts oder setzen Sie alle seine Zähler auf 0."
)

# freigeben lässt andere Objekte unberührt
ergebnis = [wert_von(lambda: db.sms("y")), wert_von(lambda: unterdrueckt(db, "sms"))]
assert ergebnis == [None, 2], f"Nach freigeben(web) ergeben sms und unterdrueckt bei db01 {ergebnis!r}, erwartet war [None, 2]."

# freigeben auf einem Objekt, das noch nie gedrosselt wurde
neu = Kanal("neu")
ergebnis = wert_von(lambda: freigeben(neu))
assert ergebnis is None and wert_von(lambda: neu.sms("a")) == 1, f"freigeben auf einem unbenutzten Objekt ergibt {ergebnis!r}, erwartet war kein Fehler."

# Ein Aufruf mit Ausnahme zählt als ausgeführt, die Ausnahme fliegt weiter
kanal = Kanal("dns")
ergebnis = [wert_von(lambda: kanal.anruf(0)), wert_von(lambda: kanal.anruf(112))]
assert ergebnis == ["Testfehler: keine gültige Nummer", None], (
    f"anruf(0) und danach anruf(112) ergeben {ergebnis!r}, erwartet war der Testfehler und danach None.\n"
    "Tipp: Zählen Sie den Aufruf, bevor Sie die Methode aufrufen."
)

# Unhashbare Objekte funktionieren
eins, zwei = Messpunkt("raum1"), Messpunkt("raum1")
ergebnis = [wert_von(lambda: eins.melde()), wert_von(lambda: eins.melde()), wert_von(lambda: zwei.melde())]
assert ergebnis == [1, None, 1], (
    f"Bei zwei gleichen, aber unhashbaren Objekten ergibt melde {ergebnis!r}, erwartet war [1, None, 1].\n"
    "Tipp: Ein Dictionary {self: zaehler} im Dekorator scheitert hier; der Zustand gehört in self.__dict__."
)

# Name, Docstring und __wrapped__ bleiben erhalten
methode = Kanal.__dict__["sms"]
ergebnis = (methode.__name__, methode.__doc__, getattr(methode, "__wrapped__", None) is not None)
assert ergebnis == ("sms", "Schickt eine SMS.", True), f"Die dekorierte Methode hat Name, Docstring, __wrapped__ = {ergebnis!r}.\nTipp: functools.wraps(methode)."

# Die Methode lässt sich auch über die Klasse aufrufen
kanal = Kanal("lb")
ergebnis = [wert_von(lambda: Kanal.sms(kanal, "a")), wert_von(lambda: kanal.sms("b")), wert_von(lambda: Kanal.sms(kanal, "c"))]
assert ergebnis == [1, 2, None], f"Kanal.sms(kanal, …) und kanal.sms(…) im Wechsel ergeben {ergebnis!r}, erwartet war [1, 2, None]."

# Gelöschte Objekte vererben ihre Zähler nicht an neue
ergebnisse = []
for _ in range(50):
    kanal = Kanal("tmp")
    wert_von(lambda: [kanal.anruf(1), kanal.anruf(1)])
    del kanal
    ergebnisse.append(wert_von(lambda: Kanal("tmp").anruf(2)))
assert ergebnisse == ["verbunden"] * 50, (
    f"Neue Objekte bekommen bei anruf unter anderem {sorted(set(map(repr, ergebnisse)))}, erwartet war jedes Mal 'verbunden'.\n"
    "Tipp: id(self) als Schlüssel kann ein gelöschtes Objekt mit einem neuen verwechseln."
)

# Die Ausgabe des Programms
erwartet = "1\n2\nNone\n1\n1\n3"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Aufrufe auf mehreren Objekten, verglichen mit einem Modell
zufall = Zufall(5034)
grenzen = {"sms": 2, "anruf": 1, "pager": 0}
for _ in range(40):
    kanaele = [Kanal(f"s{nummer}") for nummer in range(zufall.randint(1, 4))]
    modell = [{name: [0, 0] for name in grenzen} for _ in kanaele]
    for _ in range(zufall.randint(0, 30)):
        stelle = zufall.randrange(len(kanaele))
        aktion = zufall.choice(["sms", "anruf", "pager", "freigeben", "zaehlen"])
        kanal = kanaele[stelle]
        if aktion == "freigeben":
            wert_von(lambda: freigeben(kanal))
            modell[stelle] = {name: [0, 0] for name in grenzen}
            continue
        if aktion == "zaehlen":
            name = zufall.choice(list(grenzen))
            ergebnis = wert_von(lambda: unterdrueckt(kanal, name))
            assert ergebnis == modell[stelle][name][1], f"unterdrueckt(…, {name!r}) ergibt {ergebnis!r}, erwartet war {modell[stelle][name][1]}."
            continue
        zaehler = modell[stelle][aktion]
        laeuft = zaehler[0] < grenzen[aktion]
        vorher = len(kanal.ereignisse)
        argumente = {"sms": ("t",), "anruf": (5,), "pager": ()}[aktion]
        ergebnis = wert_von(lambda: getattr(kanal, aktion)(*argumente))
        if laeuft:
            zaehler[0] += 1
        else:
            zaehler[1] += 1
        assert (len(kanal.ereignisse) > vorher) == laeuft and (ergebnis is None) != laeuft, (
            f"Aufruf {aktion} bei {kanal.server} ergibt {ergebnis!r}; erwartet war, dass er {'läuft' if laeuft else 'unterdrückt wird'}."
        )

# Obere Grenze: 10 000 Objekte mit je zehn Aufrufen
kanaele = [Kanal(f"srv{nummer}") for nummer in range(10000)]
for kanal in kanaele:
    for _ in range(5):
        kanal.sms("x")
        kanal.anruf(7)
ergebnis = [sum(len(kanal.ereignisse) for kanal in kanaele), sum(unterdrueckt(kanal, "sms") + unterdrueckt(kanal, "anruf") for kanal in kanaele)]
assert ergebnis == [30000, 70000], f"Bei 10 000 Objekten mit je 5 sms und 5 anruf ergeben sich {ergebnis[0]} ausgeführte und {ergebnis[1]} unterdrückte Aufrufe, erwartet war 30 000 und 70 000."
