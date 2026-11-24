"""Aufgabe 5_050 – Typwächter                                    Stufe 5 ★★★★★

Ein Analyseteam sagt für eine Spritzgussanlage voraus, welche Teile
Ausschuss werden. Seine Auswertungs-Pipeline besteht aus kleinen
Funktionen, die in einer gemeinsamen Bibliothek liegen: Messwerte
normalisieren, eine Stichprobe ziehen, einen Lernschritt des Modells
rechnen. Die Einstellungen kommen aus einer Konfigurationsdatei und
einer Weboberfläche, und dort ist jeder Wert zunächst ein Text. Neulich
hat jemand lernrate="0.01" übergeben; der Fehler zeigte sich erst tief
im Training als rätselhafte Meldung über Sequenzen und Kommazahlen. Ein
anderes Mal kam anzahl=True an, und weil True in Python als 1 zählt,
lief alles durch, nur mit einer Stichprobe aus einem einzigen Wert.

Alle Funktionen der Bibliothek tragen schon Typannotationen. Ein
Dekorator soll sie beim Aufruf durchsetzen und einen falschen Aufruf
sofort mit einer klaren Meldung abweisen, bevor die Funktion
überhaupt anfängt. Schreiben Sie:

- `passt(wert, typ)` gibt True zurück, wenn wert zur Annotation typ
  passt, sonst False. Grundsätzlich gilt isinstance(wert, typ), mit
  diesen Festlegungen: True und False passen nicht zu int und nicht zu
  float, nur zu bool. Eine ganze Zahl passt auch zu float (lernrate=1
  ist gemeint wie 1.0). Zur Annotation None passt nur der Wert None.
- `typgeprueft(funktion)` ist ein Dekorator. Beim Dekorieren berechnet
  er einmal die Signatur der Funktion und prüft, dass jede Annotation
  unterstützt wird: eine Klasse (int, float, str, bool, list, dict,
  tuple, eigene Klassen) oder None. Steht etwas anderes da, etwa
  list[float], int | None oder der Text "int", löst schon das Dekorieren
  einen TypeError aus, dessen Meldung Funktion und Parameter nennt.
- Bei jedem Aufruf ordnet die dekorierte Funktion die Argumente den
  Parametern zu, auch die Standardwerte, und prüft jeden annotierten
  Parameter in der Reihenfolge der Signatur. Bei *werte: float muss
  jedes einzelne Argument passen, bei **optionen: int jeder Wert. Passt
  eines nicht, löst sie einen TypeError aus, ohne die Funktion
  aufzurufen; die Meldung nennt die Funktion, den ersten unpassenden
  Parameter, den erwarteten und den erhaltenen Typ (die Namen der
  Klassen, für die Annotation None einfach "None"). Parameter ohne
  Annotation werden nicht geprüft. Passen die Argumente gar nicht zur
  Signatur (eines fehlt, eines zu viel), kommt der TypeError von Python
  selbst; den lassen Sie durch.
- Ist die Rückgabe annotiert (-> list, -> None), prüft sie nach dem
  Aufruf auch das Ergebnis und löst bei einem unpassenden einen
  TypeError aus, der die Funktion, den erwarteten und den erhaltenen Typ
  nennt. Sonst gibt sie das Ergebnis zurück. Name, Docstring und
  Signatur der Funktion bleiben erhalten.

    lernschritt(0.5, 2.0, lernrate=0.1)    →  0.3
    lernschritt(1, 2)                      →  0.8
    lernschritt(0.5, 2.0, lernrate="0.1")  →  TypeError: lernschritt: Parameter
                                              lernrate erwartet float, bekommen str
    stichprobe([4, 8, 15], True)           →  TypeError: stichprobe: Parameter
                                              anzahl erwartet int, bekommen bool

    @typgeprueft
    def schwelle(wert: list[float]): ...   →  TypeError beim Dekorieren

Grenzen: Eine dekorierte Funktion hat 0 bis 100 Parameter jeder Art
(auch mit Standardwerten, nur als Schlüsselwort, *args und **kwargs),
annotiert oder nicht. Die Argumente sind beliebige Werte, und eine
dekorierte Funktion wird bis zu 10 000-mal aufgerufen.

Hintergrund: Seit Aufgabe 4_016 tragen Ihre Funktionen Annotationen,
aber Python selbst beachtet sie nicht: lernschritt(0.5, 2.0, "0.1")
läuft los, als stünde nichts da. Annotationen sind nur Werte, die
Python an der Funktion ablegt, damit Werkzeuge wie mypy sie lesen. Zur
Laufzeit liest sie auch inspect.signature (Aufgabe 5_049): Jeder
Parameter der Signatur hat neben name, kind und default das Attribut
annotation, und die Signatur selbst hat return_annotation:

    import inspect

    def lernschritt(gewicht: float, gradient: float, lernrate=0.1) -> float:
        ...

    signatur = inspect.signature(lernschritt)
    signatur.parameters["gewicht"].annotation    →  <class 'float'>
    signatur.parameters["lernrate"].annotation   →  <class 'inspect._empty'>
    signatur.return_annotation                   →  <class 'float'>

Fehlt eine Annotation, steht dort der Platzhalter inspect.Parameter.empty
(bei der Rückgabe inspect.Signature.empty, dasselbe Objekt); man
vergleicht mit is. Ob eine Annotation eine Klasse ist, sagt
isinstance(annotation, type): Für int, list und eigene Klassen ist das
True, für list[float], int | None, None und den Text "int" False.

Wie in Aufgabe 5_049 ordnet signatur.bind(*args, **kwargs) die
Argumente eines Aufrufs den Parametern zu, so wie Python es beim Aufruf
täte, und löst denselben TypeError aus, wenn das nicht geht.
apply_defaults() ergänzt die Standardwerte, und arguments ist dann ein
Dictionary Parametername → Wert in der Reihenfolge der Signatur; bei
*werte steht dort ein Tupel, bei **optionen ein Dictionary:

    gebunden = signatur.bind(0.5, 2.0)
    gebunden.apply_defaults()
    gebunden.arguments   →  {'gewicht': 0.5, 'gradient': 2.0, 'lernrate': 0.1}

Den Dekorator selbst bauen Sie wie in Aufgabe 4_022 mit einer Hülle und
functools.wraps; mit Argumenten wie in Aufgabe 4_023 braucht er hier
nicht zu arbeiten. Die Signatur berechnen Sie einmal beim Dekorieren
außerhalb der Hülle: Die Hülle ist ein Closure und sieht die Variable
bei jedem Aufruf, und inspect.signature ist viel zu langsam, um es bei
jedem der vielen Aufrufe einer Pipeline zu wiederholen.

Zu bool: bool ist in Python eine Unterklasse von int, deshalb ist
isinstance(True, int) True. Für eine Anzahl oder eine Lernrate ist True
aber fast immer ein Versehen, darum schließt passt das aus. Genau so
unterscheidet functools.singledispatch aus Aufgabe 5_032 nach dem Typ,
nur wählt es eine Fassung aus, statt abzulehnen. Bibliotheken wie
pydantic oder typeguard prüfen auf diese Art auch verschachtelte
Annotationen wie list[float]; hier bleiben Sie bei einfachen Klassen.
"""

