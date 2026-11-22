# Automatisch erzeugt aus lehrkraft/muster/2_041_maskenzeiten.py - nicht von Hand ändern.
# vorlage-hash: 0d16111cc7013aee
# text-hash: ec5046c845c96acd
# thema: datenanalyse
# inhalt: Summe je Kategorie

import ast


def beispiel():
    """Baut das Protokoll aus dem Beispiel neu."""
    return [
        {"maske": "Anmeldung", "sekunden": 14},
        {"maske": "Warenkorb", "sekunden": 31},
        {"maske": "Zahlung", "sekunden": 52},
        {"maske": "Warenkorb", "sekunden": 9},
        {"maske": "Zahlung", "sekunden": 40},
    ]


def zeilen(*paare):
    """Baut ein Protokoll aus Paaren (maske, sekunden)."""
    return [{"maske": maske, "sekunden": sekunden} for maske, sekunden in paare]


def vergleichsloesung(protokoll):
    """Rechnet langsam, aber offensichtlich richtig: für jede Maske alle passenden Zeilen addieren."""
    ergebnis = {}
    for maske in set(zeile["maske"] for zeile in protokoll):
        ergebnis[maske] = sum(zeile["sekunden"] for zeile in protokoll if zeile["maske"] == maske)
    return ergebnis


def hinweis_zu(ergebnis, protokoll):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if not isinstance(ergebnis, dict):
        return "\nTipp: Geben Sie ein Dictionary mit return zurück."
    letzte = {}
    for zeile in protokoll:
        letzte[zeile["maske"]] = zeile["sekunden"]
    if ergebnis == letzte and ergebnis != vergleichsloesung(protokoll):
        return (
            "\nTipp: Es steht jeweils nur die letzte Zeit da. Addieren Sie zur bisherigen Summe: "
            "summen[maske] = summen.get(maske, 0) + zeile[\"sekunden\"]."
        )
    return ""


# Das Beispiel aus der Aufgabe: Warenkorb wird aus zwei Zeilen zusammengezählt
erwartet = {"Anmeldung": 14, "Warenkorb": 40, "Zahlung": 92}
try:
    ergebnis = zeit_je_maske(beispiel())
    tipp = hinweis_zu(ergebnis, beispiel())
except KeyError as fehler:
    ergebnis = f"KeyError: {fehler}"
    tipp = "\nTipp: Beim ersten Vorkommen gibt es den Schlüssel noch nicht; summen.get(maske, 0) liefert dann 0."
assert ergebnis == erwartet, f"zeit_je_maske(<Beispiel>) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{tipp}"

# Ein anderes Protokoll (nicht fest hinschreiben!)
daten = zeilen(("Suche", 5), ("Treffer", 12), ("Suche", 7), ("Suche", 3))
ergebnis = zeit_je_maske(daten)
assert ergebnis == {"Suche": 15, "Treffer": 12}, (
    f"zeit_je_maske({daten!r}) ergibt {ergebnis!r}, erwartet war {{'Suche': 15, 'Treffer': 12}}."
    f"{hinweis_zu(ergebnis, daten)}"
)

# Ein Protokoll, in dem jede Maske nur einmal vorkommt
daten = zeilen(("Start", 3), ("Profil", 8), ("Hilfe", 20))
ergebnis = zeit_je_maske(daten)
assert ergebnis == {"Start": 3, "Profil": 8, "Hilfe": 20}, (
    f"zeit_je_maske({daten!r}) ergibt {ergebnis!r}, erwartet war {{'Start': 3, 'Profil': 8, 'Hilfe': 20}}."
)

# Eine einzige Zeile
ergebnis = zeit_je_maske(zeilen(("Anmeldung", 3600)))
assert ergebnis == {"Anmeldung": 3600}, (
    f'zeit_je_maske([{{"maske": "Anmeldung", "sekunden": 3600}}]) ergibt {ergebnis!r}, erwartet war {{"Anmeldung": 3600}}.'
)

# Leeres Protokoll ergibt ein leeres Dictionary
ergebnis = zeit_je_maske([])
assert ergebnis == {}, f"zeit_je_maske([]) ergibt {ergebnis!r}, erwartet war {{}} (ein leeres Dictionary)."

