# Automatisch erzeugt aus lehrkraft/muster/3_058_kabelplan.py - nicht von Hand ändern.
# vorlage-hash: 16cb85c6a64b86b5
# text-hash: f00f95add642fded
# thema: algorithmen
# inhalt: Graph als Dictionary, Breitensuche

import ast
import copy

KABEL = [
    ("core", "sw1"),
    ("core", "sw2"),
    ("sw1", "srv1"),
    ("sw2", "srv2"),
    ("srv2", "srv3"),
    ("sw1", "sw2"),
    ("nas", "srv9"),
]
GRAPH = {
    "core": ["sw1", "sw2"],
    "sw1": ["core", "srv1", "sw2"],
    "sw2": ["core", "srv2", "sw1"],
    "srv1": ["sw1"],
    "srv2": ["sw2", "srv3"],
    "srv3": ["srv2"],
    "nas": ["srv9"],
    "srv9": ["nas"],
}


def wert_von(funktion, *argumente):
    """Ruft funktion mit Kopien der Argumente auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*copy.deepcopy(argumente))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_abstaende(kabel, start):
    """Langsame Vergleichslösung: verbessert so lange Abstände über jedes Kabel, bis sich nichts mehr ändert."""
    abstand = {start: 0}
    geaendert = True
    while geaendert:
        geaendert = False
        for a, b in kabel:
            for von, nach in [(a, b), (b, a)]:
                if von in abstand and (nach not in abstand or abstand[von] + 1 < abstand[nach]):
                    abstand[nach] = abstand[von] + 1
                    geaendert = True
    return abstand


def vergleich_zu_weit(kabel, start, hoechstens):
    """Vergleichslösung für zu_weit aus den langsam berechneten Abständen."""
    abstand = vergleich_abstaende(kabel, start)
    geraete = {geraet for paar in kabel for geraet in paar}
    return sorted(geraet for geraet in geraete if abstand.get(geraet, hoechstens + 1) > hoechstens)


def kurz(wert):
    """Kürzt lange Werte für die Meldung."""
    text = repr(wert)
    return text if len(text) <= 300 else text[:200] + f" … ({len(wert)} Einträge)"


def meldung(funktion, argumente, erwartet, hinweis=""):
    """Prüft funktion(*argumente) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, *argumente)
    gezeigt = ", ".join(kurz(argument) for argument in argumente)
    text = f"{funktion.__name__}({gezeigt})\nergibt   {kurz(ergebnis)}\nerwartet {kurz(erwartet)}{hinweis}"
    return ergebnis == erwartet, text


def graph_aus(kabel):
    """Baut den Graphen für die Tests selbst, damit ein Fehler in als_graph sprungzahlen nicht stört."""
    graph = {}
    for a, b in kabel:
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, []).append(a)
    return graph


def zufallskabel(zufall, geraete, anzahl, vorhanden=()):
    """Erzeugt bis zu anzahl neue, verschiedene Kabel zwischen den Geräten g0, g1, …"""
    kabel = []
    gesehen = set()
    for a, b in vorhanden:
        gesehen.add((int(a[1:]), int(b[1:])))
        gesehen.add((int(b[1:]), int(a[1:])))
    for _ in range(anzahl):
        a, b = zufall.sample(range(geraete), 2)
        if (a, b) not in gesehen:
            gesehen.add((a, b))
            gesehen.add((b, a))
            kabel.append((f"g{a}", f"g{b}"))
    return kabel


# als_graph: die Nachbarn eines Geräts
graph = wert_von(als_graph, KABEL)
ergebnis = graph.get("sw1") if isinstance(graph, dict) else graph
assert ergebnis == ["core", "srv1", "sw2"], (
    f"als_graph(kabel)['sw1'] ergibt {ergebnis!r}, erwartet war ['core', 'srv1', 'sw2'].\n"
    "Tipp: Ein Kabel (a, b) macht b zum Nachbarn von a und a zum Nachbarn von b."
)

