# Automatisch erzeugt aus lehrkraft/muster/4_057_abnahme.py - nicht von Hand ändern.
# vorlage-hash: b319065947990b4d
# text-hash: fdfe5f8642c5f72b
# thema: datenanalyse
# inhalt: polars group_by und join

import polars as pl

SCHEMA_ANFORDERUNGEN = {"id": pl.String, "art": pl.String, "prioritaet": pl.String}
SCHEMA_TESTS = {"anforderung": pl.String, "testfall": pl.String, "bestanden": pl.Boolean}
BEISPIEL_ANFORDERUNGEN = [
    ("A1", "funktional", "muss"),
    ("A2", "funktional", "soll"),
    ("A3", "nicht funktional", "muss"),
    ("A4", "nicht funktional", "kann"),
    ("A5", "funktional", "kann"),
]
BEISPIEL_TESTS = [("A1", "T1", True), ("A1", "T2", True), ("A2", "T3", False), ("A2", "T4", True), ("A3", "T5", False), ("A5", "T6", True), ("A9", "T7", True)]


def tabellen(anforderungen, tests):
    """Baut die beiden DataFrames aus Listen von Tupeln, auch wenn sie leer sind."""
    links = pl.DataFrame(anforderungen, schema=SCHEMA_ANFORDERUNGEN, orient="row")
    rechts = pl.DataFrame(tests, schema=SCHEMA_TESTS, orient="row")
    return links, rechts


def zeilen_von(funktion, anforderungen, tests):
    """Ruft die Funktion mit frischen Tabellen auf und gibt das Ergebnis als Liste von Dictionaries zurück.

    Ein Fehler oder ein Ergebnis, das kein DataFrame ist, wird als Text beschrieben.
    """
    links, rechts = tabellen(anforderungen, tests)
    try:
        ergebnis = funktion(links, rechts)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"
    if not isinstance(ergebnis, pl.DataFrame):
        return f"keinen polars-DataFrame, sondern {type(ergebnis).__name__}: {ergebnis!r}"
    return ergebnis.to_dicts()


def vergleich_status(anforderungen, tests):
    """Vergleichslösung für status_je_anforderung mit Schleifen und Dictionaries."""
    zeilen = []
    for kennung, art, prioritaet in sorted(anforderungen):
        eigene = [bestanden for anforderung, _, bestanden in tests if anforderung == kennung]
        anzahl = len(eigene)
        gut = sum(1 for bestanden in eigene if bestanden)
        if anzahl == 0:
            status = "offen"
        elif gut == anzahl:
            status = "erfüllt"
        else:
            status = "verfehlt"
        zeilen.append({"id": kennung, "art": art, "prioritaet": prioritaet, "tests": anzahl, "bestanden": gut, "status": status})
    return zeilen


def vergleich_bericht(anforderungen, tests):
    """Vergleichslösung für abnahmebericht."""
    je_art = {}
    for zeile in vergleich_status(anforderungen, tests):
        anzahl, erfuellt = je_art.get(zeile["art"], (0, 0))
        je_art[zeile["art"]] = (anzahl + 1, erfuellt + (zeile["status"] == "erfüllt"))
    return [{"art": art, "anzahl": anzahl, "erfuellt": erfuellt, "quote": round(erfuellt / anzahl * 100, 1)} for art, (anzahl, erfuellt) in sorted(je_art.items())]


def vergleich_blockierende(anforderungen, tests):
    """Vergleichslösung für blockierende."""
    return [{"id": z["id"], "status": z["status"]} for z in vergleich_status(anforderungen, tests) if z["prioritaet"] == "muss" and z["status"] != "erfüllt"]


def gleich(ergebnis, erwartet):
    """True, wenn zwei Listen von Zeilen gleich sind; quote darf um 0.11 abweichen (Rundung)."""
    if not isinstance(ergebnis, list) or len(ergebnis) != len(erwartet):
        return False
    for zeile, soll in zip(ergebnis, erwartet):
        if list(zeile) != list(soll):
            return False
        for spalte, wert in soll.items():
            if spalte == "quote":
                if zeile[spalte] is None or abs(zeile[spalte] - wert) > 0.11:
                    return False
            elif zeile[spalte] != wert:
                return False
    return True


