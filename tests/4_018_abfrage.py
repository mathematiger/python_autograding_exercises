# Automatisch erzeugt aus lehrkraft/muster/4_018_abfrage.py - nicht von Hand ändern.
# vorlage-hash: 06f50f2a50161777
# text-hash: 23167d15aea4ce9f
# thema: funktionen
# inhalt: *args und **kwargs

import inspect


def kunden_tabelle():
    """Baut die Beispieltabelle aus der Aufgabe neu."""
    return [
        {"nr": 1, "name": "Ada", "ort": "Bonn", "status": "aktiv"},
        {"nr": 2, "name": "Bo", "ort": "Jena", "status": "aktiv"},
        {"nr": 3, "name": "Cem", "ort": "Bonn", "status": "gesperrt"},
    ]


def arten(funktion):
    """Gibt die Arten der Parameter zurück: "normal", "*" oder "**"."""
    namen = {inspect.Parameter.VAR_POSITIONAL: "*", inspect.Parameter.VAR_KEYWORD: "**"}
    return [namen.get(parameter.kind, "normal") for parameter in inspect.signature(funktion).parameters.values()]


# Die Funktionen sammeln ihre Argumente mit * und **
ergebnis = (arten(filtere), arten(waehle), arten(abfrage))
assert ergebnis == (["normal", "**"], ["normal", "*"], ["normal", "*", "**"]), (
    f"Die Parameterlisten haben die Arten {ergebnis}; erwartet war filtere(tabelle, **bedingungen), "
    "waehle(tabelle, *spalten) und abfrage(tabelle, *spalten, **bedingungen).\n"
    "Tipp: Ändern Sie die vorgegebenen Funktionsköpfe nicht."
)

# filtere aus dem Beispiel
kunden = kunden_tabelle()
ergebnis = [zeile["name"] for zeile in filtere(kunden, ort="Bonn")]
assert ergebnis == ["Ada", "Cem"], (
    f'filtere(kunden, ort="Bonn") liefert die Zeilen von {ergebnis}, erwartet waren Ada und Cem.\n'
    'Tipp: bedingungen ist ein Dictionary, hier {"ort": "Bonn"}; gehen Sie mit .items() hindurch.'
)

# Mehrere Bedingungen müssen alle gelten
ergebnis = [zeile["name"] for zeile in filtere(kunden, ort="Bonn", status="aktiv")]
assert ergebnis == ["Ada"], (
    f'filtere(kunden, ort="Bonn", status="aktiv") liefert die Zeilen von {ergebnis}, erwartet war nur Ada.\n'
    "Tipp: Eine Zeile passt nur, wenn jede Bedingung stimmt, nicht schon, wenn eine stimmt."
)

# Ohne Bedingungen passen alle Zeilen, ohne Treffer kommt []
ergebnis = (filtere(kunden), filtere(kunden, ort="Kiel"), filtere([], ort="Bonn"), filtere([]))
assert ergebnis == (kunden, [], [], []), (
    f'filtere(kunden), filtere(kunden, ort="Kiel"), filtere([], ort="Bonn") und filtere([]) ergeben {ergebnis!r}; '
    "erwartet war die ganze Tabelle und dreimal []."
)

# Eine Zeile ohne die genannte Spalte passt nicht, auch Zahlen und negative Werte werden verglichen
tabelle = [{"nr": 1, "rabatt": -5}, {"nr": 2}, {"nr": 3, "rabatt": 0}, {"nr": 4, "rabatt": -5}]
try:
    ergebnis = [zeile["nr"] for zeile in filtere(tabelle, rabatt=-5)]
except KeyError as fehler:
    ergebnis = f"KeyError {fehler}"
assert ergebnis == [1, 4], (
    f"filtere({tabelle}, rabatt=-5) liefert die Zeilen mit nr {ergebnis!r}, erwartet waren 1 und 4.\n"
    'Tipp: Fehlt die Spalte, passt die Zeile nicht; zeile[spalte] würde dann einen KeyError auslösen, "spalte in zeile" nicht.'
)

# Eine Bedingung auf eine Spalte, die keine Zeile hat
assert filtere(tabelle, ort="Bonn") == [], f'filtere({tabelle}, ort="Bonn") ergibt {filtere(tabelle, ort="Bonn")!r}, erwartet war [].'

# waehle aus dem Beispiel, Spalten in der Reihenfolge des Aufrufs
ergebnis = waehle(kunden, "name", "nr")
erwartet = [{"name": "Ada", "nr": 1}, {"name": "Bo", "nr": 2}, {"name": "Cem", "nr": 3}]
assert ergebnis == erwartet and [list(zeile) for zeile in ergebnis] == [["name", "nr"]] * 3, (
    f'waehle(kunden, "name", "nr") ergibt {ergebnis!r}, erwartet war {erwartet!r} (Spalten in dieser Reihenfolge).\n'
    "Tipp: spalten ist ein Tupel; bauen Sie für jede Zeile ein neues Dictionary in der Reihenfolge von spalten."
)

