# Automatisch erzeugt aus lehrkraft/muster/4_036_firewallprotokoll.py - nicht von Hand ändern.
# vorlage-hash: 5a845c0079502f77
# text-hash: 128588b805c3aacf
# thema: kontrollfluss
# inhalt: Generator-Pipeline

import types

BEISPIEL = [
    "# Protokoll fw-01",
    "ACCEPT 10.0.0.12 10.0.1.5:443 1500",
    "",
    "DROP 203.0.113.7 10.0.1.5:22 60\n",
    "DROP 198.51.100.3 10.0.1.9:3389 52",
]
SAUBER = ["ACCEPT 10.0.0.12 10.0.1.5:443 1500", "DROP 203.0.113.7 10.0.1.5:22 60", "DROP 198.51.100.3 10.0.1.9:3389 52"]
TUPEL = [
    ("ACCEPT", "10.0.0.12", "10.0.1.5", 443, 1500),
    ("DROP", "203.0.113.7", "10.0.1.5", 22, 60),
    ("DROP", "198.51.100.3", "10.0.1.9", 3389, 52),
]


class Zaehlquelle:
    """Ein Iterable, das mitzählt, wie viele Zeilen schon abgeholt wurden; ohne Liste darf es unendlich sein."""

    def __init__(self, zeile_zu_nummer, laenge=None):
        """Merkt sich, wie aus einer Zeilennummer die Zeile wird, und die Länge (None = unendlich)."""
        self.zeile_zu_nummer = zeile_zu_nummer
        self.laenge = laenge
        self.gelesen = 0

    def __iter__(self):
        """Liefert die Zeilen der Reihe nach und zählt jede abgeholte Zeile."""
        nummer = 0
        while self.laenge is None or nummer < self.laenge:
            self.gelesen += 1
            yield self.zeile_zu_nummer(nummer)
            nummer += 1


def jede_dritte_drop(nummer):
    """Unendliches Protokoll: Zeile 2, 5, 8, … ist DROP von 192.0.2.<nummer % 250>, dazwischen ACCEPT und Kommentare."""
    if nummer % 3 == 0:
        return "# Zwischenstand"
    if nummer % 3 == 1:
        return f"ACCEPT 10.0.0.{nummer % 250} 10.0.1.5:443 {nummer % 65536}"
    return f"DROP 192.0.2.{nummer % 250} 10.0.1.5:22 60"


def vergleich_tupel(zeilen):
    """Vergleichslösung: zerlegt die Zeilen mit einem regulären Ausdruck statt mit split."""
    import re

    ergebnis = []
    for zeile in zeilen:
        treffer = re.fullmatch(r"\s*(ACCEPT|DROP) (\S+) (\S+):(\d+) (\d+)\s*", zeile)
        if treffer:
            aktion, absender, ziel, port, groesse = treffer.groups()
            ergebnis.append((aktion, absender, ziel, int(port), int(groesse)))
    return ergebnis


def zufallszeile(zufall):
    """Erzeugt eine zufällige Zeile: Paket, Leerzeile oder Kommentar, mit zufälligem Rand."""
    art = zufall.random()
    rand_vorn = zufall.choice(["", " ", "\t"])
    rand_hinten = zufall.choice(["", "\n", "  \n"])
    if art < 0.15:
        return rand_vorn + rand_hinten
    if art < 0.25:
        return rand_vorn + "# Kommentar 1.2.3.4:80" + rand_hinten
    aktion = zufall.choice(["ACCEPT", "DROP"])
    absender = ".".join(str(zufall.randint(0, 255)) for _ in range(4))
    ziel = ".".join(str(zufall.randint(0, 255)) for _ in range(4))
    port = zufall.choice([0, 22, 443, zufall.randint(0, 65535)])
    groesse = zufall.choice([0, 65535, zufall.randint(0, 65535)])
    return f"{rand_vorn}{aktion} {absender} {ziel}:{port} {groesse}{rand_hinten}"


# lies im Beispiel
ergebnis = list(lies(BEISPIEL))
assert ergebnis == SAUBER, f"list(lies(zeilen)) ergibt im Beispiel {ergebnis!r}, erwartet war {SAUBER!r}."

# lies entfernt Leerzeichen und Zeilenumbrüche am Rand, auch Tabulatoren
ergebnis = list(lies(["  DROP 1.2.3.4 5.6.7.8:80 10 \n", "\tACCEPT 1.1.1.1 2.2.2.2:53 70\t"]))
assert ergebnis == ["DROP 1.2.3.4 5.6.7.8:80 10", "ACCEPT 1.1.1.1 2.2.2.2:53 70"], (
    f"lies mit Rand-Leerzeichen ergibt {ergebnis!r}, erwartet war ['DROP 1.2.3.4 5.6.7.8:80 10', "
    "'ACCEPT 1.1.1.1 2.2.2.2:53 70'].\nTipp: zeile.strip() entfernt Leerzeichen, Tabulatoren und Zeilenumbrüche."
)

