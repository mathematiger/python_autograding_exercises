# Automatisch erzeugt aus lehrkraft/muster/5_046_ferndiagnose.py - nicht von Hand ändern.
# vorlage-hash: 895ba9ef0e4fee90
# text-hash: ccac1a9f4b51cc42
# thema: nebenlaeufigkeit
# inhalt: submit, Future, as_completed

from concurrent.futures import Future

BEISPIEL_ZEITEN = {"PC-01": 0.3, "PC-02": 0.1, "PC-03": 0.2}
BEISPIEL = {
    "PC-01": {"cpu": 97, "ram_frei_mb": 210},
    "PC-02": {"cpu": 12, "ram_frei_mb": 5400},
    "PC-03": ConnectionError("keine Antwort"),
}
DREI = ["PC-01", "PC-02", "PC-03"]


def stelle_ein(diagnosen, zeiten=None, zeit=0.02):
    """Setzt DIAGNOSEN und ANTWORTZEIT neu und leert PROTOKOLL und den Lastzähler."""
    DIAGNOSEN.clear()
    DIAGNOSEN.update(diagnosen)
    ANTWORTZEIT.clear()
    for name in diagnosen:
        ANTWORTZEIT[name] = zeit
    ANTWORTZEIT.update(zeiten or {})
    PROTOKOLL.clear()
    LAST.update(gleichzeitig=0, hoechstens=0)


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich(diagnosen, rechner):
    """Vergleichslösung: was diagnose liefern soll, ohne Threads."""
    berichte = {}
    fehler = {}
    for name in sorted(rechner):
        antwort = diagnosen[name]
        if isinstance(antwort, Exception):
            fehler[name] = f"{type(antwort).__name__}: {antwort}"
        else:
            berichte[name] = dict(antwort)
    return berichte, fehler


def zeile_passt(zeile, erwartet):
    """Vergleicht eine Meldung locker, nur der Name des Rechners vorn muss genau stimmen."""
    return isinstance(zeile, str) and zeile.split(":")[0] == erwartet.split(":")[0] and vergleichbar(zeile) == vergleichbar(erwartet)


# starte_abfragen: ein Future je Rechner
stelle_ein(BEISPIEL)
with ThreadPoolExecutor(max_workers=3) as pool:
    abfragen = wert_von(lambda: starte_abfragen(pool, DREI))
    if isinstance(abfragen, dict):
        for future in abfragen:
            if isinstance(future, Future):
                future.exception()
art = sorted({type(schluessel).__name__ for schluessel in abfragen}) if isinstance(abfragen, dict) else abfragen
assert isinstance(abfragen, dict) and len(abfragen) == 3 and art == ["Future"], (
    f"starte_abfragen(pool, {DREI}) ergibt {abfragen!r}; erwartet war ein Dictionary mit drei Futures als Schlüsseln.\n"
    "Tipp: abfragen[pool.submit(hole_diagnose, name)] = name."
)

# starte_abfragen: jedes Future gehört zu seinem Rechner
zuordnung = {name: future.result() if future.exception() is None else repr(future.exception()) for future, name in abfragen.items()}
assert zuordnung == {
    "PC-01": BEISPIEL["PC-01"], "PC-02": BEISPIEL["PC-02"], "PC-03": repr(BEISPIEL["PC-03"])
}, f"Die Futures liefern {zuordnung}; erwartet war zu jedem Rechner seine eigene Diagnose."

# starte_abfragen: alle Abfragen laufen gleichzeitig
stelle_ein(BEISPIEL, zeit=0.15)
with ThreadPoolExecutor(max_workers=3) as pool:
    beginn = time.perf_counter()
    wert_von(lambda: starte_abfragen(pool, DREI))
    dauer = time.perf_counter() - beginn
assert dauer < 0.1 and LAST["hoechstens"] == 3, (
    f"starte_abfragen hat {dauer:.2f} s gebraucht, höchstens {LAST['hoechstens']} Abfragen liefen gleichzeitig; "
    "erwartet war, dass es sofort zurückkehrt und alle drei gleichzeitig laufen.\n"
    "Tipp: pool.submit kehrt sofort zurück; rufen Sie in starte_abfragen nicht result() auf."
)

