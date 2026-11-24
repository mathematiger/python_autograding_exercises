# Automatisch erzeugt aus lehrkraft/muster/5_045_prozessuebergaenge.py - nicht von Hand ändern.
# vorlage-hash: c58154c50d7e1d81
# text-hash: c87cdc158e4bdbac
# thema: nebenlaeufigkeit
# inhalt: threading: Race Condition, Lock

import copy

STANDORTE = {
    "Hamburg": [
        ["eingang", "pruefung", "versand"],
        ["eingang", "pruefung", "rueckfrage", "pruefung", "versand"],
    ],
    "Leipzig": [["eingang", "pruefung", "versand"]],
    "Köln": [["eingang", "rueckfrage", "pruefung", "versand"]],
}
ERWARTET = {
    ("eingang", "pruefung"): 3,
    ("eingang", "rueckfrage"): 1,
    ("pruefung", "rueckfrage"): 1,
    ("pruefung", "versand"): 4,
    ("rueckfrage", "pruefung"): 2,
}
SCHRITTE = ["eingang", "pruefung", "rueckfrage", "versand", "abschluss"]
eigene_pruefung = pruefe_schritt


class Spion:
    """Eine Sperre, die mitzählt, wie oft sie genommen wurde, und weiß, ob sie gerade gehalten wird."""

    def __init__(self):
        """Legt die echte Sperre und die Zähler an."""
        self.echt = threading.Lock()
        self.genommen = 0

    def acquire(self, *argumente, **schluesselwerte):
        """Nimmt die echte Sperre und zählt mit."""
        ergebnis = self.echt.acquire(*argumente, **schluesselwerte)
        self.genommen += 1
        return ergebnis

    def release(self):
        """Gibt die echte Sperre frei."""
        self.echt.release()

    def locked(self):
        """Sagt, ob die Sperre gerade gehalten wird."""
        return self.echt.locked()

    def __enter__(self):
        """Nimmt die Sperre beim Betreten des with-Blocks."""
        self.acquire()
        return self

    def __exit__(self, art, wert, verlauf):
        """Gibt die Sperre am Ende des with-Blocks frei."""
        self.release()
        return False


class BeobachtetesDict(dict):
    """Ein Dictionary, das bei jedem Schreiben notiert, ob die Sperre gerade gehalten wird."""

    def __init__(self, sperre):
        """Merkt sich die Sperre, deren Zustand notiert wird."""
        super().__init__()
        self.sperre = sperre
        self.beim_schreiben = []

    def __setitem__(self, schluessel, wert):
        """Notiert den Zustand der Sperre und schreibt den Wert."""
        self.beim_schreiben.append(self.sperre.locked())
        super().__setitem__(schluessel, wert)


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich(standorte):
    """Vergleichslösung: zählt alle Übergänge nacheinander, ohne Threads."""
    anzahl = {}
    for faelle in standorte.values():
        for fall in faelle:
            for stelle in range(len(fall) - 1):
                paar = (fall[stelle], fall[stelle + 1])
                anzahl[paar] = anzahl.get(paar, 0) + 1
    return dict(sorted(anzahl.items()))


def zufallsstandorte(zufall, standorte, faelle, schritte):
    """Erzeugt zufällige Standorte mit zufälligen Fällen."""
    ergebnis = {}
    for nummer in range(standorte):
        ergebnis[f"S{nummer}"] = [
            [zufall.choice(SCHRITTE) for _ in range(zufall.randint(1, schritte))] for _ in range(zufall.randint(0, faelle))
        ]
    return ergebnis


class Mitschrift:
    """Ein Zähler-Ersatz, der nur aufschreibt, welche Übergänge gezählt werden sollen."""

    def __init__(self):
        """Legt die leere Liste an."""
        self.aufrufe = []

    def zaehle(self, von, nach):
        """Schreibt den Übergang auf."""
        self.aufrufe.append((von, nach))


