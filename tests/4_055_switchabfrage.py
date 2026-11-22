# Automatisch erzeugt aus lehrkraft/muster/4_055_switchabfrage.py - nicht von Hand ändern.
# vorlage-hash: 1b3ed8c01a72f557
# text-hash: 23adcd8e542746f2
# thema: fehler
# inhalt: closing, suppress, Callback

class Testfehler(Exception):
    """Eine Ausnahme, die nur im Test vorkommt."""


class Testsitzung:
    """Eine Sitzung, die mitschreibt, wie oft sie geschlossen wurde."""

    def __init__(self, netz, host):
        """Öffnet die Sitzung im Testnetz."""
        self.netz = netz
        self.host = host
        self.geschlossen = 0
        netz.offene.append(host)

    def sende(self, befehl):
        """Gibt die Antwort zurück; KeyError bei einem unbekannten Befehl."""
        if self.geschlossen:
            raise RuntimeError("Sitzung schon geschlossen")
        return self.netz.switches[self.host][befehl]

    def close(self):
        """Schließt die Sitzung."""
        self.geschlossen += 1
        if self.geschlossen == 1:
            self.netz.offene.remove(self.host)


class Testnetz:
    """Ein Verwaltungsnetz für die Tests: zählt Verbindungsversuche und offene Sitzungen."""

    def __init__(self, switches, nicht_erreichbar=(), abgelehnt=()):
        """switches: host → {befehl: antwort}; nicht_erreichbar: TimeoutError; abgelehnt: ConnectionRefusedError."""
        self.switches = switches
        self.nicht_erreichbar = set(nicht_erreichbar)
        self.abgelehnt = set(abgelehnt)
        self.offene = []
        self.versuche = []
        self.sitzungen = []

    def verbinde(self, host):
        """Öffnet eine Testsitzung oder löst den passenden Fehler aus."""
        self.versuche.append(host)
        if host in self.nicht_erreichbar:
            raise TimeoutError(f"{host} antwortet nicht")
        if host in self.abgelehnt:
            raise ConnectionRefusedError(f"{host} lehnt ab")
        sitzung = Testsitzung(self, host)
        self.sitzungen.append(sitzung)
        return sitzung


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def beispielnetz():
    """Das Netz aus dem Aufgabentext."""
    return Testnetz({"sw-1": {"show version": "IOS 15.2"}, "sw-3": {"show version": "IOS 16.9"}}, nicht_erreichbar=["sw-2"])


def wirf(_):
    """Eine Aktion, die mit einem Testfehler abbricht."""
    raise Testfehler("Konfiguration unlesbar")


# mit_sitzung im Beispiel: das Ergebnis der Aktion kommt zurück
netz = beispielnetz()
ergebnis = wert_von(lambda: mit_sitzung(netz, "sw-1", lambda s: s.sende("show version")))
assert ergebnis == "IOS 15.2", (
    f"mit_sitzung(netz, 'sw-1', lambda s: s.sende('show version')) ergibt {ergebnis!r}, erwartet war 'IOS 15.2'.\n"
    "Tipp: Öffnen Sie die Sitzung mit netz.verbinde(host) und geben Sie aktion(sitzung) zurück."
)

# mit_sitzung im Beispiel: danach ist die Sitzung geschlossen
assert netz.offene == [] and [s.geschlossen for s in netz.sitzungen] == [1], (
    f"Nach mit_sitzung sind noch {netz.offene} offen (close-Aufrufe: {[s.geschlossen for s in netz.sitzungen]}), erwartet war keine offene Sitzung.\n"
    "Tipp: with closing(netz.verbinde(host)) as sitzung: ruft am Ende sitzung.close() auf."
)

# mit_sitzung mit einem anderen Switch und einer anderen Aktion (nicht fest hinschreiben!)
netz = Testnetz({"core": {"show clock": "12:00:01", "show vlan": "10, 20"}})
ergebnis = wert_von(lambda: mit_sitzung(netz, "core", lambda s: (s.sende("show vlan"), s.sende("show clock"))))
assert ergebnis == ("10, 20", "12:00:01") and netz.offene == [], f"mit_sitzung mit zwei Befehlen ergibt {ergebnis!r}, offen: {netz.offene}."

# mit_sitzung: die Aktion bekommt die Sitzung selbst
netz = beispielnetz()
ergebnis = wert_von(lambda: mit_sitzung(netz, "sw-3", lambda s: s is netz.sitzungen[0]))
assert ergebnis is True, f"Die Aktion bekommt {ergebnis!r}; erwartet war, dass sie die Sitzung von netz.verbinde erhält."

