# Automatisch erzeugt aus lehrkraft/muster/4_041_co2_bilanz.py - nicht von Hand ändern.
# vorlage-hash: 6b1e2c01d9a2611d
# text-hash: 7c73b8043cb88aee
# thema: datenanalyse
# inhalt: pandas: groupby und agg

import pandas as pd

SPALTEN = ["inventar", "standort", "typ", "kwh_jahr", "alter"]
BEISPIEL = [
    {"inventar": 1, "standort": "Kiel", "typ": "Notebook", "kwh_jahr": 40, "alter": 2},
    {"inventar": 2, "standort": "Kiel", "typ": "Drucker", "kwh_jahr": 150, "alter": 6},
    {"inventar": 3, "standort": "Bonn", "typ": "Notebook", "kwh_jahr": 35, "alter": 4},
    {"inventar": 4, "standort": "Kiel", "typ": "Notebook", "kwh_jahr": 45, "alter": 1},
]


def tabelle(zeilen):
    """Baut einen DataFrame mit den fünf Spalten, auch wenn zeilen leer ist."""
    return pd.DataFrame(zeilen, columns=SPALTEN)


def zeilen_von(funktion, zeilen, *argumente):
    """Ruft die Funktion mit einer neuen Tabelle auf und gibt das Ergebnis als Liste von Dictionaries zurück.

    Ein Fehler, ein Ergebnis ohne DataFrame oder ein Schlüssel im Index wird als Text beschrieben.
    """
    try:
        ergebnis = funktion(tabelle(zeilen), *argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"
    if not isinstance(ergebnis, pd.DataFrame):
        return f"keinen DataFrame, sondern {type(ergebnis).__name__}: {ergebnis!r}"
    if ergebnis.index.name in ("standort", "typ"):
        return f"einen DataFrame mit {ergebnis.index.name} im Index statt in einer Spalte (reset_index fehlt)"
    return ergebnis.to_dict("records")


def passt(ergebnis, erwartet, spalte):
    """True, wenn zwei Listen von Zeilen gleich sind; in spalte darf die letzte Stelle um 1 abweichen.

    pandas und Python runden Grenzfälle wie 12.25 nicht immer gleich, beides ist richtig.
    """
    if not isinstance(ergebnis, list) or len(ergebnis) != len(erwartet):
        return False
    for zeile, soll in zip(ergebnis, erwartet):
        wert = zeile.get(spalte)
        if not isinstance(wert, (int, float)) or abs(wert - soll[spalte]) > 0.1001:
            return False
        if {**zeile, spalte: 0} != {**soll, spalte: 0}:
            return False
    return True


def vergleich_standorte(zeilen):
    """Vergleichslösung mit Dictionaries statt pandas."""
    anzahl = {}
    kwh = {}
    for zeile in zeilen:
        anzahl[zeile["standort"]] = anzahl.get(zeile["standort"], 0) + 1
        kwh[zeile["standort"]] = kwh.get(zeile["standort"], 0) + zeile["kwh_jahr"]
    return [{"standort": ort, "anzahl": anzahl[ort], "kwh": kwh[ort]} for ort in sorted(anzahl)]


def vergleich_bilanz(zeilen, gramm):
    """Vergleichslösung für co2_bilanz mit sorted."""
    bilanz = [{**zeile, "co2_kg": round(zeile["kwh"] * gramm / 1000, 1)} for zeile in vergleich_standorte(zeilen)]
    return sorted(bilanz, key=lambda zeile: (-zeile["co2_kg"], zeile["standort"]))


def vergleich_typen(zeilen):
    """Vergleichslösung für typen_uebersicht mit Dictionaries."""
    werte = {}
    alter = {}
    for zeile in zeilen:
        werte.setdefault(zeile["typ"], []).append(zeile["kwh_jahr"])
        alter[zeile["typ"]] = max(alter.get(zeile["typ"], 0), zeile["alter"])
    return [
        {"typ": typ, "anzahl": len(werte[typ]), "kwh_mittel": round(sum(werte[typ]) / len(werte[typ]), 1), "aeltestes": alter[typ]}
        for typ in sorted(werte)
    ]


def zufallsgeraete(zufall, anzahl):
    """Erzeugt anzahl zufällige Geräte innerhalb der Grenzen."""
    orte = zufall.sample(["Kiel", "Bonn", "Ulm", "Essen", "Jena", "Hof"], zufall.randint(1, 6))
    typen = ["Notebook", "Monitor", "Drucker", "Switch", "Server"]
    zeilen = []
    for nummer in range(1, anzahl + 1):
        zeilen.append(
            {
                "inventar": nummer,
                "standort": zufall.choice(orte),
                "typ": zufall.choice(typen),
                "kwh_jahr": zufall.choice([0, 5000, zufall.randint(0, 500)]),
                "alter": zufall.randint(0, 20),
            }
        )
    zufall.shuffle(zeilen)
    return zeilen


# verbrauch_je_standort im Beispiel
ergebnis = zeilen_von(verbrauch_je_standort, BEISPIEL)
erwartet = [{"standort": "Bonn", "anzahl": 1, "kwh": 35}, {"standort": "Kiel", "anzahl": 3, "kwh": 235}]
assert ergebnis == erwartet, (
    f"verbrauch_je_standort(geraete) ergibt {ergebnis}, erwartet war {erwartet}.\n"
    'Tipp: geraete.groupby("standort").agg(anzahl=("inventar", "count"), kwh=("kwh_jahr", "sum")) und danach reset_index().'
)

# verbrauch_je_standort mit anderen Geräten (nicht fest hinschreiben!)
zeilen = [
    {"inventar": 7, "standort": "Ulm", "typ": "Server", "kwh_jahr": 2000, "alter": 3},
    {"inventar": 8, "standort": "Essen", "typ": "Monitor", "kwh_jahr": 60, "alter": 5},
    {"inventar": 9, "standort": "Ulm", "typ": "Switch", "kwh_jahr": 300, "alter": 8},
    {"inventar": 10, "standort": "Essen", "typ": "Monitor", "kwh_jahr": 0, "alter": 0},
]
ergebnis = zeilen_von(verbrauch_je_standort, zeilen)
erwartet = [{"standort": "Essen", "anzahl": 2, "kwh": 60}, {"standort": "Ulm", "anzahl": 2, "kwh": 2300}]
assert ergebnis == erwartet, f"Bei vier Geräten in Ulm und Essen ergibt verbrauch_je_standort {ergebnis}, erwartet war {erwartet}."

# Ein einziger Standort
zeilen = [{**zeile, "standort": "Hof"} for zeile in BEISPIEL]
ergebnis = zeilen_von(verbrauch_je_standort, zeilen)
erwartet = [{"standort": "Hof", "anzahl": 4, "kwh": 270}]
assert ergebnis == erwartet, f"Stehen alle Geräte in Hof, ergibt verbrauch_je_standort {ergebnis}, erwartet war {erwartet}."

# co2_bilanz im Beispiel
ergebnis = zeilen_von(co2_bilanz, BEISPIEL, 380)
erwartet = [
    {"standort": "Kiel", "anzahl": 3, "kwh": 235, "co2_kg": 89.3},
    {"standort": "Bonn", "anzahl": 1, "kwh": 35, "co2_kg": 13.3},
]
assert passt(ergebnis, erwartet, "co2_kg"), (
    f"co2_bilanz(geraete, 380) ergibt {ergebnis}, erwartet war {erwartet}.\n"
    "Tipp: Rechnen Sie co2_kg als neue Spalte auf dem Ergebnis von verbrauch_je_standort und sortieren Sie absteigend."
)

# co2_kg ist auf eine Nachkommastelle gerundet
ergebnis = zeilen_von(co2_bilanz, BEISPIEL, 380)
werte = [zeile.get("co2_kg") for zeile in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert werte == [89.3, 13.3], f"co2_bilanz(geraete, 380) hat in co2_kg {werte}, erwartet war genau [89.3, 13.3]."

# co2_kg ist auch bei vielen Nachkommastellen auf eine gerundet
zeilen = [{"inventar": 1, "standort": "Hof", "typ": "Switch", "kwh_jahr": 1, "alter": 1}]
ergebnis = zeilen_von(co2_bilanz, zeilen, 123)
werte = [zeile.get("co2_kg") for zeile in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert werte == [0.1], (
    f"Bei 1 kWh und 123 g/kWh hat co2_bilanz in co2_kg {werte}, erwartet war [0.1] (0.123 auf eine Stelle gerundet).\n"
    "Tipp: .round(1) auf der neuen Spalte."
)

# co2_bilanz: bei gleichem CO₂ nach Standort sortiert
zeilen = [
    {"inventar": 1, "standort": "Ulm", "typ": "Monitor", "kwh_jahr": 100, "alter": 1},
    {"inventar": 2, "standort": "Bonn", "typ": "Monitor", "kwh_jahr": 100, "alter": 1},
    {"inventar": 3, "standort": "Essen", "typ": "Server", "kwh_jahr": 900, "alter": 1},
]
ergebnis = zeilen_von(co2_bilanz, zeilen, 500)
orte = [zeile["standort"] for zeile in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert orte == ["Essen", "Bonn", "Ulm"], (
    f"co2_bilanz mit 900, 100 und 100 kWh ergibt die Reihenfolge {orte}, erwartet war ['Essen', 'Bonn', 'Ulm'].\n"
    "Tipp: sort_values(by=[\"co2_kg\", \"standort\"], ascending=[False, True])."
)

# co2_bilanz mit 0 Gramm pro kWh (Ökostrom)
ergebnis = zeilen_von(co2_bilanz, BEISPIEL, 0)
werte = [(zeile["standort"], zeile.get("co2_kg")) for zeile in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert werte == [("Bonn", 0), ("Kiel", 0)], f"co2_bilanz(geraete, 0) ergibt {werte}, erwartet war [('Bonn', 0.0), ('Kiel', 0.0)]."

# typen_uebersicht im Beispiel
ergebnis = zeilen_von(typen_uebersicht, BEISPIEL)
erwartet = [
    {"typ": "Drucker", "anzahl": 1, "kwh_mittel": 150.0, "aeltestes": 6},
    {"typ": "Notebook", "anzahl": 3, "kwh_mittel": 40.0, "aeltestes": 4},
]
assert passt(ergebnis, erwartet, "kwh_mittel"), (
    f"typen_uebersicht(geraete) ergibt {ergebnis}, erwartet war {erwartet}.\n"
    'Tipp: agg mit ("kwh_jahr", "mean") und ("alter", "max").'
)

# kwh_mittel ist auf eine Nachkommastelle gerundet
zeilen = [
    {"inventar": 1, "standort": "Kiel", "typ": "Monitor", "kwh_jahr": 10, "alter": 1},
    {"inventar": 2, "standort": "Kiel", "typ": "Monitor", "kwh_jahr": 10, "alter": 2},
    {"inventar": 3, "standort": "Kiel", "typ": "Monitor", "kwh_jahr": 11, "alter": 3},
]
ergebnis = zeilen_von(typen_uebersicht, zeilen)
werte = [zeile.get("kwh_mittel") for zeile in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert werte == [10.3], f"Bei 10, 10 und 11 kWh hat typen_uebersicht in kwh_mittel {werte}, erwartet war [10.3]."

# Die übergebene Tabelle bleibt unverändert
geraete_test = tabelle(BEISPIEL)
for funktion, argumente in [(verbrauch_je_standort, ()), (co2_bilanz, (380,)), (typen_uebersicht, ())]:
    try:
        funktion(geraete_test, *argumente)
    except Exception:
        pass
assert list(geraete_test.columns) == SPALTEN and geraete_test.to_dict("records") == BEISPIEL, (
    f"Nach den drei Aufrufen hat die übergebene Tabelle die Spalten {list(geraete_test.columns)}; erwartet war sie unverändert."
)

# Eine leere Tabelle ergibt leere Ergebnisse
ergebnis = [zeilen_von(verbrauch_je_standort, []), zeilen_von(co2_bilanz, [], 380), zeilen_von(typen_uebersicht, [])]
assert ergebnis == [[], [], []], f"Mit einer leeren Tabelle ergeben die drei Funktionen {ergebnis}, erwartet war [[], [], []]."

# Ohne Schleife über Zeilen oder Gruppen
benutzt = [name for name in ["for", "while", "iterrows", "itertuples", "apply"] if verwendet(name)]
assert benutzt == [], f"Ihr Code verwendet {benutzt}. Lassen Sie groupby und agg die Gruppen zusammenfassen."

# Die Ausgabe des Programms
erwartet = "[{'standort': 'Bonn', 'anzahl': 1, 'kwh': 35}, {'standort': 'Kiel', 'anzahl': 3, 'kwh': 235}]\n[89.3, 13.3]\n[150.0, 40.0]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Inventarlisten
zufall = Zufall(4041)
for _ in range(60):
    zeilen = zufallsgeraete(zufall, zufall.randint(1, 15))
    gramm = zufall.randint(0, 1000)
    ergebnis = zeilen_von(verbrauch_je_standort, zeilen)
    erwartet = vergleich_standorte(zeilen)
    assert ergebnis == erwartet, f"Bei den Geräten {zeilen} ergibt verbrauch_je_standort {ergebnis}, erwartet war {erwartet}."
    ergebnis = zeilen_von(typen_uebersicht, zeilen)
    erwartet = vergleich_typen(zeilen)
    assert passt(ergebnis, erwartet, "kwh_mittel"), (
        f"Bei den Geräten {zeilen} ergibt typen_uebersicht {ergebnis}, erwartet war {erwartet}."
    )
    ergebnis = zeilen_von(co2_bilanz, zeilen, gramm)
    erwartet = vergleich_bilanz(zeilen, gramm)
    assert passt(ergebnis, erwartet, "co2_kg"), f"Bei den Geräten {zeilen} ergibt co2_bilanz(geraete, {gramm}) {ergebnis}, erwartet war {erwartet}."

# Obere Grenze: 20 000 Geräte
zeilen = zufallsgeraete(zufall, 20000)
ergebnis = [zeilen_von(verbrauch_je_standort, zeilen), zeilen_von(co2_bilanz, zeilen, 999)]
assert ergebnis[0] == vergleich_standorte(zeilen) and passt(ergebnis[1], vergleich_bilanz(zeilen, 999), "co2_kg"), (
    "Bei 20 000 Geräten stimmen die Ergebnisse von verbrauch_je_standort oder co2_bilanz nicht."
)