# Uebergaenge: zaehler ist ein leeres Dictionary, sperre ein Lock
zaehler = wert_von(Uebergaenge)
inhalt = getattr(zaehler, "zaehler", "(kein Attribut zaehler)")
sperre = getattr(zaehler, "sperre", "(kein Attribut sperre)")
assert inhalt == {} and isinstance(sperre, type(threading.Lock())), (
    f"Uebergaenge() hat zaehler = {inhalt!r} und sperre = {sperre!r}; erwartet waren {{}} und threading.Lock().\n"
    "Tipp: In __init__ self.zaehler = {} und self.sperre = threading.Lock()."
)

# zaehle: ein Übergang
zaehler = Uebergaenge()
wert_von(lambda: zaehler.zaehle("eingang", "pruefung"))
assert getattr(zaehler, "zaehler", None) == {("eingang", "pruefung"): 1}, (
    f"Nach zaehle('eingang', 'pruefung') ist zaehler {getattr(zaehler, 'zaehler', None)!r}, "
    "erwartet war {('eingang', 'pruefung'): 1}."
)

# zaehle: derselbe Übergang zweimal und ein anderer
wert_von(lambda: zaehler.zaehle("eingang", "pruefung"))
wert_von(lambda: zaehler.zaehle("pruefung", "versand"))
assert getattr(zaehler, "zaehler", None) == {("eingang", "pruefung"): 2, ("pruefung", "versand"): 1}, (
    f"Nach drei Aufrufen ist zaehler {getattr(zaehler, 'zaehler', None)!r}, "
    "erwartet war {('eingang', 'pruefung'): 2, ('pruefung', 'versand'): 1}."
)

# zaehle: pruefe_schritt wird für jeden Übergang aufgerufen
geprueft = []


def pruefe_schritt(von, nach):
    """Schreibt den Aufruf auf und prüft wie das Original."""
    geprueft.append((von, nach))
    eigene_pruefung(von, nach)


zaehler = Uebergaenge()
wert_von(lambda: zaehler.zaehle("eingang", "pruefung"))
pruefe_schritt = eigene_pruefung
assert geprueft == [("eingang", "pruefung")], (
    f"Bei zaehle('eingang', 'pruefung') wurde pruefe_schritt so aufgerufen: {geprueft}; erwartet war einmal mit "
    "('eingang', 'pruefung')."
)

# zaehle: ein ungültiger Schritt ergibt einen ValueError und wird nicht gezählt
zaehler = Uebergaenge()
ergebnis = wert_von(lambda: zaehler.zaehle("eingang", ""))
assert str(ergebnis).startswith("ValueError") and getattr(zaehler, "zaehler", None) == {}, (
    f"zaehle('eingang', '') ergibt {ergebnis!r}, danach ist zaehler {getattr(zaehler, 'zaehler', None)!r}; "
    "erwartet war ein ValueError und ein leerer Zähler.\nTipp: Schreiben Sie den neuen Stand erst nach pruefe_schritt."
)

# zaehle: nach dem Fehler ist die Sperre wieder frei
sperre = getattr(zaehler, "sperre", None)
frei = sperre is not None and not sperre.locked()
if sperre is not None and sperre.locked():
    sperre.release()
assert frei, (
    "Nach dem ValueError in zaehle ist die Sperre noch gesperrt; jeder weitere Aufruf würde für immer warten.\n"
    "Tipp: with self.sperre: gibt die Sperre auch bei einer Ausnahme frei."
)

# zaehle: die Sperre wird genommen
zaehler = Uebergaenge()
spion = Spion()
zaehler.sperre = spion
wert_von(lambda: zaehler.zaehle("eingang", "pruefung"))
assert spion.genommen >= 1, (
    f"zaehle hat die Sperre {spion.genommen}-mal genommen, erwartet war mindestens einmal.\n"
    "Tipp: with self.sperre: um Lesen, Prüfen und Schreiben."
)

# zaehle: pruefe_schritt läuft unter der Sperre
gesperrt_beim_pruefen = []


def pruefe_schritt(von, nach):
    """Notiert, ob die Sperre gerade gehalten wird, und prüft wie das Original."""
    gesperrt_beim_pruefen.append(spion.locked())
    eigene_pruefung(von, nach)


