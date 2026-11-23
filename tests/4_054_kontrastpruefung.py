# Automatisch erzeugt aus lehrkraft/muster/4_054_kontrastpruefung.py - nicht von Hand ändern.
# vorlage-hash: cf731580d478e790
# text-hash: 7979013da9030ed4
# thema: datenanalyse
# inhalt: assign, query, Method Chaining

import pandas as pd

SPALTEN = ["seite", "element", "vorne", "hinten", "pt", "fett"]
ERGEBNISSPALTEN = ["seite", "element", "kontrast", "mindest"]
BEISPIEL = [
    {"seite": "Anmeldung", "element": "Knopf", "vorne": 1.0, "hinten": 0.2, "pt": 14, "fett": True},
    {"seite": "Anmeldung", "element": "Hinweistext", "vorne": 0.3, "hinten": 1.0, "pt": 11, "fett": False},
    {"seite": "Anmeldung", "element": "Überschrift", "vorne": 0.1, "hinten": 0.9, "pt": 20, "fett": True},
    {"seite": "Start", "element": "Fußzeile", "vorne": 0.4, "hinten": 0.05, "pt": 10, "fett": False},
    {"seite": "Start", "element": "Link", "vorne": 0.15, "hinten": 1.0, "pt": 12, "fett": False},
    {"seite": "Start", "element": "Banner", "vorne": 1.0, "hinten": 0.45, "pt": 24, "fett": False},
]


def tabelle(zeilen):
    """Baut einen DataFrame mit den sechs Spalten, auch wenn zeilen leer ist."""
    df = pd.DataFrame(zeilen, columns=SPALTEN)
    return df.astype({"vorne": float, "hinten": float, "pt": int, "fett": bool})


def ergebnis_von(aufruf):
    """Führt den Aufruf aus; liefert den DataFrame oder einen Text, der den Fehler beschreibt."""
    try:
        ergebnis = aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"
    if not isinstance(ergebnis, pd.DataFrame):
        return f"keinen DataFrame, sondern {type(ergebnis).__name__}: {ergebnis!r}"
    return ergebnis


def kontrast(zeile):
    """Vergleichslösung: Kontrast einer Zeile mit Python gerechnet und gerundet."""
    hell = max(zeile["vorne"], zeile["hinten"])
    dunkel = min(zeile["vorne"], zeile["hinten"])
    return round((hell + 0.05) / (dunkel + 0.05), 2)


def mindest(zeile):
    """Vergleichslösung: 3.0 für großen Text, sonst 4.5."""
    if zeile["pt"] >= 18 or (zeile["pt"] >= 14 and zeile["fett"]):
        return 3.0
    return 4.5


def erwartete_verstoesse(zeilen):
    """Vergleichslösung für verstoesse als Liste von Dictionaries."""
    gefunden = []
    for zeile in zeilen:
        if kontrast(zeile) < mindest(zeile):
            gefunden.append({"seite": zeile["seite"], "element": zeile["element"], "kontrast": kontrast(zeile), "mindest": mindest(zeile)})
    return sorted(gefunden, key=lambda eintrag: (eintrag["seite"], eintrag["element"]))


def erwartet_knapp(zeilen, abstand):
    """Vergleichslösung für knapp als Liste von Dictionaries."""
    gefunden = []
    for zeile in zeilen:
        if mindest(zeile) <= kontrast(zeile) < mindest(zeile) + abstand:
            gefunden.append({"seite": zeile["seite"], "element": zeile["element"], "kontrast": kontrast(zeile), "mindest": mindest(zeile)})
    return sorted(gefunden, key=lambda eintrag: (eintrag["kontrast"], eintrag["element"]))


