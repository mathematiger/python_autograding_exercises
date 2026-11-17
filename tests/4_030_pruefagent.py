# Automatisch erzeugt aus lehrkraft/muster/4_030_pruefagent.py - nicht von Hand ändern.
# vorlage-hash: 0d9778818ec91e13
# text-hash: a508ee8be1b1fa96
# thema: funktionen
# inhalt: Dekoratoren auf Methoden und Klassen

class Speicher:
    """Testklasse für zaehle_aufrufe einzeln."""

    def __init__(self):
        self.daten = {}

    @zaehle_aufrufe
    def schreibe(self, schluessel, wert=None, *, notiz=""):
        """Legt einen Wert ab."""
        self.daten[schluessel] = (wert, notiz)
        return len(self.daten)

    @zaehle_aufrufe
    def lies(self, schluessel):
        """Liest einen Wert."""
        return self.daten[schluessel]


def zaehler(objekt):
    """Liefert self.aufrufe des Objekts oder eine Beschreibung, falls es fehlt."""
    return getattr(objekt, "aufrufe", "(kein Attribut aufrufe)")


# zaehle_aufrufe: Die Methode funktioniert weiter und gibt ihren Wert zurück
s = Speicher()
try:
    ergebnis = (s.schreibe("a", 1), s.schreibe("b", 2), s.lies("a"))
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == (1, 2, (1, "")), (
    f"Mit @zaehle_aufrufe liefern s.schreibe('a', 1), s.schreibe('b', 2), s.lies('a') {ergebnis!r}, "
    "erwartet war (1, 2, (1, '')).\nTipp: Die Hülle bekommt self als ersten Parameter und gibt "
    "return methode(self, *args, **kwargs) zurück."
)

# zaehle_aufrufe: Die Aufrufe werden je Methode gezählt
s = Speicher()
s.schreibe("a", 1)
s.schreibe("b", 2)
s.lies("a")
assert zaehler(s) == {"schreibe": 2, "lies": 1}, (
    f"Nach zweimal schreibe und einmal lies ist s.aufrufe {zaehler(s)!r}, erwartet war {{'schreibe': 2, 'lies': 1}}.\n"
    "Tipp: Legen Sie self.aufrufe beim ersten Aufruf als {} an und zählen Sie unter methode.__name__."
)

# zaehle_aufrufe: Schlüsselwort-Argumente kommen an
s = Speicher()
s.schreibe("x", wert=5, notiz="neu")
assert s.daten == {"x": (5, "neu")} and zaehler(s) == {"schreibe": 1}, (
    f"Nach s.schreibe('x', wert=5, notiz='neu') ist daten {s.daten!r} und aufrufe {zaehler(s)!r}, "
    "erwartet waren {'x': (5, 'neu')} und {'schreibe': 1}.\nTipp: Reichen Sie *args und **kwargs weiter."
)

# zaehle_aufrufe: Zwei Objekte zählen getrennt
a = Speicher()
b = Speicher()
a.schreibe("k", 1)
a.schreibe("k", 2)
b.schreibe("k", 3)
assert (zaehler(a), zaehler(b)) == ({"schreibe": 2}, {"schreibe": 1}), (
    f"Zwei Objekte: a schreibt zweimal, b einmal; a.aufrufe ist {zaehler(a)!r}, b.aufrufe {zaehler(b)!r}, "
    "erwartet waren {'schreibe': 2} und {'schreibe': 1}.\n"
    "Tipp: Speichern Sie die Zähler in self, nicht im Dekorator oder in einer globalen Variablen."
)

# zaehle_aufrufe: Auch ein Aufruf mit Ausnahme zählt, und die Ausnahme kommt durch
s = Speicher()
try:
    s.lies("fehlt")
    ausnahme = None
except KeyError as fehler:
    ausnahme = fehler
assert ausnahme is not None and zaehler(s) == {"lies": 1}, (
    f"s.lies('fehlt') soll einen KeyError durchlassen und trotzdem zählen; Ausnahme: {ausnahme!r}, "
    f"aufrufe: {zaehler(s)!r}, erwartet {{'lies': 1}}.\nTipp: Zählen Sie, bevor Sie die Methode aufrufen."
)

# zaehle_aufrufe: Name und Docstring bleiben erhalten
bekommen = (Speicher.schreibe.__name__, Speicher.schreibe.__doc__)
assert bekommen == ("schreibe", "Legt einen Wert ab."), (
    f"Speicher.schreibe.__name__ und __doc__ sind {bekommen!r}, erwartet war ('schreibe', 'Legt einen Wert ab.').\n"
    "Tipp: Setzen Sie @functools.wraps(methode) über die innere Funktion."
)

