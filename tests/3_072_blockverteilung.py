# Automatisch erzeugt aus lehrkraft/muster/3_072_blockverteilung.py - nicht von Hand ändern.
# vorlage-hash: e65b962b2ec9422a
# text-hash: cb0e4dabf09eabe1
# thema: algorithmen
# inhalt: Schnelles Potenzieren modulo m

import ast
import inspect


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_potenz(basis, exponent, modul):
    """Vergleichslösung für kleine Exponenten: multipliziert exponent-mal und nimmt jedes Mal den Rest."""
    ergebnis = 1 % modul
    for _ in range(exponent):
        ergebnis = ergebnis * basis % modul
    return ergebnis


def potenz_ohne_schleife(block):
    """Vergleichslösung für große Blöcke: das eingebaute pow mit drei Argumenten."""
    return pow(16807, block, 2147483647)


def pruefe(funktion, argumente, erwartet, hinweis=""):
    """Prüft funktion(*argumente) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, *argumente)
    gezeigt = ", ".join(repr(argument) for argument in argumente)
    return ergebnis == erwartet, f"{funktion.__name__}({gezeigt}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"


def rechnet_mit_hoch():
    """Prüft im Quelltext von potenz_mod und knoten_fuer, ob ** oder pow vorkommt."""
    for funktion in (potenz_mod, knoten_fuer):
        try:
            baum = ast.parse(inspect.getsource(funktion))
        except (OSError, TypeError, SyntaxError):
            continue
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.BinOp) and isinstance(knoten.op, ast.Pow):
                return True
            if isinstance(knoten, ast.AugAssign) and isinstance(knoten.op, ast.Pow):
                return True
            if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Name) and knoten.func.id == "pow":
                return True
    return False


HOCH_GEFUNDEN = rechnet_mit_hoch()


def nur_ohne_hoch():
    """Bricht den folgenden Test ab, wenn die Lösung ** oder pow verwendet (er liefe sonst ewig)."""
    if HOCH_GEFUNDEN:
        raise RuntimeError(
            "Test übersprungen: Ihre Lösung rechnet mit ** oder pow. Mit Exponenten bis 10**18 würde ** eine Zahl mit "
            "Trillionen Stellen bauen. Schreiben Sie das schnelle Potenzieren selbst, siehe Hintergrund."
        )


SCHRITTE_KLEIN = None


def nur_schnell():
    """Bricht den folgenden Test ab, wenn potenz_mod für große Exponenten ewig bräuchte."""
    nur_ohne_hoch()
    if SCHRITTE_KLEIN is None or SCHRITTE_KLEIN > 300:
        raise RuntimeError(
            "Test übersprungen, weil der Laufzeittest von potenz_mod nicht bestanden ist: Mit Exponenten bis "
            "10**18 würde Ihre Lösung zu lange rechnen."
        )


# potenz_mod: das erste Beispiel aus der Aufgabe
stimmt, text = pruefe(potenz_mod, (3, 13, 7), 3, "\nTipp: 3 hoch 13 ist 1594323, und 1594323 % 7 ist 3.")
assert stimmt, text

# potenz_mod: das zweite Beispiel (nicht fest hinschreiben!)
stimmt, text = pruefe(potenz_mod, (2, 10, 1000), 24)
assert stimmt, text

# potenz_mod: noch andere Zahlen
stimmt, text = pruefe(potenz_mod, (5, 117, 19), vergleich_potenz(5, 117, 19))
assert stimmt, text

# potenz_mod: Exponent 1 ergibt die Basis modulo modul
stimmt, text = pruefe(potenz_mod, (45, 1, 7), 3, "\nTipp: Auch die Basis selbst muss modulo modul genommen werden.")
assert stimmt, text

# potenz_mod: Exponent 0 ergibt 1
stimmt, text = pruefe(potenz_mod, (9, 0, 5), 1, "\nTipp: Beginnen Sie mit ergebnis = 1; ohne Durchlauf bleibt es dabei.")
assert stimmt, text

# potenz_mod: Basis 0
stimmt, text = pruefe(potenz_mod, (0, 5, 7), 0)
assert stimmt, text

# potenz_mod: 0 hoch 0 ist 1
stimmt, text = pruefe(potenz_mod, (0, 0, 7), 1)
assert stimmt, text

# potenz_mod: modulo 1 ist alles 0, auch hoch 0
stimmt, text = pruefe(
    potenz_mod, (9, 0, 1), 0,
    "\nTipp: Auch das Startergebnis 1 muss modulo modul genommen werden: 1 % 1 ist 0.",
)
assert stimmt, text

# potenz_mod: Basis größer als modul
stimmt, text = pruefe(potenz_mod, (10**18, 3, 1000003), vergleich_potenz(10**18, 3, 1000003))
assert stimmt, text

# potenz_mod: weder ** noch pow
assert not HOCH_GEFUNDEN, (
    "potenz_mod oder knoten_fuer rechnet mit ** oder pow. Schreiben Sie das schnelle Potenzieren selbst: "
    "Quadrieren, Exponent halbieren, bei ungeradem Exponenten ins Ergebnis multiplizieren."
)

zufall = Zufall(3072)

# potenz_mod: viele zufällige Zahlen
for _ in range(300):
    basis = zufall.randint(0, zufall.choice([10, 1000, 10**18]))
    exponent = zufall.randint(0, 200)
    modul = zufall.randint(1, zufall.choice([2, 50, 10**9, 10**18]))
    stimmt, text = pruefe(potenz_mod, (basis, exponent, modul), vergleich_potenz(basis, exponent, modul))
    assert stimmt, text

# Laufzeit: potenz_mod braucht O(log exponent) Schritte
nur_ohne_hoch()
ergebnis, SCHRITTE_KLEIN = zaehle_schritte(potenz_mod, 3, 100_000, 1_000_003)
assert ergebnis == vergleich_potenz(3, 100_000, 1_000_003) and SCHRITTE_KLEIN <= 300, (
    f"potenz_mod(3, 100000, 1000003) ergibt {ergebnis!r} mit {SCHRITTE_KLEIN} Schritten; erwartet war "
    f"{vergleich_potenz(3, 100_000, 1_000_003)} mit höchstens 300 Schritten (O(log n)). Wer die Basis "
    "100000-mal multipliziert, braucht mindestens 100000 Schritte.\n"
    "Tipp: Halbieren Sie den Exponenten in jedem Durchlauf und quadrieren Sie die Potenz."
)

# Obere Grenze: potenz_mod mit Exponent 10**18
nur_schnell()
ergebnis, schritte = zaehle_schritte(potenz_mod, 16807, 10**18, 2147483647)
assert ergebnis == 302335999 and schritte <= 800, (
    f"potenz_mod(16807, 10**18, 2147483647) ergibt {ergebnis!r} mit {schritte} Schritten; erwartet war "
    "302335999 mit höchstens 800 Schritten."
)

# Obere Grenze: großer Modul, Zwischenergebnisse bleiben klein genug
nur_schnell()
stimmt, text = pruefe(potenz_mod, (10**18 - 1, 10**18, 10**18), 1)
assert stimmt, text

# knoten_fuer: das erste Beispiel aus der Aufgabe
stimmt, text = pruefe(
    knoten_fuer, (1, 10), 7,
    "\nTipp: 16807 hoch 1 modulo 2147483647 ist 16807, und 16807 % 10 ist 7. Verwenden Sie potenz_mod.",
)
assert stimmt, text

# knoten_fuer: andere Blöcke und Knotenzahlen (nicht fest hinschreiben!)
stimmt, text = pruefe(knoten_fuer, (2, 1000), 249)
assert stimmt, text

# knoten_fuer: Block 0 liegt auf Knoten 1 % anzahl_knoten
stimmt, text = pruefe(knoten_fuer, (0, 7), 1)
assert stimmt, text

# knoten_fuer: ein einziger Knoten
stimmt, text = pruefe(knoten_fuer, (123456, 1), 0)
assert stimmt, text

# knoten_fuer: das zweite Beispiel mit Block 10**18
nur_schnell()
stimmt, text = pruefe(knoten_fuer, (10**18, 10), 9)
assert stimmt, text

# verteilung: das Beispiel aus der Aufgabe
stimmt, text = pruefe(
    verteilung, ([1, 2, 3, 4, 5], 3), [0, 3, 2],
    "\nTipp: Legen Sie eine Liste mit anzahl_knoten Nullen an und zählen Sie für jeden Block knoten_fuer hoch.",
)
assert stimmt, text

# verteilung: andere Blöcke (nicht fest hinschreiben!)
erwartet = [0, 0]
for block in [10, 20, 30, 40]:
    erwartet[vergleich_potenz(16807, block, 2147483647) % 2] += 1
stimmt, text = pruefe(verteilung, ([10, 20, 30, 40], 2), erwartet)
assert stimmt, text

# verteilung: keine Blöcke
stimmt, text = pruefe(verteilung, ([], 4), [0, 0, 0, 0], "\nTipp: Auch ohne Blöcke hat die Liste anzahl_knoten Einträge.")
assert stimmt, text

# verteilung: Knoten ohne Block zählen mit 0
stimmt, text = pruefe(verteilung, ([0, 0, 0], 3), [0, 3, 0])
assert stimmt, text

# verteilung: viele zufällige Listen
for _ in range(100):
    bloecke = [zufall.randint(0, 300) for _ in range(zufall.randint(0, 20))]
    anzahl = zufall.randint(1, 8)
    erwartet = [0] * anzahl
    for block in bloecke:
        erwartet[vergleich_potenz(16807, block, 2147483647) % anzahl] += 1
    stimmt, text = pruefe(verteilung, (bloecke, anzahl), erwartet)
    assert stimmt, text

# Obere Grenze: 2000 große Blocknummern auf 1000 Knoten
nur_schnell()
bloecke = [zufall.randint(0, 10**18) for _ in range(2000)]
ergebnis = wert_von(verteilung, bloecke, 1000)
erwartet = [0] * 1000
for block in bloecke:
    erwartet[potenz_ohne_schleife(block) % 1000] += 1
assert ergebnis == erwartet, (
    f"verteilung mit 2000 Blöcken auf 1000 Knoten ergibt {str(ergebnis)[:80]}…, erwartet war {str(erwartet)[:80]}…"
)