def gleich(ergebnis, erwartet):
    """True, wenn zwei Listen von Zeilen gleich sind; Kommazahlen dürfen um 0.011 abweichen."""
    if not isinstance(ergebnis, list) or len(ergebnis) != len(erwartet):
        return False
    for zeile, soll in zip(ergebnis, erwartet):
        if list(zeile) != list(soll):
            return False
        for spalte, wert in soll.items():
            if isinstance(wert, float):
                if abs(float(zeile[spalte]) - wert) > 0.011:
                    return False
            elif zeile[spalte] != wert:
                return False
    return True


def zeilen(df):
    """Der DataFrame als Liste von Dictionaries, oder der Text, wenn es keiner ist."""
    if isinstance(df, str):
        return df
    return df.to_dict("records")


# mit_kontrast im Beispiel: eine Spalte kontrast mit den Werten
df = tabelle(BEISPIEL)
ergebnis = ergebnis_von(lambda: mit_kontrast(df))
werte = ergebnis["kontrast"].tolist() if isinstance(ergebnis, pd.DataFrame) and "kontrast" in ergebnis else ergebnis
assert isinstance(werte, list) and gleich([{"k": float(w)} for w in werte], [{"k": w} for w in [4.2, 3.0, 6.33, 4.5, 5.25, 2.1]]), (
    f"mit_kontrast(elemente)['kontrast'] ergibt {werte!r}, erwartet war [4.2, 3.0, 6.33, 4.5, 5.25, 2.1].\n"
    "Tipp: Die hellere Farbe liefert d[['vorne', 'hinten']].max(axis=1), die dunklere .min(axis=1)."
)

# mit_kontrast: alle bisherigen Spalten bleiben, kontrast kommt als letzte dazu
assert isinstance(ergebnis, pd.DataFrame) and list(ergebnis.columns) == SPALTEN + ["kontrast"], (
    f"mit_kontrast gibt die Spalten {list(ergebnis.columns) if isinstance(ergebnis, pd.DataFrame) else ergebnis} zurück, "
    f"erwartet war {SPALTEN + ['kontrast']}.\nTipp: Hilfsspalten können Sie am Ende mit drop(columns=[...]) wieder entfernen."
)

# mit_kontrast verändert die übergebene Tabelle nicht
assert df.equals(tabelle(BEISPIEL)), (
    "mit_kontrast hat den übergebenen DataFrame verändert.\nTipp: assign gibt eine neue Tabelle zurück; df['kontrast'] = … ändert df selbst."
)

# mit_kontrast: auf zwei Nachkommastellen gerundet
zeile = {"seite": "Profil", "element": "Text", "vorne": 0.0, "hinten": 1.0 / 3.0, "pt": 12, "fett": False}
ergebnis = ergebnis_von(lambda: mit_kontrast(tabelle([zeile])))
wert = ergebnis["kontrast"].tolist() if isinstance(ergebnis, pd.DataFrame) and "kontrast" in ergebnis else ergebnis
assert wert == [kontrast(zeile)], f"Bei vorne 0.0 und hinten 1/3 ergibt mit_kontrast {wert!r}, erwartet war [{kontrast(zeile)}].\nTipp: .round(2)"

# mit_mindestwert im Beispiel: die Spalte gross
ergebnis = ergebnis_von(lambda: mit_mindestwert(tabelle(BEISPIEL)))
werte = [bool(w) for w in ergebnis["gross"].tolist()] if isinstance(ergebnis, pd.DataFrame) and "gross" in ergebnis else ergebnis
assert werte == [True, False, True, False, False, True], (
    f"mit_mindestwert(elemente)['gross'] ergibt {werte!r}, erwartet war [True, False, True, False, False, True].\n"
    "Tipp: Groß ist (pt >= 18) | ((pt >= 14) & fett)."
)

# mit_mindestwert im Beispiel: die Spalte mindest
werte = ergebnis["mindest"].tolist() if isinstance(ergebnis, pd.DataFrame) and "mindest" in ergebnis else ergebnis
assert werte == [3.0, 4.5, 3.0, 4.5, 4.5, 3.0], (
    f"mit_mindestwert(elemente)['mindest'] ergibt {werte!r}, erwartet war [3.0, 4.5, 3.0, 4.5, 4.5, 3.0].\n"
    "Tipp: 3.0 für großen, 4.5 für normalen Text, z. B. mit map({True: 3.0, False: 4.5})."
)

