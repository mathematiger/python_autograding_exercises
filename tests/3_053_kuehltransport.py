# Automatisch erzeugt aus lehrkraft/muster/3_053_kuehltransport.py - nicht von Hand ändern.
# vorlage-hash: 2c80693ec4730836
# text-hash: 0d364dba91ffa1f3
# thema: datenanalyse
# inhalt: pandas: read_csv und astype

import io

import pandas as pd

KOPF = "logger;zeit;temperatur;tuer\n"
BEISPIEL = KOPF + "00731;08:00;-18,5;0\n00731;08:15;-12,0;1\n04120;08:00;-19,25;0\n"
SPALTEN = ["logger", "zeit", "temperatur", "tuer"]


def aufruf(funktion, argument):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(argument)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def spalte(ergebnis, name):
    """Die Werte einer Spalte als Liste; sonst eine Beschreibung, was stattdessen herauskam."""
    if not isinstance(ergebnis, pd.DataFrame):
        return f"(kein DataFrame, sondern {type(ergebnis).__name__}: {ergebnis!r})"
    if name not in ergebnis.columns:
        return f"(keine Spalte {name}, Spalten: {list(ergebnis.columns)})"
    return ergebnis[name].tolist()


def typ(ergebnis, name):
    """Der Datentyp einer Spalte als Text, oder eine Beschreibung, was stattdessen herauskam."""
    if not isinstance(ergebnis, pd.DataFrame) or name not in ergebnis.columns:
        return f"(keine Spalte {name})"
    return str(ergebnis[name].dtype)


def gerundet(werte):
    """Rundet Kommazahlen auf vier Stellen, damit float32 und float64 vergleichbar sind."""
    if not isinstance(werte, list):
        return werte
    return [round(float(wert), 4) for wert in werte]


def zeilen_text(zeilen):
    """Baut aus Tupeln (logger, zeit, temperatur, tuer) den CSV-Text des Gateways mit Dezimalkomma."""
    text = KOPF
    for logger, zeit, temperatur, tuer in zeilen:
        text += f"{logger};{zeit};{str(temperatur).replace('.', ',')};{tuer}\n"
    return text


def als_zeilen(df):
    """Die Zeilen eines DataFrames als Listen, temperatur auf vier Stellen gerundet; sonst eine Beschreibung."""
    if not isinstance(df, pd.DataFrame) or list(df.columns) != SPALTEN:
        return f"(kein DataFrame mit den Spalten {SPALTEN}: {df!r})"
    zeilen = []
    for logger, zeit, temperatur, tuer in df.values.tolist():
        zeilen.append([logger, zeit, round(float(temperatur), 4), tuer])
    return zeilen


def zufallszeilen(zufall, anzahl):
    """Erzeugt zufällige Zeilen innerhalb der Grenzen, Logger oft mit Nullen vorn."""
    zeilen = []
    for _ in range(anzahl):
        logger = f"{zufall.choice([0, 0, 1, 9]) * 10000 + zufall.randint(0, 9999):05}"
        zeit = f"{zufall.randint(0, 23):02}:{zufall.choice([0, 15, 30, 45]):02}"
        zeilen.append((logger, zeit, zufall.randint(-4000, 3000) / 100, zufall.randint(0, 1)))
    return zeilen


# lade_messungen im Beispiel: ein DataFrame mit drei Zeilen und vier Spalten
df = aufruf(lade_messungen, BEISPIEL)
assert isinstance(df, pd.DataFrame) and df.shape == (3, 4), (
    f"lade_messungen(text) ergibt {df!r},\nerwartet war ein DataFrame mit 3 Zeilen und 4 Spalten.\n"
    'Tipp: pd.read_csv(io.StringIO(text), sep=";") – ohne sep=";" landet alles in einer Spalte.'
)

# lade_messungen im Beispiel: die Spaltennamen
assert list(df.columns) == SPALTEN, f"Die Spalten heißen {list(df.columns)}, erwartet war {SPALTEN}."

# lade_messungen im Beispiel: temperatur als Zahl mit Dezimalkomma
assert spalte(df, "temperatur") == [-18.5, -12.0, -19.25], (
    f"Die Spalte temperatur ist {spalte(df, 'temperatur')!r}, erwartet war [-18.5, -12.0, -19.25].\n"
    'Tipp: Mit decimal="," liest pandas -18,5 als Zahl -18.5.'
)

# lade_messungen im Beispiel: tuer als ganze Zahl
assert spalte(df, "tuer") == [0, 1, 0], f"Die Spalte tuer ist {spalte(df, 'tuer')!r}, erwartet war [0, 1, 0]."

# lade_messungen im Beispiel: logger behält die Nullen vorn
assert spalte(df, "logger") == ["00731", "00731", "04120"], (
    f"Die Spalte logger ist {spalte(df, 'logger')!r}, erwartet war ['00731', '00731', '04120'].\n"
    'Tipp: Ohne dtype={"logger": str} rät pandas eine Zahl, und die Nullen vorn gehen verloren.'
)

# lade_messungen im Beispiel: zeit bleibt Text
assert spalte(df, "zeit") == ["08:00", "08:15", "08:00"], (
    f"Die Spalte zeit ist {spalte(df, 'zeit')!r}, erwartet war ['08:00', '08:15', '08:00']."
)

# lade_messungen mit anderen Zeilen (nicht fest hinschreiben!)
zeilen = [("00001", "23:45", -40.0, 1), ("99999", "00:00", 30.0, 0)]
df = aufruf(lade_messungen, zeilen_text(zeilen))
erwartet = [list(zeile) for zeile in zeilen]
assert als_zeilen(df) == erwartet, (
    f"lade_messungen für\n{zeilen_text(zeilen)}ergibt\n{df!r}\nerwartet waren die Zeilen {erwartet}."
)

