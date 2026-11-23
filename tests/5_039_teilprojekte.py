# Automatisch erzeugt aus lehrkraft/muster/5_039_teilprojekte.py - nicht von Hand ändern.
# vorlage-hash: 67fe762ed12e8324
# text-hash: 32a35306febdb2f2
# thema: nebenlaeufigkeit
# inhalt: async def, await, asyncio.run

import inspect
import warnings

warnings.simplefilter("ignore", RuntimeWarning)  # vergessenes await meldet der Test selbst
BEISPIEL = {"Webshop": 100, "Lager": 80, "Zahlung": 35, "App": 0}


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


def hinweis_await(ergebnis):
    """Gibt einen Tipp, wenn im Ergebnis Koroutinen-Objekte statt Zahlen stecken."""
    werte = ergebnis.values() if isinstance(ergebnis, dict) else [ergebnis]
    if any(inspect.iscoroutine(wert) for wert in werte):
        return "\nTipp: Im Ergebnis stecken Koroutinen-Objekte; schreiben Sie await vor hole_stand(...)."
    if isinstance(ergebnis, str) and "running event loop" in ergebnis:
        return "\nTipp: In einer Koroutine heißt es await, nicht asyncio.run."
    return ""


def setze_staende(staende):
    """Ersetzt den Inhalt von STAENDE und leert PROTOKOLL."""
    STAENDE.clear()
    STAENDE.update(staende)
    PROTOKOLL.clear()


# fortschritt ist eine Koroutinenfunktion
assert inspect.iscoroutinefunction(fortschritt), (
    "fortschritt ist keine Koroutinenfunktion. Schreiben Sie async def fortschritt(teilprojekte):"
)

# fortschritt: ein Teilprojekt
setze_staende(BEISPIEL)
ergebnis = ausfuehren(fortschritt, ["Lager"])
assert ergebnis == {"Lager": 80}, (
    f"asyncio.run(fortschritt(['Lager'])) ergibt {ergebnis!r}, erwartet war {{'Lager': 80}}.{hinweis_await(ergebnis)}"
)

# fortschritt: das Beispiel
setze_staende(BEISPIEL)
ergebnis = ausfuehren(fortschritt, ["Lager", "Webshop"])
assert ergebnis == {"Lager": 80, "Webshop": 100}, (
    f"asyncio.run(fortschritt(['Lager', 'Webshop'])) ergibt {ergebnis!r}, erwartet war {{'Lager': 80, 'Webshop': 100}}."
    + hinweis_await(ergebnis)
)

# fortschritt: andere Stände (nicht fest hinschreiben!)
setze_staende({"Lager": 10, "Webshop": 55, "Druck": 100})
ergebnis = ausfuehren(fortschritt, ["Druck", "Webshop", "Lager"])
assert ergebnis == {"Druck": 100, "Webshop": 55, "Lager": 10}, (
    f"Mit STAENDE = {{'Lager': 10, 'Webshop': 55, 'Druck': 100}} ergibt fortschritt(['Druck', 'Webshop', 'Lager']) "
    f"{ergebnis!r}.\nTipp: Lesen Sie die Stände mit hole_stand, nicht aus einer festen Tabelle."
)

# fortschritt: nacheinander, jede Frage erst nach der vorigen Antwort
setze_staende(BEISPIEL)
ausfuehren(fortschritt, ["Webshop", "Lager", "App"])
erwartet = ["frage Webshop", "antwort Webshop", "frage Lager", "antwort Lager", "frage App", "antwort App"]
assert PROTOKOLL == erwartet, (
    f"Das Protokoll ist {PROTOKOLL}, erwartet war {erwartet}.\n"
    "Tipp: Warten Sie in einer Schleife mit await auf jede Abfrage, bevor Sie die nächste beginnen."
)

# fortschritt: keine Teilprojekte
setze_staende(BEISPIEL)
ergebnis = ausfuehren(fortschritt, [])
assert ergebnis == {} and PROTOKOLL == [], f"asyncio.run(fortschritt([])) ergibt {ergebnis!r}, erwartet war {{}}."

# offene ist eine Koroutinenfunktion
assert inspect.iscoroutinefunction(offene), "offene ist keine Koroutinenfunktion. Schreiben Sie async def offene(teilprojekte):"

