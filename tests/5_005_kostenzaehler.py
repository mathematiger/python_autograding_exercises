# Automatisch erzeugt aus lehrkraft/muster/5_005_kostenzaehler.py - nicht von Hand ändern.
# vorlage-hash: 1ef0fc8057062ca8
# text-hash: ecd99bcb7f591cef
# thema: klassen
# inhalt: `__getattr__`, Proxy-Objekt

import copy


def neuer_dienst():
    """Gibt einen Kostenzaehler um einen frischen Speicherdienst mit den Preisen aus der Aufgabe zurück."""
    return Kostenzaehler(Speicherdienst("eu-central"), dict(PREISE))


# __init__ legt die vier Attribute an
dienst = neuer_dienst()
ergebnis = (type(dienst.__dict__.get("ziel")).__name__, dienst.__dict__.get("preise"), dienst.__dict__.get("kosten"), dienst.__dict__.get("aufrufe"))
assert ergebnis == ("Speicherdienst", PREISE, 0, {}), (
    f"Nach Kostenzaehler(Speicherdienst(...), PREISE) sind ziel, preise, kosten und aufrufe im __dict__: {ergebnis}; "
    f"erwartet war ('Speicherdienst', {PREISE}, 0, {{}})."
)

# Das Beispiel aus der Aufgabe
dienst = neuer_dienst()
ergebnis = (
    dienst.hochladen("bericht.pdf", b"PDF-Daten"),
    dienst.herunterladen("bericht.pdf"),
    dienst.auflisten(),
    dienst.region,
    dienst.kosten,
    dienst.aufrufe,
)
erwartet = (9, b"PDF-Daten", ["bericht.pdf"], "eu-central", 7, {"hochladen": 1, "herunterladen": 1})
assert ergebnis == erwartet, f"Das Beispiel aus der Aufgabe ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"

# Die Aufrufe landen wirklich beim Ziel
speicher = Speicherdienst("us-east")
dienst = Kostenzaehler(speicher, dict(PREISE))
dienst.hochladen("a.txt", b"abc")
assert speicher._dateien == {"a.txt": b"abc"}, (
    f"Nach dienst.hochladen('a.txt', b'abc') hat der echte Speicherdienst die Dateien {speicher._dateien!r}, "
    "erwartet war {'a.txt': b'abc'}."
)

# Kostenlose Methoden und Datenattribute kommen unverändert vom Ziel
speicher = Speicherdienst("us-east")
dienst = Kostenzaehler(speicher, dict(PREISE))
methode = dienst.auflisten
assert dienst.region == "us-east" and methode == speicher.auflisten and dienst.kosten == 0 and dienst.aufrufe == {}, (
    f"dienst.region ergibt {dienst.region!r}, dienst.auflisten ist {methode!r}; erwartet waren 'us-east' und die "
    "unveränderte Methode des Ziels, ohne Kosten.\n"
    "Tipp: Nicht berechnete Attribute geben Sie mit getattr(ziel, name) einfach weiter."
)

# Kosten und Zähler über mehrere Aufrufe, auch über eine gemerkte Methode
dienst = neuer_dienst()
hochladen = dienst.hochladen
for nummer in range(4):
    hochladen(f"datei{nummer}", b"x" * nummer)
dienst.herunterladen("datei2")
assert (dienst.kosten, dienst.aufrufe) == (22, {"hochladen": 4, "herunterladen": 1}), (
    f"Nach viermal hochladen über hochladen = dienst.hochladen und einmal herunterladen sind kosten und aufrufe "
    f"{dienst.kosten!r} und {dienst.aufrufe!r}; erwartet waren 22 und {{'hochladen': 4, 'herunterladen': 1}}.\n"
    "Tipp: Zählen Sie in der Funktion, die Sie zurückgeben, nicht schon beim Nachschlagen."
)

# Nur nachschlagen kostet nichts
dienst = neuer_dienst()
dienst.hochladen
dienst.herunterladen
assert (dienst.kosten, dienst.aufrufe) == (0, {}), (
    f"Nach dienst.hochladen ohne Aufruf sind kosten und aufrufe {dienst.kosten!r} und {dienst.aufrufe!r}, "
    "erwartet waren 0 und {}. Berechnet wird erst der Aufruf."
)

