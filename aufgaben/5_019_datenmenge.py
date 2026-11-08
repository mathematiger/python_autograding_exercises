"""Aufgabe 5_019 – Datenmengen                                   Stufe 5 ★★★★★

Ein Werkzeug zur Netzwerküberwachung liest von jedem Switch-Port, wie
viele Bytes übertragen wurden, und rechnet daraus Berichte. Damit
niemand Bytes mit Paketzahlen oder Bits durcheinanderbringt, steckt
jede Menge in einem Objekt der Klasse Datenmenge, und gerechnet wird
mit den gewohnten Operatoren. Dazu gehört ein veränderlicher
Portzaehler, der den Verkehr eines Ports über den Tag aufsummiert.
Vervollständigen Sie die Operatoren:

Datenmenge (unveränderlich, Attribut bytes; __init__, __eq__ und
__repr__ sind vorgegeben):

- `__add__`: Datenmenge + Datenmenge ergibt eine neue Datenmenge mit
  der Summe der Bytes. Bei jedem anderen Typ rechts: NotImplemented.
- `__radd__`: Steht links die ganze Zahl 0, ist das Ergebnis eine
  Datenmenge mit denselben Bytes, damit sum(liste) funktioniert. Bei
  allem anderen links: NotImplemented.
- `__mul__` und `__rmul__`: Datenmenge * int und int * Datenmenge
  ergeben das Vielfache (für Hochrechnungen). bool zählt nicht als
  int; sonst NotImplemented.

Portzaehler (veränderlich, Attribute port, gesamt und messungen):

- `__iadd__`: zaehler += datenmenge addiert die Menge zu gesamt,
  erhöht messungen um 1 und gibt dasselbe Objekt zurück. Bei jedem
  anderen Typ: NotImplemented.

    a = Datenmenge(1500)
    b = Datenmenge(500)
    a + b                     →  Datenmenge(2000)
    sum([a, b, a])            →  Datenmenge(3500)
    3 * b                     →  Datenmenge(1500)
    a + 5                     →  TypeError
    z = Portzaehler("Gi0/1")
    z += a
    z += b
    z.gesamt, z.messungen     →  Datenmenge(2000), 2

Grenzen: bytes ist eine ganze Zahl von 0 bis 10**18, Faktoren beim
Multiplizieren sind ganze Zahlen von 0 bis 10**6. Rechts oder links
können beliebige andere Objekte stehen (Zahlen, Texte, True, None,
Objekte fremder Klassen); dann muss die Methode NotImplemented
zurückgeben, nicht selbst einen Fehler auslösen.

Hintergrund: Bei a + b ruft Python zuerst a.__add__(b) auf. Kann a
mit b nichts anfangen, soll die Methode nicht raten und keinen Fehler
werfen, sondern den besonderen Wert NotImplemented zurückgeben. Dann
fragt Python das rechte Objekt: b.__radd__(a), das r steht für
„rechts“ (reflected). Erst wenn auch das NotImplemented liefert, löst
Python den TypeError aus:

    class Meter:
        def __init__(self, wert):
            self.wert = wert

        def __add__(self, other):
            if isinstance(other, Meter):
                return Meter(self.wert + other.wert)
            return NotImplemented          # nicht: raise TypeError

        def __radd__(self, other):
            if other == 0:                 # 0 + Meter(...) kommt von sum()
                return Meter(self.wert)
            return NotImplemented

    Meter(2) + Meter(3)                    # Meter.__add__
    sum([Meter(2), Meter(3)])              # beginnt mit 0 + Meter(2): __radd__
    Meter(2) + "x"                         # __add__ und str.__radd__? → TypeError

Warum nicht gleich raise TypeError? Weil dann eine fremde Klasse, die
sehr wohl weiß, wie man sich zu einem Meter addiert, nie gefragt
würde. NotImplemented ist eine Konstante, keine Ausnahme;
NotImplementedError ist etwas ganz anderes (für abstrakte Methoden).
sum(liste) fängt bei 0 an und rechnet 0 + liste[0] + liste[1] …, darum
braucht eine Klasse, die summiert werden soll, ein __radd__ für die 0;
sum(liste, start) nimmt einen anderen Startwert. Bei 3 * meter fragt
Python entsprechend erst int.__mul__, das NotImplemented liefert, dann
meter.__rmul__(3). Achtung: True ist in Python eine Unterklasse von int,
isinstance(True, int) ist True; wer bool ausschließen will, prüft das
eigens.

a += b ruft zuerst a.__iadd__(b) auf (i für in place, an Ort und
Stelle). Gibt es kein __iadd__ oder liefert es NotImplemented, rechnet
Python a = a + b. Der Unterschied zeigt sich bei einem zweiten Namen
für dasselbe Objekt: Bei einem unveränderlichen Objekt bindet += den
Namen a an ein neues Objekt, der zweite Name sieht weiter das alte.
Ein veränderliches Objekt ändert sich in __iadd__ selbst und muss sich
am Ende mit return self zurückgeben, denn Python weist das Ergebnis
wieder a zu. Ohne return stünde danach None in a. Genau so verhalten
sich Listen: liste += [1] verändert die Liste, zahl += 1 baut eine neue
Zahl.
"""


class Datenmenge:
    """Eine unveränderliche Menge übertragener Daten in Bytes."""

    def __init__(self, anzahl_bytes):
        self.bytes = anzahl_bytes

    def __eq__(self, other):
        """Zwei Datenmengen sind gleich, wenn sie gleich viele Bytes haben."""
        if not isinstance(other, Datenmenge):
            return NotImplemented
        return self.bytes == other.bytes

    def __repr__(self):
        return f"Datenmenge({self.bytes})"

    def __add__(self, other):
        """Datenmenge + Datenmenge."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __radd__(self, other):
        """0 + Datenmenge, damit sum() funktioniert."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __mul__(self, faktor):
        """Datenmenge * ganze Zahl."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __rmul__(self, faktor):
        """Ganze Zahl * Datenmenge."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Portzaehler:
    """Summiert den Verkehr eines Switch-Ports auf."""

    def __init__(self, port):
        self.port = port
        self.gesamt = Datenmenge(0)
        self.messungen = 0

    def __iadd__(self, other):
        """zaehler += Datenmenge: verändert den Zähler selbst."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


a = Datenmenge(1500)
b = Datenmenge(500)
print(a + b, sum([a, b, a]), 3 * b)
z = Portzaehler("Gi0/1")
z += a
z += b
print(z.gesamt, z.messungen)
