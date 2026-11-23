"""Aufgabe 4_048 – Rackzähler                                    Stufe 4 ★★★★☆

Ein Rechenzentrum vermietet ganze Serverschränke (Racks) an Kunden und
rechnet den Strom nach Verbrauch ab. In jedem Rack sitzt ein
Stromzähler, der wie ein Zähler im Haushalt immer weiter hochzählt; das
Abrechnungssystem liest den Zählerstand in Kilowattstunden (kWh) einmal
täglich aus. Die Zählerstände kommen als Iterator aus der Datenbank: Er
lässt sich nur einmal durchlaufen, und wie viele Werte er hat, weiß man
vorher nicht. Schreiben Sie mit dem Modul itertools drei Funktionen,
die je eine Liste zurückgeben:

- `verbraeuche(zaehlerstaende)`: der Verbrauch jedes Tages, also jeder
  Zählerstand minus den davor.
- `rueckspruenge(zaehlerstaende)`: die Stellen (gezählt ab 0) der
  Zählerstände, die kleiner sind als der davor. Ein Zähler läuft nie
  rückwärts; so ein Sprung heißt, dass der Zähler getauscht oder
  zurückgesetzt wurde und die Abrechnung dort von Hand geprüft werden
  muss.
- `vergleich(tageswerte, abstand)` bekommt Tagesverbräuche und gibt zu
  jedem Wert, zu dem es einen Wert abstand Tage später gibt, den
  Unterschied zurück: späterer Wert minus früherer. Mit abstand 7
  vergleicht man jeden Tag mit demselben Wochentag der Vorwoche.
  Benutzen Sie dafür tee.

Alle Funktionen bekommen einen Iterator, der sich nur einmal durchlaufen
lässt; Indizes und len() gibt es darum nicht.

    verbraeuche(iter([100, 112, 125, 125, 140]))   →  [12, 13, 0, 15]
    rueckspruenge(iter([500, 520, 3, 9, 8]))       →  [2, 4]
    vergleich(iter([10, 12, 11, 15, 13]), 2)       →  [1, 3, 2]

Im letzten Beispiel wird 11 mit 10 verglichen, 15 mit 12 und 13 mit 11.

Grenzen: Jeder Iterator liefert 0 bis 200 000 ganze Zahlen von 0 bis
10**9. 1 ≤ abstand ≤ 1000.

Hintergrund: Oft braucht man jedes Element zusammen mit seinem
Nachfolger. Bei einer Liste geht zip(werte, werte[1:]), aber bei einem
Iterator gibt es kein Slicing, und zweimal durchlaufen kann man ihn
auch nicht. itertools.pairwise liefert die Paare direkt:

    from itertools import islice, pairwise, tee

    list(pairwise([3, 5, 9, 10]))      →  [(3, 5), (5, 9), (9, 10)]
    list(pairwise([7]))                →  []

Aus n Werten werden n - 1 Paare. Mit enumerate (Aufgabe 2_021) zählt
man die Paare mit; enumerate(pairwise(werte), start=1) gibt jedem Paar
die Stelle seines zweiten Elements.

pairwise kennt nur den Abstand 1. Für größere Abstände hilft tee: tee(it)
macht aus einem Iterator zwei unabhängige, die dieselben Werte liefern.
Den einen schiebt man mit islice (Aufgabe 4_040) um ein paar Elemente
vor, dann passt zip die beiden zusammen:

    vorne, hinten = tee(iter([1, 2, 3, 4, 5]))
    hinten = islice(hinten, 2, None)       # überspringt zwei Werte
    list(zip(vorne, hinten))               →  [(1, 3), (2, 4), (3, 5)]

tee merkt sich intern die Werte, die der eine Iterator schon gelesen
hat und der andere noch nicht; bei einem Abstand von k sind das nur k
Werte. Den ursprünglichen Iterator darf man nach tee nicht mehr selbst
benutzen, sonst fehlen den Kopien Werte. tee(it, 3) liefert drei
Kopien. Das frühere Rezept für pairwise in der Python-Dokumentation
war genau so gebaut (mit Abstand 1).
"""

from itertools import islice, pairwise, tee


def verbraeuche(zaehlerstaende):
    """Gibt die Unterschiede aufeinanderfolgender Zählerstände zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def rueckspruenge(zaehlerstaende):
    """Gibt die Stellen der Zählerstände zurück, die kleiner sind als der davor."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def vergleich(tageswerte, abstand):
    """Gibt zu jedem Wert den Unterschied zum Wert abstand Tage später zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(verbraeuche(iter([100, 112, 125, 125, 140])))
print(rueckspruenge(iter([500, 520, 3, 9, 8])))
print(vergleich(iter([10, 12, 11, 15, 13]), 2))
