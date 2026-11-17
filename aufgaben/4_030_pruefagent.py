"""Aufgabe 4_030 – Prüfagent                                     Stufe 4 ★★★★☆

Ein Monitoring-System lässt auf jedem Server kleine Prüfagenten laufen, die
Messwerte entgegennehmen und Alarm melden. Das Betriebsteam will wissen, wie
oft jede Methode eines Agenten aufgerufen wird, um zu erkennen, ob ein Agent
hängt oder mit Anfragen überflutet wird. Die Zählung soll nicht in jede
Methode hineingeschrieben werden, sondern einmal als Dekorator entstehen, der
sich auf Methoden setzen lässt, und einmal als Klassen-Dekorator, der das für
alle Methoden einer Klasse auf einen Schlag erledigt. Schreiben Sie:

- `zaehle_aufrufe(methode)`, einen Dekorator für Methoden. Die umhüllte
  Methode erhöht bei jedem Aufruf im Dictionary `self.aufrufe` den Zähler
  unter dem Namen der Methode um 1 und ruft dann die ursprüngliche Methode
  mit allen Argumenten auf; deren Rückgabewert gibt sie zurück. Gibt es
  `self.aufrufe` noch nicht, legt sie es als leeres Dictionary an. Der Aufruf
  zählt auch, wenn die Methode eine Ausnahme auslöst. Name und Docstring der
  Methode bleiben erhalten (functools.wraps).
- `alle_zaehlen(klasse)`, einen Klassen-Dekorator. Er umhüllt jede Funktion,
  die direkt im Klassenkörper steht und deren Name nicht mit einem
  Unterstrich beginnt, mit zaehle_aufrufe, und gibt die Klasse selbst
  zurück. Andere Klassenattribute (Zahlen, Texte) und Methoden wie __init__
  oder _intern bleiben unverändert.

    @alle_zaehlen
    class CpuAgent:
        GRENZE = 90
        def __init__(self): self.werte = []
        def messe(self, wert): self.werte.append(wert)
        def ist_alarm(self): return max(self.werte, default=0) > self.GRENZE

    agent = CpuAgent()
    agent.messe(45); agent.messe(95); agent.ist_alarm()
    agent.aufrufe            →  {"messe": 2, "ist_alarm": 1}
    CpuAgent.messe.__name__  →  "messe"

Grenzen: Die Methoden haben beliebige Positions- und Schlüsselwort-
Argumente. Jedes Objekt hat seine eigenen Zähler; zwei Agenten zählen
getrennt. Ein Objekt bekommt bis zu 100 000 Aufrufe. Die Klassen enthalten
im Körper nur normale Methoden (keine staticmethod, classmethod oder
property) und einfache Werte.

Hintergrund: Ein Dekorator (Aufgabe 4_022) ist eine Funktion, die eine
Funktion bekommt und eine neue zurückgibt. Auf einer Methode funktioniert
das genauso, denn im Klassenkörper ist eine Methode zunächst eine normale
Funktion, deren erster Parameter self ist. Die Hülle muss darum self als
ersten Parameter entgegennehmen und an die ursprüngliche Methode
weitergeben; so kommt sie auch an das Objekt heran:

    def protokolliert(methode):
        @functools.wraps(methode)
        def huelle(self, *args, **kwargs):
            print(f"{type(self).__name__}.{methode.__name__}{args}")
            return methode(self, *args, **kwargs)
        return huelle

Weil die Hülle bei jedem Aufruf ihr self bekommt, kann sie Zustand im
Objekt ablegen statt im Dekorator; so hat jedes Objekt seinen eigenen.
getattr(self, "name", None) und vars(self) helfen, ein Attribut nur beim
ersten Mal anzulegen: getattr(objekt, "name", standard) liest das
Attribut name oder liefert standard, wenn es fehlt, und "name" in
vars(objekt) fragt, ob das Objekt selbst das Attribut hat.

Ein Klassen-Dekorator ist eine Funktion, die eine fertige Klasse bekommt.
@registriere über class Agent: bedeutet Agent = registriere(Agent). Er kann
die Klasse untersuchen und verändern und gibt sie (meist dieselbe) zurück:

    def zeige_methoden(klasse):
        for name, wert in vars(klasse).items():
            if callable(wert):
                print(name)
        return klasse

vars(klasse) liefert die Attribute, die direkt im Klassenkörper stehen, als
Dictionary (geerbte nicht). callable(wert) ist True für alles, was man
aufrufen kann, etwa Funktionen; setattr(klasse, "name", wert) wirkt wie
klasse.name = wert, nur mit dem Namen als Text. Ändern sollte man die Klasse nicht während des
Durchlaufens dieses Dictionarys, sondern mit setattr(klasse, name, neu) über
eine Kopie wie list(vars(klasse).items()). Klassen-Dekoratoren sind die
einfache Alternative zu Metaklassen (Stufe 5), wenn man eine Klasse nur
einmal nach dem Erzeugen anpassen will; @dataclass ist auch einer.
"""

import functools


def zaehle_aufrufe(methode):
    """Dekorator: zählt die Aufrufe von methode je Objekt in self.aufrufe."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def alle_zaehlen(klasse):
    """Klassen-Dekorator: versieht alle öffentlichen Methoden von klasse mit zaehle_aufrufe."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
    return klasse


@alle_zaehlen
class CpuAgent:
    """Nimmt CPU-Auslastungen in Prozent entgegen und meldet Alarm über der Grenze."""

    GRENZE = 90

    def __init__(self):
        self.werte = []

    def messe(self, wert):
        """Speichert einen Messwert."""
        self.werte.append(wert)

    def ist_alarm(self):
        """True, wenn ein Messwert über der Grenze liegt."""
        return max(self.werte, default=0) > self.GRENZE


agent = CpuAgent()
agent.messe(45)
agent.messe(95)
print(agent.ist_alarm(), getattr(agent, "aufrufe", {}))