# alle_zaehlen: Das Beispiel aus der Aufgabe
agent = CpuAgent()
agent.messe(45)
agent.messe(95)
alarm = agent.ist_alarm()
assert alarm is True and zaehler(agent) == {"messe": 2, "ist_alarm": 1}, (
    f"CpuAgent: nach messe(45), messe(95), ist_alarm() ist das Ergebnis {alarm!r} und aufrufe "
    f"{zaehler(agent)!r}, erwartet waren True und {{'messe': 2, 'ist_alarm': 1}}."
)

# alle_zaehlen: Die Methode wird umhüllt, Name und Docstring bleiben erhalten
class Anzeige:
    def zeige(self):
        """Zeigt den Stand."""
        return "Stand"

urspruenglich = Anzeige.zeige
Anzeige = alle_zaehlen(Anzeige)  # dasselbe wie @alle_zaehlen über der Klasse
bekommen = (Anzeige.zeige is not urspruenglich, Anzeige.zeige.__name__, Anzeige.zeige.__doc__)
assert bekommen == (True, "zeige", "Zeigt den Stand."), (
    "Nach alle_zaehlen(Anzeige) erwartet: Anzeige.zeige ist umhüllt (nicht mehr die ursprüngliche Funktion), "
    f"__name__ 'zeige' und __doc__ 'Zeigt den Stand.'; bekommen (umhüllt, __name__, __doc__) = {bekommen!r}.\n"
    + ("Tipp: Ersetzen Sie die Methode mit setattr(klasse, name, zaehle_aufrufe(wert))."
       if not bekommen[0] else "Tipp: zaehle_aufrufe braucht @functools.wraps(methode) über der Hülle.")
)

# alle_zaehlen: __init__, Namen mit Unterstrich und Werte bleiben, wie sie sind
class RamAgent:
    GRENZE = 80
    EINHEIT = "Prozent"

    def __init__(self):
        self.letzter = None

    def _umrechnen(self, wert):
        return round(wert)

    def messe(self, wert):
        self.letzter = self._umrechnen(wert)
        return self.letzter

RamAgent = alle_zaehlen(RamAgent)  # dasselbe wie @alle_zaehlen über der Klasse

# alle_zaehlen: __init__, Namen mit Unterstrich und Werte bleiben, wie sie sind
ergebnis = (lambda ram: (ram.messe(81.6), RamAgent.GRENZE, RamAgent.EINHEIT, zaehler(ram)))(RamAgent())
assert ergebnis == (82, 80, "Prozent", {"messe": 1}), (
    "RamAgent mit GRENZE, EINHEIT, __init__, _umrechnen und messe: nach messe(81.6) erwartet "
    f"(82, 80, 'Prozent', {{'messe': 1}}) für (Ergebnis, GRENZE, EINHEIT, aufrufe), bekommen {ergebnis!r}.\n"
    "Tipp: Umhüllen Sie nur Funktionen (callable), deren Name nicht mit _ beginnt."
)

# alle_zaehlen: geerbte Methoden werden nicht doppelt gezählt
class Basis:
    def melde(self):
        return "ok"

Basis = alle_zaehlen(Basis)  # dasselbe wie @alle_zaehlen über der Klasse

class Kind(Basis):
    def pruefe(self):
        return self.melde()

Kind = alle_zaehlen(Kind)

# alle_zaehlen: geerbte Methoden werden nicht doppelt gezählt
ergebnis = (lambda kind: (kind.pruefe(), zaehler(kind)))(Kind())
assert ergebnis == ("ok", {"pruefe": 1, "melde": 1}), (
    f"Kind(Basis), beide mit @alle_zaehlen: kind.pruefe() ruft melde auf; Ergebnis und aufrufe sind {ergebnis!r}, "
    f"erwartet waren 'ok' und {{'pruefe': 1, 'melde': 1}}.\n"
    "Tipp: Gehen Sie mit vars(klasse) nur die Attribute durch, die direkt in der Klasse stehen."
)

# Viele zufällige Aufrufe auf mehreren Agenten
zufall = Zufall(4030)
agenten = [CpuAgent() for _ in range(4)]
erwartet = [{} for _ in agenten]
for _ in range(2000):
    nummer = zufall.randrange(len(agenten))
    if zufall.random() < 0.7:
        agenten[nummer].messe(zufall.randint(0, 100))
        name = "messe"
    else:
        agenten[nummer].ist_alarm()
        name = "ist_alarm"
    erwartet[nummer][name] = erwartet[nummer].get(name, 0) + 1
bekommen = [zaehler(agent) for agent in agenten]
assert bekommen == erwartet, f"Nach 2000 zufälligen Aufrufen auf vier Agenten sind die Zähler {bekommen}, erwartet war {erwartet}."

# Obere Grenze: 100 000 Aufrufe auf einem Objekt
viel = CpuAgent()
for wert in range(100_000):
    viel.messe(wert % 100)
assert zaehler(viel) == {"messe": 100_000} and len(viel.werte) == 100_000, (
    f"Nach 100 000 Aufrufen von messe ist aufrufe {zaehler(viel)!r}, erwartet war {{'messe': 100000}}."
)
