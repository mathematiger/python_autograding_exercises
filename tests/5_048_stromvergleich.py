# Automatisch erzeugt aus lehrkraft/muster/5_048_stromvergleich.py - nicht von Hand ändern.
# vorlage-hash: 39c1113ec5fc3b34
# text-hash: 4eb68d65d614a7fa
# thema: nebenlaeufigkeit
# inhalt: Übung: asyncio und Threads

import inspect
import warnings

warnings.simplefilter("ignore", RuntimeWarning)  # vergessenes await meldet der Test selbst
BEISPIEL = {
    "Stadtwerk": {"grundpreis": 180, "arbeitspreis": 28, "co2": 380},
    "Windkraft Nord": {"grundpreis": 240, "arbeitspreis": 29, "co2": 20},
    "Sonnenstrom": {"grundpreis": 120, "arbeitspreis": 31, "co2": 40},
    "Graustrom24": ConnectionError("Wartungsarbeiten"),
    "Flussstrom": {"grundpreis": 90, "arbeitspreis": 27, "co2": 30},
}
BEISPIEL_DAUER = {"Stadtwerk": 0.02, "Windkraft Nord": 0.05, "Sonnenstrom": 0.01, "Graustrom24": 0.01, "Flussstrom": 0.2}
FUENF = list(BEISPIEL)
LANGSAM = 0.1  # deutlich über dem Zeitlimit LIMIT, aber unter 3 · LIMIT
LIMIT = 0.04


def stelle_ein(angebote, dauer=None, zeit=0.005):
    """Setzt ANGEBOTE und DAUER neu und leert LAST und AUFRUFE."""
    ANGEBOTE.clear()
    ANGEBOTE.update(angebote)
    DAUER.clear()
    for name in angebote:
        DAUER[name] = zeit
    DAUER.update(dauer or {})
    LAST.update(gleichzeitig=0, hoechstens=0)
    AUFRUFE.clear()


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def ausfuehren(funktion, *argumente):
    """Führt eine Koroutinenfunktion mit asyncio.run aus; ein Fehler wird als Text zurückgegeben."""
    return wert_von(lambda: asyncio.run(funktion(*argumente)))


def erwartete_antworten(angebote, dauer, zeitlimit):
    """Vergleichslösung: was beide Fassungen liefern sollen, ohne zu warten."""
    antworten = {}
    for name, angebot in angebote.items():
        if dauer[name] > zeitlimit:
            antworten[name] = "Zeitlimit"
        elif isinstance(angebot, Exception):
            antworten[name] = f"{type(angebot).__name__}: {angebot}"
        else:
            antworten[name] = dict(angebot)
    return antworten


def vergleich_bestes(antworten, verbrauch, co2_grenze):
    """Vergleichslösung: sortiert alle passenden Angebote nach Kosten und Stelle im Dictionary."""
    kandidaten = []
    for stelle, (name, angebot) in enumerate(antworten.items()):
        if isinstance(angebot, dict) and angebot["co2"] <= co2_grenze:
            kosten = round((100 * angebot["grundpreis"] + angebot["arbeitspreis"] * verbrauch) / 100, 2)
            kandidaten.append((kosten, stelle, name))
    if not kandidaten:
        return None
    kosten, _, name = min(kandidaten)
    return name, kosten


def mit_sammelpunkt(anzahl, aufruf):
    """Führt aufruf aus; jede blockierende Anfrage wartet dabei, bis anzahl Anfragen gleichzeitig warten.

    Gibt (Ergebnis, alle_getroffen) zurück. Kommen nicht alle innerhalb einer halben Sekunde zusammen,
    bricht der Sammelpunkt, und jede weitere Anfrage scheitert sofort, damit nichts hängen bleibt.
    """
    sammelpunkt = threading.Barrier(anzahl, timeout=0.5)
    original = angebot_blockierend

    def erst_sammeln(anbieter):
        """Wartet am Sammelpunkt und fragt dann wie gewohnt."""
        sammelpunkt.wait()
        return original(anbieter)

    globals()["angebot_blockierend"] = erst_sammeln
    try:
        ergebnis = wert_von(aufruf)
    finally:
        globals()["angebot_blockierend"] = original
    return ergebnis, not sammelpunkt.broken


