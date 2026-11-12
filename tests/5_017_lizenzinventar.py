# Automatisch erzeugt aus lehrkraft/muster/5_017_lizenzinventar.py - nicht von Hand ändern.
# vorlage-hash: 91a1198868bbc2d5
# text-hash: 2316d260237d53f5
# thema: klassen
# inhalt: virtuelle Unterklassen

# Klassen mit jahreskosten gelten als Lizenzpflichtig, ohne zu erben
ergebnis = (issubclass(OfficeAbo, Lizenzpflichtig), issubclass(ServerLizenz, Lizenzpflichtig),
            isinstance(OfficeAbo(1, 1), Lizenzpflichtig))
assert ergebnis == (True, True, True), (
    "issubclass(OfficeAbo, Lizenzpflichtig), issubclass(ServerLizenz, Lizenzpflichtig) und "
    f"isinstance(OfficeAbo(1, 1), Lizenzpflichtig) ergeben {ergebnis!r}, erwartet war (True, True, True).\n"
    'Tipp: Suchen Sie in __subclasshook__ in jeder Klasse von unterklasse.__mro__ nach "jahreskosten" in '
    "klasse.__dict__ und geben Sie beim Fund True zurück."
)

# Klassen ohne jahreskosten sind keine Unterklassen
ergebnis = (issubclass(Notiz, Lizenzpflichtig), issubclass(int, Lizenzpflichtig), issubclass(FreiesOffice, Lizenzpflichtig))
assert ergebnis == (False, False, False), (
    "issubclass(Notiz, …), issubclass(int, …) und issubclass(FreiesOffice, Lizenzpflichtig) ergeben "
    f"{ergebnis!r}, erwartet war (False, False, False)."
)

# jahreskosten = None schaltet die Methode ab, auch wenn die Basisklasse sie hat
ergebnis = issubclass(Testversion, Lizenzpflichtig)
assert ergebnis is False, (
    f"issubclass(Testversion, Lizenzpflichtig) ergibt {ergebnis!r}, erwartet war False.\n"
    "Tipp: Testversion setzt jahreskosten = None. Nehmen Sie den ersten Fund in der __mro__ und geben Sie False "
    "zurück, wenn dort None steht; hasattr würde das None nicht bemerken."
)


# Eine geerbte Methode zählt
class Mehrjahresabo(OfficeAbo):
    """Erbt jahreskosten von OfficeAbo."""


ergebnis = issubclass(Mehrjahresabo, Lizenzpflichtig)
assert ergebnis is True, (
    f"issubclass(Mehrjahresabo, Lizenzpflichtig) ergibt {ergebnis!r}, erwartet war True "
    "(jahreskosten ist von OfficeAbo geerbt).\nTipp: Sehen Sie alle Klassen in unterklasse.__mro__ an, nicht nur "
    "unterklasse.__dict__."
)


# Der Hook gilt nur für Lizenzpflichtig selbst, nicht für echte Unterklassen davon
class Cloudspeicher(Lizenzpflichtig):
    """Echte Unterklasse von Lizenzpflichtig."""

    def jahreskosten(self):
        """Gibt einen festen Betrag zurück."""
        return 600


ergebnis = (issubclass(OfficeAbo, Cloudspeicher), issubclass(Cloudspeicher, Lizenzpflichtig),
            isinstance(Cloudspeicher(), Lizenzpflichtig))
assert ergebnis == (False, True, True), (
    "issubclass(OfficeAbo, Cloudspeicher), issubclass(Cloudspeicher, Lizenzpflichtig) und "
    f"isinstance(Cloudspeicher(), Lizenzpflichtig) ergeben {ergebnis!r}, erwartet war (False, True, True).\n"
    "Tipp: Der Hook wird an Cloudspeicher vererbt. Geben Sie NotImplemented zurück, wenn cls nicht "
    "Lizenzpflichtig ist; sonst wäre jede Klasse mit jahreskosten eine Unterklasse von Cloudspeicher."
)


# Ohne Fund NotImplemented, damit register weiter wirkt
class Rahmenvertrag:
    """Hat keine Methode jahreskosten, wird aber von Hand registriert."""


Lizenzpflichtig.register(Rahmenvertrag)
ergebnis = (issubclass(Rahmenvertrag, Lizenzpflichtig), einordnen(Rahmenvertrag()))
assert ergebnis == (True, "lizenzpflichtig"), (
    "Nach Lizenzpflichtig.register(Rahmenvertrag) ergeben issubclass(Rahmenvertrag, Lizenzpflichtig) und "
    f"einordnen(Rahmenvertrag()) {ergebnis!r}, erwartet war (True, 'lizenzpflichtig').\n"
    "Tipp: Findet der Hook jahreskosten nicht, soll er NotImplemented zurückgeben, nicht False; False würde "
    "auch registrierte Klassen ablehnen."
)

@kostenlos
class Bildbetrachter:
    """Freie Software, mit dem Dekorator eingetragen."""


# kostenlos trägt ein und gibt die Klasse zurück, auch als Dekorator
ist_klasse = isinstance(Bildbetrachter, type)
ergebnis = (ist_klasse, ist_klasse and issubclass(Bildbetrachter, Kostenlos), ist_klasse and Kostenlos in Bildbetrachter.__mro__)
assert ergebnis == (True, True, False), (
    "Nach @kostenlos über class Bildbetrachter ergeben isinstance(Bildbetrachter, type), "
    f"issubclass(Bildbetrachter, Kostenlos) und Kostenlos in Bildbetrachter.__mro__ {ergebnis!r}, erwartet war "
    "(True, True, False).\nTipp: Kostenlos.register(klasse) trägt ein und gibt klasse zurück; erben soll die "
    "Klasse nicht."
)