# sammle: das Beispiel
stelle_ein(BEISPIEL, BEISPIEL_ZEITEN)
with ThreadPoolExecutor(max_workers=3) as pool:
    abfragen = {pool.submit(hole_diagnose, name): name for name in DREI}
    ergebnis = wert_von(lambda: sammle(abfragen))
erwartet = vergleich(BEISPIEL, DREI)
assert ergebnis == erwartet, (
    f"sammle ergibt\n{ergebnis!r}\nerwartet war\n{erwartet}\n"
    "Tipp: future.result() löst die Ausnahme aus dem Thread erneut aus; fangen Sie sie mit try/except ab."
)

# sammle: meldet in der Reihenfolge, in der die Ergebnisse fertig werden
erwartet = ["PC-02: ok", "PC-03: ConnectionError: keine Antwort", "PC-01: ok"]
assert len(PROTOKOLL) == 3 and all(zeile_passt(zeile, soll) for zeile, soll in zip(PROTOKOLL, erwartet)), (
    f"sammle meldet {PROTOKOLL}; erwartet war {erwartet}: PC-02 antwortet nach 0.1 s, PC-03 nach 0.2 s, PC-01 nach 0.3 s.\n"
    "Tipp: for future in as_completed(abfragen): liefert die Futures, sobald sie fertig sind."
)

# sammle: die Meldung bei einem Fehler nennt die Ausnahme
assert len(PROTOKOLL) == 3 and PROTOKOLL[1] == "PC-03: ConnectionError: keine Antwort", (
    f"Die Meldung für PC-03 ist {PROTOKOLL[1] if len(PROTOKOLL) > 1 else PROTOKOLL!r}, "
    "erwartet war 'PC-03: ConnectionError: keine Antwort'.\nTipp: f\"{name}: {type(fehler).__name__}: {fehler}\"."
)

# sammle: berichte und fehler nach den Namen sortiert
ergebnis_ok = isinstance(ergebnis, tuple) and len(ergebnis) == 2 and all(isinstance(teil, dict) for teil in ergebnis)
assert ergebnis_ok and list(ergebnis[0]) == ["PC-01", "PC-02"], (
    f"Die Schlüssel von berichte sind {list(ergebnis[0]) if ergebnis_ok else ergebnis!r}, erwartet war ['PC-01', 'PC-02'].\n"
    "Tipp: dict(sorted(berichte.items()))."
)

# sammle: auch unerwartete Ausnahmen werden einzeln abgefangen
diagnosen = {"a": {"cpu": 1}, "b": ValueError("kaputte Antwort"), "c": TimeoutError("zu langsam"), "d": {"cpu": 2}}
stelle_ein(diagnosen)
with ThreadPoolExecutor(max_workers=4) as pool:
    abfragen = {pool.submit(hole_diagnose, name): name for name in diagnosen}
    ergebnis = wert_von(lambda: sammle(abfragen))
assert ergebnis == vergleich(diagnosen, list(diagnosen)), (
    f"Mit einem ValueError und einem TimeoutError ergibt sammle\n{ergebnis!r}\nerwartet war\n{vergleich(diagnosen, list(diagnosen))}\n"
    "Tipp: except Exception fängt jede Art von Fehler; ein Fehler darf die übrigen Rechner nicht verhindern."
)

# sammle: alle Rechner melden einen Fehler
diagnosen = {"x": OSError("Netz weg"), "y": ConnectionRefusedError("abgelehnt")}
stelle_ein(diagnosen)
with ThreadPoolExecutor(max_workers=2) as pool:
    abfragen = {pool.submit(hole_diagnose, name): name for name in diagnosen}
    ergebnis = wert_von(lambda: sammle(abfragen))
assert ergebnis == ({}, {"x": "OSError: Netz weg", "y": "ConnectionRefusedError: abgelehnt"}), (
    f"sammle ergibt {ergebnis!r}, erwartet war ({{}}, {{'x': 'OSError: Netz weg', 'y': 'ConnectionRefusedError: abgelehnt'}})."
)

# sammle: keine Abfragen
PROTOKOLL.clear()
ergebnis = wert_von(lambda: sammle({}))
assert ergebnis == ({}, {}) and PROTOKOLL == [], f"sammle({{}}) ergibt {ergebnis!r} und meldet {PROTOKOLL}; erwartet war ({{}}, {{}}) ohne Meldung."

