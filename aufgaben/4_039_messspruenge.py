"""Aufgabe 4_039 – Messsprünge                                   Stufe 4 ★★★★☆

In einer Fertigungshalle schicken Sensoren ihre Messwerte über MQTT an
einen zentralen Server, den Broker. Jede Nachricht hat ein Topic, eine
Adresse aus Ebenen mit / dazwischen wie "halle1/presse3/temp", und
einen Wert. Der Broker schreibt alle Nachrichten als Zeilen in ein
Protokoll:

    halle1/presse3/temp 61.5
    halle1/presse4/temp 58.0
    halle1/presse3/temp ERR
    halle1/presse3/temp 75.0

Ein plötzlicher Sprung eines Werts deutet auf einen Defekt hin, etwa ein
festsitzendes Ventil. Die Instandhaltung will darum zu einem
Topic-Muster wissen, wann ein Sensor zum ersten Mal einen Sprung meldet.
Im Muster steht + für genau eine beliebige Ebene: "halle1/+/temp" passt
zu "halle1/presse3/temp", aber nicht zu "halle1/presse3/druck" oder
"halle1/presse3/kopf/temp".

Das Protokoll ist sehr lang oder läuft sogar ohne Ende weiter. Schreiben
Sie darum alles lazy, mit Generatoren:

- `Messprotokoll(zeilen)` ist ein Iterable: `__init__` (vorgegeben)
  merkt sich zeilen, ein Iterable, das sich mehrfach durchlaufen lässt.
  Schreiben Sie `__iter__` als Generatormethode, die für jede gültige
  Zeile ein Tupel (topic, wert) mit wert als float liefert. Gültig ist
  eine Zeile, die aus genau zwei durch Leerzeichen getrennten Teilen
  besteht, deren zweiter sich mit float(...) umwandeln lässt; alle
  anderen Zeilen (leer, ERR, 21,5, zu viele Teile) werden übersprungen.
  Jeder Durchlauf beginnt wieder von vorn.
- `passend(messungen, muster)` ist eine Generatorfunktion, die von den
  Tupeln (topic, wert) nur die liefert, deren Topic zum Muster passt.
- `spruenge(messungen, schwelle)` ist eine Generatorfunktion, die sich
  zu jedem Topic den letzten Wert merkt. Unterscheidet sich ein neuer
  Wert davon um mehr als schwelle (nach oben oder unten), liefert sie
  ein Tupel (topic, alter_wert, neuer_wert). Der erste Wert eines Topics
  ist nie ein Sprung.
- `erster_sprung(protokoll, muster, schwelle)` steckt die drei zu einer
  Kette zusammen und gibt den ersten Sprung zurück, oder None, wenn das
  (endliche) Protokoll keinen hat. Sie liest nur so viele Zeilen wie
  nötig.

    protokoll = Messprotokoll(["halle1/presse3/temp 61.5",
                               "halle1/presse4/temp 58.0",
                               "halle1/presse3/temp ERR",
                               "halle1/presse3/temp 75.0"])
    list(protokoll)  →  [("halle1/presse3/temp", 61.5),
                         ("halle1/presse4/temp", 58.0),
                         ("halle1/presse3/temp", 75.0)]
    erster_sprung(protokoll, "halle1/+/temp", 10)
        →  ("halle1/presse3/temp", 61.5, 75.0)
    erster_sprung(protokoll, "halle1/+/temp", 20)  →  None

Grenzen: Ein Protokoll hat bis zu 100 000 Zeilen oder ist unendlich.
Topics und Muster bestehen aus 1 bis 6 Ebenen ohne Leerzeichen; eine
Ebene im Muster ist ein Name oder +, eine Ebene in einem Topic nie +.
Werte und schwelle liegen zwischen -10**6 und 10**6, schwelle ≥ 0. Ein
Unterschied genau gleich schwelle ist kein Sprung.

Hintergrund: Diese Übung verbindet die Aufgaben 4_032 bis 4_038.
Ein Iterable ist ein Objekt mit __iter__, das bei jedem Aufruf einen
neuen Iterator liefert (Aufgabe 4_033); darum kann man es mehrfach und
sogar verschachtelt durchlaufen. Am kürzesten schreibt man __iter__ als
Generatormethode mit yield (Aufgabe 4_035):

    class Seriennummern:
        def __init__(self, texte):
            self.texte = texte

        def __iter__(self):
            for text in self.texte:
                if text.isdigit():
                    yield int(text)

Generatorfunktionen, die als Eingabe wieder ein Iterable bekommen,
lassen sich zu einer Pipeline zusammenstecken (Aufgabe 4_036): Jede
Stufe holt sich erst dann den nächsten Wert, wenn die Stufe nach ihr
einen haben will. Eine Stufe darf sich dabei etwas merken, etwa in
einem Dictionary in ihren lokalen Variablen; es lebt so lange wie der
Generator. Den ersten Wert einer Pipeline holt next(kette); next(kette,
None) gibt None zurück statt StopIteration auszulösen, wenn die Kette
leer ist (Aufgabe 4_034):

    kette = (zahl for zahl in Seriennummern(["12", "x", "40"]) if zahl > 20)
    next(kette, None)   →  40
    next(kette, None)   →  None

Wer dagegen in einer Stufe erst alle Werte in einer Liste sammelt, liest
das ganze Protokoll, und bei einem unendlichen kommt er nie an.

Ob ein Text sich in eine Zahl umwandeln lässt, prüft man am einfachsten,
indem man es versucht: float(text) in try, und except ValueError fängt
den Fehlschlag ab (Aufgabe 3_007).
"""


class Messprotokoll:
    """Die Zeilen eines Broker-Protokolls, als Tupel (topic, wert) beliebig oft durchlaufbar."""

    def __init__(self, zeilen):
        self.zeilen = zeilen

    def __iter__(self):
        """Liefert für jede gültige Zeile das Tupel (topic, wert)."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def passend(messungen, muster):
    """Liefert die Messungen, deren Topic zum Muster mit + passt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def spruenge(messungen, schwelle):
    """Liefert (topic, alter_wert, neuer_wert) für jeden Sprung um mehr als schwelle."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def erster_sprung(protokoll, muster, schwelle):
    """Gibt den ersten Sprung der passenden Topics zurück, sonst None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokoll = Messprotokoll(
    ["halle1/presse3/temp 61.5", "halle1/presse4/temp 58.0", "halle1/presse3/temp ERR", "halle1/presse3/temp 75.0"]
)
print(list(protokoll))
print(erster_sprung(protokoll, "halle1/+/temp", 10))
print(erster_sprung(protokoll, "halle1/+/temp", 20))