# offene: das Beispiel
setze_staende(BEISPIEL)
ergebnis = ausfuehren(offene, ["Webshop", "Lager", "Zahlung", "App"])
assert ergebnis == ["Lager", "Zahlung", "App"], (
    f"asyncio.run(offene([...])) ergibt {ergebnis!r}, erwartet war ['Lager', 'Zahlung', 'App'].{hinweis_await(ergebnis)}"
)

# offene: genau 99 und 100 Prozent
setze_staende({"A": 99, "B": 100})
ergebnis = ausfuehren(offene, ["B", "A"])
assert ergebnis == ["A"], (
    f"Mit den Ständen A: 99 und B: 100 ergibt offene(['B', 'A']) {ergebnis!r}, erwartet war ['A'].\n"
    "Tipp: Offen ist, was unter 100 steht (< 100)."
)

# offene: alles fertig
setze_staende({"A": 100, "B": 100})
ergebnis = ausfuehren(offene, ["A", "B"])
assert ergebnis == [], f"Wenn alles auf 100 steht, ergibt offene(['A', 'B']) {ergebnis!r}, erwartet war []."

# offene fragt über fortschritt ab, jedes Teilprojekt einmal
setze_staende(BEISPIEL)
ausfuehren(offene, ["Lager", "App"])
assert PROTOKOLL == ["frage Lager", "antwort Lager", "frage App", "antwort App"], (
    f"Bei offene(['Lager', 'App']) ist das Protokoll {PROTOKOLL}; jedes Teilprojekt soll genau einmal abgefragt werden."
)

# morgenbericht ist eine gewöhnliche Funktion
assert not inspect.iscoroutinefunction(morgenbericht), (
    "morgenbericht ist mit async def geschrieben. Es soll eine gewöhnliche Funktion sein, die asyncio.run aufruft."
)

# morgenbericht: das Beispiel
setze_staende(BEISPIEL)
ergebnis = aufrufen(morgenbericht, ["Webshop", "Lager", "Zahlung", "App"])
if inspect.iscoroutine(ergebnis):
    ergebnis.close()
    hinweis = "\nTipp: Geben Sie asyncio.run(offene(teilprojekte)) zurück, nicht offene(teilprojekte) selbst."
else:
    hinweis = ""
assert ergebnis == ["Lager", "Zahlung", "App"], (
    f"morgenbericht([...]) ergibt {ergebnis!r}, erwartet war ['Lager', 'Zahlung', 'App'].{hinweis}"
)

# morgenbericht: zweimal hintereinander
setze_staende({"X": 5, "Y": 100})
ergebnisse = [aufrufen(morgenbericht, ["X", "Y"]), aufrufen(morgenbericht, ["Y"])]
assert ergebnisse == [["X"], []], f"Zwei Aufrufe von morgenbericht ergeben {ergebnisse!r}, erwartet war [['X'], []]."

# morgenbericht benutzt asyncio.run
assert verwendet("run"), "Ihr Code verwendet asyncio.run nicht. Führen Sie offene damit in morgenbericht aus."

# Die Ausgabe des Programms
erwartet = "['Lager', 'Zahlung', 'App']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Projekte
zufall = Zufall(5039)
for _ in range(200):
    namen = [f"T{nummer}" for nummer in range(zufall.randint(0, 8))]
    staende = {name: zufall.choice([0, 50, 99, 100, zufall.randint(0, 100)]) for name in namen}
    reihenfolge = zufall.sample(namen, len(namen))
    setze_staende(staende)
    ergebnis = aufrufen(morgenbericht, reihenfolge)
    erwartet = [name for name in reihenfolge if staende[name] < 100]
    assert ergebnis == erwartet, f"Mit STAENDE = {staende} ergibt morgenbericht({reihenfolge}) {ergebnis!r}, erwartet war {erwartet}."
    fragen = [eintrag for eintrag in PROTOKOLL if eintrag.startswith("frage")]
    assert fragen == [f"frage {name}" for name in reihenfolge], f"Bei {reihenfolge} wurde so abgefragt: {PROTOKOLL}"

# Obere Grenze: 1000 Teilprojekte
namen = [f"T{nummer}" for nummer in range(1000)]
setze_staende({name: nummer % 101 for nummer, name in enumerate(namen)})
ergebnis = aufrufen(morgenbericht, namen)
assert ergebnis == [name for nummer, name in enumerate(namen) if nummer % 101 < 100], (
    "Bei 1000 Teilprojekten stimmt morgenbericht nicht."
)
