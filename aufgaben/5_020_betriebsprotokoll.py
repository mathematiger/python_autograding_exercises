"""Aufgabe 5_020 – Betriebsprotokoll                             Stufe 5 ★★★★★

Ein Rechenzentrum betreibt virtuelle Maschinen (VMs) für Kunden. Ein
Automatisierungsskript verteilt neue VMs auf Hosts und startet sie.
Zwei Bausteine fehlen noch:

Erstens eine Platzierungsregel: Ein Host hat eine bestimmte Zahl
freier CPU-Kerne und freien Arbeitsspeicher (RAM) in GB. Die Regel
soll sich wie eine Funktion benutzen lassen, damit man sie direkt an
filter oder an andere Werkzeuge übergeben kann, und sie soll mitzählen,
wie oft sie gefragt wurde. Vervollständigen Sie `Platzierungsregel`:

- `__call__(self, vm)` bekommt eine VM als Tupel (name, kerne, ram) und
  gibt True zurück, wenn kerne höchstens so groß ist wie die freien
  Kerne und ram höchstens so groß wie der freie RAM des Hosts. Jeder
  Aufruf erhöht das Attribut gefragt um 1.

Zweitens ein Betriebsprotokoll: Für die Abrechnung und für
Störungsberichte soll jeder Aufruf bestimmter Funktionen mitgeschrieben
werden. Schreiben Sie dafür den Dekorator als Klasse `Protokolliert`:

- `__init__(self, funktion)` merkt sich die Funktion, übernimmt mit
  functools.update_wrapper ihren Namen und Docstring und legt die
  Attribute aufrufe (leere Liste) und fehler (0) an.
- `__call__(self, *args, **kwargs)` hängt zuerst das Paar (args, kwargs)
  an aufrufe an, ruft dann die Funktion auf und gibt ihr Ergebnis
  zurück. Löst die Funktion eine Ausnahme aus, erhöht es fehler um 1
  und lässt die Ausnahme weiterlaufen.

    regel = Platzierungsregel(kerne=8, ram=32)
    vms = [("web", 2, 8), ("db", 8, 64), ("cache", 4, 16)]
    list(filter(regel, vms))      →  [("web", 2, 8), ("cache", 4, 16)]
    regel.gefragt                 →  3

    @Protokolliert
    def starte_vm(name, ram=4):
        ...
    starte_vm("web", ram=8)
    starte_vm.aufrufe             →  [(("web",), {"ram": 8})]
    starte_vm.__name__            →  "starte_vm"

Grenzen: Kerne und RAM sind ganze Zahlen von 0 bis 10**6. Die
dekorierten Funktionen haben beliebige Parameter und dürfen jede
Ausnahme auslösen; jede dekorierte Funktion hat ihr eigenes Protokoll.

Hintergrund: Ein Objekt lässt sich wie eine Funktion aufrufen, wenn
seine Klasse die Methode __call__ hat: regel(vm) ist dann dasselbe wie
regel.__call__(vm), oder genauer type(regel).__call__(regel, vm).
callable(objekt) sagt, ob das geht. Der Vorteil gegenüber einer
einfachen Funktion: Das Objekt hat Attribute. Es kann seine
Einstellungen (hier die freien Kerne) und seinen Zustand (hier den
Zähler) offen tragen, man kann beides von außen lesen, und jede Instanz
hat ihren eigenen Zustand:

    class Zaehler:
        def __init__(self):
            self.stand = 0

        def __call__(self, schritt=1):
            self.stand += schritt
            return self.stand

    klick = Zaehler()
    klick(); klick(); klick(5)     →  7
    klick.stand                    →  7
    callable(klick)                →  True

Darum kann eine Klasse auch ein Dekorator sein (Dekoratoren in Aufgabe
4_022). @Protokolliert über def starte_vm bedeutet
starte_vm = Protokolliert(starte_vm): Der Name starte_vm zeigt danach
auf ein Protokolliert-Objekt, das die echte Funktion in einem Attribut
hält. Ein Aufruf starte_vm(...) landet in __call__, das vorher und
nachher etwas erledigen kann. Mit *args und **kwargs (Aufgabe 4_018)
nimmt __call__ beliebige Argumente an und reicht sie unverändert weiter.

Gegenüber einem Dekorator mit Closure und nonlocal (Aufgabe 4_024) ist
der Zustand hier ein gewöhnliches Attribut, und Methoden wie reset
lassen sich einfach ergänzen. functools.update_wrapper(self, funktion)
tut für das Objekt, was @functools.wraps für eine innere Funktion tut:
Es kopiert __name__, __doc__ und weitere Angaben der Funktion auf das
Objekt und setzt __wrapped__ auf die ursprüngliche Funktion. Eine
Grenze hat diese Form: Auf Methoden in einer Klasse angewendet, bekommt
__call__ kein self des Objekts mit, weil das Protokolliert-Objekt kein
Deskriptor ist (Aufgabe 5_001); dafür bräuchte es noch ein __get__.

Damit eine Ausnahme weiterläuft, fängt man sie, zählt und wirft sie mit
einem einfachen raise ohne Argument weiter:

    try:
        return funktion(*args, **kwargs)
    except Exception:
        ...
        raise
"""

import functools


class Platzierungsregel:
    """Prüft, ob eine VM auf einen Host mit freien Kernen und RAM passt; zählt die Anfragen."""

    def __init__(self, kerne, ram):
        self.kerne = kerne
        self.ram = ram
        self.gefragt = 0

    def __call__(self, vm):
        """Gibt True zurück, wenn die VM (name, kerne, ram) auf den Host passt."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Protokolliert:
    """Dekorator, der jeden Aufruf einer Funktion mitschreibt und Fehler zählt."""

    def __init__(self, funktion):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __call__(self, *args, **kwargs):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@Protokolliert
def starte_vm(name, ram=4):
    """Startet eine VM und meldet, mit wie viel RAM."""
    return f"{name} läuft mit {ram} GB"


regel = Platzierungsregel(kerne=8, ram=32)
vms = [("web", 2, 8), ("db", 8, 64), ("cache", 4, 16)]
print(list(filter(regel, vms)), regel.gefragt)
print(starte_vm("web", ram=8))
print(starte_vm.aufrufe, starte_vm.__name__)
