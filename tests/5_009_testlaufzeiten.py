# Automatisch erzeugt aus lehrkraft/muster/5_009_testlaufzeiten.py - nicht von Hand ändern.
# vorlage-hash: 54cc71dacde15288
# text-hash: ef55a3010b895d68
# thema: datenanalyse
# inhalt: DuckDB: Fensterfunktionen

def tabelle(zeilen):
    """Baut das DataFrame der Läufe aus einer Liste von Tupeln (build, modul, test, dauer_ms)."""
    return pd.DataFrame(zeilen, columns=["build", "modul", "test", "dauer_ms"])


def als_liste(ergebnis):
    """Macht aus dem Ergebnis eine Liste von Tupeln mit Python-Zahlen, damit der Vergleich nicht am Typ scheitert."""
    try:
        return [tuple(None if wert is None else (wert.item() if hasattr(wert, "item") else wert) for wert in zeile) for zeile in ergebnis]
    except TypeError:
        return ergebnis


def langsamste_von_hand(zeilen, build, k):
    """Vergleichslösung in Python: sortieren und je Modul abzählen."""
    im_build = [zeile for zeile in zeilen if zeile[0] == build]
    im_build.sort(key=lambda zeile: (zeile[1], -zeile[3], zeile[2]))
    ergebnis = []
    platz = 0
    vorheriges_modul = None
    for _, modul, test, dauer in im_build:
        platz = platz + 1 if modul == vorheriges_modul else 1
        vorheriges_modul = modul
        if platz <= k:
            ergebnis.append((modul, test, dauer, platz))
    return ergebnis


def veraenderungen_von_hand(zeilen):
    """Vergleichslösung in Python: nach Test und Build sortieren und mit der Zeile davor vergleichen."""
    sortiert = sorted(zeilen, key=lambda zeile: (zeile[1], zeile[2], zeile[0]))
    ergebnis = []
    vorher = None
    for build, modul, test, dauer in sortiert:
        differenz = None
        if vorher is not None and vorher[1:3] == (modul, test):
            differenz = dauer - vorher[3]
        ergebnis.append((modul, test, build, dauer, differenz))
        vorher = (build, modul, test, dauer)
    return ergebnis


def gesamtdauer_von_hand(zeilen):
    """Vergleichslösung in Python: Summen je Build in einem Dictionary, dann über drei Builds mitteln."""
    summen = {}
    for build, _, _, dauer in zeilen:
        summen[build] = summen.get(build, 0) + dauer
    builds = sorted(summen)
    ergebnis = []
    for nummer, build in enumerate(builds):
        fenster = [summen[b] for b in builds[max(0, nummer - 2) : nummer + 1]]
        ergebnis.append((build, summen[build], sum(fenster) / len(fenster)))
    return ergebnis


def gleich_mit_toleranz(ergebnis, erwartet):
    """True, wenn beide Listen von (build, summe, schnitt) gleich sind; schnitt darf minimal abweichen."""
    if not isinstance(ergebnis, list) or len(ergebnis) != len(erwartet):
        return False
    for zeile, soll in zip(ergebnis, erwartet):
        if not isinstance(zeile, tuple) or len(zeile) != 3 or zeile[:2] != soll[:2]:
            return False
        if not isinstance(zeile[2], (int, float)) or abs(zeile[2] - soll[2]) > 1e-6 * max(1, abs(soll[2])):
            return False
    return True


BEISPIEL = [
    (101, "login", "passwort", 120), (101, "login", "sperre", 340), (101, "login", "token", 80),
    (101, "suche", "volltext", 900), (102, "login", "passwort", 130), (102, "login", "sperre", 310),
    (102, "login", "token", 130), (102, "suche", "volltext", 1250), (103, "login", "passwort", 125),
    (103, "suche", "volltext", 1100),
]

# langsamste_tests aus dem Beispiel, mit Gleichstand bei 130 ms
ergebnis = als_liste(langsamste_tests(tabelle(BEISPIEL), 102, 2))
erwartet = [("login", "sperre", 310, 1), ("login", "passwort", 130, 2), ("suche", "volltext", 1250, 1)]
assert ergebnis == erwartet, (
    f"langsamste_tests(laeufe, 102, 2) ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
    "Tipp: ROW_NUMBER() OVER (PARTITION BY modul ORDER BY dauer_ms DESC, test) nummeriert je Modul durch; "
    "passwort und token brauchen beide 130 ms, passwort kommt alphabetisch zuerst."
)