zaehler = Uebergaenge()
spion = Spion()
zaehler.sperre = spion
wert_von(lambda: zaehler.zaehle("eingang", "pruefung"))
pruefe_schritt = eigene_pruefung
assert gesperrt_beim_pruefen == [True], (
    f"Beim Aufruf von pruefe_schritt war die Sperre {gesperrt_beim_pruefen} gehalten; erwartet war [True].\n"
    "Tipp: Lesen, pruefe_schritt und Schreiben gehören alle in denselben with-Block; sonst kann ein anderer Thread "
    "zwischen Lesen und Schreiben dazwischenkommen."
)

# zaehle: geschrieben wird unter der Sperre
zaehler = Uebergaenge()
spion = Spion()
zaehler.sperre = spion
zaehler.zaehler = BeobachtetesDict(spion)
wert_von(lambda: zaehler.zaehle("eingang", "pruefung"))
assert zaehler.zaehler.beim_schreiben and all(zaehler.zaehler.beim_schreiben), (
    f"Beim Schreiben in zaehler war die Sperre {zaehler.zaehler.beim_schreiben} gehalten; erwartet war jedes Mal True.\n"
    "Tipp: Auch self.zaehler[paar] = bisher + 1 gehört unter die Sperre."
)

# stand: die gezählten Paare
zaehler = Uebergaenge()
for von, nach in [("z", "a"), ("b", "c"), ("a", "z"), ("b", "c")]:
    wert_von(lambda: zaehler.zaehle(von, nach))
ergebnis = wert_von(zaehler.stand)
assert ergebnis == {("a", "z"): 1, ("b", "c"): 2, ("z", "a"): 1}, (
    f"stand() ergibt {ergebnis!r}, erwartet war {{('a', 'z'): 1, ('b', 'c'): 2, ('z', 'a'): 1}} (Reihenfolge egal).\n"
    "Tipp: stand() gibt ein Dictionary mit denselben Einträgen wie self.zaehler zurück."
)

# stand: nach den Paaren sortiert
reihenfolge = list(ergebnis) if isinstance(ergebnis, dict) else ergebnis
assert reihenfolge == [("a", "z"), ("b", "c"), ("z", "a")], (
    f"Hier geht es um die Reihenfolge: Die Schlüssel von stand() kommen als {reihenfolge!r}, "
    "erwartet war [('a', 'z'), ('b', 'c'), ('z', 'a')].\nTipp: dict(sorted(self.zaehler.items()))."
)

# stand: eine Kopie, kein Verweis auf den Zähler
if isinstance(ergebnis, dict):
    ergebnis[("x", "y")] = 99
assert ("x", "y") not in getattr(zaehler, "zaehler", {}), (
    "Eine Änderung am Ergebnis von stand() ändert den Zähler selbst; erwartet war eine Kopie."
)

# stand: liest unter der Sperre
spion = Spion()
zaehler.sperre = spion
wert_von(zaehler.stand)
assert spion.genommen >= 1, "stand() nimmt die Sperre nicht; ein anderer Thread könnte gerade mitten im Schreiben sein."

# zaehle_faelle: jeder Übergang eines Falls, in der Reihenfolge
mitschrift = Mitschrift()
wert_von(lambda: zaehle_faelle(mitschrift, [["eingang", "pruefung", "rueckfrage", "pruefung"]]))
assert mitschrift.aufrufe == [("eingang", "pruefung"), ("pruefung", "rueckfrage"), ("rueckfrage", "pruefung")], (
    f"zaehle_faelle mit dem Fall eingang → pruefung → rueckfrage → pruefung ruft zaehle so auf: {mitschrift.aufrufe}; "
    "erwartet waren drei Übergänge.\nTipp: zip(fall, fall[1:]) liefert die Paare aufeinanderfolgender Schritte."
)

# zaehle_faelle: mehrere Fälle
mitschrift = Mitschrift()
wert_von(lambda: zaehle_faelle(mitschrift, [["a", "b"], ["c", "d", "e"]]))
assert mitschrift.aufrufe == [("a", "b"), ("c", "d"), ("d", "e")], (
    f"zaehle_faelle mit [['a', 'b'], ['c', 'd', 'e']] ruft zaehle so auf: {mitschrift.aufrufe}; "
    "erwartet war [('a', 'b'), ('c', 'd'), ('d', 'e')]: kein Übergang vom Ende eines Falls zum nächsten."
)

