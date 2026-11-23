# Automatisch erzeugt aus lehrkraft/muster/4_044_wissensdatenbank.py - nicht von Hand ändern.
# vorlage-hash: bc43ca834b8186fa
# text-hash: e5df5cc380097b6e
# thema: kontrollfluss
# inhalt: itertools.groupby

def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def eintrag(kategorie, titel, aufrufe):
    """Baut einen Artikel als Dictionary."""
    return {"kategorie": kategorie, "titel": titel, "aufrufe": aufrufe}


def vergleich_kategorien(artikel):
    """Vergleichslösung mit einem Dictionary statt groupby."""
    anzahl = {}
    summe = {}
    for zeile in artikel:
        anzahl[zeile["kategorie"]] = anzahl.get(zeile["kategorie"], 0) + 1
        summe[zeile["kategorie"]] = summe.get(zeile["kategorie"], 0) + zeile["aufrufe"]
    return [(kategorie, anzahl[kategorie], summe[kategorie]) for kategorie in sorted(anzahl)]


def vergleich_meistgelesen(artikel):
    """Vergleichslösung: merkt sich je Kategorie den bisher besten Artikel."""
    beste = {}
    for zeile in artikel:
        bisher = beste.get(zeile["kategorie"])
        if bisher is None or (-zeile["aufrufe"], zeile["titel"]) < (-bisher["aufrufe"], bisher["titel"]):
            beste[zeile["kategorie"]] = zeile
    return {kategorie: zeile["titel"] for kategorie, zeile in beste.items()}


def vergleich_suchen(protokoll):
    """Vergleichslösung mit einem Zähler für den laufenden Begriff."""
    ergebnis = []
    stelle = 0
    while stelle < len(protokoll):
        ende = stelle
        while ende < len(protokoll) and protokoll[ende] == protokoll[stelle]:
            ende += 1
        if ende - stelle >= 2:
            ergebnis.append((protokoll[stelle], ende - stelle))
        stelle = ende
    return ergebnis


BEISPIEL = [
    eintrag("VPN", "Verbindung bricht ab", 120),
    eintrag("Drucker", "Treiber installieren", 40),
    eintrag("VPN", "Zertifikat erneuern", 75),
]
SUCHEN = ["vpn", "vpn", "drucker", "vpn", "wlan", "wlan", "wlan"]

# kategorien im Beispiel
ergebnis = wert_von(lambda: kategorien(BEISPIEL))
assert ergebnis == [("Drucker", 1, 40), ("VPN", 2, 195)], (
    f"kategorien(artikel) ergibt {ergebnis!r}, erwartet war [('Drucker', 1, 40), ('VPN', 2, 195)].\n"
    "Tipp: groupby fasst nur Nachbarn zusammen; sortieren Sie die Artikel vorher nach der Kategorie."
)

# kategorien mit bereits sortierten Artikeln (nicht fest hinschreiben!)
artikel = [eintrag("Mail", "Abwesenheit", 10), eintrag("Mail", "Postfach voll", 30), eintrag("WLAN", "Gastzugang", 5)]
ergebnis = wert_von(lambda: kategorien(artikel))
assert ergebnis == [("Mail", 2, 40), ("WLAN", 1, 5)], f"kategorien für zwei Mail- und einen WLAN-Artikel ergibt {ergebnis!r}, erwartet war [('Mail', 2, 40), ('WLAN', 1, 5)]."

# kategorien: dieselbe Kategorie an weit auseinanderliegenden Stellen
artikel = [eintrag("A", "a1", 1), eintrag("B", "b1", 2), eintrag("A", "a2", 3), eintrag("B", "b2", 4), eintrag("A", "a3", 5)]
ergebnis = wert_von(lambda: kategorien(artikel))
assert ergebnis == [("A", 3, 9), ("B", 2, 6)], (
    f"kategorien für A, B, A, B, A ergibt {ergebnis!r}, erwartet war [('A', 3, 9), ('B', 2, 6)].\n"
    "Tipp: Ohne Sortieren beginnt bei jedem Wechsel eine neue Gruppe; sorted(artikel, key=...) mit demselben key wie groupby."
)