# Andere Builds und andere k (nicht fest hinschreiben!)
for build, k in [(101, 1), (101, 3), (103, 5), (101, 100)]:
    ergebnis = als_liste(langsamste_tests(tabelle(BEISPIEL), build, k))
    erwartet = langsamste_von_hand(BEISPIEL, build, k)
    assert ergebnis == erwartet, (
        f"langsamste_tests(laeufe, {build}, {k}) ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
        "Tipp: Nur Zeilen des gewünschten Builds zählen, und je Modul höchstens k Tests."
    )

# Gleichstand: Plätze laufen trotzdem durch, kein Platz doppelt
gleich = [(7, "druck", "c", 50), (7, "druck", "a", 50), (7, "druck", "b", 50), (7, "druck", "d", 10)]
ergebnis = als_liste(langsamste_tests(tabelle(gleich), 7, 3))
erwartet = [("druck", "a", 50, 1), ("druck", "b", 50, 2), ("druck", "c", 50, 3)]
assert ergebnis == erwartet, (
    f"Bei drei gleich langen Tests a, b, c ergibt langsamste_tests(…, 7, 3)\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
    "Tipp: RANK() würde allen dreien Platz 1 geben; verlangt sind die Plätze 1, 2, 3 (ROW_NUMBER)."
)

# Unbekannter Build ergibt eine leere Liste
ergebnis = als_liste(langsamste_tests(tabelle(BEISPIEL), 999, 3))
assert ergebnis == [], f"langsamste_tests(laeufe, 999, 3) ergibt {ergebnis!r}, erwartet war [], weil es Build 999 nicht gibt."

# veraenderungen aus dem Beispiel
ergebnis = als_liste(veraenderungen(tabelle(BEISPIEL)))
erwartet = veraenderungen_von_hand(BEISPIEL)
assert ergebnis == erwartet, (
    f"veraenderungen(laeufe) ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
    "Tipp: LAG(dauer_ms) OVER (PARTITION BY modul, test ORDER BY build) liefert die Dauer im vorigen Build "
    "desselben Tests, beim ersten Lauf NULL (in Python None)."
)

# Lücken in den Builds, Test fehlt in einem Build, unsortierte Zeilen, Dauer 0
luecken = [(50, "bericht", "pdf", 0), (10, "bericht", "pdf", 400), (30, "bericht", "csv", 70), (99, "bericht", "csv", 10**7)]
ergebnis = als_liste(veraenderungen(tabelle(luecken)))
erwartet = [("bericht", "csv", 30, 70, None), ("bericht", "csv", 99, 10**7, 10**7 - 70),
            ("bericht", "pdf", 10, 400, None), ("bericht", "pdf", 50, 0, -400)]
assert ergebnis == erwartet, (
    f"veraenderungen mit den Läufen {luecken} ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
    "Tipp: Verglichen wird mit dem vorigen Build, in dem derselbe Test lief, nicht mit build - 1; "
    "die Zeilen sind nicht sortiert."
)

# Gleicher Testname in zwei Modulen ist nicht derselbe Test
zwei_module = [(1, "a", "start", 10), (2, "b", "start", 30), (3, "a", "start", 15)]
ergebnis = als_liste(veraenderungen(tabelle(zwei_module)))
erwartet = [("a", "start", 1, 10, None), ("a", "start", 3, 15, 5), ("b", "start", 2, 30, None)]
assert ergebnis == erwartet, (
    f"veraenderungen mit dem Test start in den Modulen a und b ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
    "Tipp: Ein Test ist durch Modul und Namen bestimmt; PARTITION BY braucht beide Spalten."
)

# gesamtdauer aus dem Beispiel
ergebnis = als_liste(gesamtdauer(tabelle(BEISPIEL)))
erwartet = [(101, 1440, 1440.0), (102, 1820, 1630.0), (103, 1225, 1495.0)]
assert gleich_mit_toleranz(ergebnis, erwartet), (
    f"gesamtdauer(laeufe) ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"
)