# mit_mindestwert: kontrast ist auch dabei
assert isinstance(ergebnis, pd.DataFrame) and "kontrast" in ergebnis, (
    f"mit_mindestwert gibt die Spalten {list(ergebnis.columns) if isinstance(ergebnis, pd.DataFrame) else ergebnis} zurück; "
    "erwartet war auch kontrast.\nTipp: Bauen Sie auf mit_kontrast(elemente) auf."
)

# mit_mindestwert verändert die übergebene Tabelle nicht
df = tabelle(BEISPIEL)
ergebnis_von(lambda: mit_mindestwert(df))
assert df.equals(tabelle(BEISPIEL)), "mit_mindestwert hat den übergebenen DataFrame verändert."

# verstoesse im Beispiel: die richtigen Elemente
ergebnis = zeilen(ergebnis_von(lambda: verstoesse(tabelle(BEISPIEL))))
gefunden = sorted(zeile.get("element") for zeile in ergebnis) if isinstance(ergebnis, list) else ergebnis
assert gefunden == ["Banner", "Hinweistext"], (
    f"verstoesse(elemente) findet {gefunden!r}, erwartet waren Banner und Hinweistext.\n"
    "Tipp: Großer Text braucht 3.0, normaler 4.5; filtern Sie mit query(\"kontrast < mindest\")."
)

# verstoesse im Beispiel: Spalten, Werte und Reihenfolge
erwartet = erwartete_verstoesse(BEISPIEL)
assert gleich(ergebnis, erwartet), (
    f"verstoesse(elemente) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: Wählen Sie am Ende mit [['seite', 'element', 'kontrast', 'mindest']] die Spalten aus und sortieren Sie nach seite und element."
)

# verstoesse: der Index beginnt bei 0
ergebnis = ergebnis_von(lambda: verstoesse(tabelle(BEISPIEL)))
index = list(ergebnis.index) if isinstance(ergebnis, pd.DataFrame) else ergebnis
assert index == [0, 1], f"Der Index von verstoesse(elemente) ist {index!r}, erwartet war [0, 1].\nTipp: reset_index(drop=True)"

# verstoesse mit anderen Elementen (nicht fest hinschreiben!)
andere = [
    {"seite": "Suche", "element": "Platzhalter", "vorne": 0.4, "hinten": 1.0, "pt": 12, "fett": False},
    {"seite": "Kontakt", "element": "Absenden", "vorne": 0.9, "hinten": 0.3, "pt": 16, "fett": True},
    {"seite": "Kontakt", "element": "Anrede", "vorne": 0.02, "hinten": 0.8, "pt": 12, "fett": False},
    {"seite": "Kontakt", "element": "Datenschutz", "vorne": 0.5, "hinten": 1.0, "pt": 9, "fett": True},
]
ergebnis = zeilen(ergebnis_von(lambda: verstoesse(tabelle(andere))))
assert gleich(ergebnis, erwartete_verstoesse(andere)), f"verstoesse ergibt {ergebnis!r}, erwartet war {erwartete_verstoesse(andere)}."

