# Automatisch erzeugt aus lehrkraft/muster/5_043_luefterschaltung.py - nicht von Hand ändern.
# vorlage-hash: 80121e8fa34471ee
# text-hash: 591470760a217d11
# thema: nebenlaeufigkeit
# inhalt: async for, asynchrone Generatoren

import inspect
import warnings

warnings.simplefilter("ignore", RuntimeWarning)  # vergessenes await meldet der Test selbst
WERTE = [24.0, 27.5, 28.0, 26.0, 25.0, 24.5, 29.0]
GELESEN = []


def ausfuehren(koroutine_von, *argumente):
    """Führt eine Koroutine mit asyncio.run aus; ein Fehler wird als Text zurückgegeben."""
    PROTOKOLL.clear()
    GELESEN.clear()
    try:
        return asyncio.run(asyncio.wait_for(koroutine_von(*argumente), 1.5))
    except TimeoutError:
        return "TimeoutError: nach 1,5 Sekunden nicht fertig (liest es eine endlose Quelle ganz?)"
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


async def endlos(werte):
    """Wiederholt die Werte endlos und merkt sich in GELESEN, wie viele schon abgeholt wurden."""
    PROTOKOLL.append("verbunden")
    try:
        while True:
            for wert in werte:
                await asyncio.sleep(0)
                GELESEN.append(wert)
                yield wert
    finally:
        PROTOKOLL.append("getrennt")


async def befehle_aus(werte, ein, aus):
    """Sammelt die Befehle von schaltbefehle aus einem Sensor mit werte."""
    gesammelt = []
    async for befehl in schaltbefehle(sensor(werte), ein, aus):
        gesammelt.append(befehl)
    return gesammelt


async def erste_aus_endlos(anzahl, werte):
    """Ruft erste mit einer endlosen Quelle auf und hält fest, ob die Quelle bei der Rückkehr geschlossen ist."""
    ergebnis = await erste(endlos(werte), anzahl)
    return ergebnis, list(PROTOKOLL)


async def erste_befehle_endlos(anzahl, werte, ein, aus):
    """Holt mit erste die ersten Befehle aus schaltbefehle über einer endlosen Quelle."""
    return await erste(schaltbefehle(endlos(werte), ein, aus), anzahl)


async def drei_befehle_endlos(werte, ein, aus):
    """Holt ohne erste genau drei Befehle aus schaltbefehle über einer endlosen Quelle und schließt sie."""
    befehle = schaltbefehle(endlos(werte), ein, aus)
    gesammelt = [await anext(befehle), await anext(befehle), await anext(befehle)]
    await befehle.aclose()
    return gesammelt


def vergleich(werte, ein, aus):
    """Vergleichslösung: die Schaltbefehle mit einer gewöhnlichen Schleife."""
    befehle = []
    an = False
    for nummer, wert in enumerate(werte):
        if not an and wert >= ein:
            an = True
            befehle.append(("ein", nummer, wert))
        elif an and wert <= aus:
            an = False
            befehle.append(("aus", nummer, wert))
    return befehle


# schaltbefehle ist ein asynchroner Generator
assert inspect.isasyncgenfunction(schaltbefehle), (
    "schaltbefehle ist kein asynchroner Generator. Schreiben Sie async def mit yield darin."
)

# schaltbefehle: das Beispiel
ergebnis = ausfuehren(befehle_aus, WERTE, 28, 25)
erwartet = vergleich(WERTE, 28, 25)
assert ergebnis == erwartet, (
    f"Die Befehle von schaltbefehle(sensor({WERTE}), 28, 25) sind {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: async for wert in quelle: …, und yield (befehl, nummer, wert) bei jedem Schalten."
)

# schaltbefehle: andere Grenzen (nicht fest hinschreiben!)
ergebnis = ausfuehren(befehle_aus, WERTE, 27, 24.5)
erwartet = vergleich(WERTE, 27, 24.5)
assert ergebnis == erwartet, f"Mit ein=27 und aus=24.5 sind die Befehle {ergebnis!r}, erwartet war {erwartet}."

# schaltbefehle: genau auf den Grenzen wird geschaltet
werte = [30, 30, 20, 20, 30]
ergebnis = ausfuehren(befehle_aus, werte, 30, 20)
assert ergebnis == [("ein", 0, 30), ("aus", 2, 20), ("ein", 4, 30)], (
    f"Für {werte} mit ein=30 und aus=20 sind die Befehle {ergebnis!r}, erwartet war "
    "[('ein', 0, 30), ('aus', 2, 20), ('ein', 4, 30)].\nTipp: „mindestens ein“ ist >=, „höchstens aus“ ist <=."
)

# schaltbefehle: kein zweites Einschalten, solange der Lüfter läuft
werte = [29, 31, 26, 33, 24, 23]
ergebnis = ausfuehren(befehle_aus, werte, 28, 25)
assert ergebnis == [("ein", 0, 29), ("aus", 4, 24)], (
    f"Für {werte} mit ein=28 und aus=25 sind die Befehle {ergebnis!r}, erwartet war [('ein', 0, 29), ('aus', 4, 24)].\n"
    "Tipp: Merken Sie sich, ob der Lüfter an ist; ein Befehl kommt nur, wenn sich das ändert."
)

# schaltbefehle: am Anfang aus, ein kühler Wert schaltet nichts
ergebnis = ausfuehren(befehle_aus, [10, 12], 28, 25)
assert ergebnis == [], f"Für [10, 12] mit ein=28 und aus=25 sind die Befehle {ergebnis!r}, erwartet war []."