def arten_der_aufrufe():
    """Die Menge der Fassungen, die seit dem letzten stelle_ein gefragt wurden."""
    return {art for art, _ in AUFRUFE}


ERWARTET = erwartete_antworten(BEISPIEL, BEISPIEL_DAUER, 0.1)

# frage_mit_zeitlimit ist eine Koroutinenfunktion
assert inspect.iscoroutinefunction(frage_mit_zeitlimit), (
    "frage_mit_zeitlimit ist keine Koroutinenfunktion. Schreiben Sie async def frage_mit_zeitlimit(...):"
)

# frage_mit_zeitlimit: ein Anbieter antwortet rechtzeitig
stelle_ein(BEISPIEL, BEISPIEL_DAUER)
ergebnis = ausfuehren(frage_mit_zeitlimit, "Sonnenstrom", 0.1)
assert ergebnis == BEISPIEL["Sonnenstrom"], (
    f"asyncio.run(frage_mit_zeitlimit('Sonnenstrom', 0.1)) ergibt {ergebnis!r}, erwartet war {BEISPIEL['Sonnenstrom']}.\n"
    "Tipp: return await asyncio.wait_for(angebot_async(anbieter), zeitlimit)."
)

# frage_mit_zeitlimit: ein anderer Anbieter (nicht fest hinschreiben!)
ergebnis = ausfuehren(frage_mit_zeitlimit, "Windkraft Nord", 0.1)
assert ergebnis == BEISPIEL["Windkraft Nord"], (
    f"asyncio.run(frage_mit_zeitlimit('Windkraft Nord', 0.1)) ergibt {ergebnis!r}, erwartet war {BEISPIEL['Windkraft Nord']}."
)

# frage_mit_zeitlimit: ein Fehler des Anbieters wird zum Text
ergebnis = ausfuehren(frage_mit_zeitlimit, "Graustrom24", 0.1)
assert ergebnis == "ConnectionError: Wartungsarbeiten", (
    f"asyncio.run(frage_mit_zeitlimit('Graustrom24', 0.1)) ergibt {ergebnis!r}, erwartet war "
    "'ConnectionError: Wartungsarbeiten'.\nTipp: except Exception as ausnahme: return als_text(ausnahme)."
)

# frage_mit_zeitlimit: zu langsam ergibt "Zeitlimit"
ergebnis = ausfuehren(frage_mit_zeitlimit, "Flussstrom", 0.05)
assert ergebnis == "Zeitlimit", (
    f"Flussstrom antwortet erst nach 0.2 s; asyncio.run(frage_mit_zeitlimit('Flussstrom', 0.05)) ergibt {ergebnis!r}, "
    "erwartet war 'Zeitlimit'.\nTipp: Fangen Sie den TimeoutError von wait_for vor dem allgemeinen except Exception ab."
)

# frage_mit_zeitlimit: andere Fehlerarten
stelle_ein({"a": ValueError("Preis fehlt"), "b": KeyError("co2")})
ergebnisse = [ausfuehren(frage_mit_zeitlimit, name, 0.1) for name in "ab"]
assert ergebnisse == ["ValueError: Preis fehlt", "KeyError: 'co2'"], (
    f"Bei einem ValueError und einem KeyError ergibt frage_mit_zeitlimit {ergebnisse!r}, "
    "erwartet war ['ValueError: Preis fehlt', \"KeyError: 'co2'\"].\nTipp: Fangen Sie jede Exception ab, nicht nur ConnectionError."
)

# hole_async: das Beispiel
stelle_ein(BEISPIEL, BEISPIEL_DAUER)
ergebnis = ausfuehren(hole_async, FUENF, 0.1)
assert ergebnis == ERWARTET, (
    f"asyncio.run(hole_async({FUENF}, 0.1)) ergibt\n{ergebnis!r}\nerwartet war\n{ERWARTET}\n"
    "Tipp: asyncio.gather über frage_mit_zeitlimit für jeden Anbieter, dann dict(zip(anbieter, antworten))."
)

