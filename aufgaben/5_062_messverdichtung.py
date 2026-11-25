"""Aufgabe 5_062 – Messverdichtung                               Stufe 5 ★★★★★

Ein Monitoring-System misst jede Sekunde Kennzahlen wie die Antwortzeit
einer Webschnittstelle in Millisekunden oder die CPU-Auslastung. So
viele Einzelwerte will niemand ansehen. Darum werden die Messwerte in
Fenstern verdichtet: Sind fenster Werte einer Kennzahl beisammen, macht
eine Verdichtungsstrategie daraus einen Wert, und das Fenster beginnt
von vorn. Welche Strategie passt, hängt von der Kennzahl ab: der
Mittelwert für die CPU, das Maximum für die Temperatur, für
Antwortzeiten oft das 95. Perzentil (der Wert, unter dem 95 Prozent der
Messungen liegen). Jeder verdichtete Wert geht an alle angemeldeten
Beobachter: das Dashboard, einen Exporter für die Langzeitablage und
eine Alarmregel. Beobachter kommen und gehen zur Laufzeit.

Strategien und Beobachter sollen Funktionen sein, keine
Klassenhierarchie (siehe Hintergrund). Schreiben Sie:

- `mittelwert(werte)` gibt den Mittelwert der Liste werte zurück.
- `perzentil(p)` gibt eine Strategie zurück, die das p-te Perzentil
  einer Liste werte bestimmt, ohne die Liste zu verändern: Sortiert
  man werte aufsteigend, ist es der Wert an der Stelle rang (ab 1
  gezählt), wobei rang die kleinste ganze Zahl ist, die mindestens
  p · len(werte) / 100 ist.
- `alarm_ab(schwelle, meldungen)` gibt einen Beobachter zurück, der bei
  jedem Aufruf mit (name, wert) das Paar (name, wert) an die Liste
  meldungen hängt, wenn wert größer als schwelle ist.
- in der Klasse `Kennzahl` die Methoden
  - `anmelden(self, beobachter)`: meldet einen Beobachter an, also
    etwas, das man mit (name, wert) aufrufen kann, und gibt ihn zurück.
    Ist er schon angemeldet (gleich nach ==), passiert nichts.
  - `abmelden(self, beobachter)`: meldet ihn wieder ab; ist er nicht
    angemeldet, ValueError.
  - `erfasse(self, wert)`: hängt wert an das aktuelle Fenster. Ist es
    damit voll, verdichtet sie es mit self.strategie, beginnt ein leeres
    Fenster, ruft jeden Beobachter mit (self.name, verdichteter Wert)
    auf, in der Reihenfolge der Anmeldung, und gibt den verdichteten
    Wert zurück; sonst None. Benachrichtigt werden alle, die beim
    Verdichten angemeldet sind, auch wenn sich einer von ihnen während
    der Benachrichtigung abmeldet. Wird self.strategie ausgetauscht,
    gilt die neue Strategie ab dem nächsten vollen Fenster.

    antwortzeit = Kennzahl("api.antwortzeit", mittelwert, fenster=3)
    dashboard = Dashboard()
    export, alarme = [], []
    antwortzeit.anmelden(dashboard.zeige)
    antwortzeit.anmelden(partial(exportiere, export))
    antwortzeit.anmelden(alarm_ab(200, alarme))
    [antwortzeit.erfasse(ms) for ms in [120, 180, 150, 240, 310, 290]]
        →  [None, None, 150.0, None, None, 280.0]
    dashboard.anzeige    →  {"api.antwortzeit": 280.0}
    export               →  ["api.antwortzeit;150.0", "api.antwortzeit;280.0"]
    alarme               →  [("api.antwortzeit", 280.0)]
    perzentil(95)([12, 50, 7, 31])   →  50   (rang 4 von 7, 12, 31, 50)
    perzentil(50)([12, 50, 7, 31])   →  12   (rang 2)

Auch eingebaute Funktionen wie max und min sind fertige Strategien:
Kennzahl("temperatur", max, fenster=60).

Grenzen: fenster ist eine ganze Zahl von 1 bis 10 000, jeder Messwert
eine ganze Zahl oder eine Kommazahl von -10**9 bis 10**9. Eine
Strategie bekommt eine Liste mit 1 bis 10 000 Werten, p ist eine ganze
Zahl von 1 bis 100, schwelle eine Zahl wie die Messwerte. Eine Kennzahl
bekommt bis zu 200 000 Werte und hat bis zu 10 Beobachter: Funktionen,
gebundene Methoden, partial-Objekte, Lambdas oder Objekte mit __call__.

Hintergrund: Das Entwurfsmuster Strategie trennt, was getan wird
(verdichten), davon, wie es getan wird (Mittelwert, Maximum …), sodass
man das Wie austauschen kann. Das Muster Beobachter lässt ein Objekt
andere benachrichtigen, ohne sie zu kennen. Beide stammen aus der Zeit
von Sprachen, in denen man nur Objekte herumreichen konnte, und
werden darum meist mit Klassen aufgeschrieben, wie in Java oder C++:

    class Verdichtung(ABC):                 # die Strategie-Schnittstelle
        @abstractmethod
        def verdichte(self, werte): ...

    class Mittelwert(Verdichtung):
        def verdichte(self, werte):
            return sum(werte) / len(werte)

    class Beobachter(ABC):                  # die Beobachter-Schnittstelle
        @abstractmethod
        def aktualisiere(self, name, wert): ...

    class Alarm(Beobachter):
        def __init__(self, schwelle):
            self.schwelle = schwelle
        def aktualisiere(self, name, wert):
            if wert > self.schwelle: ...

    kennzahl = Kennzahl("cpu", Mittelwert(), 5)
    kennzahl.anmelden(Alarm(90))            # ruft später alarm.aktualisiere(...)

Eine Klasse mit genau einer Methode ist in Python fast immer eine
verkleidete Funktion. Funktionen sind Werte (Aufgabe 3_028), also kann
die Strategie einfach die Funktion selbst sein, und die Kennzahl ruft
self.strategie(werte) auf. Braucht eine Strategie Einstellungen wie p
beim Perzentil, baut eine Fabrikfunktion eine Closure, die sich p merkt
(Aufgabe 4_021), oder functools.partial belegt das Argument vor
(Aufgabe 4_028):

    def gekappt(grenze):                    # Strategie-Fabrik mit Closure
        def strategie(werte):
            return min(max(werte), grenze)
        return strategie

    def gekapptes_maximum(werte, grenze):
        return min(max(werte), grenze)

    kennzahl.strategie = gekappt(100)
    kennzahl.strategie = partial(gekapptes_maximum, grenze=100)   # dasselbe

Für Beobachter heißt das Gleiche Callback (Rückruffunktion): Die
Kennzahl merkt sich eine Liste von Aufrufbarem und ruft jedes davon auf.
Was aufrufbar ist, ist dabei egal: eine Funktion, eine gebundene Methode
wie dashboard.zeige, die sich ihr Objekt merkt, ein partial-Objekt oder
ein Objekt mit __call__ (Aufgabe 5_020), wenn der Beobachter Zustand
braucht. Drei Stolperstellen:

    kennzahl.anmelden(lambda name, wert: print(wert))
    kennzahl.abmelden(lambda name, wert: print(wert))   # ValueError

Jede Lambda ist ein neues Objekt; abmelden kann man nur, was man sich
gemerkt hat. Darum gibt anmelden den Beobachter zurück (rueckruf =
kennzahl.anmelden(...)), so kann man es sogar als Dekorator schreiben:
@kennzahl.anmelden über einem def. Zweitens ist dashboard.zeige bei
jedem Zugriff ein neues Methodenobjekt: dashboard.zeige is
dashboard.zeige ist False, aber == ist True. Suchen Sie also mit == (in,
remove), nicht mit is. Drittens darf sich ein Beobachter beim Aufruf
abmelden; wer dabei über die Liste selbst läuft, überspringt den
nächsten, weil remove alle folgenden einen Platz nach vorn rückt.
Laufen Sie darum über eine Kopie (list(self.beobachter)).

Klassen lohnen sich weiterhin, wenn mehrere Methoden zusammengehören
(eine Strategie mit Namen, Einheit und Verdichtung) oder wenn die
Schnittstelle dokumentiert werden soll; dann beschreibt sie ein
Protocol (Aufgabe 5_016), und Funktionen wie Klassen erfüllen es.

Tipp: Rechnen Sie den Rang mit ganzen Zahlen, (p * n + 99) // 100, oder
mit math.ceil(p * n / 100). math.ceil(p / 100 * n) rundet manchmal
falsch: 7 / 100 * 100 ist 7.000000000000001.
"""