# Schlüsselwortargumente werden weitergereicht
dienst = neuer_dienst()
ergebnis = dienst.hochladen(daten=b"12345", name="k.bin")
assert ergebnis == 5 and dienst.herunterladen(name="k.bin") == b"12345", (
    f"dienst.hochladen(daten=b'12345', name='k.bin') ergibt {ergebnis!r}, erwartet war 5.\n"
    "Tipp: Reichen Sie *args und **kwargs an die Methode weiter."
)

# Ein Aufruf mit Ausnahme wird trotzdem berechnet, die Ausnahme kommt durch
dienst = neuer_dienst()
try:
    dienst.herunterladen("gibt_es_nicht")
    fehler = None
except KeyError as ausnahme:
    fehler = ausnahme
assert fehler is not None and (dienst.kosten, dienst.aufrufe) == (2, {"herunterladen": 1}), (
    f"dienst.herunterladen('gibt_es_nicht') soll einen KeyError auslösen und trotzdem 2 Cent berechnen; "
    f"Ausnahme: {fehler!r}, kosten {dienst.kosten!r}, aufrufe {dienst.aufrufe!r}.\n"
    "Tipp: Addieren und zählen Sie vor dem Aufruf der Methode."
)

# Unbekannte Attribute lösen AttributeError aus
dienst = neuer_dienst()
try:
    dienst.loeschen
    fehler = None
except AttributeError as ausnahme:
    fehler = ausnahme
vorhanden = hasattr(dienst, "gibt_es_nicht")
standard = getattr(dienst, "x", "standard")
assert fehler is not None and not vorhanden and standard == "standard", (
    "Unbekannte Attribute sollen einen AttributeError auslösen. Erwartet: dienst.loeschen löst AttributeError aus, "
    "hasattr(dienst, 'gibt_es_nicht') ist False, getattr(dienst, 'x', 'standard') ist 'standard'; "
    f"bekommen: {fehler!r}, {vorhanden!r}, {standard!r}."
)

# Mit Preis 0 und ohne Preise
dienst = Kostenzaehler(Speicherdienst("eu"), {"auflisten": 0})
dienst.auflisten()
dienst.hochladen("a", b"")
assert (dienst.kosten, dienst.aufrufe) == (0, {"auflisten": 1}), (
    f"Mit preise = {{'auflisten': 0}} sind nach auflisten() und hochladen(...) kosten und aufrufe "
    f"{dienst.kosten!r} und {dienst.aufrufe!r}; erwartet waren 0 und {{'auflisten': 1}}."
)

# Ein beliebiges Ziel ohne Preise, hier eine Liste
dienst = Kostenzaehler([3, 1, 2], {})
dienst.sort()
ergebnis = (dienst.ziel, dienst.index(2), dienst.kosten, dienst.aufrufe)
assert ergebnis == ([1, 2, 3], 1, 0, {}), (
    "Ein Kostenzaehler um die Liste [3, 1, 2] ohne Preise soll sort() und index(2) an die Liste weiterreichen; "
    f"ziel, index(2), kosten und aufrufe sind {ergebnis!r}, erwartet waren ([1, 2, 3], 1, 0, {{}})."
)

# Auch ein leeres Ziel, das als falsch gilt, bekommt die Zugriffe
leer = []
dienst = Kostenzaehler(leer, {"append": 1})
dienst.append(7)
assert leer == [7] and (dienst.kosten, dienst.aufrufe) == (1, {"append": 1}), (
    f"Ein Kostenzaehler um die leere Liste mit preise = {{'append': 1}} soll append(7) weiterreichen und zählen; "
    f"die Liste ist danach {leer!r}, kosten und aufrufe sind {dienst.kosten!r} und {dienst.aufrufe!r}; "
    "erwartet waren [7], 1 und {'append': 1}.\n"
    "Tipp: Prüfen Sie, ob ziel in self.__dict__ steht, nicht, ob es wahr ist."
)

