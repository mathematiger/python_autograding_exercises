"""Aufgabe 5_017 – Lizenzinventar                                Stufe 5 ★★★★★

Die IT-Abteilung eines Unternehmens soll für die Budgetplanung die
jährlichen Lizenzkosten der gesamten Software berechnen. Das Inventar
ist eine Liste von Objekten aus verschiedenen Modulen: Abos, Kauflizenzen
mit Wartungsvertrag, freie Software. Die Klassen stammen teils von
Herstellern und dürfen nicht geändert werden; keine von ihnen erbt von
einer gemeinsamen Basisklasse. Gemeinsam ist den kostenpflichtigen nur,
dass sie eine Methode jahreskosten() haben. Statt sie alle umzubauen,
sollen zwei abstrakte Basisklassen sie von außen einordnen:
`Lizenzpflichtig` erkennt eine Klasse an ihrer Methode, `Kostenlos`
bekommt ihre Klassen ausdrücklich zugewiesen. Vervollständigen Sie:

- `Lizenzpflichtig.__subclasshook__(cls, unterklasse)`: Wird der Hook
  für Lizenzpflichtig selbst gefragt (nicht für eine Unterklasse davon),
  sucht er in den Klassen von unterklasse.__mro__ der Reihe nach den
  Namen jahreskosten in ihrem __dict__. Beim ersten Fund gibt er False
  zurück, wenn dort None steht, sonst True. Wird der Name nirgends
  gefunden, oder wird der Hook für eine Unterklasse von Lizenzpflichtig
  gefragt, gibt er NotImplemented zurück.
- `kostenlos(klasse)`: ein Klassendekorator, der klasse als virtuelle
  Unterklasse von Kostenlos einträgt und klasse zurückgibt.
- `einordnen(objekt)` gibt "lizenzpflichtig" zurück, wenn objekt eine
  Instanz von Lizenzpflichtig ist, sonst "kostenlos", wenn es eine
  Instanz von Kostenlos ist, sonst "unbekannt".
- `gesamtkosten(inventar)` gibt die Summe von jahreskosten() aller
  lizenzpflichtigen Objekte zurück. Kostenlose zählen nicht. Ist ein
  Objekt unbekannt, löst die Funktion einen TypeError aus, denn dann
  wäre die Summe unvollständig.

    inventar = [OfficeAbo(25, 120), ServerLizenz(8000, 20), FreiesOffice()]
    [einordnen(objekt) for objekt in inventar]
        →  ["lizenzpflichtig", "lizenzpflichtig", "kostenlos"]
    gesamtkosten(inventar)               →  4600    (25 · 120 + 20 % von 8000)
    issubclass(OfficeAbo, Lizenzpflichtig)    →  True
    einordnen(Testversion(5, 120))       →  "kostenlos"   (jahreskosten = None)
    gesamtkosten([Notiz("Einkauf")])     →  TypeError

Grenzen: inventar hat 0 bis 10 000 Objekte beliebiger Klassen.
jahreskosten() liefert eine ganze Zahl von 0 bis 10**7. Kostenlos und
Lizenzpflichtig zugleich wird keine Klasse. Gezählt werden nur
Lizenzgebühren: „kostenlos“ heißt hier ohne Lizenzgebühr. Support für
freie Software oder das Abo, in das eine Testversion meist übergeht,
gehören nicht in diese Rechnung.

Hintergrund: Mit abc.ABC und @abstractmethod (Aufgabe 4_011) erzwingt
man eine Schnittstelle bei Klassen, die von der abstrakten Basisklasse
erben. Oft kann man aber fremde Klassen nicht ändern, und trotzdem soll
isinstance(objekt, Basis) die Frage „passt das Objekt zu dieser
Schnittstelle?“ beantworten. Dafür kennt die Metaklasse ABCMeta (die
hinter ABC steckt, vergleiche Aufgabe 5_013) zwei Wege zu virtuellen
Unterklassen: Klassen, die issubclass und isinstance als Unterklasse
gelten lassen, obwohl sie nicht erben und nicht in __mro__ stehen.

Der erste Weg ist register. Basis.register(Klasse) trägt Klasse von
Hand ein und gibt sie zurück; deshalb kann man register auch direkt als
Klassendekorator schreiben. Ein Klassendekorator funktioniert wie die
Funktionsdekoratoren aus Aufgabe 4_022, nur über einer class-Anweisung:
@deko über class K: bedeutet K = deko(K). Was deko zurückgibt, steht
danach unter dem Namen K; darum muss ein Klassendekorator die Klasse
zurückgeben. Geprüft wird bei register nichts, es ist ein Versprechen
des Programmierers:

    class Druckbar(ABC):
        pass

    Druckbar.register(tuple)
    isinstance((1, 2), Druckbar)   →  True
    Druckbar in tuple.__mro__      →  False    (virtuell, nicht geerbt)

    @Druckbar.register             # dasselbe wie Beleg = Druckbar.register(Beleg)
    class Beleg:
        pass

Der zweite Weg ist der Klassenmethoden-Hook __subclasshook__. Bei
issubclass(K, Basis) fragt ABCMeta zuerst Basis.__subclasshook__(K).
True heißt „ja, Unterklasse“, False heißt „nein“, und zwar endgültig,
auch wenn K erbt oder registriert ist. NotImplemented heißt „ich weiß
es nicht“; dann entscheidet ABCMeta wie sonst über Vererbung und
register. So arbeiten die Klassen in collections.abc: Jede Klasse mit
__len__ gilt als collections.abc.Sized, ohne davon zu erben.

    class HatLaenge(ABC):
        @classmethod
        def __subclasshook__(cls, unterklasse):
            if cls is not HatLaenge:
                return NotImplemented
            for klasse in unterklasse.__mro__:
                if "__len__" in klasse.__dict__:
                    return klasse.__dict__["__len__"] is not None
            return NotImplemented

    issubclass(list, HatLaenge)    →  True
    issubclass(int, HatLaenge)     →  False

Drei Feinheiten. Erstens sucht man im __dict__ der Klassen der __mro__
statt mit hasattr: Geerbte Methoden sollen zählen, aber ein None, das
eine Unterklasse einträgt, schaltet die Methode ausdrücklich ab (so
macht es Python selbst mit __hash__ = None). hasattr fände auch dieses
None und hielte die Methode für vorhanden; der Gang durch die __mro__
findet den ersten Eintrag und erkennt das None. Zweitens
wird der Hook an Unterklassen von HatLaenge vererbt; ohne die Abfrage
cls is not HatLaenge würde jede Unterklasse jede Klasse mit __len__ als
ihre Unterklasse ansehen. Drittens merkt sich ABCMeta die Antworten in
einem Cache; register macht ihn ungültig, darum darf man auch nach
einer ersten Abfrage noch registrieren.
"""

