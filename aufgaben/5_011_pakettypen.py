"""Aufgabe 5_011 – Pakettypen                                     Stufe 5 ★★★★★

Ein Werkzeug für die Projektplanung verwaltet Arbeitspakete. Jedes Projekt
hat seine eigenen Arten von Paketen: Ein Softwareprojekt kennt
"Entwicklung", "Test" und "Doku", ein Netzwerkumbau "Verkabelung" und
"Abnahme". Jede Art hat einen Stundensatz (Euro pro Stunde) und
Pflichtangaben, die beim Anlegen eines Pakets nicht fehlen dürfen, bei
"Test" etwa die Testumgebung. Die Arten stehen in der
Projektkonfiguration, die erst beim Start des Programms gelesen wird;
Klassen dafür kann man also nicht vorher in den Quelltext schreiben. (In
der Praxis genügt dafür oft eine einzige Klasse mit einem Attribut für die
Art; hier üben Sie, Klassen zur Laufzeit zu erzeugen.) Die gemeinsame
Oberklasse `Arbeitspaket` ist vorgegeben. Vervollständigen Sie zwei
Funktionen:

- `erzeuge_typ(name, stundensatz, pflichtangaben)` erzeugt mit type()
  eine neue Unterklasse von Arbeitspaket mit dem Klassennamen name und
  gibt sie zurück. Sie hat die Klassenattribute stundensatz und
  pflichtangaben (als Tupel, in der gegebenen Reihenfolge) und eine
  Methode `__repr__`, die für ein Paket der Klasse Test mit Titel
  "Lasttest" und 12 Stunden Test('Lasttest', 12) liefert. Ist name kein
  gültiger Bezeichner (name.isidentifier()) oder stundensatz negativ,
  löst die Funktion einen ValueError aus, dessen Meldung den falschen
  Wert enthält.
- `typen_aus(konfiguration)` bekommt eine Liste von Dictionaries mit den
  Schlüsseln "name", "stundensatz" und "pflicht" und gibt ein Dictionary
  zurück, das jedem Namen seine mit erzeuge_typ erzeugte Klasse zuordnet,
  in der Reihenfolge der Konfiguration. Kommt ein Name zweimal vor, löst
  die Funktion einen ValueError aus, dessen Meldung den Namen enthält.

    typen = typen_aus([
        {"name": "Entwicklung", "stundensatz": 95, "pflicht": ["modul"]},
        {"name": "Test", "stundensatz": 80, "pflicht": ["umgebung", "modul"]},
    ])
    Test = typen["Test"]
    paket = Test("Lasttest", 12, umgebung="staging", modul="login")
    paket.kosten()                      →  960   (Euro)
    paket                               →  Test('Lasttest', 12)
    Test.__name__, Test.pflichtangaben  →  ("Test", ("umgebung", "modul"))
    issubclass(Test, Arbeitspaket)      →  True
    Test("Lasttest", 12, modul="login") →  ValueError: Pflichtangabe umgebung fehlt

Grenzen: name ist ein Text mit 0 bis 50 Zeichen, stundensatz eine ganze
Zahl von -10**6 bis 10**6, pflichtangaben eine Liste von 0 bis 20
Bezeichnern ohne Wiederholung. konfiguration hat 0 bis 1000 Einträge.
Die übergebenen Listen bleiben unverändert, und eine spätere Änderung an
ihnen ändert die erzeugten Klassen nicht.

Hintergrund: Mit einem Argument kennen Sie type schon: type(3) ist int,
die Klasse eines Objekts. Klassen sind in Python selbst Objekte, und ihre
Klasse ist type: type(int) ist type. Das heißt, type ist die Klasse, aus
der Klassen gemacht werden, eine Metaklasse. Ruft man type mit drei
Argumenten auf, baut es eine neue Klasse, genau wie eine class-Anweisung:

    class Punkt(Basis):
        dimension = 2

        def laenge(self):
            return abs(self.x) + abs(self.y)

ist dasselbe wie

    def laenge(self):
        return abs(self.x) + abs(self.y)

    Punkt = type("Punkt", (Basis,), {"dimension": 2, "laenge": laenge})

Das erste Argument ist der Klassenname (er landet in Punkt.__name__ und
in Fehlermeldungen), das zweite das Tupel der Oberklassen (das Komma in
(Basis,) macht daraus ein Tupel), das dritte ein Dictionary mit allem,
was sonst im Klassenkörper stünde: Klassenattribute und Methoden. Eine
Methode ist dabei einfach eine Funktion, deren erster Parameter self
ist; Python macht sie beim Zugriff über ein Objekt zur gebundenen
Methode (Funktionen sind Deskriptoren, Aufgabe 5_002). Die
class-Anweisung tut intern nichts anderes: Sie führt den Klassenkörper
aus, sammelt die Namen in einem Dictionary und ruft dann type(name,
oberklassen, dictionary) auf.

Weil man type wie eine gewöhnliche Funktion aufruft, kann man Klassen
bauen, deren Name und Inhalt erst zur Laufzeit feststehen, etwa aus
einer Konfiguration. Eine Methode, die man dafür in einer Funktion
definiert, sieht deren lokale Variablen (Closure); einfacher ist es oft,
in der Methode type(self).__name__ oder self.stundensatz zu lesen, denn
das findet Python über die Klasse des Objekts. Jeder Aufruf von type
erzeugt eine neue, eigene Klasse, auch bei gleichem Namen. Vorsicht:
super() ohne Argumente funktioniert nur in Methoden, die in einem
Klassenkörper stehen. In einer außerhalb definierten Methode ruft man
die Oberklasse ausdrücklich auf, etwa Arbeitspaket.__init__(self, …).
"""


class Arbeitspaket:
    """Gemeinsame Oberklasse aller Arbeitspakete; Unterklassen setzen stundensatz und pflichtangaben."""

    stundensatz = 0
    pflichtangaben = ()

    def __init__(self, titel, stunden, **angaben):
        """Legt ein Paket an und prüft, dass alle Pflichtangaben der Klasse da sind."""
        for pflicht in self.pflichtangaben:
            if pflicht not in angaben:
                raise ValueError(f"Pflichtangabe {pflicht} fehlt")
        self.titel = titel
        self.stunden = stunden
        self.angaben = dict(angaben)

    def kosten(self):
        """Gibt die Kosten des Pakets zurück: Stunden mal Stundensatz der Klasse."""
        return self.stunden * self.stundensatz


def erzeuge_typ(name, stundensatz, pflichtangaben):
    """Erzeugt mit type() eine Unterklasse von Arbeitspaket und gibt sie zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def typen_aus(konfiguration):
    """Gibt zu jedem Namen der Konfiguration die erzeugte Klasse zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


typen = typen_aus([
    {"name": "Entwicklung", "stundensatz": 95, "pflicht": ["modul"]},
    {"name": "Test", "stundensatz": 80, "pflicht": ["umgebung", "modul"]},
])
Test = typen["Test"]
paket = Test("Lasttest", 12, umgebung="staging", modul="login")
print(paket.kosten(), paket)
print(Test.__name__, Test.pflichtangaben, issubclass(Test, Arbeitspaket))
