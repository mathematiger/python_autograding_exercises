# Automatisch erzeugt aus lehrkraft/muster/5_009_abdeckungsverlauf.py - nicht von Hand ändern.
# vorlage-hash: 4b8a357ae99ddb1e
# text-hash: 5f2e619c91bc3dd9
# thema: datenanalyse
# inhalt: DuckDB: Fensterfunktionen

def tabelle(zeilen):
    """Baut aus Tupeln (modul, build, abdeckung) den DataFrame mit festen Datentypen, auch wenn er leer ist."""
    return pd.DataFrame(
        {
            "modul": pd.Series([z[0] for z in zeilen], dtype=object),
            "build": pd.Series([z[1] for z in zeilen], dtype="int64"),
            "abdeckung": pd.Series([z[2] for z in zeilen], dtype="int64"),
        }
    )


def nach_modul(zeilen):
    """Ordnet jedem Modul die Liste (build, abdeckung) zu, nach build sortiert."""
    gruppen = {}
    for modul, build, abdeckung in zeilen:
        gruppen.setdefault(modul, []).append((build, abdeckung))
    return {modul: sorted(paare) for modul, paare in sorted(gruppen.items())}


def schnitt_von_hand(zeilen):
    """Rechnet den gleitenden Schnitt mit Python-Listen nach."""
    ergebnis = []
    for modul, paare in nach_modul(zeilen).items():
        for index, (build, _) in enumerate(paare):
            fenster = [abdeckung for _, abdeckung in paare[max(0, index - 2) : index + 1]]
            ergebnis.append((modul, build, sum(fenster) / len(fenster)))
    return ergebnis


def rueckschritte_von_hand(zeilen):
    """Sucht die Builds mit gesunkener Abdeckung mit Python-Listen."""
    ergebnis = []
    for modul, paare in nach_modul(zeilen).items():
        for (_, vorher), (build, jetzt) in zip(paare, paare[1:]):
            if jetzt < vorher:
                ergebnis.append((modul, build, vorher, jetzt))
    return ergebnis


def stand_von_hand(zeilen):
    """Nimmt zu jedem Modul das letzte Paar der sortierten Liste."""
    return [(modul, paare[-1][0], paare[-1][1]) for modul, paare in nach_modul(zeilen).items()]


def gleich_mit_toleranz(ergebnis, erwartet):
    """Vergleicht Listen von Tupeln; Kommazahlen dürfen in der letzten Stelle abweichen."""
    if not isinstance(ergebnis, list) or len(ergebnis) != len(erwartet):
        return False
    for zeile, soll in zip(ergebnis, erwartet):
        if not isinstance(zeile, tuple) or len(zeile) != len(soll):
            return False
        for wert, sollwert in zip(zeile, soll):
            if isinstance(sollwert, float):
                if not isinstance(wert, (int, float)) or abs(wert - sollwert) > 1e-9:
                    return False
            elif wert != sollwert or type(wert) is not type(sollwert):
                return False
    return True


BEISPIEL = [("api", 1, 60), ("api", 2, 70), ("ui", 1, 40), ("api", 3, 65), ("ui", 4, 45), ("api", 7, 80)]
builds = tabelle(BEISPIEL)

# gleitender_schnitt aus dem Beispiel
ergebnis = gleitender_schnitt(builds)
erwartet = [("api", 1, 60.0), ("api", 2, 65.0), ("api", 3, 65.0), ("api", 7, 215 / 3), ("ui", 1, 40.0), ("ui", 4, 42.5)]
assert gleich_mit_toleranz(ergebnis, erwartet), (
    f"gleitender_schnitt(builds) ergibt für das Beispiel\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
    "Tipp: AVG(abdeckung) OVER (PARTITION BY modul ORDER BY build ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), "
    "und am Ende ORDER BY modul, build."
)

# rueckschritte aus dem Beispiel
ergebnis = rueckschritte(builds)
assert gleich_mit_toleranz(ergebnis, [("api", 3, 70, 65)]), (
    f"rueckschritte(builds) ergibt {ergebnis!r}, erwartet war [('api', 3, 70, 65)].\n"
    "Tipp: LAG(abdeckung) OVER (PARTITION BY modul ORDER BY build) ist der Wert des vorigen Builds; filtern Sie "
    "außen in einer Unterabfrage oder mit QUALIFY, denn in WHERE geht das nicht."
)

# neuester_stand aus dem Beispiel
ergebnis = neuester_stand(builds)
assert gleich_mit_toleranz(ergebnis, [("api", 7, 80), ("ui", 4, 45)]), (
    f"neuester_stand(builds) ergibt {ergebnis!r}, erwartet war [('api', 7, 80), ('ui', 4, 45)].\n"
    "Tipp: ROW_NUMBER() OVER (PARTITION BY modul ORDER BY build DESC) ist beim neuesten Build 1."
)

