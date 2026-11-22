"""Aufgabe 4_061 – Stromkreise                                   Stufe 4 ★★★★☆

In einem Serverraum hängen die Geräte jedes Racks an Steckdosenleisten,
die an einem eigenen, abgesicherten Stromkreis hängen. Die Sicherung
löst aus, wenn mehr Strom fließt als ihr Nennstrom in Ampere (A). Die
größte Leistung, die ein Stromkreis liefern kann, ist Spannung mal
Strom: bei 230 Volt und einer 16-A-Sicherung 230 · 16 = 3680 Watt. Das
Betriebsteam pflegt die Geräte in einer Liste mit Zeilen der Form
name;watt und will vor jedem Einbau die Auslastung prüfen.

Die Datensätze sind klein und ändern sich nicht, darum sollen sie
benannte Tupel werden. Schreiben Sie:

- `Verbraucher` mit collections.namedtuple, Felder name (Text) und watt
  (ganze Zahl).
- `Stromkreis` als Unterklasse von typing.NamedTuple mit den Feldern
  name (Text), ampere (ganze Zahl) und spannung (ganze Zahl, Standardwert
  230) und der Methode max_watt(), die spannung · ampere zurückgibt.
- `lies_verbraucher(zeilen)` macht aus einer Liste solcher Zeilen eine
  Liste von Verbraucher-Tupeln, watt als ganze Zahl.
- `auslastung(kreis, verbraucher)` gibt zurück, wie viel Prozent von
  kreis.max_watt() alle Verbraucher zusammen brauchen, gerundet auf eine
  Nachkommastelle.
- `aufgeruestet(kreis, ampere)` gibt einen neuen Stromkreis zurück, der
  dem alten gleicht, aber eine Sicherung mit ampere hat.

    kreis = Stromkreis("A1", 16)
    server = lies_verbraucher(["db-01;450", "web-01;320", "switch-01;90"])
    server[0]                    →  Verbraucher(name='db-01', watt=450)
    server[0].watt               →  450
    kreis                        →  Stromkreis(name='A1', ampere=16, spannung=230)
    kreis.max_watt()             →  3680
    auslastung(kreis, server)    →  23.4
    aufgeruestet(kreis, 32)      →  Stromkreis(name='A1', ampere=32, spannung=230)

Grenzen: 0 bis 10 000 Zeilen, jede genau name;watt mit einem nicht
leeren Namen ohne Semikolon und watt von 1 bis 5000. ampere ist eine
ganze Zahl von 1 bis 63, spannung eine von 100 bis 400.

Hintergrund: Ein Tupel wie ("db-01", 450) ist schnell gebaut, aber
eintrag[1] sagt nicht, was die 1 bedeutet. Ein benanntes Tupel gibt den
Stellen Namen und bleibt trotzdem ein Tupel. collections.namedtuple baut
die Klasse aus einem Namen und einer Liste der Felder:

    from collections import namedtuple

    Punkt = namedtuple("Punkt", ["x", "y"])
    p = Punkt(3, y=4)
    p.x, p[1]            →  (3, 4)      über den Namen und über die Stelle
    x, y = p             # auspacken wie jedes Tupel
    p == (3, 4)          →  True        es ist ein Tupel
    p.x = 5              # AttributeError: unveränderlich

Dieselbe Klasse mit Typannotationen (Aufgabe 4_016), Standardwerten und
eigenen Methoden schreibt man als Unterklasse von typing.NamedTuple, so
ähnlich wie eine Datenklasse (Aufgabe 4_012):

    from typing import NamedTuple

    class Bildschirm(NamedTuple):
        modell: str
        zoll: float
        hertz: int = 60                 # Standardwert, steht hinter den Feldern ohne

        def ist_gross(self):
            return self.zoll >= 27

    b = Bildschirm("X27", 27.0)
    b.hertz              →  60
    b.ist_gross()        →  True

Weil man ein Tupel nicht ändern kann, liefert b._replace(hertz=144) ein
neues mit einem anderen Wert; b._asdict() macht ein Dictionary daraus,
Bildschirm._fields ist ("modell", "zoll", "hertz"). Der Unterstrich
heißt hier nicht „privat“, er hält nur die Namen der Felder frei. Gegen
eine Datenklasse mit frozen=True (Aufgabe 4_014) ist ein benanntes Tupel
kleiner und überall dort einsetzbar, wo ein Tupel erwartet wird; dafür
ist es auch gleich einem gewöhnlichen Tupel mit denselben Werten.
"""

from collections import namedtuple
from typing import NamedTuple

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Stromkreis(NamedTuple):
    """Ein abgesicherter Stromkreis mit Namen, Nennstrom der Sicherung und Spannung."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def lies_verbraucher(zeilen):
    """Macht aus Zeilen der Form name;watt eine Liste von Verbraucher-Tupeln."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auslastung(kreis, verbraucher):
    """Gibt die Auslastung des Stromkreises in Prozent zurück, gerundet auf eine Stelle."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def aufgeruestet(kreis, ampere):
    """Gibt einen neuen Stromkreis mit einer anderen Sicherung zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kreis = Stromkreis("A1", 16)
server = lies_verbraucher(["db-01;450", "web-01;320", "switch-01;90"])
print(server[0], server[0].watt)
print(kreis, kreis.max_watt())
print(auslastung(kreis, server))
print(aufgeruestet(kreis, 32))