# Zwei Zähler zählen getrennt
erster = neuer_dienst()
zweiter = neuer_dienst()
erster.hochladen("a", b"1")
assert (erster.kosten, zweiter.kosten, zweiter.aufrufe) == (5, 0, {}), (
    f"Nach erster.hochladen(...) sind die Kosten {erster.kosten!r} und {zweiter.kosten!r}, "
    f"erwartet waren 5 und 0; zweiter.aufrufe ist {zweiter.aufrufe!r}."
)

# Ohne __init__ gibt es AttributeError statt endloser Rekursion
roh = Kostenzaehler.__new__(Kostenzaehler)
try:
    roh.hochladen
    ergebnis = "kein Fehler"
except AttributeError:
    ergebnis = "AttributeError"
except RecursionError:
    ergebnis = "RecursionError"
assert ergebnis == "AttributeError", (
    f"Bei einem Kostenzaehler ohne __init__ ergibt der Zugriff auf hochladen: {ergebnis}; erwartet war AttributeError.\n"
    "Tipp: self.ziel landet wieder in __getattr__, wenn ziel fehlt. Lesen Sie es mit self.__dict__.get(\"ziel\")."
)

# copy.copy funktioniert, die Kopie reicht an dasselbe Ziel weiter
dienst = neuer_dienst()
dienst.hochladen("a", b"12")
try:
    kopie = copy.copy(dienst)
    ergebnis = (kopie.herunterladen("a"), kopie.ziel is dienst.ziel, kopie.region)
except RecursionError:
    ergebnis = "RecursionError"
assert ergebnis == (b"12", True, "eu-central"), (
    f"copy.copy(dienst) und dann herunterladen('a'), ziel und region ergeben {ergebnis!r}; erwartet war "
    "(b'12', True, 'eu-central')."
)

# 300 zufällige Testläufe, nachgerechnet
zufall = Zufall(5005)
for _ in range(300):
    preise = {name: zufall.randint(0, 10**4) for name in zufall.sample(["hochladen", "herunterladen", "auflisten"], zufall.randint(0, 3))}
    dienst = Kostenzaehler(Speicherdienst("eu"), dict(preise))
    kosten = 0
    aufrufe = {}
    protokoll = []
    for _ in range(zufall.randint(0, 12)):
        name = zufall.choice(["hochladen", "herunterladen", "auflisten"])
        argumente = {"hochladen": (zufall.choice("abc"), b"x"), "herunterladen": (zufall.choice("abc"),), "auflisten": ()}[name]
        protokoll.append(f"{name}{argumente!r}")
        try:
            getattr(dienst, name)(*argumente)
        except KeyError:
            pass
        if name in preise:
            kosten += preise[name]
            aufrufe[name] = aufrufe.get(name, 0) + 1
    assert (dienst.kosten, dienst.aufrufe) == (kosten, aufrufe), (
        f"Mit preise = {preise} und den Aufrufen {', '.join(protokoll)} sind kosten und aufrufe "
        f"{dienst.kosten!r} und {dienst.aufrufe!r}; erwartet waren {kosten} und {aufrufe}."
    )

# An der oberen Grenze: 100 000 Aufrufe
dienst = Kostenzaehler(Speicherdienst("eu"), {"hochladen": 10**4, "herunterladen": 1})
for nummer in range(50000):
    dienst.hochladen("f", b"")
    dienst.herunterladen("f")
assert (dienst.kosten, dienst.aufrufe) == (50000 * 10**4 + 50000, {"hochladen": 50000, "herunterladen": 50000}), (
    f"Nach je 50 000 Aufrufen von hochladen (10 000 Cent) und herunterladen (1 Cent) sind kosten und aufrufe "
    f"{dienst.kosten!r} und {dienst.aufrufe!r}."
)

# Die Ausgabe des Programms stimmt (aufrufe darf auch ein Counter oder defaultdict sein)
erwartete_ausgabe = "9\nb'PDF-Daten'\n['bericht.pdf'] eu-central\n7 {'hochladen': 1, 'herunterladen': 1}"
zeilen = AUSGABE.split("\n")
assert (
    zeilen[:3] == ["9", "b'PDF-Daten'", "['bericht.pdf'] eu-central"]
    and len(zeilen) == 4
    and zeilen[3].startswith("7 ")
    and "{'hochladen': 1, 'herunterladen': 1}" in zeilen[3]
), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
