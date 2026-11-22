"""Aufgabe 3_043 – Messstellen                                   Stufe 3 ★★★☆☆

Das Monitoring einer Serverhalle überwacht die Auslastung der Rechner
in Prozent. Jede Messstelle sammelt ihre Messwerte und zählt Alarme:
Ein Wert über dem Grenzwert ist ein Alarm. Für alle Messstellen gilt
zunächst derselbe Grenzwert von 80 Prozent; ändert das Betriebsteam ihn,
soll er sofort für alle Messstellen gelten, die keinen eigenen haben.
Manche Rechner laufen absichtlich unter Volllast und bekommen deshalb
einen eigenen Grenzwert. Außerdem bekommt jede neue Messstelle eine
laufende Nummer, 1 für die erste, 2 für die zweite und so weiter.

Ein Kollege hat angefangen und dabei die Liste der Messwerte als
Klassenattribut angelegt. Seitdem landen die Werte jeder Messstelle bei
allen Messstellen. Vervollständigen Sie die Klasse `Messstelle`:

- Die Klassenattribute grenzwert = 80 und angelegt = 0 sind vorgegeben.
  Die falsche Zeile werte = [] im Klassenrumpf ist schon gelöscht.
- `__init__(self, name)` zählt Messstelle.angelegt um 1 hoch, setzt
  self.nummer auf den neuen Stand, merkt sich den Namen und legt für
  jede Messstelle eine eigene, leere Liste self.werte an.
- `messen(self, wert)` hängt den Wert an die eigene Liste an.
- `alarme(self)` gibt zurück, wie viele Werte echt über dem Grenzwert
  liegen, der für diese Messstelle gilt: ihr eigener, wenn sie einen
  hat, sonst der gemeinsame.
- `eigener_grenzwert(self, grenze)` gibt dieser einen Messstelle einen
  eigenen Grenzwert; der gemeinsame und die anderen Messstellen bleiben
  unverändert.

Dazu die Funktion `gemeinsamer_grenzwert(grenze)`, die den Grenzwert für
alle Messstellen ändert, die keinen eigenen haben.

    a = Messstelle("web-01")
    b = Messstelle("render-01")
    a.messen(85); a.messen(70); b.messen(95)
    a.nummer, b.nummer          →  (1, 2)
    a.werte, b.werte            →  ([85, 70], [95])
    b.eigener_grenzwert(98)
    a.alarme(), b.alarme()      →  (1, 0)
    gemeinsamer_grenzwert(90)
    a.alarme(), b.alarme()      →  (0, 0)

Grenzen: Es werden bis zu 10 000 Messstellen mit zusammen bis zu
100 000 Werten angelegt. Werte und Grenzwerte sind ganze Zahlen von 0
bis 100. Ein Wert genau auf dem Grenzwert ist kein Alarm. Die Tests
setzen vor jedem Durchgang Messstelle.angelegt = 0 und
Messstelle.grenzwert = 80.

Hintergrund: Klassen mit __init__ und Methoden kennen Sie aus Aufgabe
3_037. Ein Attribut, das im Klassenrumpf steht, gehört der Klasse und
ist für alle Objekte dasselbe (Klassenattribut). Ein Attribut, das man
über self.name = ... setzt, gehört nur diesem einen Objekt
(Instanzattribut). Beim Lesen von self.name sucht Python zuerst beim
Objekt und dann bei der Klasse:

    class Drucker:
        papier = "A4"           # Klassenattribut

    d1 = Drucker()
    d2 = Drucker()
    d1.papier = "A3"            # neues Instanzattribut nur bei d1
    d1.papier, d2.papier        →  ("A3", "A4")
    Drucker.papier = "Letter"
    d1.papier, d2.papier        →  ("A3", "Letter")

Vorsicht: self.zaehler += 1 liest den Wert zwar bei der Klasse, schreibt
das Ergebnis aber als neues Instanzattribut zurück; die Klasse zählt
dann nicht mit. Ein gemeinsamer Zähler wird darum über den Klassennamen
geändert: Klasse.zaehler += 1. Und eine Liste als Klassenattribut ist
eine einzige Liste für alle Objekte; append über ein Objekt verändert
sie für alle.
"""


class Messstelle:
    """Eine Messstelle mit eigener Messreihe; Grenzwert und Zähler gehören der Klasse."""

    grenzwert = 80
    angelegt = 0

    def __init__(self, name):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def messen(self, wert):
        """Hängt den Wert an die Messreihe dieser Messstelle an."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def alarme(self):
        """Gibt die Zahl der Werte über dem geltenden Grenzwert zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def eigener_grenzwert(self, grenze):
        """Gibt nur dieser Messstelle einen eigenen Grenzwert."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gemeinsamer_grenzwert(grenze):
    """Ändert den Grenzwert für alle Messstellen ohne eigenen Grenzwert."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


a = Messstelle("web-01")
b = Messstelle("render-01")
a.messen(85)
a.messen(70)
b.messen(95)
print(a.nummer, a.werte, b.nummer, b.werte)
b.eigener_grenzwert(98)
print("Alarme:", a.alarme(), b.alarme())
gemeinsamer_grenzwert(90)
print("Alarme:", a.alarme(), b.alarme())
