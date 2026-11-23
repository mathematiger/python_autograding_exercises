# Automatisch erzeugt aus lehrkraft/muster/4_045_stoerungscodes.py - nicht von Hand ändern.
# vorlage-hash: 4e5cb9803bf325b0
# text-hash: b2117bc6588243ca
# thema: datenanalyse
# inhalt: pandas: merge

import pandas as pd

STOERUNGEN = [
    {"id": 1, "host": "web01", "code": "NET07"},
    {"id": 2, "host": "db02", "code": "DSK01"},
    {"id": 3, "host": "web01", "code": "APP99"},
    {"id": 4, "host": "web02", "code": "NET07"},
]
KATALOG = [
    {"code": "DSK01", "ursache": "Hardware", "schwere": 3},
    {"code": "NET07", "ursache": "Netz", "schwere": 2},
    {"code": "MEM02", "ursache": "Hardware", "schwere": 2},
]


def stoerungstabelle(zeilen):
    """Baut den DataFrame der Störungen, auch wenn zeilen leer ist."""
    return pd.DataFrame(zeilen, columns=["id", "host", "code"])


def katalogtabelle(zeilen):
    """Baut den DataFrame des Katalogs, auch wenn zeilen leer ist."""
    return pd.DataFrame(zeilen, columns=["code", "ursache", "schwere"])


