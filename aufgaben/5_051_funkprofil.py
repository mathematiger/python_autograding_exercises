"""Aufgabe 5_051 – Funkprofil                                    Stufe 5 ★★★★★

Ein Firmengebäude wird mit WLAN ausgeleuchtet: In jedem Flur hängt ein
Accesspoint, ein Funkgerät, über das sich Laptops und Telefone mit dem
Netz verbinden. Das Netzwerkteam verwaltet die Einstellungen jedes
Geräts in einer Datenklasse `Accesspoint`: den Funkkanal (im 2,4-GHz-
Band sind in Europa die Kanäle 1 bis 13 erlaubt), die Sendeleistung in
dBm (eine logarithmische Einheit für Leistung, hier 1 bis 20) und die
höchste Zahl gleichzeitig verbundener Geräte (1 bis 250). Neulich hat
ein Skript kanal=14 eingetragen, ein Wert, der in Japan erlaubt ist,
hier aber nicht; das Gerät hat die ganze Konfiguration abgelehnt, und
ein Stockwerk war eine Stunde ohne Netz.

Jedes dieser Felder soll deshalb bei jeder Zuweisung geprüft werden,
im Konstruktor wie danach, und zwar mit einem einzigen,
wiederverwendbaren Deskriptor `Bereich`, der mit @dataclass
zusammenarbeitet. `__init__` von Bereich ist vorgegeben und speichert
kleinster, groesster und standard. Vervollständigen Sie:

- `erlaubt(self, wert)` gibt True zurück, wenn wert eine ganze Zahl
  (int, nicht bool, nicht 6.0) von kleinster bis groesster
  einschließlich ist, sonst False.
- `__init__`: zusätzlich zum Vorgegebenen prüfen, dass standard, wenn
  er nicht None ist, selbst erlaubt ist; sonst ValueError.
- `__set_name__(self, besitzer, name)` merkt sich den Feldnamen.
- `__set__(self, objekt, wert)` speichert erlaubte Werte im Objekt.
  Sonst löst es einen ValueError aus, dessen Meldung den Feldnamen und
  beide Grenzen nennt; der alte Wert bleibt.
- `__get__(self, objekt, typ=None)` liefert beim Zugriff über ein Objekt
  dessen gespeicherten Wert. Beim Zugriff über die Klasse (objekt ist
  None) liefert es den Standardwert. Hat das Feld keinen Standardwert
  (standard ist None), löst es dort einen AttributeError aus; dann wird
  das Feld für die Datenklasse ein Pflichtfeld.

    ap = Accesspoint("Flur-OG2", 6)
    ap                          →  Accesspoint(name='Flur-OG2', kanal=6,
                                               sendeleistung=17, max_geraete=64)
    ap.kanal = 11               →  in Ordnung
    ap.kanal = 14               →  ValueError: kanal muss von 1 bis 13 gehen, nicht 14
    Accesspoint("Lager", 6, 25) →  ValueError (sendeleistung)
    Accesspoint("Lager")        →  TypeError: kanal fehlt (Pflichtfeld)
    Accesspoint.sendeleistung   →  17
    Bereich(1, 13, standard=14) →  ValueError
    Bereich(1, 13).erlaubt(True) →  False

Grenzen: Für Bereich gilt -10**9 ≤ kleinster ≤ groesster ≤ 10**9, und
standard ist None oder eine ganze Zahl von -10**18 bis 10**18. wert in
__set__ kann eine ganze Zahl von -10**18 bis 10**18, eine Kommazahl,
True oder False, ein Text oder None sein. Eine Klasse hat beliebig viele
Bereich-Felder, und es gibt beliebig viele Objekte.

Hintergrund: In Aufgabe 5_001 haben Sie einen Daten-Deskriptor gebaut:
ein Klassenattribut mit `__get__` und `__set__`, das Python bei jedem
Lesen und Schreiben des Attributs fragt, und in Aufgabe 5_002 gesehen,
dass property genau so arbeitet. @dataclass (Aufgaben 4_012 und 4_014)
schreibt `__init__`, `__repr__` und `__eq__` aus den annotierten
Klassenattributen. Beides lässt sich verbinden, man muss aber wissen, in
welcher Reihenfolge was passiert:

    @dataclass
    class Accesspoint:
        name: str
        kanal: int = Bereich(1, 13)

1. Beim Ausführen des Klassenkörpers entsteht das Objekt Bereich(1, 13)
   und landet als Klassenattribut kanal. Sobald die Klasse fertig ist,
   ruft Python `__set_name__(Accesspoint, "kanal")` auf, noch bevor der
   Dekorator drankommt.
2. @dataclass sucht dann für jedes Feld den Standardwert mit
   getattr(Accesspoint, "kanal"). Weil kanal ein Deskriptor ist, landet
   das in `__get__(None, Accesspoint)`. Was dort zurückkommt, wird der
   Standardwert des Felds. Gibt `__get__` wie in Aufgabe 5_001 bei
   objekt None sich selbst zurück, wird der Deskriptor selbst zum
   Standardwert, und Accesspoint("Lager") versucht, kanal das
   Bereich-Objekt zuzuweisen. Löst `__get__` dort einen AttributeError
   aus, bedeutet das „kein Standardwert“, und das Feld wird ein
   Pflichtfeld wie name.
3. Der erzeugte `__init__` enthält die Zeile `self.kanal = kanal`. Das
   ist eine gewöhnliche Zuweisung, also läuft sie durch `__set__`: Die
   Prüfung gilt im Konstruktor, ohne dass Sie `__post_init__` (Aufgabe
   4_014) schreiben, und genauso bei jeder späteren Zuweisung, die
   `__post_init__` nicht sehen würde. `__repr__` und `__eq__` lesen die
   Felder mit getattr, also über `__get__`.

Ein kleines Beispiel mit einem anderen Deskriptor:

    from dataclasses import dataclass

    class Kennung:
        def __init__(self, standard=None):
            self.standard = standard

        def __set_name__(self, besitzer, name):
            self.name = name
            self.speicher = "_" + name        # z. B. "_hostname"

        def __get__(self, objekt, typ=None):
            if objekt is None:
                if self.standard is None:
                    raise AttributeError(self.name)   # Pflichtfeld
                return self.standard                  # Standardwert
            return getattr(objekt, self.speicher)

        def __set__(self, objekt, wert):
            if not isinstance(wert, str) or wert == "":
                raise ValueError(f"{self.name} muss ein nicht leerer Text sein")
            setattr(objekt, self.speicher, wert)

    @dataclass
    class Router:
        hostname: str = Kennung()
        standort: str = Kennung("Keller")

    Router("rt01")        →  Router(hostname='rt01', standort='Keller')
    Router("")            →  ValueError
    Router()              →  TypeError: missing ... 'hostname'

`__set_name__` liefert zwei Dinge: den Namen für verständliche Meldungen
und einen Speicherort. Hier liegt der Wert unter "_hostname" im Objekt,
damit vars(r) und der Feldname nicht durcheinanderkommen; den Wert unter
demselben Namen in `objekt.__dict__` abzulegen wie in Aufgabe 5_001 geht
ebenso, weil ein Daten-Deskriptor beim Lesen vor dem `__dict__` gefragt
wird. Nur im Deskriptor selbst darf der Wert nie liegen: Es gibt ein
Bereich-Objekt pro Feld, aber viele Accesspoints. Und Achtung bei
setattr(objekt, self.name, wert) mit dem Feldnamen selbst: Das ruft
wieder `__set__` auf, endlos.

Der Preis der Lösung: Accesspoint.sendeleistung liefert jetzt den
Standardwert 17 statt des Deskriptors. Wer den Deskriptor selbst
braucht, findet ihn mit vars(Accesspoint)["sendeleistung"].
"""

from dataclasses import dataclass


class Bereich:
    """Deskriptor für ein ganzzahliges Feld einer Datenklasse mit erlaubtem Bereich."""

    def __init__(self, kleinster, groesster, standard=None):
        """Merkt sich die Grenzen und den Standardwert (None: Pflichtfeld)."""
        self.kleinster = kleinster
        self.groesster = groesster
        self.standard = standard
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def erlaubt(self, wert):
        """Prüft, ob wert eine ganze Zahl (kein bool) im Bereich ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __set_name__(self, besitzer, name):
        """Merkt sich den Feldnamen."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __get__(self, objekt, typ=None):
        """Liefert den Wert im Objekt, über die Klasse den Standardwert."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __set__(self, objekt, wert):
        """Speichert wert im Objekt, wenn er erlaubt ist, sonst ValueError."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@dataclass
class Accesspoint:
    """Einstellungen eines WLAN-Accesspoints."""

    name: str
    kanal: int = Bereich(1, 13)
    sendeleistung: int = Bereich(1, 20, standard=17)
    max_geraete: int = Bereich(1, 250, standard=64)


ap = Accesspoint("Flur-OG2", 6)
print(ap)
