# Automatisch erzeugt aus lehrkraft/muster/2_030_kundenstamm.py - nicht von Hand ändern.
# vorlage-hash: 64d1e308693c3d57
# text-hash: b57a90753e3e8ff7
# thema: datenstrukturen
# inhalt: Liste von Dictionaries filtern

def beispiel():
    """Baut die Kundendaten aus dem Beispiel neu."""
    return [
        {"name": "Ada Weber", "adresse": {"plz": "33098", "ort": "Paderborn"}, "bestellungen": [120, 35, 260]},
        {"name": "Ben Kaya", "adresse": {"plz": "44135", "ort": "Dortmund"}, "bestellungen": []},
        {"name": "Cem Ott", "adresse": {"plz": "33100", "ort": "Paderborn"}, "bestellungen": [99, 100]},
    ]


def kunde(name, ort, bestellungen, plz="10115"):
    """Baut einen Kunden-Datensatz für die Tests."""
    return {"name": name, "adresse": {"plz": plz, "ort": ort}, "bestellungen": bestellungen}


# kunden_in aus dem Beispiel
daten = beispiel()
ergebnis = kunden_in(daten, "Paderborn")
assert ergebnis == ["Ada Weber", "Cem Ott"], (
    f'kunden_in(<Beispiel>, "Paderborn") ergibt {ergebnis!r}, erwartet war ["Ada Weber", "Cem Ott"].\n'
    'Tipp: Der Ort steht eine Stufe tiefer: kunde["adresse"]["ort"]. Zurück kommen nur die Namen.'
)

# grosse_bestellungen findet die richtigen Beträge (die Namen zählen hier noch nicht)
ergebnis = grosse_bestellungen(daten, 100)
if isinstance(ergebnis, list):
    betraege = [eintrag[-1] if isinstance(eintrag, (tuple, list)) and eintrag else eintrag for eintrag in ergebnis]
else:
    betraege = ergebnis
assert betraege == [120, 260, 100], (
    f"grosse_bestellungen(<Beispiel>, 100) ergibt {ergebnis!r}, erwartet waren die Beträge 120, 260 und 100.\n"
    "Tipp: Gehen Sie mit einer zweiten Schleife durch die Liste kunde[\"bestellungen\"]. "
    "Ein Betrag genau gleich mindestens zählt mit."
)

# grosse_bestellungen aus dem Beispiel
ergebnis = grosse_bestellungen(daten, 100)
erwartet = [("Ada Weber", 120), ("Ada Weber", 260), ("Cem Ott", 100)]
assert ergebnis == erwartet, (
    f"grosse_bestellungen(<Beispiel>, 100) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Gehen Sie mit einer zweiten Schleife durch die Liste kunde[\"bestellungen\"] und hängen Sie für "
    "jede passende Bestellung ein Tupel (name, betrag) an. Ein Betrag genau gleich mindestens zählt mit."
)

# Die Kundendaten bleiben unverändert
assert daten == beispiel(), (
    f"Nach den Aufrufen sind die Kundendaten {daten!r}, erwartet war unverändert {beispiel()!r}.\n"
    "Tipp: Bauen Sie eine neue Liste mit append auf, statt aus kunden oder den Bestellungen zu entfernen."
)

# Anderer Ort (nicht fest hinschreiben!)
ergebnis = kunden_in(beispiel(), "Dortmund")
assert ergebnis == ["Ben Kaya"], f'kunden_in(<Beispiel>, "Dortmund") ergibt {ergebnis!r}, erwartet war ["Ben Kaya"].'

# Ort, in dem kein Kunde wohnt, und Groß- und Kleinschreibung
ergebnis = (kunden_in(beispiel(), "Bielefeld"), kunden_in(beispiel(), "paderborn"))
assert ergebnis == ([], []), (
    f'kunden_in(<Beispiel>, "Bielefeld") und kunden_in(<Beispiel>, "paderborn") ergeben {ergebnis!r}, '
    "erwartet war ([], [])."
)

# Doppelte Namen kommen bei kunden_in doppelt vor, in der Reihenfolge der Liste
daten = [kunde("Eva Rot", "Köln", [5]), kunde("Max Blau", "Bonn", [7]), kunde("Eva Rot", "Köln", [500, 600])]
ergebnis = kunden_in(daten, "Köln")
assert ergebnis == ["Eva Rot", "Eva Rot"], (
    f"Für {daten} ergibt kunden_in(…, 'Köln') {ergebnis!r}, erwartet war ['Eva Rot', 'Eva Rot']."
)

# Doppelte Namen bei grosse_bestellungen, in der Reihenfolge der Liste
ergebnis = grosse_bestellungen(daten, 6)
erwartet = [("Max Blau", 7), ("Eva Rot", 500), ("Eva Rot", 600)]
assert ergebnis == erwartet, (
    f"Für {daten} ergibt grosse_bestellungen(…, 6) {ergebnis!r}, erwartet war {erwartet!r}."
)

# Ränder: mindestens 1 nimmt jede Bestellung, 10**6 nur die größten
daten = [kunde("A", "X", [1, 10**6, 999999]), kunde("B", "Y", [])]
ergebnis = (grosse_bestellungen(daten, 1), grosse_bestellungen(daten, 10**6))
erwartet = ([("A", 1), ("A", 10**6), ("A", 999999)], [("A", 10**6)])
assert ergebnis == erwartet, (
    f"Für {daten} ergeben grosse_bestellungen(…, 1) und (…, 10**6) {ergebnis!r}, erwartet war {erwartet!r}."
)

