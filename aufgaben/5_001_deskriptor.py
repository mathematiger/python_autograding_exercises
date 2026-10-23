"""Aufgabe 5_001 – Deskriptoren                                  Stufe 5 ★★★★★

Ein Zeichenprogramm verwaltet Rechtecke. Breite und Höhe müssen immer positive
Zahlen sein, und zwar bei jeder Zuweisung, nicht nur im Konstruktor. Statt die
Prüfung in jedem Setter zu wiederholen, soll sie einmal in einem Deskriptor
`Positiv` stehen, der dann für beliebig viele Attribute in beliebig vielen
Klassen wiederverwendet wird. Vervollständigen Sie `Positiv`:

- `__set_name__(self, besitzer, name)` merkt sich den Attributnamen, unter dem
  der Deskriptor in der Klasse steht, z. B. "breite".
- `__set__(self, objekt, wert)` prüft, dass wert eine Zahl größer als 0 ist,
  und speichert ihn im `__dict__` des Objekts unter dem gemerkten Namen. Bei
  einem Verstoß: ValueError mit dem Attributnamen in der Meldung.
- `__get__(self, objekt, typ=None)` liefert den gespeicherten Wert. Wird der
  Deskriptor über die Klasse abgefragt (objekt ist None), gibt er sich selbst
  zurück.

    r = Rechteck(3, 4)
    r.flaeche()      →  12
    r.breite = 5
    r.flaeche()      →  20
    r.hoehe = -1     →  ValueError: hoehe muss positiv sein
    Rechteck.breite  →  das Positiv-Objekt selbst

Hintergrund: Attributzugriff ist in Python nicht fest verdrahtet. Wenn ein
Klassenattribut ein Objekt ist, das `__get__`, `__set__` oder `__delete__`
definiert, nennt man es einen Deskriptor, und Python ruft bei `r.breite`,
`r.breite = 5` und `del r.breite` diese Methoden auf, statt direkt ins
`__dict__` der Instanz zu greifen. Genau so sind `property`, `classmethod`,
`staticmethod` und sogar normale Methoden gebaut: Eine Funktion in einer Klasse
ist ein Deskriptor, dessen `__get__` die gebundene Methode (mit `self`)
zurückgibt.

Die Suchreihenfolge bei `r.breite`: Zuerst schaut Python, ob die Klasse (oder
eine Basisklasse) ein Attribut `breite` hat, das ein Daten-Deskriptor ist
(definiert `__set__` oder `__delete__`). Falls ja, gewinnt dessen `__get__`.
Sonst kommt `r.__dict__["breite"]` dran, dann Nicht-Daten-Deskriptoren und
einfache Klassenattribute. Deshalb darf ein Daten-Deskriptor den Wert ruhig
unter demselben Namen im Instanz-`__dict__` ablegen: Beim Lesen wird trotzdem
er gefragt, und er holt den Wert von dort.

Seit Python 3.6 bekommt ein Deskriptor über `__set_name__(besitzer, name)`
mitgeteilt, unter welchem Namen er in der Klasse steht. Vorher musste man den
Namen von Hand übergeben (`breite = Positiv("breite")`). Ein Skelett:

    class Positiv:
        def __set_name__(self, besitzer, name):
            self.name = name

        def __get__(self, objekt, typ=None):
            if objekt is None:
                return self
            return objekt.__dict__[self.name]

        def __set__(self, objekt, wert):
            ...  # prüfen, dann objekt.__dict__[self.name] = wert

Ein einziges Deskriptor-Objekt wird von allen Instanzen der Klasse geteilt;
darum darf der Wert nicht im Deskriptor selbst liegen, sondern muss im Objekt
gespeichert werden, das `__set__` als Argument bekommt.
"""


class Positiv:
    """Deskriptor für ein Attribut, das nur positive Zahlen annimmt."""

    def __set_name__(self, besitzer, name):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __get__(self, objekt, typ=None):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __set__(self, objekt, wert):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Rechteck:
    """Ein Rechteck mit positiver Breite und Höhe."""

    breite = Positiv()
    hoehe = Positiv()

    def __init__(self, breite, hoehe):
        self.breite = breite
        self.hoehe = hoehe

    def flaeche(self):
        """Flächeninhalt des Rechtecks."""
        return self.breite * self.hoehe


r = Rechteck(3, 4)
print(r.flaeche())
