# Automatisch erzeugt aus lehrkraft/muster/5_015_soll_ist.py - nicht von Hand ändern.
# vorlage-hash: b80c18cfc4353ace
# text-hash: b17c990a8e9f4a75
# thema: datenanalyse
# inhalt: pandas, polars und SQL im Vergleich

import inspect

SPALTEN = ["schritt", "anzahl", "schnitt", "soll", "ueberschritten"]
BEISPIEL = [
    (1, "erfassen", 4), (1, "pruefen", 25), (1, "freigeben", 90), (1, "buchen", 3),
    (2, "erfassen", 7), (2, "pruefen", 15), (2, "freigeben", 200), (2, "buchen", 2),
    (3, "erfassen", 5), (3, "pruefen", 32), (3, "freigeben", 150),
]
SOLL = [("erfassen", 5), ("pruefen", 20), ("freigeben", 120), ("buchen", 5), ("mahnen", 10)]
ERWARTET = [
    ("freigeben", 3, 440 / 3, 120, 2), ("pruefen", 3, 24.0, 20, 2),
    ("erfassen", 3, 16 / 3, 5, 1), ("buchen", 2, 2.5, 5, 0),
]
VERBINDUNG = duckdb.connect()


def pandas_tabellen(messungen, sollzeiten):
    """Baut die beiden pandas-DataFrames mit festen Spaltentypen."""
    tabelle = pd.DataFrame(messungen, columns=["vorgang", "schritt", "ist"])
    soll = pd.DataFrame(sollzeiten, columns=["schritt", "soll"])
    return (
        tabelle.astype({"vorgang": "int64", "schritt": "object", "ist": "int64"}),
        soll.astype({"schritt": "object", "soll": "int64"}),
    )


def polars_tabellen(messungen, sollzeiten):
    """Baut die beiden polars-DataFrames mit festen Spaltentypen."""
    tabelle = pl.DataFrame(messungen, schema={"vorgang": pl.Int64, "schritt": pl.String, "ist": pl.Int64}, orient="row")
    soll = pl.DataFrame(sollzeiten, schema={"schritt": pl.String, "soll": pl.Int64}, orient="row")
    return tabelle, soll


def duckdb_tabellen(messungen, sollzeiten):
    """Legt messungen und sollzeiten in der gemeinsamen Test-Verbindung neu an und gibt sie zurück."""
    tabelle, soll = pandas_tabellen(messungen, sollzeiten)
    VERBINDUNG.register("neue_messungen", tabelle)
    VERBINDUNG.register("neue_sollzeiten", soll)
    VERBINDUNG.execute("CREATE OR REPLACE TABLE messungen (vorgang BIGINT, schritt VARCHAR, ist BIGINT)")
    VERBINDUNG.execute("CREATE OR REPLACE TABLE sollzeiten (schritt VARCHAR, soll BIGINT)")
    VERBINDUNG.execute("INSERT INTO messungen SELECT * FROM neue_messungen")
    VERBINDUNG.execute("INSERT INTO sollzeiten SELECT * FROM neue_sollzeiten")
    VERBINDUNG.unregister("neue_messungen")
    VERBINDUNG.unregister("neue_sollzeiten")
    return VERBINDUNG


def python_wert(wert):
    """Macht aus numpy- und anderen Zahlen gewöhnliche Python-Werte."""
    return wert.item() if hasattr(wert, "item") else wert


def zeilen_pandas(ergebnis):
    """Gibt die Zeilen eines pandas-Ergebnisses als Liste von Tupeln zurück."""
    return [tuple(python_wert(wert) for wert in zeile) for zeile in ergebnis.itertuples(index=False, name=None)]


def zeilen_polars(ergebnis):
    """Gibt die Zeilen eines polars-Ergebnisses als Liste von Tupeln zurück."""
    return [tuple(zeile) for zeile in ergebnis.rows()]


def zeilen_sql(ergebnis):
    """Gibt die Zeilen eines DuckDB-Ergebnisses als Liste von Tupeln zurück."""
    try:
        return [tuple(python_wert(wert) for wert in zeile) for zeile in ergebnis]
    except TypeError:
        return ergebnis


