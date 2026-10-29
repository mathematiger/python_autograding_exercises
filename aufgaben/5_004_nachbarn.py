"""Aufgabe 5_004 – Nächste Nachbarn mit __slots__                  Stufe 5 ★★★★★

Eine Fabrik will früh erkennen, wann ein Lüfter in einer Maschine
kaputtgeht. Zu jedem Lüfter misst ein Sensor die Vibration (x) und die
Temperatur (y). Aus früheren Messungen weiß man für viele Punkte (x, y),
ob der Lüfter "normal" lief oder kurz danach "defekt" war. Ein neuer
Messpunkt wird nach dem Verfahren der k nächsten Nachbarn eingeordnet:
Man sucht die k bekannten Punkte, die ihm am nächsten liegen, und nimmt
die Klasse, die unter ihnen die meisten Stimmen hat. Manche Punkte sind
besonders gut gesichert und zählen mehr; sie sind GewichteterPunkt-
Objekte mit einer eigenen Stimme.

Die Fabrik speichert Millionen solcher Punkte. Jedes gewöhnliche Python-
Objekt trägt ein eigenes Dictionary für seine Attribute mit sich, und das
kostet viel Speicher. Außerdem ist schon einmal ein Fehler passiert:
punkt.klase = "defekt" mit Tippfehler legte still ein neues Attribut an,
statt klasse zu ändern. Vervollständigen Sie:

- `Messpunkt` bekommt `__slots__` für x, y und klasse. Dann hat es kein
  `__dict__` mehr, und eine Zuweisung an ein anderes Attribut löst einen
  AttributeError aus.
- `GewichteterPunkt` bekommt `__slots__` nur für das neue Attribut
  gewicht; auch es hat dann kein `__dict__`.
- `klassifiziere(punkte, x, y, k)` gibt die Klasse zurück, die unter den
  k Punkten mit dem kleinsten Abstand zu (x, y) die größte Summe der
  Stimmen (Methode `stimme()`) hat. Bei gleichem Abstand gilt der Punkt
  als näher, der in punkte weiter vorn steht. Haben mehrere Klassen
  dieselbe Summe, gewinnt die, deren nächster Punkt unter den k am
  nächsten liegt.

    punkte = [Messpunkt(1, 1, "normal"), Messpunkt(2, 1, "normal"),
              Messpunkt(8, 9, "defekt"), GewichteterPunkt(3, 2, "defekt", 3)]
    klassifiziere(punkte, 2, 2, 1)   →  "normal"   (nur der Punkt (2, 1))
    klassifiziere(punkte, 2, 2, 3)   →  "defekt"   (2 Stimmen gegen 3)
    punkte[0].klase = "defekt"       →  AttributeError

Grenzen: x und y sind ganze Zahlen oder Kommazahlen mit -10**4 ≤ x, y ≤ 10**4,
klasse ein nicht leerer Text, gewicht eine Zahl größer als 0. punkte ist
eine Liste mit 1 bis 2000 Punkten, auch gemischt, 1 ≤ k ≤ len(punkte).

Hintergrund: Normalerweise speichert Python die Attribute eines Objekts
in einem Dictionary, das man als objekt.__dict__ ansehen kann. Das ist
bequem, denn man kann jederzeit neue Attribute anlegen, aber jedes Objekt
schleppt ein eigenes Dictionary mit sich herum. Mit __slots__ legt eine
Klasse stattdessen ein für alle Mal fest, welche Attribute ihre Objekte
haben dürfen:

    class Punkt:
        __slots__ = ("x", "y")

        def __init__(self, x, y):
            self.x = x
            self.y = y

    p = Punkt(1, 2)
    p.x = 5            # erlaubt
    p.z = 3            →  AttributeError: 'Punkt' object has no attribute 'z'
    p.__dict__         →  AttributeError

Python legt für jeden Namen in __slots__ in der Klasse einen Deskriptor
an (wie in Aufgabe 5_001), der den Wert an einer festen Stelle im Objekt
speichert, ähnlich wie in einem Tupel. Das Objekt braucht dann kein
Dictionary mehr und ist deutlich kleiner; bei Millionen Objekten spart
das viel Speicher, und der Zugriff wird etwas schneller. Der Preis: Man
kann keine Attribute mehr nachträglich ergänzen, und ein Klassenattribut
mit demselben Namen wie ein Slot (etwa gewicht = 1 als Standardwert)
ist verboten, weil dort schon der Deskriptor steht.

Bei der Vererbung muss jede Klasse mitmachen. Eine Unterklasse ohne
eigenes __slots__ bekommt wieder ein __dict__, und alle Vorteile sind
weg. Die Unterklasse nennt in ihrem __slots__ nur die neuen Attribute; die
geerbten Slots der Basisklasse gelten weiter, und sie noch einmal
aufzuführen, würde den Platz doppelt belegen:

    class Punkt3D(Punkt):
        __slots__ = ("z",)

Tipp: sorted(punkte, key=…) sortiert stabil: Punkte mit gleichem Abstand
bleiben in ihrer Reihenfolge. Ein Dictionary von Klasse zu Summe zählt die
Stimmen.
"""


class Messpunkt:
    """Ein bekannter Messpunkt (x, y) mit seiner Klasse."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __init__(self, x, y, klasse):
        """Speichert die Koordinaten und die Klasse."""
        self.x = x
        self.y = y
        self.klasse = klasse

    def abstand_quadrat(self, x, y):
        """Gibt das Quadrat des Abstands zum Punkt (x, y) zurück; zum Vergleichen genügt das."""
        return (self.x - x) ** 2 + (self.y - y) ** 2

    def stimme(self):
        """Ein gewöhnlicher Punkt hat eine Stimme."""
        return 1


class GewichteterPunkt(Messpunkt):
    """Ein Messpunkt, der mit dem Gewicht gewicht abstimmt."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __init__(self, x, y, klasse, gewicht):
        """Speichert zusätzlich das Gewicht."""
        super().__init__(x, y, klasse)
        self.gewicht = gewicht

    def stimme(self):
        """Ein gewichteter Punkt stimmt mit seinem Gewicht ab."""
        return self.gewicht


def klassifiziere(punkte, x, y, k):
    """Gibt die Klasse mit den meisten Stimmen unter den k nächsten Punkten zu (x, y) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


punkte = [
    Messpunkt(1, 1, "normal"),
    Messpunkt(2, 1, "normal"),
    Messpunkt(8, 9, "defekt"),
    GewichteterPunkt(3, 2, "defekt", 3),
]
print(klassifiziere(punkte, 2, 2, 1))
print(klassifiziere(punkte, 2, 2, 3))
