# Automatisch erzeugt aus lehrkraft/muster/4_029_ticketbilanz.py - nicht von Hand ändern.
# vorlage-hash: 9142c9fe39b638d1
# text-hash: 234d6514c792d300
# thema: funktionen
# inhalt: functools.reduce

def ticket(nummer, prioritaet, kategorie, minuten):
    """Baut ein Ticket-Dictionary."""
    return {"nummer": nummer, "prioritaet": prioritaet, "kategorie": kategorie, "minuten": minuten}


def kopien(tickets):
    """Tiefe Kopie einer Ticketliste, um Veränderungen zu erkennen."""
    return [dict(eintrag) for eintrag in tickets]


def summe_vergleich(tickets):
    """Vergleichslösung für gesamtminuten mit sum."""
    return sum(eintrag["minuten"] for eintrag in tickets)


def dringendstes_vergleich(tickets):
    """Vergleichslösung für dringendstes mit min (liefert bei Gleichstand das erste)."""
    return min(tickets, key=lambda eintrag: eintrag["prioritaet"], default=None)


def kategorien_vergleich(tickets):
    """Vergleichslösung für minuten_je_kategorie mit einer Schleife."""
    ergebnis = {}
    for eintrag in tickets:
        ergebnis[eintrag["kategorie"]] = ergebnis.get(eintrag["kategorie"], 0) + eintrag["minuten"]
    return ergebnis


def nummer_von(eintrag):
    """Nummer eines Tickets für Fehlermeldungen; None bleibt None."""
    return eintrag["nummer"] if isinstance(eintrag, dict) and "nummer" in eintrag else eintrag


BEISPIEL = [ticket(1, 3, "Drucker", 20), ticket(2, 1, "Netzwerk", 45), ticket(3, 1, "Drucker", 10)]

# gesamtminuten: das Beispiel aus der Aufgabe
ergebnis = gesamtminuten(kopien(BEISPIEL))
assert ergebnis == 75, f"gesamtminuten(<Beispiel>) ergibt {ergebnis!r}, erwartet war 75 (20 + 45 + 10)."

# gesamtminuten: andere Tickets (nicht fest hinschreiben!)
liste = [ticket(7, 2, "Konto", 5), ticket(8, 4, "Konto", 0), ticket(9, 2, "Mail", 120)]
ergebnis = gesamtminuten(liste)
assert ergebnis == 125, f"gesamtminuten({liste}) ergibt {ergebnis!r}, erwartet war 125."

# gesamtminuten: leere Liste ergibt 0
try:
    ergebnis = gesamtminuten([])
except TypeError as fehler:
    ergebnis = f"TypeError: {fehler}"
assert ergebnis == 0, (
    f"gesamtminuten([]) ergibt {ergebnis!r}, erwartet war 0.\n"
    "Tipp: Geben Sie reduce den Startwert 0 als drittes Argument mit."
)

# dringendstes: das Beispiel aus der Aufgabe, bei Gleichstand das erste
ergebnis = dringendstes(kopien(BEISPIEL))
assert nummer_von(ergebnis) == 2, (
    f"dringendstes(<Beispiel>) liefert das Ticket {nummer_von(ergebnis)!r}, erwartet war Ticket 2 "
    "(Priorität 1, vor Ticket 3 mit ebenfalls Priorität 1).\n"
    "Tipp: Ersetzen Sie das bisherige Ticket nur, wenn das neue eine echt kleinere Prioritätszahl hat (<, nicht <=)."
)

# dringendstes: das ganze Ticket-Dictionary kommt zurück
ergebnis = dringendstes(kopien(BEISPIEL))
assert ergebnis == BEISPIEL[1], f"dringendstes(<Beispiel>) liefert {ergebnis!r}, erwartet war das ganze Ticket {BEISPIEL[1]!r}."

# dringendstes: das dringendste Ticket steht ganz vorn oder ganz hinten
vorn = [ticket(5, 1, "A", 1), ticket(6, 2, "A", 1), ticket(7, 3, "A", 1)]
hinten = [ticket(5, 4, "A", 1), ticket(6, 3, "A", 1), ticket(7, 2, "A", 1)]
ergebnisse = (nummer_von(dringendstes(vorn)), nummer_von(dringendstes(hinten)))
assert ergebnisse == (5, 7), (
    f"Bei Prioritäten 1, 2, 3 und 4, 3, 2 (Nummern 5, 6, 7) liefert dringendstes die Tickets {ergebnisse!r}, erwartet war (5, 7)."
)

# dringendstes: leere Liste ergibt None
try:
    ergebnis = dringendstes([])
except TypeError as fehler:
    ergebnis = f"TypeError: {fehler}"
assert ergebnis is None, (
    f"dringendstes([]) ergibt {ergebnis!r}, erwartet war None.\n"
    "Tipp: Mit dem Startwert None und einer Funktion, die None durch das erste Ticket ersetzt, geht es ohne Sonderfall."
)