def gleich(ergebnis, erwartet):
    """True, wenn beide Listen von Zeilen gleich sind; der Durchschnitt darf minimal abweichen."""
    if not isinstance(ergebnis, list) or len(ergebnis) != len(erwartet):
        return False
    for zeile, soll in zip(ergebnis, erwartet):
        if not isinstance(zeile, tuple) or len(zeile) != 5:
            return False
        if zeile[:2] != soll[:2] or zeile[3:] != soll[3:]:
            return False
        if not isinstance(zeile[2], (int, float)) or abs(zeile[2] - soll[2]) > 1e-9 * max(1, abs(soll[2])):
            return False
    return True


def von_hand(messungen, sollzeiten):
    """Vergleichslösung ohne Bibliothek: Dictionaries je Schritt, dann sortieren."""
    soll_von = dict(sollzeiten)
    istzeiten = {}
    for _, schritt, ist in messungen:
        istzeiten.setdefault(schritt, []).append(ist)
    zeilen = []
    for schritt, werte in istzeiten.items():
        drueber = len([ist for ist in werte if ist > soll_von[schritt]])
        zeilen.append((schritt, len(werte), sum(werte) / len(werte), soll_von[schritt], drueber))
    zeilen.sort(key=lambda zeile: zeile[0])
    zeilen.sort(key=lambda zeile: zeile[4], reverse=True)
    return zeilen


def grenzmeldung(name, ergebnis):
    """Meldung für die obere Grenze: nennt die erste Zeile, die nicht stimmt."""
    nummer = 0
    while nummer < min(len(ergebnis), len(GROSS_ERWARTET)) and gleich(ergebnis[nummer : nummer + 1], GROSS_ERWARTET[nummer : nummer + 1]):
        nummer = nummer + 1
    return (
        f"{name} bei 100 000 Messungen zu 1000 Schritten liefert {len(ergebnis)} Zeilen (erwartet {len(GROSS_ERWARTET)}); "
        f"Zeile {nummer} ist {ergebnis[nummer : nummer + 1]!r}, erwartet {GROSS_ERWARTET[nummer : nummer + 1]!r}."
    )


def alle_drei(messungen, sollzeiten):
    """Ruft die drei Fassungen auf und gibt ihre Ergebnisse als Listen von Tupeln zurück."""
    return (
        zeilen_pandas(auswertung_pandas(*pandas_tabellen(messungen, sollzeiten))),
        zeilen_polars(auswertung_polars(*polars_tabellen(messungen, sollzeiten))),
        zeilen_sql(auswertung_sql(duckdb_tabellen(messungen, sollzeiten))),
    )


def erste_abweichung(ergebnisse, erwartet):
    """Gibt den Namen der ersten Fassung zurück, deren Ergebnis nicht stimmt, sonst None."""
    for name, ergebnis in zip(["auswertung_pandas", "auswertung_polars", "auswertung_sql"], ergebnisse):
        if not gleich(ergebnis, erwartet):
            return name, ergebnis
    return None


def ohne(funktion, verbotene):
    """Gibt die verbotenen Textstücke zurück, die im Quelltext der Funktion stehen."""
    try:
        quelltext = inspect.getsource(funktion)
    except (OSError, TypeError):
        return ["(Quelltext nicht lesbar)"]
    return [stueck for stueck in verbotene if stueck in quelltext]


# auswertung_pandas gibt einen pandas-DataFrame mit den fünf Spalten zurück
ergebnis = auswertung_pandas(*pandas_tabellen(BEISPIEL, SOLL))
assert isinstance(ergebnis, pd.DataFrame) and list(ergebnis.columns) == SPALTEN, (
    f"auswertung_pandas soll einen pandas-DataFrame mit den Spalten {SPALTEN} zurückgeben, bekommen: "
    f"{type(ergebnis).__name__}" + (f" mit den Spalten {list(ergebnis.columns)}" if hasattr(ergebnis, "columns") else "")
    + ".\nTipp: groupby(\"schritt\", as_index=False).agg(anzahl=(\"ist\", \"size\"), …) legt die Namen gleich fest."
)

