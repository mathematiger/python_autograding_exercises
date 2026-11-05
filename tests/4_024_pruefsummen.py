# Automatisch erzeugt aus lehrkraft/muster/4_024_pruefsummen.py - nicht von Hand ändern.
# vorlage-hash: 61ee238e40c9df0b
# text-hash: 5c0fb0e247e6d609
# thema: funktionen
# inhalt: Dekoratoren mit eigenem Cache

def fehler_bei(aufruf):
    """Führt aufruf() aus und gibt die ausgelöste Ausnahme zurück, sonst None."""
    try:
        aufruf()
    except Exception as fehler:
        return fehler
    return None


# Die Ausgabe des Programms stimmt
ssl = pruefsumme(b"libssl 3.0")[:8]
libc = pruefsumme(b"libc 2.39")[:8]
erwartete_ausgabe = f"{ssl}\n{ssl}\n{libc}\n{ssl}\n2 2 pruefsumme"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"

@zaehle
def addiere(a, b=0, *, c=0):
    """Addiert drei Zahlen."""
    return a + b + c


# zaehle zählt jeden Aufruf und reicht Argumente und Ergebnis durch
vorher = getattr(addiere, "aufrufe", None)
ergebnisse = (addiere(1), addiere(1, 2), addiere(a=1, b=2, c=3))
assert vorher == 0 and ergebnisse == (1, 3, 6) and addiere.aufrufe == 3, (
    f"Mit @zaehle ist addiere.aufrufe zuerst {vorher!r}; addiere(1), addiere(1, 2) und addiere(a=1, b=2, c=3) ergeben "
    f"{ergebnisse!r}, danach ist aufrufe {getattr(addiere, 'aufrufe', None)!r}; erwartet war 0, (1, 3, 6) und 3.\n"
    "Tipp: Setzen Sie huelle.aufrufe = 0, bevor Sie huelle zurückgeben, und erhöhen Sie es in der Hülle."
)

@zaehle
def lies(pfad):
    """Liest eine Datei, die es nicht gibt."""
    raise FileNotFoundError(pfad)


# zaehle zählt auch Aufrufe, die mit einer Ausnahme enden
fehler = (fehler_bei(lambda: lies("/etc/a")), fehler_bei(lambda: lies("/etc/b")))
assert all(isinstance(f, FileNotFoundError) for f in fehler) and lies.aufrufe == 2, (
    f"Zwei Aufrufe einer Funktion, die FileNotFoundError auslöst, ergeben {fehler!r} und aufrufe = {lies.aufrufe!r}; "
    "erwartet waren zwei FileNotFoundError und aufrufe = 2.\nTipp: Zählen Sie, bevor Sie funktion aufrufen."
)

# Jede gezählte Funktion hat ihren eigenen Zähler
eins = zaehle(len)
zwei = zaehle(len)
eins("abc")
eins("de")
zwei("f")
assert (eins.aufrufe, zwei.aufrufe) == (2, 1), (
    f"Zwei mit zaehle dekorierte Funktionen haben nach 2 und 1 Aufrufen die Zähler {(eins.aufrufe, zwei.aufrufe)!r}, "
    "erwartet war (2, 1).\nTipp: Der Zähler gehört an die Hüllfunktion, nicht in eine Variable auf Modulebene."
)

# zwischenspeicher ruft die Funktion für gleiche Argumente nur einmal auf
aufrufe = []


@zwischenspeicher
def langsam(daten, verfahren="sha256"):
    """Merkt sich jeden echten Aufruf und gibt die Prüfsumme zurück."""
    aufrufe.append((daten, verfahren))
    return hashlib.new(verfahren, daten).hexdigest()


ergebnisse = [langsam(b"a"), langsam(b"a"), langsam(b"b"), langsam(b"a", verfahren="md5"), langsam(b"a", verfahren="md5")]
erwartet = [pruefsumme(b"a"), pruefsumme(b"a"), pruefsumme(b"b"), hashlib.md5(b"a").hexdigest(), hashlib.md5(b"a").hexdigest()]
assert ergebnisse == erwartet and len(aufrufe) == 3, (
    f"Fünf Aufrufe mit drei verschiedenen Argumenten rufen die Funktion {len(aufrufe)}-mal auf ({aufrufe!r}); erwartet "
    "waren 3 Aufrufe und die richtigen Prüfsummen.\nTipp: Prüfen Sie mit schluessel in huelle.cache, ob es das Ergebnis schon gibt."
)

# Der cache hat die verlangten Schlüssel
schluessel = sorted(langsam.cache, key=repr)
erwartet = sorted([((b"a",), ()), ((b"b",), ()), ((b"a",), (("verfahren", "md5"),))], key=repr)
assert schluessel == erwartet, (
    f"Die Schlüssel in langsam.cache sind {schluessel!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Der Schlüssel ist (args, tuple(sorted(kwargs.items())))."
)

# Benannte Argumente in anderer Reihenfolge ergeben denselben Schlüssel
gezaehlt_kw = zaehle(lambda a=0, b=0: a - b)
gemerkt_kw = zwischenspeicher(gezaehlt_kw)
ergebnisse = (gemerkt_kw(a=5, b=2), gemerkt_kw(b=2, a=5))
assert ergebnisse == (3, 3) and gezaehlt_kw.aufrufe == 1, (
    f"f(a=5, b=2) und f(b=2, a=5) ergeben {ergebnisse!r} mit {gezaehlt_kw.aufrufe} echten Aufrufen, erwartet war "
    "(3, 3) mit einem Aufruf.\nTipp: sorted(kwargs.items()) bringt die benannten Argumente in eine feste Reihenfolge."
)