# schaltbefehle: keine Werte
ergebnis = ausfuehren(befehle_aus, [], 28, 25)
assert ergebnis == [], f"Ohne Werte sind die Befehle {ergebnis!r}, erwartet war []."

# erste: die ersten Werte des Sensors
ergebnis = ausfuehren(erste, sensor(WERTE), 3)
assert ergebnis == [24.0, 27.5, 28.0], (
    f"erste(sensor(werte), 3) ergibt {ergebnis!r}, erwartet war [24.0, 27.5, 28.0].\n"
    "Tipp: async for mit break, sobald anzahl Elemente gesammelt sind."
)

# erste: mehr verlangt, als es gibt
ergebnis = ausfuehren(erste, sensor([1, 2]), 5)
assert ergebnis == [1, 2], f"erste(sensor([1, 2]), 5) ergibt {ergebnis!r}, erwartet war [1, 2]."

# erste: anzahl 0
ergebnis = ausfuehren(erste, sensor(WERTE), 0)
assert ergebnis == [], f"erste(sensor(werte), 0) ergibt {ergebnis!r}, erwartet war []."

# erste: hört bei einer endlosen Quelle auf
ergebnis = ausfuehren(erste_aus_endlos, 4, [1, 2, 3])
werte = ergebnis[0] if isinstance(ergebnis, tuple) else ergebnis
assert werte == [1, 2, 3, 1], (
    f"erste(endlose Quelle 1, 2, 3, 1, 2, …, 4) ergibt {werte!r}, erwartet war [1, 2, 3, 1].\n"
    "Tipp: Mit einer asynchronen Comprehension über eine endlose Quelle kommt man nie an; brechen Sie ab."
)

# erste: liest nicht mehr als nötig
assert GELESEN == [1, 2, 3, 1], f"erste(…, 4) hat {len(GELESEN)} Werte aus der Quelle geholt, erwartet waren 4."

# erste: die Quelle ist geschlossen, bevor erste zurückkehrt
protokoll = ergebnis[1] if isinstance(ergebnis, tuple) else []
assert protokoll == ["verbunden", "getrennt"], (
    f"Als erste zurückkehrte, stand im PROTOKOLL {protokoll}; erwartet war ['verbunden', 'getrennt'].\n"
    "Tipp: Nach break ist ein asynchroner Generator noch offen; async with aclosing(quelle) oder "
    "await quelle.aclose() schließt ihn."
)

# erste: auch Schaltbefehle aus einer endlosen Quelle
ergebnis = ausfuehren(erste_befehle_endlos, 3, [20, 30, 22], 28, 25)
assert ergebnis == [("ein", 1, 30), ("aus", 2, 22), ("ein", 4, 30)], (
    f"Die ersten drei Befehle aus einer endlosen Quelle 20, 30, 22, 20, 30, … sind {ergebnis!r}, "
    "erwartet war [('ein', 1, 30), ('aus', 2, 22), ('ein', 4, 30)]."
)

# schaltbefehle: liest nur so viele Werte, wie es braucht
ergebnis = ausfuehren(drei_befehle_endlos, [20, 30, 22], 28, 25)
assert GELESEN == [20, 30, 22, 20, 30], (
    f"Für drei Befehle hat schaltbefehle {len(GELESEN)} Werte geholt, erwartet waren 5.\n"
    "Tipp: Liefern Sie jeden Befehl sofort mit yield, statt erst alle Werte zu sammeln."
)

# schaltplan: das Beispiel
ergebnis = ausfuehren(schaltplan, WERTE, 28, 25)
assert ergebnis == vergleich(WERTE, 28, 25), (
    f"schaltplan(werte, 28, 25) ergibt {ergebnis!r}, erwartet war {vergleich(WERTE, 28, 25)}."
)

# schaltplan: der Sensor wurde benutzt und am Ende getrennt
assert PROTOKOLL == ["verbunden", "getrennt"], (
    f"Nach schaltplan steht im PROTOKOLL {PROTOKOLL}; erwartet war ['verbunden', 'getrennt'].\n"
    "Tipp: schaltbefehle(sensor(werte), ein, aus)."
)

# Die Ausgabe des Programms
erwartet = f"{vergleich(WERTE, 28, 25)}\n{WERTE[:3]}"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Messreihen
zufall = Zufall(5043)
for _ in range(300):
    werte = [zufall.randint(-50, 150) / zufall.choice([1, 2]) for _ in range(zufall.randint(0, 12))]
    aus = zufall.randint(-50, 140)
    ein = zufall.randint(aus + 1, 150)
    ergebnis = ausfuehren(schaltplan, werte, ein, aus)
    assert ergebnis == vergleich(werte, ein, aus), (
        f"schaltplan({werte}, {ein}, {aus}) ergibt {ergebnis!r}, erwartet war {vergleich(werte, ein, aus)}."
    )
    anzahl = zufall.randint(0, 14)
    ergebnis = ausfuehren(erste, sensor(werte), anzahl)
    assert ergebnis == werte[:anzahl], f"erste(sensor({werte}), {anzahl}) ergibt {ergebnis!r}, erwartet war {werte[:anzahl]}."

# Obere Grenze: 10 000 Messwerte
werte = [zufall.randint(-50, 150) for _ in range(10000)]
ergebnis = ausfuehren(schaltplan, werte, 60, 40)
assert ergebnis == vergleich(werte, 60, 40), "Bei 10 000 Messwerten stimmt schaltplan nicht."

# Obere Grenze: erste mit 10 000 Messwerten
ergebnis = ausfuehren(erste, sensor(werte), 10000)
assert ergebnis == werte, "Bei 10 000 Messwerten stimmt erste nicht."
