"""Aufgabe 4_082 – Änderungsanträge                              Stufe 4 ★★★★☆

In einem Softwareprojekt darf niemand den vereinbarten Umfang einfach
ändern. Wünscht der Kunde eine neue Funktion, stellt er einen
Änderungsantrag (Change Request); ein Ausschuss schätzt den Aufwand in
Personentagen und entscheidet, ob und wann das Team ihn umsetzt. Das
Projektbüro baut dafür ein kleines Modul. Zwei Werte heißen darin
gleich: STUNDEN_PRO_TAG auf Modulebene ist die Arbeitszeit laut Vertrag
(ein Personentag hat 8 Stunden), Projektteam.STUNDEN_PRO_TAG dagegen
sind die Stunden, die jede Person des Teams pro Tag für
Änderungsanträge frei hat. Vervollständigen Sie das Modul:

- `neuer_antrag(titel, tage)` erhöht die globale Variable LETZTE_NUMMER
  um 1 und gibt {"nummer": "CR-001", "titel": titel, "tage": tage}
  zurück, die Nummer mit mindestens drei Ziffern.
- In der Klasse `Projektteam` legen Sie im Klassenkörper, unter PERSONEN
  und STUNDEN_PRO_TAG, zwei Klassenattribute an: TAGESSTUNDEN (wie viele
  Stunden das ganze Team pro Tag für Anträge hat) und WOCHENPLAN (eine
  Liste mit fünfmal TAGESSTUNDEN, einmal je Wochentag).
- `Projektteam.dauer(self, antrag)` gibt zurück, wie viele Arbeitstage
  das Team für den Antrag braucht, aufgerundet: Der Aufwand in Stunden
  ist antrag["tage"] mal die Stunden laut Vertrag; pro Tag schafft das
  Team PERSONEN mal seine STUNDEN_PRO_TAG. Unterklassen ändern PERSONEN
  oder STUNDEN_PRO_TAG; dauer soll dann deren Werte nehmen.
- `bereich(funktion, name)` sagt, wo Python den Namen name sucht und
  findet, wenn funktion ihn benutzt: "lokal", "umschließend", "global"
  oder "eingebaut", und None, wenn es ihn nirgends gibt.

    antrag = neuer_antrag("Export als PDF", 3)
    antrag                          →  {"nummer": "CR-001",
                                        "titel": "Export als PDF", "tage": 3}
    neuer_antrag("Zweite Sprache", 5)["nummer"]   →  "CR-002"
    Projektteam.TAGESSTUNDEN        →  6
    Projektteam.WOCHENPLAN          →  [6, 6, 6, 6, 6]
    Projektteam().dauer(antrag)     →  4     (3 · 8 = 24 Stunden, 24 / 6)
    bereich(Projektteam.dauer, "STUNDEN_PRO_TAG")   →  "global"
    bereich(Projektteam.dauer, "self")              →  "lokal"
    bereich(neuer_antrag, "LETZTE_NUMMER")          →  "global"
    bereich(neuer_antrag, "str")                    →  "eingebaut"

Grenzen: titel ist ein nicht leerer Text, tage eine ganze Zahl von 1 bis
1000. LETZTE_NUMMER ist eine ganze Zahl von 0 bis 99 998; die Tests
setzen sie auch von außen. In Unterklassen ist 1 ≤ PERSONEN ≤ 50 und
1 ≤ STUNDEN_PRO_TAG ≤ 8. funktion ist eine mit def oder lambda
geschriebene Funktion, name ein Name, den sie als Variable benutzt
(nicht nur als Attribut hinter einem Punkt) oder der einer ihrer
Parameter ist.

Hintergrund: Wo eine Variable gilt, kennen Sie im Groben: lokal in der
Funktion, global im Modul (Aufgabe 2_013), dazwischen die Variablen
einer umgebenden Funktion (Closures, Aufgabe 4_021). Liest eine
Funktion einen Namen, sucht Python ihn in genau dieser Reihenfolge,
kurz LEGB:

    L  Local       lokal: Parameter und alles, was die Funktion zuweist
    E  Enclosing   in umgebenden Funktionen (von innen nach außen)
    G  Global      auf Modulebene
    B  Built-in    eingebaut: len, print, str, max, ValueError …

Der erste Treffer gilt. Darum kann ein globaler Name einen eingebauten
verdecken: Nach max = 3 auf Modulebene ist max(1, 2) ein TypeError,
weil Python das globale max zuerst findet. Ob ein Name lokal ist,
entscheidet Python schon beim Übersetzen der Funktion, nicht erst beim
Aufruf: Steht irgendwo in der Funktion eine Zuweisung an ihn, ist er in
der ganzen Funktion lokal, und Lesen vor der Zuweisung gibt einen
UnboundLocalError (Aufgabe 2_013). Mit global name am Anfang der
Funktion schreiben Sie stattdessen die globale Variable, mit nonlocal
die einer umgebenden Funktion (Aufgabe 4_021):

    ZAEHLER = 0

    def weiter():
        global ZAEHLER
        ZAEHLER += 1
        return ZAEHLER

Eine Sonderrolle hat der Klassenkörper. Seine Zeilen laufen einmal von
oben nach unten, wenn die Klasse entsteht, und sehen dabei die Namen,
die weiter oben im Klassenkörper stehen, wie auf Modulebene. Für die
Funktionen darin ist er aber kein umschließender Bereich: Eine Methode
überspringt die Klasse und sucht direkt global. Klassenattribute
erreicht sie nur über self oder den Klassennamen (Aufgabe 3_043):

    TAGE = 10

    class Phase:
        TAGE = 15
        WOCHEN = TAGE // 5            # 3: im Klassenkörper gilt TAGE = 15

        def laenge(self):
            return TAGE               # 10: die globale Variable!

        def richtig(self):
            return self.TAGE          # 15, in Unterklassen deren Wert

Dasselbe gilt für eine Comprehension im Klassenkörper, denn sie läuft
wie eine kleine eigene Funktion. Nur der Ausdruck ganz rechts (hinter
dem ersten in) wird noch im Klassenkörper ausgewertet:

    class Phase:
        TAGE = 15
        PLAN = [TAGE for _ in range(3)]    # NameError: TAGE
        PLAN = [8 for _ in range(TAGE)]    # geht: range(TAGE) steht vorn
        PLAN = [TAGE] * 3                  # geht und ist kürzer

Wo eine Funktion ihre Namen sucht, kann man sie selbst fragen. Ihr
Codeobjekt funktion.__code__ führt die Namen in Tupeln: co_varnames
enthält die Parameter und lokalen Variablen, co_cellvars die lokalen
Variablen, die eine innere Funktion mitbenutzt, co_freevars die Namen
aus umgebenden Funktionen (Aufgabe 4_081) und co_names alle übrigen
Namen, also die globalen und eingebauten (dazu auch Attributnamen wie
ceil in math.ceil). Die globalen Variablen der Funktion stehen im
Dictionary funktion.__globals__, die eingebauten im Modul builtins:

    import builtins
    hasattr(builtins, "len")          →  True
"""

import builtins
import math

STUNDEN_PRO_TAG = 8  # Arbeitsstunden eines Personentags laut Vertrag
LETZTE_NUMMER = 0  # zuletzt vergebene Nummer eines Änderungsantrags


def neuer_antrag(titel, tage):
    """Vergibt die nächste Nummer und gibt den neuen Antrag als Dictionary zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Projektteam:
    """Ein Projektteam, das einen Teil seines Arbeitstags für Änderungsanträge frei hat."""

    PERSONEN = 3
    STUNDEN_PRO_TAG = 2  # Stunden je Person und Tag für Änderungsanträge
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def dauer(self, antrag):
        """Gibt die aufgerundete Zahl der Arbeitstage zurück, die das Team für antrag braucht."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bereich(funktion, name):
    """Gibt "lokal", "umschließend", "global", "eingebaut" oder None zurück: wo funktion den Namen findet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


antrag = neuer_antrag("Export als PDF", 3)
print(antrag)
print(neuer_antrag("Zweite Sprache", 5)["nummer"])
print(Projektteam.TAGESSTUNDEN, Projektteam.WOCHENPLAN)
print(Projektteam().dauer(antrag))
print(bereich(Projektteam.dauer, "STUNDEN_PRO_TAG"))
