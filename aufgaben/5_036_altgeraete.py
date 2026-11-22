"""Aufgabe 5_036 – Altgeräte                                     Stufe 5 ★★★★★

Eine Firma tauscht ihre Laptops alle vier Jahre aus. Damit die alten
Geräte nicht im Müll landen, holt ein Wiederaufbereiter (Refurbisher)
sie ab, prüft sie, setzt sie instand und verkauft sie weiter; das spart
Rohstoffe und die Energie für die Herstellung neuer Geräte. Jeder
Standort meldet seine Altgeräte, und dasselbe Gerät kommt oft mehrmals
vor: einmal aus der Inventarliste, einmal vom Abholschein, später mit
dem Prüfergebnis. Ein Gerät ist durch Hersteller und Seriennummer
eindeutig bestimmt; sein Zustand ("ungeprüft", "gut", "Akku schwach" …)
ändert sich dagegen während der Aufbereitung. Schreiben Sie:

- `Geraetekennung`, eine Datenklasse mit frozen=True und den Feldern
  hersteller und seriennummer (beide Texte).
- `Altgeraet(hersteller, seriennummer, zustand)`, eine gewöhnliche
  Klasse. Die Eigenschaft kennung liefert die Geraetekennung des Geräts
  und lässt sich nicht neu setzen (AttributeError); zustand ist ein
  gewöhnliches Attribut, das man ändern darf. Zwei Altgeräte sind gleich,
  wenn ihre Kennungen gleich sind, egal welcher Zustand. Der Vergleich mit
  etwas, das kein Altgeraet ist, gibt NotImplemented zurück. Altgeräte
  sind hashbar, und ihr Hashwert ändert sich nicht, wenn sich der
  Zustand ändert.
- `bestand(meldungen)` gibt eine Menge mit je einem Altgeraet pro Gerät
  zurück; behalten wird jeweils die erste Meldung.
- `aktueller_zustand(meldungen)` gibt ein Dictionary Geraetekennung →
  Zustand der letzten Meldung dieses Geräts zurück, die Geräte in der
  Reihenfolge ihrer ersten Meldung.

    a = Altgeraet("Lenovo", "PF-1234", "ungeprüft")
    b = Altgeraet("Dell", "CN-0815", "Akku schwach")
    c = Altgeraet("Lenovo", "PF-1234", "Display defekt")
    a == c, hash(a) == hash(c)     →  (True, True)
    a.kennung                      →  Geraetekennung(hersteller='Lenovo', seriennummer='PF-1234')
    len(bestand([a, b, c]))        →  2
    aktueller_zustand([a, b, c])   →  {Geraetekennung('Lenovo', 'PF-1234'): 'Display defekt',
                                       Geraetekennung('Dell', 'CN-0815'): 'Akku schwach'}
    lager = {a}
    a.zustand = "gut"
    a in lager                     →  True

Grenzen: 0 bis 100 000 Meldungen; Hersteller, Seriennummer und Zustand
sind nicht leere Texte. bestand und aktueller_zustand sollen O(n)
Schritte brauchen.

Hintergrund: Wie __eq__ und __hash__ zusammen Objekte in Mengen und
als Schlüssel bringen, steht in Aufgabe 4_003; frozen=True kennen Sie
aus Aufgabe 4_014. Eine Menge legt jedes Objekt in einem Fach ab, das
sein Hashwert bestimmt, und sucht später nur in diesem Fach, dort mit
==. Daraus folgt der Vertrag, auf den sich jede Menge und jedes
Dictionary verlassen:

    Aus a == b folgt hash(a) == hash(b).
    Der Hashwert eines Objekts ändert sich nicht, solange es in einer
    Menge oder als Schlüssel in einem Dictionary steckt.

Wer den ersten Satz bricht, bekommt Doppelte in der Menge; wer den
zweiten bricht, verliert Objekte:

    @dataclass(unsafe_hash=True)        # Hash aus allen Feldern, obwohl veränderlich
    class Platz:
        raum: str
        belegt: bool

    p = Platz("A1", False)
    plaetze = {p}
    p.belegt = True                     # neuer Hashwert, aber p liegt im alten Fach
    p in plaetze                        →  False
    list(plaetze)[0] == p               →  True

Python schützt vor dem ersten Fehler so gut es geht: Eine Klasse, die
__eq__ definiert, aber kein __hash__, bekommt __hash__ = None und ist
unhashbar (TypeError). Genauso eine Datenklasse mit dem Standard
eq=True: Nur frozen=True (unveränderlich, also sicher) oder ausdrücklich
unsafe_hash=True geben ihr ein __hash__ aus allen Feldern, die verglichen
werden.

Der saubere Weg für veränderliche Dinge ist, Identität und Zustand zu
trennen: Gleichheit und Hash beruhen nur auf einem unveränderlichen
Schlüssel, alles andere darf sich ändern, ohne den Vertrag zu berühren.
Den Schlüssel schützt man vor Zuweisung, etwa mit einer property ohne
Setter (Aufgabe 4_005):

    class Konto:
        def __init__(self, iban, saldo):
            self._iban = iban
            self.saldo = saldo              # darf sich ändern
        @property
        def iban(self):
            return self._iban               # konto.iban = … gibt AttributeError
        def __eq__(self, other):
            if not isinstance(other, Konto):
                return NotImplemented
            return self.iban == other.iban
        def __hash__(self):
            return hash(self.iban)

NotImplemented sagt Python, dass dieser Vergleich nicht zuständig ist;
Python fragt dann die andere Seite und nimmt am Ende die Identität, so
dass konto == "DE12…" einfach False ergibt statt eines Fehlers. Ein
Hash aus einem Tupel der Schlüsselfelder oder aus einer frozen
Datenklasse ist bequem, denn deren __hash__ erfüllt den Vertrag schon.
"""

from dataclasses import dataclass

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Altgeraet:
    """Ein gemeldetes Altgerät; gleich ist, was dieselbe Kennung hat."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __repr__(self):
        """Zeigt Kennung und Zustand, damit Meldungen in Tests lesbar sind."""
        return f"Altgeraet({self.kennung.hersteller!r}, {self.kennung.seriennummer!r}, {self.zustand!r})"


def bestand(meldungen):
    """Gibt eine Menge mit je einem Altgerät pro Kennung zurück, jeweils der ersten Meldung."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def aktueller_zustand(meldungen):
    """Gibt ein Dictionary Kennung → Zustand der letzten Meldung zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


a = Altgeraet("Lenovo", "PF-1234", "ungeprüft")
b = Altgeraet("Dell", "CN-0815", "Akku schwach")
c = Altgeraet("Lenovo", "PF-1234", "Display defekt")
print(a == c, hash(a) == hash(c))
print(a.kennung)
print(len(bestand([a, b, c])))
print(aktueller_zustand([a, b, c]))
lager = {a}
a.zustand = "gut"
print(a in lager)