def ergebnis_von(funktion, stoerungen, katalog):
    """Ruft die Funktion mit neuen Tabellen auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(stoerungstabelle(stoerungen), katalogtabelle(katalog))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def zeilen_von(ergebnis):
    """Die Zeilen eines DataFrames als Liste von Dictionaries; sonst eine Beschreibung."""
    if not isinstance(ergebnis, pd.DataFrame):
        return f"keinen DataFrame, sondern {type(ergebnis).__name__}: {ergebnis!r}"
    return ergebnis.to_dict("records")


def vergleich_ursache(stoerungen, katalog):
    """Vergleichslösung mit einem Dictionary vom Code zur Katalogzeile."""
    nach_code = {zeile["code"]: zeile for zeile in katalog}
    return [{**zeile, "ursache": nach_code[zeile["code"]]["ursache"], "schwere": nach_code[zeile["code"]]["schwere"]}
            for zeile in stoerungen if zeile["code"] in nach_code]


def vergleich_zaehlen(stoerungen, katalog):
    """Vergleichslösung für je_ursache mit einem Dictionary."""
    nach_code = {zeile["code"]: zeile["ursache"] for zeile in katalog}
    anzahl = {}
    for zeile in stoerungen:
        ursache = nach_code.get(zeile["code"], "unbekannt")
        anzahl[ursache] = anzahl.get(ursache, 0) + 1
    return anzahl


def zufallsdaten(zufall, anzahl_stoerungen, anzahl_codes):
    """Erzeugt zufällige Störungen und einen Katalog, der nur einen Teil der Codes kennt."""
    codes = [f"C{nummer:03d}" for nummer in range(anzahl_codes)]
    katalog = [
        {"code": code, "ursache": zufall.choice(["Hardware", "Netz", "Software", "Strom"]), "schwere": zufall.randint(1, 3)}
        for code in zufall.sample(codes, zufall.randint(0, len(codes)))
    ]
    stoerungen = [
        {"id": nummer, "host": zufall.choice(["web01", "web02", "db01"]), "code": zufall.choice(codes + ["X999"])}
        for nummer in zufall.sample(range(1, 10**6), anzahl_stoerungen)
    ]
    return stoerungen, katalog


# mit_ursache im Beispiel: die Ursachen
ergebnis = ergebnis_von(mit_ursache, STOERUNGEN, KATALOG)
werte = ergebnis["ursache"].tolist() if isinstance(ergebnis, pd.DataFrame) and "ursache" in ergebnis.columns else ergebnis
assert werte == ["Netz", "Hardware", "Netz"], (
    f'mit_ursache(stoerungen, katalog)["ursache"] ergibt {werte!r}, erwartet war ["Netz", "Hardware", "Netz"].\n'
    'Tipp: stoerungen.merge(katalog, on="code") verknüpft beide Tabellen über den Code.'
)

# mit_ursache im Beispiel: alle Spalten und Werte
ergebnis = zeilen_von(ergebnis_von(mit_ursache, STOERUNGEN, KATALOG))
erwartet = vergleich_ursache(STOERUNGEN, KATALOG)
assert ergebnis == erwartet, f"mit_ursache(stoerungen, katalog) ergibt {ergebnis}, erwartet war {erwartet}."

# mit_ursache: Störungen ohne Katalogeintrag fallen weg, Katalogcodes ohne Störung auch
ergebnis = zeilen_von(ergebnis_von(mit_ursache, STOERUNGEN, KATALOG))
ids = [zeile["id"] for zeile in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert ids == [1, 2, 4], (
    f"mit_ursache enthält die Störungen {ids}, erwartet waren [1, 2, 4] (APP99 steht nicht im Katalog).\n"
    'Tipp: how="inner" behält nur Zeilen, deren Code in beiden Tabellen steht; how="left" behält alle Störungen.'
)

# mit_ursache mit anderen Daten (nicht fest hinschreiben!)
stoerungen = [{"id": 7, "host": "fw01", "code": "PWR01"}, {"id": 3, "host": "fw02", "code": "PWR01"}]
katalog = [{"code": "PWR01", "ursache": "Strom", "schwere": 3}]
ergebnis = zeilen_von(ergebnis_von(mit_ursache, stoerungen, katalog))
erwartet = vergleich_ursache(stoerungen, katalog)
assert ergebnis == erwartet, f"mit_ursache für zwei PWR01-Störungen ergibt {ergebnis}, erwartet war {erwartet}."

# mit_ursache mit leerem Katalog und ohne Störungen
ergebnis = [len(zeilen_von(ergebnis_von(mit_ursache, STOERUNGEN, []))), len(zeilen_von(ergebnis_von(mit_ursache, [], KATALOG)))]
assert ergebnis == [0, 0], f"mit_ursache mit leerem Katalog bzw. ohne Störungen hat {ergebnis} Zeilen, erwartet war [0, 0]."

# ohne_eintrag im Beispiel
ergebnis = ergebnis_von(ohne_eintrag, STOERUNGEN, KATALOG)
assert ergebnis == ["APP99"], (
    f"ohne_eintrag(stoerungen, katalog) ergibt {ergebnis!r}, erwartet war ['APP99'].\n"
    'Tipp: merge(..., how="left", indicator=True) und dann die Zeilen mit _merge == "left_only".'
)

# ohne_eintrag: sortiert, jeder Code einmal
stoerungen = [{"id": nummer, "host": "h", "code": code} for nummer, code in enumerate(["ZZ1", "AA1", "ZZ1", "NET07", "AA1"])]
ergebnis = ergebnis_von(ohne_eintrag, stoerungen, KATALOG)
assert ergebnis == ["AA1", "ZZ1"], f"ohne_eintrag für die Codes ZZ1, AA1, ZZ1, NET07, AA1 ergibt {ergebnis!r}, erwartet war ['AA1', 'ZZ1']."

# ohne_eintrag gibt eine gewöhnliche Liste zurück
ergebnis = ergebnis_von(ohne_eintrag, STOERUNGEN, KATALOG)
assert type(ergebnis) is list, f"ohne_eintrag gibt {type(ergebnis).__name__} zurück, erwartet war eine Liste (sorted(...) liefert eine)."

# ohne_eintrag: alle Codes bekannt, leerer Katalog, keine Störungen
ergebnis = [
    ergebnis_von(ohne_eintrag, STOERUNGEN[:2], KATALOG),
    ergebnis_von(ohne_eintrag, STOERUNGEN, []),
    ergebnis_von(ohne_eintrag, [], KATALOG),
]
assert ergebnis == [[], ["APP99", "DSK01", "NET07"], []], (
    f"ohne_eintrag mit nur bekannten Codes, mit leerem Katalog und ohne Störungen ergibt {ergebnis!r}, "
    "erwartet war [[], ['APP99', 'DSK01', 'NET07'], []]."
)

# je_ursache im Beispiel
ergebnis = ergebnis_von(je_ursache, STOERUNGEN, KATALOG)
assert ergebnis == {"Hardware": 1, "Netz": 2, "unbekannt": 1}, (
    f"je_ursache(stoerungen, katalog) ergibt {ergebnis!r}, erwartet war {{'Hardware': 1, 'Netz': 2, 'unbekannt': 1}}.\n"
    'Tipp: Mit how="left" bleiben alle Störungen; fillna("unbekannt") ersetzt die fehlenden Ursachen.'
)

# je_ursache: mehrere Codes mit derselben Ursache
katalog = KATALOG + [{"code": "APP99", "ursache": "Software", "schwere": 1}]
stoerungen = STOERUNGEN + [{"id": 5, "host": "db01", "code": "MEM02"}]
ergebnis = ergebnis_von(je_ursache, stoerungen, katalog)
assert ergebnis == {"Hardware": 2, "Netz": 2, "Software": 1}, (
    f"je_ursache mit DSK01 und MEM02 (beide Hardware) ergibt {ergebnis!r}, erwartet war {{'Hardware': 2, 'Netz': 2, 'Software': 1}}."
)

# je_ursache: leerer Katalog und keine Störungen
ergebnis = [ergebnis_von(je_ursache, STOERUNGEN, []), ergebnis_von(je_ursache, [], KATALOG)]
assert ergebnis == [{"unbekannt": 4}, {}], (
    f"je_ursache mit leerem Katalog und ohne Störungen ergibt {ergebnis!r}, erwartet war [{{'unbekannt': 4}}, {{}}]."
)

# Die übergebenen Tabellen bleiben unverändert
stoerungen_test, katalog_test = stoerungstabelle(STOERUNGEN), katalogtabelle(KATALOG)
for funktion in [mit_ursache, ohne_eintrag, je_ursache]:
    try:
        funktion(stoerungen_test, katalog_test)
    except Exception:
        pass
assert zeilen_von(stoerungen_test) == STOERUNGEN and zeilen_von(katalog_test) == KATALOG, (
    "Nach den drei Aufrufen haben sich die übergebenen Tabellen verändert; erwartet war, dass sie bleiben, wie sie waren."
)

# merge wird benutzt
assert verwendet("merge"), "Verknüpfen Sie die Tabellen mit merge."

# Die Ausgabe des Programms
erwartet = "['Netz', 'Hardware', 'Netz']\n['APP99']\n[('Hardware', 1), ('Netz', 2), ('unbekannt', 1)]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Störungen und Kataloge: mit_ursache
zufall = Zufall(4045)
faelle = []
for _ in range(80):
    faelle.append(zufallsdaten(zufall, zufall.randint(0, 12), zufall.randint(1, 6)))
for stoerungen, katalog in faelle:
    ergebnis = zeilen_von(ergebnis_von(mit_ursache, stoerungen, katalog))
    erwartet = vergleich_ursache(stoerungen, katalog)
    assert ergebnis == erwartet, f"Bei den Störungen {stoerungen} und dem Katalog {katalog} ergibt mit_ursache {ergebnis}, erwartet war {erwartet}."

# Viele zufällige Störungen und Kataloge: ohne_eintrag
for stoerungen, katalog in faelle:
    bekannt = {zeile["code"] for zeile in katalog}
    ergebnis = ergebnis_von(ohne_eintrag, stoerungen, katalog)
    erwartet = sorted({zeile["code"] for zeile in stoerungen} - bekannt)
    assert ergebnis == erwartet, (
        f"Bei den Störungen {stoerungen} und dem Katalog {katalog} ergibt ohne_eintrag {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Viele zufällige Störungen und Kataloge: je_ursache
for stoerungen, katalog in faelle:
    ergebnis = ergebnis_von(je_ursache, stoerungen, katalog)
    erwartet = vergleich_zaehlen(stoerungen, katalog)
    assert ergebnis == erwartet, (
        f"Bei den Störungen {stoerungen} und dem Katalog {katalog} ergibt je_ursache {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Obere Grenze: mit_ursache mit 50 000 Störungen und 1000 Katalogeinträgen
stoerungen, katalog = zufallsdaten(zufall, 50000, 1000)
ergebnis = zeilen_von(ergebnis_von(mit_ursache, stoerungen, katalog))
assert ergebnis == vergleich_ursache(stoerungen, katalog), (
    "Bei 50 000 Störungen und 1000 Katalogeinträgen stimmt das Ergebnis von mit_ursache nicht."
)

# Obere Grenze: je_ursache mit 50 000 Störungen und 1000 Katalogeinträgen
ergebnis = ergebnis_von(je_ursache, stoerungen, katalog)
assert ergebnis == vergleich_zaehlen(stoerungen, katalog), (
    "Bei 50 000 Störungen und 1000 Katalogeinträgen stimmt das Ergebnis von je_ursache nicht."
)
