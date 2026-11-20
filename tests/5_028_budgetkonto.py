# Automatisch erzeugt aus lehrkraft/muster/5_028_budgetkonto.py - nicht von Hand ändern.
# vorlage-hash: b7dc188532737bcc
# text-hash: 76223ac3f9339282
# thema: kontrollfluss
# inhalt: throw, close, finally in Generatoren

def schritt(konto, aktion, wert=None):
    """Führt next, send, throw oder close aus; eine Ausnahme wird als Text zurückgegeben."""
    try:
        if aktion == "next":
            return next(konto)
        if aktion == "send":
            return konto.send(wert)
        if aktion == "throw":
            return konto.throw(wert)
        return konto.close()
    except StopIteration:
        return "StopIteration"
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def neues_konto(budget):
    """Legt ein Konto mit eigenem Protokoll an und startet es; gibt (konto, protokoll, erster Wert) zurück."""
    protokoll = []
    konto = budgetkonto(budget, protokoll)
    return konto, protokoll, schritt(konto, "next")


def vergleich(budget, buchungen):
    """Vergleichslösung für abrechnen, ohne Generator."""
    rest = budget
    eintraege = []
    for buchung in buchungen:
        if buchung < 0:
            rest -= buchung
            eintraege.append(f"storniert: {-buchung}")
        elif buchung <= rest:
            rest -= buchung
            eintraege.append(f"gebucht: {buchung}")
        else:
            eintraege.append(f"abgelehnt: {buchung}")
    eintraege.append(f"Abschluss: Rest {rest}")
    return eintraege


class Beobachter:
    """Hülle um ein Konto, die sich merkt, welche Methoden abrechnen aufruft."""

    def __init__(self, konto):
        """Merkt sich das echte Konto und legt die Liste der Aufrufe an."""
        self.konto = konto
        self.aufrufe = []

    def __iter__(self):
        """Ein Generator ist sein eigener Iterator; die Hülle auch."""
        return self

    def __next__(self):
        """Reicht next an das Konto weiter."""
        self.aufrufe.append("next")
        return next(self.konto)

    def send(self, wert):
        """Reicht send an das Konto weiter."""
        self.aufrufe.append("send")
        return self.konto.send(wert)

    def throw(self, *argumente):
        """Reicht throw an das Konto weiter."""
        self.aufrufe.append("throw")
        return self.konto.throw(*argumente)

    def close(self):
        """Reicht close an das Konto weiter."""
        self.aufrufe.append("close")
        return self.konto.close()


def aufrufe_in_abrechnen(budget, buchungen):
    """Ruft abrechnen auf und gibt zurück, welche Methoden es am Konto aufruft."""
    global budgetkonto
    echtes_budgetkonto = budgetkonto
    beobachter = []

    def beobachtet(*argumente):
        """Erzeugt ein echtes Konto in einer Hülle, die mitschreibt."""
        beobachter.append(Beobachter(echtes_budgetkonto(*argumente)))
        return beobachter[-1]

    budgetkonto = beobachtet
    try:
        abrechnen(budget, buchungen)
    finally:
        budgetkonto = echtes_budgetkonto
    return [b.aufrufe for b in beobachter]


def gleich(protokoll, erwartet):
    """Vergleicht zwei Protokolle Eintrag für Eintrag, ohne auf Groß-/Kleinschreibung und Satzzeichen zu achten."""
    return [vergleichbar(str(eintrag)) for eintrag in protokoll] == [vergleichbar(eintrag) for eintrag in erwartet]


# Das erste next liefert das Budget
konto, protokoll, erster = neues_konto(1000)
assert erster == 1000, (
    f"next(budgetkonto(1000, protokoll)) ergibt {erster!r}, erwartet war 1000.\n"
    "Tipp: Das erste yield liefert den Rest, und am Anfang ist der Rest das Budget."
)

# send bucht eine Ausgabe und liefert den Rest
konto, protokoll, _ = neues_konto(1000)
ergebnis = schritt(konto, "send", 300)
assert ergebnis == 700, f"Nach next() ergibt send(300) {ergebnis!r}, erwartet war 700."

# Mehrere Ausgaben nacheinander (nicht fest hinschreiben!)
konto, protokoll, _ = neues_konto(1000)
ergebnis = [schritt(konto, "send", betrag) for betrag in (100, 250, 50)]
assert ergebnis == [900, 650, 600], f"send(100), send(250), send(50) ergeben {ergebnis!r}, erwartet war [900, 650, 600]."

