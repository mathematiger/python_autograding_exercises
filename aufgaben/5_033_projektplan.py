"""Aufgabe 5_033 – Projektplan                                   Stufe 5 ★★★★★

Ein Planungswerkzeug für IT-Projekte zeigt ein Balkendiagramm aller
Arbeitspakete. Jedes Paket hat eine Dauer in Tagen und eine Liste von
Vorgängern, die fertig sein müssen, bevor es beginnen kann. Daraus
ergibt sich für jedes Paket der früheste Endzeitpunkt, und der größte
davon ist die Projektdauer. Die vorgegebene Funktion
`berechne_endzeitpunkte(pakete)` rechnet das aus. Bei Plänen mit
Tausenden Paketen dauert das, und die Oberfläche fragt bei jedem
Neuzeichnen mehrmals nach denselben Werten. Ergänzen Sie die Klasse
`Projektplan`:

- `endzeitpunkte` ist eine functools.cached_property: Beim ersten
  Zugriff ruft sie berechne_endzeitpunkte(self.pakete) auf, danach
  liefert sie das gespeicherte Ergebnis.
- `projektdauer` ist ebenfalls eine cached_property: der größte Wert
  aus endzeitpunkte, 0 bei einem leeren Plan. Sie benutzt endzeitpunkte
  und rechnet nicht selbst noch einmal.
- `hinzufuegen(name, dauer, vorgaenger)` trägt ein neues Paket ein und
  `dauer_aendern(name, dauer)` ändert die Dauer eines vorhandenen. Beide
  sorgen dafür, dass endzeitpunkte und projektdauer beim nächsten
  Zugriff neu berechnet werden, auch wenn sie bisher nie abgefragt
  wurden.

Der Konstruktor rechnet noch nichts aus. Jedes Objekt hat seinen
eigenen Zwischenspeicher.

    plan = Projektplan({"Analyse": (5, []), "Entwurf": (3, ["Analyse"])})
    plan.endzeitpunkte    →  {"Analyse": 5, "Entwurf": 8}   (rechnet)
    plan.projektdauer     →  8                              (rechnet nicht)
    plan.hinzufuegen("Test", 4, ["Entwurf"])
    plan.projektdauer     →  12                             (rechnet neu)
    plan.dauer_aendern("Analyse", 7)
    plan.endzeitpunkte["Test"]  →  14

Grenzen: Ein Plan hat 0 bis 2000 Pakete mit verschiedenen Namen;
dauer ist eine ganze Zahl von 0 bis 1000. Jedes Paket hat 0 bis 10
Vorgänger, und die stehen im Plan schon vor ihm (auch bei hinzufuegen),
darum gibt es keine Kreise. dauer_aendern bekommt nur Namen, die im
Plan stehen.

Hintergrund: Eine property (Aufgabe 5_002) rechnet bei jedem Zugriff
von vorn. Für teure Werte, die sich selten ändern, gibt es
functools.cached_property. Sie wird wie property über eine Methode
geschrieben, rechnet aber nur beim ersten Zugriff und legt das
Ergebnis im __dict__ des Objekts unter demselben Namen ab:

    from functools import cached_property

    class Bericht:
        def __init__(self, zeilen):
            self.zeilen = zeilen

        @cached_property
        def summe(self):
            print("rechne …")
            return sum(self.zeilen)

    b = Bericht([1, 2, 3])
    b.summe            # gibt "rechne …" aus, dann 6
    b.summe            # 6, ohne zu rechnen
    b.__dict__         # {'zeilen': [1, 2, 3], 'summe': 6}

Warum das funktioniert, wissen Sie aus Aufgabe 5_001: cached_property
ist ein Deskriptor, der nur __get__ hat, also kein Daten-Deskriptor.
Bei b.summe schaut Python darum zuerst ins __dict__ des Objekts. Steht
der Wert dort, wird __get__ gar nicht mehr gefragt; nur beim ersten Mal
fehlt er, dann rechnet __get__ und trägt ihn ein. Daraus folgt
dreierlei. Erstens hat jedes Objekt seinen eigenen Wert, weil jedes
sein eigenes __dict__ hat. Zweitens vergisst man den Wert, indem man
den Eintrag löscht: del b.summe (das löst einen AttributeError aus,
wenn noch nichts gespeichert ist) oder b.__dict__.pop("summe", None)
(das geht immer). Drittens braucht das Objekt ein __dict__; mit
__slots__ (Aufgabe 5_004) geht cached_property nicht.

Der Unterschied zu functools.lru_cache auf einer Methode (Aufgabe
4_025): lru_cache speichert in einem Cache, den alle Objekte der Klasse
teilen, braucht hashbare Argumente (auch self) und hält jedes Objekt,
das einmal darin steht, am Leben, bis der Cache es verdrängt.
cached_property speichert am Objekt selbst und verschwindet mit ihm.
Wer den Wert vergessen muss, wenn sich die Daten ändern, macht das an
genau den Stellen, die die Daten ändern, am besten über eine kleine
Hilfsmethode.
"""

from functools import cached_property


def berechne_endzeitpunkte(pakete):
    """Gibt für jedes Paket den frühesten Endzeitpunkt zurück (vorgegeben, bei großen Plänen teuer).

    Jedes Paket steht hinter seinen Vorgängern, darum sind deren Endzeitpunkte schon bekannt.
    """
    ende = {}
    for name, (dauer, vorgaenger) in pakete.items():
        ende[name] = dauer + max((ende[vor] for vor in vorgaenger), default=0)
    return ende


class Projektplan:
    """Ein Projektplan, der Endzeitpunkte und Projektdauer zwischenspeichert."""

    def __init__(self, pakete):
        """Übernimmt die Pakete als Dictionary name → (dauer, vorgaenger)."""
        self.pakete = dict(pakete)

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
    def endzeitpunkte(self):
        """Die frühesten Endzeitpunkte aller Pakete, beim ersten Zugriff berechnet."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
    def projektdauer(self):
        """Der späteste Endzeitpunkt, 0 bei einem leeren Plan."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def hinzufuegen(self, name, dauer, vorgaenger):
        """Trägt ein neues Paket ein; die gespeicherten Werte werden ungültig."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def dauer_aendern(self, name, dauer):
        """Ändert die Dauer eines Pakets; die gespeicherten Werte werden ungültig."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


plan = Projektplan({"Analyse": (5, []), "Entwurf": (3, ["Analyse"])})
print(plan.endzeitpunkte)
print(plan.projektdauer)
plan.hinzufuegen("Test", 4, ["Entwurf"])
print(plan.projektdauer)
plan.dauer_aendern("Analyse", 7)
print(plan.endzeitpunkte["Test"])
