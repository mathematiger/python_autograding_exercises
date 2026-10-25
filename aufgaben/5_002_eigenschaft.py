"""Aufgabe 5_002 – property nachbauen                           Stufe 5 ★★★★★

Ein Überwachungssystem schlägt Alarm, wenn ein Messwert eines Servers, etwa
die CPU-Auslastung in Prozent, über einem Schwellwert liegt. Die Klasse
`Alarmregel` (unten vorgegeben) benutzt dafür berechnete und geprüfte
Attribute, wie man sie mit @property schreibt. Hier steht aber statt
property der Deskriptor `Eigenschaft`, und den bauen Sie selbst, damit klar
wird, was property eigentlich tut. Vervollständigen Sie `Eigenschaft`:

- `__init__(self, fget, fset=None)` speichert die Funktion zum Lesen und
  die zum Schreiben in den Attributen `fget` und `fset`.
- `__get__(self, objekt, typ=None)` gibt sich selbst zurück, wenn objekt
  None ist (Zugriff über die Klasse); sonst ruft es fget(objekt) auf und
  gibt das Ergebnis zurück.
- `__set__(self, objekt, wert)` ruft fset(objekt, wert) auf. Gibt es keine
  Funktion zum Schreiben, löst es einen AttributeError aus.
- `setter(self, fset)` gibt eine **neue** Eigenschaft mit demselben fget und
  dem neuen fset zurück. Die alte bleibt unverändert.

    regel = Alarmregel("CPU", 90)
    regel.schwellwert           →  90
    regel.schwellwert = 120     →  ValueError (nur 0 bis 100)
    regel.beschreibung          →  'Alarm, wenn CPU über 90 %'
    regel.beschreibung = "x"    →  AttributeError (nur lesbar)
    regel.pruefe(95)            →  True
    Alarmregel.schwellwert      →  das Eigenschaft-Objekt selbst

Hintergrund: In Aufgabe 5_001 haben Sie gesehen, dass Python bei
regel.schwellwert nachschaut, ob in der Klasse ein Deskriptor mit diesem
Namen steht, und dann dessen __get__ aufruft. property ist nichts anderes
als ein solcher Deskriptor, nur in C geschrieben. Er hält zwei Funktionen
fest und ruft sie zur richtigen Zeit auf. Entscheidend ist, wie der
Dekorator arbeitet. Die Schreibweise

    @Eigenschaft
    def beschreibung(self):
        ...

bedeutet genau dasselbe wie

    def beschreibung(self):
        ...
    beschreibung = Eigenschaft(beschreibung)

Die Funktion wird also zu fget, und im Klassenkörper steht unter dem Namen
beschreibung jetzt das Eigenschaft-Objekt. Beim Setter geht es weiter:

    @schwellwert.setter
    def schwellwert(self, wert):
        ...

heißt schwellwert = schwellwert.setter(funktion). Rechts steht noch die
alte Eigenschaft mit nur einem fget; setter liefert eine neue mit fget und
fset, und die ersetzt die alte unter demselben Namen. Deshalb müssen beide
Funktionen gleich heißen. Dass setter ein neues Objekt baut, statt das alte
zu verändern, macht Eigenschaften sicher wiederverwendbar: Eine Unterklasse
kann mit @Oberklasse.wert.setter einen anderen Setter bekommen, ohne den der
Oberklasse zu überschreiben. Das echte property macht es genauso und hat
zusätzlich deleter für del und übernimmt den Docstring von fget.

Wichtig ist noch: Weil Eigenschaft ein __set__ hat, ist sie ein
Daten-Deskriptor, auch wenn fset fehlt. Sie hat damit Vorrang vor dem
__dict__ der Instanz. Ohne __set__ würde regel.beschreibung = "x" einfach
einen Eintrag im __dict__ anlegen, der das berechnete Attribut ab dann
verdeckt. Darum löst man in __set__ einen AttributeError aus, statt __set__
wegzulassen.

Tipp: type(self)(...) erzeugt ein neues Objekt derselben Klasse wie self.
"""


class Eigenschaft:
    """Nachbau von property: ein Daten-Deskriptor mit Funktionen zum Lesen und Schreiben."""

    def __init__(self, fget, fset=None):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __get__(self, objekt, typ=None):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __set__(self, objekt, wert):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def setter(self, fset):
        """Gibt eine neue Eigenschaft mit demselben fget und dem neuen fset zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Alarmregel:
    """Alarm, sobald ein Messwert über dem Schwellwert in Prozent liegt."""

    def __init__(self, metrik, schwellwert):
        self.metrik = metrik
        self.schwellwert = schwellwert

    @Eigenschaft
    def schwellwert(self):
        """Der Schwellwert in Prozent."""
        return self._schwellwert

    @schwellwert.setter
    def schwellwert(self, wert):
        """Setzt den Schwellwert; nur 0 bis 100 Prozent sind erlaubt."""
        if not 0 <= wert <= 100:
            raise ValueError(f"Der Schwellwert muss zwischen 0 und 100 liegen, nicht {wert!r}.")
        self._schwellwert = wert

    @Eigenschaft
    def beschreibung(self):
        """Die Regel als Text."""
        return f"Alarm, wenn {self.metrik} über {self.schwellwert} %"

    def pruefe(self, messwert):
        """Gibt True zurück, wenn messwert einen Alarm auslöst."""
        return messwert > self.schwellwert


regel = Alarmregel("CPU", 90)
print(regel.beschreibung)
regel.schwellwert = 75
print(regel.beschreibung, regel.pruefe(80))