# als_graph: das ganze Beispiel
stimmt, text = meldung(als_graph, [KABEL], GRAPH, "\nTipp: Jedes Gerät aus kabel braucht einen Eintrag.")
assert stimmt, text

# als_graph: andere Kabel (nicht fest hinschreiben!)
stimmt, text = meldung(als_graph, [[("a", "b"), ("c", "a")]], {"a": ["b", "c"], "b": ["a"], "c": ["a"]})
assert stimmt, text

# als_graph: keine Kabel
stimmt, text = meldung(als_graph, [[]], {})
assert stimmt, text

# sprungzahlen: das Beispiel
stimmt, text = meldung(
    sprungzahlen, [GRAPH, "core"], {"core": 0, "sw1": 1, "sw2": 1, "srv1": 2, "srv2": 2, "srv3": 3},
    "\nTipp: Ein Nachbar bekommt den Abstand seines Vorgängers plus 1.",
)
assert stimmt, text

# sprungzahlen: von einem anderen Start aus
stimmt, text = meldung(
    sprungzahlen, [GRAPH, "srv3"], {"srv3": 0, "srv2": 1, "sw2": 2, "core": 3, "sw1": 3, "srv1": 4}
)
assert stimmt, text

# sprungzahlen: der kürzeste Weg zählt, nicht der zuerst gefundene
graph = {"a": ["b", "c"], "b": ["a", "d"], "c": ["a", "e"], "d": ["b", "e"], "e": ["c", "d"]}
stimmt, text = meldung(
    sprungzahlen, [graph, "a"], {"a": 0, "b": 1, "c": 1, "d": 2, "e": 2},
    "\nTipp: Eine Warteschlange (popleft) besucht erst alle Knoten im Abstand 1, dann alle im Abstand 2; "
    "ein Stapel (pop) geht zu tief.",
)
assert stimmt, text

# sprungzahlen: ein Ring endet
graph = {"a": ["b", "c"], "b": ["a", "c"], "c": ["b", "a"]}
stimmt, text = meldung(
    sprungzahlen, [graph, "a"], {"a": 0, "b": 1, "c": 1},
    "\nTipp: Stellen Sie nur Nachbarn an, die noch nicht in abstand stehen.",
)
assert stimmt, text

# sprungzahlen: ein Start ohne Kabel erreicht nur sich selbst
stimmt, text = meldung(
    sprungzahlen, [GRAPH, "drucker"], {"drucker": 0}, "\nTipp: graph.get(knoten, []) statt graph[knoten]."
)
assert stimmt, text

# sprungzahlen verändert den Graphen nicht
graph = copy.deepcopy(GRAPH)
try:
    sprungzahlen(graph, "core")
except Exception:
    pass
assert graph == GRAPH, f"Nach sprungzahlen(graph, 'core') ist graph {graph}; er sollte unverändert bleiben."

# zu_weit: das Beispiel
stimmt, text = meldung(zu_weit, [KABEL, "core", 2], ["nas", "srv3", "srv9"])
assert stimmt, text

# zu_weit: andere Grenze
stimmt, text = meldung(zu_weit, [KABEL, "core", 1], ["nas", "srv1", "srv2", "srv3", "srv9"])
assert stimmt, text

# zu_weit: genau hoechstens Sprünge sind nicht zu weit
stimmt, text = meldung(zu_weit, [KABEL, "core", 3], ["nas", "srv9"], "\nTipp: „mehr als hoechstens“ heißt >.")
assert stimmt, text

# zu_weit: unerreichbare Geräte zählen auch bei großer Grenze
stimmt, text = meldung(
    zu_weit, [KABEL, "core", 100000], ["nas", "srv9"],
    "\nTipp: Gehen Sie alle Geräte des Graphen durch, nicht nur die aus sprungzahlen.",
)
assert stimmt, text

