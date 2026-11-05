# Automatisch erzeugt aus lehrkraft/muster/2_027_testkonten.py - nicht von Hand ändern.
# vorlage-hash: a1f8dc1ce86ffbac
# text-hash: 6481c68d7e08a66b
# thema: datenstrukturen
# inhalt: Dictionary als Datensatz

# konto aus dem Beispiel
ergebnis = konto("Kim", 34, "vorstand")
assert ergebnis == {"name": "Kim", "alter": 34, "rolle": "vorstand"}, (
    f'konto("Kim", 34, "vorstand") ergibt {ergebnis!r}, erwartet war {{"name": "Kim", "alter": 34, "rolle": "vorstand"}}.\n'
    'Tipp: Die Schlüssel heißen genau "name", "alter" und "rolle".'
)

# Ohne Rolle ist die Rolle "gast"
ergebnis = konto("Ali", 17)
assert ergebnis == {"name": "Ali", "alter": 17, "rolle": "gast"}, (
    f'konto("Ali", 17) ergibt {ergebnis!r}, erwartet war {{"name": "Ali", "alter": 17, "rolle": "gast"}}.'
)

# Jeder Aufruf liefert ein neues Dictionary
erstes = konto("A", 1)
zweites = konto("A", 1)
erstes["alter"] = 99
assert zweites == {"name": "A", "alter": 1, "rolle": "gast"}, (
    f"Nach einer Änderung am ersten Ergebnis von konto ist das zweite {zweites!r}; jeder Aufruf soll ein neues "
    "Dictionary zurückgeben."
)

# Gültige Datensätze, auch an den Grenzen
for datensatz in [
    {"name": "Kim", "alter": 34, "rolle": "vorstand"},
    {"rolle": "mitglied", "name": "B", "alter": 0},
    {"alter": 120, "rolle": "gast", "name": "x" * 100},
]:
    ergebnis = ist_gueltig(datensatz)
    assert ergebnis is True, f"ist_gueltig({datensatz!r}) ergibt {ergebnis!r}, erwartet war True."

# Ungültige Werte
for datensatz, grund in [
    ({"name": "Kim", "alter": 121, "rolle": "gast"}, "Das Alter darf höchstens 120 sein."),
    ({"name": "Kim", "alter": -1, "rolle": "gast"}, "Das Alter darf nicht negativ sein."),
    ({"name": "", "alter": 30, "rolle": "gast"}, "Der Name darf nicht leer sein."),
    ({"name": "Kim", "alter": 30, "rolle": "admin"}, "Die Rolle muss gast, mitglied oder vorstand sein."),
    ({"name": "Kim", "alter": 30, "rolle": "Gast"}, "Die Rollen sind kleingeschrieben."),
    ({"name": "Kim", "alter": 30, "rolle": ""}, "Auch eine leere Rolle ist falsch."),
]:
    ergebnis = ist_gueltig(datensatz)
    assert ergebnis is False, f"ist_gueltig({datensatz!r}) ergibt {ergebnis!r}, erwartet war False. {grund}"

# Fehlende und zusätzliche Felder
for datensatz, grund in [
    ({"name": "Kim", "alter": 34}, 'Das Feld "rolle" fehlt.'),
    ({"alter": 34, "rolle": "gast"}, 'Das Feld "name" fehlt.'),
    ({"name": "Kim", "rolle": "gast"}, 'Das Feld "alter" fehlt.'),
    ({}, "Der Datensatz ist leer."),
    ({"name": "Kim", "alter": 34, "rolle": "gast", "email": "kim@verein.de"}, 'Das Feld "email" ist zu viel.'),
]:
    try:
        ergebnis = ist_gueltig(datensatz)
    except KeyError as fehler:
        ergebnis = f"KeyError: {fehler}"
    assert ergebnis is False, (
        f"ist_gueltig({datensatz!r}) ergibt {ergebnis!r}, erwartet war False. {grund}\n"
        "Tipp: Prüfen Sie zuerst, ob genau die drei Schlüssel vorhanden sind, bevor Sie die Werte lesen."
    )

# beschreibe aus dem Beispiel und für ungültige Datensätze
for datensatz, erwartet in [
    ({"name": "Kim", "alter": 34, "rolle": "vorstand"}, "Kim (34 Jahre, vorstand)"),
    ({"rolle": "gast", "alter": 0, "name": "Neu"}, "Neu (0 Jahre, gast)"),
    ({"name": "Kim", "alter": 34}, "ungültiger Datensatz"),
    ({"name": "Kim", "alter": 200, "rolle": "gast"}, "ungültiger Datensatz"),
]:
    try:
        ergebnis = beschreibe(datensatz)
    except KeyError as fehler:
        ergebnis = f"KeyError: {fehler}"
    assert ergebnis == erwartet, (
        f"beschreibe({datensatz!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Fragen Sie zuerst mit ist_gueltig, ob der Datensatz gültig ist."
    )

