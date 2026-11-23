# Automatisch erzeugt aus lehrkraft/muster/5_042_logsammler.py - nicht von Hand ändern.
# vorlage-hash: df658221cf8d9f53
# text-hash: cb12e1464eec0036
# thema: nebenlaeufigkeit
# inhalt: asyncio.Queue, Erzeuger, Verbraucher

import ast
import inspect
import warnings

warnings.simplefilter("ignore", RuntimeWarning)  # vergessenes await meldet der Test selbst
QUELLEN = {
    "web1": ["INFO start", "ERROR Platte voll", "INFO ok"],
    "db1": ["WARN langsam", "ERROR Verbindung weg"],
}
ECHTE_QUEUE = asyncio.Queue


class Beobachtete(ECHTE_QUEUE):
    """Eine asyncio.Queue, die mitschreibt, was abgelegt, geholt und erledigt wird."""

    alle = []

    def __init__(self, maxsize=0):
        """Merkt sich die Schlange und legt die Listen für die Beobachtung an."""
        super().__init__(maxsize)
        self.abgelegt = []
        self.geholt = 0
        self.erledigt = 0
        self.hoechststand = 0
        Beobachtete.alle.append(self)

    def put_nowait(self, eintrag):
        """Legt ab und merkt sich Eintrag und Füllstand."""
        super().put_nowait(eintrag)
        self.abgelegt.append(eintrag)
        self.hoechststand = max(self.hoechststand, self.qsize())

    def get_nowait(self):
        """Holt und zählt mit."""
        eintrag = super().get_nowait()
        self.geholt += 1
        return eintrag

    def task_done(self):
        """Meldet erledigt und zählt mit."""
        super().task_done()
        self.erledigt += 1


def ausfuehren(koroutine_von, *argumente):
    """Führt eine Koroutine mit beobachteter Queue aus; ein Fehler wird als Text zurückgegeben."""
    Beobachtete.alle.clear()
    BEARBEITET.clear()
    asyncio.Queue = Beobachtete
    try:
        return asyncio.run(asyncio.wait_for(koroutine_von(*argumente), 1.5))
    except TimeoutError:
        return "TimeoutError: nach 1,5 Sekunden nicht fertig (wartet etwas für immer?)"
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"
    finally:
        asyncio.Queue = ECHTE_QUEUE


def erwartete_zahlen(quellen):
    """Vergleichslösung: die Stufen aller Zeilen gezählt."""
    zahlen = {}
    for zeilen in quellen.values():
        for zeile in zeilen:
            stufe = zeile.split()[0]
            zahlen[stufe] = zahlen.get(stufe, 0) + 1
    return zahlen


async def nur_erzeuger(server, zeilen):
    """Lässt erzeuger in eine große Schlange schreiben und gibt deren Inhalt zurück."""
    schlange = asyncio.Queue()
    await erzeuger(server, zeilen, schlange)
    return [schlange.get_nowait() for _ in range(schlange.qsize())]


async def nur_verbraucher(eintraege, zaehler):
    """Lässt verbraucher eine vorbereitete Schlange abarbeiten; gibt (zaehler, Rest, Schlange) zurück."""
    schlange = asyncio.Queue()
    for eintrag in eintraege:
        schlange.put_nowait(eintrag)
    await verbraucher(schlange, zaehler)
    return zaehler, schlange.qsize(), schlange