from functools import partial


class Dashboard:
    """Zeigt zu jeder Kennzahl den zuletzt verdichteten Wert an."""

    def __init__(self):
        self.anzeige = {}

    def zeige(self, name, wert):
        """Merkt sich wert als aktuellen Wert der Kennzahl name."""
        self.anzeige[name] = wert


def exportiere(zeilen, name, wert):
    """Hängt für die Langzeitablage eine Zeile "name;wert" an zeilen an."""
    zeilen.append(f"{name};{wert}")


def mittelwert(werte):
    """Gibt den Mittelwert der Werte zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def perzentil(p):
    """Gibt eine Strategie zurück, die das p-te Perzentil einer Liste bestimmt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def alarm_ab(schwelle, meldungen):
    """Gibt einen Beobachter zurück, der Werte über schwelle in meldungen sammelt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Kennzahl:
    """Eine Kennzahl, deren Messwerte fensterweise verdichtet und an Beobachter gemeldet werden."""

    def __init__(self, name, strategie, fenster):
        self.name = name
        self.strategie = strategie
        self.fenster = fenster
        self.werte = []
        self.beobachter = []

    def anmelden(self, beobachter):
        """Meldet beobachter an (höchstens einmal) und gibt ihn zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def abmelden(self, beobachter):
        """Meldet beobachter ab; ValueError, wenn er nicht angemeldet ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def erfasse(self, wert):
        """Nimmt wert auf; gibt bei vollem Fenster den verdichteten Wert zurück, sonst None."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


antwortzeit = Kennzahl("api.antwortzeit", mittelwert, fenster=3)
dashboard = Dashboard()
export, alarme = [], []
antwortzeit.anmelden(dashboard.zeige)
antwortzeit.anmelden(partial(exportiere, export))
antwortzeit.anmelden(alarm_ab(200, alarme))
print([antwortzeit.erfasse(ms) for ms in [120, 180, 150, 240, 310, 290]])
print(dashboard.anzeige, export, alarme)
print(perzentil(95)([12, 50, 7, 31]), perzentil(50)([12, 50, 7, 31]))