# Der gleitende Durchschnitt schaut nur auf drei Builds
fuenf = [(build, "m", "t", dauer) for build, dauer in [(1, 100), (2, 200), (4, 600), (8, 100), (9, 800)]]
ergebnis = als_liste(gesamtdauer(tabelle(fuenf)))
erwartet = [(1, 100, 100.0), (2, 200, 150.0), (4, 600, 300.0), (8, 100, 300.0), (9, 800, 500.0)]
assert gleich_mit_toleranz(ergebnis, erwartet), (
    f"gesamtdauer bei fünf Builds mit den Summen 100, 200, 600, 100, 800 ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
    "Tipp: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW nimmt die aktuelle und die zwei vorigen Zeilen; "
    "ohne Rahmen wäre es der Durchschnitt über alle bisherigen Builds."
)

# Ein einziger Lauf
ergebnis = (als_liste(langsamste_tests(tabelle([(5, "x", "y", 0)]), 5, 1)), als_liste(gesamtdauer(tabelle([(5, "x", "y", 0)]))))
assert ergebnis[0] == [("x", "y", 0, 1)] and gleich_mit_toleranz(ergebnis[1], [(5, 0, 0.0)]), (
    f"Bei nur einem Lauf (5, 'x', 'y', 0) ergeben langsamste_tests(…, 5, 1) und gesamtdauer {ergebnis!r}, "
    "erwartet waren [('x', 'y', 0, 1)] und [(5, 0, 0.0)]."
)

# Die Auswertung läuft über DuckDB
assert verwendet("sql") or verwendet("execute") or verwendet("query"), (
    "Werten Sie mit SQL in DuckDB aus: duckdb.sql(...) oder duckdb.execute(...)."
)

# 60 zufällige Protokolle
zufall = Zufall(5009)
for _ in range(60):
    module = zufall.sample(["api", "db", "ui"], zufall.randint(1, 2))
    tests = ["a", "b", "c"]
    builds = sorted(zufall.sample(range(1, 20), zufall.randint(1, 4)))
    zeilen = [
        (build, modul, test, zufall.choice([zufall.randint(0, 20), zufall.randint(0, 10**7)]))
        for build in builds for modul in module for test in tests if zufall.random() < 0.7
    ] or [(builds[0], module[0], "a", 5)]
    zufall.shuffle(zeilen)
    build = zufall.choice(builds + [99])
    k = zufall.randint(1, 4)
    df = tabelle(zeilen)
    ergebnis = als_liste(langsamste_tests(df, build, k))
    erwartet = langsamste_von_hand(zeilen, build, k)
    assert ergebnis == erwartet, f"langsamste_tests mit den Läufen {zeilen}, build={build}, k={k} ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"
    ergebnis = als_liste(veraenderungen(df))
    erwartet = veraenderungen_von_hand(zeilen)
    assert ergebnis == erwartet, f"veraenderungen mit den Läufen {zeilen} ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"
    ergebnis = als_liste(gesamtdauer(df))
    erwartet = gesamtdauer_von_hand(zeilen)
    assert gleich_mit_toleranz(ergebnis, erwartet), f"gesamtdauer mit den Läufen {zeilen} ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"

# An der oberen Grenze: 10 000 Läufe mit großen Dauern und Build-Nummern
gross = [(10**6 - 1000 * (nummer % 100), f"modul_{nummer % 7}", f"test_{nummer // 100}", (nummer * 7919) % (10**7 + 1)) for nummer in range(10000)]
df = tabelle(gross)
ergebnis = (
    als_liste(langsamste_tests(df, 10**6, 100)) == langsamste_von_hand(gross, 10**6, 100),
    als_liste(veraenderungen(df)) == veraenderungen_von_hand(gross),
    gleich_mit_toleranz(als_liste(gesamtdauer(df)), gesamtdauer_von_hand(gross)),
)
assert ergebnis == (True, True, True), (
    "Bei 10 000 Läufen mit Build-Nummern bis 10**6 und Dauern bis 10**7 stimmen "
    f"langsamste_tests, veraenderungen und gesamtdauer: {ergebnis} (True heißt richtig)."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "[('login', 'sperre', 310, 1), ('login', 'passwort', 130, 2), ('suche', 'volltext', 1250, 1)]\n"
    "[('login', 'passwort', 101, 120, None), ('login', 'passwort', 102, 130, 10), ('login', 'passwort', 103, 125, -5)]\n"
    "[(101, 1440, 1440.0), (102, 1820, 1630.0), (103, 1225, 1495.0)]"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
