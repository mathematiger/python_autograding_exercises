"""Aufgabe 4_030 – Alarmregeln registrieren                      Stufe 4 ★★★★☆

Das Monitoring eines Rechenzentrums kennt verschiedene Arten von
Alarmregeln, jede als eigene Klasse mit einer Methode
`ausloesen(self, werte)`, die für eine Messreihe True liefert, wenn Alarm
ausgelöst werden soll. Die Konfiguration nennt die Regeln nur beim Namen
("Schwellwert", "Dauerlast" …), deshalb braucht das Monitoring ein
Verzeichnis REGELN vom Klassennamen auf die Klasse. Außerdem fallen Sensoren
manchmal aus und liefern dann None statt einer Zahl; diese Lücken soll
keine Regel selbst behandeln müssen. Vervollständigen Sie zwei Dekoratoren:

- `registriere(klasse)` ist ein Klassen-Dekorator. Er trägt die Klasse
  unter ihrem Namen (klasse.__name__) in REGELN ein und gibt sie unverändert
  zurück. Hat die Klasse keine aufrufbare Methode ausloesen, löst er einen
  TypeError aus. Ist der Name schon in REGELN, einen ValueError; die alte
  Klasse bleibt dann eingetragen.
- `ohne_ausfaelle(methode)` ist ein Dekorator für Methoden mit der Form
  methode(self, werte). Die verpackte Methode ruft das Original mit einer
  neuen Liste auf, in der alle None fehlen, und gibt dessen Ergebnis
  zurück. Die übergebene Liste bleibt unverändert. Name und Docstring der
  Methode bleiben erhalten (functools.wraps).

Die Klassen Schwellwert und Dauerlast sind vorgegeben und benutzen beide
Dekoratoren:

    REGELN["Schwellwert"] is Schwellwert           →  True
    Schwellwert(80).ausloesen([75, None, 82])      →  True
    Dauerlast(70, 3).ausloesen([71, None, 75, 90]) →  True  (die letzten 3 Messungen)
    Dauerlast(70, 3).ausloesen([71, 75, 60, None]) →  False
    Schwellwert.ausloesen.__name__                 →  "ausloesen"

Grenzen: werte ist eine Liste mit 0 bis 100 000 Elementen, jedes eine ganze
Zahl oder Kommazahl von -10**6 bis 10**6 oder None. Die Klassennamen sind
beliebige gültige Namen. ohne_ausfaelle wird nur auf Methoden mit genau den
Parametern self und werte angewendet.

Hintergrund: Ein Dekorator ist eine Funktion, die etwas bekommt und etwas
zurückgibt, das an seine Stelle tritt (Aufgabe 4_022). Das funktioniert
nicht nur mit Funktionen, sondern auch mit Klassen:

    @registriere
    class Schwellwert:
        ...

ist dasselbe wie class Schwellwert: ... und danach
Schwellwert = registriere(Schwellwert). Ein Klassen-Dekorator kann die
Klasse prüfen, irgendwo eintragen oder ihr Attribute hinzufügen. Er muss
die Klasse am Ende mit return zurückgeben; sonst heißt Schwellwert danach
None. Typische Anwendungen sind Verzeichnisse von Plugins oder Befehlen,
@dataclass (Aufgabe 4_012) und functools.total_ordering (Aufgabe 4_004).

    VERZEICHNIS = {}

    def merken(klasse):
        VERZEICHNIS[klasse.__name__] = klasse
        return klasse

Ein Dekorator auf einer Methode verpackt eine ganz normale Funktion, denn
im Klassenkörper ist def ausloesen(self, werte) nichts anderes. Der
einzige Unterschied: Die innere Funktion bekommt beim Aufruf
objekt.ausloesen(liste) als erstes Argument das Objekt, also self, und
muss es an das Original weiterreichen.

    def protokolliert(methode):
        @functools.wraps(methode)
        def verpackt(self, werte):
            print("Aufruf von", methode.__name__)
            return methode(self, werte)
        return verpackt

Vergisst man self in der inneren Funktion, landet das Objekt im Parameter
werte und die Liste bleibt übrig: TypeError. Will man den Dekorator für
beliebige Methoden schreiben, nimmt man def verpackt(self, *args,
**kwargs) (Aufgabe 4_018).
"""

import functools

REGELN = {}


def registriere(klasse):
    """Klassen-Dekorator: trägt klasse unter ihrem Namen in REGELN ein und gibt sie zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ohne_ausfaelle(methode):
    """Methoden-Dekorator: ruft methode(self, werte) mit einer Liste ohne None auf."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@registriere
class Schwellwert:
    """Alarm, sobald eine Messung über der Grenze liegt."""

    def __init__(self, grenze):
        self.grenze = grenze

    @ohne_ausfaelle
    def ausloesen(self, werte):
        """True, wenn ein Wert über der Grenze liegt."""
        return any(wert > self.grenze for wert in werte)


@registriere
class Dauerlast:
    """Alarm, wenn die letzten anzahl Messungen alle über der Grenze liegen."""

    def __init__(self, grenze, anzahl):
        self.grenze = grenze
        self.anzahl = anzahl

    @ohne_ausfaelle
    def ausloesen(self, werte):
        """True, wenn die letzten anzahl Werte alle über der Grenze liegen."""
        letzte = werte[-self.anzahl :]
        return len(letzte) == self.anzahl and all(wert > self.grenze for wert in letzte)


print(sorted(REGELN))
print(Dauerlast(70, 3).ausloesen([71, None, 75, 90]))
