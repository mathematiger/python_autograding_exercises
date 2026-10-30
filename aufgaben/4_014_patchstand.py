"""Aufgabe 4_014 – Patchstand                                      Stufe 4 ★★★★☆

Im Rechenzentrum laufen Hunderte Server, und auf jedem ist eine Version
des Betriebssystems installiert. Versionsnummern haben die Form
major.minor.patch, etwa 2.10.1: Die erste Zahl ändert sich bei großen
Umbauten, die zweite bei neuen Funktionen, die dritte bei
Fehlerkorrekturen (Patches). Nach einer Sicherheitswarnung will das
Betriebsteam wissen, welche Server noch unter einer Mindestversion
liegen und dringend ein Update brauchen.

Als Text verglichen wäre "2.9.0" größer als "2.10.1", weil das Zeichen
9 nach 1 kommt. Darum soll eine Datenklasse `Version` die drei Zahlen
speichern und richtig vergleichen. Vervollständigen Sie:

- `Version` mit den Feldern `major`, `minor` und `patch` (Standardwert
  0), in dieser Reihenfolge. Der Dekorator kommt an die Stelle der
  pass-Zeile direkt über class Version. Versionen sind unveränderlich
  (frozen), lassen sich mit <, <=, > und >= vergleichen und sortieren
  (order), und
  `__post_init__` löst einen ValueError aus, wenn eines der Felder keine
  ganze Zahl oder negativ ist. True und False zählen dabei nicht als
  ganze Zahl. `__str__` steht schon im Code.
- `veraltet(server, mindest)`: server ist ein Dictionary von Servername
  zu Version. Die Funktion gibt die Namen aller Server zurück, deren
  Version kleiner als mindest ist, alphabetisch sortiert.

    v = Version(2, 10, 1)
    str(v)                           →  "2.10.1"
    Version(2, 9) < Version(2, 10)   →  True
    Version(2, 1) == Version(2, 1, 0)   →  True
    v.patch = 2                      →  dataclasses.FrozenInstanceError
    Version(1, -1)                   →  ValueError
    server = {"web01": Version(2, 9, 3), "db01": Version(2, 10, 1), "mail": Version(1, 4, 0)}
    veraltet(server, Version(2, 10))      →  ["mail", "web01"]

Grenzen: Die Argumente von Version können ganze Zahlen von -10**6 bis
10**6, Kommazahlen, Texte, True oder False sein; gültig sind nur ganze
Zahlen ab 0. server hat 0 bis 100 000 Einträge, die Namen sind
verschiedene, nicht leere Texte.

Hintergrund: Der Dekorator @dataclass aus Aufgabe 4_012 nimmt Argumente,
die weitere Methoden erzeugen:

    from dataclasses import dataclass

    @dataclass(frozen=True, order=True)
    class Punkt:
        x: int
        y: int = 0

order=True erzeugt __lt__, __le__, __gt__ und __ge__. Verglichen wird
wie bei Tupeln: zuerst das erste Feld, nur bei Gleichheit das zweite und
so weiter. Punkt(1, 9) < Punkt(2, 0) ist also True. Darum bestimmt die
Reihenfolge der Felder, wonach sortiert wird. sorted, min und max
funktionieren damit ohne key.

frozen=True macht die Objekte unveränderlich: Jede Zuweisung an ein Feld,
auch p.x = 5 nach dem Erzeugen, löst dataclasses.FrozenInstanceError aus
(eine Unterklasse von AttributeError). Dafür bekommt die Klasse ein
__hash__, das aus den Feldern berechnet wird; unveränderliche Objekte
kann man darum in Mengen stecken und als Schlüssel in Dictionaries
verwenden (Aufgabe 4_003). Bei veränderlichen Objekten wäre das
gefährlich, weil sich der Hashwert nach dem Einfügen ändern könnte.

Weil @dataclass das __init__ selbst schreibt, kann man dort keine Prüfung
einbauen. Dafür gibt es __post_init__: Das erzeugte __init__ ruft es auf,
nachdem alle Felder gesetzt sind:

    @dataclass(frozen=True)
    class Temperatur:
        grad: float

        def __post_init__(self):
            if self.grad < -273.15:
                raise ValueError("kälter als der absolute Nullpunkt")

Lesen geht in __post_init__ wie überall mit self.grad. Schreiben dagegen
verhindert frozen auch hier; wer einen Wert nachträglich umrechnen will,
muss object.__setattr__(self, "grad", wert) benutzen.

Tipp: type(wert) is int ist bei True und False falsch, isinstance(True,
int) dagegen wahr, weil bool eine Unterklasse von int ist.
"""

from dataclasses import dataclass


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
class Version:
    """Eine Versionsnummer major.minor.patch, unveränderlich und richtig vergleichbar."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __str__(self):
        """Gibt die Version in der Form major.minor.patch zurück."""
        return f"{self.major}.{self.minor}.{self.patch}"


def veraltet(server, mindest):
    """Gibt die Namen der Server mit einer Version unter mindest alphabetisch sortiert zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


server = {"web01": Version(2, 9, 3), "db01": Version(2, 10, 1), "mail": Version(1, 4, 0)}
print(veraltet(server, Version(2, 10)))
print(", ".join(str(version) for version in sorted(server.values())))