# hole_async: in der Reihenfolge der Liste
assert isinstance(ergebnis, dict) and list(ergebnis) == FUENF, (
    f"Die Schlüssel von hole_async sind {list(ergebnis) if isinstance(ergebnis, dict) else ergebnis!r}, erwartet war {FUENF}."
)

# hole_async: alle Anfragen laufen gleichzeitig
assert LAST["hoechstens"] == 5, (
    f"Bei hole_async liefen höchstens {LAST['hoechstens']} von 5 Anfragen gleichzeitig, erwartet waren alle 5.\n"
    "Tipp: Mit einem await je Anbieter in einer Schleife wartet jede Anfrage auf die vorige; übergeben Sie alle an gather."
)

# hole_async: fragt die asyncio-Fassung der Schnittstelle
assert arten_der_aufrufe() == {"async"}, (
    f"hole_async hat diese Fassungen der Schnittstelle benutzt: {arten_der_aufrufe() or 'keine'}; erwartet war nur angebot_async."
)

# hole_async: andere Anbieter und Reihenfolge
angebote = {"Ost": {"grundpreis": 0, "arbeitspreis": 40, "co2": 500}, "West": OSError("kein Netz")}
stelle_ein(angebote)
ergebnis = ausfuehren(hole_async, ["West", "Ost"], 0.1)
erwartet = {"West": "OSError: kein Netz", "Ost": angebote["Ost"]}
assert ergebnis == erwartet and list(ergebnis) == ["West", "Ost"], (
    f"asyncio.run(hole_async(['West', 'Ost'], 0.1)) ergibt {ergebnis!r}, erwartet war {erwartet}."
)

# hole_async: mehrere langsame Anbieter verpassen alle das Zeitlimit
angebote = {name: {"grundpreis": 1, "arbeitspreis": 1, "co2": 1} for name in ["a", "b", "c", "d"]}
stelle_ein(angebote, {"a": LANGSAM, "b": LANGSAM, "c": LANGSAM})
ergebnis = ausfuehren(hole_async, list(angebote), LIMIT)
erwartet = {"a": "Zeitlimit", "b": "Zeitlimit", "c": "Zeitlimit", "d": angebote["d"]}
assert ergebnis == erwartet, (
    f"a, b und c antworten erst nach {LANGSAM} s, d sofort; hole_async(['a', 'b', 'c', 'd'], {LIMIT}) ergibt\n"
    f"{ergebnis!r}\nerwartet war\n{erwartet}\nTipp: Jede Anfrage bekommt ihr eigenes wait_for."
)

# hole_async: keine Anbieter
stelle_ein({})
ergebnis = ausfuehren(hole_async, [], 0.1)
assert ergebnis == {}, f"asyncio.run(hole_async([], 0.1)) ergibt {ergebnis!r}, erwartet war {{}}."

# hole_threads: das Beispiel
stelle_ein(BEISPIEL, BEISPIEL_DAUER)
aufrufer, ergebnis = threading.get_ident(), wert_von(lambda: hole_threads(FUENF, 0.1))  # in einer Anweisung, also im selben Thread
assert ergebnis == ERWARTET, (
    f"hole_threads({FUENF}, 0.1) ergibt\n{ergebnis!r}\nerwartet war\n{ERWARTET}\n"
    "Tipp: pool.submit(angebot_blockierend, name) für jeden Anbieter, dann as_completed(futures, timeout=zeitlimit)."
)

# hole_threads: in der Reihenfolge der Liste
assert isinstance(ergebnis, dict) and list(ergebnis) == FUENF, (
    f"Die Schlüssel von hole_threads sind {list(ergebnis) if isinstance(ergebnis, dict) else ergebnis!r}, erwartet war {FUENF}.\n"
    "Tipp: as_completed liefert in der Reihenfolge des Fertigwerdens; bauen Sie das Ergebnis danach in der Reihenfolge der Liste."
)

# hole_threads: fragt die blockierende Fassung aus eigenen Threads
eigene = {kennung for art, kennung in AUFRUFE if art == "blockierend"}
assert arten_der_aufrufe() == {"blockierend"} and len(AUFRUFE) == 5 and aufrufer not in eigene, (
    f"hole_threads hat die Schnittstelle so gefragt: {[art for art, _ in AUFRUFE]}"
    f"{' (auch aus dem aufrufenden Thread)' if aufrufer in eigene else ''}; erwartet war fünfmal "
    "angebot_blockierend, jedes Mal aus einem Thread des Pools.\nTipp: pool.submit(angebot_blockierend, name)."
)