# mit_sitzung: nach einer Ausnahme in der Aktion ist die Sitzung geschlossen
netz = beispielnetz()
ergebnis = wert_von(lambda: mit_sitzung(netz, "sw-1", wirf))
assert netz.offene == [], (
    f"Nach einer Ausnahme in der Aktion ist noch {netz.offene} offen.\n"
    "Tipp: closing schließt die Sitzung auch dann, wenn im with-Block eine Ausnahme fliegt."
)

# mit_sitzung: die Ausnahme der Aktion fliegt weiter
assert ergebnis == "Testfehler: Konfiguration unlesbar", f"Eine Ausnahme in der Aktion ergibt {ergebnis!r}; erwartet war, dass sie weiterfliegt."

# mit_sitzung: ein nicht erreichbarer Switch löst den Fehler von verbinde aus
netz = beispielnetz()
ergebnis = wert_von(lambda: mit_sitzung(netz, "sw-2", lambda s: "lief"))
assert ergebnis.startswith("TimeoutError"), f"mit_sitzung für den nicht erreichbaren sw-2 ergibt {ergebnis!r}, erwartet war, dass der TimeoutError weiterfliegt."

# mit_sitzung benutzt closing
assert verwendet("closing"), "Benutzen Sie in mit_sitzung contextlib.closing."

# befrage_alle im Beispiel
netz = beispielnetz()
ergebnis = wert_von(lambda: befrage_alle(netz, ["sw-1", "sw-2", "sw-3"], "show version"))
assert ergebnis == {"sw-1": "IOS 15.2", "sw-3": "IOS 16.9"}, (
    f"befrage_alle(netz, ['sw-1', 'sw-2', 'sw-3'], 'show version') ergibt {ergebnis!r}, erwartet war {{'sw-1': 'IOS 15.2', 'sw-3': 'IOS 16.9'}}.\n"
    "Tipp: Setzen Sie with suppress(TimeoutError, ConnectionError): in die Schleife, um eine einzelne Abfrage."
)

# befrage_alle im Beispiel: alle Sitzungen sind danach geschlossen
assert netz.offene == [] and len(netz.sitzungen) == 2, f"Nach befrage_alle sind {netz.offene} offen, geöffnet wurden {len(netz.sitzungen)}; erwartet: 2 geöffnet, keine offen."

# befrage_alle mit anderen Switches und Befehl (nicht fest hinschreiben!)
netz = Testnetz({"a": {"show vlan": "1"}, "b": {"show vlan": "1, 99"}, "c": {"show vlan": "5"}})
ergebnis = wert_von(lambda: befrage_alle(netz, ["c", "a", "b"], "show vlan"))
assert ergebnis == {"c": "5", "a": "1", "b": "1, 99"} and list(ergebnis) == ["c", "a", "b"], (
    f"befrage_alle(netz, ['c', 'a', 'b'], 'show vlan') ergibt {ergebnis!r}, erwartet war {{'c': '5', 'a': '1', 'b': '1, 99'}} in dieser Reihenfolge."
)

# befrage_alle: auch ein abgelehnter Switch (ConnectionRefusedError) wird übersprungen
netz = Testnetz({"a": {"x": "1"}, "c": {"x": "3"}}, abgelehnt=["b"])
ergebnis = wert_von(lambda: befrage_alle(netz, ["a", "b", "c"], "x"))
assert ergebnis == {"a": "1", "c": "3"}, (
    f"befrage_alle mit einem Switch, der die Anmeldung ablehnt, ergibt {ergebnis!r}, erwartet war {{'a': '1', 'c': '3'}}.\n"
    "Tipp: ConnectionRefusedError ist eine Unterart von ConnectionError."
)

# befrage_alle: nach einem nicht erreichbaren Switch geht es weiter
netz = Testnetz({"b": {"x": "2"}, "c": {"x": "3"}}, nicht_erreichbar=["a"])
ergebnis = wert_von(lambda: befrage_alle(netz, ["a", "b", "c"], "x"))
assert ergebnis == {"b": "2", "c": "3"}, (
    f"befrage_alle, wenn der erste Switch nicht erreichbar ist, ergibt {ergebnis!r}, erwartet war {{'b': '2', 'c': '3'}}.\n"
    "Tipp: Steht suppress um die ganze Schleife, endet sie beim ersten Fehler."
)

# befrage_alle: keine Hosts oder keiner erreichbar
netz = Testnetz({}, nicht_erreichbar=["a", "b"])
ergebnis = wert_von(lambda: [befrage_alle(netz, [], "x"), befrage_alle(netz, ["a", "b"], "x")])
assert ergebnis == [{}, {}], f"befrage_alle ohne Hosts und ohne erreichbaren Switch ergibt {ergebnis!r}, erwartet war jeweils {{}}."