# lade_messungen: Randfall nur Kopfzeile, eine leere Tabelle mit vier Spalten
df = aufruf(lade_messungen, KOPF)
assert isinstance(df, pd.DataFrame) and df.shape == (0, 4) and list(df.columns) == SPALTEN, (
    f"lade_messungen bei nur einer Kopfzeile ergibt {df!r}, erwartet war ein leerer DataFrame mit den Spalten {SPALTEN}."
)

# kompakt im Beispiel: tuer wird True und False
geladen = pd.read_csv(io.StringIO(BEISPIEL), sep=";", decimal=",", dtype={"logger": str})
ergebnis = aufruf(kompakt, geladen.copy())
assert spalte(ergebnis, "tuer") == [False, True, False], (
    f"kompakt(df)['tuer'] ist {spalte(ergebnis, 'tuer')!r}, erwartet war [False, True, False].\n"
    'Tipp: messungen.astype({"temperatur": "float32", "tuer": bool}) gibt eine neue Tabelle zurück.'
)

# kompakt im Beispiel: tuer hat den Datentyp bool
assert typ(ergebnis, "tuer") == "bool", f"Die Spalte tuer hat den Datentyp {typ(ergebnis, 'tuer')}, erwartet war bool."

# kompakt im Beispiel: temperatur behält die Werte
assert gerundet(spalte(ergebnis, "temperatur")) == [-18.5, -12.0, -19.25], (
    f"kompakt(df)['temperatur'] ist {spalte(ergebnis, 'temperatur')!r}, erwartet war [-18.5, -12.0, -19.25]."
)

# kompakt im Beispiel: temperatur hat den Datentyp float32
assert typ(ergebnis, "temperatur") == "float32", (
    f"Die Spalte temperatur hat den Datentyp {typ(ergebnis, 'temperatur')}, erwartet war float32.\n"
    'Tipp: astype("float32") als Text, denn float allein ist float64.'
)

# kompakt im Beispiel: logger und zeit bleiben, wie sie sind
assert spalte(ergebnis, "logger") == ["00731", "00731", "04120"] and spalte(ergebnis, "zeit") == ["08:00", "08:15", "08:00"], (
    f"kompakt(df) hat logger {spalte(ergebnis, 'logger')!r} und zeit {spalte(ergebnis, 'zeit')!r}; beide sollten bleiben."
)

# kompakt im Beispiel: dieselben Spalten in derselben Reihenfolge
assert isinstance(ergebnis, pd.DataFrame) and list(ergebnis.columns) == SPALTEN, (
    f"kompakt(df) hat die Spalten {spalte(ergebnis, '') if not isinstance(ergebnis, pd.DataFrame) else list(ergebnis.columns)}, "
    f"erwartet war {SPALTEN}."
)

# kompakt lässt die übergebene Tabelle unverändert
original = geladen.copy()
aufruf(kompakt, original)
assert typ(original, "tuer") == "int64" and typ(original, "temperatur") == "float64", (
    f"Nach kompakt(df) hat df die Typen tuer {typ(original, 'tuer')} und temperatur {typ(original, 'temperatur')}; "
    "erwartet waren unverändert int64 und float64.\nTipp: astype gibt eine neue Tabelle zurück; weisen Sie nichts an messungen zu."
)

# kompakt: Randfall leere Tabelle
leer = pd.DataFrame({"logger": pd.Series([], dtype=str), "zeit": pd.Series([], dtype=str),
                     "temperatur": pd.Series([], dtype=float), "tuer": pd.Series([], dtype=int)})
ergebnis = aufruf(kompakt, leer)
assert isinstance(ergebnis, pd.DataFrame) and len(ergebnis) == 0 and typ(ergebnis, "tuer") == "bool", (
    f"kompakt einer leeren Tabelle ergibt {ergebnis!r}, erwartet war eine leere Tabelle mit tuer als bool."
)

# Die Ausgabe des Programms
erwartet = "['00731', '00731', '04120']\n[-18.5, -12.0, -19.25]\n[False, True, False]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Exporte
zufall = Zufall(3053)
for _ in range(50):
    zeilen = zufallszeilen(zufall, zufall.randint(1, 8))
    text = zeilen_text(zeilen)
    df = aufruf(lade_messungen, text)
    erwartet = [list(zeile) for zeile in zeilen]
    assert als_zeilen(df) == erwartet, (
        f"lade_messungen für\n{text}ergibt\n{df!r}\nerwartet waren die Zeilen {erwartet}."
    )
    ergebnis = aufruf(kompakt, df)
    assert spalte(ergebnis, "tuer") == [zeile[3] == 1 for zeile in zeilen], f"kompakt für\n{text}ergibt tuer {spalte(ergebnis, 'tuer')!r}."
    assert gerundet(spalte(ergebnis, "temperatur")) == [zeile[2] for zeile in zeilen], (
        f"kompakt für\n{text}ergibt temperatur {spalte(ergebnis, 'temperatur')!r}."
    )

# Obere Grenze: 10 000 Zeilen
zeilen = zufallszeilen(zufall, 10000)
df = aufruf(lade_messungen, zeilen_text(zeilen))
assert spalte(df, "logger") == [zeile[0] for zeile in zeilen], "Bei 10 000 Zeilen stimmt die Spalte logger nicht."
ergebnis = aufruf(kompakt, df)
assert typ(ergebnis, "temperatur") == "float32" and len(ergebnis) == 10000, "Bei 10 000 Zeilen stimmt kompakt nicht."
