"""Aufgabe 5_013 – Prüfregeln                                   Stufe 5 ★★★★★

Ein Monitoring-Werkzeug überwacht Server. Für jede Messgröße (CPU-Last,
freier Speicher, Temperatur …) gibt es eine Prüfregel: eine Klasse mit
einer Kennung wie "cpu" und einer Methode pruefe(wert), die "ok",
"warnung" oder "kritisch" liefert. Neue Regeln schreiben verschiedene
Teams als Erweiterung, und eine fehlerhafte Regel soll nicht erst
nachts beim ersten Messwert auffallen, sondern schon, wenn ihre Klasse
definiert wird. Außerdem soll das Werkzeug alle Regeln finden, ohne
dass jemand sie in eine Liste einträgt. Vervollständigen Sie die
Metaklasse `Pruefmeta`:

- `__new__(mcs, name, basen, namensraum)` erzeugt die Klasse. Hat
  keine der Basen die Metaklasse Pruefmeta, ist die neue Klasse eine
  Wurzel (wie `Pruefregel` unten): Sie bekommt ein eigenes, leeres
  Verzeichnis ihrer Regeln und wird nicht geprüft. Jede andere Klasse
  ist eine Regel und muss jeden Namen aus dem Tupel pflicht ihrer
  Wurzel haben (selbst definiert oder geerbt), sonst TypeError mit der
  Meldung "<Klassenname> fehlt: <fehlende Namen>", die Namen in der
  Reihenfolge von pflicht durch ", " getrennt. Außerdem muss
  kennung ein nicht leerer Text und pruefe aufrufbar sein, und die
  kennung darf in ihrer Wurzel noch nicht vergeben sein; sonst
  ebenfalls TypeError. Eine abgelehnte Klasse wird nicht eingetragen.
- `__iter__(cls)` durchläuft die Regeln der Wurzel von cls in der
  Reihenfolge ihrer Definition, `__len__(cls)` gibt ihre Anzahl zurück,
  `__getitem__(cls, kennung)` die Regel mit dieser Kennung (KeyError,
  wenn es sie nicht gibt). Diese Methoden arbeiten auf der Klasse
  selbst: for regel in Pruefregel, len(Pruefregel), Pruefregel["cpu"].

    class CpuLast(Pruefregel):
        kennung = "cpu"
        def pruefe(self, wert):
            return "kritisch" if wert > 95 else "warnung" if wert > 80 else "ok"

    class Kaputt(Pruefregel):         →  TypeError: Kaputt fehlt: kennung, pruefe
        pass

    len(Pruefregel), Pruefregel["cpu"]       →  (1, CpuLast)
    auswerten({"cpu": 91})                   →  {"cpu": "warnung"}

Grenzen: Eine Wurzel hat ein Tupel pflicht mit 0 bis 20 Namen und 0 bis
10 000 Regeln; es kann mehrere Wurzeln mit getrennten Verzeichnissen
geben. Regeln dürfen voneinander erben (dann brauchen sie eine eigene
kennung). kennung kann ein beliebiger Wert sein, auch fehlen.

Hintergrund: In Aufgabe 5_011 haben Sie gesehen, dass type die Klasse
aller Klassen ist und eine class-Anweisung im Grunde type(name, basen,
namensraum) aufruft. Schreibt man class Regel(metaclass=Meta), ruft
Python stattdessen Meta(name, basen, namensraum) auf. Eine eigene
Metaklasse ist eine Unterklasse von type; in ihrem __new__ entsteht die
Klasse mit super().__new__(mcs, name, basen, namensraum), und davor oder
danach kann man prüfen und eintragen:

    class Meta(type):
        def __new__(mcs, name, basen, namensraum):
            if "run" not in namensraum:
                raise TypeError(f"{name} braucht run")
            return super().__new__(mcs, name, basen, namensraum)

Der erste Parameter heißt nach Konvention mcs (die Metaklasse), so wie
self das Objekt und cls die Klasse. Die Metaklasse wird vererbt: Jede
Unterklasse von Pruefregel wird wieder mit Pruefmeta gebaut, ohne dass
dort metaclass= steht. Mit isinstance(basis, Pruefmeta) erkennt man, ob
eine Basis schon dazugehört. Ob ein Name geerbt oder selbst definiert
ist, prüft hasattr(klasse, name) auf der fertigen Klasse; in namensraum
stehen nur die eigenen Namen.

Methoden einer Metaklasse sind Methoden der Klassen, so wie Methoden
einer Klasse Methoden ihrer Objekte sind. Definiert die Metaklasse
__iter__, __len__ oder __getitem__, funktionieren for, len() und []
auf der Klasse selbst. (list[int] funktioniert übrigens anders, über
__class_getitem__, nächste Aufgabe.) Die Objekte der Regeln bekommen
diese Methoden nicht: len(CpuLast()) ist ein Fehler.

__init_subclass__ (Aufgabe 5_010) kann Unterklassen auch prüfen und
eintragen, und oft genügt das. Eine Metaklasse kann mehr: Sie sieht
auch die Wurzel selbst, sie kann Operatoren für Klassen definieren wie
hier, und sie kann sogar das Erzeugen von Objekten (__call__) steuern.
Der Preis: Eine Klasse kann nur eine Metaklasse haben, und wer von zwei
Klassen mit verschiedenen Metaklassen erben will, bekommt einen
„metaclass conflict“. abc.ABC (Aufgabe 4_011) ist genau so gebaut: Seine
Metaklasse ABCMeta prüft die abstrakten Methoden, allerdings erst beim
Erzeugen eines Objekts.
"""


class Pruefmeta(type):
    """Metaklasse für Prüfregeln: prüft die Schnittstelle und führt ein Verzeichnis je Wurzel."""

    def __new__(mcs, name, basen, namensraum):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(cls):
        """Durchläuft die Regeln der Wurzel in der Reihenfolge ihrer Definition."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(cls):
        """Gibt die Anzahl der Regeln der Wurzel zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __getitem__(cls, kennung):
        """Gibt die Regel mit dieser Kennung zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Pruefregel(metaclass=Pruefmeta):
    """Wurzel aller Prüfregeln des Monitorings."""

    pflicht = ("kennung", "pruefe")


class CpuLast(Pruefregel):
    """Prüft die CPU-Last in Prozent."""

    kennung = "cpu"

    def pruefe(self, wert):
        """Über 95 % kritisch, über 80 % Warnung."""
        if wert > 95:
            return "kritisch"
        if wert > 80:
            return "warnung"
        return "ok"


def auswerten(messwerte):
    """Prüft jeden Messwert mit der Regel seiner Kennung; Kennungen ohne Regel werden übersprungen."""
    ergebnis = {}
    for regel in Pruefregel:
        if regel.kennung in messwerte:
            ergebnis[regel.kennung] = regel().pruefe(messwerte[regel.kennung])
    return ergebnis


try:

    class Kaputt(Pruefregel):
        """Eine Regel ohne kennung und pruefe."""

except TypeError as fehler:
    print(fehler)
print(len(Pruefregel), Pruefregel["cpu"].__name__)
print(auswerten({"cpu": 91}))