from abc import ABC, abstractmethod


class Lizenzpflichtig(ABC):
    """Alles, was jährliche Lizenzkosten verursacht; erkannt an der Methode jahreskosten."""

    @abstractmethod
    def jahreskosten(self):
        """Gibt die Lizenzkosten pro Jahr in Euro zurück."""

    @classmethod
    def __subclasshook__(cls, unterklasse):
        """Erkennt Klassen mit einer Methode jahreskosten als virtuelle Unterklassen."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Kostenlos(ABC):
    """Markierung für Software ohne Lizenzkosten; die Klassen werden mit register eingetragen."""


def kostenlos(klasse):
    """Klassendekorator: trägt klasse als virtuelle Unterklasse von Kostenlos ein und gibt sie zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def einordnen(objekt):
    """Gibt "lizenzpflichtig", "kostenlos" oder "unbekannt" zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gesamtkosten(inventar):
    """Summiert die Jahreskosten aller lizenzpflichtigen Objekte; TypeError bei unbekannten Objekten."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


# --- Klassen der Hersteller und anderer Module; sie dürfen nicht geändert werden ---


class OfficeAbo:
    """Abo mit festem Preis pro Arbeitsplatz und Jahr."""

    def __init__(self, plaetze, preis_pro_platz):
        self.plaetze = plaetze
        self.preis_pro_platz = preis_pro_platz

    def jahreskosten(self):
        """Gibt plaetze mal preis_pro_platz zurück."""
        return self.plaetze * self.preis_pro_platz


class ServerLizenz:
    """Einmal gekaufte Lizenz; jährlich kostet nur der Wartungsvertrag, ein Prozentsatz des Kaufpreises."""

    def __init__(self, kaufpreis, wartung_prozent):
        self.kaufpreis = kaufpreis
        self.wartung_prozent = wartung_prozent

    def jahreskosten(self):
        """Gibt die jährliche Wartungsgebühr zurück."""
        return self.kaufpreis * self.wartung_prozent // 100


class Testversion(OfficeAbo):
    """Abo in der kostenlosen Testphase; jahreskosten ist ausdrücklich abgeschaltet."""

    jahreskosten = None


class FreiesOffice:
    """Freie Bürosoftware ohne Lizenzkosten."""


class Notiz:
    """Ein Objekt, das nichts mit Software zu tun hat."""

    def __init__(self, text):
        self.text = text


kostenlos(FreiesOffice)
kostenlos(Testversion)

inventar = [OfficeAbo(25, 120), ServerLizenz(8000, 20), FreiesOffice()]
print([einordnen(objekt) for objekt in inventar])
print(gesamtkosten(inventar))