# kunden_in ohne Kunden
ergebnis = kunden_in([], "Paderborn")
assert ergebnis == [], f'kunden_in([], "Paderborn") ergibt {ergebnis!r}, erwartet war [].'

# grosse_bestellungen ohne Kunden
ergebnis = grosse_bestellungen([], 50)
assert ergebnis == [], f"grosse_bestellungen([], 50) ergibt {ergebnis!r}, erwartet war []."


# Vergleichslösung: über Indizes statt über die Elemente
def kunden_in_von_hand(kunden, ort):
    """Sammelt die Namen über die Indizes der Liste."""
    namen = []
    for index in range(len(kunden)):
        adresse = kunden[index]["adresse"]
        if adresse["ort"] == ort:
            namen.append(kunden[index]["name"])
    return namen


def grosse_von_hand(kunden, mindestens):
    """Sammelt die großen Bestellungen über die Indizes beider Listen."""
    gross = []
    for index in range(len(kunden)):
        betraege = kunden[index]["bestellungen"]
        for stelle in range(len(betraege)):
            if not betraege[stelle] < mindestens:
                gross.append((kunden[index]["name"], betraege[stelle]))
    return gross


def kopie(kunden):
    """Kopiert die Kundendaten Stufe für Stufe, damit Änderungen auffallen."""
    ergebnis = []
    for eintrag in kunden:
        ergebnis.append(kunde(eintrag["name"], eintrag["adresse"]["ort"], list(eintrag["bestellungen"]),
                              eintrag["adresse"]["plz"]))
    return ergebnis


# 300 zufällige Kundenlisten für kunden_in
zufall = Zufall(2030)
ORTE = ["Paderborn", "Dortmund", "Bonn", "Köln", "Kiel"]
NAMEN = ["Ada", "Ben", "Cem", "Dana", "Eli", "Fynn"]
for _ in range(300):
    daten = []
    for _ in range(zufall.randint(0, 8)):
        betraege = [zufall.randint(1, 300) for _ in range(zufall.randint(0, 5))]
        daten.append(kunde(zufall.choice(NAMEN), zufall.choice(ORTE), betraege, str(zufall.randint(10000, 99999))))
    vorher = kopie(daten)
    ort = zufall.choice(ORTE)
    mindestens = zufall.randint(1, 300)
    ergebnis = kunden_in(daten, ort)
    erwartet = kunden_in_von_hand(vorher, ort)
    assert ergebnis == erwartet, f"kunden_in({vorher}, {ort!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    assert daten == vorher, f"Nach kunden_in sind die Kundendaten {daten!r}, erwartet war unverändert {vorher!r}."

# 300 zufällige Kundenlisten für grosse_bestellungen
zufall = Zufall(2030)
for _ in range(300):
    daten = []
    for _ in range(zufall.randint(0, 8)):
        betraege = [zufall.randint(1, 300) for _ in range(zufall.randint(0, 5))]
        daten.append(kunde(zufall.choice(NAMEN), zufall.choice(ORTE), betraege, str(zufall.randint(10000, 99999))))
    vorher = kopie(daten)
    ort = zufall.choice(ORTE)
    mindestens = zufall.randint(1, 300)
    ergebnis = grosse_bestellungen(daten, mindestens)
    erwartet = grosse_von_hand(vorher, mindestens)
    assert ergebnis == erwartet, (
        f"grosse_bestellungen({vorher}, {mindestens}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )
    assert daten == vorher, f"Nach den Aufrufen sind die Kundendaten {daten!r}, erwartet war unverändert {vorher!r}."

# Obere Grenze: 10 000 Kunden mit je 100 Bestellungen
daten = []
for nummer in range(10000):
    daten.append(kunde(f"Kunde {nummer}", ORTE[nummer % 5], list(range(nummer % 7 + 1, 10**6, 10007))[:100]))
ergebnis = kunden_in(daten, "Kiel")
assert isinstance(ergebnis, list) and len(ergebnis) == 2000 and ergebnis[0] == "Kunde 4" and ergebnis[-1] == "Kunde 9999", (
    "Bei 10 000 Kunden, von denen jeder fünfte (Kunde 4, Kunde 9, …) in Kiel wohnt, erwartet kunden_in(…, 'Kiel') "
    f"2000 Namen von 'Kunde 4' bis 'Kunde 9999'; bekommen {len(ergebnis) if isinstance(ergebnis, list) else ergebnis!r} Einträge."
)

# Obere Grenze: große Bestellungen bei 10 000 Kunden
ergebnis = grosse_bestellungen(daten, 990000)
erwartet = grosse_von_hand(daten, 990000)
assert ergebnis == erwartet, (
    f"Bei 10 000 Kunden mit je 100 Bestellungen ergibt grosse_bestellungen(…, 990000) "
    f"{len(ergebnis) if isinstance(ergebnis, list) else ergebnis!r} Einträge, erwartet waren {len(erwartet)}, "
    f"beginnend mit {erwartet[:2]}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['Ada Weber', 'Cem Ott']\n[('Ada Weber', 120), ('Ada Weber', 260), ('Cem Ott', 100)]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