# Ohne Spalten kommen Kopien aller Zeilen
ergebnis = waehle(kunden)
gleich = ergebnis == kunden_tabelle()
if ergebnis:
    ergebnis[0]["name"] = "geändert"
assert gleich and kunden == kunden_tabelle(), (
    f"waehle(kunden) soll Kopien aller Zeilen mit allen Spalten liefern, deren Änderung die Tabelle nicht berührt; "
    f"{'das Ergebnis enthält nicht alle Zeilen und Spalten' if not gleich else 'nach einer Änderung am Ergebnis hat sich die Tabelle verändert'}.\n"
    "Tipp: Ist spalten leer, macht dict(zeile) eine Kopie der ganzen Zeile."
)

# Eine fehlende Spalte löst ValueError mit ihrem Namen aus
for tabelle, spalten in [(kunden, ("telefon",)), ([{"nr": 1, "name": "Ada"}, {"nr": 2}], ("nr", "name"))]:
    try:
        waehle(tabelle, *spalten)
        meldung = None
    except ValueError as ausnahme:
        meldung = str(ausnahme)
    except KeyError as ausnahme:
        meldung = f"KeyError {ausnahme}"
    fehlend = spalten[-1]
    assert meldung is not None and not meldung.startswith("KeyError") and fehlend in meldung, (
        f"waehle({tabelle}, {', '.join(map(repr, spalten))}) muss einen ValueError auslösen, dessen Meldung "
        f"{fehlend!r} enthält; bekommen: {meldung!r}.\n"
        "Tipp: Prüfen Sie mit spalte in zeile und lösen Sie raise ValueError(f\"Spalte {spalte} fehlt\") aus."
    )

# waehle auf einer leeren Tabelle und eine Tabelle mit verschiedenen Spalten
tabelle = [{"nr": 1, "ort": "Bonn"}, {"nr": 2, "plz": "07743"}]
ergebnis = (waehle([], "nr"), waehle([]), waehle(tabelle, "nr"), waehle(tabelle))
assert ergebnis == ([], [], [{"nr": 1}, {"nr": 2}], tabelle), (
    f'waehle([], "nr"), waehle([]), waehle({tabelle}, "nr") und waehle({tabelle}) ergeben {ergebnis!r}; '
    f"erwartet war ([], [], [{{'nr': 1}}, {{'nr': 2}}], {tabelle!r})."
)

# abfrage aus dem Beispiel
try:
    ergebnis = abfrage(kunden, "name", status="aktiv")
except TypeError as fehler:
    ergebnis = f"TypeError: {fehler}"
assert ergebnis == [{"name": "Ada"}, {"name": "Bo"}], (
    f'abfrage(kunden, "name", status="aktiv") ergibt {ergebnis!r}, erwartet war [{{"name": "Ada"}}, {{"name": "Bo"}}].\n'
    "Tipp: Reichen Sie weiter: waehle(filtere(tabelle, **bedingungen), *spalten)."
)

# abfrage mit mehreren Spalten und Bedingungen, ohne Spalten, ohne Bedingungen
for spalten, bedingungen, erwartet in [
    (("nr", "ort"), {"ort": "Bonn", "status": "gesperrt"}, [{"nr": 3, "ort": "Bonn"}]),
    ((), {"nr": 2}, [kunden_tabelle()[1]]),
    (("nr",), {}, [{"nr": 1}, {"nr": 2}, {"nr": 3}]),
    ((), {}, kunden_tabelle()),
    (("telefon",), {"ort": "Kiel"}, []),
]:
    ergebnis = abfrage(kunden, *spalten, **bedingungen)
    aufruf = ", ".join(["kunden"] + [repr(s) for s in spalten] + [f"{k}={v!r}" for k, v in bedingungen.items()])
    assert ergebnis == erwartet, (
        f"abfrage({aufruf}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Ohne * und ** beim Weiterreichen kommen spalten als ein einziges Tupel und bedingungen als ein Dictionary an."
    )

# abfrage meldet eine fehlende Spalte wie waehle, aber nur in den gefilterten Zeilen
tabelle = [{"nr": 1, "name": "Ada"}, {"nr": 2}]
try:
    ergebnis = abfrage(tabelle, "name", nr=1)
    meldung = None
except ValueError as ausnahme:
    ergebnis = None
    meldung = str(ausnahme)
try:
    abfrage(tabelle, "name", nr=2)
    meldung_zwei = None
