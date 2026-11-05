# Automatisch erzeugt aus lehrkraft/muster/5_015_ticketauswertung.py - nicht von Hand ändern.
# vorlage-hash: e5778860fc272094
# text-hash: 1d68840682fc40ab
# thema: datenanalyse
# inhalt: pandas, polars und SQL im Vergleich

import ast
import inspect
import textwrap

SPALTEN = ["nummer", "kategorie", "status", "minuten", "frist"]


def als_pandas(zeilen):
    """Baut das pandas-DataFrame aus einer Liste von Tupeln."""
    tabelle = pd.DataFrame(zeilen, columns=SPALTEN)
    # Bei 0 Zeilen hätte pandas sonst Spalten vom Typ object
    return tabelle.astype({"nummer": "int64", "kategorie": "object", "status": "object", "minuten": "int64", "frist": "int64"})


def als_polars(zeilen):
    """Baut das polars-DataFrame aus einer Liste von Tupeln."""
    schema = {"nummer": pl.Int64, "kategorie": pl.String, "status": pl.String, "minuten": pl.Int64, "frist": pl.Int64}
    return pl.DataFrame(zeilen, schema=schema, orient="row")


def als_verbindung(zeilen):
    """Legt eine neue DuckDB-Verbindung mit der Tabelle tickets an."""
    neu = duckdb.connect()
    neu.execute("CREATE TABLE tickets (nummer BIGINT, kategorie VARCHAR, status VARCHAR, minuten BIGINT, frist BIGINT)")
    neu.register("quelle", als_pandas(zeilen))
    neu.execute("INSERT INTO tickets SELECT * FROM quelle")
    neu.unregister("quelle")
    return neu


def als_liste(ergebnis):
    """Macht aus dem Ergebnis eine Liste von Tupeln mit Python-Werten, damit der Vergleich nicht am Typ scheitert."""
    try:
        return [tuple(wert.item() if hasattr(wert, "item") else wert for wert in zeile) for zeile in ergebnis]
    except TypeError:
        return ergebnis


def gleich(ergebnis, erwartet):
    """Vergleicht zwei Berichte; der Durchschnitt darf in der letzten Stelle abweichen."""
    ergebnis = als_liste(ergebnis)
    if not isinstance(ergebnis, list) or len(ergebnis) != len(erwartet):
        return False
    for zeile, soll in zip(ergebnis, erwartet):
        if not isinstance(zeile, tuple) or len(zeile) != 4:
            return False
        if (zeile[0], zeile[1], zeile[3]) != (soll[0], soll[1], soll[3]) or abs(zeile[2] - soll[2]) > 1e-9:
            return False
    return True


def bericht_von_hand(zeilen, mindestens):
    """Vergleichslösung in reinem Python mit einem Dictionary je Kategorie."""
    gruppen = {}
    for _, kategorie, status, minuten, frist in zeilen:
        if status != "geschlossen":
            continue
        anzahl, summe, verstoesse = gruppen.get(kategorie, (0, 0, 0))
        gruppen[kategorie] = (anzahl + 1, summe + minuten, verstoesse + (1 if minuten > frist else 0))
    ergebnis = []
    for kategorie in sorted(gruppen):
        anzahl, summe, verstoesse = gruppen[kategorie]
        if anzahl >= mindestens:
            ergebnis.append((kategorie, anzahl, summe / anzahl, verstoesse))
    return ergebnis


def alle_drei(zeilen, mindestens):
    """Ruft die drei Funktionen mit denselben Tickets auf; eine Ausnahme wird als Text zurückgegeben."""
    ergebnisse = []
    for funktion, tabelle in [(bericht_pandas, als_pandas), (bericht_polars, als_polars), (bericht_sql, als_verbindung)]:
        try:
            ergebnisse.append(funktion(tabelle(zeilen), mindestens))
        except Exception as fehler:
            ergebnisse.append(f"{type(fehler).__name__}: {fehler}")
    return ergebnisse


def pruefe_alle(zeilen, mindestens, hinweis=""):
    """Gibt eine Fehlermeldung zurück, wenn eine der drei Funktionen etwas anderes liefert, sonst einen leeren Text."""
    erwartet = bericht_von_hand(zeilen, mindestens)
    namen = ["bericht_pandas", "bericht_polars", "bericht_sql"]
    for name, ergebnis in zip(namen, alle_drei(zeilen, mindestens)):
        if not gleich(ergebnis, erwartet):
            return (
                f"{name} ergibt für die Tickets {zeilen} mit mindestens={mindestens} den Bericht {als_liste(ergebnis)!r}, "
                f"erwartet war {erwartet!r}.{hinweis}"
            )
    return ""


BEISPIEL = [
    (1, "drucker", "geschlossen", 45, 60),
    (2, "netz", "geschlossen", 130, 120),
    (3, "drucker", "geschlossen", 75, 60),
    (4, "netz", "offen", 300, 120),
    (5, "software", "geschlossen", 20, 240),
    (6, "drucker", "geschlossen", 60, 60),
]

# Das Beispiel mit mindestens 1 und 2, in allen drei Bibliotheken
for mindestens in [1, 2]:
    meldung = pruefe_alle(BEISPIEL, mindestens, "\nTipp: Werten Sie nur Tickets mit status 'geschlossen' aus.")
    assert not meldung, meldung

