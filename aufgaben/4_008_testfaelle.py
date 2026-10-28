"""Aufgabe 4_008 – Testfälle                                     Stufe 4 ★★★★☆

Ein Entwicklungsteam testet seine Funktionen nach dem Blackbox-Verfahren:
Man kennt nur die Beschreibung einer Funktion, nicht ihren Code, und
überlegt sich dazu Eingaben mit dem erwarteten Ergebnis. Besonders
ergiebig sind die Grenzwerte, also die Eingaben direkt an einer Grenze aus
der Beschreibung. Jeder Testfall bekommt eine fortlaufende Nummer
TF001, TF002, …, damit man im Testbericht und im Fehlerticket eindeutig
auf ihn verweisen kann. Außerdem soll jeder Testfall, sobald er angelegt
ist, automatisch in einem gemeinsamen Verzeichnis stehen, damit man alle
auf einmal ausführen kann und keiner vergessen wird.

Vervollständigen Sie die Klasse `Testfall`. Sie hat zwei Klassenattribute:
`anzahl` zählt, wie viele Testfälle bisher angelegt wurden, und `alle` ist
ein Dictionary von der Nummer zum Testfall.

- `__init__(self, eingabe, erwartet)` speichert die Attribute `eingabe` und
  `erwartet`, zählt `anzahl` um eins hoch, vergibt daraus die Nummer als
  Attribut `nummer` (dreistellig mit führenden Nullen) und trägt den
  Testfall unter seiner Nummer in `alle` ein.
- Die Klassenmethode `finde(cls, nummer)` gibt den Testfall mit dieser
  Nummer zurück, oder None, wenn es ihn nicht gibt.
- Die Klassenmethode `fehlgeschlagen(cls, funktion)` ruft funktion für
  jeden Testfall in `alle` mit dessen Eingabe auf und gibt die Liste der
  Nummern zurück, bei denen nicht das erwartete Ergebnis herauskommt, in
  der Reihenfolge, in der die Testfälle angelegt wurden.
- Die Klassenmethode `zuruecksetzen(cls)` setzt `anzahl` auf 0 und leert
  `alle`, damit die nächste Testreihe wieder bei TF001 beginnt.

    Testfall.zuruecksetzen()
    a = Testfall(0, 4.9)
    b = Testfall(2000, 4.9)
    a.nummer, b.nummer             →  "TF001", "TF002"
    Testfall.anzahl                →  2
    Testfall.finde("TF002") is b   →  True
    Testfall.finde("TF099")        →  None
    Testfall.fehlgeschlagen(versandkosten)  →  Nummern der Testfälle,
                                               die versandkosten nicht besteht

Grenzen: Eine Testreihe hat höchstens 999 Testfälle, die Nummern reichen also
von TF001 bis TF999. `eingabe` und `erwartet` sind beliebige Werte, die sich
mit == vergleichen lassen. `funktion` gibt für jede Eingabe einen Wert zurück,
ohne eine Ausnahme auszulösen. `nummer` in finde ist ein beliebiger Text.

Hintergrund: Ein Attribut, das direkt im Klassenkörper steht, gehört der
Klasse selbst und nicht einem einzelnen Objekt. Alle Objekte teilen es.
Damit kann eine Klasse etwas über alle ihre Objekte wissen, zum Beispiel
wie viele es gibt (ein Zähler) oder welche es gibt (eine Registry, ein
Verzeichnis aller Objekte):

    class Sensor:
        anzahl = 0
        verzeichnis = []

        def __init__(self, name):
            Sensor.anzahl += 1
            self.name = name
            Sensor.verzeichnis.append(self)

    Sensor("Halle 1")
    Sensor("Halle 2")
    Sensor.anzahl          # 2
    Sensor.verzeichnis[1].name  # "Halle 2"

Lesen kann man ein Klassenattribut auch über ein Objekt: self.anzahl
findet nichts im Objekt und schaut dann in der Klasse nach. Beim Zuweisen
gilt das nicht. self.anzahl += 1 liest den Wert der Klasse, schreibt das
Ergebnis aber als neues Attribut in das Objekt; der Zähler der Klasse
bleibt stehen, und jedes Objekt hat danach seine eigene 1. Wer einen
Klassenzähler hochzählt, schreibt deshalb Sensor.anzahl += 1 oder in einer
Klassenmethode cls.anzahl += 1. Anders bei der Liste:
self.verzeichnis.append(...) weist nichts zu, sondern verändert die gemeinsame Liste der
Klasse, das klappt also auch über self. In Klassenmethoden (Aufgabe 4_006)
erreicht man die Klassenattribute über cls.

Tipp: f"TF{zahl:03d}" schreibt eine Zahl dreistellig mit führenden
Nullen. Ein Dictionary behält die Reihenfolge, in der die Einträge
hinzugefügt wurden.
"""


class Testfall:
    """Ein Blackbox-Testfall mit Eingabe, erwartetem Ergebnis und fortlaufender Nummer."""

    anzahl = 0
    alle = {}

    def __init__(self, eingabe, erwartet):
        """Speichert den Testfall, vergibt die nächste Nummer und trägt ihn in alle ein."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    @classmethod
    def finde(cls, nummer):
        """Gibt den Testfall mit dieser Nummer zurück, sonst None."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    @classmethod
    def fehlgeschlagen(cls, funktion):
        """Gibt die Nummern aller Testfälle zurück, bei denen funktion falsch rechnet."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    @classmethod
    def zuruecksetzen(cls):
        """Beginnt eine neue Testreihe ohne Testfälle."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __repr__(self):
        """Liefert z. B. Testfall('TF001', 0 → 4.9)."""
        return f"Testfall({self.nummer!r}, {self.eingabe!r} → {self.erwartet!r})"


def versandkosten(gramm):
    """Laut Beschreibung: bis einschließlich 2000 g 4.90 Euro, darüber 6.90 Euro."""
    if gramm < 2000:
        return 4.9
    return 6.9


Testfall.zuruecksetzen()
Testfall(0, 4.9)
Testfall(1999, 4.9)
Testfall(2000, 4.9)
Testfall(2001, 6.9)
print(Testfall.anzahl, "Testfälle:", list(Testfall.alle.values()))
print("Fehlgeschlagen:", Testfall.fehlgeschlagen(versandkosten))