# Das Fenster endet am Anfang des Moduls, und Module mischen sich nicht
zeilen = [("b", 5, 10), ("a", 9, 90), ("b", 2, 30), ("a", 1, 0), ("b", 9, 20), ("b", 7, 20), ("a", 4, 100)]
erwartet = [("a", 1, 0.0), ("a", 4, 50.0), ("a", 9, 190 / 3), ("b", 2, 30.0), ("b", 5, 20.0), ("b", 7, 20.0), ("b", 9, 50 / 3)]
ergebnis = gleitender_schnitt(tabelle(zeilen))
assert gleich_mit_toleranz(ergebnis, erwartet), (
    f"gleitender_schnitt mit den Zeilen {zeilen} ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
    "Tipp: Das Fenster geht nach der Buildnummer, nicht nach der Reihenfolge im DataFrame, und nur innerhalb eines Moduls."
)

# Rückschritte: gleich bleiben ist kein Rückschritt, der erste Build eines Moduls auch nicht
ergebnis = rueckschritte(tabelle(zeilen))
erwartet = [("a", 9, 100, 90), ("b", 5, 30, 10)]
assert gleich_mit_toleranz(ergebnis, erwartet), (
    f"rueckschritte mit den Zeilen {zeilen} ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Nur echt kleiner zählt; beim ersten Build ist LAG NULL, und ein Vergleich mit NULL ist nie wahr."
)

# Neuester Stand nach der größten Nummer, nicht nach der letzten Zeile
ergebnis = neuester_stand(tabelle(zeilen))
erwartet = [("a", 9, 90), ("b", 9, 20)]
assert gleich_mit_toleranz(ergebnis, erwartet), f"neuester_stand mit den Zeilen {zeilen} ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Leere Tabelle und eine einzige Zeile
for zeilen, erwartet in [([], ([], [], [])), ([("x_1", 10**6, 100)], ([("x_1", 10**6, 100.0)], [], [("x_1", 10**6, 100)]))]:
    daten = tabelle(zeilen)
    ergebnis = (gleitender_schnitt(daten), rueckschritte(daten), neuester_stand(daten))
    assert all(gleich_mit_toleranz(e, s) for e, s in zip(ergebnis, erwartet)), (
        f"Bei den Zeilen {zeilen} ergeben die drei Funktionen {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Der DataFrame bleibt unverändert
daten = tabelle(BEISPIEL)
gleitender_schnitt(daten)
rueckschritte(daten)
neuester_stand(daten)
assert list(daten.itertuples(index=False, name=None)) == BEISPIEL and list(daten.columns) == ["modul", "build", "abdeckung"], (
    "Nach den Auswertungen hat sich der DataFrame verändert; die Funktionen sollen ihn nur lesen."
)

# DuckDB wird benutzt, ohne Python-Schleife
assert (verwendet("abfrage") or verwendet("sql")) and not verwendet("for"), (
    "Lassen Sie DuckDB rechnen: Geben Sie die SQL-Abfrage an die Hilfsfunktion abfrage(builds, sql) "
    "und schreiben Sie keine for-Schleife."
)

# 50 zufällige Buildverläufe, verglichen mit einer Rechnung in Python
zufall = Zufall(5009)
for _ in range(50):
    zeilen = []
    for modul in zufall.sample(["api", "ui", "db", "core_2", "x"], zufall.randint(0, 3)):
        for build in zufall.sample(range(1, 30), zufall.randint(1, 6)):
            zeilen.append((modul, build, zufall.choice([0, 100, 50, zufall.randint(0, 100)])))
    zufall.shuffle(zeilen)
    daten = tabelle(zeilen)
    for funktion, vergleich in [(gleitender_schnitt, schnitt_von_hand), (rueckschritte, rueckschritte_von_hand), (neuester_stand, stand_von_hand)]:
        ergebnis = funktion(daten)
        erwartet = vergleich(zeilen)
        assert gleich_mit_toleranz(ergebnis, erwartet), (
            f"{funktion.__name__} mit den Zeilen {zeilen} ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"
        )

# An der oberen Grenze: 100 000 Zeilen, Zahl der Python-Zeilen bleibt klein
zeilen = [(f"modul{nummer % 50}", (nummer * 7919) % 10**6 + 1, (nummer * 37) % 101) for nummer in range(100000)]
daten = tabelle(zeilen)
schnitt, schritte_schnitt = zaehle_schritte(gleitender_schnitt, daten)
rueck, schritte_rueck = zaehle_schritte(rueckschritte, daten)
stand, schritte_stand = zaehle_schritte(neuester_stand, daten)
ok = gleich_mit_toleranz(schnitt, schnitt_von_hand(zeilen)) and gleich_mit_toleranz(rueck, rueckschritte_von_hand(zeilen))
ok = ok and gleich_mit_toleranz(stand, stand_von_hand(zeilen))
assert ok and max(schritte_schnitt, schritte_rueck, schritte_stand) <= 30, (
    f"Bei 100 000 Zeilen stimmen die Ergebnisse{'' if ok else ' nicht'}; die drei Funktionen brauchen "
    f"{schritte_schnitt}, {schritte_rueck} und {schritte_stand} ausgeführte Python-Zeilen, erwartet waren je höchstens 30.\n"
    "Tipp: Rechnen Sie alles in einer SQL-Abfrage und geben Sie fetchall() direkt zurück."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "[('api', 1, 60.0), ('api', 2, 65.0), ('api', 3, 65.0), ('api', 7, 71.67), ('ui', 1, 40.0), ('ui', 4, 42.5)]\n"
    "[('api', 3, 70, 65)]\n"
    "[('api', 7, 80), ('ui', 4, 45)]"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