import functools
import inspect
import random


def passt(wert, typ):
    """Prüft, ob wert zur Annotation typ passt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def typgeprueft(funktion):
    """Dekorator: prüft bei jedem Aufruf Argumente und Ergebnis anhand der Annotationen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@typgeprueft
def normalisiere(werte: list, untergrenze: float = 0.0, obergrenze: float = 1.0) -> list:
    """Bildet die Messwerte linear auf den Bereich von untergrenze bis obergrenze ab."""
    kleinster, groesster = min(werte), max(werte)
    breite = (groesster - kleinster) or 1
    return [untergrenze + (wert - kleinster) / breite * (obergrenze - untergrenze) for wert in werte]


@typgeprueft
def stichprobe(daten: list, anzahl: int, startwert: int = 0) -> list:
    """Zieht anzahl Werte aus daten, mit festem Startwert für den Zufall."""
    return random.Random(startwert).sample(daten, anzahl)


@typgeprueft
def lernschritt(gewicht: float, gradient: float, lernrate: float = 0.1) -> float:
    """Ein Schritt des Gradientenverfahrens: das Gewicht ein Stück gegen den Gradienten verschieben."""
    return gewicht - lernrate * gradient


print(normalisiere([2, 4, 6]))
print(lernschritt(0.5, 2.0, lernrate=0.1))
try:
    lernschritt(0.5, 2.0, lernrate="0.1")
except TypeError as fehler:
    print(fehler)
