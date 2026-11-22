# Automatisch erzeugt aus lehrkraft/muster/3_038_kundenstamm.py - nicht von Hand ändern.
# vorlage-hash: e9bcf79176470001
# text-hash: 02fa3e0776965fd8
# thema: datenanalyse
# inhalt: pandas: DataFrame, Spalten

import pandas as pd

SPALTEN = ["kundennummer", "name", "ort", "email", "telefon"]
KUNDEN = [
    {"kundennummer": 1001, "name": "Weber GmbH", "ort": "Kassel", "email": "info@weber.example", "telefon": "0561 1234"},
    {"kundennummer": 1002, "name": "Lindner KG", "ort": "Fulda", "email": "post@lindner.example", "telefon": "0661 9876"},
]
DREI = [
    {"kundennummer": 7, "name": "Arslan IT", "ort": "Marburg", "email": "a@arslan.example", "telefon": "06421 1"},
    {"kundennummer": 3, "name": "Berg & Sohn", "ort": "Gießen", "email": "b@berg.example", "telefon": "0641 2"},
    {"kundennummer": 9, "name": "Chen AG", "ort": "Marburg", "email": "c@chen.example", "telefon": "06421 3"},
]


def als_zeilen(df):
    """Liest einen DataFrame als Liste von Dictionaries, für Vergleiche und Meldungen."""
    return df.to_dict("records")


def als_liste(werte):
    """Macht aus einer Series oder Liste eine Liste, damit der Inhalt auch bei falschem Typ verglichen wird."""
    try:
        return list(werte)
    except TypeError:
        return werte


def kunden_zufaellig(zufall, anzahl):
    """Erzeugt anzahl zufällige Kundendatensätze, Namen und Orte auch doppelt."""
    orte = ["Kassel", "Fulda", "Marburg", "Gießen", "Hanau"]
    namen = ["Weber GmbH", "Lindner KG", "Chen AG", "Arslan IT", "Novak OHG"]
    datensaetze = []
    for nummer in range(anzahl):
        name = zufall.choice(namen)
        datensaetze.append(
            {
                "kundennummer": zufall.randint(1, 10**6),
                "name": name,
                "ort": zufall.choice(orte),
                "email": f"kontakt{zufall.randint(0, 50)}@{name.split()[0].lower()}.example",
                "telefon": f"0{zufall.randint(100, 9999)} {zufall.randint(1, 99999)}",
            }
        )
    return datensaetze


# als_tabelle gibt einen DataFrame zurück
tabelle = als_tabelle(KUNDEN)
assert isinstance(tabelle, pd.DataFrame), (
    f"als_tabelle(kunden) ergibt ein Objekt vom Typ {type(tabelle).__name__}, erwartet war ein DataFrame.\n"
    "Tipp: pd.DataFrame(datensaetze) baut die Tabelle aus der Liste von Dictionaries."
)

# Die Tabelle hat eine Spalte je Schlüssel, in dieser Reihenfolge
tabelle = als_tabelle(KUNDEN)
assert list(tabelle.columns) == SPALTEN, f"Die Spalten von als_tabelle(kunden) sind {list(tabelle.columns)}, erwartet war {SPALTEN}."

# Die Tabelle hat eine Zeile je Datensatz mit den richtigen Werten
tabelle = als_tabelle(KUNDEN)
assert als_zeilen(tabelle) == KUNDEN, f"Die Zeilen von als_tabelle(kunden) sind {als_zeilen(tabelle)}, erwartet war {KUNDEN}."

# Drei andere Kunden, Reihenfolge bleibt (nicht fest hinschreiben!)
tabelle = als_tabelle(DREI)
assert als_zeilen(tabelle) == DREI, f"als_tabelle mit drei Kunden ergibt die Zeilen {als_zeilen(tabelle)}, erwartet war {DREI}."

# Ein einziger Datensatz
tabelle = als_tabelle(KUNDEN[:1])
assert len(tabelle) == 1 and als_zeilen(tabelle) == KUNDEN[:1], (
    f"als_tabelle mit einem Datensatz ergibt die Zeilen {als_zeilen(tabelle)}, erwartet war {KUNDEN[:1]}."
)

# adressliste gibt einen DataFrame zurück
ergebnis = adressliste(pd.DataFrame(KUNDEN))
assert isinstance(ergebnis, pd.DataFrame), (
    f"adressliste(tabelle) ergibt ein Objekt vom Typ {type(ergebnis).__name__}, erwartet war ein DataFrame.\n"
    'Tipp: Mit einer Liste in den eckigen Klammern, tabelle[["name", "ort"]], kommt ein DataFrame heraus.'
)