# auswertung_pandas aus dem Beispiel
ergebnis = zeilen_pandas(auswertung_pandas(*pandas_tabellen(BEISPIEL, SOLL)))
assert gleich(ergebnis, ERWARTET), (
    f"auswertung_pandas mit den Daten aus dem Beispiel ergibt\n{ergebnis!r}\nerwartet war\n{ERWARTET!r}\n"
    "Tipp: merge, eine Spalte ist > soll, groupby mit agg, dann "
    "sort_values([\"ueberschritten\", \"schritt\"], ascending=[False, True])."
)

# auswertung_polars gibt einen polars-DataFrame mit den fünf Spalten zurück
ergebnis = auswertung_polars(*polars_tabellen(BEISPIEL, SOLL))
assert isinstance(ergebnis, pl.DataFrame) and ergebnis.columns == SPALTEN, (
    f"auswertung_polars soll einen polars-DataFrame mit den Spalten {SPALTEN} zurückgeben, bekommen: "
    f"{type(ergebnis).__name__}" + (f" mit den Spalten {ergebnis.columns}" if hasattr(ergebnis, "columns") else "")
    + ".\nTipp: Geben Sie jedem Ausdruck in agg mit .alias(…) seinen Namen; bei einem LazyFrame fehlt noch collect()."
)

# auswertung_polars aus dem Beispiel
ergebnis = zeilen_polars(auswertung_polars(*polars_tabellen(BEISPIEL, SOLL)))
assert gleich(ergebnis, ERWARTET), (
    f"auswertung_polars mit den Daten aus dem Beispiel ergibt\n{ergebnis!r}\nerwartet war\n{ERWARTET!r}\n"
    "Tipp: join, group_by mit agg, dann sort([\"ueberschritten\", \"schritt\"], descending=[True, False]); "
    "ohne sort ist die Reihenfolge der Gruppen zufällig."
)

# auswertung_sql aus dem Beispiel
ergebnis = auswertung_sql(duckdb_tabellen(BEISPIEL, SOLL))
assert isinstance(ergebnis, list) and gleich(zeilen_sql(ergebnis), ERWARTET), (
    f"auswertung_sql mit den Daten aus dem Beispiel ergibt\n{ergebnis!r}\nerwartet war\n{ERWARTET!r}\n"
    "Tipp: JOIN … USING (schritt), GROUP BY schritt, soll, COUNT(*) FILTER (WHERE ist > soll), "
    "ORDER BY ueberschritten DESC, schritt, und am Ende .fetchall()."
)

# Ein Schritt, der nur in den Sollzeiten steht, kommt nicht vor; genau die Sollzeit ist nicht überschritten
messungen = [(8, "buchen", 5), (8, "buchen", 6), (9, "buchen", 5)]
sollzeiten = [("mahnen", 10), ("buchen", 5)]
erwartet = [("buchen", 3, 16 / 3, 5, 1)]
abweichung = erste_abweichung(alle_drei(messungen, sollzeiten), erwartet)
assert abweichung is None, (
    f"{abweichung[0]} mit den Messungen {messungen} und den Sollzeiten {sollzeiten} ergibt\n{abweichung[1]!r}\n"
    f"erwartet war\n{erwartet!r}\n"
    "Tipp: Nur Schritte mit Messung zählen (inner join, kein left join von den Sollzeiten aus); "
    "eine Istzeit von genau 5 bei Soll 5 ist nicht überschritten (>, nicht >=)."
)

