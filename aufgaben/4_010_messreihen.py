"""Aufgabe 4_010 – Messreihen mit Mixins                           Stufe 4 ★★★★☆

Ein Monitoring-System sammelt Messwerte von Servern: die CPU-Last in
Prozent, die Temperatur im Gehäuse, den freien Arbeitsspeicher. Jede
Messreihe hat einen Namen, eine Einheit und eine Liste von Werten; das
erledigt die vorgegebene Klasse `Messreihe`. Manche Messreihen brauchen
zusätzlich eine Alarmschwelle, manche eine kleine Statistik, manche
beides. Statt für jede Kombination eine eigene Klasse mit kopiertem Code
zu schreiben, steckt jede Fähigkeit in einer eigenen kleinen Klasse, einem
Mixin, und eine Messreihe erbt genau die Mixins, die sie braucht.

Vervollständigen Sie:

- `SchwellwertMixin`: `ueberschreitungen()` gibt die Liste aller Werte
  zurück, die echt größer als `self.schwellwert` sind, in der Reihenfolge
  der Messung; genau die Schwelle ist noch kein Alarm. `beschreibung()`
  hängt an die Beschreibung der nächsten Klasse ", Schwelle <schwellwert>"
  an.
- `StatistikMixin`: `spitze()` gibt den größten Wert zurück, bei einer
  leeren Messreihe None. `beschreibung()` hängt ", <Anzahl> Werte" an.
- `CpuLast(name, schwellwert)`: eine Messreihe mit der Einheit "%", die
  beide Mixins erbt. `__init__` überlässt Name und Einheit mit super() der
  Basisklasse und speichert `schwellwert`.

Beide `beschreibung()` holen den Anfang der Beschreibung mit
super().beschreibung() und schreiben nie fest Messreihe davor.

    cpu = CpuLast("srv01", 90)
    for wert in [35, 92, 90, 97]:
        cpu.hinzufuegen(wert)
    cpu.ueberschreitungen()   →  [92, 97]
    cpu.spitze()              →  97
    cpu.beschreibung()        →  "srv01 (%), 4 Werte, Schwelle 90"

Grenzen: Messwerte und Schwelle sind ganze Zahlen oder Kommazahlen mit
-10**6 ≤ wert ≤ 10**6, auch negativ (die Mixins sollen für jede Messreihe
taugen, etwa für Temperaturen). Eine Messreihe hat 0 bis 100 000 Werte.
`name` ist ein nicht leerer Text.

Hintergrund: Eine Klasse darf mehrere Basisklassen haben:

    class CpuLast(SchwellwertMixin, StatistikMixin, Messreihe):
        ...

Sie erbt dann die Methoden aller drei. Ein Mixin ist eine Klasse, die
allein nichts taugt und nur eine Fähigkeit beisteuert; es hat meist kein
eigenes __init__ und verlässt sich auf Attribute, die andere Klassen
anlegen, hier self.werte und self.schwellwert. Welche Methode Python bei
cpu.beschreibung() nimmt, wenn mehrere Klassen eine haben, legt die Method
Resolution Order (MRO) fest, eine Reihenfolge aller Basisklassen, die man
mit CpuLast.__mro__ ansehen kann:

    CpuLast → SchwellwertMixin → StatistikMixin → Messreihe → object

Python sucht eine Methode der Reihe nach in diesen Klassen und nimmt die
erste, die es findet. Wichtig ist, was super() bedeutet: nicht „meine
Basisklasse“, sondern „die nächste Klasse in der MRO des Objekts“. Ruft
SchwellwertMixin.beschreibung super().beschreibung() auf, landet der Aufruf
bei einem CpuLast-Objekt in StatistikMixin, und dessen super() führt zu
Messreihe:

    class A:
        def name(self):
            return "A"

    class B(A):
        def name(self):
            return super().name() + "B"

    class C(A):
        def name(self):
            return super().name() + "C"

    class D(B, C):
        pass

    D().name()   →  "ACB"

Obwohl B nur von A erbt, ruft super() in B bei einem D-Objekt C auf, weil
C in der MRO von D nach B kommt. So arbeiten alle Klassen zusammen, und
jede Methode läuft genau einmal. Schreibt eine Klasse dagegen fest
A.name(self), überspringt sie alle Klassen dazwischen. Die Reihenfolge der
Basisklassen in der Klammer bestimmt die MRO: Mixins stehen links, die
eigentliche Basisklasse rechts.

Tipp: Bei class D(C, B) wäre das Ergebnis "ABC".
"""


class Messreihe:
    """Eine Reihe von Messwerten mit Name und Einheit."""

    def __init__(self, name, einheit):
        """Speichert Name und Einheit und legt eine leere Werteliste an."""
        self.name = name
        self.einheit = einheit
        self.werte = []

    def hinzufuegen(self, wert):
        """Hängt einen neuen Messwert an."""
        self.werte.append(wert)

    def beschreibung(self):
        """Liefert z. B. srv01 (%)."""
        return f"{self.name} ({self.einheit})"


class SchwellwertMixin:
    """Fähigkeit: Werte über self.schwellwert finden."""

    def ueberschreitungen(self):
        """Gibt alle Werte zurück, die echt größer als die Schwelle sind."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def beschreibung(self):
        """Hängt die Schwelle an die Beschreibung der nächsten Klasse an."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class StatistikMixin:
    """Fähigkeit: einfache Statistik über self.werte."""

    def spitze(self):
        """Gibt den größten Wert zurück, bei leerer Messreihe None."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def beschreibung(self):
        """Hängt die Anzahl der Werte an die Beschreibung der nächsten Klasse an."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class CpuLast(SchwellwertMixin, StatistikMixin, Messreihe):
    """CPU-Last in Prozent mit Alarmschwelle und Statistik."""

    def __init__(self, name, schwellwert):
        """Speichert Name und Schwelle; die Einheit ist immer %."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


cpu = CpuLast("srv01", 90)
for wert in [35, 92, 90, 97]:
    cpu.hinzufuegen(wert)
print(cpu.beschreibung())
print("Über der Schwelle:", cpu.ueberschreitungen())
print("Spitze:", cpu.spitze())