# Eine Maske mit 0 Sekunden kommt trotzdem ins Ergebnis
daten = zeilen(("Start", 0), ("Hilfe", 4), ("Start", 0))
ergebnis = zeit_je_maske(daten)
assert ergebnis == {"Start": 0, "Hilfe": 4}, (
    f"zeit_je_maske({daten!r}) ergibt {ergebnis!r}, erwartet war {{'Start': 0, 'Hilfe': 4}}.\n"
    "Tipp: Legen Sie jede Maske an, die vorkommt, auch wenn ihre Zeit 0 ist (kein if zeile[\"sekunden\"] > 0)."
)

# Groß- und Kleinschreibung zählt
daten = zeilen(("Zahlung", 10), ("zahlung", 5))
ergebnis = zeit_je_maske(daten)
assert ergebnis == {"Zahlung": 10, "zahlung": 5}, (
    f"zeit_je_maske({daten!r}) ergibt {ergebnis!r}, erwartet war {{'Zahlung': 10, 'zahlung': 5}}.\n"
    "Tipp: Benutzen Sie den Namen der Maske unverändert als Schlüssel, ohne lower()."
)

# Das Protokoll bleibt unverändert
daten = beispiel()
zeit_je_maske(daten)
assert daten == beispiel(), f"Nach zeit_je_maske ist das Protokoll {daten!r}, erwartet war unverändert {beispiel()!r}."

# Jeder Aufruf liefert ein neues Dictionary (keine Summen aus früheren Aufrufen)
erstes = zeit_je_maske(zeilen(("Start", 1)))
zweites = zeit_je_maske(zeilen(("Start", 1)))
assert erstes == {"Start": 1} and zweites == {"Start": 1} and erstes is not zweites, (
    f"Zweimal zeit_je_maske([{{'maske': 'Start', 'sekunden': 1}}]) ergibt {erstes!r} und {zweites!r}, "
    "erwartet war beide Male ein neues {'Start': 1}.\n"
    "Tipp: Legen Sie das Dictionary innerhalb der Funktion an, nicht außerhalb."
)

# 300 zufällige Protokolle, verglichen mit einer langsamen Vergleichslösung
zufall = Zufall(2041)
for runde in range(300):
    namen = ["Start", "Suche", "Warenkorb", "Zahlung", "zahlung", "Hilfe"][: zufall.randint(1, 6)]
    daten = zeilen(*[(zufall.choice(namen), zufall.randint(0, 3600)) for _ in range(runde // 10)])
    ergebnis = zeit_je_maske(daten)
    erwartet = vergleichsloesung(daten)
    assert ergebnis == erwartet, (
        f"zeit_je_maske({daten!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis_zu(ergebnis, daten)}"
    )

# Obere Grenze: 100 000 Zeilen mit 50 verschiedenen Masken
daten = zeilen(*[(f"Maske {nummer % 50}", nummer % 3601) for nummer in range(100000)])
ergebnis = zeit_je_maske(daten)
erwartet = {}
for nummer in range(50):
    # Maske nummer kommt in den Zeilen nummer, nummer + 50, … vor
    erwartet[f"Maske {nummer}"] = sum(zeile % 3601 for zeile in range(nummer, 100000, 50))
assert ergebnis == erwartet, (
    "Bei 100 000 Zeilen mit den Masken 'Maske 0' bis 'Maske 49' stimmt das Ergebnis nicht; "
    f"erwartet z. B. 'Maske 0': {erwartet['Maske 0']}, bekommen: {ergebnis.get('Maske 0') if isinstance(ergebnis, dict) else ergebnis!r}."
)

# Die Ausgabe des Programms stimmt (die Reihenfolge der Masken ist egal)
try:
    gedruckt = ast.literal_eval(AUSGABE.strip())
except (ValueError, SyntaxError):
    gedruckt = AUSGABE
assert gedruckt == {"Anmeldung": 14, "Warenkorb": 40, "Zahlung": 92}, (
    f"Erwartete Ausgabe: {{'Anmeldung': 14, 'Warenkorb': 40, 'Zahlung': 92}} – Ihr Programm: {AUSGABE}"
)
