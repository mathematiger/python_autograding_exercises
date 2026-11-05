"""Aufgabe 5_016 – Messquellen                                  Stufe 5 ★★★★★

Ein Monitoring-System überwacht die Server einer Firma. Seine Messwerte
kommen aus ganz verschiedenen Quellen: einer Klasse des Betriebsteams,
die die CPU-Last liest, einer Bibliothek eines Herstellers für die
Temperaturfühler im Serverschrank, einem kleinen Skript, das die
Antwortzeit einer Webseite misst. Die Klassen stammen von verschiedenen
Leuten und haben keine gemeinsame Basisklasse, und die Klasse des
Herstellers kann man nicht ändern. Gemeinsam ist ihnen nur, dass jede
ein Attribut name und eine Methode messe() ohne Argumente hat, die
eine Zahl liefert. Genau das soll als Schnittstelle festgehalten und
geprüft werden. Vervollständigen Sie:

- `Messquelle` als typing.Protocol mit dem Attribut name: str und der
  Methode messe(self) -> float, so ausgezeichnet, dass isinstance(obj,
  Messquelle) zur Laufzeit funktioniert.
- `abfragen(quellen)` bekommt eine Liste beliebiger Objekte. Für jedes
  Objekt, das eine Messquelle ist, ruft sie messe() auf. Sie gibt ein
  Tupel (werte, abgelehnt) zurück: werte ist ein Dictionary von name
  auf Messwert in der Reihenfolge der Liste, abgelehnt die Liste der
  Positionen (ab 0) der Objekte, die keine Messquelle sind.
- `Mittelwert(name, quellen)` ist selbst eine Messquelle, ohne von
  Messquelle zu erben: Sie fasst mehrere Quellen zusammen, etwa die
  vier Temperaturfühler eines Schranks. messe() gibt den Durchschnitt
  der Messwerte aller ihrer Quellen zurück. Ist quellen leer oder ist
  eines der Objekte keine Messquelle, löst schon der Konstruktor einen
  TypeError aus.

    class CpuLast:                       # erbt von nichts
        def __init__(self, name, werte): ...
        def messe(self): ...

    cpu = CpuLast("srv1-cpu", [42.0])
    isinstance(cpu, Messquelle)          →  True
    isinstance("srv1", Messquelle)       →  False
    abfragen([cpu, "srv1", Fuehler("rack-oben", 24.5)])
        →  ({"srv1-cpu": 42.0, "rack-oben": 24.5}, [1])
    Mittelwert("rack", [Fuehler("o", 24.5), Fuehler("u", 21.5)]).messe()  →  23.0

Grenzen: quellen hat 0 bis 10 000 Objekte beliebiger Art: Zahlen,
Texte, Objekte eigener Klassen mit nur einem der beiden Bestandteile
oder mit beiden, auch Klassen, die name erst im Konstruktor setzen oder
als property anbieten. Die Namen der Messquellen in einem Aufruf sind
verschieden. messe() liefert Zahlen von -10**6 bis 10**6. Ein
Mittelwert hat 1 bis 1000 Quellen, auch andere Mittelwerte; eine
leere Liste ist ungültig.

Hintergrund: Vererbung (Aufgabe 4_006) und abstrakte Basisklassen
(Aufgabe 4_011) verlangen, dass jede Klasse ausdrücklich von der
Schnittstelle erbt. Das nennt man nominale Typen: Entscheidend ist der
Name in der Klassenzeile. Python selbst denkt aber meist strukturell
(„Duck Typing“): Was eine Methode messe hat, kann man messen, egal, wie
die Klasse heißt. typing.Protocol beschreibt genau so eine Struktur:

    from typing import Protocol, runtime_checkable

    @runtime_checkable
    class Schaltbar(Protocol):
        name: str

        def schalte(self, an: bool) -> None: ...

    class Luefter:                       # erbt nicht von Schaltbar
        def __init__(self):
            self.name = "Lüfter 1"

        def schalte(self, an):
            print("an" if an else "aus")

    def alle_aus(geraete: list[Schaltbar]) -> None:
        for geraet in geraete:
            geraet.schalte(False)

    isinstance(Luefter(), Schaltbar)     # True

Eine Klasse erfüllt das Protokoll, wenn sie alle Attribute und Methoden
hat, die darin stehen; erben muss sie nicht. Werkzeuge wie mypy prüfen
das beim Lesen des Codes, auch die Typen der Argumente und Ergebnisse.
Zur Laufzeit dagegen ist ein Protokoll zunächst nur eine Beschreibung;
isinstance(obj, Schaltbar) löst einen TypeError aus. Erst
@runtime_checkable erlaubt isinstance, und dann prüft Python nur, ob das
Objekt jeden Namen aus dem Protokoll hat (wie mit hasattr), nicht deren
Typen oder Parameter. Ein Attribut mit Typannotation wie name: str gehört
ebenfalls zum Protokoll; der Rumpf einer Methode im Protokoll ist nur
... (Ellipsis), denn ausgeführt wird er nie. Eine Klasse wie Mittelwert
ist eine Messquelle, sobald sie name und messe hat; sie darf aber auch
ausdrücklich von einem Protokoll erben, das macht sie zur normalen
Unterklasse. Hier soll sie es nicht, damit Sie sehen, dass die Struktur
genügt. Den Durchschnitt berechnen Sie mit sum(...) / len(...).
"""

from typing import Protocol, runtime_checkable


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def abfragen(quellen):
    """Misst alle Messquellen; gibt (werte, Positionen der übrigen Objekte) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Mittelwert:
    """Eine Messquelle, die den Durchschnitt mehrerer Messquellen liefert."""

    def __init__(self, name, quellen):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def messe(self):
        """Gibt den Durchschnitt der Messwerte aller Quellen zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class CpuLast:
    """Liest die CPU-Last eines Servers; hier liefert sie der Reihe nach vorgegebene Werte."""

    def __init__(self, name, werte):
        self.name = name
        self._werte = list(werte)
        self._naechster = 0

    def messe(self):
        """Gibt den nächsten Wert zurück, nach dem letzten wieder den ersten."""
        wert = self._werte[self._naechster % len(self._werte)]
        self._naechster = self._naechster + 1
        return wert


class Fuehler:
    """Ein Temperaturfühler aus der Bibliothek des Herstellers, der immer dieselbe Temperatur meldet."""

    def __init__(self, name, temperatur):
        self.name = name
        self.temperatur = temperatur

    def messe(self):
        """Gibt die Temperatur in Grad Celsius zurück."""
        return self.temperatur


cpu = CpuLast("srv1-cpu", [42.0])
print(isinstance(cpu, Messquelle), isinstance("srv1", Messquelle))
print(abfragen([cpu, "srv1", Fuehler("rack-oben", 24.5)]))
print(Mittelwert("rack", [Fuehler("o", 24.5), Fuehler("u", 21.5)]).messe())
