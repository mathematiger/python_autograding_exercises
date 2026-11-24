# Automatisch erzeugt aus lehrkraft/muster/4_081_schaltregeln.py - nicht von Hand ändern.
# vorlage-hash: 7b4fb9a118c692f0
# text-hash: 08c63ee6203229e8
# thema: funktionen
# inhalt: späte Bindung in Closures

def neue_grenzen():
    """Baut jedes Mal ein frisches Dictionary wie im Aufgabentext."""
    return {"luefter_serverraum": 27.0, "luefter_lager": 30.0, "luefter_buero": 24.5}


def rufe(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def regeln_von(baue, grenzen):
    """Ruft baue(grenzen) auf; liefert (Regeln, Meldung oder None)."""
    ergebnis, fehler = rufe(baue, grenzen)
    aufruf = f"{baue.__name__}({grenzen!r})" if len(grenzen) <= 4 else f"{baue.__name__}(<{len(grenzen)} Aktoren>)"
    if fehler is not None:
        return None, f"{aufruf} löst {fehler} aus."
    if not isinstance(ergebnis, dict):
        return None, f"{aufruf} ergibt {ergebnis!r}, erwartet war ein Dictionary aktor → Schaltregel."
    if set(ergebnis) != set(grenzen):
        return None, f"{aufruf} hat die Schlüssel {sorted(ergebnis)}, erwartet waren {sorted(grenzen)}."
    return ergebnis, None


def schaltet(regeln, aktor, temperatur):
    """Ruft die Regel eines Aktors auf; ein Fehler wird als Text zurückgegeben."""
    ergebnis, fehler = rufe(regeln[aktor], temperatur)
    return ergebnis if fehler is None else fehler


TIPP_SPAET = (
    "\nTipp: Eine Regel aus einer Comprehension oder Schleife sieht den letzten Wert der Schleifenvariablen. "
    "Bauen Sie jede Regel in einer eigenen Fabrikfunktion, die den Wert als Parameter bekommt."
)

# schaltregeln: ein Dictionary mit einer Regel je Aktor
regeln, meldung = regeln_von(schaltregeln, neue_grenzen())
assert meldung is None and all(callable(regel) for regel in regeln.values()), meldung or (
    f"schaltregeln(grenzen) ergibt {regeln!r}; jeder Wert soll eine Funktion sein, die man mit der Temperatur aufruft."
)

# schaltregeln: das Beispiel, Lager bei 28 Grad ist aus
regeln, meldung = regeln_von(schaltregeln, neue_grenzen())
ergebnis = meldung or schaltet(regeln, "luefter_lager", 28.0)
assert ergebnis is False, (
    meldung
    or f'schaltregeln(grenzen)["luefter_lager"](28.0) ergibt {ergebnis!r}, erwartet war False (Grenze 30.0).'
    + (TIPP_SPAET if ergebnis is True else "")
)

# schaltregeln: das Beispiel, Büro bei 28 Grad ist an
regeln, meldung = regeln_von(schaltregeln, neue_grenzen())
ergebnis = meldung or schaltet(regeln, "luefter_buero", 28.0)
assert ergebnis is True, (
    meldung or f'schaltregeln(grenzen)["luefter_buero"](28.0) ergibt {ergebnis!r}, erwartet war True (Grenze 24.5).'
)

# schaltregeln: jede Regel hat die Grenze ihres eigenen Aktors
regeln, meldung = regeln_von(schaltregeln, neue_grenzen())
ergebnisse = None if meldung else {aktor: schaltet(regeln, aktor, 27.5) for aktor in neue_grenzen()}
erwartet = {"luefter_serverraum": True, "luefter_lager": False, "luefter_buero": True}
assert ergebnisse == erwartet, meldung or (
    f"Bei 27.5 Grad ergeben die Regeln {ergebnisse!r}, erwartet war {erwartet!r}." + TIPP_SPAET
)

# schaltregeln: die Temperatur genau auf der Grenze schaltet aus
regeln, meldung = regeln_von(schaltregeln, neue_grenzen())
ergebnis = meldung or schaltet(regeln, "luefter_buero", 24.5)
assert ergebnis is False, (
    meldung
    or f'schaltregeln(grenzen)["luefter_buero"](24.5) ergibt {ergebnis!r}, erwartet war False: Nur über der '
    "Grenze wird eingeschaltet (>, nicht >=)."
)

# schaltregeln: andere Grenzen (nicht fest hinschreiben!)
grenzen = {"pumpe_kuehlung": -5, "luefter_halle": 110.5}
regeln, meldung = regeln_von(schaltregeln, grenzen)
ergebnisse = None if meldung else [schaltet(regeln, "pumpe_kuehlung", -4), schaltet(regeln, "luefter_halle", 110)]
assert ergebnisse == [True, False], meldung or (
    f"Für {grenzen!r} ergeben pumpe_kuehlung(-4) und luefter_halle(110) {ergebnisse!r}, erwartet war [True, False]."
)

# schaltregeln: eine spätere Änderung der Grenzen ändert die Regeln nicht
grenzen = neue_grenzen()
regeln, meldung = regeln_von(schaltregeln, grenzen)
grenzen["luefter_lager"] = 25.0
ergebnis = meldung or schaltet(regeln, "luefter_lager", 28.0)
assert ergebnis is False, meldung or (
    f'Nach grenzen["luefter_lager"] = 25.0 ergibt die alte Regel für 28.0 {ergebnis!r}, erwartet war False: Die '
    "Regeln behalten die Grenze vom Bauen.\nTipp: Lesen Sie grenzen[aktor] nicht erst in der Regel, sondern "
    "übergeben Sie den Wert beim Bauen an eine Fabrikfunktion."
)

# schaltregeln: die Regeln arbeiten auch, wenn grenzen danach geleert wird
grenzen = neue_grenzen()
regeln, meldung = regeln_von(schaltregeln, grenzen)
grenzen.clear()
ergebnis = meldung or schaltet(regeln, "luefter_buero", 25.0)
assert ergebnis is True, meldung or (
    f'Nach grenzen.clear() ergibt die Regel für luefter_buero bei 25.0 {ergebnis!r}, erwartet war True.'
)

# schaltregeln: keine Aktoren
regeln, meldung = regeln_von(schaltregeln, {})
assert meldung is None and regeln == {}, meldung or f"schaltregeln({{}}) ergibt {regeln!r}, erwartet war {{}}."

# live_regeln: das Beispiel, mit der Grenze beim Bauen
regeln, meldung = regeln_von(live_regeln, neue_grenzen())
ergebnisse = None if meldung else [schaltet(regeln, "luefter_lager", 28.0), schaltet(regeln, "luefter_buero", 28.0)]
assert ergebnisse == [False, True], meldung or (
    f"live_regeln(grenzen) ergibt für luefter_lager und luefter_buero bei 28.0 {ergebnisse!r}, erwartet war "
    "[False, True]."
)

# live_regeln: jede Regel gehört zu ihrem eigenen Aktor
regeln, meldung = regeln_von(live_regeln, neue_grenzen())
ergebnisse = None if meldung else {aktor: schaltet(regeln, aktor, 27.5) for aktor in neue_grenzen()}
erwartet = {"luefter_serverraum": True, "luefter_lager": False, "luefter_buero": True}
assert ergebnisse == erwartet, meldung or (
    f"Bei 27.5 Grad ergeben die live-Regeln {ergebnisse!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Der Aktor muss früh gebunden werden (Fabrikfunktion mit aktor als Parameter), nur die Grenze spät."
)

# live_regeln: eine geänderte Grenze wirkt sofort
grenzen = neue_grenzen()
regeln, meldung = regeln_von(live_regeln, grenzen)
grenzen["luefter_lager"] = 25.0
ergebnis = meldung or schaltet(regeln, "luefter_lager", 28.0)
assert ergebnis is True, meldung or (
    f'Nach grenzen["luefter_lager"] = 25.0 ergibt die live-Regel für 28.0 {ergebnis!r}, erwartet war True.\n'
    "Tipp: Lesen Sie grenzen[aktor] erst im Rumpf der Regel, bei jedem Aufruf neu, und kopieren Sie grenzen nicht."
)

# live_regeln: mehrere Änderungen nacheinander
grenzen = neue_grenzen()
regeln, meldung = regeln_von(live_regeln, grenzen)
ergebnisse = []
for neu in [25.0, 29.0, 28.0]:
    grenzen["luefter_lager"] = neu
    ergebnisse.append(meldung or schaltet(regeln, "luefter_lager", 28.0))
assert ergebnisse == [True, False, False], meldung or (
    f"Mit den Grenzen 25.0, 29.0 und 28.0 ergibt die live-Regel bei 28.0 {ergebnisse!r}, erwartet war "
    "[True, False, False] (auf der Grenze aus)."
)

# live_regeln: keine Aktoren
regeln, meldung = regeln_von(live_regeln, {})
assert meldung is None and regeln == {}, meldung or f"live_regeln({{}}) ergibt {regeln!r}, erwartet war {{}}."


def schwelle(grenze):
    """Testfunktion: eine Closure mit einer Variablen."""
    return lambda wert: wert > grenze


def band(unten, oben):
    """Testfunktion: eine Closure mit zwei Variablen."""

    def drin(wert):
        """True, wenn wert im Band liegt."""
        return unten <= wert <= oben

    return drin


def zaehler():
    """Testfunktion: eine Closure, deren Variable sich bei jedem Aufruf ändert."""
    stand = 0

    def weiter():
        """Erhöht den Stand."""
        nonlocal stand
        stand += 1
        return stand

    return weiter


def ohne_closure(wert):
    """Testfunktion ohne äußere Variablen."""
    return wert * 2


# gebundene_werte: eine Variable
ergebnis, fehler = rufe(gebundene_werte, schwelle(27.0))
assert ergebnis == {"grenze": 27.0}, (
    f"gebundene_werte(schwelle(27.0)) ergibt {ergebnis!r}, erwartet war {{'grenze': 27.0}}."
    + (f"\nDie Funktion löst {fehler} aus." if fehler else "")
    + "\nTipp: Die Namen stehen in funktion.__code__.co_freevars, die Zellen in funktion.__closure__; den Wert "
    "einer Zelle liefert zelle.cell_contents."
)

# gebundene_werte: zwei Variablen (nicht fest hinschreiben!)
ergebnis, fehler = rufe(gebundene_werte, band(18, 26.5))
assert ergebnis == {"unten": 18, "oben": 26.5}, (
    f"gebundene_werte(band(18, 26.5)) ergibt {ergebnis!r}, erwartet war {{'unten': 18, 'oben': 26.5}}."
    + (f"\nDie Funktion löst {fehler} aus." if fehler else "")
    + "\nTipp: zip(namen, zellen) ordnet jedem Namen seine Zelle zu."
)

# gebundene_werte: eine Funktion ohne äußere Variablen
ergebnis, fehler = rufe(gebundene_werte, ohne_closure)
assert ergebnis == {}, (
    f"gebundene_werte(ohne_closure) ergibt {ergebnis!r}, erwartet war {{}}."
    + (f"\nDie Funktion löst {fehler} aus." if fehler else "")
    + "\nTipp: Ohne äußere Variablen ist funktion.__closure__ None."
)

# gebundene_werte: der aktuelle Wert, nicht der beim Bauen
weiter = zaehler()
weiter()
weiter()
ergebnis, fehler = rufe(gebundene_werte, weiter)
assert ergebnis == {"stand": 2}, (
    f"Nach zwei Aufrufen eines Zählers ergibt gebundene_werte {ergebnis!r}, erwartet war {{'stand': 2}}: Die Zelle "
    "enthält immer den aktuellen Wert." + (f"\nDie Funktion löst {fehler} aus." if fehler else "")
)

# gebundene_werte: Regeln aus einer Comprehension teilen sich eine Zelle
falsche = [lambda wert: wert > g for g in (24.5, 27.0, 30.0)]
ergebnis, fehler = rufe(gebundene_werte, falsche[0])
assert ergebnis == {"g": 30.0}, (
    "Für die erste von [lambda wert: wert > g for g in (24.5, 27.0, 30.0)] ergibt gebundene_werte "
    f"{ergebnis!r}, erwartet war {{'g': 30.0}}." + (f"\nDie Funktion löst {fehler} aus." if fehler else "")
)



def live_fabrik(grenzen):
    """Baut wie live_regeln eine Fabrik, deren Regeln den Aktor und das Dictionary grenzen binden."""

    def regel_fuer(aktor):
        """Gibt eine Regel zurück, die grenzen[aktor] erst beim Aufruf liest."""
        return lambda temperatur: temperatur > grenzen[aktor]

    return regel_fuer


# gebundene_werte: eine live-Regel bindet den Aktor und das Dictionary selbst
grenzen = neue_grenzen()
ergebnis, fehler = rufe(gebundene_werte, live_fabrik(grenzen)("luefter_lager"))
werte = list(ergebnis.values()) if isinstance(ergebnis, dict) else []
assert "luefter_lager" in werte and any(wert is grenzen for wert in werte), (
    "Für eine Regel lambda temperatur: temperatur > grenzen[aktor] aus einer Fabrik ergibt gebundene_werte "
    f"{ergebnis!r}; erwartet waren unter den Werten der Aktor 'luefter_lager' und das Dictionary grenzen selbst "
    "(nicht eine Kopie)." + (f"\nDie Funktion löst {fehler} aus." if fehler else "")
)

# 200 zufällige Grenzen: beide Regelarten gegen eine Vergleichslösung
zufall = Zufall(4081)
for _ in range(200):
    grenzen = {f"aktor{nummer}": zufall.randint(-500, 1500) / 10 for nummer in range(zufall.randint(0, 6))}
    alt = dict(grenzen)
    fest, meldung = regeln_von(schaltregeln, grenzen)
    assert meldung is None, meldung
    live, meldung = regeln_von(live_regeln, grenzen)
    assert meldung is None, meldung
    for aktor in grenzen:
        grenzen[aktor] = zufall.randint(-500, 1500) / 10
    for aktor in grenzen:
        temperatur = zufall.choice([alt[aktor], grenzen[aktor], zufall.randint(-500, 1500) / 10])
        ergebnis = schaltet(fest, aktor, temperatur)
        assert ergebnis is (temperatur > alt[aktor]), (
            f"schaltregeln: Regel für {aktor} (Grenze beim Bauen {alt[aktor]}, jetzt {grenzen[aktor]}) ergibt bei "
            f"{temperatur} {ergebnis!r}, erwartet war {temperatur > alt[aktor]}."
        )
        ergebnis = schaltet(live, aktor, temperatur)
        assert ergebnis is (temperatur > grenzen[aktor]), (
            f"live_regeln: Regel für {aktor} (Grenze beim Bauen {alt[aktor]}, jetzt {grenzen[aktor]}) ergibt bei "
            f"{temperatur} {ergebnis!r}, erwartet war {temperatur > grenzen[aktor]}."
        )

# Obere Grenze: 1000 Aktoren, jede Regel mit ihrer eigenen Grenze
grenzen = {f"luefter_{nummer:04d}": -50 + nummer * 0.2 for nummer in range(1000)}
fest, meldung = regeln_von(schaltregeln, grenzen)
live, zweite_meldung = regeln_von(live_regeln, grenzen)
falsch = [] if meldung or zweite_meldung else [
    aktor for aktor, grenze in grenzen.items()
    if schaltet(fest, aktor, grenze + 0.1) is not True or schaltet(live, aktor, grenze) is not False
]
assert not meldung and not zweite_meldung and not falsch, meldung or zweite_meldung or (
    f"Bei 1000 Aktoren schalten {len(falsch)} Regeln falsch, zuerst {falsch[0]} (Grenze {grenzen[falsch[0]]})."
)
