# Automatisch erzeugt aus lehrkraft/muster/4_082_aenderungsantraege.py - nicht von Hand ändern.
# vorlage-hash: 808679881d5fa1f3
# text-hash: 38ce8fbd183a0860
# thema: funktionen
# inhalt: LEGB, global, Klassenkörper

def rufe(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDie Funktion löst {fehler} aus." if fehler else ""


def nummer_als_zahl(antrag):
    """Gibt die Zahl hinter "CR-" in antrag["nummer"] zurück, sonst None; das Format prüft ein eigener Test."""
    try:
        return int(antrag["nummer"].removeprefix("CR-"))
    except Exception:
        return None


def ohne_format(antrag):
    """Gibt den Antrag mit der Nummer als Zahl zurück, damit Inhaltstests das Format nicht mitprüfen."""
    if not isinstance(antrag, dict) or nummer_als_zahl(antrag) is None:
        return antrag
    return {**antrag, "nummer": nummer_als_zahl(antrag)}


def projektteam():
    """Gibt die Klasse Projektteam zurück oder None, wenn sie wegen eines Fehlers im Klassenkörper fehlt."""
    try:
        return Projektteam
    except NameError:
        return None


def ohne_klasse():
    """Erklärt, warum es Projektteam nicht gibt, wenn sie fehlt; sonst ein leerer Text."""
    if projektteam() is not None:
        return ""
    return (
        "\nDie Klasse Projektteam ist nicht entstanden, weil ihr Klassenkörper einen Fehler auslöst (siehe die "
        "Meldung zu Ihrem Programm oben).\nTipp: Eine Comprehension im Klassenkörper sieht TAGESSTUNDEN nicht "
        "(siehe Hintergrund); [TAGESSTUNDEN] * 5 geht."
    )


def team(personen, stunden):
    """Baut eine Unterklasse von Projektteam mit anderen Klassenattributen (None, wenn Projektteam fehlt)."""
    if projektteam() is None:
        return None
    return type("Testteam", (Projektteam,), {"PERSONEN": personen, "STUNDEN_PRO_TAG": stunden})


def erwartete_dauer(tage, personen, stunden):
    """Vergleichslösung: zählt Tage hoch, bis die Stunden reichen."""
    tage_noetig = 0
    while tage_noetig * personen * stunden < tage * 8:
        tage_noetig += 1
    return tage_noetig


def dauer_von(klasse, tage):
    """Ruft klasse().dauer für einen Antrag mit tage Personentagen auf; liefert (Ergebnis, Fehlertext)."""
    if klasse is None:
        return None, None
    return rufe(lambda: klasse().dauer({"nummer": "CR-100", "titel": "Test", "tage": tage}))


TIPP_GLOBAL = (
    "\nTipp: Weist eine Funktion LETZTE_NUMMER etwas zu, ist der Name lokal (UnboundLocalError). "
    "Kündigen Sie mit global LETZTE_NUMMER an, dass Sie die globale Variable meinen."
)

# neuer_antrag: der erste Antrag bekommt CR-001
LETZTE_NUMMER = 0
ergebnis, fehler = rufe(neuer_antrag, "Export als PDF", 3)
erwartet = {"nummer": "CR-001", "titel": "Export als PDF", "tage": 3}
assert ohne_format(ergebnis) == ohne_format(erwartet), (
    f"Mit LETZTE_NUMMER = 0 ergibt neuer_antrag('Export als PDF', 3) {ergebnis!r}, erwartet war {erwartet!r}."
    + absturz(fehler) + (TIPP_GLOBAL if fehler and "Unbound" in fehler else "")
)

# neuer_antrag: der nächste Antrag bekommt die nächste Nummer
LETZTE_NUMMER = 0
rufe(neuer_antrag, "Export als PDF", 3)
ergebnis, fehler = rufe(neuer_antrag, "Zweite Sprache", 5)
assert ohne_format(ergebnis) == {"nummer": 2, "titel": "Zweite Sprache", "tage": 5}, (
    f"Der zweite Aufruf ergibt {ergebnis!r}, erwartet war {{'nummer': 'CR-002', 'titel': 'Zweite Sprache', "
    "'tage': 5}." + absturz(fehler) + (TIPP_GLOBAL if fehler and "Unbound" in fehler else "")
)

# neuer_antrag: zählt in der globalen Variablen LETZTE_NUMMER
LETZTE_NUMMER = 0
for _ in range(3):
    rufe(neuer_antrag, "Test", 1)
assert LETZTE_NUMMER == 3, (
    f"Nach drei Aufrufen von neuer_antrag ist LETZTE_NUMMER {LETZTE_NUMMER!r}, erwartet war 3." + TIPP_GLOBAL
)

# neuer_antrag: liest den aktuellen Stand von LETZTE_NUMMER (nicht fest hinschreiben!)
LETZTE_NUMMER = 41
ergebnis, fehler = rufe(neuer_antrag, "Dunkles Design", 12)
assert ergebnis is not None and ergebnis.get("nummer") == "CR-042", (
    f"Mit LETZTE_NUMMER = 41 ergibt neuer_antrag('Dunkles Design', 12) {ergebnis!r}, erwartet war die Nummer "
    "'CR-042'." + absturz(fehler)
    + (
        "\nTipp: Die Nummer ist dreistellig mit führenden Nullen: f\"CR-{nummer:03d}\"."
        if nummer_als_zahl(ergebnis) == 42
        else ""
    )
)

# neuer_antrag: ab 1000 vierstellig
LETZTE_NUMMER = 999
ergebnis, fehler = rufe(neuer_antrag, "Schnittstelle", 30)
assert ergebnis is not None and ergebnis.get("nummer") == "CR-1000", (
    f"Mit LETZTE_NUMMER = 999 ergibt neuer_antrag {ergebnis!r}, erwartet war die Nummer 'CR-1000' (mindestens drei "
    "Ziffern, mehr wenn nötig)." + absturz(fehler)
)

# Projektteam: TAGESSTUNDEN im Klassenkörper
wert = getattr(projektteam(), "TAGESSTUNDEN", "fehlt")
assert wert == 6, (
    f"Projektteam.TAGESSTUNDEN ist {wert!r}, erwartet war 6 (PERSONEN · STUNDEN_PRO_TAG = 3 · 2)."
    + (
        ohne_klasse()
        or "\nTipp: Im Klassenkörper sehen Sie die Namen, die weiter oben in der Klasse stehen: "
        "TAGESSTUNDEN = PERSONEN * STUNDEN_PRO_TAG."
    )
)

# Projektteam: WOCHENPLAN im Klassenkörper
wert = getattr(projektteam(), "WOCHENPLAN", "fehlt")
assert wert == [6, 6, 6, 6, 6], (
    f"Projektteam.WOCHENPLAN ist {wert!r}, erwartet war [6, 6, 6, 6, 6].\n"
    "Tipp: Eine Comprehension im Klassenkörper sieht TAGESSTUNDEN nicht; [TAGESSTUNDEN] * 5 geht."
)

# dauer: das Beispiel
ergebnis, fehler = dauer_von(projektteam(), 3)
assert ergebnis == 4, (
    f"Projektteam().dauer(antrag) mit 3 Personentagen ergibt {ergebnis!r}, erwartet war 4: 3 · 8 = 24 Stunden laut "
    "Vertrag, das Team schafft 3 · 2 = 6 Stunden pro Tag." + absturz(fehler) + ohne_klasse()
    + ("\nTipp: Ihre Methode rechnet den Aufwand mit 2 statt 8 Stunden pro Personentag. Der Vertrag steht in der "
       "globalen Variablen STUNDEN_PRO_TAG; self.STUNDEN_PRO_TAG ist die Zeit des Teams." if ergebnis == 1 else "")
)

# dauer: wird aufgerundet
ergebnis, fehler = dauer_von(projektteam(), 5)
assert ergebnis == 7, (
    f"Projektteam().dauer(antrag) mit 5 Personentagen ergibt {ergebnis!r}, erwartet war 7: 40 Stunden / 6 Stunden "
    "pro Tag sind 6,67 Tage, angefangene Tage zählen ganz.\nTipp: math.ceil rundet auf." + absturz(fehler) + ohne_klasse()
)

# dauer: geht genau auf
ergebnis, fehler = dauer_von(projektteam(), 6)
assert ergebnis == 8, (
    f"Projektteam().dauer(antrag) mit 6 Personentagen ergibt {ergebnis!r}, erwartet war 8 (48 / 6, ohne Rest)."
    + absturz(fehler) + ohne_klasse()
)

# dauer: eine Unterklasse mit mehr Personen
ergebnis, fehler = dauer_von(team(6, 2), 3)
assert ergebnis == 2, (
    f"Für eine Unterklasse mit PERSONEN = 6 ergibt dauer bei 3 Personentagen {ergebnis!r}, erwartet war 2 "
    "(24 Stunden / 12 Stunden pro Tag)." + absturz(fehler) + ohne_klasse()
    + "\nTipp: Lesen Sie die Klassenattribute über self (self.PERSONEN), dann gelten die Werte der Unterklasse. "
    "Projektteam.PERSONEN oder TAGESSTUNDEN sind die Werte der Basisklasse."
)

# dauer: eine Unterklasse mit anderen Stunden pro Person
ergebnis, fehler = dauer_von(team(3, 8), 3)
assert ergebnis == 1, (
    f"Für eine Unterklasse mit STUNDEN_PRO_TAG = 8 ergibt dauer bei 3 Personentagen {ergebnis!r}, erwartet war 1 "
    "(24 Stunden / 24 Stunden pro Tag)." + absturz(fehler) + ohne_klasse()
)

# dauer: der Vertrag zählt auch in Unterklassen 8 Stunden pro Personentag
ergebnis, fehler = dauer_von(team(1, 1), 2)
assert ergebnis == 16, (
    f"Für eine Unterklasse mit PERSONEN = 1 und STUNDEN_PRO_TAG = 1 ergibt dauer bei 2 Personentagen {ergebnis!r}, "
    "erwartet war 16 (2 · 8 Stunden laut Vertrag, 1 Stunde pro Tag)." + absturz(fehler) + ohne_klasse()
)

# dauer: ein Personentag
ergebnis, fehler = dauer_von(projektteam(), 1)
assert ergebnis == 2, f"Projektteam().dauer(antrag) mit 1 Personentag ergibt {ergebnis!r}, erwartet war 2 (8 / 6)." + absturz(
    fehler
) + ohne_klasse()


def mit_closure(start):
    """Testfunktion: start ist lokal, wird aber von innen mitbenutzt."""
    summe = start

    def innen(wert):
        """Benutzt summe aus der umgebenden Funktion."""
        return summe + wert + len([wert])

    return innen


def verdeckt(werte):
    """Testfunktion: benutzt max und das globale LETZTE_NUMMER."""
    return max(werte) + LETZTE_NUMMER


def fehlt_noch():
    """Testfunktion: benutzt einen Namen, den es nirgends gibt."""
    return gibt_es_nicht + 1  # noqa: F821 - absichtlich undefiniert


def pruefe_bereich(funktion, name, erwartet, tipp=""):
    """Ruft bereich auf und vergleicht; liefert (stimmt, Meldung)."""
    ergebnis, fehler = rufe(bereich, funktion, name)
    text = f"bereich({funktion.__name__}, {name!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{absturz(fehler)}"
    return ergebnis == erwartet, text + tipp


# bereich: ein Parameter ist lokal
stimmt, text = pruefe_bereich(
    neuer_antrag, "titel", "lokal", "\nTipp: Parameter und lokale Variablen stehen in funktion.__code__.co_varnames."
)
assert stimmt, text

# bereich: eine globale Variable
stimmt, text = pruefe_bereich(
    neuer_antrag, "LETZTE_NUMMER", "global", "\nTipp: Die globalen Variablen stehen in funktion.__globals__."
)
assert stimmt, text

# bereich: in einer Methode ist der gleichnamige Klassenname nicht sichtbar
stimmt, text = (
    pruefe_bereich(Projektteam.dauer, "STUNDEN_PRO_TAG", "global") if projektteam() else (False, ohne_klasse().strip())
)
assert stimmt, text

# bereich: self in einer Methode ist lokal
stimmt, text = pruefe_bereich(Projektteam.dauer, "self", "lokal") if projektteam() else (False, ohne_klasse().strip())
assert stimmt, text

# bereich: eine eingebaute Funktion
stimmt, text = pruefe_bereich(
    verdeckt, "max", "eingebaut", "\nTipp: hasattr(builtins, name) sagt, ob es einen eingebauten Namen gibt."
)
assert stimmt, text

# bereich: ein Name aus der umgebenden Funktion
stimmt, text = pruefe_bereich(
    mit_closure(5), "summe", "umschließend", "\nTipp: Namen aus umgebenden Funktionen stehen in co_freevars."
)
assert stimmt, text

# bereich: eine lokale Variable, die eine innere Funktion mitbenutzt, ist trotzdem lokal
stimmt, text = pruefe_bereich(
    mit_closure, "summe", "lokal", "\nTipp: Solche Variablen stehen in co_cellvars statt in co_varnames."
)
assert stimmt, text

# bereich: in einer inneren Funktion ist ein eigener Parameter lokal und len eingebaut
innen = mit_closure(5)
erstes, text_eins = pruefe_bereich(innen, "wert", "lokal")
zweites, text_zwei = pruefe_bereich(innen, "len", "eingebaut")
assert erstes and zweites, text_eins if not erstes else text_zwei

# bereich: ein globaler Name verdeckt den eingebauten
verdeckt_mit_max = type(verdeckt)(verdeckt.__code__, {"max": 3, "LETZTE_NUMMER": 0})
stimmt, text = pruefe_bereich(
    verdeckt_mit_max, "max", "global",
    "\nTipp: Python sucht global vor eingebaut; prüfen Sie funktion.__globals__ vor builtins.",
)
assert stimmt, text

# bereich: ein Name, den es nirgends gibt
stimmt, text = pruefe_bereich(fehlt_noch, "gibt_es_nicht", None)
assert stimmt, text

# 300 zufällige Teams und Anträge: dauer gegen eine Vergleichslösung
zufall = Zufall(4082)
for _ in range(300):
    personen, stunden, tage = zufall.randint(1, 50), zufall.randint(1, 8), zufall.randint(1, 1000)
    ergebnis, fehler = dauer_von(team(personen, stunden), tage)
    erwartet = erwartete_dauer(tage, personen, stunden)
    assert ergebnis == erwartet, (
        f"Team mit PERSONEN = {personen}, STUNDEN_PRO_TAG = {stunden}: dauer für {tage} Personentage ergibt "
        f"{ergebnis!r}, erwartet war {erwartet}." + absturz(fehler) + ohne_klasse()
    )

# Obere Grenze: Nummern bis CR-99999
LETZTE_NUMMER = 0
nummern = [rufe(neuer_antrag, f"Antrag {i}", 1)[0] for i in range(99999)]
falsch = [i for i, antrag in enumerate(nummern) if not antrag or nummer_als_zahl(antrag) != i + 1]
assert not falsch, (
    f"Bei {len(nummern)} Anträgen hat Antrag Nummer {falsch[0] + 1} den Eintrag {nummern[falsch[0]]!r}, "
    f"erwartet war 'CR-{falsch[0] + 1:03d}'."
)