# verstoesse: 14 pt fett ist groß, 14 pt normal nicht, 18 pt immer
grenzfaelle = [
    {"seite": "A", "element": "fett14", "vorne": 1.0, "hinten": 0.25, "pt": 14, "fett": True},
    {"seite": "A", "element": "normal14", "vorne": 1.0, "hinten": 0.25, "pt": 14, "fett": False},
    {"seite": "A", "element": "normal18", "vorne": 1.0, "hinten": 0.25, "pt": 18, "fett": False},
    {"seite": "A", "element": "fett13", "vorne": 1.0, "hinten": 0.25, "pt": 13, "fett": True},
    {"seite": "A", "element": "normal17", "vorne": 1.0, "hinten": 0.25, "pt": 17, "fett": False},
]
ergebnis = zeilen(ergebnis_von(lambda: verstoesse(tabelle(grenzfaelle))))
assert gleich(ergebnis, erwartete_verstoesse(grenzfaelle)), (
    f"Bei Kontrast 3.5 ergibt verstoesse {ergebnis!r}, erwartet war {erwartete_verstoesse(grenzfaelle)}.\n"
    "Tipp: Groß ist (pt >= 18) | ((pt >= 14) & fett)."
)

# verstoesse: genau der Mindestwert ist kein Verstoß (Fußzeile mit 4.5)
ergebnis = zeilen(ergebnis_von(lambda: verstoesse(tabelle([BEISPIEL[3]]))))
assert ergebnis == [], (
    f"Die Fußzeile mit Kontrast 4.5 ergibt in verstoesse {ergebnis!r}, erwartet war [].\n"
    "Tipp: Vergleichen Sie den gerundeten Kontrast mit <, nicht <=."
)

# verstoesse: Schrift heller als Hintergrund und umgekehrt ergeben denselben Kontrast
gedreht = [dict(zeile, vorne=zeile["hinten"], hinten=zeile["vorne"]) for zeile in BEISPIEL]
ergebnis = zeilen(ergebnis_von(lambda: verstoesse(tabelle(gedreht))))
assert gleich(ergebnis, erwartete_verstoesse(BEISPIEL)), f"Mit vertauschten Farben ergibt verstoesse {ergebnis!r}, erwartet war dasselbe wie vorher."

# verstoesse: leere Tabelle
ergebnis = ergebnis_von(lambda: verstoesse(tabelle([])))
assert isinstance(ergebnis, pd.DataFrame) and len(ergebnis) == 0 and list(ergebnis.columns) == ERGEBNISSPALTEN, (
    f"verstoesse einer leeren Tabelle ergibt {ergebnis!r}, erwartet war ein leerer DataFrame mit den Spalten {ERGEBNISSPALTEN}."
)

# verstoesse verändert die übergebene Tabelle nicht
df = tabelle(BEISPIEL)
ergebnis_von(lambda: verstoesse(df))
assert df.equals(tabelle(BEISPIEL)), "verstoesse hat den übergebenen DataFrame verändert."

# knapp im Beispiel
ergebnis = zeilen(ergebnis_von(lambda: knapp(tabelle(BEISPIEL), 1.0)))
assert gleich(ergebnis, erwartet_knapp(BEISPIEL, 1.0)), (
    f"knapp(elemente, 1.0) ergibt {ergebnis!r}, erwartet war {erwartet_knapp(BEISPIEL, 1.0)}.\n"
    'Tipp: query("mindest <= kontrast < mindest + @abstand") holt abstand mit @ in die Bedingung.'
)

# knapp: der Index beginnt bei 0
ergebnis = ergebnis_von(lambda: knapp(tabelle(BEISPIEL), 1.0))
index = list(ergebnis.index) if isinstance(ergebnis, pd.DataFrame) else ergebnis
assert index == [0, 1], f"Der Index von knapp(elemente, 1.0) ist {index!r}, erwartet war [0, 1].\nTipp: reset_index(drop=True)"

# knapp mit einem anderen Abstand (nicht fest hinschreiben!)
ergebnis = zeilen(ergebnis_von(lambda: knapp(tabelle(BEISPIEL), 1.5)))
assert gleich(ergebnis, erwartet_knapp(BEISPIEL, 1.5)), f"knapp(elemente, 1.5) ergibt {ergebnis!r}, erwartet war {erwartet_knapp(BEISPIEL, 1.5)}."

