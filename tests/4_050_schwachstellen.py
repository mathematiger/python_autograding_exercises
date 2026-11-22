# Automatisch erzeugt aus lehrkraft/muster/4_050_schwachstellen.py - nicht von Hand ändern.
# vorlage-hash: 1e3d1162b586bda5
# text-hash: 35bd52e33673dfa8
# thema: datenanalyse
# inhalt: pandas: pivot_table

import math

import pandas as pd

SPALTEN = ["system", "schweregrad", "tage_offen"]
GRADE = ["niedrig", "mittel", "hoch", "kritisch"]
BEISPIEL = [
    {"system": "web01", "schweregrad": "hoch", "tage_offen": 12},
    {"system": "db01", "schweregrad": "kritisch", "tage_offen": 3},
    {"system": "web01", "schweregrad": "hoch", "tage_offen": 5},
    {"system": "web01", "schweregrad": "niedrig", "tage_offen": 40},
]


def tabelle(zeilen):
    """Baut einen DataFrame mit den drei Spalten."""
    return pd.DataFrame(zeilen, columns=SPALTEN)


def ergebnis_von(funktion, zeilen):
    """Ruft die Funktion mit einer neuen Tabelle auf; ein Fehler oder etwas anderes als ein DataFrame wird als Text beschrieben."""
    try:
        ergebnis = funktion(tabelle(zeilen))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"
    if not isinstance(ergebnis, pd.DataFrame):
        return f"keinen DataFrame, sondern {type(ergebnis).__name__}: {ergebnis!r}"
    return ergebnis


def zellen(ergebnis):
    """Die Zellen als Dictionary Zeile → {Spalte: Wert}; NaN wird None, ganze Kommazahlen werden int."""
    if isinstance(ergebnis, str):
        return ergebnis
    zeilen = {}
    for zeile, werte in ergebnis.to_dict("index").items():
        zeilen[zeile] = {}
        for spalte, wert in werte.items():
            if isinstance(wert, float) and math.isnan(wert):
                wert = None
            elif isinstance(wert, float) and wert == int(wert):
                wert = int(wert)
            zeilen[zeile][spalte] = wert
        zeilen[zeile] = dict(zeilen[zeile])
    return zeilen


def aufbau(ergebnis):
    """Die Zeilen- und Spaltennamen in ihrer Reihenfolge."""
    if isinstance(ergebnis, str):
        return ergebnis
    return (list(ergebnis.index), list(ergebnis.columns))


def vergleich_anzahl(zeilen):
    """Vergleichslösung mit Dictionaries."""
    systeme = sorted({zeile["system"] for zeile in zeilen})
    matrix = {system: {grad: 0 for grad in GRADE} for system in systeme}
    for zeile in zeilen:
        matrix[zeile["system"]][zeile["schweregrad"]] += 1
    return matrix


def vergleich_dauer(zeilen):
    """Vergleichslösung: sammelt die Tage je Zelle und bildet den Mittelwert."""
    systeme = sorted({zeile["system"] for zeile in zeilen})
    tage = {system: {grad: [] for grad in GRADE} for system in systeme}
    for zeile in zeilen:
        tage[zeile["system"]][zeile["schweregrad"]].append(zeile["tage_offen"])
    return {
        system: {grad: (round(sum(werte) / len(werte), 1) if werte else None) for grad, werte in spalten.items()}
        for system, spalten in tage.items()
    }


def vergleich_gesamt(zeilen):
    """Vergleichslösung: Anzahlen mit Summenspalte und Summenzeile."""
    matrix = vergleich_anzahl(zeilen)
    for werte in matrix.values():
        werte["gesamt"] = sum(werte.values())
    matrix["gesamt"] = {spalte: sum(werte[spalte] for werte in matrix.values()) for spalte in GRADE + ["gesamt"]}
    return matrix