# hole_threads: alle Anfragen laufen gleichzeitig
stelle_ein(BEISPIEL)
ergebnis, getroffen = mit_sammelpunkt(5, lambda: hole_threads(FUENF, 1))
assert getroffen, (
    "Bei hole_threads haben nie alle 5 Anfragen gleichzeitig gewartet.\n"
    "Tipp: Erst alle Aufrufe einreichen, dann abholen; rufen Sie result() nicht gleich nach submit auf."
)

# hole_threads: andere Anbieter und Reihenfolge
angebote = {"Ost": {"grundpreis": 0, "arbeitspreis": 40, "co2": 500}, "West": OSError("kein Netz")}
stelle_ein(angebote)
ergebnis = wert_von(lambda: hole_threads(["West", "Ost"], 0.1))
erwartet = {"West": "OSError: kein Netz", "Ost": angebote["Ost"]}
assert ergebnis == erwartet and list(ergebnis) == ["West", "Ost"], (
    f"hole_threads(['West', 'Ost'], 0.1) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: future.result() löst die Ausnahme aus dem Thread erneut aus; machen Sie mit als_text einen Text daraus."
)

# hole_threads: mehrere langsame Anbieter haben dieselbe Frist
angebote = {name: {"grundpreis": 1, "arbeitspreis": 1, "co2": 1} for name in ["a", "b", "c", "d"]}
stelle_ein(angebote, {"a": LANGSAM, "b": LANGSAM, "c": LANGSAM})
ergebnis = wert_von(lambda: hole_threads(list(angebote), LIMIT))
erwartet = {"a": "Zeitlimit", "b": "Zeitlimit", "c": "Zeitlimit", "d": angebote["d"]}
assert ergebnis == erwartet, (
    f"a, b und c antworten erst nach {LANGSAM} s, d sofort; hole_threads(['a', 'b', 'c', 'd'], {LIMIT}) ergibt\n"
    f"{ergebnis!r}\nerwartet war\n{erwartet}\n"
    "Tipp: Eine gemeinsame Frist für alle: as_completed(futures, timeout=zeitlimit). Mit result(timeout=…) je Future "
    "addieren sich die Wartezeiten."
)

# hole_threads: keine Anbieter
stelle_ein({})
ergebnis = wert_von(lambda: hole_threads([], 0.1))
assert ergebnis == {}, (
    f"hole_threads([], 0.1) ergibt {ergebnis!r}, erwartet war {{}}.\n"
    "Tipp: ThreadPoolExecutor(max_workers=0) löst einen ValueError aus; nehmen Sie mindestens einen Arbeiter."
)

# hole_threads: auch 40 Anbieter werden alle gleichzeitig gefragt
angebote = {f"A{nummer:02d}": {"grundpreis": nummer, "arbeitspreis": 30, "co2": 100} for nummer in range(40)}
stelle_ein(angebote)
ergebnis, getroffen = mit_sammelpunkt(40, lambda: hole_threads(list(angebote), 1))
assert getroffen and ergebnis == angebote, (
    f"Bei 40 Anbietern {'stimmt das Ergebnis nicht' if getroffen else 'haben nie alle 40 Anfragen gleichzeitig gewartet'}.\n"
    "Tipp: ThreadPoolExecutor(max_workers=len(anbieter)); ohne Angabe nimmt der Pool nur wenige Arbeiter."
)

# bestes_angebot: das Beispiel
ergebnis = wert_von(lambda: bestes_angebot(dict(ERWARTET), 20000, 100))
assert ergebnis == ("Windkraft Nord", 6040), (
    f"bestes_angebot(antworten, 20000, 100) ergibt {ergebnis!r}, erwartet war ('Windkraft Nord', 6040.0).\n"
    "Tipp: Kosten = grundpreis + arbeitspreis * verbrauch / 100; Stadtwerk liegt über der CO₂-Grenze."
)

