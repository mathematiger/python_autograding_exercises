"""Aufgabe 5_014 – Sensorstapel                                 Stufe 5 ★★★★★

Ein IoT-Gateway sammelt Werte von Sensoren in einer Halle: Temperaturen
als Kommazahlen, Zählerstände als ganze Zahlen, Statusmeldungen als
Text. Fällt die Verbindung zur Zentrale aus, legt das Gateway die Werte
auf einem Stapel ab und schickt nach der Störung zuerst die neuesten,
denn die sind für die Steuerung am wichtigsten. Weil schon einmal ein
Text in einem Temperaturstapel gelandet ist und die Auswertung
durcheinanderbrachte, soll ein Stapel wie bei list[int] mit dem Typ
seiner Elemente angelegt werden und falsche Werte gleich beim Ablegen
ablehnen. Vervollständigen Sie die Klasse `Stapel`:

- `__class_getitem__(cls, typ)` gibt eine Unterklasse von cls zurück,
  deren Klassenattribut elementtyp gleich typ ist und deren
  `__name__` "Stapel[float]" lautet (Name von cls, dann der Name von
  typ in eckigen Klammern). Für dasselbe cls und denselben typ kommt
  immer dieselbe Klasse zurück. Ist typ keine Klasse (etwa ein Tupel
  wie bei Stapel[int, str] oder eine Zahl) oder ist cls schon
  parametrisiert (Stapel[int][str]), löst sie einen TypeError aus.
- `lege_ab(self, wert)` legt wert oben auf den Stapel. Ist wert keine
  Instanz von elementtyp (isinstance), löst die Methode einen TypeError
  aus, dessen Meldung den Wert und den erwarteten Typ nennt, und der
  Stapel bleibt unverändert.
- `nimm(self)` entfernt den obersten Wert und gibt ihn zurück; auf
  einem leeren Stapel löst sie einen IndexError aus.
- `__len__` gibt die Anzahl der Werte zurück, `__repr__` z. B.
  "Stapel[float]([21.5, 22.0])" mit den Werten von unten nach oben.

Ein Stapel ohne Typ, Stapel(), nimmt alles an (elementtyp ist object).

    temperaturen = Stapel[float]()
    temperaturen.lege_ab(21.5)
    temperaturen.lege_ab(22.0)
    temperaturen                         →  Stapel[float]([21.5, 22.0])
    temperaturen.lege_ab("defekt")       →  TypeError
    temperaturen.nimm()                  →  22.0
    Stapel[float] is Stapel[float]       →  True
    isinstance(temperaturen, Stapel)     →  True

Grenzen: typ kann eine beliebige Klasse sein, auch eine eigene, oder
ein anderer Wert. Werte sind beliebige Objekte; für isinstance gilt wie
immer, dass True eine Instanz von int ist und 3 keine von float. Ein
Stapel hat bis zu 100 000 Werte, lege_ab und nimm sollen O(1) Schritte
brauchen. Auch Unterklassen von Stapel lassen sich parametrisieren.

Hintergrund: Seit Python 3.9 kann man list[int] oder dict[str, float]
schreiben. Dahinter steckt die Methode __class_getitem__: Steht hinter
einer Klasse (nicht hinter einem Objekt) eine eckige Klammer, ruft
Python Klasse.__class_getitem__(inhalt) auf. Sie ist automatisch eine
Klassenmethode, ihr erster Parameter ist die Klasse. Bei mehreren
Angaben, Klasse[a, b], bekommt sie das Tupel (a, b).

    class Kiste:
        def __class_getitem__(cls, inhalt):
            return f"Kiste mit {inhalt.__name__}"

    print(Kiste[int])          # Kiste mit int

Was sie zurückgibt, ist ganz ihr überlassen. list[int] liefert ein
types.GenericAlias, das sich nur den Typ merkt: list[int]() ist eine
ganz normale Liste und nimmt auch Texte an. Typannotationen wie in
Aufgabe 4_016 und 4_017, auch eigene Klassen mit typing.Generic und
TypeVar, werden zur Laufzeit nie geprüft; das tun nur Werkzeuge wie
mypy. Will man die Prüfung beim Ausführen, gibt __class_getitem__ eine
echte Unterklasse zurück, die den Typ kennt. Eine Klasse zur Laufzeit
erzeugen Sie mit type(name, basen, namensraum) (Aufgabe 5_011):

    variante = type(f"{cls.__name__}[{typ.__name__}]", (cls,), {"elementtyp": typ})

Damit Stapel[float] is Stapel[float] gilt und nicht bei jedem Zugriff
eine neue Klasse entsteht, merkt man sich die erzeugten Klassen in
einem Dictionary mit dem Schlüssel (cls, typ). Ob etwas eine Klasse ist,
prüft isinstance(typ, type). Um eine schon parametrisierte Klasse zu
erkennen, legt man beim Erzeugen ein eigenes Kennzeichen in den
namensraum, etwa "_parametrisiert": True, und fragt in
__class_getitem__ danach.
"""


class Stapel:
    """Ein Stapel (zuletzt abgelegt, zuerst genommen), der den Typ seiner Elemente prüft."""

    elementtyp = object
    _parametrisiert = False
    _varianten = {}

    def __init__(self):
        self._werte = []

    def __class_getitem__(cls, typ):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def lege_ab(self, wert):
        """Legt wert oben auf den Stapel, wenn er den richtigen Typ hat."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def nimm(self):
        """Entfernt den obersten Wert und gibt ihn zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __repr__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


temperaturen = Stapel[float]()
temperaturen.lege_ab(21.5)
temperaturen.lege_ab(22.0)
print(temperaturen)
try:
    temperaturen.lege_ab("defekt")
except TypeError:
    print("abgelehnt")
print(temperaturen.nimm(), len(temperaturen))
