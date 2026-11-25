"""Aufgabe 4_089 – Inventur                                      Stufe 4 ★★★★☆

Die IT-Abteilung eines Krankenhauses hat ein eigenes Lager für
Netzwerk-Hardware: Switches, Access Points, Patchkabel, Transceiver.
Jede Lieferung wird als Zugang gebucht, jede Entnahme für eine Station
als Abgang. Der Bestand im Programm ist damit der Soll-Bestand. Einmal
im Quartal wird gezählt (Inventur), und dabei kommt immer heraus, dass
Soll und Ist nicht ganz zusammenpassen: Ein Kabel wurde ohne Buchung
mitgenommen, ein Karton doppelt gezählt. Die Differenzen werden dann
als Inventurbuchungen ins Journal geschrieben, damit der Bestand wieder
stimmt. Während gezählt wird, darf niemand buchen, sonst vergleicht man
Äpfel mit Birnen.

Dieses kleine Projekt verbindet mehrere Sprachmittel aus Stufe 4.
Vervollständigen Sie:

- die Aufzählung `Buchungsart` mit den Mitgliedern ZUGANG, ABGANG und
  INVENTUR (die Werte dürfen Sie selbst wählen),
- die Datenklasse `Artikel` mit den Feldern nummer, bezeichnung und
  bestand (Standardwert 0), in dieser Reihenfolge,
- die unveränderliche Datenklasse `Buchung` (frozen) mit den Feldern
  nummer, art (eine Buchungsart) und menge, in dieser Reihenfolge;
  menge ist die Änderung des Bestands, also negativ bei einem Abgang.
  Der Dekorator kommt an die Stelle der pass-Zeile direkt über class
  Buchung.
- die Fehlerklassen unter `LagerFehler`: `UnbekannterArtikel(nummer)`
  speichert das Attribut nummer, `BestandZuGering(nummer, bestand,
  menge)` die Attribute nummer, bestand und menge. Beide geben eine
  verständliche Meldung an Exception weiter. `LagerGesperrt` ist
  schon fertig.
- in der Klasse `Lager` (`__init__` und `anlegen` sind vorgegeben):
  - `_artikel(nummer)` gibt den Artikel zurück oder löst
    UnbekannterArtikel aus,
  - `zugang(nummer, menge)` erhöht den Bestand und hängt
    Buchung(nummer, Buchungsart.ZUGANG, menge) an das Journal,
  - `abgang(nummer, menge)` senkt den Bestand und hängt
    Buchung(nummer, Buchungsart.ABGANG, -menge) an; ist menge größer
    als der Bestand, löst sie BestandZuGering aus,
  - beide lösen während einer Inventur LagerGesperrt aus, und bei
    jedem Fehler bleiben Bestand und Journal unverändert,
  - `inventur()` ist ein Kontextmanager. Beim Betreten sperrt er das
    Lager und gibt ein leeres Dictionary zaehlung an den with-Block,
    in das die Zählenden Artikelnummer → gezählte Menge eintragen.
    Endet der Block ohne Fehler, setzt er für jeden gezählten Artikel,
    dessen Ist vom Soll abweicht, den Bestand auf das Ist und bucht
    Buchung(nummer, Buchungsart.INVENTUR, ist - soll), nach
    Artikelnummer sortiert. Nicht gezählte Artikel bleiben, wie sie
    sind. Steht in zaehlung eine unbekannte Nummer, löst er
    UnbekannterArtikel aus und bucht gar nichts. Bricht der Block mit
    einer Ausnahme ab, bucht er ebenfalls nichts, und die Ausnahme
    fliegt weiter. In jedem Fall ist das Lager danach wieder frei.
    Eine zweite Inventur, während eine läuft, löst LagerGesperrt aus.

    lager = Lager()
    lager.anlegen("SW-24", "Switch 24 Ports")
    lager.anlegen("AP-6", "WLAN-Access-Point")
    lager.anlegen("PK-3", "Patchkabel 3 m")
    lager.zugang("SW-24", 10)
    lager.zugang("PK-3", 200)
    lager.abgang("SW-24", 3)
    lager.abgang("AP-6", 1)         →  BestandZuGering (Bestand 0, verlangt 1)
    lager.zugang("FW-1", 2)         →  UnbekannterArtikel
    with lager.inventur() as zaehlung:
        zaehlung["SW-24"] = 6       # Soll 7: einer fehlt
        zaehlung["PK-3"] = 212      # Soll 200: zwölf mehr
        zaehlung["AP-6"] = 0        # Soll 0: stimmt
        lager.zugang("AP-6", 4)     →  LagerGesperrt
    lager.artikel["SW-24"].bestand  →  6
    lager.journal[-2:]
        →  [Buchung(nummer='PK-3', art=<Buchungsart.INVENTUR: …>, menge=12),
            Buchung(nummer='SW-24', art=<Buchungsart.INVENTUR: …>, menge=-1)]

(Im with-Block oben würde die Ausnahme von zugang die Inventur
abbrechen; im Programm unten ist sie deshalb mit try abgefangen.)

Grenzen: Artikelnummern sind nicht leere Texte. Bei zugang und abgang
ist menge eine ganze Zahl von 1 bis 10**6, gezählte Mengen sind ganze
Zahlen von 0 bis 10**6, die Nummern in zaehlung beliebige nicht leere
Texte. Ein Lager hat bis zu 10 000 Artikel und bekommt bis zu 100 000
Buchungen. zugang und abgang sollen O(1) Schritte brauchen, inventur
O(k log k) für k gezählte Artikel.

Hintergrund: Ein kleines Projekt besteht aus mehreren Teilen, die je
eine Aufgabe haben. Bevor man schreibt, legt man sie fest, von innen
nach außen:

- Modell: Was wird gespeichert? Datenklassen (Aufgabe 4_012 und 4_014)
  für die Dinge, eine Aufzählung (Aufgabe 4_015) für feste Arten statt
  Texten, bei denen ein Tippfehler unbemerkt bliebe.
- Fehler: Was kann schiefgehen? Eine eigene Hierarchie (Aufgabe 4_056)
  mit einer gemeinsamen Oberklasse, damit Aufrufer alle Lagerfehler auf
  einmal mit except LagerFehler abfangen können oder einen gezielt.
- Logik: eine Klasse, die das Modell besitzt und ihre Regeln selbst
  durchsetzt, wie das Konto in Aufgabe 4_001: erst alles prüfen, dann
  ändern, damit ein Fehler nichts halb erledigt zurücklässt.
- Abläufe: Was muss am Ende immer passieren? Ein Kontextmanager
  (Aufgaben 4_051 und 4_052) räumt auch bei Ausnahmen auf.

In einem größeren Projekt wäre jeder Teil ein eigenes Modul, und die
Teile importieren nur von innen nach außen; das Modell weiß nichts vom
Lager:

    lagerverwaltung/
        modell.py      # Buchungsart, Artikel, Buchung
        fehler.py      # LagerFehler und Unterklassen
        lager.py       # from modell import Artikel, Buchung, Buchungsart
                       # from fehler import UnbekannterArtikel, …
        main.py        # if __name__ == "__main__": … (Aufgabe 1_049)

Hier steht alles in einer Datei, aber in derselben Reihenfolge. So
sieht das an einem anderen Beispiel aus, der Ausgabe von Leihlaptops:

    class Zustand(Enum):
        FREI = "frei"
        VERLIEHEN = "verliehen"

    @dataclass
    class Laptop:
        inventarnummer: str
        zustand: Zustand = Zustand.FREI

    class AusleihFehler(Exception):
        pass

    class Ausleihe:
        def __init__(self):
            self.laptops = {}

        def verleihen(self, nummer):
            laptop = self.laptops.get(nummer)
            if laptop is None or laptop.zustand is not Zustand.FREI:
                raise AusleihFehler(f"{nummer} ist nicht verfügbar")   # erst prüfen …
            laptop.zustand = Zustand.VERLIEHEN                         # … dann ändern

Für die Inventur braucht der Kontextmanager drei Stellen: was vor dem
Block passiert, was nur nach einem erfolgreichen Block passiert, und
was immer passiert. Mit contextlib.contextmanager (Aufgabe 4_052) und
try/finally sieht das so aus; contextmanager funktioniert auch über
einer Methode, dann bekommt sie wie jede Methode self:

    @contextmanager
    def sammelausgabe(self):
        self.gesperrt = True                # vorher
        liste = []
        try:
            yield liste                     # hier läuft der with-Block
            for nummer in liste:            # nur ohne Ausnahme im Block
                ...
        finally:
            self.gesperrt = False           # immer

Fliegt im with-Block eine Ausnahme, kommt sie an der Stelle des yield
wieder heraus; die Zeilen danach im try laufen dann nicht, finally schon.
Prüfen Sie die ganze zaehlung, bevor Sie den ersten Bestand ändern.
"""