# Gebuchte Ausgaben stehen im Protokoll
konto, protokoll, _ = neues_konto(1000)
schritt(konto, "send", 300)
assert gleich(protokoll, ["gebucht: 300"]), f"Nach send(300) ist das Protokoll {protokoll!r}, erwartet war ['gebucht: 300']."

# Eine zu große Ausgabe wird abgelehnt, der Rest bleibt
konto, protokoll, _ = neues_konto(1000)
ergebnis = [schritt(konto, "send", 300), schritt(konto, "send", 900)]
assert ergebnis == [700, 700] and gleich(protokoll, ["gebucht: 300", "abgelehnt: 900"]), (
    f"send(300), send(900) ergeben {ergebnis!r} mit Protokoll {protokoll!r}, erwartet war [700, 700] "
    "mit ['gebucht: 300', 'abgelehnt: 900']."
)

# Genau der ganze Rest darf gebucht werden
konto, protokoll, _ = neues_konto(500)
ergebnis = schritt(konto, "send", 500)
assert ergebnis == 0 and gleich(protokoll, ["gebucht: 500"]), (
    f"budgetkonto(500, ...): send(500) ergibt {ergebnis!r} mit Protokoll {protokoll!r}, erwartet war 0 mit ['gebucht: 500']."
)

# Eine Ausgabe von 0 wird gebucht
konto, protokoll, _ = neues_konto(0)
ergebnis = schritt(konto, "send", 0)
assert ergebnis == 0 and gleich(protokoll, ["gebucht: 0"]), (
    f"budgetkonto(0, ...): send(0) ergibt {ergebnis!r} mit Protokoll {protokoll!r}, erwartet war 0 mit ['gebucht: 0']."
)

# throw(Storno(...)) schreibt den Betrag gut und liefert den neuen Rest
konto, protokoll, _ = neues_konto(1000)
ergebnis = [schritt(konto, "send", 300), schritt(konto, "throw", Storno(200))]
assert ergebnis == [700, 900], (
    f"send(300), throw(Storno(200)) ergeben {ergebnis!r}, erwartet war [700, 900].\n"
    "Tipp: Fangen Sie Storno mit try/except direkt um das yield ab und lassen Sie die Schleife weiterlaufen."
)

# Der Storno steht im Protokoll
konto, protokoll, _ = neues_konto(1000)
schritt(konto, "send", 300)
schritt(konto, "throw", Storno(200))
assert gleich(protokoll, ["gebucht: 300", "storniert: 200"]), (
    f"Nach send(300), throw(Storno(200)) ist das Protokoll {protokoll!r}, erwartet war ['gebucht: 300', 'storniert: 200']."
)

# Nach einem Storno läuft das Konto weiter
konto, protokoll, _ = neues_konto(100)
ergebnis = [schritt(konto, "throw", Storno(50)), schritt(konto, "send", 150), schritt(konto, "send", 1)]
assert ergebnis == [150, 0, 0], (
    f"budgetkonto(100, ...): throw(Storno(50)), send(150), send(1) ergeben {ergebnis!r}, erwartet war [150, 0, 0]."
)

# close schreibt den Abschluss ins Protokoll
konto, protokoll, _ = neues_konto(1000)
schritt(konto, "send", 300)
schritt(konto, "close")
assert gleich(protokoll, ["gebucht: 300", "Abschluss: Rest 700"]), (
    f"Nach send(300) und close() ist das Protokoll {protokoll!r}, erwartet war ['gebucht: 300', 'Abschluss: Rest 700'].\n"
    "Tipp: Ein finally-Block um die Schleife läuft auch, wenn close() GeneratorExit hineinwirft."
)

# Das ganze Beispiel aus der Aufgabe
konto, protokoll, _ = neues_konto(1000)
ergebnis = [schritt(konto, "send", 300), schritt(konto, "send", 900), schritt(konto, "throw", Storno(200)), schritt(konto, "close")]
erwartet = ["gebucht: 300", "abgelehnt: 900", "storniert: 200", "Abschluss: Rest 900"]
assert ergebnis == [700, 700, 900, None] and gleich(protokoll, erwartet), (
    f"Das Beispiel ergibt {ergebnis!r} mit Protokoll {protokoll!r},\nerwartet war [700, 700, 900, None] mit {erwartet!r}."
)

# close ohne weitere Buchungen
konto, protokoll, _ = neues_konto(42)
ergebnis = schritt(konto, "close")
assert ergebnis is None and gleich(protokoll, ["Abschluss: Rest 42"]), (
    f"Direkt nach next() ergibt close() {ergebnis!r} mit Protokoll {protokoll!r}, erwartet war None mit ['Abschluss: Rest 42'].\n"
    "Tipp: Fangen Sie GeneratorExit nicht ab, um danach weiterzumachen; ein yield danach löst einen RuntimeError aus."
)