# Auch None, 0 und "" werden gemerkt
for ergebnis_original in [None, 0, "", False]:
    innen = zaehle(lambda x, wert=ergebnis_original: wert)
    aussen = zwischenspeicher(innen)
    ergebnisse = (aussen(1), aussen(1), aussen(1))
    assert ergebnisse == (ergebnis_original,) * 3 and innen.aufrufe == 1, (
        f"Eine Funktion, die {ergebnis_original!r} zurückgibt, wird bei drei gleichen Aufrufen {innen.aufrufe}-mal "
        f"aufgerufen (Ergebnisse {ergebnisse!r}); erwartet war ein einziger Aufruf.\n"
        "Tipp: cache.get(schluessel) ist auch dann falsch, wenn das gemerkte Ergebnis None oder 0 ist; prüfen Sie mit in."
    )

# Ausnahmen werden nicht gemerkt, sondern weitergegeben
versuche = []


@zwischenspeicher
def unzuverlaessig(server):
    """Scheitert beim ersten Versuch, klappt beim zweiten."""
    versuche.append(server)
    if len(versuche) == 1:
        raise ConnectionError(server)
    return f"ok {server}"


erster = fehler_bei(lambda: unzuverlaessig("srv1"))
zweiter = unzuverlaessig("srv1")
dritter = unzuverlaessig("srv1")
assert isinstance(erster, ConnectionError) and (zweiter, dritter) == ("ok srv1", "ok srv1") and len(versuche) == 2, (
    f"Erster Aufruf: {erster!r}, zweiter {zweiter!r}, dritter {dritter!r}, insgesamt {len(versuche)} echte Aufrufe; "
    "erwartet war ConnectionError, dann zweimal 'ok srv1' mit insgesamt 2 echten Aufrufen.\n"
    "Tipp: Speichern Sie das Ergebnis erst, wenn funktion ohne Ausnahme fertig ist."
)

# cache_leeren leert den cache, danach wird neu gerechnet
innen = zaehle(pruefsumme)
aussen = zwischenspeicher(innen)
aussen(b"x")
aussen(b"y")
leeren = getattr(aussen, "cache_leeren", None)
if callable(leeren):
    leeren()
nach_leeren = dict(aussen.cache)
aussen(b"x")
assert callable(leeren) and nach_leeren == {} and innen.aufrufe == 3 and len(aussen.cache) == 1, (
    f"Nach cache_leeren() ist der cache {nach_leeren!r}; insgesamt {innen.aufrufe} echte Aufrufe für x, y, (leeren), x; "
    "erwartet war ein leerer cache und 3 echte Aufrufe.\nTipp: Hängen Sie eine innere Funktion ohne Argumente als "
    "huelle.cache_leeren an, die huelle.cache.clear() aufruft."
)

# Jede Funktion hat ihren eigenen cache
erste = zwischenspeicher(lambda x: x + 1)
zweite = zwischenspeicher(lambda x: x * 10)
ergebnisse = (erste(3), zweite(3))
assert ergebnisse == (4, 30) and erste.cache is not zweite.cache, (
    f"Zwei Funktionen mit zwischenspeicher ergeben für 3 die Werte {ergebnisse!r}, erwartet war (4, 30).\n"
    "Tipp: Legen Sie den cache im Dekorator für jede Hüllfunktion neu an, nicht einmal für alle."
)

# functools.wraps übernimmt Name und Docstring
angaben = (langsam.__name__, langsam.__doc__, addiere.__name__)
erwartet = ("langsam", "Merkt sich jeden echten Aufruf und gibt die Prüfsumme zurück.", "addiere")
assert angaben == erwartet, (
    f"Name und Docstring der dekorierten Funktionen sind {angaben!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Schreiben Sie @functools.wraps(funktion) über jede Hüllfunktion."
)

# Viele zufällige Aufrufe: so viele echte Aufrufe wie verschiedene Argumente
zufall = Zufall(4024)
for _ in range(100):
    innen = zaehle(lambda a, b=1: a * b)
    aussen = zwischenspeicher(innen)
    verschiedene = set()
    for _ in range(zufall.randint(0, 30)):
        a = zufall.randint(-3, 3)
        if zufall.random() < 0.5:
            ergebnis = aussen(a)
            verschiedene.add(((a,), ()))
            erwartet = a
        else:
            b = zufall.randint(0, 2)
            ergebnis = aussen(a, b=b)
            verschiedene.add(((a,), (("b", b),)))
            erwartet = a * b
        assert ergebnis == erwartet, f"Der Aufruf mit a={a} ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    assert innen.aufrufe == len(verschiedene) and set(aussen.cache) == verschiedene, (
        f"Bei {len(verschiedene)} verschiedenen Argumenten wurde die Funktion {innen.aufrufe}-mal aufgerufen, der cache "
        f"hat {len(aussen.cache)} Einträge; erwartet war genau ein Aufruf und ein Eintrag je verschiedenem Argument."
    )

# An der oberen Grenze: 100 000 Aufrufe mit 10 000 verschiedenen Argumenten
innen = zaehle(pruefsumme)
aussen = zwischenspeicher(innen)
for nummer in range(100000):
    aussen(b"datei %d" % (nummer % 10000))
assert innen.aufrufe == 10000 and len(aussen.cache) == 10000 and aussen(b"datei 42") == pruefsumme(b"datei 42"), (
    f"100 000 Aufrufe mit 10 000 verschiedenen Dateien rechnen {innen.aufrufe}-mal, der cache hat {len(aussen.cache)} "
    "Einträge; erwartet waren je 10 000."
)
