# Automatisch erzeugt aus lehrkraft/muster/4_037_bestellabfrage.py - nicht von Hand ändern.
# vorlage-hash: 93f20ebc59a43dd6
# text-hash: ac315b3031f41225
# thema: datenanalyse
# inhalt: DuckDB: SQL auf DataFrame

import pandas as pd

BEISPIEL = {
    "bestellnummer": [1001, 1002, 1003, 1004, 1005],
    "kunde": ["Nowak", "Becker", "Nowak", "O'Brien", "Becker"],
    "betrag_cent": [4999, 12900, 1500, 7900, 2500],
}


def tabelle(nummern, kunden, betraege):
    """Baut den DataFrame aus drei Listen, auch für leere Listen mit passenden Spalten."""
    return pd.DataFrame(
        {
            "bestellnummer": pd.Series(nummern, dtype="int64"),
            "kunde": pd.Series(kunden, dtype="object"),
            "betrag_cent": pd.Series(betraege, dtype="int64"),
        }
    )


def beispiel():
    """Ein frischer DataFrame mit dem Beispiel."""
    return tabelle(BEISPIEL["bestellnummer"], BEISPIEL["kunde"], BEISPIEL["betrag_cent"])


def ergebnis_von(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def als_python(ergebnis):
    """Wandelt Tupel und Zahlen in einfache Python-Werte um, damit int und numpy-Zahlen gleich zählen."""
    if isinstance(ergebnis, (list, tuple)):
        return type(ergebnis)(als_python(teil) for teil in ergebnis)
    if hasattr(ergebnis, "item"):
        return ergebnis.item()
    return ergebnis


def vergleich_umsatz(nummern, kunden, betraege):
    """Vergleichslösung ohne SQL: Summen und Anzahlen mit Dictionaries."""
    summen = {}
    anzahlen = {}
    for kunde, betrag in zip(kunden, betraege):
        summen[kunde] = summen.get(kunde, 0) + betrag
        anzahlen[kunde] = anzahlen.get(kunde, 0) + 1
    zeilen = [(kunde, summen[kunde], anzahlen[kunde]) for kunde in summen]
    return sorted(zeilen, key=lambda zeile: (-zeile[1], zeile[0]))


def zufallsbestellungen(zufall, anzahl, kundenzahl):
    """Erzeugt anzahl zufällige Bestellungen mit eindeutigen Nummern; gibt die drei Spalten zurück."""
    namen = ["Nowak", "Becker", "O'Brien", "Öztürk", "Le Roux", "x' OR '1'='1", "Weiß", "anna", "Anna"]
    namen = namen[:kundenzahl] + [f"Kunde {nummer}" for nummer in range(max(0, kundenzahl - len(namen)))]
    nummern = zufall.sample(range(1, 10**9), anzahl)
    kunden = [zufall.choice(namen) for _ in range(anzahl)]
    betraege = [zufall.choice([0, 10**7, zufall.randint(0, 10**7), zufall.randint(0, 5000)]) for _ in range(anzahl)]
    return nummern, kunden, betraege


# bestellungen_von im Beispiel
ergebnis = als_python(ergebnis_von(bestellungen_von, beispiel(), "Nowak"))
assert ergebnis == [1001, 1003], (
    f'bestellungen_von(bestellungen, "Nowak") ergibt {ergebnis!r}, erwartet war [1001, 1003].'
    + ("\nTipp: fetchall() liefert Tupel; nehmen Sie aus jedem Tupel den ersten Wert." if ergebnis == [(1001,), (1003,)] else "")
)

# bestellungen_von für einen anderen Kunden (nicht fest hinschreiben!)
ergebnis = als_python(ergebnis_von(bestellungen_von, beispiel(), "Becker"))
assert ergebnis == [1002, 1005], f'bestellungen_von(bestellungen, "Becker") ergibt {ergebnis!r}, erwartet war [1002, 1005].'

# bestellungen_von sortiert nach Bestellnummer, auch wenn die Tabelle anders sortiert ist
ergebnis = als_python(ergebnis_von(bestellungen_von, tabelle([30, 10, 20], ["Kim", "Kim", "Kim"], [1, 2, 3]), "Kim"))
assert ergebnis == [10, 20, 30], (
    f"Bei den Bestellnummern 30, 10, 20 ergibt bestellungen_von {ergebnis!r}, erwartet war [10, 20, 30].\n"
    "Tipp: ORDER BY bestellnummer."
)

# bestellungen_von für einen Kunden ohne Bestellung
ergebnis = als_python(ergebnis_von(bestellungen_von, beispiel(), "Schulz"))
assert ergebnis == [], f'bestellungen_von(bestellungen, "Schulz") ergibt {ergebnis!r}, erwartet war [].'

# bestellungen_von mit einem Apostroph im Namen
ergebnis = als_python(ergebnis_von(bestellungen_von, beispiel(), "O'Brien"))
assert ergebnis == [1004], (
    f'bestellungen_von(bestellungen, "O\'Brien") ergibt {ergebnis!r}, erwartet war [1004].\n'
    "Tipp: Setzen Sie den Namen nicht mit einem f-String in die Abfrage, sondern als ? mit duckdb.execute(abfrage, [kunde])."
)

# bestellungen_von ist sicher gegen SQL-Injection
ergebnis = als_python(ergebnis_von(bestellungen_von, beispiel(), "x' OR '1'='1"))
assert ergebnis == [], (
    f"bestellungen_von(bestellungen, \"x' OR '1'='1\") ergibt {ergebnis!r}, erwartet war [] (diesen Kunden gibt es nicht).\n"
    "Tipp: Mit einem ? in der Abfrage wird der Name nie als SQL gelesen."
)

# umsatz_je_kunde im Beispiel
ergebnis = als_python(ergebnis_von(umsatz_je_kunde, beispiel()))
erwartet = [("Becker", 15400, 2), ("O'Brien", 7900, 1), ("Nowak", 6499, 2)]
assert ergebnis == erwartet, (
    f"umsatz_je_kunde(bestellungen) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: GROUP BY kunde mit SUM(betrag_cent) und COUNT(*), dann ORDER BY summe DESC, kunde."
)

# umsatz_je_kunde: bei gleicher Summe nach Namen
ergebnis = als_python(ergebnis_von(umsatz_je_kunde, tabelle([1, 2, 3, 4], ["Zander", "Adler", "Moll", "Moll"], [500, 500, 200, 300])))
erwartet = [("Adler", 500, 1), ("Moll", 500, 2), ("Zander", 500, 1)]
assert ergebnis == erwartet, f"Bei drei Kunden mit je 500 Cent ergibt umsatz_je_kunde {ergebnis!r}, erwartet war {erwartet!r}."

# umsatz_je_kunde mit Bestellungen zu 0 Cent
ergebnis = als_python(ergebnis_von(umsatz_je_kunde, tabelle([1, 2], ["Kim", "Lee"], [0, 0])))
assert ergebnis == [("Kim", 0, 1), ("Lee", 0, 1)], f"Bei zwei Bestellungen zu 0 Cent ergibt umsatz_je_kunde {ergebnis!r}, erwartet war [('Kim', 0, 1), ('Lee', 0, 1)]."

# stammkunden im Beispiel
ergebnis = als_python(ergebnis_von(stammkunden, beispiel(), 2))
assert ergebnis == ["Becker", "Nowak"], (
    f"stammkunden(bestellungen, 2) ergibt {ergebnis!r}, erwartet war ['Becker', 'Nowak'].\n"
    "Tipp: HAVING COUNT(*) >= ? prüft die Gruppen nach dem GROUP BY."
)

# stammkunden mit mindestanzahl 1: alle Kunden
ergebnis = als_python(ergebnis_von(stammkunden, beispiel(), 1))
assert ergebnis == ["Becker", "Nowak", "O'Brien"], f"stammkunden(bestellungen, 1) ergibt {ergebnis!r}, erwartet war ['Becker', 'Nowak', \"O'Brien\"]."

# stammkunden, wenn niemand genug Bestellungen hat
ergebnis = als_python(ergebnis_von(stammkunden, beispiel(), 3))
assert ergebnis == [], f"stammkunden(bestellungen, 3) ergibt {ergebnis!r}, erwartet war []."

# Eine leere Tabelle
leer = tabelle([], [], [])
ergebnis = [als_python(ergebnis_von(f, leer, *argumente)) for f, argumente in [(bestellungen_von, ["Nowak"]), (umsatz_je_kunde, []), (stammkunden, [1])]]
assert ergebnis == [[], [], []], f"Mit einer leeren Tabelle ergeben die drei Funktionen {ergebnis!r}, erwartet war [[], [], []]."

# Die übergebene Tabelle bleibt unverändert
df = beispiel()
bestellungen_von(df, "Nowak")
umsatz_je_kunde(df)
stammkunden(df, 2)
assert df.to_dict("list") == BEISPIEL, f"Nach den Aufrufen enthält die Tabelle {df.to_dict('list')}, erwartet war das unveränderte Beispiel."

# Die Abfragen laufen über DuckDB
assert verwendet("sql") or verwendet("execute"), "Schreiben Sie die Abfragen in SQL mit duckdb.sql(...) oder duckdb.execute(...)."

# Die Ausgabe des Programms
erwartet = "[1001, 1003]\n[('Becker', 15400, 2), (\"O'Brien\", 7900, 1), ('Nowak', 6499, 2)]\n['Becker', 'Nowak']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Tabellen
zufall = Zufall(4037)
for _ in range(40):
    nummern, kunden, betraege = zufallsbestellungen(zufall, zufall.randint(0, 25), zufall.randint(1, 9))
    df = tabelle(nummern, kunden, betraege)
    kunde = zufall.choice(kunden + ["niemand"])
    erwartet = sorted(nummer for nummer, name in zip(nummern, kunden) if name == kunde)
    ergebnis = als_python(ergebnis_von(bestellungen_von, df, kunde))
    assert ergebnis == erwartet, f"Bei {list(zip(nummern, kunden))} ergibt bestellungen_von(…, {kunde!r}) {ergebnis!r}, erwartet war {erwartet!r}."
    erwartet = vergleich_umsatz(nummern, kunden, betraege)
    ergebnis = als_python(ergebnis_von(umsatz_je_kunde, df))
    assert ergebnis == erwartet, f"Bei {list(zip(nummern, kunden, betraege))} ergibt umsatz_je_kunde {ergebnis!r}, erwartet war {erwartet!r}."
    mindestanzahl = zufall.randint(1, 5)
    erwartet = sorted(zeile[0] for zeile in vergleich_umsatz(nummern, kunden, betraege) if zeile[2] >= mindestanzahl)
    ergebnis = als_python(ergebnis_von(stammkunden, df, mindestanzahl))
    assert ergebnis == erwartet, f"Bei {list(zip(nummern, kunden))} ergibt stammkunden(…, {mindestanzahl}) {ergebnis!r}, erwartet war {erwartet!r}."

# Obere Grenze: 100 000 Bestellungen von 500 Kunden mit Beträgen bis 10**7
nummern, kunden, betraege = zufallsbestellungen(zufall, 100000, 500)
df = tabelle(nummern, kunden, betraege)
ergebnis = als_python(ergebnis_von(umsatz_je_kunde, df))
assert ergebnis == vergleich_umsatz(nummern, kunden, betraege), "Bei 100 000 Bestellungen stimmt umsatz_je_kunde nicht."

# Obere Grenze: stammkunden bei 100 000 Bestellungen
ergebnis = als_python(ergebnis_von(stammkunden, df, 200))
erwartet = sorted(zeile[0] for zeile in vergleich_umsatz(nummern, kunden, betraege) if zeile[2] >= 200)
assert ergebnis == erwartet, f"Bei 100 000 Bestellungen ergibt stammkunden(…, 200) {len(ergebnis)} Kunden, erwartet waren {len(erwartet)}."

# Obere Grenze: bestellungen_von bei 100 000 Bestellungen
ergebnis = als_python(ergebnis_von(bestellungen_von, df, "Nowak"))
assert ergebnis == sorted(n for n, k in zip(nummern, kunden) if k == "Nowak"), "Bei 100 000 Bestellungen stimmt bestellungen_von(…, \"Nowak\") nicht."