# knapp: sortiert nach kontrast, bei Gleichstand nach element
gleichstand = [
    {"seite": "A", "element": "Zeile", "vorne": 1.0, "hinten": 0.15, "pt": 12, "fett": False},
    {"seite": "B", "element": "Spalte", "vorne": 1.0, "hinten": 0.15, "pt": 12, "fett": False},
    {"seite": "A", "element": "Kopf", "vorne": 1.0, "hinten": 0.17, "pt": 12, "fett": False},
]
ergebnis = zeilen(ergebnis_von(lambda: knapp(tabelle(gleichstand), 1.0)))
assert gleich(ergebnis, erwartet_knapp(gleichstand, 1.0)), (
    f"knapp ergibt {ergebnis!r}, erwartet war {erwartet_knapp(gleichstand, 1.0)}.\nTipp: sort_values(['kontrast', 'element'])"
)

# knapp mit Abstand 0 findet nichts
ergebnis = zeilen(ergebnis_von(lambda: knapp(tabelle(BEISPIEL), 0)))
assert ergebnis == [], f"knapp(elemente, 0) ergibt {ergebnis!r}, erwartet war []."

# knapp und verstoesse benutzen assign und query
assert verwendet("assign") and verwendet("query"), "Bauen Sie die Spalten mit assign und filtern Sie mit query."

# Die Ausgabe des Programms
erwartet = (
    "[4.2, 3.0, 6.33, 4.5, 5.25, 2.1]\n"
    "[{'seite': 'Anmeldung', 'element': 'Hinweistext', 'kontrast': 3.0, 'mindest': 4.5}, "
    "{'seite': 'Start', 'element': 'Banner', 'kontrast': 2.1, 'mindest': 3.0}]\n"
    "['Fußzeile', 'Link']"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

zufall = Zufall(4054)
berichte = []
for _ in range(40):
    elemente_zufall = []
    for nummer in range(zufall.randint(0, 15)):
        elemente_zufall.append(
            {
                "seite": zufall.choice(["Start", "Suche", "Profil", "Hilfe"]),
                "element": f"Element {nummer}",
                "vorne": zufall.random(),
                "hinten": zufall.random(),
                "pt": zufall.randint(6, 72),
                "fett": zufall.random() < 0.5,
            }
        )
    berichte.append((elemente_zufall, zufall.uniform(0, 5)))

# Viele zufällige Prüfberichte: verstoesse
for elemente_zufall, abstand in berichte:
    ergebnis = zeilen(ergebnis_von(lambda: verstoesse(tabelle(elemente_zufall))))
    erwartet = erwartete_verstoesse(elemente_zufall)
    assert gleich(ergebnis, erwartet), f"Für {elemente_zufall} ergibt verstoesse {ergebnis!r}, erwartet war {erwartet}."

# Viele zufällige Prüfberichte: knapp
for elemente_zufall, abstand in berichte:
    ergebnis = zeilen(ergebnis_von(lambda: knapp(tabelle(elemente_zufall), abstand)))
    erwartet = erwartet_knapp(elemente_zufall, abstand)
    assert gleich(ergebnis, erwartet), f"Für {elemente_zufall} ergibt knapp(…, {abstand}) {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 1000 Elemente
grosse = [
    {"seite": f"Seite {nummer % 37}", "element": f"E{nummer}", "vorne": zufall.random(), "hinten": zufall.random(), "pt": zufall.randint(6, 72), "fett": nummer % 2 == 0}
    for nummer in range(1000)
]
ergebnis = zeilen(ergebnis_von(lambda: verstoesse(tabelle(grosse))))
assert gleich(ergebnis, erwartete_verstoesse(grosse)), "Bei 1000 Elementen stimmt verstoesse nicht."
# Obere Grenze: knapp bei 1000 Elementen
ergebnis = zeilen(ergebnis_von(lambda: knapp(tabelle(grosse), 2.5)))
assert gleich(ergebnis, erwartet_knapp(grosse, 2.5)), "Bei 1000 Elementen stimmt knapp nicht."