def dauer_passt(ergebnis, erwartet):
    """True, wenn die Mittelwerte bis auf die letzte Stelle stimmen (pandas und Python runden Grenzfälle verschieden)."""
    if not isinstance(ergebnis, dict) or list(ergebnis) != list(erwartet):
        return False
    for system, werte in erwartet.items():
        if list(ergebnis[system]) != list(werte):
            return False
        for grad, wert in werte.items():
            ist = ergebnis[system][grad]
            if (ist is None) != (wert is None):
                return False
            if wert is not None and abs(ist - wert) > 0.1001:
                return False
    return True


def zufallszeilen(zufall, anzahl, systeme):
    """Zufällige Funde auf den angegebenen Systemen."""
    return [
        {"system": zufall.choice(systeme), "schweregrad": zufall.choice(GRADE), "tage_offen": zufall.randint(0, 3650)}
        for _ in range(anzahl)
    ]


# anzahl_matrix im Beispiel: die Zahlen stimmen
ergebnis = ergebnis_von(anzahl_matrix, BEISPIEL)
erwartet = vergleich_anzahl(BEISPIEL)
gefunden = zellen(ergebnis)
assert isinstance(gefunden, dict) and all(
    gefunden.get(system, {}).get(grad, 0) == anzahl for system, werte in erwartet.items() for grad, anzahl in werte.items() if anzahl
), (
    f"anzahl_matrix(funde) ergibt\n{ergebnis}\nerwartet war {erwartet}.\n"
    'Tipp: funde.pivot_table(index="system", columns="schweregrad", values="tage_offen", aggfunc="count").'
)

# anzahl_matrix im Beispiel: 0 statt NaN in leeren Zellen
vorhanden = list(ergebnis.columns) if isinstance(ergebnis, pd.DataFrame) else []
assert gefunden == {system: {grad: anzahl for grad, anzahl in werte.items() if grad in vorhanden} for system, werte in erwartet.items()}, (
    f"anzahl_matrix(funde) ergibt\n{ergebnis}\nIn Zellen ohne Fund soll 0 stehen.\nTipp: fill_value=0."
)

# anzahl_matrix im Beispiel: alle vier Schweregrade in der verlangten Reihenfolge
assert aufbau(ergebnis) == (["db01", "web01"], GRADE) and gefunden == erwartet, (
    f"anzahl_matrix(funde) hat die Zeilen und Spalten {aufbau(ergebnis)}, erwartet war (['db01', 'web01'], {GRADE}).\n"
    f'Tipp: .reindex(columns=["niedrig", "mittel", "hoch", "kritisch"], fill_value=0) ergänzt "mittel" und ordnet die Spalten.'
)

# anzahl_matrix mit anderen Funden (nicht fest hinschreiben!)
zeilen = [
    {"system": "mail", "schweregrad": "mittel", "tage_offen": 1},
    {"system": "app2", "schweregrad": "mittel", "tage_offen": 9},
    {"system": "mail", "schweregrad": "mittel", "tage_offen": 2},
    {"system": "mail", "schweregrad": "kritisch", "tage_offen": 0},
    {"system": "app2", "schweregrad": "niedrig", "tage_offen": 4},
]
ergebnis = ergebnis_von(anzahl_matrix, zeilen)
assert zellen(ergebnis) == vergleich_anzahl(zeilen) and aufbau(ergebnis) == (["app2", "mail"], GRADE), (
    f"anzahl_matrix ergibt für {zeilen}\n{ergebnis}\nerwartet war {vergleich_anzahl(zeilen)}."
)

# anzahl_matrix mit einem einzigen Fund
zeilen = [{"system": "fw", "schweregrad": "hoch", "tage_offen": 7}]
ergebnis = ergebnis_von(anzahl_matrix, zeilen)
assert zellen(ergebnis) == {"fw": {"niedrig": 0, "mittel": 0, "hoch": 1, "kritisch": 0}} and aufbau(ergebnis) == (["fw"], GRADE), (
    f"anzahl_matrix mit einem einzigen Fund ergibt\n{ergebnis}\nerwartet war eine Zeile fw mit 0, 0, 1, 0."
)

