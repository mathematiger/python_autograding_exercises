"""Aufgabe 4_009 – Kaufen oder leasen                            Stufe 4 ★★★★☆

Eine Firma braucht neue Laptops für ihre Beschäftigten und holt Angebote
ein. Manche Händler verkaufen die Geräte: Man zahlt einmal den Kaufpreis
und danach jedes Jahr für einen Wartungsvertrag. Andere verleasen sie: Man
zahlt eine feste monatliche Rate und am Ende eine Abschlusszahlung, wenn
man die Geräte zurückgibt. Um die Angebote vergleichen zu können, rechnet
die IT-Abteilung die Gesamtkosten über die geplante Nutzungsdauer aus.

Die Basisklasse `Beschaffung` ist vorgegeben. Sie speichert Bezeichnung
und Laufzeit in Monaten, prüft die Laufzeit und bietet `monatlich()` und
`__str__()`; beide rufen `self.gesamtkosten()` auf, das jede Unterklasse
selbst festlegen muss. Vervollständigen Sie:

- `Kauf(bezeichnung, laufzeit_monate, kaufpreis, wartung_pro_jahr)`:
  `__init__` überlässt Bezeichnung und Laufzeit mit super() der
  Basisklasse und speichert `kaufpreis` und `wartung_pro_jahr`.
  `gesamtkosten()` ist der Kaufpreis plus die Wartung für die Laufzeit,
  anteilig nach Monaten (wartung_pro_jahr / 12 pro Monat).
- `Leasing(bezeichnung, laufzeit_monate, rate, abschlusszahlung=0)`:
  genauso mit `rate` und `abschlusszahlung`. `gesamtkosten()` ist die
  Rate mal die Laufzeit plus die Abschlusszahlung.
- Die Funktion `guenstigste(angebote)` bekommt eine nicht leere Liste
  beliebiger Beschaffungen und gibt die mit den kleinsten Gesamtkosten
  zurück; bei Gleichstand die erste.

Beide `gesamtkosten()` runden auf zwei Nachkommastellen.

    kauf = Kauf("Laptop A", 36, 1200, 100)
    leasing = Leasing("Laptop B", 36, 38, 50)
    kauf.gesamtkosten()         →  1500.0
    leasing.gesamtkosten()      →  1418
    print(leasing)              →  Laptop B (Leasing): 1418.00 Euro, 39.39 Euro im Monat
    guenstigste([kauf, leasing]) is leasing   →  True

Grenzen: `laufzeit_monate` ist eine ganze Zahl mit -1000 ≤ laufzeit_monate
≤ 600; Werte <= 0 lehnt die Basisklasse mit einem ValueError ab.
`kaufpreis`, `wartung_pro_jahr`, `rate` und `abschlusszahlung` sind ganze
Zahlen oder Kommazahlen mit 0 ≤ wert ≤ 10**6. `angebote` ist eine Liste mit
1 ≤ len(angebote) ≤ 1000 Objekten beliebiger Unterklassen von Beschaffung.

Hintergrund: Eine Unterklasse erbt alle Attribute und Methoden ihrer
Basisklasse und kann einzelne davon neu schreiben (überschreiben). Damit
die Basisklasse ihre Arbeit im Konstruktor trotzdem erledigt, ruft der
Konstruktor der Unterklasse sie mit super() auf:

    class Fahrzeug:
        def __init__(self, kennzeichen):
            self.kennzeichen = kennzeichen

        def beschreibung(self):
            return f"{self.kennzeichen}: {self.raeder()} Räder"

    class Motorrad(Fahrzeug):
        def __init__(self, kennzeichen, hubraum):
            super().__init__(kennzeichen)
            self.hubraum = hubraum

        def raeder(self):
            return 2

super() liefert die Basisklasse, gebunden an das aktuelle Objekt; so
setzt Fahrzeug.__init__ das Kennzeichen und prüft es gegebenenfalls, ohne
dass Motorrad diesen Code kopieren muss. Bemerkenswert ist beschreibung:
Sie steht in Fahrzeug, ruft aber self.raeder() auf, und welches raeder
dabei läuft, entscheidet sich erst beim Aufruf am tatsächlichen Objekt.
Bei einem Motorrad ist es Motorrad.raeder, bei einem Auto Auto.raeder.
Das heißt Polymorphie (Vielgestaltigkeit): Verschiedene Klassen bieten
dieselbe Schnittstelle, hier die Methode raeder, und Code, der nur diese
Schnittstelle benutzt, funktioniert mit allen, auch mit Klassen, die erst
später geschrieben werden. Eine Funktion wie guenstigste braucht deshalb
kein if isinstance(...): Sie ruft einfach gesamtkosten() auf, und jedes
Angebot rechnet auf seine Weise. Die Basisklasse löst in ihrer eigenen
gesamtkosten einen NotImplementedError aus; so fällt sofort auf, wenn
eine Unterklasse vergessen hat, die Methode zu überschreiben.

Tipp: Bei 7 Monaten und 100 Euro Wartung im Jahr fallen 58.33 Euro
Wartung an.
"""


class Beschaffung:
    """Ein Angebot für eine Anschaffung mit Bezeichnung und Laufzeit in Monaten."""

    def __init__(self, bezeichnung, laufzeit_monate):
        """Speichert Bezeichnung und Laufzeit; die Laufzeit muss positiv sein."""
        if laufzeit_monate <= 0:
            raise ValueError("Die Laufzeit muss positiv sein")
        self.bezeichnung = bezeichnung
        self.laufzeit_monate = laufzeit_monate

    def gesamtkosten(self):
        """Gibt die Kosten über die ganze Laufzeit zurück; jede Unterklasse legt sie fest."""
        raise NotImplementedError("Unterklassen müssen gesamtkosten() festlegen")

    def monatlich(self):
        """Gibt die Gesamtkosten pro Monat zurück, auf Cent gerundet."""
        return round(self.gesamtkosten() / self.laufzeit_monate, 2)

    def __str__(self):
        """Liefert z. B. Laptop B (Leasing): 1418.00 Euro, 39.39 Euro im Monat."""
        art = type(self).__name__
        return f"{self.bezeichnung} ({art}): {self.gesamtkosten():.2f} Euro, {self.monatlich():.2f} Euro im Monat"


class Kauf(Beschaffung):
    """Ein Kaufangebot mit Kaufpreis und jährlicher Wartung."""

    def __init__(self, bezeichnung, laufzeit_monate, kaufpreis, wartung_pro_jahr):
        """Speichert alle Angaben; Bezeichnung und Laufzeit über die Basisklasse."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def gesamtkosten(self):
        """Gibt Kaufpreis plus anteilige Wartung über die Laufzeit zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Leasing(Beschaffung):
    """Ein Leasingangebot mit monatlicher Rate und Abschlusszahlung."""

    def __init__(self, bezeichnung, laufzeit_monate, rate, abschlusszahlung=0):
        """Speichert alle Angaben; Bezeichnung und Laufzeit über die Basisklasse."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def gesamtkosten(self):
        """Gibt alle Raten plus die Abschlusszahlung zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def guenstigste(angebote):
    """Gibt das Angebot mit den kleinsten Gesamtkosten zurück, bei Gleichstand das erste."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kauf = Kauf("Laptop A", 36, 1200, 100)
leasing = Leasing("Laptop B", 36, 38, 50)
print(kauf)
print(leasing)
print("Günstigstes Angebot:", guenstigste([kauf, leasing]).bezeichnung)