# bestes_angebot: ohne strenge CO₂-Grenze gewinnt das Stadtwerk
ergebnis = wert_von(lambda: bestes_angebot(dict(ERWARTET), 20000, 1000))
assert ergebnis == ("Stadtwerk", 5780), f"bestes_angebot(antworten, 20000, 1000) ergibt {ergebnis!r}, erwartet war ('Stadtwerk', 5780.0)."

# bestes_angebot: anderer Verbrauch
ergebnis = wert_von(lambda: bestes_angebot(dict(ERWARTET), 1000, 100))
assert ergebnis == ("Sonnenstrom", 430), (
    f"bestes_angebot(antworten, 1000, 100) ergibt {ergebnis!r}, erwartet war ('Sonnenstrom', 430.0): "
    "bei wenig Verbrauch zählt der Grundpreis mehr."
)

# bestes_angebot: Kosten auf zwei Nachkommastellen gerundet
antworten = {"x": {"grundpreis": 99.99, "arbeitspreis": 27.35, "co2": 10}}
ergebnis = wert_von(lambda: bestes_angebot(antworten, 333, 50))
assert ergebnis == ("x", 191.07), (
    f"bestes_angebot({antworten}, 333, 50) ergibt {ergebnis!r}, erwartet war ('x', 191.07).\n"
    "Tipp: round(kosten, 2)."
)

# bestes_angebot: CO₂ genau an der Grenze zählt mit
antworten = {"knapp": {"grundpreis": 100, "arbeitspreis": 30, "co2": 50}, "teuer": {"grundpreis": 500, "arbeitspreis": 30, "co2": 10}}
ergebnis = wert_von(lambda: bestes_angebot(antworten, 1000, 50))
assert ergebnis == ("knapp", 400), (
    f"bestes_angebot({antworten}, 1000, 50) ergibt {ergebnis!r}, erwartet war ('knapp', 400.0): co2 ≤ co2_grenze."
)

# bestes_angebot: bei gleichen Kosten gewinnt der erste
antworten = {"erst": {"grundpreis": 200, "arbeitspreis": 30, "co2": 0}, "zweit": {"grundpreis": 100, "arbeitspreis": 40, "co2": 0}}
ergebnis = wert_von(lambda: bestes_angebot(antworten, 1000, 0))
assert ergebnis == ("erst", 500), f"bestes_angebot({antworten}, 1000, 0) ergibt {ergebnis!r}, erwartet war ('erst', 500.0)."

# bestes_angebot: Verbrauch 0, dann zählt nur der Grundpreis
ergebnis = wert_von(lambda: bestes_angebot(antworten, 0, 0))
assert ergebnis == ("zweit", 100), f"bestes_angebot({antworten}, 0, 0) ergibt {ergebnis!r}, erwartet war ('zweit', 100.0)."

# bestes_angebot: nur Fehler und Zeitlimits
antworten = {"a": "Zeitlimit", "b": "ConnectionError: weg"}
ergebnis = wert_von(lambda: bestes_angebot(antworten, 1000, 1000))
assert ergebnis is None, (
    f"bestes_angebot({antworten}, 1000, 1000) ergibt {ergebnis!r}, erwartet war None.\n"
    "Tipp: Überspringen Sie Antworten, die Texte sind."
)

# bestes_angebot: kein Angebot unter der Grenze
ergebnis = wert_von(lambda: bestes_angebot(dict(ERWARTET), 20000, 10))
assert ergebnis is None, f"bestes_angebot(antworten, 20000, 10) ergibt {ergebnis!r}, erwartet war None, denn kein Angebot hat co2 ≤ 10."

# bestes_angebot: keine Antworten
ergebnis = wert_von(lambda: bestes_angebot({}, 1000, 100))
assert ergebnis is None, f"bestes_angebot({{}}, 1000, 100) ergibt {ergebnis!r}, erwartet war None."

