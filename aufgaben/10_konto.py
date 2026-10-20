"""Aufgabe 10 – Girokonto                                        Stufe 4 ★★★★☆

Eine kleine Bank braucht ein Modell für Girokonten. Ein Konto gehört einer
Person und hat einen Kontostand in Euro. Man kann einzahlen und abheben, aber
nie mehr abheben, als auf dem Konto ist. Vervollständigen Sie die Klasse
`Konto`:

- `__init__(self, inhaber, stand=0)` speichert Inhaber und Anfangsstand als
  Attribute `inhaber` und `stand`.
- `einzahlen(self, betrag)` erhöht den Stand. Ein Betrag <= 0 löst einen
  ValueError aus.
- `abheben(self, betrag)` verringert den Stand. Ein Betrag <= 0 oder ein Betrag
  über dem Stand löst einen ValueError aus; der Stand bleibt dann unverändert.
- `__str__(self)` liefert z. B. "Konto von Anna: 120 Euro".

    konto = Konto("Anna", 100)
    konto.einzahlen(50)
    konto.abheben(30)
    print(konto)        →  Konto von Anna: 120 Euro
    konto.abheben(500)  →  ValueError

Hintergrund: Eine Klasse beschreibt einen Bauplan für Objekte, die Zustand
(Attribute) und Verhalten (Methoden) bündeln. `__init__` wird beim Erzeugen
aufgerufen und legt die Attribute auf `self` an; `self` ist das jeweilige
Objekt. Methoden bekommen `self` immer als ersten Parameter, beim Aufruf
`konto.abheben(30)` übergibt Python es automatisch.

Wichtig ist hier die Invariante „der Stand wird nie negativ“: Die Klasse
schützt ihren Zustand selbst, statt sich auf die Vorsicht der Aufrufer zu
verlassen. Dazu prüft jede Methode ihre Argumente und wirft bei einem Verstoß
eine Ausnahme, bevor sie etwas ändert:

    def abheben(self, betrag):
        if betrag > self.stand:
            raise ValueError("Nicht genug Guthaben")
        self.stand -= betrag

`raise` bricht die Methode ab; der Aufrufer kann die Ausnahme mit try/except
behandeln. Die Zeichenkette in der Ausnahme sollte sagen, was schiefging.

`__str__` ist eine der „Dunder“-Methoden (double underscore), über die Python
eingebaute Operationen an Ihre Klasse delegiert: print(konto) und str(konto)
rufen konto.__str__() auf. Andere Beispiele sind __len__ für len(), __eq__
für == und __add__ für +. Sie kommen in den nächsten Aufgaben.
"""


class Konto:
    """Ein Girokonto mit Inhaber und Kontostand, der nie negativ wird."""

    def __init__(self, inhaber, stand=0):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def einzahlen(self, betrag):
        """Erhöht den Kontostand um betrag; betrag muss positiv sein."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def abheben(self, betrag):
        """Verringert den Kontostand um betrag; nie unter 0."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __str__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


konto = Konto("Anna", 100)
konto.einzahlen(50)
konto.abheben(30)
print(konto)