# kategorien ohne Artikel und mit Artikeln ohne Aufrufe
ergebnis = wert_von(lambda: [kategorien([]), kategorien([eintrag("Neu", "x", 0)])])
assert ergebnis == [[], [("Neu", 1, 0)]], f"kategorien([]) und kategorien mit einem Artikel ohne Aufrufe ergeben {ergebnis!r}, erwartet war [[], [('Neu', 1, 0)]]."

# kategorien lässt die übergebene Liste unverändert
artikel = [eintrag("B", "b", 1), eintrag("A", "a", 2)]
wert_von(lambda: kategorien(artikel))
assert artikel == [eintrag("B", "b", 1), eintrag("A", "a", 2)], (
    f"Nach kategorien ist die Liste {artikel}, erwartet war sie unverändert.\nTipp: sorted(...) statt artikel.sort()."
)

# groupby wird benutzt
assert verwendet("groupby"), "Benutzen Sie itertools.groupby."

# meistgelesen im Beispiel
ergebnis = wert_von(lambda: meistgelesen(BEISPIEL))
erwartet = {"Drucker": "Treiber installieren", "VPN": "Verbindung bricht ab"}
assert ergebnis == erwartet, (
    f"meistgelesen(artikel) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Sortieren Sie nach Kategorie und absteigend nach Aufrufen; next(gruppe) ist dann der meistgelesene Artikel."
)

# meistgelesen: der meistgelesene Artikel steht nicht vorn (nicht fest hinschreiben!)
artikel = [eintrag("Mail", "Abwesenheit", 10), eintrag("Mail", "Signatur", 90), eintrag("Mail", "Postfach voll", 30)]
ergebnis = wert_von(lambda: meistgelesen(artikel))
assert ergebnis == {"Mail": "Signatur"}, f"meistgelesen mit 10, 90 und 30 Aufrufen ergibt {ergebnis!r}, erwartet war {{'Mail': 'Signatur'}}."

# meistgelesen bei Gleichstand: der alphabetisch erste Titel
artikel = [eintrag("Mail", "Signatur", 50), eintrag("Mail", "Abwesenheit", 50), eintrag("Mail", "Postfach voll", 50)]
ergebnis = wert_von(lambda: meistgelesen(artikel))
assert ergebnis == {"Mail": "Abwesenheit"}, (
    f"meistgelesen mit drei Artikeln zu je 50 Aufrufen ergibt {ergebnis!r}, erwartet war {{'Mail': 'Abwesenheit'}}.\n"
    "Tipp: Sortieren Sie zusätzlich nach dem Titel, etwa mit key=lambda a: (a[\"kategorie\"], -a[\"aufrufe\"], a[\"titel\"])."
)

# meistgelesen ohne Artikel und mit verstreuten Kategorien
artikel = [eintrag("A", "a1", 1), eintrag("B", "b1", 9), eintrag("A", "a2", 3)]
ergebnis = wert_von(lambda: [meistgelesen([]), meistgelesen(artikel)])
assert ergebnis == [{}, {"A": "a2", "B": "b1"}], f"meistgelesen([]) und meistgelesen für A, B, A ergeben {ergebnis!r}, erwartet war [{{}}, {{'A': 'a2', 'B': 'b1'}}]."

# wiederholte_suchen im Beispiel
ergebnis = wert_von(lambda: wiederholte_suchen(SUCHEN))
assert ergebnis == [("vpn", 2), ("wlan", 3)], (
    f"wiederholte_suchen({SUCHEN}) ergibt {ergebnis!r}, erwartet war [('vpn', 2), ('wlan', 3)].\n"
    "Tipp: Hier nicht sortieren; groupby(protokoll) liefert genau die Läufe direkt hintereinander."
)

# wiederholte_suchen: derselbe Begriff in zwei getrennten Läufen
ergebnis = wert_von(lambda: wiederholte_suchen(["vpn", "vpn", "mail", "vpn", "vpn", "vpn"]))
assert ergebnis == [("vpn", 2), ("vpn", 3)], (
    f'wiederholte_suchen(["vpn", "vpn", "mail", "vpn", "vpn", "vpn"]) ergibt {ergebnis!r}, erwartet war [("vpn", 2), ("vpn", 3)].'
)