# befrage_alle: ein unbekannter Befehl (KeyError) fliegt weiter, die Sitzung wird trotzdem geschlossen
netz = Testnetz({"a": {"x": "1"}, "b": {}})
ergebnis = wert_von(lambda: befrage_alle(netz, ["a", "b"], "x"))
assert isinstance(ergebnis, str) and ergebnis.startswith("KeyError") and netz.offene == [], (
    f"befrage_alle mit einem Befehl, den b nicht kennt, ergibt {ergebnis!r}, offen: {netz.offene}; "
    "erwartet war, dass der KeyError weiterfliegt und keine Sitzung offen bleibt.\n"
    "Tipp: suppress soll nur TimeoutError und ConnectionError schlucken."
)

# befrage_alle benutzt suppress und mit_sitzung
assert verwendet("suppress") and verwendet("mit_sitzung"), "Benutzen Sie in befrage_alle contextlib.suppress und mit_sitzung."

# erster_erreichbarer im Beispiel
netz = beispielnetz()
ergebnis = wert_von(lambda: erster_erreichbarer(netz, ["sw-2", "sw-3", "sw-1"], "show version"))
assert ergebnis == ("sw-3", "IOS 16.9"), f"erster_erreichbarer(netz, ['sw-2', 'sw-3', 'sw-1'], 'show version') ergibt {ergebnis!r}, erwartet war ('sw-3', 'IOS 16.9')."

# erster_erreichbarer öffnet nach dem ersten Treffer keine Sitzung mehr
assert netz.versuche == ["sw-2", "sw-3"] and netz.offene == [], (
    f"erster_erreichbarer hat sich bei {netz.versuche} angemeldet (offen: {netz.offene}), erwartet war nur ['sw-2', 'sw-3'] und keine offene Sitzung.\n"
    "Tipp: Ein return im with-Block von suppress beendet die Funktion sofort."
)

# erster_erreichbarer: der erste Switch ist gleich erreichbar
netz = Testnetz({"a": {"x": "1"}, "b": {"x": "2"}})
ergebnis = wert_von(lambda: erster_erreichbarer(netz, ["b", "a"], "x"))
assert ergebnis == ("b", "2"), f"erster_erreichbarer(netz, ['b', 'a'], 'x') ergibt {ergebnis!r}, erwartet war ('b', '2')."

# erster_erreichbarer: keiner erreichbar oder keine Hosts
netz = Testnetz({}, nicht_erreichbar=["a"], abgelehnt=["b"])
ergebnis = wert_von(lambda: [erster_erreichbarer(netz, ["a", "b"], "x"), erster_erreichbarer(netz, [], "x")])
assert ergebnis == [None, None], f"erster_erreichbarer ohne erreichbaren Switch ergibt {ergebnis!r}, erwartet war jeweils None."

# Die Ausgabe des Programms
erwartet = "IOS 15.2\n{'sw-1': 'IOS 15.2', 'sw-3': 'IOS 16.9'}\n('sw-3', 'IOS 16.9')\nset()"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Netze
zufall = Zufall(4055)
for _ in range(200):
    hosts = [f"sw-{nummer}" for nummer in range(zufall.randint(0, 12))]
    zustand = {host: zufall.choice(["ok", "ok", "timeout", "abgelehnt"]) for host in hosts}
    switches = {host: {"show version": f"V{zufall.randint(1, 99)}"} for host in hosts if zustand[host] == "ok"}
    netz = Testnetz(
        switches,
        nicht_erreichbar=[h for h in hosts if zustand[h] == "timeout"],
        abgelehnt=[h for h in hosts if zustand[h] == "abgelehnt"],
    )
    zufall.shuffle(hosts)
    erwartet = {host: switches[host]["show version"] for host in hosts if host in switches}
    ergebnis = wert_von(lambda: befrage_alle(netz, hosts, "show version"))
    assert ergebnis == erwartet and list(ergebnis) == list(erwartet) and netz.offene == [], (
        f"befrage_alle für {zustand} in der Reihenfolge {hosts} ergibt {ergebnis!r}, erwartet war {erwartet}."
    )
    erster = next(((host, antwort) for host, antwort in erwartet.items()), None)
    ergebnis = wert_von(lambda: erster_erreichbarer(netz, hosts, "show version"))
    assert ergebnis == erster and netz.offene == [], f"erster_erreichbarer für {zustand} in der Reihenfolge {hosts} ergibt {ergebnis!r}, erwartet war {erster}."

# Obere Grenze: 500 Switches, jeder dritte nicht erreichbar
hosts = [f"sw-{nummer}" for nummer in range(500)]
switches = {host: {"show version": host.upper()} for nummer, host in enumerate(hosts) if nummer % 3}
netz = Testnetz(switches, nicht_erreichbar=[host for host in hosts if host not in switches])
ergebnis = wert_von(lambda: befrage_alle(netz, hosts, "show version"))
assert ergebnis == {host: host.upper() for host in switches} and netz.offene == [], "Bei 500 Switches stimmt befrage_alle nicht oder Sitzungen bleiben offen."
