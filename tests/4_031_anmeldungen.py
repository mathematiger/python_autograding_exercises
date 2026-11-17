# Automatisch erzeugt aus lehrkraft/muster/4_031_anmeldungen.py - nicht von Hand ändern.
# vorlage-hash: b45786c0e17ca82c
# text-hash: 575872442d919222
# thema: datenanalyse
# inhalt: polars select, filter, with_columns

SCHEMA = {"benutzer": pl.String, "stunde": pl.Int64, "fehlversuche": pl.Int64}


def tabelle(zeilen):
    """Baut aus Tupeln (benutzer, stunde, fehlversuche) einen DataFrame mit festen Spaltentypen."""
    return pl.DataFrame(zeilen, schema=SCHEMA, orient="row")


def ist_nachts(stunde):
    """Vergleichslösung ohne polars: liegt die Stunde nachts?"""
    return stunde < 6 or stunde >= 22


def verdaechtig_von_hand(zeilen, schwelle):
    """Vergleichslösung ohne polars für verdaechtig, als Liste von Dictionaries."""
    ergebnis = []
    for benutzer, stunde, versuche in zeilen:
        if ist_nachts(stunde) and versuche >= schwelle:
            ergebnis.append({"benutzer": benutzer, "fehlversuche": versuche})
    return ergebnis


def kennzahlen_von_hand(zeilen):
    """Vergleichslösung ohne polars für kennzahlen, als Liste mit einem Dictionary."""
    versuche = [zeile[2] for zeile in zeilen]
    hoechstwert = max(versuche) if versuche else None
    betroffen = len([wert for wert in versuche if wert > 0])
    return [{"summe": sum(versuche), "hoechstwert": hoechstwert, "betroffen": betroffen}]


def als_text(wert):
    """Beschreibt ein Ergebnis für eine Fehlermeldung: DataFrames als to_dicts(), sonst repr."""
    if isinstance(wert, pl.DataFrame):
        return repr(wert.to_dicts())
    return f"{wert!r} (Typ {type(wert).__name__})"


BEISPIEL = [("anna", 3, 40), ("ben", 10, 2), ("anna", 23, 0), ("cem", 5, 12)]

# mit_nachtmarke gibt einen DataFrame zurück
ergebnis = mit_nachtmarke(tabelle(BEISPIEL))
assert isinstance(ergebnis, pl.DataFrame), (
    f"mit_nachtmarke gibt {als_text(ergebnis)} zurück, erwartet war ein polars-DataFrame.\n"
    "Tipp: with_columns ändert den DataFrame nicht, sondern gibt einen neuen zurück. Geben Sie ihn mit return zurück."
)

# mit_nachtmarke hängt die Spalte nachts hinten an
spalten = mit_nachtmarke(tabelle(BEISPIEL)).columns
assert spalten == ["benutzer", "stunde", "fehlversuche", "nachts"], (
    f"mit_nachtmarke liefert die Spalten {spalten}, erwartet waren ['benutzer', 'stunde', 'fehlversuche', 'nachts'].\n"
    'Tipp: with_columns(ausdruck.alias("nachts")) hängt eine Spalte mit diesem Namen an.'
)

# Das Beispiel: Stunden 3, 10, 23, 5 ergeben True, False, True, True
nachts = mit_nachtmarke(tabelle(BEISPIEL))["nachts"].to_list()
assert nachts == [True, False, True, True], (
    f"Für die Stunden [3, 10, 23, 5] ergibt die Spalte nachts {nachts}, erwartet war [True, False, True, True].\n"
    "Tipp: Nachts heißt stunde < 6 oder stunde >= 22: (pl.col(\"stunde\") < 6) | (pl.col(\"stunde\") >= 22)."
)

# Die übrigen Spalten bleiben unverändert
werte = mit_nachtmarke(tabelle(BEISPIEL)).select("benutzer", "stunde", "fehlversuche").rows()
assert werte == BEISPIEL, f"mit_nachtmarke verändert die übrigen Spalten: {werte}, erwartet war {BEISPIEL}."

# Grenzen der Nacht: 5 und 22 zählen dazu, 6 und 21 nicht
stunden = [0, 5, 6, 21, 22, 23]
nachts = mit_nachtmarke(tabelle([("x", stunde, 1) for stunde in stunden]))["nachts"].to_list()
erwartet = [True, True, False, False, True, True]
assert nachts == erwartet, (
    f"Für die Stunden {stunden} ergibt nachts {nachts}, erwartet war {erwartet}.\n"
    "Tipp: Vor 6 heißt < 6, ab 22 heißt >= 22."
)