# status_je_anforderung im Beispiel: Anzahl der Tests je Anforderung
ergebnis = zeilen_von(status_je_anforderung, BEISPIEL_ANFORDERUNGEN, BEISPIEL_TESTS)
anzahlen = [zeile.get("tests") for zeile in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert anzahlen == [2, 2, 1, 0, 1], (
    f"status_je_anforderung ergibt in der Spalte tests {anzahlen!r}, erwartet war [2, 2, 1, 0, 1].\n"
    "Tipp: Zählen Sie mit tests.group_by(\"anforderung\").agg(pl.len().alias(\"tests\")), verknüpfen Sie mit how=\"left\" "
    "und ersetzen Sie fehlende Werte mit fill_null(0)."
)

# status_je_anforderung im Beispiel: Anzahl der bestandenen Tests
bestanden = [zeile.get("bestanden") for zeile in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert bestanden == [2, 1, 0, 0, 1], (
    f"status_je_anforderung ergibt in der Spalte bestanden {bestanden!r}, erwartet war [2, 1, 0, 0, 1].\n"
    "Tipp: pl.col(\"bestanden\").sum() zählt die True-Werte."
)

# status_je_anforderung im Beispiel: der Status
status = [zeile.get("status") for zeile in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert status == ["erfüllt", "verfehlt", "verfehlt", "offen", "erfüllt"], (
    f"status_je_anforderung ergibt in der Spalte status {status!r}, erwartet war ['erfüllt', 'verfehlt', 'verfehlt', 'offen', 'erfüllt'].\n"
    "Tipp: pl.when(pl.col(\"tests\") == 0).then(pl.lit(\"offen\")).when(…).then(…).otherwise(…)"
)

# status_je_anforderung im Beispiel: alle Spalten in der richtigen Reihenfolge
erwartet = vergleich_status(BEISPIEL_ANFORDERUNGEN, BEISPIEL_TESTS)
assert gleich(ergebnis, erwartet), f"status_je_anforderung ergibt {ergebnis!r}, erwartet war {erwartet}."

# status_je_anforderung mit anderen Daten, unsortiert (nicht fest hinschreiben!)
andere_anforderungen = [("B7", "funktional", "muss"), ("B2", "nicht funktional", "soll"), ("B5", "funktional", "muss")]
andere_tests = [("B5", "X1", False), ("B5", "X2", False), ("B2", "X3", True), ("B7", "X4", True), ("B7", "X5", False), ("B2", "X6", True)]
ergebnis = zeilen_von(status_je_anforderung, andere_anforderungen, andere_tests)
erwartet = vergleich_status(andere_anforderungen, andere_tests)
assert gleich(ergebnis, erwartet), f"status_je_anforderung ergibt {ergebnis!r}, erwartet war {erwartet}.\nTipp: Sortieren Sie am Ende mit sort(\"id\")."

# status_je_anforderung: keine Tests, alles offen
ergebnis = zeilen_von(status_je_anforderung, BEISPIEL_ANFORDERUNGEN, [])
erwartet = vergleich_status(BEISPIEL_ANFORDERUNGEN, [])
assert gleich(ergebnis, erwartet), f"status_je_anforderung ohne Tests ergibt {ergebnis!r}, erwartet war {erwartet}."

# status_je_anforderung: keine Anforderungen
ergebnis = zeilen_von(status_je_anforderung, [], BEISPIEL_TESTS)
assert ergebnis == [], f"status_je_anforderung ohne Anforderungen ergibt {ergebnis!r}, erwartet war ein leerer DataFrame."

# status_je_anforderung verändert die übergebenen Tabellen nicht
links, rechts = tabellen(BEISPIEL_ANFORDERUNGEN, BEISPIEL_TESTS)
try:
    status_je_anforderung(links, rechts)
except Exception:
    pass
assert links.equals(tabellen(BEISPIEL_ANFORDERUNGEN, [])[0]) and rechts.shape == (7, 3), "status_je_anforderung hat eine der übergebenen Tabellen verändert."

# abnahmebericht im Beispiel
ergebnis = zeilen_von(abnahmebericht, BEISPIEL_ANFORDERUNGEN, BEISPIEL_TESTS)
erwartet = vergleich_bericht(BEISPIEL_ANFORDERUNGEN, BEISPIEL_TESTS)
assert gleich(ergebnis, erwartet), (
    f"abnahmebericht ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: Gruppieren Sie das Ergebnis von status_je_anforderung nach art; (pl.col(\"status\") == \"erfüllt\").sum() zählt die erfüllten."
)

# abnahmebericht mit anderen Daten (nicht fest hinschreiben!)
ergebnis = zeilen_von(abnahmebericht, andere_anforderungen, andere_tests)
erwartet = vergleich_bericht(andere_anforderungen, andere_tests)
assert gleich(ergebnis, erwartet), f"abnahmebericht ergibt {ergebnis!r}, erwartet war {erwartet}."

# abnahmebericht: nur eine Art, alles erfüllt
nur_eine = [("C1", "nicht funktional", "muss"), ("C2", "nicht funktional", "soll")]
ergebnis = zeilen_von(abnahmebericht, nur_eine, [("C1", "T", True), ("C2", "T", True)])
assert gleich(ergebnis, [{"art": "nicht funktional", "anzahl": 2, "erfuellt": 2, "quote": 100.0}]), f"abnahmebericht mit nur nicht funktionalen Anforderungen ergibt {ergebnis!r}."

# abnahmebericht: keine Anforderungen
ergebnis = zeilen_von(abnahmebericht, [], [])
assert ergebnis == [], f"abnahmebericht ohne Anforderungen ergibt {ergebnis!r}, erwartet war ein leerer DataFrame."

# blockierende im Beispiel
ergebnis = zeilen_von(blockierende, BEISPIEL_ANFORDERUNGEN, BEISPIEL_TESTS)
assert ergebnis == [{"id": "A3", "status": "verfehlt"}], f"blockierende ergibt {ergebnis!r}, erwartet war [{{'id': 'A3', 'status': 'verfehlt'}}]."

# blockierende: auch offene Muss-Anforderungen blockieren
ergebnis = zeilen_von(blockierende, andere_anforderungen + [("B1", "funktional", "muss")], andere_tests)
erwartet = vergleich_blockierende(andere_anforderungen + [("B1", "funktional", "muss")], andere_tests)
assert ergebnis == erwartet, f"blockierende ergibt {ergebnis!r}, erwartet war {erwartet}."

# blockierende: alles erfüllt, nichts blockiert
ergebnis = zeilen_von(blockierende, [("D1", "funktional", "muss")], [("D1", "T", True)])
assert ergebnis == [], f"blockierende ergibt {ergebnis!r}, erwartet war []."

# Die Ausgabe des Programms
erwartet = (
    "['erfüllt', 'verfehlt', 'verfehlt', 'offen', 'erfüllt']\n"
    "[{'art': 'funktional', 'anzahl': 3, 'erfuellt': 2, 'quote': 66.7}, {'art': 'nicht funktional', 'anzahl': 2, 'erfuellt': 0, 'quote': 0.0}]\n"
    "[{'id': 'A3', 'status': 'verfehlt'}]"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

zufall = Zufall(4057)
lastenhefte = []
for _ in range(40):
    kennungen = [f"R{nummer:03d}" for nummer in zufall.sample(range(1000), zufall.randint(0, 12))]
    anforderungen_zufall = [(k, zufall.choice(["funktional", "nicht funktional"]), zufall.choice(["muss", "soll", "kann"])) for k in kennungen]
    moegliche = kennungen + ["R999X"]
    tests_zufall = [(zufall.choice(moegliche), f"T{n}", zufall.random() < 0.7) for n in range(zufall.randint(0, 30))]
    lastenhefte.append((anforderungen_zufall, tests_zufall))


def pruefe_zufaellig(funktion, vergleich):
    """Vergleicht funktion mit der Vergleichslösung für alle zufälligen Lastenhefte; gibt (stimmt, Meldung) zurück."""
    for anforderungen_zufall, tests_zufall in lastenhefte:
        ergebnis = zeilen_von(funktion, anforderungen_zufall, tests_zufall)
        erwartet = vergleich(anforderungen_zufall, tests_zufall)
        if not gleich(ergebnis, erwartet):
            return False, f"{funktion.__name__}({anforderungen_zufall}, {tests_zufall}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    return True, ""


# Viele zufällige Lastenhefte: status_je_anforderung
stimmt, meldung = pruefe_zufaellig(status_je_anforderung, vergleich_status)
assert stimmt, meldung

# Viele zufällige Lastenhefte: abnahmebericht
stimmt, meldung = pruefe_zufaellig(abnahmebericht, vergleich_bericht)
assert stimmt, meldung

# Viele zufällige Lastenhefte: blockierende
stimmt, meldung = pruefe_zufaellig(blockierende, vergleich_blockierende)
assert stimmt, meldung

# Obere Grenze: 1000 Anforderungen und 10 000 Tests
anforderungen_gross = [(f"R{n:04d}", zufall.choice(["funktional", "nicht funktional"]), zufall.choice(["muss", "soll", "kann"])) for n in range(1000)]
tests_gross = [(f"R{zufall.randint(0, 1100):04d}", f"T{n}", zufall.random() < 0.9) for n in range(10000)]
ergebnis = zeilen_von(abnahmebericht, anforderungen_gross, tests_gross)
assert gleich(ergebnis, vergleich_bericht(anforderungen_gross, tests_gross)), "Bei 1000 Anforderungen und 10 000 Tests stimmt abnahmebericht nicht."