# anzahl_matrix verändert die übergebene Tabelle nicht
funde = tabelle(BEISPIEL)
try:
    anzahl_matrix(funde)
except Exception:
    pass
assert funde.to_dict("records") == BEISPIEL and list(funde.columns) == SPALTEN, "anzahl_matrix hat die übergebene Tabelle verändert."

# anzahl_matrix benutzt pivot_table
assert verwendet("pivot_table"), "Benutzen Sie pivot_table, wie verlangt."

# mittlere_dauer im Beispiel
ergebnis = ergebnis_von(mittlere_dauer, BEISPIEL)
gefunden = zellen(ergebnis)
assert isinstance(gefunden, dict) and gefunden.get("web01", {}).get("hoch") == 8.5 and gefunden.get("db01", {}).get("kritisch") == 3, (
    f"mittlere_dauer(funde) ergibt\n{ergebnis}\nerwartet war bei web01/hoch 8.5 und bei db01/kritisch 3.0.\n"
    'Tipp: aggfunc="mean" bildet den Mittelwert von tage_offen.'
)

# mittlere_dauer: NaN, wo es keinen Fund gibt (nicht 0), alle vier Spalten
erwartet = vergleich_dauer(BEISPIEL)
assert dauer_passt(gefunden, erwartet) and aufbau(ergebnis) == (["db01", "web01"], GRADE), (
    f"mittlere_dauer(funde) ergibt\n{ergebnis}\nerwartet war {erwartet} (None steht für NaN).\n"
    "Tipp: Ohne fill_value bleibt NaN stehen; 0 Tage wäre ein echter Wert. reindex(columns=...) ergänzt fehlende Schweregrade mit NaN."
)

# mittlere_dauer rundet auf eine Nachkommastelle
zeilen = [
    {"system": "dns", "schweregrad": "mittel", "tage_offen": 1},
    {"system": "dns", "schweregrad": "mittel", "tage_offen": 1},
    {"system": "dns", "schweregrad": "mittel", "tage_offen": 2},
    {"system": "dns", "schweregrad": "kritisch", "tage_offen": 10},
    {"system": "ad", "schweregrad": "kritisch", "tage_offen": 0},
]
ergebnis = ergebnis_von(mittlere_dauer, zeilen)
assert dauer_passt(zellen(ergebnis), vergleich_dauer(zeilen)) and aufbau(ergebnis) == (["ad", "dns"], GRADE), (
    f"mittlere_dauer ergibt für {zeilen}\n{ergebnis}\nerwartet war {vergleich_dauer(zeilen)}.\n"
    "Tipp: (1 + 1 + 2) / 3 = 1.333…; runden Sie das Ergebnis mit .round(1)."
)

# mittlere_dauer: genau eine Nachkommastelle, nicht mehr
wert = zellen(ergebnis)["dns"]["mittel"] if isinstance(ergebnis, pd.DataFrame) else ergebnis
assert wert == 1.3, f"mittlere_dauer ergibt bei dns/mittel {wert!r}, erwartet war 1.3 (gerundet auf eine Nachkommastelle)."

# mit_gesamt im Beispiel: Summenzeile und Summenspalte
ergebnis = ergebnis_von(mit_gesamt, BEISPIEL)
gefunden = zellen(ergebnis)
assert isinstance(gefunden, dict) and gefunden.get("gesamt", {}).get("gesamt") == 4 and gefunden.get("web01", {}).get("gesamt") == 3, (
    f"mit_gesamt(funde) ergibt\n{ergebnis}\nerwartet war bei gesamt/gesamt 4 und bei web01/gesamt 3.\n"
    'Tipp: margins=True, margins_name="gesamt".'
)

