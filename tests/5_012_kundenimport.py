# Automatisch erzeugt aus lehrkraft/muster/5_012_kundenimport.py - nicht von Hand ändern.
# vorlage-hash: 612f15e2631fa002
# text-hash: 744f0fc26c3cf12d
# thema: datenanalyse
# inhalt: polars Lazy-Modus

import ast
import inspect
import textwrap

BEISPIEL = """kunden_nr,name,email,ort
1001,Ada Berg, Ada.Berg@Example.org ,Bonn
1002,Bo Lang,,Jena
1003,Cem Koch,cem@example.org,Bonn
1004,Ada Berg,ada.berg@example.org,Bonn
"""


def collect_aufrufe(funktion):
    """Zählt, wie oft im Quelltext der Funktion .collect() steht."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return -1
    anzahl = 0
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute) and knoten.func.attr == "collect":
            anzahl = anzahl + 1
    return anzahl


def als_lazy(zeilen):
    """Baut aus Tupeln (kunden_nr, name, email, ort) einen LazyFrame mit festen Spaltentypen."""
    schema = {"kunden_nr": pl.Int64, "name": pl.String, "email": pl.String, "ort": pl.String}
    return pl.DataFrame(zeilen, schema=schema, orient="row").lazy()


def bereinigt_von_hand(zeilen):
    """Bereinigt eine Liste von Tupeln ohne polars."""
    behalten = {}
    for nummer, name, email, ort in sorted(zeilen):
        if email is None:
            continue
        sauber = email.strip().lower()
        if sauber not in behalten:
            behalten[sauber] = (nummer, name, sauber, ort)
    return sorted(behalten.values())


def je_ort_von_hand(zeilen):
    """Zählt die bereinigten Kunden je Ort ohne polars."""
    anzahl = {}
    for _, _, _, ort in bereinigt_von_hand(zeilen):
        anzahl[ort] = anzahl.get(ort, 0) + 1
    paare = [(-menge, ort) for ort, menge in anzahl.items()]
    return [(ort, -minus) for minus, ort in sorted(paare)]


# lade gibt einen LazyFrame zurück, der den Text liest
kunden = lade(BEISPIEL)
assert isinstance(kunden, pl.LazyFrame), (
    f"lade(csv_text) gibt {type(kunden).__name__} zurück, erwartet war ein LazyFrame.\n"
    "Tipp: pl.scan_csv liefert einen LazyFrame, pl.read_csv einen DataFrame, der schon alles gelesen hat."
)

# lade liest noch nichts: Der Plan beginnt mit dem Lesen des Texts (SCAN), nicht mit fertigen Daten
plan_text = kunden.explain()
assert "SCAN" in plan_text.upper(), (
    f"lade(csv_text).explain() zeigt {plan_text!r}; der Plan soll mit dem Einlesen (SCAN) beginnen.\n"
    "Tipp: pl.read_csv(...).lazy() hat den Text schon gelesen; benutzen Sie pl.scan_csv."
)

# lade liest alle Zeilen und Spalten unverändert
ergebnis = kunden.collect().rows()
erwartet = [
    (1001, "Ada Berg", " Ada.Berg@Example.org ", "Bonn"),
    (1002, "Bo Lang", None, "Jena"),
    (1003, "Cem Koch", "cem@example.org", "Bonn"),
    (1004, "Ada Berg", "ada.berg@example.org", "Bonn"),
]
assert ergebnis == erwartet, (
    f"lade(csv_text).collect().rows() ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: lade soll den Text nur lesen, noch nichts bereinigen."
)

# bereinigt gibt einen LazyFrame zurück
plan = bereinigt(lade(BEISPIEL))
assert isinstance(plan, pl.LazyFrame), (
    f"bereinigt(kunden) gibt {type(plan).__name__} zurück, erwartet war ein LazyFrame.\n"
    "Tipp: Rufen Sie in bereinigt kein collect() auf; jede Methode eines LazyFrame liefert wieder einen LazyFrame."
)

# bereinigt aus dem Beispiel
ergebnis = plan.collect().rows()
erwartet = [(1001, "Ada Berg", "ada.berg@example.org", "Bonn"), (1003, "Cem Koch", "cem@example.org", "Bonn")]
assert ergebnis == erwartet, (
    f"bereinigt(lade(csv_text)).collect().rows() ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Erst Zeilen ohne E-Mail weglassen, dann die Adressen bereinigen, dann sortieren und Dubletten entfernen."
)

# bereinigt rechnet nichts aus: ein Plan, dessen Ausführung scheitern würde, bleibt unberührt
def scheitert(spalte):
    """Löst einen Fehler aus, sobald polars wirklich rechnet."""
    raise RuntimeError("Der Plan wurde ausgeführt")


falle = als_lazy([(1, "A", "a@x.de", "Kiel")]).with_columns(pl.col("kunden_nr").map_batches(scheitert, return_dtype=pl.Int64))
try:
    ergebnis = type(bereinigt(falle)).__name__
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == "LazyFrame", (
    f"bereinigt soll nur den Plan erweitern und nichts ausrechnen; bei einem Plan, der beim Ausführen scheitert, "
    f"ergibt sich {ergebnis!r} statt eines LazyFrame.\nTipp: Kein collect(), kein .rows(), kein Umweg über einen DataFrame."
)

# bereinigt enthält kein collect()
anzahl = collect_aufrufe(bereinigt)
assert anzahl == 0, (
    f"bereinigt darf collect() nicht aufrufen; gefunden: {anzahl}-mal"
    + (" (der Quelltext von bereinigt ließ sich nicht lesen)." if anzahl == -1 else ".")
)

# Die kleinste Kundennummer gewinnt, auch wenn sie weiter hinten steht
zeilen = [(30, "C", "x@y.de", "Kiel"), (10, "A", " X@Y.DE", "Bonn"), (20, "B", "x@y.de ", "Jena")]
ergebnis = bereinigt(als_lazy(zeilen)).collect().rows()
assert ergebnis == [(10, "A", "x@y.de", "Bonn")], (
    f"bereinigt bei {zeilen} ergibt {ergebnis!r}, erwartet war [(10, 'A', 'x@y.de', 'Bonn')].\n"
    "Tipp: unique(keep='first') behält die erste Zeile; sortieren Sie vorher nach kunden_nr."
)

# Dubletten zählen erst nach dem Bereinigen, und die Reihenfolge stimmt
zeilen = [(5, "E", "e@x.de", "Ulm"), (2, "B", "B@x.de", "Ulm"), (9, "B2", "b@x.de", "Ulm"), (1, "A", None, "Ulm")]
ergebnis = bereinigt(als_lazy(zeilen)).collect().rows()
assert ergebnis == [(2, "B", "b@x.de", "Ulm"), (5, "E", "e@x.de", "Ulm")], (
    f"bereinigt bei {zeilen} ergibt {ergebnis!r}, erwartet war [(2, 'B', 'b@x.de', 'Ulm'), (5, 'E', 'e@x.de', 'Ulm')].\n"
    "Tipp: Erst die Adressen bereinigen, dann nach Dubletten suchen; zum Schluss nach kunden_nr sortiert."
)

# Leere Tabelle und nur fehlende Adressen
ergebnis = (bereinigt(als_lazy([])).collect().rows(), bereinigt(als_lazy([(1, "A", None, "Bonn")])).collect().rows())
assert ergebnis == ([], []), f"bereinigt einer leeren Tabelle und einer ohne E-Mail-Adressen ergibt {ergebnis!r}, erwartet war ([], [])."

# kunden_je_ort aus dem Beispiel
ergebnis = kunden_je_ort(lade(BEISPIEL))
assert ergebnis == [("Bonn", 2)], (
    f"kunden_je_ort(lade(csv_text)) ergibt {ergebnis!r}, erwartet war [('Bonn', 2)].\n"
    "Tipp: Bo Lang aus Jena hat keine Adresse und fällt beim Bereinigen weg; zählen Sie mit group_by und pl.len()."
)

# kunden_je_ort sortiert nach Anzahl absteigend, dann nach Ort
zeilen = [(1, "A", "a@x", "Ulm"), (2, "B", "b@x", "Aue"), (3, "C", "c@x", "Ulm"), (4, "D", "d@x", "Kiel"), (5, "E", "e@x", "Aue"), (6, "F", "a@x", "Kiel")]
ergebnis = kunden_je_ort(als_lazy(zeilen))
assert ergebnis == [("Aue", 2), ("Ulm", 2), ("Kiel", 1)], (
    f"kunden_je_ort bei {zeilen} ergibt {ergebnis!r}, erwartet war [('Aue', 2), ('Ulm', 2), ('Kiel', 1)].\n"
    "Tipp: sort(['anzahl', 'ort'], descending=[True, False]); F aus Kiel ist eine Dublette von A."
)

# kunden_je_ort bei leerer Tabelle, mit genau einem collect() und über bereinigt
ergebnis = kunden_je_ort(als_lazy([]))
quelltext = inspect.getsource(kunden_je_ort)
assert ergebnis == [] and collect_aufrufe(kunden_je_ort) == 1 and "bereinigt(" in quelltext, (
    f"kunden_je_ort einer leeren Tabelle ergibt {ergebnis!r} (erwartet []); die Funktion soll bereinigt(…) benutzen und "
    f"genau einmal collect() aufrufen, sie ruft es {collect_aufrufe(kunden_je_ort)}-mal auf."
)

ORTE = ["Bonn", "Jena", "Kiel", "Ulm"]
ADRESSEN = ["a@x.de", " A@x.de", "b@x.de ", "B@X.DE", "c@y.org", None]

# 200 zufällige Kundentabellen
zufall = Zufall(5012)
for _ in range(200):
    nummern = zufall.sample(range(1, 10**9), zufall.randint(0, 8))
    zeilen = [(nummer, "N" + str(nummer % 7), zufall.choice(ADRESSEN), zufall.choice(ORTE)) for nummer in nummern]
    kunden = als_lazy(zeilen)
    ergebnis = bereinigt(kunden).collect().rows()
    erwartet = bereinigt_von_hand(zeilen)
    assert ergebnis == erwartet, f"bereinigt bei {zeilen} ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    ergebnis = kunden_je_ort(kunden)
    erwartet = je_ort_von_hand(zeilen)
    assert ergebnis == erwartet, f"kunden_je_ort bei {zeilen} ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# lade mit zufälligem CSV-Text
for _ in range(20):
    nummern = zufall.sample(range(1, 10**9), zufall.randint(0, 5))
    zeilen = [(nummer, "N" + str(nummer % 7), zufall.choice(["a@x.de", "b@y.de"]), zufall.choice(ORTE)) for nummer in nummern]
    text = "kunden_nr,name,email,ort\n" + "".join(f"{n},{name},{mail},{ort}\n" for n, name, mail, ort in zeilen)
    ergebnis = lade(text).collect().rows()
    assert ergebnis == zeilen, f"lade mit dem Text {text!r} liefert {ergebnis!r}, erwartet war {zeilen!r}."

# An der oberen Grenze: 100 000 Kunden
zeilen = []
for nummer in range(100000):
    adresse = None if nummer % 10 == 0 else f"  Kunde{(nummer * 7) % 60000}@Example.ORG "
    zeilen.append((10**9 - nummer * 3, f"Name {nummer}", adresse, ORTE[nummer % 4]))
kunden = als_lazy(zeilen)
ergebnis = bereinigt(kunden).collect()
erwartet = bereinigt_von_hand(zeilen)
je_ort = kunden_je_ort(kunden)
assert ergebnis.rows() == erwartet and je_ort == je_ort_von_hand(zeilen), (
    f"Bei 100 000 Kunden liefert bereinigt {ergebnis.height} Zeilen (erwartet {len(erwartet)}), die erste "
    f"{ergebnis.rows()[:1]} (erwartet {erwartet[:1]}); kunden_je_ort ergibt {je_ort}, erwartet war {je_ort_von_hand(zeilen)}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['ada.berg@example.org', 'cem@example.org']\n[1001, 1003]\n[('Bonn', 2)]"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
