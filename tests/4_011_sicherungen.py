# Automatisch erzeugt aus lehrkraft/muster/4_011_sicherungen.py - nicht von Hand ändern.
# vorlage-hash: 54a23f53c957197e
# text-hash: 8261aa0d733a36c5
# thema: klassen
# inhalt: `abc.ABC` und `@abstractmethod`

# Das Beispiel aus der Aufgabe
web = Vollsicherung("web01", 40)
db = InkrementelleSicherung("db01", 500, 20)
ergebnis = (web.speicherbedarf(7), db.speicherbedarf(7), gesamtbedarf([web, db], 7))
assert ergebnis == (280, 620, 900), (
    f"Für web01 (Vollsicherung, 40 GB) und db01 (inkrementell, 500 GB, 20 GB Änderung) ergeben speicherbedarf(7) "
    f"und gesamtbedarf {ergebnis!r}, erwartet war (280, 620, 900)."
)

# Eine Sicherung direkt anzulegen, ist verboten
try:
    Sicherung("alt", 10)
    fehler = None
except TypeError as ausnahme:
    fehler = ausnahme
assert fehler is not None, (
    'Sicherung("alt", 10) muss einen TypeError auslösen, weil Sicherung abstrakt ist.\n'
    "Tipp: Markieren Sie speicherbedarf in Sicherung mit @abstractmethod."
)

# speicherbedarf ist in Sicherung abstrakt
assert getattr(Sicherung.__dict__.get("speicherbedarf"), "__isabstractmethod__", False), (
    "Sicherung braucht eine Methode speicherbedarf(self, tage) mit dem Dekorator @abstractmethod."
)

# speicherbedarf ist die einzige abstrakte Methode von Sicherung
assert set(Sicherung.__abstractmethods__) == {"speicherbedarf"}, (
    f"Abstrakt sollen in Sicherung nur speicherbedarf sein, gefunden: {sorted(Sicherung.__abstractmethods__)}."
)


# Eine Unterklasse ohne speicherbedarf lässt sich nicht anlegen
class Spiegelung(Sicherung):
    """Eine Unterklasse, die speicherbedarf vergessen hat."""

    def bericht(self, tage):
        """Überschreibt nur bericht."""
        return "Spiegelung"


try:
    Spiegelung("san01", 100)
    fehler = None
except TypeError as ausnahme:
    fehler = ausnahme
assert fehler is not None, (
    'Eine Unterklasse von Sicherung ohne speicherbedarf muss beim Anlegen einen TypeError auslösen; Spiegelung("san01", '
    "100) hat aber geklappt.\nTipp: Das erledigt Python selbst, wenn speicherbedarf in Sicherung mit @abstractmethod "
    "markiert ist."
)


# Eine neue Unterklasse mit speicherbedarf funktioniert sofort, auch mit bericht
class DifferenzielleSicherung(Sicherung):
    """Jeden Tag alle Änderungen seit der Vollsicherung."""

    def __init__(self, system, daten_gb, aenderung_gb):
        """Speichert zusätzlich die tägliche Änderung."""
        super().__init__(system, daten_gb)
        self.aenderung_gb = aenderung_gb

    def speicherbedarf(self, tage):
        """Eine volle Kopie plus 1, 2, …, tage - 1 Änderungen."""
        return self.daten_gb + self.aenderung_gb * (tage - 1) * tage // 2


diff = DifferenzielleSicherung("mail01", 100, 10)
ergebnis = (diff.bericht(4), gesamtbedarf([diff, Vollsicherung("x", 1)], 4))
assert ergebnis == ("mail01: 160 GB für 4 Tage", 164), (
    f"Eine eigene Unterklasse DifferenzielleSicherung(\"mail01\", 100, 10) ergibt mit bericht(4) und gesamtbedarf "
    f"{ergebnis!r}, erwartet war ('mail01: 160 GB für 4 Tage', 164).\n"
    "Tipp: gesamtbedarf ruft für jede Sicherung deren eigenes speicherbedarf auf."
)

# Weitere Werte, auch ein einziger Tag (nicht fest hinschreiben!)
for sicherung, tage, erwartet in [
    (Vollsicherung("a", 40), 1, 40),
    (Vollsicherung("a", 25), 30, 750),
    (InkrementelleSicherung("b", 500, 20), 1, 500),
    (InkrementelleSicherung("b", 300, 7), 2, 307),
    (InkrementelleSicherung("b", 300, 7), 30, 503),
]:
    ergebnis = sicherung.speicherbedarf(tage)
    art = type(sicherung).__name__
    assert ergebnis == erwartet, (
        f"{art} mit {sicherung.daten_gb} GB ergibt speicherbedarf({tage}) = {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Inkrementell ist es eine volle Kopie und eine Änderung für jeden Tag nach dem ersten."
    )

# Datenmenge oder Änderung 0
for sicherung, erwartet in [
    (Vollsicherung("a", 0), 0),
    (InkrementelleSicherung("b", 0, 5), 45),
    (InkrementelleSicherung("b", 80, 0), 80),
]:
    ergebnis = sicherung.speicherbedarf(10)
    assert ergebnis == erwartet, (
        f"{type(sicherung).__name__} mit {sicherung.daten_gb} GB ergibt speicherbedarf(10) = {ergebnis!r}, erwartet war {erwartet}."
    )

# Eine leere Liste braucht keinen Platz
ergebnis = gesamtbedarf([], 7)
assert ergebnis == 0, f"gesamtbedarf([], 7) ergibt {ergebnis!r}, erwartet war 0."

# Viele zufällige, gemischte Listen
zufall = Zufall(4011)
for _ in range(300):
    sicherungen = []
    tage = zufall.choice([1, 2, zufall.randint(1, 3650)])
    erwartet = 0
    for _ in range(zufall.randint(0, 8)):
        daten = zufall.randint(0, 10**6)
        if zufall.random() < 0.5:
            sicherungen.append(Vollsicherung("v", daten))
            erwartet += daten * tage
        else:
            aenderung = zufall.randint(0, daten)
            sicherungen.append(InkrementelleSicherung("i", daten, aenderung))
            erwartet += daten + aenderung * (tage - 1)
    ergebnis = gesamtbedarf(sicherungen, tage)
    beschreibung = ", ".join(
        f"Vollsicherung({s.daten_gb})" if isinstance(s, Vollsicherung)
        else f"Inkrementell({s.daten_gb}, {s.aenderung_gb})"
        for s in sicherungen
    )
    assert ergebnis == erwartet, (
        f"gesamtbedarf([{beschreibung}], {tage}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    )

# An der oberen Grenze: 100 000 Sicherungen mit 10**6 GB über 3650 Tage
sicherungen = [Vollsicherung("v", 10**6), InkrementelleSicherung("i", 10**6, 10**6)] * 50000
ergebnis = gesamtbedarf(sicherungen, 3650)
erwartet = 50000 * (10**6 * 3650 + 10**6 * 3650)
assert ergebnis == erwartet, (
    f"Für je 50 000 Voll- und inkrementelle Sicherungen mit 10**6 GB ergibt gesamtbedarf(…, 3650) {ergebnis!r}, "
    f"erwartet war {erwartet}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "web01: 280 GB für 7 Tage\ndb01: 620 GB für 7 Tage\nZusammen: 900 GB"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