# mit_gesamt im Beispiel: alle Zellen, Zeilen und Spalten
erwartet = vergleich_gesamt(BEISPIEL)
assert gefunden == erwartet and aufbau(ergebnis) == (["db01", "web01", "gesamt"], GRADE + ["gesamt"]), (
    f"mit_gesamt(funde) hat die Zeilen und Spalten {aufbau(ergebnis)} und ergibt\n{ergebnis}\nerwartet war {erwartet}.\n"
    'Tipp: Nehmen Sie "gesamt" mit in die Liste für reindex(columns=...).'
)

# mit_gesamt mit anderen Funden
zeilen = [
    {"system": "z", "schweregrad": "niedrig", "tage_offen": 1},
    {"system": "a", "schweregrad": "niedrig", "tage_offen": 2},
    {"system": "z", "schweregrad": "niedrig", "tage_offen": 3},
]
ergebnis = ergebnis_von(mit_gesamt, zeilen)
assert zellen(ergebnis) == vergleich_gesamt(zeilen) and aufbau(ergebnis) == (["a", "z", "gesamt"], GRADE + ["gesamt"]), (
    f"mit_gesamt ergibt für {zeilen}\n{ergebnis}\nerwartet war {vergleich_gesamt(zeilen)}."
)

# Die Ausgabe des Programms
erwartet = (
    "{'db01': {'niedrig': 0, 'mittel': 0, 'hoch': 0, 'kritisch': 1}, "
    "'web01': {'niedrig': 1, 'mittel': 0, 'hoch': 2, 'kritisch': 0}}\n8.5\n4"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Scans
zufall = Zufall(4050)
for _ in range(25):
    systeme = zufall.sample(["web01", "web02", "db01", "mail", "vpn", "dc1", "backup"], zufall.randint(1, 4))
    zeilen = zufallszeilen(zufall, zufall.randint(1, 12), systeme)
    ergebnis = ergebnis_von(anzahl_matrix, zeilen)
    assert zellen(ergebnis) == vergleich_anzahl(zeilen) and aufbau(ergebnis)[1] == GRADE, (
        f"anzahl_matrix ergibt für {zeilen}\n{ergebnis}\nerwartet war {vergleich_anzahl(zeilen)}."
    )
    ergebnis = ergebnis_von(mittlere_dauer, zeilen)
    assert dauer_passt(zellen(ergebnis), vergleich_dauer(zeilen)) and aufbau(ergebnis)[1] == GRADE, (
        f"mittlere_dauer ergibt für {zeilen}\n{ergebnis}\nerwartet war {vergleich_dauer(zeilen)}."
    )
    ergebnis = ergebnis_von(mit_gesamt, zeilen)
    assert zellen(ergebnis) == vergleich_gesamt(zeilen) and aufbau(ergebnis)[1] == GRADE + ["gesamt"], (
        f"mit_gesamt ergibt für {zeilen}\n{ergebnis}\nerwartet war {vergleich_gesamt(zeilen)}."
    )

# Obere Grenze: anzahl_matrix und mit_gesamt mit 20 000 Funden auf 200 Systemen
systeme = [f"srv{nummer:03d}" for nummer in range(200)]
zeilen = zufallszeilen(zufall, 20000, systeme)
ergebnis = [zellen(ergebnis_von(anzahl_matrix, zeilen)), zellen(ergebnis_von(mit_gesamt, zeilen))]
assert ergebnis == [vergleich_anzahl(zeilen), vergleich_gesamt(zeilen)], "Bei 20 000 Funden stimmen anzahl_matrix oder mit_gesamt nicht."
# Obere Grenze: mittlere_dauer mit 20 000 Funden
assert dauer_passt(zellen(ergebnis_von(mittlere_dauer, zeilen)), vergleich_dauer(zeilen)), "Bei 20 000 Funden stimmt mittlere_dauer nicht."
