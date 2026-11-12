"""Aufgabe 4_030 – Prozessschritte                               Stufe 4 ★★★★☆

Ein Versandhändler will verstehen, wo seine Aufträge hängen bleiben. Die
Auftragsbearbeitung besteht aus Schritten wie „prüfen“, „freigeben“ und
„versenden“, und jeder Schritt ist eine Klasse mit einer Methode
`bearbeite`. Für die Prozessanalyse sollen zwei Dekoratoren dafür sorgen,
dass erstens alle Schritte an einer Stelle bekannt sind und zweitens jeder
Aufruf protokolliert wird, ohne dass jemand den Code der Schritte ändert.

Vervollständigen Sie:

- `prozessschritt(name)`, einen Dekorator mit Argument für Klassen. Er trägt
  die Klasse im Dictionary `SCHRITTE` unter name ein, setzt das
  Klassenattribut `schrittname` auf name und gibt die Klasse selbst zurück.
  Ist name schon vergeben, löst er einen ValueError aus und ändert nichts.
- `protokolliert(methode)`, einen Dekorator für Methoden. Die umhüllte
  Methode verhält sich wie die ursprüngliche und hängt nach jedem Aufruf
  das Tupel (Methodenname, Positionsargumente ohne self als Tupel,
  Schlüsselwortargumente als Dictionary, Ergebnis) an die Liste
  `protokoll` des Objekts an. Hat das Objekt noch keine solche Liste, legt
  sie sie an; jedes Objekt hat seine eigene. Löst die Methode eine
  Ausnahme aus, wird nichts eingetragen, und die Ausnahme geht weiter.
  Name und Docstring der Methode bleiben erhalten.

    @prozessschritt("pruefen")
    class Pruefung:
        def __init__(self, grenze):
            self.grenze = grenze

        @protokolliert
        def bearbeite(self, betrag):
            return betrag <= self.grenze

    schritt = Pruefung(1000)
    schritt.bearbeite(250)        →  True
    schritt.bearbeite(betrag=5000)  →  False
    schritt.protokoll  →  [("bearbeite", (250,), {}, True),
                           ("bearbeite", (), {"betrag": 5000}, False)]
    SCHRITTE["pruefen"] is Pruefung  →  True
    Pruefung.schrittname             →  "pruefen"

Grenzen: name ist ein nicht leerer Text. Die dekorierten Methoden haben
beliebig viele Positions- und Schlüsselwortargumente und können jede
Ausnahme auslösen. Ein Objekt wird bis zu 10 000-mal aufgerufen. Hat ein
Objekt schon ein Attribut protokoll, ist es eine Liste.

Hintergrund: Ein Dekorator ist eine Funktion, die ein Objekt bekommt und
ein Objekt zurückgibt (Aufgaben 4_022 und 4_023). Das @ funktioniert über
einer class genauso wie über einer def:

    @prozessschritt("pruefen")
    class Pruefung: ...

bedeutet Pruefung = prozessschritt("pruefen")(Pruefung). Ein
Klassendekorator bekommt also die fertige Klasse. Meist gibt er sie selbst
zurück, nachdem er sie irgendwo eingetragen oder ihr Attribute gegeben hat
(setattr oder klasse.attribut = …); das ist eine leichtere Alternative zu
einer Registry über Klassenattribute (Aufgabe 4_009). Gibt er nichts
zurück, steht unter dem Klassennamen hinterher None.

Ein Dekorator auf einer Methode bekommt die Funktion aus dem Klassenrumpf,
bevor die Klasse überhaupt existiert. Die Hülle, die er zurückgibt, wird
dann zur Methode; beim Aufruf schritt.bearbeite(250) bekommt sie wie jede
Methode zuerst das Objekt:

    def protokolliert(methode):
        @functools.wraps(methode)
        def huelle(self, *argumente, **benannte):
            ergebnis = methode(self, *argumente, **benannte)
            ...  # self.protokoll ergänzen
            return ergebnis
        return huelle

So kommt die Hülle an das Objekt heran und kann dessen Attribute lesen und
schreiben. functools.wraps überträgt __name__ und __doc__ der Methode auf
die Hülle. Ob ein Objekt ein Attribut schon hat, verrät hasattr(self,
"protokoll").
"""

import functools

SCHRITTE = {}


def prozessschritt(name):
    """Dekorator mit Argument: trägt eine Klasse unter name in SCHRITTE ein."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def protokolliert(methode):
    """Dekorator für Methoden: schreibt jeden erfolgreichen Aufruf in self.protokoll."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@prozessschritt("pruefen")
class Pruefung:
    """Prüft, ob ein Auftrag ohne Freigabe weiterlaufen darf."""

    def __init__(self, grenze):
        self.grenze = grenze

    @protokolliert
    def bearbeite(self, betrag):
        """Gibt True zurück, wenn betrag höchstens die Grenze ist."""
        return betrag <= self.grenze


@prozessschritt("versenden")
class Versand:
    """Wählt die Versandart eines Auftrags."""

    @protokolliert
    def bearbeite(self, auftrag, express=False):
        """Gibt die Versandart für den Auftrag zurück."""
        if auftrag == "":
            raise ValueError("Auftrag ohne Nummer")
        return "Express" if express else "Standard"


schritt = Pruefung(1000)
schritt.bearbeite(250)
schritt.bearbeite(betrag=5000)
print(schritt.protokoll)
print(SCHRITTE["pruefen"] is Pruefung, Pruefung.schrittname)
