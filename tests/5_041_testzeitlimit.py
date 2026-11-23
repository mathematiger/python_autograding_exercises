# Automatisch erzeugt aus lehrkraft/muster/5_041_testzeitlimit.py - nicht von Hand ändern.
# vorlage-hash: f409477c8794e727
# text-hash: 0232e3817bbf61e9
# thema: nebenlaeufigkeit
# inhalt: create_task, wait_for, Abbruch

import inspect
import warnings

warnings.simplefilter("ignore", RuntimeWarning)  # vergessenes await meldet der Test selbst
DREI = ["oberflaeche", "datenbank", "schnittstellen"]


def ausfuehren(funktion, *argumente):
    """Führt eine Koroutinenfunktion mit asyncio.run aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return asyncio.run(funktion(*argumente))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def stelle_ein(haengt=(), kaputt=()):
    """Setzt HAENGT und KAPUTT neu und leert PROTOKOLL."""
    HAENGT.clear()
    HAENGT.update(haengt)
    KAPUTT.clear()
    KAPUTT.update(kaputt)
    PROTOKOLL.clear()


def gleichzeitig():
    """True, wenn im PROTOKOLL alle Sammlungen begonnen haben, bevor die erste fertig war."""
    beginne = [stelle for stelle, eintrag in enumerate(PROTOKOLL) if eintrag.startswith("beginn")]
    andere = [stelle for stelle, eintrag in enumerate(PROTOKOLL) if not eintrag.startswith("beginn")]
    return not andere or not beginne or max(beginne) < min(andere)


def erwartet_fuer(namen, haengt, kaputt):
    """Vergleichslösung: das Ergebnis jeder Sammlung aus HAENGT und KAPUTT abgelesen."""
    ergebnisse = {}
    for name in namen:
        if name in haengt:
            ergebnisse[name] = "abgebrochen"
        elif name in kaputt:
            ergebnisse[name] = "fehlgeschlagen"
        else:
            ergebnisse[name] = "bestanden"
    return ergebnisse


# mit_zeitlimit ist eine Koroutinenfunktion
assert inspect.iscoroutinefunction(mit_zeitlimit), "mit_zeitlimit ist keine Koroutinenfunktion. Schreiben Sie async def."

# mit_zeitlimit: eine Sammlung besteht
stelle_ein()
ergebnis = ausfuehren(mit_zeitlimit, "oberflaeche", 1)
assert ergebnis == "bestanden", (
    f"asyncio.run(mit_zeitlimit('oberflaeche', 1)) ergibt {ergebnis!r}, erwartet war 'bestanden'.\n"
    "Tipp: await asyncio.wait_for(testlauf(name), sekunden)."
)

# mit_zeitlimit: die Sammlung ist wirklich gelaufen
assert PROTOKOLL == ["beginn oberflaeche", "ende oberflaeche", "aufgeraeumt oberflaeche"], (
    f"Das Protokoll ist {PROTOKOLL}; erwartet war, dass testlauf('oberflaeche') einmal ganz läuft."
)

# mit_zeitlimit: ein fehlgeschlagener Test
stelle_ein(kaputt={"datenbank"})
ergebnis = ausfuehren(mit_zeitlimit, "datenbank", 1)
assert ergebnis == "fehlgeschlagen", (
    f"Mit KAPUTT = {{'datenbank'}} ergibt mit_zeitlimit('datenbank', 1) {ergebnis!r}, erwartet war 'fehlgeschlagen'.\n"
    "Tipp: wait_for gibt den AssertionError von testlauf unverändert weiter; fangen Sie ihn mit except ab."
)

# mit_zeitlimit: eine hängende Sammlung wird abgebrochen
stelle_ein(haengt={"schnittstellen"})
ergebnis = ausfuehren(mit_zeitlimit, "schnittstellen", 0.05)
assert ergebnis == "abgebrochen", (
    f"Mit HAENGT = {{'schnittstellen'}} ergibt mit_zeitlimit('schnittstellen', 0.05) {ergebnis!r}, "
    "erwartet war 'abgebrochen'.\nTipp: Bei Zeitüberschreitung löst wait_for einen TimeoutError aus."
)

# mit_zeitlimit: die abgebrochene Sammlung hat aufgeräumt
assert PROTOKOLL == ["beginn schnittstellen", "aufgeraeumt schnittstellen"], (
    f"Das Protokoll ist {PROTOKOLL}; erwartet war ['beginn schnittstellen', 'aufgeraeumt schnittstellen'].\n"
    "Tipp: wait_for bricht die Koroutine ab und wartet, bis ihr finally gelaufen ist; asyncio.sleep als "
    "eigenes Zeitlimit tut das nicht."
)

# mit_zeitlimit: eine kaputte, aber nicht hängende Sammlung ist nicht abgebrochen
stelle_ein(kaputt={"a"})
ergebnisse = [ausfuehren(mit_zeitlimit, "a", 0.05), ausfuehren(mit_zeitlimit, "b", 0.05)]
assert ergebnisse == ["fehlgeschlagen", "bestanden"], (
    f"mit_zeitlimit('a', 0.05) und mit_zeitlimit('b', 0.05) ergeben {ergebnisse!r}, erwartet war "
    "['fehlgeschlagen', 'bestanden']."
)

# alle ist eine Koroutinenfunktion
assert inspect.iscoroutinefunction(alle), "alle ist keine Koroutinenfunktion. Schreiben Sie async def alle(namen, sekunden):"

# alle: ohne Probleme
stelle_ein()
ergebnis = ausfuehren(alle, DREI, 1)
assert ergebnis == erwartet_fuer(DREI, set(), set()), (
    f"asyncio.run(alle({DREI}, 1)) ergibt {ergebnis!r}, erwartet war {erwartet_fuer(DREI, set(), set())}."
)

# alle: das Beispiel
stelle_ein(haengt={"schnittstellen"}, kaputt={"datenbank"})
ergebnis = ausfuehren(alle, DREI, 0.05)
erwartet = erwartet_fuer(DREI, {"schnittstellen"}, {"datenbank"})
assert ergebnis == erwartet, f"Im Beispiel ergibt alle {ergebnis!r}, erwartet war {erwartet}."

# alle: in der Reihenfolge der Liste
assert isinstance(ergebnis, dict) and list(ergebnis) == DREI, (
    f"Die Schlüssel des Ergebnisses sind {list(ergebnis) if isinstance(ergebnis, dict) else ergebnis!r}, "
    f"erwartet war die Reihenfolge {DREI}."
)

# alle: alle Sammlungen laufen gleichzeitig
assert gleichzeitig(), (
    f"Das Protokoll ist {PROTOKOLL}; alle Sammlungen sollten beginnen, bevor die erste fertig ist.\n"
    "Tipp: Legen Sie zuerst alle Tasks mit create_task an und warten Sie erst danach mit await auf sie."
)

# alle: auch die abgebrochene Sammlung hat aufgeräumt
assert "aufgeraeumt schnittstellen" in PROTOKOLL, (
    f"Das Protokoll ist {PROTOKOLL}; die abgebrochene Sammlung schnittstellen hat nicht aufgeräumt."
)

# alle: mehrere hängende Sammlungen warten gemeinsam
stelle_ein(haengt={"h1", "h2", "h3", "h4"})
ergebnis = ausfuehren(alle, ["h1", "ok", "h2", "h3", "h4"], 0.05)
erwartet = erwartet_fuer(["h1", "ok", "h2", "h3", "h4"], {"h1", "h2", "h3", "h4"}, set())
assert ergebnis == erwartet and gleichzeitig(), f"alle ergibt {ergebnis!r}, erwartet war {erwartet}; Protokoll: {PROTOKOLL}"

# alle: keine Sammlungen
stelle_ein()
ergebnis = ausfuehren(alle, [], 1)
assert ergebnis == {}, f"asyncio.run(alle([], 1)) ergibt {ergebnis!r}, erwartet war {{}}."

# alle benutzt create_task
assert verwendet("create_task"), "Ihr Code verwendet asyncio.create_task nicht. Starten Sie damit jede Sammlung als Task."

# Die Ausgabe des Programms
erwartet = str(erwartet_fuer(DREI, {"schnittstellen"}, {"datenbank"}))
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Läufe ohne hängende Sammlungen
zufall = Zufall(5041)
for _ in range(200):
    namen = zufall.sample([f"s{nummer}" for nummer in range(10)], zufall.randint(0, 8))
    kaputt = {name for name in namen if zufall.random() < 0.4}
    stelle_ein(kaputt=kaputt)
    ergebnis = ausfuehren(alle, namen, 5)
    erwartet = erwartet_fuer(namen, set(), kaputt)
    assert ergebnis == erwartet and gleichzeitig(), (
        f"Mit KAPUTT = {kaputt} ergibt alle({namen}, 5) {ergebnis!r}, erwartet war {erwartet}; Protokoll: {PROTOKOLL}"
    )

# Einige zufällige Läufe mit hängenden Sammlungen
for _ in range(10):
    namen = zufall.sample([f"s{nummer}" for nummer in range(10)], zufall.randint(1, 6))
    haengt = {name for name in namen if zufall.random() < 0.4}
    kaputt = {name for name in namen if zufall.random() < 0.4}
    stelle_ein(haengt, kaputt)
    ergebnis = ausfuehren(alle, namen, 0.03)
    erwartet = erwartet_fuer(namen, haengt, kaputt)
    aufgeraeumt = sorted(eintrag[len("aufgeraeumt ") :] for eintrag in PROTOKOLL if eintrag.startswith("aufgeraeumt"))
    assert ergebnis == erwartet and aufgeraeumt == sorted(namen), (
        f"Mit HAENGT = {haengt}, KAPUTT = {kaputt} ergibt alle({namen}, 0.03) {ergebnis!r}, erwartet war {erwartet}; "
        f"Protokoll: {PROTOKOLL}"
    )

# Obere Grenze: 1000 Sammlungen, davon 100 hängend
namen = [f"s{nummer}" for nummer in range(1000)]
haengt = set(namen[::10])
kaputt = set(namen[3::7])
stelle_ein(haengt, kaputt)
ergebnis = ausfuehren(alle, namen, 0.2)
assert ergebnis == erwartet_fuer(namen, haengt, kaputt) and gleichzeitig(), "Bei 1000 Sammlungen stimmt alle nicht."