# Der übergebene DataFrame bleibt unverändert
original = tabelle(BEISPIEL)
mit_nachtmarke(original)
assert original.columns == ["benutzer", "stunde", "fehlversuche"], (
    f"Nach mit_nachtmarke(protokoll) hat protokoll die Spalten {original.columns}; er darf nicht verändert werden."
)

# verdaechtig: das Beispiel aus der Aufgabe
ergebnis = verdaechtig(tabelle(BEISPIEL), 10)
erwartet = [{"benutzer": "anna", "fehlversuche": 40}, {"benutzer": "cem", "fehlversuche": 12}]
assert isinstance(ergebnis, pl.DataFrame) and ergebnis.to_dicts() == erwartet, (
    f"verdaechtig(protokoll, 10) ergibt {als_text(ergebnis)}, erwartet war {erwartet}."
    + ("\nTipp: Mit select(\"benutzer\", \"fehlversuche\") bleiben nur diese beiden Spalten übrig."
       if isinstance(ergebnis, pl.DataFrame) and ergebnis.columns != ["benutzer", "fehlversuche"] else "")
)

# verdaechtig: nur nächtliche Zeilen, auch wenn tagsüber viele Fehlversuche anfallen
zeilen = [("dora", 14, 500), ("emil", 2, 30)]
ergebnis = verdaechtig(tabelle(zeilen), 20)
erwartet = [{"benutzer": "emil", "fehlversuche": 30}]
assert isinstance(ergebnis, pl.DataFrame) and ergebnis.to_dicts() == erwartet, (
    f"Bei {zeilen} und schwelle 20 ergibt verdaechtig {als_text(ergebnis)}, erwartet war {erwartet}.\n"
    "Tipp: Beide Bedingungen müssen gelten: nachts & (fehlversuche >= schwelle)."
)

# verdaechtig: genau schwelle Fehlversuche zählt schon (mindestens)
zeilen = [("finn", 1, 9), ("gina", 1, 10), ("hans", 1, 11)]
ergebnis = verdaechtig(tabelle(zeilen), 10)
erwartet = [{"benutzer": "gina", "fehlversuche": 10}, {"benutzer": "hans", "fehlversuche": 11}]
assert isinstance(ergebnis, pl.DataFrame) and ergebnis.to_dicts() == erwartet, (
    f"Bei {zeilen} und schwelle 10 ergibt verdaechtig {als_text(ergebnis)}, erwartet war {erwartet}.\n"
    "Tipp: „Mindestens schwelle“ heißt >= schwelle."
)

# verdaechtig: schwelle 0 liefert alle nächtlichen Zeilen
ergebnis = verdaechtig(tabelle(BEISPIEL), 0)
erwartet = verdaechtig_von_hand(BEISPIEL, 0)
assert isinstance(ergebnis, pl.DataFrame) and ergebnis.to_dicts() == erwartet, (
    f"verdaechtig(protokoll, 0) ergibt {als_text(ergebnis)}, erwartet war {erwartet}."
)

# verdaechtig: nichts Auffälliges ergibt einen leeren DataFrame mit den beiden Spalten
ergebnis = verdaechtig(tabelle(BEISPIEL), 1000)
assert isinstance(ergebnis, pl.DataFrame) and ergebnis.height == 0 and ergebnis.columns == ["benutzer", "fehlversuche"], (
    f"verdaechtig(protokoll, 1000) ergibt {als_text(ergebnis)}"
    + (f" mit den Spalten {ergebnis.columns}" if isinstance(ergebnis, pl.DataFrame) else "")
    + ", erwartet war ein leerer DataFrame mit den Spalten ['benutzer', 'fehlversuche']."
)

# kennzahlen: das Beispiel aus der Aufgabe
ergebnis = kennzahlen(tabelle(BEISPIEL))
erwartet = [{"summe": 54, "hoechstwert": 40, "betroffen": 3}]
assert isinstance(ergebnis, pl.DataFrame) and ergebnis.to_dicts() == erwartet, (
    f"kennzahlen(protokoll) ergibt {als_text(ergebnis)}, erwartet war {erwartet}.\n"
    'Tipp: protokoll.select(pl.col("fehlversuche").sum().alias("summe"), …) liefert eine Zeile.'
)

# kennzahlen: betroffen zählt Zeilen mit Fehlversuchen, nicht die Fehlversuche
zeilen = [("ida", 3, 0), ("jan", 4, 7), ("ida", 9, 0), ("kai", 12, 1)]
ergebnis = kennzahlen(tabelle(zeilen))
erwartet = kennzahlen_von_hand(zeilen)
assert isinstance(ergebnis, pl.DataFrame) and ergebnis.to_dicts() == erwartet, (
    f"kennzahlen für {zeilen} ergibt {als_text(ergebnis)}, erwartet war {erwartet}.\n"
    'Tipp: (pl.col("fehlversuche") > 0).sum() zählt die Zeilen, in denen die Bedingung True ist.'
)