# Die Ausgabe des Programms
zeilen = [f"{name} {antwort}" for name, antwort in ERWARTET.items()]
erwartet = "\n".join(zeilen + ["True", "('Windkraft Nord', 6040.0)"])
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Anbieter: beide Fassungen liefern dasselbe
zufall = Zufall(5048)
fehlerarten = [ConnectionError, ValueError, OSError, KeyError, RuntimeError]
for runde in range(16):
    angebote = {}
    dauer = {}
    for nummer in zufall.sample(range(100), zufall.randint(0, 7)):
        name = f"Anbieter {nummer}"
        if zufall.random() < 0.25:
            angebote[name] = zufall.choice(fehlerarten)(f"Fehler {nummer}")
        else:
            angebote[name] = {"grundpreis": zufall.randint(0, 300), "arbeitspreis": zufall.randint(20, 45), "co2": zufall.randint(0, 600)}
        dauer[name] = LANGSAM if runde % 4 == 0 and zufall.random() < 0.3 else zufall.choice([0, 0.002])
    reihenfolge = list(angebote)
    erwartet = erwartete_antworten(angebote, dauer, LIMIT)
    stelle_ein(angebote, dauer)
    mit_async = ausfuehren(hole_async, reihenfolge, LIMIT)
    stelle_ein(angebote, dauer)
    mit_threads = wert_von(lambda: hole_threads(reihenfolge, LIMIT))
    assert mit_async == erwartet and mit_threads == erwartet, (
        f"Für ANGEBOTE = {angebote}\nund DAUER = {dauer} (Zeitlimit {LIMIT}) ergibt\n"
        f"hole_async   {mit_async!r}\nhole_threads {mit_threads!r}\nerwartet     {erwartet}"
    )
    verbrauch = zufall.randint(0, 50000)
    grenze = zufall.randint(0, 600)
    ergebnis = wert_von(lambda: bestes_angebot(dict(erwartet), verbrauch, grenze))
    assert ergebnis == vergleich_bestes(erwartet, verbrauch, grenze), (
        f"bestes_angebot({erwartet}, {verbrauch}, {grenze}) ergibt {ergebnis!r}, erwartet war {vergleich_bestes(erwartet, verbrauch, grenze)}."
    )

# Viele zufällige Antworten für bestes_angebot
for _ in range(500):
    antworten = {}
    for nummer in range(zufall.randint(0, 8)):
        if zufall.random() < 0.2:
            antworten[f"A{nummer}"] = zufall.choice(["Zeitlimit", "ConnectionError: weg"])
        else:
            antworten[f"A{nummer}"] = {
                "grundpreis": zufall.choice([zufall.randint(0, 10000), round(zufall.uniform(0, 500), 2)]),
                "arbeitspreis": zufall.choice([zufall.randint(0, 50), round(zufall.uniform(0, 50), 2)]),
                "co2": zufall.randint(0, 1000),
            }
    verbrauch = zufall.choice([0, zufall.randint(0, 1000), zufall.randint(0, 10**7)])
    grenze = zufall.randint(0, 1000)
    ergebnis = wert_von(lambda: bestes_angebot(dict(antworten), verbrauch, grenze))
    erwartet = vergleich_bestes(antworten, verbrauch, grenze)
    assert ergebnis == erwartet, f"bestes_angebot({antworten}, {verbrauch}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 100 Anbieter ohne Wartezeit, beide Fassungen
angebote = {f"A{nummer:03d}": {"grundpreis": nummer, "arbeitspreis": 25 + nummer % 7, "co2": nummer * 10} for nummer in range(100)}
for nummer in range(0, 100, 9):
    angebote[f"A{nummer:03d}"] = ConnectionError(f"Fehler {nummer}")
erwartet = erwartete_antworten(angebote, dict.fromkeys(angebote, 0), 1)
stelle_ein(angebote, zeit=0)
mit_async = ausfuehren(hole_async, list(angebote), 1)
stelle_ein(angebote, zeit=0)
mit_threads = wert_von(lambda: hole_threads(list(angebote), 1))
ergebnis = wert_von(lambda: bestes_angebot(mit_async, 10**7, 1000))
assert mit_async == erwartet and mit_threads == erwartet and ergebnis == vergleich_bestes(erwartet, 10**7, 1000), (
    "Bei 100 Anbietern stimmt "
    + ", ".join(
        teil for teil, ok in [("hole_async", mit_async == erwartet), ("hole_threads", mit_threads == erwartet),
                              ("bestes_angebot", ergebnis == vergleich_bestes(erwartet, 10**7, 1000))] if not ok
    )
    + " nicht."
)