# wiederholte_suchen: einzelne Begriffe zählen nicht
ergebnis = wert_von(lambda: [wiederholte_suchen(["a", "b", "a", "b"]), wiederholte_suchen([]), wiederholte_suchen(["x"])])
assert ergebnis == [[], [], []], (
    f'wiederholte_suchen(["a", "b", "a", "b"]), ([]) und (["x"]) ergeben {ergebnis!r}, erwartet war [[], [], []].'
)

# wiederholte_suchen: Groß- und Kleinschreibung zählt
ergebnis = wert_von(lambda: wiederholte_suchen(["VPN", "vpn", "vpn"]))
assert ergebnis == [("vpn", 2)], f'wiederholte_suchen(["VPN", "vpn", "vpn"]) ergibt {ergebnis!r}, erwartet war [("vpn", 2)].'

# Die Ausgabe des Programms (die Reihenfolge im Dictionary von meistgelesen ist nicht vorgegeben)
erwartet = (
    "[('Drucker', 1, 40), ('VPN', 2, 195)]\n{'Drucker': 'Treiber installieren', 'VPN': 'Verbindung bricht ab'}\n"
    "[('vpn', 2), ('wlan', 3)]"
)
erlaubt = [
    vergleichbar(erwartet),
    vergleichbar(
        "[('Drucker', 1, 40), ('VPN', 2, 195)]\n{'VPN': 'Verbindung bricht ab', 'Drucker': 'Treiber installieren'}\n"
        "[('vpn', 2), ('wlan', 3)]"
    ),
]
assert vergleichbar(AUSGABE) in erlaubt, f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Datenbanken: kategorien
zufall = Zufall(4044)
datenbanken = []
for _ in range(300):
    artikel = []
    for kategorie in zufall.sample(["VPN", "Mail", "WLAN", "Drucker", "Konto"], zufall.randint(0, 5)):
        for titel in zufall.sample(["a", "b", "c", "d", "e"], zufall.randint(1, 4)):
            artikel.append(eintrag(kategorie, titel, zufall.choice([0, 5, 10, zufall.randint(0, 10**6)])))
    zufall.shuffle(artikel)
    datenbanken.append(artikel)
for artikel in datenbanken:
    kopie = [dict(zeile) for zeile in artikel]
    ergebnis = wert_von(lambda: kategorien(artikel))
    erwartet = vergleich_kategorien(kopie)
    assert ergebnis == erwartet, f"Bei den Artikeln {kopie} ergibt kategorien {ergebnis!r}, erwartet war {erwartet!r}."

# Viele zufällige Datenbanken: meistgelesen
for artikel in datenbanken:
    kopie = [dict(zeile) for zeile in artikel]
    ergebnis = wert_von(lambda: meistgelesen(artikel))
    erwartet = vergleich_meistgelesen(kopie)
    assert ergebnis == erwartet, f"Bei den Artikeln {kopie} ergibt meistgelesen {ergebnis!r}, erwartet war {erwartet!r}."

# Viele zufällige Protokolle: wiederholte_suchen
for _ in range(300):
    protokoll = [zufall.choice(["vpn", "mail", "wlan"]) for _ in range(zufall.randint(0, 10))]
    ergebnis = wert_von(lambda: wiederholte_suchen(protokoll))
    erwartet = vergleich_suchen(protokoll)
    assert ergebnis == erwartet, f"wiederholte_suchen({protokoll}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Obere Grenze: 100 000 Artikel in 100 Kategorien
artikel = [eintrag(f"K{zufall.randint(0, 99):02d}", f"T{nummer}", zufall.randint(0, 10**6)) for nummer in range(100000)]
ergebnis = wert_von(lambda: kategorien(artikel))
assert ergebnis == vergleich_kategorien(artikel), "Bei 100 000 Artikeln stimmt das Ergebnis von kategorien nicht."

# Obere Grenze: meistgelesen mit 100 000 Artikeln
ergebnis = wert_von(lambda: meistgelesen(artikel))
assert ergebnis == vergleich_meistgelesen(artikel), "Bei 100 000 Artikeln stimmt das Ergebnis von meistgelesen nicht."

# Obere Grenze: 100 000 Suchbegriffe
protokoll = [zufall.choice(["vpn", "mail"]) for _ in range(100000)]
ergebnis = wert_von(lambda: wiederholte_suchen(protokoll))
assert ergebnis == vergleich_suchen(protokoll), "Bei 100 000 Suchbegriffen stimmt das Ergebnis von wiederholte_suchen nicht."
