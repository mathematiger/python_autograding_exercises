"""Aufgabe 4_030 – Alarmregeln                                  Stufe 4 ★★★★☆

Ein Monitoring-System prüft Messwerte der Server gegen Alarmregeln. Jede
Regel ist eine Klasse mit einer Methode pruefe(wert), die True liefert,
wenn Alarm ausgelöst werden soll. Zwei Dinge sollen ohne Änderung an den
Regelklassen selbst dazukommen:

1. Alle Regelklassen sollen sich in einem zentralen Verzeichnis
   eintragen, damit die Konfigurationsoberfläche sie anbieten kann.
2. Jede Prüfung soll protokolliert werden, damit man später nachvollziehen
   kann, warum ein Alarm kam oder nicht.

Schreiben Sie dafür zwei Dekoratoren:

- `alarmregel(klasse)` ist ein Klassendekorator. Er trägt die Klasse unter
  ihrem Namen (klasse.__name__) in das Dictionary REGELN ein und gibt die
  Klasse unverändert zurück.
- `protokolliert(methode)` ist ein Dekorator für Methoden. Die umhüllte
  Methode ruft die ursprüngliche mit allen Argumenten auf und hängt danach
  ein Tupel (Name der Methode, Argumente als Tupel, Ergebnis) an die Liste
  self.protokoll des jeweiligen Objekts an. Hat das Objekt noch kein
  Attribut protokoll, wird es als leere Liste angelegt. Löst die Methode
  eine Ausnahme aus, wird nichts eingetragen und die Ausnahme geht weiter.
  Name und Docstring der Methode bleiben erhalten (functools.wraps).

    @alarmregel
    class Schwellwert:
        def __init__(self, grenze):
            self.grenze = grenze

        @protokolliert
        def pruefe(self, wert):
            return wert > self.grenze

    REGELN["Schwellwert"] is Schwellwert   →  True
    cpu = Schwellwert(90)
    cpu.pruefe(95)                         →  True
    cpu.pruefe(40)                         →  False
    cpu.protokoll       →  [("pruefe", (95,), True), ("pruefe", (40,), False)]

Grenzen: Methoden haben beliebig viele Positions- und Schlüsselwort-
argumente; im Protokoll stehen nur die Positionsargumente ohne self.
Beliebig viele Objekte derselben Klasse existieren nebeneinander, und jedes
hat sein eigenes Protokoll. Eine Klasse kann mehrere protokollierte
Methoden haben. Es werden bis zu 10 000 Aufrufe protokolliert.

Hintergrund: Ein Dekorator ist eine Funktion, die etwas bekommt und etwas
zurückgibt (Aufgaben 4_022 bis 4_024). @name über einer Definition ist nur
eine Kurzschreibweise: Python führt erst die Definition aus und bindet dann
den Namen an das Ergebnis des Dekorators.

    @alarmregel
    class Schwellwert: ...
    # ist dasselbe wie
    class Schwellwert: ...
    Schwellwert = alarmregel(Schwellwert)

Das funktioniert mit Klassen genauso wie mit Funktionen. Ein
Klassendekorator bekommt also das fertige Klassenobjekt und kann es
irgendwo eintragen, ihm Attribute hinzufügen oder es prüfen. Gibt er die
Klasse wieder zurück, bleibt sie benutzbar wie vorher; vergisst man das
return, heißt die Klasse danach None.

Ein Dekorator auf einer Methode sieht beim Dekorieren noch kein Objekt, nur
die Funktion in der Klasse. Erst beim Aufruf cpu.pruefe(95) kommt das Objekt
als erstes Argument an. Die Hülle nimmt es deshalb als ersten Parameter
entgegen und reicht es weiter:

    def zaehlt(methode):
        @functools.wraps(methode)
        def huelle(self, *args, **kwargs):
            self.aufrufe = getattr(self, "aufrufe", 0) + 1
            return methode(self, *args, **kwargs)
        return huelle

Weil die Hülle in der Klasse steht, wird sie beim Zugriff über ein Objekt
wie jede andere Methode gebunden: cpu.pruefe(95) ruft huelle(cpu, 95) auf.
Zustand, der zu einem Objekt gehört, speichert man darum auf self, nicht in
einer Variablen des Dekorators: Die gehörte allen Objekten gemeinsam.
getattr(objekt, name, standard) liefert den Standardwert, wenn es das
Attribut nicht gibt.
"""

import functools

REGELN = {}


def alarmregel(klasse):
    """Klassendekorator: trägt die Klasse unter ihrem Namen in REGELN ein."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def protokolliert(methode):
    """Methodendekorator: schreibt jeden erfolgreichen Aufruf in self.protokoll."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@alarmregel
class Schwellwert:
    """Alarm, wenn der Wert über der Grenze liegt."""

    def __init__(self, grenze):
        self.grenze = grenze

    @protokolliert
    def pruefe(self, wert):
        """True, wenn wert größer als die Grenze ist."""
        return wert > self.grenze


cpu = Schwellwert(90)
cpu.pruefe(95)
cpu.pruefe(40)
print(cpu.protokoll)
