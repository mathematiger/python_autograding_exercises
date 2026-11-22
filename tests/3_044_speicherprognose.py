# Automatisch erzeugt aus lehrkraft/muster/3_044_speicherprognose.py - nicht von Hand ändern.
# vorlage-hash: adcbb063b0f594b8
# text-hash: f8c0ee4431e04beb
# thema: datenanalyse
# inhalt: pandas: neue Spalten berechnen

import pandas as pd

SPALTEN = ["volume", "kapazitaet_gb", "belegt_gb", "wachstum_gb"]
BEISPIEL = [
    {"volume": "vol-a", "kapazitaet_gb": 1000, "belegt_gb": 850, "wachstum_gb": 2},
    {"volume": "vol-b", "kapazitaet_gb": 2000, "belegt_gb": 500, "wachstum_gb": 120},
    {"volume": "vol-c", "kapazitaet_gb": 3000, "belegt_gb": 1000, "wachstum_gb": 10},
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
    """Die Werte einer Spalte als Liste; fehlt sie oder ist das Ergebnis kein DataFrame, eine Beschreibung."""
    if not isinstance(ergebnis, pd.DataFrame):
        return f"kein DataFrame, sondern {type(ergebnis).__name__}: {ergebnis!r}"
    if name not in ergebnis.columns:
        return f"ein DataFrame ohne Spalte {name} (Spalten: {list(ergebnis.columns)})"
    return ergebnis[name].tolist()


def vergleich_zeile(zeile):
    """Vergleichslösung für eine Zeile ohne pandas."""
    frei = zeile["kapazitaet_gb"] - zeile["belegt_gb"]
    belegung = round(zeile["belegt_gb"] / zeile["kapazitaet_gb"] * 100, 1)
    tage = frei // zeile["wachstum_gb"]
    return {**zeile, "frei_gb": frei, "belegung": belegung, "tage_bis_voll": tage, "kritisch": belegung >= 80 or tage < 14}


def passt(erhalten, erwartet):
    """True, wenn zwei Listen von Zeilen gleich sind; belegung darf um eine Rundungsstelle abweichen."""
    if not isinstance(erhalten, list) or len(erhalten) != len(erwartet):
        return False
    for zeile, soll in zip(erhalten, erwartet):
        # pandas und Python runden Grenzfälle wie 12.25 nicht immer gleich, beides ist richtig
        if not isinstance(zeile.get("belegung"), float) or abs(zeile["belegung"] - soll["belegung"]) > 0.1001:
            return False
        if {**zeile, "belegung": 0} != {**soll, "belegung": 0}:
            return False
    return True


def zufallsvolumes(zufall, anzahl):
    """Erzeugt anzahl zufällige Volumes innerhalb der Grenzen."""
    zeilen = []
    for nummer in range(anzahl):
        kapazitaet = zufall.choice([1, 100, 1000, zufall.randint(1, 100000)])
        belegt = zufall.choice([0, kapazitaet, kapazitaet * 4 // 5, zufall.randint(0, kapazitaet)])
        wachstum = zufall.choice([1, 1000, zufall.randint(1, 50)])
        zeilen.append({"volume": f"vol-{nummer}", "kapazitaet_gb": kapazitaet, "belegt_gb": belegt, "wachstum_gb": wachstum})
    return zeilen


# mit_belegung im Beispiel: freier Platz
ergebnis = ergebnis_von(mit_belegung, BEISPIEL)
assert spalte(ergebnis, "frei_gb") == [150, 1500, 2000], (
    f"mit_belegung(volumes) hat in frei_gb {spalte(ergebnis, 'frei_gb')}, erwartet war [150, 1500, 2000].\n"
    'Tipp: neu["frei_gb"] = neu["kapazitaet_gb"] - neu["belegt_gb"] rechnet für jede Zeile.'
)

# mit_belegung im Beispiel: Belegung in Prozent
ergebnis = ergebnis_von(mit_belegung, BEISPIEL)
werte = spalte(ergebnis, "belegung")
assert isinstance(werte, list) and [round(wert, 1) for wert in werte] == [85.0, 25.0, 33.3], (
    f"mit_belegung(volumes) hat in belegung {werte}, erwartet war [85.0, 25.0, 33.3].\n"
    "Tipp: belegt_gb geteilt durch kapazitaet_gb, mal 100."
)

# Die Belegung ist auf eine Nachkommastelle gerundet
ergebnis = ergebnis_von(mit_belegung, BEISPIEL)
assert spalte(ergebnis, "belegung") == [85.0, 25.0, 33.3], (
    f"mit_belegung(volumes) hat in belegung {spalte(ergebnis, 'belegung')}, erwartet war genau [85.0, 25.0, 33.3].\n"
    "Tipp: .round(1) rundet jede Zahl einer Spalte auf eine Nachkommastelle."
)

# mit_belegung behält die alten Spalten und hängt die neuen in der richtigen Reihenfolge an
ergebnis = ergebnis_von(mit_belegung, BEISPIEL)
spalten = list(ergebnis.columns) if isinstance(ergebnis, pd.DataFrame) else ergebnis
assert spalten == SPALTEN + ["frei_gb", "belegung"], (
    f"mit_belegung(volumes) hat die Spalten {spalten}, erwartet war {SPALTEN + ['frei_gb', 'belegung']}."
)

# mit_belegung mit anderen Werten (nicht fest hinschreiben!)
zeilen = [
    {"volume": "x", "kapazitaet_gb": 400, "belegt_gb": 100, "wachstum_gb": 5},
    {"volume": "y", "kapazitaet_gb": 3, "belegt_gb": 2, "wachstum_gb": 1},
]
ergebnis = ergebnis_von(mit_belegung, zeilen)
assert [spalte(ergebnis, "frei_gb"), spalte(ergebnis, "belegung")] == [[300, 1], [25.0, 66.7]], (
    f"Bei Volumes mit 100 von 400 und 2 von 3 GB ergibt mit_belegung frei_gb {spalte(ergebnis, 'frei_gb')} und "
    f"belegung {spalte(ergebnis, 'belegung')}, erwartet war [300, 1] und [25.0, 66.7]."
)

# Ein leeres und ein volles Volume
zeilen = [
    {"volume": "leer", "kapazitaet_gb": 500, "belegt_gb": 0, "wachstum_gb": 1},
    {"volume": "voll", "kapazitaet_gb": 500, "belegt_gb": 500, "wachstum_gb": 1},
]
ergebnis = ergebnis_von(mit_belegung, zeilen)
assert [spalte(ergebnis, "frei_gb"), spalte(ergebnis, "belegung")] == [[500, 0], [0.0, 100.0]], (
    f"Bei einem leeren und einem vollen Volume ergibt mit_belegung frei_gb {spalte(ergebnis, 'frei_gb')} und "
    f"belegung {spalte(ergebnis, 'belegung')}, erwartet war [500, 0] und [0.0, 100.0]."
)

# mit_belegung lässt die übergebene Tabelle unverändert
volumes_test = tabelle(BEISPIEL)
try:
    mit_belegung(volumes_test)
except Exception:
    pass
assert list(volumes_test.columns) == SPALTEN and volumes_test.to_dict("records") == BEISPIEL, (
    f"Nach mit_belegung(volumes) hat die übergebene Tabelle die Spalten {list(volumes_test.columns)}; "
    f"erwartet waren unverändert {SPALTEN}.\nTipp: Arbeiten Sie auf neu = volumes.copy()."
)

# mit_prognose im Beispiel: Tage bis voll
ergebnis = ergebnis_von(mit_prognose, BEISPIEL)
assert spalte(ergebnis, "tage_bis_voll") == [75, 12, 200], (
    f"mit_prognose(volumes) hat in tage_bis_voll {spalte(ergebnis, 'tage_bis_voll')}, erwartet war [75, 12, 200].\n"
    "Tipp: frei_gb // wachstum_gb teilt ganzzahlig, 1500 // 120 ist 12."
)

# mit_prognose im Beispiel: kritisch
ergebnis = ergebnis_von(mit_prognose, BEISPIEL)
assert spalte(ergebnis, "kritisch") == [True, True, False], (
    f"mit_prognose(volumes) hat in kritisch {spalte(ergebnis, 'kritisch')}, erwartet war [True, True, False].\n"
    "Tipp: vol-a ist zu 85 % belegt, vol-b ist in 12 Tagen voll; verknüpfen Sie beide Masken mit |."
)

# mit_prognose hängt vier Spalten in der richtigen Reihenfolge an
ergebnis = ergebnis_von(mit_prognose, BEISPIEL)
spalten = list(ergebnis.columns) if isinstance(ergebnis, pd.DataFrame) else ergebnis
erwartet = SPALTEN + ["frei_gb", "belegung", "tage_bis_voll", "kritisch"]
assert spalten == erwartet, f"mit_prognose(volumes) hat die Spalten {spalten}, erwartet war {erwartet}."

# kritisch an der Grenze: genau 80 Prozent belegt
zeilen = [{"volume": "z", "kapazitaet_gb": 1000, "belegt_gb": 800, "wachstum_gb": 1}]
ergebnis = ergebnis_von(mit_prognose, zeilen)
assert spalte(ergebnis, "kritisch") == [True], (
    f"Ein Volume mit genau 80 % Belegung und 200 Tagen Reserve hat in kritisch {spalte(ergebnis, 'kritisch')}, "
    "erwartet war [True] (mindestens 80)."
)

# kritisch nach dem Runden: 79,96 % ergibt belegung 80.0 und ist damit kritisch
zeilen = [{"volume": "z", "kapazitaet_gb": 10000, "belegt_gb": 7996, "wachstum_gb": 1}]
ergebnis = ergebnis_von(mit_prognose, zeilen)
assert spalte(ergebnis, "kritisch") == [True], (
    f"Ein Volume mit 7996 von 10 000 GB (belegung gerundet 80.0) und 2004 Tagen Reserve hat in kritisch "
    f"{spalte(ergebnis, 'kritisch')}, erwartet war [True].\n"
    "Tipp: Vergleichen Sie die gerundete Spalte belegung mit 80, nicht die ungerundete Rechnung."
)

# kritisch an der Grenze: genau 14 Tage sind noch nicht kritisch, 13 schon
zeilen = [
    {"volume": "p", "kapazitaet_gb": 1000, "belegt_gb": 300, "wachstum_gb": 50},
    {"volume": "q", "kapazitaet_gb": 1000, "belegt_gb": 300, "wachstum_gb": 51},
]
ergebnis = ergebnis_von(mit_prognose, zeilen)
assert [spalte(ergebnis, "tage_bis_voll"), spalte(ergebnis, "kritisch")] == [[14, 13], [False, True]], (
    f"Bei 700 GB frei und 50 bzw. 51 GB Wachstum ergibt mit_prognose tage_bis_voll {spalte(ergebnis, 'tage_bis_voll')} "
    f"und kritisch {spalte(ergebnis, 'kritisch')}, erwartet war [14, 13] und [False, True] (kleiner als 14)."
)

# Ein volles Volume hat 0 Tage Reserve
zeilen = [{"volume": "voll", "kapazitaet_gb": 10, "belegt_gb": 10, "wachstum_gb": 1000}]
ergebnis = ergebnis_von(mit_prognose, zeilen)
assert [spalte(ergebnis, "tage_bis_voll"), spalte(ergebnis, "kritisch")] == [[0], [True]], (
    f"Bei einem vollen Volume ergibt mit_prognose tage_bis_voll {spalte(ergebnis, 'tage_bis_voll')} und kritisch "
    f"{spalte(ergebnis, 'kritisch')}, erwartet war [0] und [True]."
)

# mit_prognose lässt die übergebene Tabelle unverändert
volumes_test = tabelle(BEISPIEL)
try:
    mit_prognose(volumes_test)
except Exception:
    pass
assert list(volumes_test.columns) == SPALTEN and volumes_test.to_dict("records") == BEISPIEL, (
    f"Nach mit_prognose(volumes) hat die übergebene Tabelle die Spalten {list(volumes_test.columns)}; "
    f"erwartet waren unverändert {SPALTEN}."
)

# Eine leere Tabelle
ergebnis = [len(ergebnis_von(mit_belegung, [])), len(ergebnis_von(mit_prognose, []))]
spalten = ergebnis_von(mit_prognose, [])
spalten = list(spalten.columns) if isinstance(spalten, pd.DataFrame) else spalten
assert ergebnis == [0, 0] and spalten == SPALTEN + ["frei_gb", "belegung", "tage_bis_voll", "kritisch"], (
    f"Mit einer leeren Tabelle haben die Ergebnisse {ergebnis} Zeilen und die Spalten {spalten}; "
    "erwartet waren 0 Zeilen mit allen acht Spalten."
)

# Ohne Schleife über die Zeilen
benutzt = [name for name in ["for", "while", "iterrows", "itertuples", "apply"] if verwendet(name)]
assert benutzt == [], f"Ihr Code verwendet {benutzt}. Rechnen Sie mit ganzen Spalten, ohne Schleife über die Zeilen."

# Die Ausgabe des Programms
erwartet = "[85.0, 25.0, 33.3]\n[75, 12, 200]\n[True, True, False]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Tabellen
zufall = Zufall(3044)
for _ in range(60):
    zeilen = zufallsvolumes(zufall, zufall.randint(0, 12))
    ergebnis = ergebnis_von(mit_prognose, zeilen)
    erwartet = [vergleich_zeile(zeile) for zeile in zeilen]
    erhalten = ergebnis.to_dict("records") if isinstance(ergebnis, pd.DataFrame) else ergebnis
    assert passt(erhalten, erwartet), f"Bei den Volumes {zeilen} ergibt mit_prognose {erhalten}, erwartet war {erwartet}."

# Obere Grenze: 10 000 Volumes
zeilen = zufallsvolumes(zufall, 10000)
ergebnis = ergebnis_von(mit_prognose, zeilen)
erhalten = ergebnis.to_dict("records") if isinstance(ergebnis, pd.DataFrame) else ergebnis
assert passt(erhalten, [vergleich_zeile(zeile) for zeile in zeilen]), "Bei 10 000 Volumes stimmt das Ergebnis von mit_prognose nicht."