# zu_weit: bei hoechstens 0 ist nur der Start nicht zu weit
stimmt, text = meldung(zu_weit, [KABEL, "sw2", 0], sorted(set(GRAPH) - {"sw2"}))
assert stimmt, text

# zu_weit: ein Start, der in keinem Kabel vorkommt
stimmt, text = meldung(zu_weit, [KABEL, "drucker", 5], sorted(GRAPH))
assert stimmt, text

# zu_weit: keine Kabel
stimmt, text = meldung(zu_weit, [[], "core", 3], [])
assert stimmt, text

# Die Ausgabe des Programms
erwartet = "{'core': 0, 'sw1': 1, 'sw2': 1, 'srv1': 2, 'srv2': 2, 'srv3': 3}\n['nas', 'srv3', 'srv9']"
ausgegeben = AUSGABE.strip().split("\n")
try:
    erste_zeile = ast.literal_eval(ausgegeben[0])
except (ValueError, SyntaxError):
    erste_zeile = None
assert (
    len(ausgegeben) == 2
    and erste_zeile == ast.literal_eval(erwartet.split("\n")[0])
    and vergleichbar(ausgegeben[1]) == vergleichbar(erwartet.split("\n")[1])
), f"Erwartete Ausgabe (die Reihenfolge im Dictionary ist egal):\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Kabelpläne
zufall = Zufall(3058)
plaene = []
for _ in range(300):
    kabel = zufallskabel(zufall, zufall.randint(2, 9), zufall.randint(0, 12))
    start = f"g{zufall.randint(0, 9)}"
    hoechstens = zufall.randint(0, 4)
    plaene.append((kabel, start, hoechstens))

# Viele zufällige Kabelpläne: sprungzahlen
for kabel, start, _ in plaene:
    stimmt, text = meldung(sprungzahlen, [graph_aus(kabel), start], vergleich_abstaende(kabel, start))
    assert stimmt, text

# Viele zufällige Kabelpläne: zu_weit
for kabel, start, hoechstens in plaene:
    stimmt, text = meldung(zu_weit, [kabel, start, hoechstens], vergleich_zu_weit(kabel, start, hoechstens))
    assert stimmt, text

# Laufzeit: eine lange Kette, vom hinteren Ende aus, braucht nicht quadratisch viele Schritte
kette = [(f"g{nummer}", f"g{nummer + 1}") for nummer in range(2000)]
graph = graph_aus(kette)
try:
    _, schritte = zaehle_schritte(sprungzahlen, graph, "g2000")
except Exception as fehler:
    schritte = f"(Abbruch: {type(fehler).__name__}: {fehler})"
assert isinstance(schritte, int) and schritte <= 20 * 2001, (
    f"Für eine Kette aus 2001 Geräten braucht sprungzahlen {schritte} Schritte, erlaubt sind 20 · 2001 = 40020.\n"
    "Tipp: Jedes Gerät kommt nur einmal in die Warteschlange; danach steht es in abstand."
)

# Obere Grenze: eine Kette aus 100 000 Kabeln
kette = [(f"g{nummer}", f"g{nummer + 1}") for nummer in range(100000)]
ergebnis = wert_von(sprungzahlen, graph_aus(kette), "g0")
erwartet = {f"g{nummer}": nummer for nummer in range(100001)}
assert ergebnis == erwartet, "Bei einer Kette aus 100 000 Kabeln stimmt sprungzahlen(graph, 'g0') nicht."

# Obere Grenze: 100 000 Kabel mit vielen Querverbindungen
kabel = kette[:50000]
kabel += zufallskabel(zufall, 50000, 50000, kabel)
ergebnis = wert_von(zu_weit, kabel, "g0", 0)
erwartet = sorted(f"g{nummer}" for nummer in range(1, 50001))
assert ergebnis == erwartet, "Bei 100 000 Kabeln stimmt zu_weit(kabel, 'g0', 0) nicht."
