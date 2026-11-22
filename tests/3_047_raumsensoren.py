# Automatisch erzeugt aus lehrkraft/muster/3_047_raumsensoren.py - nicht von Hand ändern.
# vorlage-hash: 3eee9af9df8ce075
# text-hash: 77ff55c6f69df496
# thema: datenanalyse
# inhalt: pandas: fehlende Werte

import math

import pandas as pd

SPALTEN = ["sensor", "raum", "temperatur", "feuchte"]
BEISPIEL = [
    {"sensor": "T-01", "raum": "Labor", "temperatur": 21.5, "feuchte": 40.0},
    {"sensor": "T-02", "raum": None, "temperatur": 23.0, "feuchte": 55.0},
    {"sensor": "T-03", "raum": "Lager", "temperatur": None, "feuchte": 61.0},
    {"sensor": "T-04", "raum": "Büro", "temperatur": 19.0, "feuchte": None},
    {"sensor": "T-05", "raum": "Flur", "temperatur": 20.1, "feuchte": 45.0},
]


def tabelle(zeilen):
    """Baut einen DataFrame mit den vier Spalten, auch wenn zeilen leer ist."""
    return pd.DataFrame(zeilen, columns=SPALTEN)


def ergebnis_von(funktion, zeilen):
    """Ruft die Funktion mit einer neuen Tabelle auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(tabelle(zeilen))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def spalte(ergebnis, name):
    """Die Werte einer Spalte als Liste, fehlende Werte als None; sonst eine Beschreibung des Ergebnisses."""
    if not isinstance(ergebnis, pd.DataFrame):
        return f"kein DataFrame, sondern {type(ergebnis).__name__}: {ergebnis!r}"
    if name not in ergebnis.columns:
        return f"ein DataFrame ohne Spalte {name} (Spalten: {list(ergebnis.columns)})"
    werte = []
    for wert in ergebnis[name].tolist():
        if wert is None or (isinstance(wert, float) and math.isnan(wert)):
            werte.append(None)
        else:
            werte.append(wert)
    return werte


def fehlt(wert):
    """True, wenn der Wert in den Testdaten fehlt."""
    return wert is None


def vergleich_luecken(zeilen):
    """Vergleichslösung ohne pandas."""
    anzahlen = {name: 0 for name in SPALTEN}
    for zeile in zeilen:
        for name in SPALTEN:
            if fehlt(zeile[name]):
                anzahlen[name] += 1
    return anzahlen


def vergleich_vollstaendige(zeilen):
    """Vergleichslösung: die Sensoren der Zeilen ohne Lücke."""
    return [zeile["sensor"] for zeile in zeilen if not any(fehlt(zeile[name]) for name in SPALTEN)]


def vorhandene_temperaturen(zeilen):
    """Die Temperaturen, die nicht fehlen."""
    return [zeile["temperatur"] for zeile in zeilen if not fehlt(zeile["temperatur"])]


def meldung(name, zeilen, ergebnis, erwartet, tipp=""):
    """Fehlermeldung mit den Zeilen der Tabelle, dem Ergebnis und dem erwarteten Wert."""
    zeilen_text = "\n".join(f"    {zeile}" for zeile in zeilen[:8])
    if len(zeilen) > 8:
        zeilen_text += f"\n    … ({len(zeilen)} Zeilen)"
    return f"Für die Tabelle\n{zeilen_text}\nergibt {name} {ergebnis!r},\nerwartet war {erwartet!r}.{tipp}"


def temperaturen_passen(ergebnis, zeilen):
    """True, wenn vorhandene Temperaturen gleich bleiben und Lücken den gerundeten Mittelwert bekommen."""
    werte = spalte(ergebnis, "temperatur")
    if not isinstance(werte, list) or len(werte) != len(zeilen):
        return False
    vorhanden = vorhandene_temperaturen(zeilen)
    for wert, zeile in zip(werte, zeilen):
        if wert is None:
            return False
        if not fehlt(zeile["temperatur"]):
            if abs(wert - zeile["temperatur"]) > 1e-9:
                return False
            continue
        mittel = sum(vorhanden) / len(vorhanden)
        gerundet = abs(wert * 10 - round(wert * 10)) < 1e-6
        if not gerundet or abs(wert - mittel) > 0.05 + 1e-9:
            return False
    return True


# luecken im Beispiel: ein Dictionary mit allen vier Spalten
ergebnis = ergebnis_von(luecken, BEISPIEL)
assert isinstance(ergebnis, dict) and list(ergebnis) == SPALTEN, meldung(
    "luecken", BEISPIEL, ergebnis, vergleich_luecken(BEISPIEL),
    "\nTipp: messungen.isna().sum() zählt die Lücken je Spalte; mit .items() wird daraus ein Dictionary.",
)

# luecken im Beispiel: je eine Lücke in raum, temperatur und feuchte
assert ergebnis == vergleich_luecken(BEISPIEL), meldung("luecken", BEISPIEL, ergebnis, vergleich_luecken(BEISPIEL))

# luecken mit einer anderen Tabelle (nicht fest hinschreiben!)
zeilen = [
    {"sensor": "H-1", "raum": None, "temperatur": None, "feuchte": None},
    {"sensor": "H-2", "raum": None, "temperatur": 22.0, "feuchte": 50.0},
    {"sensor": "H-3", "raum": "Küche", "temperatur": 24.5, "feuchte": None},
]
ergebnis = ergebnis_von(luecken, zeilen)
assert ergebnis == vergleich_luecken(zeilen), meldung("luecken", zeilen, ergebnis, vergleich_luecken(zeilen))

# luecken: eine Tabelle ohne Lücken
zeilen = [{"sensor": "K-1", "raum": "Halle", "temperatur": 15.0, "feuchte": 70.0}]
ergebnis = ergebnis_von(luecken, zeilen)
assert ergebnis == vergleich_luecken(zeilen), meldung("luecken", zeilen, ergebnis, vergleich_luecken(zeilen))

# luecken: leere Tabelle
ergebnis = ergebnis_von(luecken, [])
assert ergebnis == vergleich_luecken([]), meldung("luecken", [], ergebnis, vergleich_luecken([]))

# vollstaendige im Beispiel: nur T-01 und T-05 sind ganz
ergebnis = ergebnis_von(vollstaendige, BEISPIEL)
assert spalte(ergebnis, "sensor") == ["T-01", "T-05"], meldung(
    "vollstaendige(...)[\"sensor\"]", BEISPIEL, spalte(ergebnis, "sensor"), ["T-01", "T-05"],
    "\nTipp: dropna() entfernt jede Zeile, in der irgendein Wert fehlt.",
)

# vollstaendige: eine Lücke nur im Raum zählt auch (nicht nur die Messwerte)
zeilen = [
    {"sensor": "A-1", "raum": None, "temperatur": 20.0, "feuchte": 30.0},
    {"sensor": "A-2", "raum": "Archiv", "temperatur": 18.0, "feuchte": 35.0},
    {"sensor": "A-3", "raum": "Archiv", "temperatur": 18.5, "feuchte": None},
]
ergebnis = ergebnis_von(vollstaendige, zeilen)
assert spalte(ergebnis, "sensor") == vergleich_vollstaendige(zeilen), meldung(
    "vollstaendige(...)[\"sensor\"]", zeilen, spalte(ergebnis, "sensor"), vergleich_vollstaendige(zeilen),
    "\nTipp: Ohne subset betrachtet dropna alle Spalten.",
)

# vollstaendige behält alle Spalten
assert isinstance(ergebnis, pd.DataFrame) and list(ergebnis.columns) == SPALTEN, (
    f"vollstaendige(...) hat die Spalten {list(ergebnis.columns) if isinstance(ergebnis, pd.DataFrame) else ergebnis!r}, "
    f"erwartet waren {SPALTEN}."
)

# vollstaendige: die einzige Zeile hat eine Lücke
zeilen = [{"sensor": "B-1", "raum": "Bad", "temperatur": None, "feuchte": 80.0}]
ergebnis = ergebnis_von(vollstaendige, zeilen)
assert spalte(ergebnis, "sensor") == [], meldung("vollstaendige(...)[\"sensor\"]", zeilen, spalte(ergebnis, "sensor"), [])

# vollstaendige: eine einzige Zeile ohne Lücke bleibt
zeilen = [{"sensor": "B-2", "raum": "Bad", "temperatur": 24.0, "feuchte": 80.0}]
ergebnis = ergebnis_von(vollstaendige, zeilen)
assert spalte(ergebnis, "sensor") == ["B-2"], meldung("vollstaendige(...)[\"sensor\"]", zeilen, spalte(ergebnis, "sensor"), ["B-2"])

# aufgefuellt im Beispiel: der fehlende Raum heißt "unbekannt"
ergebnis = ergebnis_von(aufgefuellt, BEISPIEL)
erwartet = ["Labor", "unbekannt", "Lager", "Büro", "Flur"]
assert spalte(ergebnis, "raum") == erwartet, meldung(
    "aufgefuellt(...)[\"raum\"]", BEISPIEL, spalte(ergebnis, "raum"), erwartet,
    '\nTipp: neu["raum"] = neu["raum"].fillna("unbekannt") auf einer Kopie.',
)

# aufgefuellt im Beispiel: die fehlende Temperatur wird zum Mittelwert 20.9
erwartet = [21.5, 23.0, 20.9, 19.0, 20.1]
werte = spalte(ergebnis, "temperatur")
assert isinstance(werte, list) and len(werte) == 5 and werte[2] is not None and abs(werte[2] - 20.875) < 0.06, meldung(
    "aufgefuellt(...)[\"temperatur\"]", BEISPIEL, werte, erwartet,
    "\nTipp: messungen[\"temperatur\"].mean() übergeht die Lücke; fillna(mittel) setzt den Wert ein.",
)

# aufgefuellt im Beispiel: der Mittelwert ist auf eine Nachkommastelle gerundet
assert temperaturen_passen(ergebnis, BEISPIEL), meldung(
    "aufgefuellt(...)[\"temperatur\"]", BEISPIEL, werte, erwartet, "\nTipp: round(mittel, 1) rundet auf eine Stelle."
)

# aufgefuellt im Beispiel: die fehlende Luftfeuchte bleibt leer, alles andere bleibt gleich
erwartet = [40.0, 55.0, 61.0, None, 45.0]
assert spalte(ergebnis, "feuchte") == erwartet and spalte(ergebnis, "sensor") == ["T-01", "T-02", "T-03", "T-04", "T-05"], meldung(
    "aufgefuellt(...)[\"feuchte\"]", BEISPIEL, spalte(ergebnis, "feuchte"), erwartet,
    "\nTipp: Füllen Sie nur raum und temperatur auf, nicht die ganze Tabelle.",
)

# aufgefuellt mit einer anderen Tabelle (nicht fest hinschreiben!)
zeilen = [
    {"sensor": "C-1", "raum": None, "temperatur": None, "feuchte": 50.0},
    {"sensor": "C-2", "raum": None, "temperatur": 30.0, "feuchte": None},
    {"sensor": "C-3", "raum": "Serverraum", "temperatur": 18.0, "feuchte": 20.0},
    {"sensor": "C-4", "raum": "Kantine", "temperatur": None, "feuchte": 50.0},
]
ergebnis = ergebnis_von(aufgefuellt, zeilen)
assert temperaturen_passen(ergebnis, zeilen) and spalte(ergebnis, "raum") == ["unbekannt", "unbekannt", "Serverraum", "Kantine"], meldung(
    "aufgefuellt(...)", zeilen, ergebnis, "raum ['unbekannt', 'unbekannt', 'Serverraum', 'Kantine'], temperatur [24.0, 30.0, 18.0, 24.0]"
)

# aufgefuellt: negative Temperaturen im Mittelwert
zeilen = [
    {"sensor": "D-1", "raum": "Kühlraum", "temperatur": -18.0, "feuchte": 90.0},
    {"sensor": "D-2", "raum": "Kühlraum", "temperatur": None, "feuchte": 90.0},
    {"sensor": "D-3", "raum": "Kühlraum", "temperatur": -20.5, "feuchte": 88.0},
    {"sensor": "D-4", "raum": "Kühlraum", "temperatur": -19.6, "feuchte": 88.0},
]
ergebnis = ergebnis_von(aufgefuellt, zeilen)
assert temperaturen_passen(ergebnis, zeilen), meldung("aufgefuellt(...)[\"temperatur\"]", zeilen, spalte(ergebnis, "temperatur"), [-18.0, -19.4, -20.5, -19.6])

# aufgefuellt: eine Tabelle ohne Lücken bleibt, wie sie ist
zeilen = [{"sensor": "E-1", "raum": "Foyer", "temperatur": 21.0, "feuchte": 42.0}]
ergebnis = ergebnis_von(aufgefuellt, zeilen)
assert spalte(ergebnis, "raum") == ["Foyer"] and spalte(ergebnis, "temperatur") == [21.0], meldung("aufgefuellt", zeilen, ergebnis, zeilen)

# Leere Tabelle: vollstaendige und aufgefuellt geben leere Tabellen zurück
ergebnisse = [ergebnis_von(vollstaendige, []), ergebnis_von(aufgefuellt, [])]
assert all(isinstance(e, pd.DataFrame) and len(e) == 0 for e in ergebnisse), (
    f"Für eine leere Tabelle ergeben vollstaendige und aufgefuellt {ergebnisse!r}, erwartet waren zwei leere DataFrames."
)

# Die übergebene Tabelle bleibt unverändert
original = tabelle(BEISPIEL)
for funktion in [luecken, vollstaendige, aufgefuellt]:
    try:
        funktion(original)
    except Exception:
        pass
assert int(original.isna().sum().sum()) == 3 and len(original) == 5, (
    f"Nach dem Aufruf der Funktionen hat die übergebene Tabelle {int(original.isna().sum().sum())} Lücken und "
    f"{len(original)} Zeilen, erwartet waren 3 Lücken und 5 Zeilen.\nTipp: Arbeiten Sie auf messungen.copy()."
)

# Viele zufällige Tabellen
zufall = Zufall(3047)
raeume = ["Labor", "Lager", "Büro", "Flur", "Halle"]


def zufallszeilen(anzahl):
    """Erzeugt anzahl Zeilen mit zufälligen Lücken; mindestens eine Temperatur ist vorhanden."""
    zeilen = []
    for nummer in range(anzahl):
        zeilen.append(
            {
                "sensor": f"S-{nummer}",
                "raum": None if zufall.random() < 0.2 else zufall.choice(raeume),
                "temperatur": None if zufall.random() < 0.2 else zufall.randint(-400, 600) / 10,
                "feuchte": None if zufall.random() < 0.2 else zufall.randint(0, 1000) / 10,
            }
        )
    if anzahl > 0 and not vorhandene_temperaturen(zeilen):
        zeilen[0]["temperatur"] = 20.0
    return zeilen


for _ in range(40):
    zeilen = zufallszeilen(zufall.randint(1, 10))
    ergebnis = ergebnis_von(luecken, zeilen)
    assert ergebnis == vergleich_luecken(zeilen), meldung("luecken", zeilen, ergebnis, vergleich_luecken(zeilen))
    ergebnis = spalte(ergebnis_von(vollstaendige, zeilen), "sensor")
    assert ergebnis == vergleich_vollstaendige(zeilen), meldung("vollstaendige(...)[\"sensor\"]", zeilen, ergebnis, vergleich_vollstaendige(zeilen))
    ergebnis = ergebnis_von(aufgefuellt, zeilen)
    erwartet_raum = ["unbekannt" if fehlt(zeile["raum"]) else zeile["raum"] for zeile in zeilen]
    assert temperaturen_passen(ergebnis, zeilen) and spalte(ergebnis, "raum") == erwartet_raum, meldung(
        "aufgefuellt(...)", zeilen, ergebnis, "Räume und Temperaturen aufgefüllt"
    )

# Obere Grenze: 10 000 Zeilen
zeilen = zufallszeilen(10000)
ergebnis = ergebnis_von(luecken, zeilen)
assert ergebnis == vergleich_luecken(zeilen), f"Bei 10 000 Zeilen ergibt luecken {ergebnis!r}, erwartet war {vergleich_luecken(zeilen)!r}."
# Obere Grenze: vollstaendige bei 10 000 Zeilen
assert spalte(ergebnis_von(vollstaendige, zeilen), "sensor") == vergleich_vollstaendige(zeilen), "Bei 10 000 Zeilen stimmt vollstaendige nicht."
# Obere Grenze: aufgefuellt bei 10 000 Zeilen
assert temperaturen_passen(ergebnis_von(aufgefuellt, zeilen), zeilen), "Bei 10 000 Zeilen stimmt aufgefuellt nicht."