# Sortierung: mehr Überschreitungen zuerst, bei Gleichstand alphabetisch
messungen = [(1, "zahlen", 9), (1, "a_pruefen", 9), (1, "buchen", 9), (2, "zahlen", 9), (2, "buchen", 1), (3, "ablage", 0)]
sollzeiten = [("zahlen", 1), ("a_pruefen", 1), ("buchen", 1), ("ablage", 1)]
erwartet = [("zahlen", 2, 9.0, 1, 2), ("a_pruefen", 1, 9.0, 1, 1), ("buchen", 2, 5.0, 1, 1), ("ablage", 1, 0.0, 1, 0)]
abweichung = erste_abweichung(alle_drei(messungen, sollzeiten), erwartet)
assert abweichung is None, (
    f"{abweichung[0]} mit den Messungen {messungen} und den Sollzeiten {sollzeiten} ergibt\n{abweichung[1]!r}\n"
    f"erwartet war\n{erwartet!r}\n"
    "Tipp: ueberschritten absteigend, bei gleicher Zahl schritt aufsteigend; die Richtung gilt je Spalte."
)

# Ein Vorgang durchläuft einen Schritt mehrmals, jede Zeile zählt
messungen = [(42, "pruefen", 30), (42, "pruefen", 10), (42, "pruefen", 50), (7, "erfassen", 3)]
sollzeiten = [("pruefen", 20), ("erfassen", 2)]
erwartet = [("pruefen", 3, 30.0, 20, 2), ("erfassen", 1, 3.0, 2, 1)]
abweichung = erste_abweichung(alle_drei(messungen, sollzeiten), erwartet)
assert abweichung is None, (
    f"{abweichung[0]} mit den Messungen {messungen} und den Sollzeiten {sollzeiten} ergibt\n{abweichung[1]!r}\n"
    f"erwartet war\n{erwartet!r}\n"
    "Tipp: anzahl zählt Messungen (Zeilen), nicht verschiedene Vorgänge."
)

# Keine Messungen: leeres Ergebnis
ergebnisse = alle_drei([], [("buchen", 5)])
roh = auswertung_pandas(*pandas_tabellen([], [("buchen", 5)]))
assert ergebnisse == ([], [], []) and list(roh.columns) == SPALTEN, (
    f"Ohne Messungen sollen alle drei Fassungen ein leeres Ergebnis liefern, bekommen: {ergebnisse!r}; "
    f"die Spalten bei pandas sind {list(roh.columns)}, erwartet {SPALTEN}."
)

# Werte an den Grenzen: Istzeit 0 und 10**5, Sollzeit 1 und 10**5
messungen = [(10**9, "x", 0), (1, "x", 10**5), (5, "y", 10**5), (6, "y", 10**5 - 1)]
sollzeiten = [("x", 1), ("y", 10**5)]
erwartet = [("x", 2, 50000.0, 1, 1), ("y", 2, 99999.5, 10**5, 0)]
abweichung = erste_abweichung(alle_drei(messungen, sollzeiten), erwartet)
assert abweichung is None, (
    f"{abweichung[0]} mit den Messungen {messungen} und den Sollzeiten {sollzeiten} ergibt\n{abweichung[1]!r}\n"
    f"erwartet war\n{erwartet!r}"
)

# auswertung_pandas verändert die übergebenen DataFrames nicht
tabelle, soll = pandas_tabellen(BEISPIEL, SOLL)
vorher = (tabelle.copy(), soll.copy())
auswertung_pandas(tabelle, soll)
assert tabelle.equals(vorher[0]) and soll.equals(vorher[1]), (
    "auswertung_pandas hat die übergebenen DataFrames verändert; danach haben sie die Spalten "
    f"{list(tabelle.columns)} und {list(soll.columns)}, vorher {list(vorher[0].columns)} und {list(vorher[1].columns)}.\n"
    "Tipp: Hilfsspalten nur im Ergebnis von merge anlegen oder mit assign, das eine Kopie liefert."
)