# Ein zweites close tut nichts mehr
konto, protokoll, _ = neues_konto(42)
schritt(konto, "close")
ergebnis = schritt(konto, "close")
assert ergebnis is None and gleich(protokoll, ["Abschluss: Rest 42"]), (
    f"Nach zweimal close() ist das Protokoll {protokoll!r}, erwartet war genau einmal ['Abschluss: Rest 42']."
)

# Eine andere hineingeworfene Ausnahme läuft weiter, der Abschluss steht trotzdem im Protokoll
konto, protokoll, _ = neues_konto(1000)
schritt(konto, "send", 100)
ergebnis = schritt(konto, "throw", KeyError("Kostenstelle"))
assert ergebnis.startswith("KeyError") and gleich(protokoll, ["gebucht: 100", "Abschluss: Rest 900"]), (
    f"throw(KeyError(...)) ergibt {ergebnis!r} mit Protokoll {protokoll!r}, erwartet war ein KeyError beim Aufrufer "
    "und das Protokoll ['gebucht: 100', 'Abschluss: Rest 900'].\nTipp: Fangen Sie nur Storno ab, nicht jede Ausnahme."
)

# Nach einer anderen Ausnahme ist das Konto beendet
konto, protokoll, _ = neues_konto(1000)
schritt(konto, "throw", KeyError("Kostenstelle"))
ergebnis = schritt(konto, "send", 1)
assert ergebnis == "StopIteration" and len(protokoll) == 1, (
    f"Nach throw(KeyError(...)) ergibt send(1) {ergebnis!r} und das Protokoll ist {protokoll!r}; erwartet war "
    "StopIteration und nur der Abschluss."
)

# abrechnen im Beispiel
ergebnis = abrechnen(500, [200, -50, 400])
erwartet = ["gebucht: 200", "storniert: 50", "abgelehnt: 400", "Abschluss: Rest 350"]
assert gleich(ergebnis, erwartet), f"abrechnen(500, [200, -50, 400]) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# abrechnen ohne Buchungen
ergebnis = abrechnen(77, [])
assert gleich(ergebnis, ["Abschluss: Rest 77"]), f"abrechnen(77, []) ergibt {ergebnis!r}, erwartet war ['Abschluss: Rest 77']."

# abrechnen startet das Konto, benutzt send und throw und schließt es selbst
aufrufe = aufrufe_in_abrechnen(500, [200, -50, 400])
assert aufrufe == [["next", "send", "throw", "send", "close"]], (
    f"abrechnen(500, [200, -50, 400]) ruft am Konto {aufrufe!r} auf, erwartet war "
    "[['next', 'send', 'throw', 'send', 'close']] (ein Konto: starten, send, throw, send, close).\n"
    "Tipp: Verlassen Sie sich nicht darauf, dass Python das Konto irgendwann selbst schließt; rufen Sie konto.close() auf."
)

# Die Ausgabe des Programms
erwartet = (
    "1000 700 700 900\n['gebucht: 300', 'abgelehnt: 900', 'storniert: 200', 'Abschluss: Rest 900']\n"
    "['gebucht: 200', 'storniert: 50', 'abgelehnt: 400', 'Abschluss: Rest 350']"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Abrechnungen
zufall = Zufall(5028)
for runde in range(400):
    budget = zufall.choice([0, zufall.randint(0, 100), zufall.randint(0, 10**9)])
    buchungen = []
    for _ in range(zufall.randint(0, 8)):
        betrag = zufall.choice([0, zufall.randint(0, 60), zufall.randint(0, 10**9)])
        buchungen.append(-betrag if zufall.random() < 0.3 and betrag > 0 else betrag)
    ergebnis = abrechnen(budget, buchungen)
    erwartet = vergleich(budget, buchungen)
    assert gleich(ergebnis, erwartet), f"abrechnen({budget}, {buchungen})\n  ergibt   {ergebnis!r}\n  erwartet {erwartet!r}"

# Obere Grenze: 20 000 Buchungen
buchungen = [zufall.choice([zufall.randint(0, 10**6), -zufall.randint(1, 10**6)]) for _ in range(20000)]
ergebnis = abrechnen(10**9, buchungen)
erwartet = vergleich(10**9, buchungen)
assert gleich(ergebnis, erwartet), (
    f"abrechnen(10**9, …) mit 20 000 Buchungen ergibt {len(ergebnis)} Protokolleinträge, der letzte {ergebnis[-1:]!r}; "
    f"erwartet waren {len(erwartet)}, der letzte {erwartet[-1:]!r}."
)