# diagnose: das Beispiel
stelle_ein(BEISPIEL, BEISPIEL_ZEITEN)
ergebnis = wert_von(lambda: diagnose(list(DREI), 3))
assert ergebnis == vergleich(BEISPIEL, DREI), f"diagnose({DREI}, 3) ergibt\n{ergebnis!r}\nerwartet war\n{vergleich(BEISPIEL, DREI)}"

# diagnose: höchstens threads Abfragen gleichzeitig
diagnosen = {f"PC-{nummer:02d}": {"cpu": nummer} for nummer in range(6)}
stelle_ein(diagnosen, zeit=0.05)
ergebnis = wert_von(lambda: diagnose(list(diagnosen), 2))
assert ergebnis == vergleich(diagnosen, list(diagnosen)) and LAST["hoechstens"] == 2, (
    f"diagnose mit 6 Rechnern und threads = 2 ergibt {ergebnis!r}; gleichzeitig liefen höchstens {LAST['hoechstens']} "
    "Abfragen, erwartet waren 2.\nTipp: ThreadPoolExecutor(max_workers=threads)."
)

# diagnose: alle gleichzeitig, wenn genug Arbeiter da sind
stelle_ein(diagnosen, zeit=0.05)
wert_von(lambda: diagnose(list(diagnosen), 16))
assert LAST["hoechstens"] == 6, f"Mit 16 Arbeitern liefen höchstens {LAST['hoechstens']} von 6 Abfragen gleichzeitig, erwartet war 6."

# diagnose: keine Rechner
stelle_ein({})
ergebnis = wert_von(lambda: diagnose([], 4))
assert ergebnis == ({}, {}), f"diagnose([], 4) ergibt {ergebnis!r}, erwartet war ({{}}, {{}})."

# Die Ausgabe des Programms
erwartet = (
    "({'PC-01': {'cpu': 97, 'ram_frei_mb': 210}, 'PC-02': {'cpu': 12, 'ram_frei_mb': 5400}}, "
    "{'PC-03': 'ConnectionError: keine Antwort'})\n"
    "['PC-02: ok', 'PC-03: ConnectionError: keine Antwort', 'PC-01: ok']"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Büros
zufall = Zufall(5046)
fehlerarten = [ConnectionError, TimeoutError, ValueError, OSError, KeyError]
for _ in range(20):
    diagnosen = {}
    for nummer in zufall.sample(range(100), zufall.randint(0, 8)):
        if zufall.random() < 0.3:
            diagnosen[f"PC-{nummer:02d}"] = zufall.choice(fehlerarten)(f"Fehler {nummer}")
        else:
            diagnosen[f"PC-{nummer:02d}"] = {"cpu": zufall.randint(0, 100)}
    stelle_ein(diagnosen, zeit=0.005)
    ergebnis = wert_von(lambda: diagnose(list(diagnosen), zufall.randint(1, 16)))
    assert ergebnis == vergleich(diagnosen, list(diagnosen)), (
        f"diagnose für {diagnosen}\nergibt   {ergebnis!r}\nerwartet {vergleich(diagnosen, list(diagnosen))}"
    )
    assert sorted(zeile.split(":")[0] for zeile in PROTOKOLL) == sorted(diagnosen), (
        f"Für {sorted(diagnosen)} meldet sammle {PROTOKOLL}; erwartet war genau eine Meldung je Rechner."
    )

# Obere Grenze: 50 Rechner, 16 Arbeiter, je 0.1 Sekunden
diagnosen = {f"PC-{nummer:02d}": {"cpu": nummer} if nummer % 5 else TimeoutError("still") for nummer in range(50)}
stelle_ein(diagnosen, zeit=0.1)
beginn = time.perf_counter()
ergebnis = wert_von(lambda: diagnose(list(diagnosen), 16))
dauer = time.perf_counter() - beginn
assert ergebnis == vergleich(diagnosen, list(diagnosen)) and dauer < 0.8, (
    f"diagnose für 50 Rechner mit 16 Arbeitern dauert {dauer:.2f} s (erwartet etwa 0.4 s) und ergibt "
    f"{len(ergebnis[0]) if isinstance(ergebnis, tuple) else ergebnis!r} Berichte."
)