# zaehle_faelle: ein Fall mit nur einem Schritt hat keinen Übergang
mitschrift = Mitschrift()
wert_von(lambda: zaehle_faelle(mitschrift, [["eingang"], []]))
assert mitschrift.aufrufe == [], f"zaehle_faelle mit [['eingang']] ruft zaehle so auf: {mitschrift.aufrufe}; erwartet war gar nicht."

# parallel_auswerten: das Beispiel
ergebnis = wert_von(lambda: parallel_auswerten(copy.deepcopy(STANDORTE)))
assert ergebnis == ERWARTET, (
    f"parallel_auswerten(standorte) ergibt\n{ergebnis!r}\nerwartet war (Reihenfolge egal)\n{ERWARTET}"
)

# parallel_auswerten: das Beispiel nach den Paaren sortiert
reihenfolge = list(ergebnis) if isinstance(ergebnis, dict) else ergebnis
assert reihenfolge == list(ERWARTET), (
    f"Hier geht es um die Reihenfolge: Die Schlüssel von parallel_auswerten kommen als\n{reihenfolge!r}\n"
    f"erwartet war\n{list(ERWARTET)}\nTipp: Geben Sie zaehler.stand() zurück; stand() sortiert die Paare."
)

# parallel_auswerten: jeder Standort in einem eigenen Thread
threads_beim_pruefen = []


def pruefe_schritt(von, nach):
    """Notiert den Thread und prüft wie das Original."""
    threads_beim_pruefen.append(threading.current_thread())
    eigene_pruefung(von, nach)


wert_von(lambda: parallel_auswerten(copy.deepcopy(STANDORTE)))
pruefe_schritt = eigene_pruefung
verschiedene = {id(thread) for thread in threads_beim_pruefen if thread is not threading.main_thread()}
assert len(verschiedene) == 3, (
    f"Bei drei Standorten wurde aus {len(verschiedene)} verschiedenen Threads gezählt (ohne den Hauptthread); "
    "erwartet waren 3.\nTipp: threading.Thread(target=zaehle_faelle, args=(zaehler, faelle)) und start()."
)

# parallel_auswerten: keine Standorte
ergebnis = wert_von(lambda: parallel_auswerten({}))
assert ergebnis == {}, f"parallel_auswerten({{}}) ergibt {ergebnis!r}, erwartet war {{}}."

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar(str(ERWARTET)), f"Erwartete Ausgabe:\n{ERWARTET}\nIhr Programm:\n{AUSGABE}"

# Viele Threads zählen gleichzeitig, kein Übergang geht verloren
standorte = {f"S{nummer}": [["eingang", "pruefung"] * 5] * 50 for nummer in range(6)}
ergebnis = wert_von(lambda: parallel_auswerten(standorte))
assert ergebnis == vergleich(standorte), (
    f"Sechs Standorte mit je 50 Fällen aus 10 Schritten ergeben {ergebnis!r}, erwartet war {vergleich(standorte)}.\n"
    "Tipp: Fehlen Übergänge, liest und schreibt zaehle nicht im selben gesperrten Abschnitt."
)

# Viele zufällige Standorte
zufall = Zufall(5045)
for _ in range(30):
    standorte = zufallsstandorte(zufall, zufall.randint(0, 4), 6, 6)
    ergebnis = wert_von(lambda: parallel_auswerten(copy.deepcopy(standorte)))
    assert ergebnis == vergleich(standorte), f"parallel_auswerten({standorte})\nergibt   {ergebnis!r}\nerwartet {vergleich(standorte)}"

# Obere Grenze: 10 Standorte mit je 100 Fällen aus 10 Schritten
standorte = {f"S{nummer}": [[zufall.choice(SCHRITTE) for _ in range(10)] for _ in range(100)] for nummer in range(10)}
ergebnis = wert_von(lambda: parallel_auswerten(copy.deepcopy(standorte)))
assert ergebnis == vergleich(standorte), (
    f"Bei 10 Standorten mit je 100 Fällen zählt parallel_auswerten {sum(ergebnis.values()) if isinstance(ergebnis, dict) else ergebnis!r} "
    f"Übergänge, erwartet waren {sum(vergleich(standorte).values())}."
)
