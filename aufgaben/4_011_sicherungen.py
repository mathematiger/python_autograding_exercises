"""Aufgabe 4_011 – Sicherungen planen                             Stufe 4 ★★★★☆

Ein Rechenzentrum sichert die Daten seiner Server jede Nacht auf ein
Speichersystem und bewahrt die Sicherungen eine Zeit lang auf. Wie viel
Platz das braucht, hängt von der Art der Sicherung ab:

- Bei der Vollsicherung wird jede Nacht eine vollständige Kopie angelegt.
  Wer 7 Tage aufbewahrt, braucht siebenmal die Datenmenge.
- Bei der inkrementellen Sicherung gibt es eine einzige Vollsicherung am
  ersten Tag; an jedem weiteren Tag werden nur die Änderungen seit dem
  Vortag gesichert. Bei 7 Tagen sind das eine volle Kopie und 6
  Änderungen.

Im Planungsprogramm ist jede Sicherung ein Objekt einer Unterklasse von
`Sicherung`. Jede Unterklasse muss eine Methode `speicherbedarf(tage)`
haben, sonst kann `bericht` nicht arbeiten. Damit niemand eine Unterklasse
vergisst oder aus Versehen eine allgemeine `Sicherung` anlegt, soll Python
das selbst verhindern. Vervollständigen Sie:

- In `Sicherung` die abstrakte Methode `speicherbedarf(self, tage)`.
  `Sicherung` erbt schon von `ABC`.
- `Vollsicherung.speicherbedarf(tage)`: Datenmenge mal Tage.
- `InkrementelleSicherung.speicherbedarf(tage)`: eine volle Datenmenge
  plus eine Änderung für jeden weiteren Tag.
- `gesamtbedarf(sicherungen, tage)`: die Summe des Speicherbedarfs aller
  Sicherungen der Liste, bei einer leeren Liste 0.

    web = Vollsicherung("web01", 40)
    db = InkrementelleSicherung("db01", 500, 20)
    web.speicherbedarf(7)          →  280
    db.speicherbedarf(7)           →  620
    db.bericht(7)                  →  "db01: 620 GB für 7 Tage"
    gesamtbedarf([web, db], 7)     →  900
    Sicherung("alt", 10)           →  TypeError

Grenzen: system ist ein nicht leerer Text, daten_gb und aenderung_gb sind
ganze Zahlen von 0 bis 10**6, tage eine ganze Zahl von 1 bis 3650. Eine
Liste enthält 0 bis 100 000 Sicherungen, auch gemischt.

Hintergrund: Manche Klassen sind nur als gemeinsamer Rahmen für ihre
Unterklassen gedacht. Von ihnen selbst soll es keine Objekte geben, weil
ihnen etwas Wesentliches fehlt. So eine Klasse heißt abstrakt. Python
bietet dafür das Modul abc (abstract base classes): Eine Klasse, die von
ABC erbt, kann Methoden mit dem Dekorator @abstractmethod markieren. Die
Methode bekommt meist nur einen Docstring als Rumpf, denn sie legt nur
fest, dass es sie geben muss und was sie tun soll:

    from abc import ABC, abstractmethod

    class Form(ABC):
        @abstractmethod
        def flaeche(self):
            '''Gibt den Flächeninhalt zurück.'''

        def beschreibung(self):
            return f"Fläche {self.flaeche()}"

    class Quadrat(Form):
        def __init__(self, seite):
            self.seite = seite

        def flaeche(self):
            return self.seite ** 2

    Quadrat(3).beschreibung()   →  "Fläche 9"
    Form()                      →  TypeError: Can't instantiate abstract class Form …

Python lässt ein Objekt nur dann entstehen, wenn die Klasse jede abstrakte
Methode überschreibt. Vergisst eine Unterklasse flaeche, schlägt schon
das Anlegen des Objekts fehl, nicht erst viel später der Aufruf. Die
anderen Methoden der abstrakten Klasse, hier beschreibung, dürfen die
abstrakte Methode trotzdem schon benutzen: Bei einem Quadrat-Objekt ruft
self.flaeche() die Methode von Quadrat auf. Die abstrakte Klasse ist
damit ein Vertrag, den jede Unterklasse erfüllen muss.
"""

from abc import ABC, abstractmethod


class Sicherung(ABC):
    """Gemeinsamer Rahmen für alle Arten von Sicherungen eines Systems mit daten_gb Gigabyte Daten."""

    def __init__(self, system, daten_gb):
        """Speichert den Namen des Systems und die Datenmenge in GB."""
        self.system = system
        self.daten_gb = daten_gb

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def bericht(self, tage):
        """Liefert z. B. "web01: 280 GB für 7 Tage"."""
        return f"{self.system}: {self.speicherbedarf(tage)} GB für {tage} Tage"


class Vollsicherung(Sicherung):
    """Jeden Tag eine vollständige Kopie."""

    def speicherbedarf(self, tage):
        """Datenmenge mal Anzahl der Tage."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class InkrementelleSicherung(Sicherung):
    """Am ersten Tag eine vollständige Kopie, danach jeden Tag nur die Änderungen von aenderung_gb GB."""

    def __init__(self, system, daten_gb, aenderung_gb):
        """Speichert zusätzlich die tägliche Änderung in GB."""
        super().__init__(system, daten_gb)
        self.aenderung_gb = aenderung_gb

    def speicherbedarf(self, tage):
        """Eine volle Datenmenge plus eine Änderung für jeden weiteren Tag."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gesamtbedarf(sicherungen, tage):
    """Gibt den Speicherbedarf aller Sicherungen der Liste für tage Tage zusammen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


web = Vollsicherung("web01", 40)
db = InkrementelleSicherung("db01", 500, 20)
print(web.bericht(7))
print(db.bericht(7))
print("Zusammen:", gesamtbedarf([web, db], 7), "GB")