except ValueError as ausnahme:
    meldung_zwei = str(ausnahme)
assert ergebnis == [{"name": "Ada"}] and meldung_zwei is not None and "name" in meldung_zwei, (
    f'Bei der Tabelle {tabelle} soll abfrage(tabelle, "name", nr=1) [{{"name": "Ada"}}] ergeben und '
    f'abfrage(tabelle, "name", nr=2) einen ValueError mit "name" auslösen; bekommen {ergebnis!r} '
    f"(Meldung {meldung!r}) und Meldung {meldung_zwei!r}.\nTipp: Erst filtern, dann auswählen."
)

# Die Tabelle bleibt unverändert
kunden = kunden_tabelle()
filtere(kunden, ort="Bonn")
waehle(kunden, "nr")
abfrage(kunden, "name", status="aktiv")
assert kunden == kunden_tabelle(), f"Nach den Aufrufen ist die Tabelle {kunden!r}; sie soll unverändert bleiben."


# Vergleichslösung mit all() und Mengen statt Schleifen mit break
def abfrage_von_hand(tabelle, spalten, bedingungen):
    """Rechnet abfrage nach; gibt bei einer fehlenden Spalte den Text "ValueError" zurück."""
    treffer = [zeile for zeile in tabelle if all(k in zeile and zeile[k] == v for k, v in bedingungen.items())]
    if not spalten:
        return [dict(zeile) for zeile in treffer]
    if any(not set(spalten) <= set(zeile) for zeile in treffer):
        return "ValueError"
    return [{s: zeile[s] for s in spalten} for zeile in treffer]


# 300 zufällige Tabellen und Abfragen
zufall = Zufall(4018)
SPALTEN = ["nr", "ort", "status", "punkte"]
WERTE = {"nr": [1, 2, 3], "ort": ["Bonn", "Jena"], "status": ["aktiv", "gesperrt"], "punkte": [-1, 0, 10**9]}
for _ in range(300):
    tabelle = []
    for _ in range(zufall.randint(0, 6)):
        spalten_der_zeile = zufall.sample(SPALTEN, zufall.randint(1, 4))
        tabelle.append({s: zufall.choice(WERTE[s]) for s in spalten_der_zeile})
    bedingungen = {s: zufall.choice(WERTE[s]) for s in zufall.sample(SPALTEN, zufall.randint(0, 2))}
    spalten = tuple(zufall.sample(SPALTEN, zufall.randint(0, 2)))
    erwartet = abfrage_von_hand(tabelle, spalten, bedingungen)
    try:
        ergebnis = abfrage(tabelle, *spalten, **bedingungen)
    except ValueError:
        ergebnis = "ValueError"
    aufruf = ", ".join([repr(tabelle)] + [repr(s) for s in spalten] + [f"{k}={v!r}" for k, v in bedingungen.items()])
    assert ergebnis == erwartet, f"abfrage({aufruf}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    nur_gefiltert = [zeile for zeile in tabelle if all(k in zeile and zeile[k] == v for k, v in bedingungen.items())]
    ergebnis = filtere(tabelle, **bedingungen)
    assert ergebnis == nur_gefiltert, f"filtere({tabelle!r}, **{bedingungen!r}) ergibt {ergebnis!r}, erwartet war {nur_gefiltert!r}."

# An der oberen Grenze: 100 000 Zeilen mit 20 Spalten, 19 Bedingungen, alle 20 Spalten auswählen
namen = [f"feld_{nummer}" for nummer in range(19)]
gross = [{"nr": nummer, **{name: nummer % 2 for name in namen}} for nummer in range(100000)]
gross[99999]["feld_18"] = 5
bedingungen = {name: 1 for name in namen[:18]}
bedingungen["feld_18"] = 1
ergebnis = abfrage(gross, "nr", *namen, **bedingungen)
assert len(ergebnis) == 49999 and ergebnis[0]["nr"] == 1 and ergebnis[-1]["nr"] == 99997 and list(ergebnis[0]) == ["nr", *namen], (
    f"Bei 100 000 Zeilen, 19 Bedingungen und 20 Spalten liefert abfrage {len(ergebnis)} Zeilen, "
    f"die erste mit nr {ergebnis[0]['nr'] if ergebnis else None!r}, die letzte mit nr {ergebnis[-1]['nr'] if ergebnis else None!r}; "
    "erwartet waren 49999 Zeilen von nr 1 bis nr 99997 mit allen 20 Spalten."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "2 1\n"
    "[{'name': 'Ada', 'nr': 1}, {'name': 'Bo', 'nr': 2}, {'name': 'Cem', 'nr': 3}]\n"
    "[{'name': 'Ada'}, {'name': 'Bo'}]"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