# adressliste hat genau die Spalten name und ort, in dieser Reihenfolge
ergebnis = adressliste(pd.DataFrame(KUNDEN))
assert list(ergebnis.columns) == ["name", "ort"], f"Die Spalten von adressliste(tabelle) sind {list(ergebnis.columns)}, erwartet war ['name', 'ort']."

# adressliste enthält die Namen und Orte aller Kunden
ergebnis = adressliste(pd.DataFrame(DREI))
erwartet = [{"name": zeile["name"], "ort": zeile["ort"]} for zeile in DREI]
assert als_zeilen(ergebnis) == erwartet, f"adressliste mit drei Kunden ergibt {als_zeilen(ergebnis)}, erwartet war {erwartet}."

# adressliste lässt die übergebene Tabelle unverändert
tabelle = pd.DataFrame(DREI)
adressliste(tabelle)
assert list(tabelle.columns) == SPALTEN and als_zeilen(tabelle) == DREI, (
    f"Nach adressliste(tabelle) hat die Tabelle die Spalten {list(tabelle.columns)}, erwartet waren weiter {SPALTEN}.\n"
    "Tipp: Löschen Sie keine Spalten aus der Tabelle, sondern wählen Sie die gewünschten aus."
)

# emails gibt eine gewöhnliche Liste zurück
ergebnis = emails(pd.DataFrame(KUNDEN))
assert type(ergebnis) is list, (
    f"emails(tabelle) ergibt ein Objekt vom Typ {type(ergebnis).__name__}, erwartet war eine Liste.\n"
    'Tipp: tabelle["email"] ist eine Series; .tolist() macht daraus eine Liste.'
)

# emails im Beispiel
ergebnis = als_liste(emails(pd.DataFrame(KUNDEN)))
assert ergebnis == ["info@weber.example", "post@lindner.example"], (
    f"emails(tabelle) ergibt {ergebnis!r}, erwartet war ['info@weber.example', 'post@lindner.example']."
)

# emails mit drei Kunden, Reihenfolge der Zeilen
ergebnis = als_liste(emails(pd.DataFrame(DREI)))
assert ergebnis == ["a@arslan.example", "b@berg.example", "c@chen.example"], (
    f"emails mit drei Kunden ergibt {ergebnis!r}, erwartet war ['a@arslan.example', 'b@berg.example', 'c@chen.example']."
)

# Doppelte E-Mail-Adressen bleiben doppelt
doppelt = KUNDEN + [dict(KUNDEN[0], kundennummer=1003)]
ergebnis = als_liste(emails(pd.DataFrame(doppelt)))
assert ergebnis == ["info@weber.example", "post@lindner.example", "info@weber.example"], (
    f"emails mit einer doppelten Adresse ergibt {ergebnis!r}, erwartet war "
    "['info@weber.example', 'post@lindner.example', 'info@weber.example']."
)

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar(f"{SPALTEN}\n['info@weber.example', 'post@lindner.example']"), (
    f"Erwartete Ausgabe:\n{SPALTEN}\n['info@weber.example', 'post@lindner.example']\nIhr Programm:\n{AUSGABE}"
)

# Viele zufällige Kundenlisten, alle drei Funktionen hintereinander
zufall = Zufall(3038)
for runde in range(60):
    datensaetze = kunden_zufaellig(zufall, zufall.randint(1, 12))
    tabelle = als_tabelle(datensaetze)
    assert als_zeilen(tabelle) == datensaetze, f"als_tabelle({datensaetze}) ergibt die Zeilen {als_zeilen(tabelle)}."
    adressen = als_zeilen(adressliste(tabelle))
    erwartet = [{"name": zeile["name"], "ort": zeile["ort"]} for zeile in datensaetze]
    assert adressen == erwartet, f"adressliste mit den Kunden {datensaetze} ergibt {adressen}, erwartet war {erwartet}."
    adressen_mail = als_liste(emails(tabelle))
    erwartet = [zeile["email"] for zeile in datensaetze]
    assert adressen_mail == erwartet, f"emails mit den Kunden {datensaetze} ergibt {adressen_mail}, erwartet war {erwartet}."

# Obere Grenze: 5000 Kunden
datensaetze = kunden_zufaellig(zufall, 5000)
tabelle = als_tabelle(datensaetze)
ergebnis = (len(tabelle), list(adressliste(tabelle).columns), als_liste(emails(tabelle)) == [zeile["email"] for zeile in datensaetze])
assert ergebnis == (5000, ["name", "ort"], True), (
    f"Bei 5000 Kunden: erwartet 5000 Zeilen, Adressliste mit ['name', 'ort'] und alle Adressen in der richtigen "
    f"Reihenfolge; bekommen {ergebnis[0]} Zeilen, Spalten {ergebnis[1]}, Adressen richtig: {ergebnis[2]}."
)