# minuten_je_kategorie: das Beispiel aus der Aufgabe
ergebnis = minuten_je_kategorie(kopien(BEISPIEL))
assert ergebnis == {"Drucker": 30, "Netzwerk": 45}, (
    f"minuten_je_kategorie(<Beispiel>) ergibt {ergebnis!r}, erwartet war {{'Drucker': 30, 'Netzwerk': 45}}."
)

# minuten_je_kategorie: Reihenfolge des ersten Vorkommens
liste = [ticket(1, 2, "Mail", 5), ticket(2, 2, "Konto", 7), ticket(3, 2, "Mail", 1), ticket(4, 2, "Drucker", 0)]
ergebnis = minuten_je_kategorie(liste)
assert isinstance(ergebnis, dict) and list(ergebnis.items()) == [("Mail", 6), ("Konto", 7), ("Drucker", 0)], (
    f"minuten_je_kategorie({liste}) ergibt {ergebnis!r}, erwartet war {{'Mail': 6, 'Konto': 7, 'Drucker': 0}} in dieser Reihenfolge."
)

# minuten_je_kategorie: leere Liste ergibt ein leeres Dictionary
try:
    ergebnis = minuten_je_kategorie([])
except TypeError as fehler:
    ergebnis = f"TypeError: {fehler}"
assert ergebnis == {}, f"minuten_je_kategorie([]) ergibt {ergebnis!r}, erwartet war {{}}."

# minuten_je_kategorie: zwei Aufrufe nacheinander beeinflussen sich nicht
erstes = minuten_je_kategorie([ticket(1, 1, "Mail", 10)])
zweites = minuten_je_kategorie([ticket(2, 1, "Mail", 3)])
assert (erstes, zweites) == ({"Mail": 10}, {"Mail": 3}), (
    f"minuten_je_kategorie mit einem Mail-Ticket von 10 und danach mit einem von 3 Minuten ergibt {erstes!r} und "
    f"{zweites!r}, erwartet war {{'Mail': 10}} und {{'Mail': 3}}.\n"
    "Tipp: Ein Startwert {} wird bei jedem Aufruf neu gebaut; verändern Sie aber kein Dictionary, das von außen kommt."
)

# Die Tickets bleiben unverändert
liste = kopien(BEISPIEL)
gesamtminuten(liste)
dringendstes(liste)
minuten_je_kategorie(liste)
assert liste == BEISPIEL, f"Nach den drei Funktionen ist die Ticketliste {liste!r}, erwartet war sie unverändert: {BEISPIEL!r}."

# reduce wird benutzt
assert verwendet("reduce"), "Benutzen Sie functools.reduce für die drei Funktionen."

# Ohne for- und while-Schleifen
assert not verwendet("for") and not verwendet("while"), (
    "Ihr Code enthält eine for- oder while-Schleife. Falten Sie die Liste stattdessen mit reduce zusammen."
)

# 300 zufällige Schichten
zufall = Zufall(4029)
kategorien = ["Netzwerk", "Drucker", "Konto", "Mail", "Hardware"]
for runde in range(300):
    liste = [
        ticket(nummer, zufall.randint(1, 4), zufall.choice(kategorien), zufall.randint(0, 10000))
        for nummer in range(runde % 25)
    ]
    original = kopien(liste)
    ergebnisse = (gesamtminuten(liste), nummer_von(dringendstes(liste)), minuten_je_kategorie(liste))
    erwartet = (summe_vergleich(original), nummer_von(dringendstes_vergleich(original)), kategorien_vergleich(original))
    assert ergebnisse == erwartet and liste == original, (
        f"Für die Tickets {original}\nergeben gesamtminuten, dringendstes (Nummer) und minuten_je_kategorie\n"
        f"  {ergebnisse!r}\nerwartet war\n  {erwartet!r}"
        + ("\nAußerdem wurden die Tickets verändert." if liste != original else "")
    )

# Obere Grenze: 10 000 Tickets in 20 Kategorien
liste = [ticket(nummer, (nummer * 7) % 4 + 1, f"K{nummer % 20}", (nummer * 37) % 10001) for nummer in range(10000)]
liste[6000]["prioritaet"] = 1
ergebnisse = (gesamtminuten(liste), nummer_von(dringendstes(liste)), minuten_je_kategorie(liste))
erwartet = (summe_vergleich(liste), nummer_von(dringendstes_vergleich(liste)), kategorien_vergleich(liste))
assert ergebnisse == erwartet, (
    "Bei 10 000 Tickets ergeben gesamtminuten, dringendstes (Nummer) und die ersten Einträge von minuten_je_kategorie "
    f"{ergebnisse[:2]!r} und {list(ergebnisse[2].items())[:3] if isinstance(ergebnisse[2], dict) else ergebnisse[2]!r}, "
    f"erwartet war {erwartet[:2]!r} und {list(erwartet[2].items())[:3]!r}."
)