# lies überspringt Zeilen nur aus Leerzeichen und eingerückte Kommentare
ergebnis = list(lies(["   ", "\n", "  # Kommentar", "#", "DROP 1.2.3.4 5.6.7.8:80 10"]))
assert ergebnis == ["DROP 1.2.3.4 5.6.7.8:80 10"], (
    f"lies mit Leerzeichen-Zeilen und eingerückten Kommentaren ergibt {ergebnis!r}, erwartet war ['DROP 1.2.3.4 5.6.7.8:80 10'].\n"
    "Tipp: Prüfen Sie erst nach strip(), ob die Zeile leer ist oder mit # beginnt."
)

# lies ist ein Generator
assert isinstance(lies(BEISPIEL), types.GeneratorType), (
    f"lies(zeilen) ergibt ein Objekt vom Typ {type(lies(BEISPIEL)).__name__}, erwartet war ein Generator.\n"
    "Tipp: Liefern Sie jede Zeile mit yield, statt eine Liste zurückzugeben."
)

# zerlege im Beispiel
ergebnis = list(zerlege(SAUBER))
assert ergebnis == TUPEL, f"list(zerlege(...)) ergibt im Beispiel {ergebnis!r}, erwartet war {TUPEL!r}."

# zerlege: Port und Größe sind Zahlen
ergebnis = next(zerlege(["DROP 10.9.8.7 10.0.0.1:0 65535"]))
assert ergebnis == ("DROP", "10.9.8.7", "10.0.0.1", 0, 65535) and type(ergebnis[3]) is int and type(ergebnis[4]) is int, (
    f'next(zerlege(["DROP 10.9.8.7 10.0.0.1:0 65535"])) ergibt {ergebnis!r}, erwartet war '
    "('DROP', '10.9.8.7', '10.0.0.1', 0, 65535) mit int für Port und Größe."
)

# zerlege ist ein Generator
assert isinstance(zerlege(SAUBER), types.GeneratorType), (
    f"zerlege(zeilen) ergibt ein Objekt vom Typ {type(zerlege(SAUBER)).__name__}, erwartet war ein Generator."
)

# verworfen behält nur DROP
ergebnis = list(verworfen(TUPEL))
assert ergebnis == TUPEL[1:], f"list(verworfen(...)) ergibt im Beispiel {ergebnis!r}, erwartet war {TUPEL[1:]!r}."

# verworfen ist ein Generator
assert isinstance(verworfen(TUPEL), types.GeneratorType), (
    f"verworfen(pakete) ergibt ein Objekt vom Typ {type(verworfen(TUPEL)).__name__}, erwartet war ein Generator."
)

# erste_angreifer im Beispiel
ergebnis = [erste_angreifer(BEISPIEL, 1), erste_angreifer(BEISPIEL, 5)]
assert ergebnis == [["203.0.113.7"], ["203.0.113.7", "198.51.100.3"]], (
    f"erste_angreifer(zeilen, 1) und erste_angreifer(zeilen, 5) ergeben {ergebnis!r}, erwartet war "
    "[['203.0.113.7'], ['203.0.113.7', '198.51.100.3']]."
)

# erste_angreifer mit anzahl 0
ergebnis = erste_angreifer(BEISPIEL, 0)
assert ergebnis == [], f"erste_angreifer(zeilen, 0) ergibt {ergebnis!r}, erwartet war []."

# erste_angreifer ohne verworfene Pakete
ergebnis = erste_angreifer(["ACCEPT 1.1.1.1 2.2.2.2:53 70"], 3)
assert ergebnis == [], f'erste_angreifer(["ACCEPT 1.1.1.1 2.2.2.2:53 70"], 3) ergibt {ergebnis!r}, erwartet war [].'

# erste_angreifer ohne Zeilen
ergebnis = erste_angreifer([], 3)
assert ergebnis == [], f"erste_angreifer([], 3) ergibt {ergebnis!r}, erwartet war []."

# Die Ausgabe des Programms
erwartet = f"{SAUBER}\n{TUPEL[0]}\n['203.0.113.7', '198.51.100.3']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# erste_angreifer liest nach dem letzten gebrauchten Paket nicht weiter
quelle = Zaehlquelle(jede_dritte_drop, laenge=3000)
ergebnis = erste_angreifer(quelle, 1)
assert ergebnis == ["192.0.2.2"] and quelle.gelesen <= 4, (
    f"erste_angreifer(quelle, 1) bei 3000 Zeilen ergibt {ergebnis!r} nach {quelle.gelesen} gelesenen Zeilen; "
    "erwartet war ['192.0.2.2'] nach höchstens 4 Zeilen."
)

