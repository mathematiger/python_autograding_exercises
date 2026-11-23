# Automatisch erzeugt aus lehrkraft/muster/5_040_datenknoten.py - nicht von Hand ändern.
# vorlage-hash: 45c7847eb2d83de8
# text-hash: e741c234fafd6111
# thema: nebenlaeufigkeit
# inhalt: asyncio.gather

import inspect
import warnings

warnings.simplefilter("ignore", RuntimeWarning)  # vergessenes await meldet der Test selbst
BEISPIEL_DATEN = {"nord": [("Ada", "Kiel"), ("Bo", "Bonn")], "mitte": [("Cem", "Kiel")], "sued": [("Dana", "Kiel")]}
BEISPIEL_DAUER = {"nord": 3, "mitte": 1, "sued": 2}
DREI = ["nord", "mitte", "sued"]


def ausfuehren(funktion, *argumente):
    """Führt eine Koroutinenfunktion mit asyncio.run aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return asyncio.run(funktion(*argumente))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def aufrufen(funktion, *argumente):
    """Ruft eine gewöhnliche Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def stelle_ein(daten, dauer, ausgefallen=()):
    """Setzt DATEN, DAUER und AUSGEFALLEN neu und leert PROTOKOLL."""
    DATEN.clear()
    DATEN.update(daten)
    DAUER.clear()
    DAUER.update(dauer)
    AUSGEFALLEN.clear()
    AUSGEFALLEN.update(ausgefallen)
    PROTOKOLL.clear()


def gleichzeitig():
    """True, wenn im PROTOKOLL alle Abfragen begonnen haben, bevor die erste fertig war."""
    beginne = [stelle for stelle, eintrag in enumerate(PROTOKOLL) if eintrag.startswith("beginn")]
    fertig = [stelle for stelle, eintrag in enumerate(PROTOKOLL) if not eintrag.startswith("beginn")]
    return not fertig or not beginne or max(beginne) < min(fertig)


def vergleich(knoten, ort, daten, ausgefallen):
    """Vergleichslösung für frage_robust ohne Nebenläufigkeit."""
    namen = []
    for name in knoten:
        if name not in ausgefallen:
            namen += [kunde for kunde, wohnort in daten[name] if wohnort == ort]
    return namen, [name for name in knoten if name in ausgefallen]


# frage_alle ist eine Koroutinenfunktion
assert inspect.iscoroutinefunction(frage_alle), "frage_alle ist keine Koroutinenfunktion. Schreiben Sie async def frage_alle(...):"

# frage_alle: das Beispiel liefert die richtigen Ergebnisse
stelle_ein(BEISPIEL_DATEN, BEISPIEL_DAUER)
ergebnis = ausfuehren(frage_alle, DREI, "Kiel")
assert isinstance(ergebnis, list) and sorted(map(str, ergebnis)) == sorted(map(str, [["Ada"], ["Cem"], ["Dana"]])), (
    f"asyncio.run(frage_alle(['nord', 'mitte', 'sued'], 'Kiel')) ergibt {ergebnis!r}, "
    "erwartet waren die Ergebnisse ['Ada'], ['Cem'] und ['Dana'].\n"
    "Tipp: await asyncio.gather(*[abfrage(name, ort) for name in knoten])."
)

# frage_alle: in der Reihenfolge der Liste, nicht der Antworten
assert ergebnis == [["Ada"], ["Cem"], ["Dana"]], (
    f"frage_alle ergibt {ergebnis!r}, erwartet war [['Ada'], ['Cem'], ['Dana']] in der Reihenfolge der Knoten.\n"
    "Tipp: gather liefert die Ergebnisse in der Reihenfolge der Argumente; sammeln Sie nicht in der Reihenfolge der Antworten."
)

# frage_alle: alle Abfragen laufen gleichzeitig
assert gleichzeitig(), (
    f"Das Protokoll ist {PROTOKOLL}; alle Abfragen sollten beginnen, bevor die erste fertig ist.\n"
    "Tipp: Mit einem await je Knoten in einer Schleife wartet jede Abfrage auf die vorige; übergeben Sie alle an gather."
)

# frage_alle: anderer Ort und andere Reihenfolge (nicht fest hinschreiben!)
stelle_ein(BEISPIEL_DATEN, BEISPIEL_DAUER)
ergebnis = ausfuehren(frage_alle, ["sued", "nord"], "Bonn")
assert ergebnis == [[], ["Bo"]], f"asyncio.run(frage_alle(['sued', 'nord'], 'Bonn')) ergibt {ergebnis!r}, erwartet war [[], ['Bo']]."

# frage_alle: ein Ausfall geht nach außen
stelle_ein(BEISPIEL_DATEN, BEISPIEL_DAUER, {"mitte"})
ergebnis = ausfuehren(frage_alle, DREI, "Kiel")
assert isinstance(ergebnis, str) and ergebnis.startswith("ConnectionError"), (
    f"Mit dem ausgefallenen Knoten mitte ergibt frage_alle {ergebnis!r}; erwartet war ein ConnectionError.\n"
    "Tipp: Ohne return_exceptions gibt gather die Ausnahme einfach weiter; fangen Sie sie hier nicht ab."
)