# Die Datensätze bleiben unverändert
datensatz = {"name": "Kim", "alter": 34, "rolle": "gast", "x": "y"}
ist_gueltig(datensatz)
beschreibe(datensatz)
assert datensatz == {"name": "Kim", "alter": 34, "rolle": "gast", "x": "y"}, (
    f"Nach ist_gueltig und beschreibe ist der Datensatz {datensatz!r}; er soll unverändert bleiben."
)

# beschreibe benutzt ist_gueltig
_echtes_ist_gueltig = ist_gueltig


def ist_gueltig(datensatz):
    """Hält jeden Datensatz für ungültig."""
    return False


ergebnis = beschreibe({"name": "Kim", "alter": 34, "rolle": "gast"})
ist_gueltig = _echtes_ist_gueltig
assert ergebnis == "ungültiger Datensatz", (
    "beschreibe soll ist_gueltig benutzen, um gültige von ungültigen Datensätzen zu unterscheiden; "
    "die Regeln sollen nur an einer Stelle stehen."
)


# Vergleichslösung: alle Regeln einzeln mit in und einer Schleife über die Schlüssel
def gueltig_von_hand(datensatz):
    """Prüft jeden Schlüssel einzeln und dann die Werte."""
    for schluessel in datensatz:
        if schluessel != "name" and schluessel != "alter" and schluessel != "rolle":
            return False
    if not ("name" in datensatz and "alter" in datensatz and "rolle" in datensatz):
        return False
    alter = datensatz["alter"]
    rolle_ok = datensatz["rolle"] == "gast" or datensatz["rolle"] == "mitglied" or datensatz["rolle"] == "vorstand"
    return len(datensatz["name"]) > 0 and 0 <= alter <= 120 and rolle_ok


# 500 zufällige Datensätze
zufall = Zufall(2027)
for _ in range(500):
    datensatz = {}
    for feld in zufall.sample(["name", "alter", "rolle", "email", "id"], zufall.randint(0, 5)):
        if feld == "alter":
            datensatz[feld] = zufall.choice([zufall.randint(-1000, 1000), zufall.randint(-2, 2), zufall.randint(118, 122)])
        elif feld == "rolle":
            datensatz[feld] = zufall.choice(ROLLEN + ["", "admin", "Vorstand"])
        else:
            datensatz[feld] = zufall.choice(["", "Kim", "Ali", "a" * 100])
    if zufall.random() < 0.5:
        datensatz = konto(zufall.choice(["", "Jo", "Mia"]), zufall.randint(-3, 123), zufall.choice(ROLLEN + ["chef"]))
    vorher = dict(datensatz)
    erwartet = gueltig_von_hand(datensatz)
    ergebnis = ist_gueltig(datensatz)
    assert ergebnis == erwartet and datensatz == vorher, (
        f"ist_gueltig({vorher!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}; der Datensatz ist danach {datensatz!r}."
    )
    text = beschreibe(datensatz)
    erwarteter_text = f"{vorher['name']} ({vorher['alter']} Jahre, {vorher['rolle']})" if erwartet else "ungültiger Datensatz"
    assert text == erwarteter_text, f"beschreibe({vorher!r}) ergibt {text!r}, erwartet war {erwarteter_text!r}."

# An der oberen Grenze: 10 000 Konten anlegen und prüfen
konten = [konto(f"Person {nummer}", nummer % 121, ROLLEN[nummer % 3]) for nummer in range(10000)]
gueltige = [datensatz for datensatz in konten if ist_gueltig(datensatz)]
assert len(gueltige) == 10000 and beschreibe(konten[-1]) == "Person 9999 (77 Jahre, gast)", (
    f"Von 10 000 mit konto angelegten Datensätzen sind {len(gueltige)} gültig, beschreibe(konten[-1]) ergibt "
    f"{beschreibe(konten[-1])!r}; erwartet waren 10 000 und 'Person 9999 (77 Jahre, gast)'."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "{'name': 'Kim', 'alter': 34, 'rolle': 'vorstand'}\n{'name': 'Ali', 'alter': 17, 'rolle': 'gast'}\n"
    "False False\nKim (34 Jahre, vorstand)"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