def zufallsquellen(zufall, server, zeilen):
    """Erzeugt bis zu server Server mit zusammen etwa zeilen Logzeilen."""
    quellen = {}
    for nummer in range(server):
        anzahl = zufall.randint(0, 2 * zeilen // max(server, 1))
        quellen[f"srv{nummer}"] = [
            f"{zufall.choice(['INFO', 'WARN', 'ERROR', 'DEBUG'])} Meldung {nummer}-{stelle}" for stelle in range(anzahl)
        ]
    return quellen


def verschraenkt(schlange):
    """True, wenn die Einträge der Server in der Schlange abwechseln statt Server für Server zu kommen."""
    server = [eintrag[0] for eintrag in schlange.abgelegt if eintrag is not None]
    wechsel = sum(1 for vorher, nachher in zip(server, server[1:]) if vorher != nachher)
    return wechsel > len(set(server)) - 1


# Alle drei sind Koroutinenfunktionen
keine = [f.__name__ for f in [erzeuger, verbraucher, sammle] if not inspect.iscoroutinefunction(f)]
assert not keine, f"{keine} sind keine Koroutinenfunktionen. Schreiben Sie async def."

# erzeuger: alle Zeilen als Paare in der Reihenfolge
ergebnis = ausfuehren(nur_erzeuger, "web1", QUELLEN["web1"])
erwartet = [("web1", zeile) for zeile in QUELLEN["web1"]]
assert ergebnis == erwartet, (
    f"Nach erzeuger('web1', {QUELLEN['web1']}, schlange) liegt in der Schlange {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: await schlange.put((server, zeile)) für jede Zeile."
)

# erzeuger: keine Zeilen
ergebnis = ausfuehren(nur_erzeuger, "db1", [])
assert ergebnis == [], f"Nach erzeuger('db1', [], schlange) liegt in der Schlange {ergebnis!r}, erwartet war []."

# verbraucher: zählt die Stufen und hört bei None auf
eintraege = [("a", "INFO x"), ("b", "ERROR y"), ("a", "INFO z"), None]
ergebnis = ausfuehren(nur_verbraucher, eintraege, {})
zahlen = ergebnis[0] if isinstance(ergebnis, tuple) else ergebnis
assert zahlen == {"INFO": 2, "ERROR": 1}, (
    f"verbraucher mit den Einträgen {eintraege} zählt {zahlen!r}, erwartet war {{'INFO': 2, 'ERROR': 1}}.\n"
    "Tipp: stufe = await auswerten(zeile), dann zaehler[stufe] = zaehler.get(stufe, 0) + 1; bei None return."
)

# verbraucher: benutzt auswerten für jede Zeile
assert [zeile for _, zeile in BEARBEITET] == ["INFO x", "ERROR y", "INFO z"], (
    f"auswerten wurde für {[zeile for _, zeile in BEARBEITET]} aufgerufen, erwartet war ['INFO x', 'ERROR y', 'INFO z']."
)

# verbraucher: zählt im übergebenen Dictionary weiter
ergebnis = ausfuehren(nur_verbraucher, [("a", "WARN x"), None], {"WARN": 4})
zahlen = ergebnis[0] if isinstance(ergebnis, tuple) else ergebnis
assert zahlen == {"WARN": 5}, (
    f"verbraucher mit zaehler = {{'WARN': 4}} und einer WARN-Zeile ergibt {zahlen!r}, erwartet war {{'WARN': 5}}.\n"
    "Tipp: Ändern Sie das übergebene Dictionary, statt ein neues anzulegen."
)

# verbraucher: hört beim ersten None auf und lässt den Rest liegen
ergebnis = ausfuehren(nur_verbraucher, [("a", "INFO x"), None, ("a", "ERROR y"), None], {})
assert isinstance(ergebnis, tuple) and ergebnis[:2] == ({"INFO": 1}, 2), (
    f"verbraucher mit [('a', 'INFO x'), None, ('a', 'ERROR y'), None] ergibt (zaehler, Rest) = "
    f"{ergebnis[:2] if isinstance(ergebnis, tuple) else ergebnis!r}, erwartet war ({{'INFO': 1}}, 2).\n"
    "Tipp: Nach None holt ein Verbraucher nichts mehr; jeder bekommt sein eigenes None."
)

# verbraucher: task_done nach jedem geholten Eintrag, auch nach None
schlange = ergebnis[2] if isinstance(ergebnis, tuple) else None
assert schlange is not None and schlange.erledigt == schlange.geholt == 2, (
    f"verbraucher hat {schlange.geholt if schlange else '?'} Einträge geholt und "
    f"{schlange.erledigt if schlange else '?'}-mal task_done() aufgerufen; erwartet war beides 2."
)

# sammle: das Beispiel
ergebnis = ausfuehren(sammle, QUELLEN, 2, 1)
assert ergebnis == {"INFO": 2, "ERROR": 2, "WARN": 1}, (
    f"asyncio.run(sammle(quellen, 2, 1)) ergibt {ergebnis!r}, erwartet war {{'INFO': 2, 'ERROR': 2, 'WARN': 1}}.\n"
    "Tipp: Erst die Verbraucher als Tasks starten, dann die Erzeuger mit gather, dann ein None je Verbraucher."
)

# sammle: die Schlange hat genau platz Plätze
platzzahl = [schlange.maxsize for schlange in Beobachtete.alle]
assert platzzahl == [1], (
    f"sammle(quellen, 2, 1) hat Schlangen mit den Größen {platzzahl} angelegt, erwartet war eine mit maxsize=1.\n"
    "Tipp: asyncio.Queue(maxsize=platz)."
)

# sammle: andere Quellen (nicht fest hinschreiben!)
quellen = {"fw": ["DEBUG a", "DEBUG b"], "mail": ["INFO c"], "leer": []}
ergebnis = ausfuehren(sammle, quellen, 1, 5)
assert ergebnis == erwartete_zahlen(quellen), f"sammle({quellen}, 1, 5) ergibt {ergebnis!r}, erwartet war {erwartete_zahlen(quellen)}."

# sammle: die Erzeuger laufen gleichzeitig
quellen = {f"s{nummer}": [f"INFO {nummer}-{stelle}" for stelle in range(6)] for nummer in range(3)}
ergebnis = ausfuehren(sammle, quellen, 1, 1)
schlange = Beobachtete.alle[0] if Beobachtete.alle else None
assert ergebnis == erwartete_zahlen(quellen) and schlange is not None and verschraenkt(schlange), (
    f"sammle mit drei Servern zu je sechs Zeilen und platz 1 ergibt {ergebnis!r}; in die Schlange kamen die Server "
    f"in der Folge {[eintrag[0] for eintrag in schlange.abgelegt if eintrag] if schlange else '–'}.\n"
    "Erwartet war, dass sie sich abwechseln.\nTipp: Starten Sie alle Erzeuger mit asyncio.gather, nicht nacheinander mit await."
)

# sammle: mehrere Verbraucher teilen sich die Arbeit
quellen = {"web1": [f"INFO {stelle}" for stelle in range(30)]}
ergebnis = ausfuehren(sammle, quellen, 3, 10)
helfer = {id(task) for task, _ in BEARBEITET}
assert ergebnis == {"INFO": 30} and len(helfer) == 3, (
    f"sammle mit 30 Zeilen und 3 Verbrauchern ergibt {ergebnis!r}; ausgewertet haben {len(helfer)} verschiedene "
    "Tasks, erwartet waren 3.\nTipp: Starten Sie verbraucherzahl Verbraucher mit asyncio.create_task."
)

# sammle: keine Server
ergebnis = ausfuehren(sammle, {}, 3, 2)
assert ergebnis == {}, f"sammle({{}}, 3, 2) ergibt {ergebnis!r}, erwartet war {{}}."

# sammle: alle Verbraucher hören auf
ergebnis = ausfuehren(sammle, QUELLEN, 4, 2)
schlange = Beobachtete.alle[0] if Beobachtete.alle else None
assert ergebnis == erwartete_zahlen(QUELLEN) and schlange is not None and schlange.qsize() == 0, (
    f"sammle(quellen, 4, 2) ergibt {ergebnis!r}; am Ende liegen noch "
    f"{schlange.qsize() if schlange else '?'} Einträge in der Schlange.\n"
    "Tipp: Legen Sie für jeden Verbraucher ein None ab und warten Sie mit gather, bis alle aufgehört haben."
)

# Die Ausgabe des Programms
erwartet = erwartete_zahlen(QUELLEN)
try:
    gelesen = ast.literal_eval(AUSGABE.strip())
except (ValueError, SyntaxError):
    gelesen = None
assert gelesen == erwartet, f"Erwartete Ausgabe (Reihenfolge egal):\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Läufe
zufall = Zufall(5042)
for _ in range(60):
    quellen = zufallsquellen(zufall, zufall.randint(0, 6), zufall.randint(0, 20))
    verbraucherzahl = zufall.randint(1, 5)
    platz = zufall.randint(1, 4)
    ergebnis = ausfuehren(sammle, quellen, verbraucherzahl, platz)
    schlange = Beobachtete.alle[0] if Beobachtete.alle else None
    stimmt = ergebnis == erwartete_zahlen(quellen) and schlange is not None and schlange.hoechststand <= platz
    assert stimmt, (
        f"sammle({quellen}, {verbraucherzahl}, {platz}) ergibt {ergebnis!r}, erwartet war {erwartete_zahlen(quellen)}; "
        f"höchster Füllstand der Schlange {schlange.hoechststand if schlange else '?'}."
    )

# Obere Grenze: 50 Server mit zusammen etwa 5000 Zeilen, 20 Verbraucher
quellen = zufallsquellen(zufall, 50, 5000)
ergebnis = ausfuehren(sammle, quellen, 20, 1000)
assert ergebnis == erwartete_zahlen(quellen), "Bei 50 Servern und 20 Verbrauchern stimmt das Ergebnis von sammle nicht."