# frage_alle: keine Knoten
stelle_ein(BEISPIEL_DATEN, BEISPIEL_DAUER)
ergebnis = ausfuehren(frage_alle, [], "Kiel")
assert ergebnis == [], f"asyncio.run(frage_alle([], 'Kiel')) ergibt {ergebnis!r}, erwartet war []."

# frage_robust: ohne Ausfall
stelle_ein(BEISPIEL_DATEN, BEISPIEL_DAUER)
ergebnis = ausfuehren(frage_robust, DREI, "Kiel")
assert ergebnis == (["Ada", "Cem", "Dana"], []), (
    f"asyncio.run(frage_robust(['nord', 'mitte', 'sued'], 'Kiel')) ergibt {ergebnis!r}, "
    "erwartet war (['Ada', 'Cem', 'Dana'], []).\nTipp: Hängen Sie die Ergebnisliste jedes Knotens mit extend an."
)

# frage_robust: das Beispiel mit Ausfall
stelle_ein(BEISPIEL_DATEN, BEISPIEL_DAUER, {"mitte"})
ergebnis = ausfuehren(frage_robust, DREI, "Kiel")
assert ergebnis == (["Ada", "Dana"], ["mitte"]), (
    f"Mit dem ausgefallenen Knoten mitte ergibt frage_robust {ergebnis!r}, erwartet war (['Ada', 'Dana'], ['mitte']).\n"
    "Tipp: Mit return_exceptions=True steht der ConnectionError als Objekt in der Ergebnisliste; prüfen Sie mit isinstance."
)

# frage_robust: alle gleichzeitig, auch mit Ausfall
assert gleichzeitig(), f"Das Protokoll ist {PROTOKOLL}; alle Abfragen sollten beginnen, bevor die erste fertig ist."

# frage_robust: alle ausgefallen
stelle_ein(BEISPIEL_DATEN, BEISPIEL_DAUER, set(DREI))
ergebnis = ausfuehren(frage_robust, DREI, "Kiel")
assert ergebnis == ([], DREI), f"Wenn alle Knoten ausfallen, ergibt frage_robust {ergebnis!r}, erwartet war ([], {DREI})."

# frage_robust: keine Knoten
stelle_ein(BEISPIEL_DATEN, BEISPIEL_DAUER)
ergebnis = ausfuehren(frage_robust, [], "Kiel")
assert ergebnis == ([], []), f"asyncio.run(frage_robust([], 'Kiel')) ergibt {ergebnis!r}, erwartet war ([], [])."

# kunden_in gibt das Ergebnis von frage_robust zurück
stelle_ein(BEISPIEL_DATEN, BEISPIEL_DAUER, {"nord"})
ergebnis = aufrufen(kunden_in, DREI, "Kiel")
if inspect.iscoroutine(ergebnis):
    ergebnis.close()
assert ergebnis == (["Cem", "Dana"], ["nord"]), (
    f"kunden_in(['nord', 'mitte', 'sued'], 'Kiel') mit Ausfall von nord ergibt {ergebnis!r}, "
    "erwartet war (['Cem', 'Dana'], ['nord']).\nTipp: return asyncio.run(frage_robust(knoten, ort))."
)

# gather wird benutzt
assert verwendet("gather"), "Ihr Code verwendet asyncio.gather nicht. Lassen Sie damit alle Abfragen gleichzeitig warten."

# Die Ausgabe des Programms
erwartet = "[['Ada'], ['Cem'], ['Dana']]\n(['Ada', 'Dana'], ['mitte'])"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Verteilungen
zufall = Zufall(5040)
orte = ["Kiel", "Bonn", "Jena"]
for _ in range(300):
    knoten = [f"k{nummer}" for nummer in range(zufall.randint(0, 6))]
    daten = {name: [(f"{name}-{i}", zufall.choice(orte)) for i in range(zufall.randint(0, 4))] for name in knoten}
    dauer = {name: zufall.randint(1, 5) for name in knoten}
    ausgefallen = {name for name in knoten if zufall.random() < 0.3}
    reihenfolge = zufall.sample(knoten, len(knoten))
    ort = zufall.choice(orte)
    stelle_ein(daten, dauer, ausgefallen)
    ergebnis = aufrufen(kunden_in, reihenfolge, ort)
    erwartet = vergleich(reihenfolge, ort, daten, ausgefallen)
    assert ergebnis == erwartet, (
        f"Mit DATEN = {daten}, DAUER = {dauer}, AUSGEFALLEN = {ausgefallen} ergibt kunden_in({reihenfolge}, {ort!r})\n"
        f"{ergebnis!r}, erwartet war {erwartet!r}."
    )
    assert gleichzeitig(), f"Bei {reihenfolge} liefen die Abfragen nicht gleichzeitig: {PROTOKOLL}"

# Obere Grenze: 1000 Knoten mit je 100 Kunden
knoten = [f"k{nummer}" for nummer in range(1000)]
daten = {name: [(f"{name}-{i}", orte[i % 3]) for i in range(100)] for name in knoten}
stelle_ein(daten, {name: 1 + nummer % 5 for nummer, name in enumerate(knoten)}, set(knoten[::7]))
ergebnis = aufrufen(kunden_in, knoten, "Jena")
assert ergebnis == vergleich(knoten, "Jena", daten, set(knoten[::7])), "Bei 1000 Knoten stimmt kunden_in nicht."