# Jede Fassung benutzt nur ihre eigene Bibliothek
verstoesse = {
    "auswertung_pandas": ohne(auswertung_pandas, ["duckdb", "pl.", "polars", ".sql(", ".execute("]),
    "auswertung_polars": ohne(auswertung_polars, ["pd.", "pandas", "to_pandas", "duckdb", ".sql(", ".execute("]),
    "auswertung_sql": ohne(auswertung_sql, ["pd.", "pl.", "pandas", "polars", ".df(", ".pl(", "fetchdf", "for "]),
}
verstoesse = {name: stuecke for name, stuecke in verstoesse.items() if stuecke}
assert not verstoesse, (
    f"Jede Fassung soll nur ihre eigene Bibliothek benutzen; gefunden: {verstoesse}.\n"
    "Tipp: auswertung_sql rechnet ganz in SQL und gibt fetchall() zurück, ohne Umweg über pandas, polars oder eine Schleife."
)

# auswertung_sql stellt eine SQL-Abfrage
try:
    quelltext = inspect.getsource(auswertung_sql).upper()
except (OSError, TypeError):
    quelltext = ""
assert "SELECT" in quelltext and "GROUP BY" in quelltext and "FETCHALL" in quelltext, (
    "auswertung_sql soll eine SQL-Abfrage mit SELECT … GROUP BY … ausführen und das Ergebnis mit fetchall() zurückgeben."
)

# 40 zufällige Protokolle, alle drei Fassungen gegen eine Vergleichslösung
zufall = Zufall(5015)
fehlerfall = None
for _ in range(40):
    namen = zufall.sample(["erfassen", "pruefen", "freigeben", "buchen", "a", "b_c", "zahlen"], zufall.randint(1, 5))
    sollzeiten = [(name, zufall.choice([1, zufall.randint(1, 12), 10**5])) for name in namen]
    zufall.shuffle(sollzeiten)
    genutzt = zufall.sample(namen, zufall.randint(1, len(namen)))
    messungen = [
        (zufall.randint(1, 10**9), zufall.choice(genutzt), zufall.choice([0, zufall.randint(0, 12), 10**5]))
        for _ in range(zufall.randint(0, 12))
    ]
    erwartet = von_hand(messungen, sollzeiten)
    abweichung = erste_abweichung(alle_drei(messungen, sollzeiten), erwartet)
    if abweichung is not None:
        fehlerfall = (messungen, sollzeiten, abweichung, erwartet)
        break
assert fehlerfall is None, (
    f"{fehlerfall[2][0]} mit den Messungen {fehlerfall[0]} und den Sollzeiten {fehlerfall[1]} ergibt\n"
    f"{fehlerfall[2][1]!r}\nerwartet war\n{fehlerfall[3]!r}"
)

# An der oberen Grenze: 100 000 Messungen zu 1000 Schritten
zufall = Zufall(51015)
GROSS_SOLL = [(f"schritt_{nummer}", zufall.randint(1, 10**5)) for nummer in range(1000)]
GROSS = [(zufall.randint(1, 10**9), f"schritt_{zufall.randrange(1000)}", zufall.randint(0, 10**5)) for _ in range(100000)]
GROSS_ERWARTET = von_hand(GROSS, GROSS_SOLL)

# An der oberen Grenze mit pandas
ergebnis = zeilen_pandas(auswertung_pandas(*pandas_tabellen(GROSS, GROSS_SOLL)))
assert gleich(ergebnis, GROSS_ERWARTET), grenzmeldung("auswertung_pandas", ergebnis)

# An der oberen Grenze mit polars
ergebnis = zeilen_polars(auswertung_polars(*polars_tabellen(GROSS, GROSS_SOLL)))
assert gleich(ergebnis, GROSS_ERWARTET), grenzmeldung("auswertung_polars", ergebnis)

# An der oberen Grenze mit SQL
ergebnis = zeilen_sql(auswertung_sql(duckdb_tabellen(GROSS, GROSS_SOLL)))
assert gleich(ergebnis, GROSS_ERWARTET), grenzmeldung("auswertung_sql", ergebnis)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "freigeben    3    146.7   120   2\n"
    "pruefen      3     24.0    20   2\n"
    "erfassen     3      5.3     5   1\n"
    "buchen       2      2.5     5   0\n"
    "['freigeben', 'pruefen', 'erfassen', 'buchen']\n"
    "[2, 2, 1, 0]"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