from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum


class Buchungsart(Enum):
    """Die Arten von Buchungen im Lagerjournal."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@dataclass
class Artikel:
    """Ein Artikel im Lager mit seinem Bestand laut Programm (Soll)."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
class Buchung:
    """Ein Eintrag im Lagerjournal; menge ist die Änderung des Bestands."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class LagerFehler(Exception):
    """Oberklasse aller Fehler der Lagerverwaltung."""


class UnbekannterArtikel(LagerFehler):
    """Die Artikelnummer gibt es im Lager nicht."""

    def __init__(self, nummer):
        """Speichert die unbekannte Nummer."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class BestandZuGering(LagerFehler):
    """Ein Abgang will mehr entnehmen, als da ist."""

    def __init__(self, nummer, bestand, menge):
        """Speichert Nummer, vorhandenen Bestand und verlangte Menge."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class LagerGesperrt(LagerFehler):
    """Während einer Inventur darf nicht gebucht werden."""


class Lager:
    """Das Lager: Artikel nach Nummer, ein Journal aller Buchungen und die Sperre für die Inventur."""

    def __init__(self):
        """Legt ein leeres, nicht gesperrtes Lager an."""
        self.artikel = {}
        self.journal = []
        self.gesperrt = False

    def anlegen(self, nummer, bezeichnung):
        """Legt einen neuen Artikel mit Bestand 0 an und gibt ihn zurück."""
        if nummer in self.artikel:
            raise ValueError(f"Den Artikel {nummer} gibt es schon")
        self.artikel[nummer] = Artikel(nummer, bezeichnung)
        return self.artikel[nummer]

    def _artikel(self, nummer):
        """Gibt den Artikel zu nummer zurück; UnbekannterArtikel, wenn es ihn nicht gibt."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def zugang(self, nummer, menge):
        """Bucht einen Zugang von menge Stück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def abgang(self, nummer, menge):
        """Bucht einen Abgang von menge Stück; nie mehr, als da ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    @contextmanager
    def inventur(self):
        """Sperrt das Lager für die Zählung und bucht danach die Differenzen von Soll zu Ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


lager = Lager()
lager.anlegen("SW-24", "Switch 24 Ports")
lager.anlegen("AP-6", "WLAN-Access-Point")
lager.anlegen("PK-3", "Patchkabel 3 m")
lager.zugang("SW-24", 10)
lager.zugang("PK-3", 200)
lager.abgang("SW-24", 3)
try:
    lager.abgang("AP-6", 1)
except LagerFehler as fehler:
    print("Abgelehnt:", fehler)
with lager.inventur() as zaehlung:
    zaehlung["SW-24"] = 6
    zaehlung["PK-3"] = 212
    zaehlung["AP-6"] = 0
    try:
        lager.zugang("AP-6", 4)
    except LagerFehler as fehler:
        print("Abgelehnt:", fehler)
print(lager.artikel["SW-24"].bestand, lager.journal[-2:])