# Die Stufen holen nur so viele Zeilen ab, wie gebraucht werden
quelle = Zaehlquelle(jede_dritte_drop)
erstes = next(verworfen(zerlege(lies(quelle))))
assert erstes == ("DROP", "192.0.2.2", "10.0.1.5", 22, 60) and quelle.gelesen == 3, (
    f"next(verworfen(zerlege(lies(quelle)))) bei einem unendlichen Protokoll ergibt {erstes!r} nach {quelle.gelesen} "
    "gelesenen Zeilen; erwartet war ('DROP', '192.0.2.2', '10.0.1.5', 22, 60) nach 3 Zeilen."
)

# erste_angreifer bei einem unendlichen Protokoll
quelle = Zaehlquelle(jede_dritte_drop)
ergebnis = erste_angreifer(quelle, 4)
assert ergebnis == ["192.0.2.2", "192.0.2.5", "192.0.2.8", "192.0.2.11"] and quelle.gelesen <= 13, (
    f"erste_angreifer(quelle, 4) bei einem unendlichen Protokoll ergibt {ergebnis!r} nach {quelle.gelesen} gelesenen "
    "Zeilen; erwartet war ['192.0.2.2', '192.0.2.5', '192.0.2.8', '192.0.2.11'] nach höchstens 13 Zeilen.\n"
    "Tipp: Nehmen Sie mit zip(range(anzahl), kette) nur die ersten anzahl Pakete."
)

# Viele zufällige Protokolle, jede Stufe einzeln und alles zusammen
zufall = Zufall(4036)
for runde in range(200):
    zeilen = [zufallszeile(zufall) for _ in range(zufall.randint(0, 12))]
    erwartet_sauber = [zeile.strip() for zeile in zeilen if zeile.strip() and not zeile.strip().startswith("#")]
    ergebnis = list(lies(zeilen))
    assert ergebnis == erwartet_sauber, f"list(lies({zeilen!r}))\n  ergibt   {ergebnis!r}\n  erwartet {erwartet_sauber!r}"
    erwartet_tupel = vergleich_tupel(zeilen)
    ergebnis = list(zerlege(erwartet_sauber))
    assert ergebnis == erwartet_tupel, f"list(zerlege({erwartet_sauber!r}))\n  ergibt   {ergebnis!r}\n  erwartet {erwartet_tupel!r}"
    erwartet_drop = [paket for paket in erwartet_tupel if paket[0] == "DROP"]
    ergebnis = list(verworfen(erwartet_tupel))
    assert ergebnis == erwartet_drop, f"list(verworfen({erwartet_tupel!r}))\n  ergibt   {ergebnis!r}\n  erwartet {erwartet_drop!r}"
    anzahl = zufall.randint(0, 5)
    erwartet_absender = [paket[1] for paket in erwartet_drop[:anzahl]]
    ergebnis = erste_angreifer(iter(zeilen), anzahl)
    assert ergebnis == erwartet_absender, f"erste_angreifer({zeilen!r}, {anzahl}) ergibt {ergebnis!r}, erwartet war {erwartet_absender!r}."

# Obere Grenze: 100 000 Zeilen und anzahl 10 000
quelle = Zaehlquelle(jede_dritte_drop, laenge=100000)
ergebnis = erste_angreifer(quelle, 10000)
erwartet = [f"192.0.2.{nummer % 250}" for nummer in range(2, 30000, 3)]
assert ergebnis == erwartet and quelle.gelesen <= 30001, (
    f"erste_angreifer mit 100 000 Zeilen und anzahl 10 000 ergibt {len(ergebnis)} Absender nach {quelle.gelesen} "
    f"gelesenen Zeilen; erwartet waren 10 000 nach höchstens 30 001 Zeilen. Erste Abweichung bei Nummer "
    f"{next((i for i, (a, b) in enumerate(zip(ergebnis, erwartet)) if a != b), min(len(ergebnis), len(erwartet)))}."
)

# Obere Grenze: alle 100 000 Zeilen, weniger verworfene Pakete als anzahl
quelle = Zaehlquelle(lambda nummer: "ACCEPT 1.1.1.1 2.2.2.2:53 70" if nummer < 99999 else "DROP 9.9.9.9 2.2.2.2:53 70", laenge=100000)
ergebnis = erste_angreifer(quelle, 10**4)
assert ergebnis == ["9.9.9.9"], f"Bei 99 999 ACCEPT und einem DROP in der letzten Zeile ergibt erste_angreifer {ergebnis!r}, erwartet war ['9.9.9.9']."
