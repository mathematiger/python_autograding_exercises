"""Aufgabe 5_063 – Sensorsimulation                              Stufe 5 ★★★★★

In einer Lagerhalle sollen batteriebetriebene Sensorknoten verteilt
werden. Jeder Knoten schickt in seinem festen Intervall eine Nachricht
an ein Gateway, eine Empfangsstation, die die Nachrichten puffert und
in ihrem eigenen Takt gesammelt in die Cloud hochlädt. Jede Nachricht
kostet Batterie; reicht der Rest nicht mehr für eine Nachricht, schweigt
der Knoten. Bevor die Hardware bestellt wird, will das Team ausprobieren,
welche Intervalle und welcher Takt zusammenpassen: wann welche
Nachricht oben ankommt und wie lange die Batterien reichen. Dafür
schreiben Sie eine kleine ereignisgesteuerte Simulation (siehe
Hintergrund). Die Zeit zählt in ganzen Sekunden ab 0.

- `Ereignis` ist eine dataclass mit order=True und den Feldern zeit,
  nummer und ablauf (der Generator, der zur Zeit zeit weiterlaufen
  soll). Verglichen wird nur nach zeit und bei gleicher Zeit nach
  nummer, ablauf nie.
- `Geraet` ist ein Protokoll (typing.Protocol, schon mit
  @runtime_checkable versehen): Ein Gerät hat ein Attribut name (Text)
  und eine Methode lauf(sim), die einen Generator liefert. Jeder Wert,
  den er mit yield liefert, ist die Wartezeit in Sekunden bis zu seinem
  nächsten Schritt; endet der Generator, ist das Gerät fertig.
- in der Klasse `Simulation` (jetzt, endzeit, warteschlange und zaehler
  legt __init__ schon an):
  - `plane(self, ablauf, zeit)` legt mit heapq ein Ereignis für den
    Generator ablauf zur Zeit zeit in die Warteschlange; nummer ist die
    nächste Zahl aus self.zaehler.
  - `starte(self, geraet)` erzeugt den Generator geraet.lauf(self) und
    plant ihn für die Zeit self.jetzt ein.
  - `laufe(self)` nimmt immer das früheste Ereignis heraus, solange
    seine Zeit höchstens endzeit ist, setzt jetzt auf diese Zeit und
    lässt den Generator mit next bis zum nächsten yield laufen. Liefert
    er eine Wartezeit, wird er für jetzt + Wartezeit neu eingeplant;
    endet er (StopIteration), nicht. Am Ende ist jetzt = endzeit.
    Ereignisse mit gleicher Zeit kommen also in der Reihenfolge dran,
    in der sie eingeplant wurden.
- `Sensorknoten.lauf(sim)` wartet, solange die batterie für eine
  Nachricht reicht (mindestens verbrauch), jeweils intervall Sekunden,
  zieht dann verbrauch von batterie ab und übergibt dem gateway mit
  empfange die Nachricht (sim.jetzt, name).
- `Gateway.lauf(sim)` wartet immer wieder takt Sekunden und hängt dann,
  wenn der puffer nicht leer ist, das Paar (sim.jetzt, Liste der
  Nachrichten im puffer) an uploads und beginnt einen leeren puffer.
- `simuliere(knoten, takt, endzeit)` baut ein Gateway "gateway" mit
  takt und zu jedem Tupel (name, intervall, batterie, verbrauch) der
  Liste knoten einen Sensorknoten, startet erst das Gateway und dann
  die Knoten in der Reihenfolge der Liste, lässt die Simulation bis
  endzeit laufen und gibt die uploads des Gateways zurück.

    gateway = Gateway("gateway", takt=10)
    s1 = Sensorknoten("s1", intervall=4, batterie=10, verbrauch=3, gateway=gateway)
    s2 = Sensorknoten("s2", intervall=15, batterie=100, verbrauch=1, gateway=gateway)
    sim = Simulation(endzeit=30)
    sim.starte(gateway); sim.starte(s1); sim.starte(s2)
    sim.laufe()
    gateway.uploads  →  [(10, [(4, "s1"), (8, "s1")]),
                         (20, [(12, "s1"), (15, "s2")]),
                         (30, [(30, "s2")])]
    s1.batterie, s2.batterie, sim.jetzt     →  (1, 98, 30)
    simuliere([("s1", 4, 10, 3), ("s2", 15, 100, 1)], 10, 30)
        →  dieselbe Liste wie gateway.uploads

s1 schweigt nach der dritten Nachricht, weil 1 nicht für eine weitere
reicht. Die Nachricht von s2 zur Zeit 30 kommt noch mit dem Upload
zur Zeit 30 mit: Ihr Ereignis wurde schon zur Zeit 15 eingeplant, das
des Gateways erst zur Zeit 20.

Grenzen: endzeit ist eine ganze Zahl von 0 bis 10**6, intervall und
takt von 1 bis 10 000, batterie von 0 bis 10**6, verbrauch von 1 bis
10 000. knoten hat 0 bis 1000 Tupel mit verschiedenen Namen. Andere
Geräte liefern Wartezeiten als ganze Zahlen ab 0. Bis zur endzeit gibt
es höchstens 100 000 Ereignisse; laufe soll für jedes O(log P) Schritte
brauchen, wobei P die Zahl der Geräte ist.

Hintergrund: Eine Simulation, die Sekunde für Sekunde weiterzählt und
jedes Gerät fragt, ob es gerade etwas tun will, verschwendet fast die
ganze Zeit mit Nichtstun. Eine ereignisgesteuerte Simulation springt
stattdessen von Ereignis zu Ereignis: Sie hält eine Warteschlange der
geplanten Ereignisse, nimmt immer das früheste heraus, stellt die Uhr
auf dessen Zeit und führt es aus; dabei entstehen neue Ereignisse für
später. Die Warteschlange ist ein Heap (Aufgabe 4_074), denn sie muss
nur schnell das kleinste Element liefern: heappush und heappop kosten
O(log n).

Was im Heap liegt, muss sich vergleichen lassen. Eine dataclass mit
order=True (Aufgabe 4_014) vergleicht ihre Felder der Reihe nach wie
ein Tupel; mit field(compare=False) nimmt man ein Feld davon aus:

    from dataclasses import dataclass, field

    @dataclass(order=True)
    class Auftrag:
        prioritaet: int
        nummer: int
        text: str = field(compare=False)

    Auftrag(1, 7, "b") < Auftrag(1, 8, "a")      # True, nach nummer

Die laufende nummer (Tie-Breaker) braucht man aus zwei Gründen. Erstens
haben oft mehrere Ereignisse dieselbe Zeit; ohne nummer würde Python
dann die Generatoren vergleichen und mit TypeError abbrechen, denn
Generatoren lassen sich nicht ordnen. Zweitens wird die Reihenfolge so
festgelegt: Bei gleicher Zeit kommt dran, was früher eingeplant wurde.
Damit geht jeder Lauf gleich aus, und ein Fehler lässt sich nachstellen.
itertools.count() liefert die Zahlen 0, 1, 2 … mit next.

Die Geräte selbst sind Generatoren (Aufgabe 4_034). Ein Generator hält
bei yield an und behält dabei alle lokalen Variablen und die Stelle im
Code; erst das nächste next lässt ihn weiterlaufen. Genau das braucht
ein Prozess, der wartet: Er liefert mit yield, wie lange er warten will,
und die Simulation weckt ihn zur passenden Zeit mit next wieder auf.
So schreibt man den Ablauf eines Geräts als einfache Schleife statt als
Zustandsautomaten:

    class Blinker:
        def __init__(self, name, an, aus):
            self.name, self.an, self.aus = name, an, aus
            self.protokoll = []

        def lauf(self, sim):
            while True:
                self.protokoll.append((sim.jetzt, "an"))
                yield self.an                  # an Sekunden warten
                self.protokoll.append((sim.jetzt, "aus"))
                yield self.aus

Die Simulation kennt keine Sensoren und kein Gateway, nur das, was
jedes Gerät hat: einen name und eine Methode lauf. Diese Schnittstelle
beschreibt ein Protocol (Aufgabe 5_016); Sensorknoten, Gateway und der
Blinker erfüllen es, ohne davon zu erben, und @runtime_checkable
erlaubt isinstance(objekt, Geraet). So bleibt der Aufbau des Programms
sauber getrennt: Simulation (wann), Geräte (was), simuliere (welche
Geräte mit welchen Einstellungen). Ein neues Gerät braucht keine
Änderung an der Simulation.

Echte Simulationsbibliotheken wie SimPy sind genauso gebaut. Dort
bekommt ein Prozess oft über send (Aufgabe 5_027) etwas zurück, etwa
jetzt = yield wartezeit; hier liest er die Zeit einfach aus sim.jetzt.
"""