# Leeres Protokoll: summe 0, hoechstwert None, betroffen 0
leer = tabelle([])
try:
    ergebnisse = (mit_nachtmarke(leer), verdaechtig(leer, 5), kennzahlen(leer))
    fehler = None
except Exception as ausnahme:
    ergebnisse = None
    fehler = ausnahme
assert fehler is None, f"Bei einem leeren Protokoll bricht Ihre Lösung ab: {type(fehler).__name__}: {fehler}"

# Leeres Protokoll ergibt leere Tabellen und die Kennzahlen 0, None, 0
assert (
    ergebnisse[0].height == 0
    and ergebnisse[0].columns == ["benutzer", "stunde", "fehlversuche", "nachts"]
    and ergebnisse[1].height == 0
    and ergebnisse[2].to_dicts() == [{"summe": 0, "hoechstwert": None, "betroffen": 0}]
), (
    "Bei einem leeren Protokoll erwartet: mit_nachtmarke leer mit vier Spalten, verdaechtig leer, "
    "kennzahlen [{'summe': 0, 'hoechstwert': None, 'betroffen': 0}]; bekommen: "
    f"{ergebnisse[0].columns}, {ergebnisse[1].to_dicts()}, {ergebnisse[2].to_dicts()}."
)

# Keine Schleife über die Zeilen
assert not verwendet("for") and not verwendet("while") and not verwendet("iter_rows"), (
    "Ihre Lösung benutzt eine Schleife. Arbeiten Sie mit den Ausdrücken von polars (filter, with_columns, select)."
)

# Viele zufällige Protokolle, verglichen mit einer Lösung ohne polars
zufall = Zufall(4031)
for runde in range(150):
    zeilen = [
        (zufall.choice(["anna", "ben", "cem", "dora"]), zufall.randint(0, 23), zufall.choice([0, 0, zufall.randint(0, 60)]))
        for _ in range(zufall.randint(0, 8))
    ]
    schwelle = zufall.randint(0, 40)
    ergebnis_v = verdaechtig(tabelle(zeilen), schwelle).to_dicts()
    ergebnis_k = kennzahlen(tabelle(zeilen)).to_dicts()
    erwartet_v = verdaechtig_von_hand(zeilen, schwelle)
    erwartet_k = kennzahlen_von_hand(zeilen)
    assert ergebnis_v == erwartet_v and ergebnis_k == erwartet_k, (
        f"Für das Protokoll {zeilen} und schwelle {schwelle}:\n"
        f"  verdaechtig erwartet {erwartet_v}, bekommen {ergebnis_v}\n"
        f"  kennzahlen erwartet {erwartet_k}, bekommen {ergebnis_k}"
    )

# Obere Grenze: 100 000 Zeilen mit den größten Werten
gross = pl.DataFrame({
    "benutzer": ["u" + str(nummer % 97) for nummer in range(100_000)],
    "stunde": [nummer % 24 for nummer in range(100_000)],
    "fehlversuche": [10_000 if nummer % 24 == 23 else nummer % 3 for nummer in range(100_000)],
})
anzahl_nachts = mit_nachtmarke(gross)["nachts"].sum()
anzahl_verdaechtig = verdaechtig(gross, 10_000).height
zahlen = kennzahlen(gross).to_dicts()
erwartet_zahlen = [{
    "summe": sum(gross["fehlversuche"].to_list()),
    "hoechstwert": 10_000,
    "betroffen": len([wert for wert in gross["fehlversuche"].to_list() if wert > 0]),
}]
erwartet_nachts = len([nummer for nummer in range(100_000) if ist_nachts(nummer % 24)])
assert (anzahl_nachts, anzahl_verdaechtig, zahlen) == (erwartet_nachts, 4166, erwartet_zahlen), (
    "Bei 100 000 Zeilen (Stunden 0 bis 23 reihum, 10 000 Fehlversuche um 23 Uhr) erwartet: "
    f"{erwartet_nachts} nächtliche Zeilen, 4166 verdächtige und {erwartet_zahlen}; "
    f"bekommen {anzahl_nachts}, {anzahl_verdaechtig} und {zahlen}."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar(str(verdaechtig_von_hand(BEISPIEL, 10))), (
    f"Erwartete Ausgabe: {verdaechtig_von_hand(BEISPIEL, 10)} – Ihr Programm: {AUSGABE}"
)