# Genau die Frist einzuhalten ist kein Verstoß
zeilen = [(1, "netz", "geschlossen", 120, 120), (2, "netz", "geschlossen", 121, 120), (3, "netz", "geschlossen", 0, 0)]
meldung = pruefe_alle(zeilen, 1, "\nTipp: Ein Verstoß ist nur minuten > frist, nicht minuten >= frist.")
assert not meldung, meldung

# Gruppen mit zu wenigen geschlossenen Tickets fallen weg, offene zählen nicht mit
zeilen = [(1, "a", "geschlossen", 10, 5), (2, "a", "offen", 10, 5), (3, "a", "offen", 10, 5), (4, "b", "geschlossen", 1, 5), (5, "b", "geschlossen", 3, 5)]
meldung = pruefe_alle(zeilen, 2, "\nTipp: Filtern Sie erst nach status und zählen Sie dann je Kategorie (WHERE vor HAVING).")
assert not meldung, meldung

# Der Durchschnitt wird nicht gerundet
zeilen = [(1, "x", "geschlossen", 1, 9), (2, "x", "geschlossen", 2, 9), (3, "x", "geschlossen", 2, 9)]
meldung = pruefe_alle(zeilen, 1, "\nTipp: Geben Sie den Durchschnitt ungerundet zurück (5 / 3 = 1.666…).")
assert not meldung, meldung

# Keine Tickets, nur offene Tickets, mindestens zu groß: leere Liste
for zeilen, mindestens in [([], 1), ([(1, "a", "offen", 5, 5)], 1), (BEISPIEL, 4)]:
    meldung = pruefe_alle(zeilen, mindestens, "\nTipp: Ohne passende Tickets ist der Bericht die leere Liste [].")
    assert not meldung, meldung

# Die Ergebnisse sind Listen von Tupeln
typen = [type(ergebnis).__name__ for ergebnis in alle_drei(BEISPIEL, 1)]
assert typen == ["list", "list", "list"], (
    f"bericht_pandas, bericht_polars und bericht_sql geben {typen} zurück, erwartet war jeweils eine Liste.\n"
    "Tipp: list(df.itertuples(index=False, name=None)) in pandas, df.rows() in polars, .fetchall() in DuckDB."
)

# Die Tabellen bleiben unverändert
tabelle_pandas = als_pandas(BEISPIEL)
tabelle_polars = als_polars(BEISPIEL)
bericht_pandas(tabelle_pandas, 1)
bericht_polars(tabelle_polars, 1)
assert list(tabelle_pandas.columns) == SPALTEN and tabelle_polars.columns == SPALTEN and len(tabelle_pandas) == 6, (
    f"Nach dem Bericht hat das pandas-DataFrame die Spalten {list(tabelle_pandas.columns)} und {len(tabelle_pandas)} "
    f"Zeilen, das polars-DataFrame die Spalten {tabelle_polars.columns}; erwartet waren unverändert {SPALTEN} und 6 Zeilen.\n"
    "Tipp: Rechnen Sie neue Spalten mit assign bzw. in einem neuen DataFrame aus."
)


def bauweise(funktion):
    """Gibt die Namen aller aufgerufenen Methoden und ob eine for- oder while-Anweisung vorkommt zurück."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return set(), False
    namen = set()
    mit_schleife = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute):
            namen.add(knoten.func.attr)
        if isinstance(knoten, (ast.For, ast.While)):
            mit_schleife = True
    return namen, mit_schleife


# Jede Funktion arbeitet mit ihrer Bibliothek, ohne for- oder while-Schleife
for funktion, methode, beschreibung in [
    (bericht_pandas, "groupby", "groupby von pandas"),
    (bericht_polars, "group_by", "group_by von polars"),
    (bericht_sql, "execute", "verbindung.execute(...) mit GROUP BY in SQL"),
]:
    namen, mit_schleife = bauweise(funktion)
    assert methode in namen and not mit_schleife, (
        f"{funktion.__name__} soll mit {beschreibung} gruppieren, ohne for- oder while-Schleife; gefunden: "
        f"{methode} {'ja' if methode in namen else 'nein'}, Schleife {'ja' if mit_schleife else 'nein'}."
    )

# 20 zufällige Ticketlisten: alle drei Bibliotheken liefern denselben Bericht wie die Nachrechnung
zufall = Zufall(5015)
for _ in range(20):
    zeilen = [
        (nummer, zufall.choice(["drucker", "netz", "software", "x"]), zufall.choice(["offen", "geschlossen", "geschlossen"]), zufall.choice([0, 30, 60, 61, 10**6, zufall.randint(0, 200)]), zufall.choice([0, 60, 120, 10**6]))
        for nummer in range(zufall.randint(0, 12))
    ]
    meldung = pruefe_alle(zeilen, zufall.randint(1, 4))
    assert not meldung, meldung

# An der oberen Grenze: 10 000 Tickets
zeilen = [
    (nummer, f"kategorie{'abcdefghij'[nummer % 10]}", "geschlossen" if nummer % 7 else "offen", (nummer * 7919) % 10**6, (nummer * 104729) % 10**6)
    for nummer in range(10000)
]
for mindestens in [1, 858, 10000]:
    meldung = pruefe_alle(zeilen, mindestens)
    assert not meldung, meldung[:600]