# einordnen aus dem Beispiel
inventar = [OfficeAbo(25, 120), ServerLizenz(8000, 20), FreiesOffice()]
ergebnis = [einordnen(objekt) for objekt in inventar]
assert ergebnis == ["lizenzpflichtig", "lizenzpflichtig", "kostenlos"], (
    f"Für das Beispielinventar ergibt einordnen {ergebnis!r}, erwartet war "
    "['lizenzpflichtig', 'lizenzpflichtig', 'kostenlos'].\n"
    "Tipp: Prüfen Sie mit isinstance(objekt, Lizenzpflichtig), dann mit isinstance(objekt, Kostenlos)."
)

# gesamtkosten aus dem Beispiel
ergebnis = gesamtkosten(inventar)
assert ergebnis == 4600, (
    f"Für das Beispielinventar ergibt gesamtkosten {ergebnis!r}, erwartet war 4600 (25 · 120 + 20 % von 8000).\n"
    "Tipp: Summieren Sie jahreskosten() nur der lizenzpflichtigen Objekte."
)

# Testversion ist kostenlos, Notiz unbekannt
ergebnis = (einordnen(Testversion(5, 120)), einordnen(Notiz("Einkauf")), einordnen(42), einordnen(None))
assert ergebnis == ("kostenlos", "unbekannt", "unbekannt", "unbekannt"), (
    "einordnen(Testversion(5, 120)), einordnen(Notiz(...)), einordnen(42) und einordnen(None) ergeben "
    f"{ergebnis!r}, erwartet war ('kostenlos', 'unbekannt', 'unbekannt', 'unbekannt')."
)

# Ein unbekanntes Objekt im Inventar löst TypeError aus
try:
    gesamtkosten([OfficeAbo(1, 10), Notiz("Einkauf")])
    fehler = None
except TypeError as ausnahme:
    fehler = ausnahme
assert fehler is not None, (
    "gesamtkosten([OfficeAbo(1, 10), Notiz('Einkauf')]) soll einen TypeError auslösen, es kam keiner.\n"
    'Tipp: Gibt einordnen "unbekannt" zurück, lösen Sie mit raise TypeError(...) aus.'
)

# Leeres Inventar
ergebnis = gesamtkosten([])
assert ergebnis == 0, f"gesamtkosten([]) ergibt {ergebnis!r}, erwartet war 0."

# Nur kostenlose Software
ergebnis = gesamtkosten([FreiesOffice(), Testversion(3, 50), Bildbetrachter()])
assert ergebnis == 0, (
    f"gesamtkosten([FreiesOffice(), Testversion(3, 50), Bildbetrachter()]) ergibt {ergebnis!r}, erwartet war 0.\n"
    "Tipp: Testversion hat jahreskosten = None und ist kostenlos; rufen Sie jahreskosten() nur bei lizenzpflichtigen Objekten auf."
)

# Spätes register wirkt auch nach einer ersten Abfrage
class Altsystem:
    """Wird erst nach der ersten Abfrage als kostenlos eingetragen."""


vorher = einordnen(Altsystem())
kostenlos(Altsystem)
nachher = einordnen(Altsystem())
assert (vorher, nachher) == ("unbekannt", "kostenlos"), (
    f"einordnen(Altsystem()) ergibt vor und nach kostenlos(Altsystem) {(vorher, nachher)!r}, erwartet war "
    "('unbekannt', 'kostenlos')."
)

# 300 zufällige Inventare
zufall = Zufall(5017)
for _ in range(300):
    inventar = []
    erwartet = 0
    for _ in range(zufall.randint(0, 12)):
        wurf = zufall.randint(0, 4)
        if wurf == 0:
            plaetze, preis = zufall.randint(0, 500), zufall.randint(0, 2000)
            inventar.append(OfficeAbo(plaetze, preis))
            erwartet += plaetze * preis
        elif wurf == 1:
            kaufpreis, prozent = zufall.randint(0, 10**6), zufall.randint(0, 30)
            inventar.append(ServerLizenz(kaufpreis, prozent))
            erwartet += kaufpreis * prozent // 100
        elif wurf == 2:
            inventar.append(Cloudspeicher())
            erwartet += 600
        elif wurf == 3:
            inventar.append(Testversion(zufall.randint(1, 50), 100))
        else:
            inventar.append(zufall.choice([FreiesOffice, Bildbetrachter])())
    ergebnis = gesamtkosten(inventar)
    beschreibung = [type(objekt).__name__ for objekt in inventar]
    assert ergebnis == erwartet, f"gesamtkosten für ein Inventar aus {beschreibung} ergibt {ergebnis!r}, erwartet war {erwartet}."
    if inventar:
        stelle = zufall.randrange(len(inventar))
        inventar.insert(stelle, Notiz("verirrt"))
        try:
            gesamtkosten(inventar)
            ausgeloest = False
        except TypeError:
            ausgeloest = True
        assert ausgeloest, (
            f"gesamtkosten mit einer Notiz an Stelle {stelle} in {beschreibung} soll einen TypeError auslösen, "
            "es kam keiner."
        )

# Obere Grenze: 10 000 Objekte mit großen Kosten
inventar = []
for nummer in range(10000):
    if nummer % 2 == 0:
        inventar.append(OfficeAbo(1000, 10**4))
    else:
        inventar.append(FreiesOffice())
ergebnis = gesamtkosten(inventar)
assert ergebnis == 5000 * 10**7, f"gesamtkosten für 5000 Abos zu je 10**7 Euro und 5000 freie Programme ergibt {ergebnis!r}, erwartet war {5000 * 10**7}."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['lizenzpflichtig', 'lizenzpflichtig', 'kostenlos']\n4600"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
