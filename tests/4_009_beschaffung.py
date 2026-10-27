# Automatisch erzeugt aus lehrkraft/muster/4_009_beschaffung.py - nicht von Hand ändern.
# vorlage-hash: 19fa58455005fcca

# Ein Kauf speichert seine Angaben, Bezeichnung und Laufzeit über die Basisklasse
k = Kauf("Monitor", 24, 300, 60)
angaben = tuple(getattr(k, name, None) for name in ["bezeichnung", "laufzeit_monate", "kaufpreis", "wartung_pro_jahr"])
assert angaben == ("Monitor", 24, 300, 60), (
    f'Kauf("Monitor", 24, 300, 60) hat bezeichnung, laufzeit_monate, kaufpreis, wartung_pro_jahr = {angaben!r}, '
    'erwartet waren ("Monitor", 24, 300, 60).'
)

# Gesamtkosten eines Kaufs (nicht fest hinschreiben!)
for argumente, erwartet in [
    (("Laptop A", 36, 1200, 100), 1500.0),
    (("Monitor", 24, 300, 60), 420.0),
    (("Drucker", 7, 1000, 100), 1058.33),
    (("Server", 12, 5000, 0), 5000.0),
]:
    ergebnis = Kauf(*argumente).gesamtkosten()
    assert ergebnis == erwartet, (
        f"Kauf{argumente}.gesamtkosten() ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Kaufpreis + wartung_pro_jahr * laufzeit_monate / 12, auf zwei Nachkommastellen gerundet."
    )

# Ein Leasing speichert seine Angaben; die Abschlusszahlung ist ohne Angabe 0
l = Leasing("Laptop B", 36, 38)
angaben = tuple(getattr(l, name, None) for name in ["bezeichnung", "laufzeit_monate", "rate", "abschlusszahlung"])
assert angaben == ("Laptop B", 36, 38, 0), (
    f'Leasing("Laptop B", 36, 38) hat bezeichnung, laufzeit_monate, rate, abschlusszahlung = {angaben!r}, '
    'erwartet waren ("Laptop B", 36, 38, 0).'
)

# Gesamtkosten eines Leasings
for argumente, erwartet in [
    (("Laptop B", 36, 38, 50), 1418),
    (("Laptop B", 36, 38), 1368),
    (("Tablet", 24, 19.99, 10), 489.76),
    (("Kopierer", 60, 85, 250), 5350),
    (("Software", 3, 33.333), 100.0),
]:
    ergebnis = Leasing(*argumente).gesamtkosten()
    assert ergebnis == erwartet, (
        f"Leasing{argumente}.gesamtkosten() ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: rate * laufzeit_monate + abschlusszahlung, auf zwei Nachkommastellen gerundet."
    )

# Beide sind Beschaffungen
assert isinstance(Kauf("x", 12, 1, 1), Beschaffung) and isinstance(Leasing("x", 12, 1), Beschaffung), (
    "Kauf und Leasing müssen Unterklassen von Beschaffung sein."
)

# Die Basisklasse prüft die Laufzeit, also wird sie über super() aufgerufen
for klasse, argumente in [(Kauf, ("x", 0, 100, 10)), (Leasing, ("x", -3, 20))]:
    try:
        klasse(*argumente)
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    assert fehler is not None, (
        f"{klasse.__name__}{argumente} muss einen ValueError auslösen, weil die Laufzeit nicht positiv ist.\n"
        "Tipp: Rufen Sie in __init__ mit super().__init__(bezeichnung, laufzeit_monate) die Basisklasse auf; "
        "sie prüft die Laufzeit."
    )

# super() wird benutzt
assert verwendet("super"), "Rufen Sie den Konstruktor der Basisklasse mit super().__init__(...) auf."

# monatlich und __str__ der Basisklasse funktionieren mit beiden Unterklassen
for angebot, erwartet in [
    (Kauf("Laptop A", 36, 1200, 100), "Laptop A (Kauf): 1500.00 Euro, 41.67 Euro im Monat"),
    (Leasing("Laptop B", 36, 38, 50), "Laptop B (Leasing): 1418.00 Euro, 39.39 Euro im Monat"),
]:
    assert str(angebot) == erwartet, f"str(...) ergibt {str(angebot)!r}, erwartet war {erwartet!r}."

# guenstigste wählt das Angebot mit den kleinsten Gesamtkosten
a = Kauf("A", 36, 1200, 100)
b = Leasing("B", 36, 38, 50)
c = Leasing("C", 36, 45)
d = Kauf("D", 36, 1300, 20)
for angebote, erwartet in [([a, b], b), ([b, a], b), ([a, c, d], d), ([c], c), ([a, b, c, d], d)]:
    ergebnis = guenstigste(angebote)
    namen = [angebot.bezeichnung for angebot in angebote]
    assert ergebnis is erwartet, (
        f"guenstigste(...) für die Angebote {namen} ergibt {getattr(ergebnis, 'bezeichnung', ergebnis)!r}, "
        f"erwartet war {erwartet.bezeichnung!r} mit {erwartet.gesamtkosten()} Euro."
    )

# Bei Gleichstand gewinnt das erste Angebot
e = Kauf("E", 12, 1000, 0)
f = Leasing("F", 10, 100)
ergebnis = guenstigste([e, f])
assert ergebnis is e, (
    f"Bei gleichen Gesamtkosten ergibt guenstigste([E, F]) {getattr(ergebnis, 'bezeichnung', ergebnis)!r}, "
    "erwartet war das erste Angebot 'E'.\nTipp: Ersetzen Sie das bisher beste nur bei echt kleineren Kosten."
)

# Auch in umgekehrter Reihenfolge gewinnt bei Gleichstand das erste Angebot
ergebnis = guenstigste([f, e])
assert ergebnis is f, (
    f"Bei gleichen Gesamtkosten ergibt guenstigste([F, E]) {getattr(ergebnis, 'bezeichnung', ergebnis)!r}, "
    "erwartet war das erste Angebot 'F'."
)


class Miete(Beschaffung):
    """Ein Mietangebot, das in der Aufgabe nicht vorkommt: fester Preis pro Monat."""

    def __init__(self, bezeichnung, laufzeit_monate, miete):
        """Speichert alle Angaben; Bezeichnung und Laufzeit über die Basisklasse."""
        super().__init__(bezeichnung, laufzeit_monate)
        self.miete = miete

    def gesamtkosten(self):
        """Gibt die Miete über die ganze Laufzeit zurück."""
        return self.miete * self.laufzeit_monate


# guenstigste funktioniert auch mit einer neuen Unterklasse
m = Miete("M", 36, 30)
ergebnis = guenstigste([a, m, b])
assert ergebnis is m, (
    f"guenstigste([A, M, B]) mit einem Mietangebot M für 1080 Euro ergibt {getattr(ergebnis, 'bezeichnung', ergebnis)!r}, "
    "erwartet war 'M'.\nTipp: Benutzen Sie nur gesamtkosten(), nicht isinstance oder Attribute einzelner Unterklassen."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "Laptop A (Kauf): 1500.00 Euro, 41.67 Euro im Monat\n"
    "Laptop B (Leasing): 1418.00 Euro, 39.39 Euro im Monat\n"
    "Günstigstes Angebot: Laptop B"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