import heapq
import itertools
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(order=True)
class Ereignis:
    """Der Generator ablauf soll zur Zeit zeit weiterlaufen; nummer entscheidet bei gleicher Zeit."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@runtime_checkable
class Geraet(Protocol):
    """Alles, was in der Simulation laufen kann: ein Name und ein Ablauf als Generator."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Simulation:
    """Eine ereignisgesteuerte Simulation, die bis zur endzeit läuft."""

    def __init__(self, endzeit):
        self.endzeit = endzeit
        self.jetzt = 0
        self.warteschlange = []
        self.zaehler = itertools.count()

    def plane(self, ablauf, zeit):
        """Legt ein Ereignis für den Generator ablauf zur Zeit zeit in die Warteschlange."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def starte(self, geraet):
        """Erzeugt den Ablauf des Geräts und plant ihn für jetzt ein."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def laufe(self):
        """Arbeitet die Ereignisse bis einschließlich endzeit der Zeit nach ab."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@dataclass
class Gateway:
    """Puffert die Nachrichten der Sensorknoten und lädt sie im Takt hoch."""

    name: str
    takt: int
    puffer: list = field(default_factory=list)
    uploads: list = field(default_factory=list)

    def empfange(self, nachricht):
        """Nimmt eine Nachricht (zeit, name) in den Puffer auf."""
        self.puffer.append(nachricht)

    def lauf(self, sim):
        """Lädt alle takt Sekunden den Puffer hoch, wenn er nicht leer ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@dataclass
class Sensorknoten:
    """Sendet in festem Intervall Nachrichten an das Gateway, solange die Batterie reicht."""

    name: str
    intervall: int
    batterie: int
    verbrauch: int
    gateway: Gateway

    def lauf(self, sim):
        """Wartet intervall Sekunden und sendet, solange batterie für eine Nachricht reicht."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def simuliere(knoten, takt, endzeit):
    """Simuliert ein Gateway mit den Sensorknoten aus knoten bis endzeit; gibt die Uploads zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


gateway = Gateway("gateway", takt=10)
s1 = Sensorknoten("s1", intervall=4, batterie=10, verbrauch=3, gateway=gateway)
s2 = Sensorknoten("s2", intervall=15, batterie=100, verbrauch=1, gateway=gateway)
sim = Simulation(endzeit=30)
sim.starte(gateway)
sim.starte(s1)
sim.starte(s2)
sim.laufe()
print(gateway.uploads)
print(s1.batterie, s2.batterie, sim.jetzt)
print(simuliere([("s1", 4, 10, 3), ("s2", 15, 100, 1)], 10, 30))
