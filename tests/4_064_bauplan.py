# Automatisch erzeugt aus lehrkraft/muster/4_064_bauplan.py - nicht von Hand ändern.
# vorlage-hash: 1375008d864f3cb1
# text-hash: beb8ebc54203ec4f
# thema: algorithmen
# inhalt: Topologische Sortierung (Kahn)

import copy

BEISPIEL = {
    "app": ["datenbank", "oberflaeche"],
    "oberflaeche": ["konfiguration"],
    "datenbank": ["konfiguration", "protokoll"],
    "konfiguration": [],
    "protokoll": [],
}
RING = {"kasse": ["lager"], "lager": ["kasse"], "bericht": ["kasse"], "hilfe": []}


def aufruf(funktion, abhaengigkeiten):
    """Ruft die Funktion mit einer Kopie auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(copy.deepcopy(abhaengigkeiten))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def fehler_von(funktion, abhaengigkeiten):
    """Ruft die Funktion mit einer Kopie auf und gibt die Ausnahme zurück, oder None."""
    try:
        funktion(copy.deepcopy(abhaengigkeiten))
    except Exception as fehler:
        return fehler
    return None


def plan_fehler(plan, abhaengigkeiten):
    """Beschreibt, was an einem Bauplan falsch ist, oder gibt None zurück, wenn er stimmt."""
    if not isinstance(plan, list):
        return f"bauplan ergibt {plan!r}, erwartet war eine Liste."
    if sorted(plan) != sorted(abhaengigkeiten):
        return f"bauplan ergibt {plan}, das sind nicht genau alle Module {sorted(abhaengigkeiten)}, jedes einmal."
    stelle = {modul: nummer for nummer, modul in enumerate(plan)}
    for modul, liste in abhaengigkeiten.items():
        for vorher in liste:
            if stelle[vorher] > stelle[modul]:
                return f"Im Bauplan {plan} steht {modul!r} vor {vorher!r}, braucht es aber."
    return None


def erwartete_stufen(abhaengigkeiten):
    """Vergleichslösung: die Stufe eines Moduls ist die Länge seiner längsten Kette (nur ohne Ring)."""
    stufe_von = {}

    def stufe(modul):
        """Berechnet die Stufe rekursiv und merkt sie sich."""
        if modul not in stufe_von:
            stufe_von[modul] = 1 + max((stufe(vorher) for vorher in abhaengigkeiten[modul]), default=-1)
        return stufe_von[modul]

    ergebnis = {}
    for modul in abhaengigkeiten:
        ergebnis.setdefault(stufe(modul), []).append(modul)
    return [sorted(ergebnis[nummer]) for nummer in range(len(ergebnis))]


def erreichbar(abhaengigkeiten, start):
    """Alle Module, die start über eine oder mehrere Abhängigkeiten braucht (Tiefensuche)."""
    gesehen = set()
    stapel = list(abhaengigkeiten[start])
    while stapel:
        modul = stapel.pop()
        if modul not in gesehen:
            gesehen.add(modul)
            stapel.extend(abhaengigkeiten[modul])
    return gesehen


def ohne_platz(abhaengigkeiten):
    """Vergleichslösung: die Module in einem Ring und alle, die eines davon brauchen, sortiert."""
    braucht = {modul: erreichbar(abhaengigkeiten, modul) for modul in abhaengigkeiten}
    im_ring = {modul for modul in abhaengigkeiten if modul in braucht[modul]}
    return sorted(modul for modul in abhaengigkeiten if braucht[modul] & im_ring)


def zufallsgraph(zufall, anzahl, kanten, ring):
    """Erzeugt Module m0, m1, …; ohne ring zeigen Abhängigkeiten nur auf kleinere Nummern."""
    namen = [f"m{nummer}" for nummer in range(anzahl)]
    zufall.shuffle(namen)
    graph = {name: [] for name in namen}
    for _ in range(kanten):
        a = zufall.randrange(anzahl)
        b = zufall.randrange(anzahl)
        if not ring and a == b:
            continue
        modul, vorher = (f"m{max(a, b)}", f"m{min(a, b)}") if not ring else (f"m{a}", f"m{b}")
        if vorher not in graph[modul]:
            graph[modul].append(vorher)
    return graph


# bauplan im Beispiel: alle fünf Module
plan = aufruf(bauplan, BEISPIEL)
assert isinstance(plan, list) and sorted(plan) == sorted(BEISPIEL), (
    f"bauplan(abhaengigkeiten) ergibt {plan!r}, erwartet war eine Liste mit allen fünf Modulen.\n"
    "Tipp: Zählen Sie für jedes Modul seine Abhängigkeiten und beginnen Sie mit denen, die 0 haben."
)

# bauplan im Beispiel: jedes Modul hinter seinen Abhängigkeiten
fehler = plan_fehler(plan, BEISPIEL)
assert fehler is None, fehler

# bauplan mit anderen Modulen (nicht fest hinschreiben!)
anders = {"test": ["kern", "netz"], "netz": ["kern"], "kern": [], "doku": ["test"]}
fehler = plan_fehler(aufruf(bauplan, anders), anders)
assert fehler is None, fehler

# bauplan: eine lange Kette in umgekehrter Reihenfolge im Dictionary
kette = {f"k{nummer}": [f"k{nummer - 1}"] for nummer in range(9, 0, -1)}
kette["k0"] = []
fehler = plan_fehler(aufruf(bauplan, kette), kette)
assert fehler is None, fehler + "\nTipp: Ein Modul kommt erst in die Warteschlange, wenn sein Zähler auf 0 gesunken ist."

# bauplan lässt das Dictionary unverändert
abhaengigkeiten = copy.deepcopy(BEISPIEL)
try:
    bauplan(abhaengigkeiten)
except Exception:
    pass
assert abhaengigkeiten == BEISPIEL, f"Nach bauplan(abhaengigkeiten) ist das Dictionary {abhaengigkeiten}, erwartet war es unverändert."

# Randfall: keine Module
ergebnis = aufruf(bauplan, {})
assert ergebnis == [], f"bauplan({{}}) ergibt {ergebnis!r}, erwartet war []."

# Randfall: Module ganz ohne Abhängigkeiten
unabhaengig = {"c": [], "a": [], "b": []}
fehler = plan_fehler(aufruf(bauplan, unabhaengig), unabhaengig)
assert fehler is None, fehler

# ZyklusFehler ist eine Ausnahme mit dem Attribut module
fehler = ZyklusFehler(["lager", "kasse"])
assert isinstance(fehler, Exception) and getattr(fehler, "module", None) == ["kasse", "lager"], (
    f"ZyklusFehler(['lager', 'kasse']).module ist {getattr(fehler, 'module', '(fehlt)')!r}, erwartet war ['kasse', 'lager'].\n"
    "Tipp: class ZyklusFehler(Exception) mit self.module = sorted(module) und super().__init__(meldung)."
)

# Die Meldung von ZyklusFehler nennt die Module
text = str(ZyklusFehler(["lager", "kasse"]))
assert "kasse" in text and "lager" in text, f"str(ZyklusFehler(['lager', 'kasse'])) ist {text!r}; die Meldung sollte beide Module nennen."

# bauplan mit Ring: ZyklusFehler
fehler = fehler_von(bauplan, RING)
assert isinstance(fehler, ZyklusFehler), (
    f"bauplan(ring) löst {fehler!r} aus, erwartet war ein ZyklusFehler.\n"
    "Tipp: Stehen am Ende weniger Module im Plan, als es gibt, liegt ein Ring vor."
)

# bauplan mit Ring: module nennt Ring und Abhängige, nicht die übrigen
assert getattr(fehler, "module", None) == ["bericht", "kasse", "lager"], (
    f"Bei bauplan(ring) ist fehler.module {getattr(fehler, 'module', '(fehlt)')!r}, erwartet war ['bericht', 'kasse', 'lager'].\n"
    "Tipp: Ohne Platz sind die Module, deren Zähler am Ende noch über 0 liegt; hilfe hat einen Platz bekommen."
)

# bauplan: ein Modul, das sich selbst braucht
fehler = fehler_von(bauplan, {"a": ["a"], "b": []})
assert isinstance(fehler, ZyklusFehler) and fehler.module == ["a"], (
    f"bauplan({{'a': ['a'], 'b': []}}) löst {fehler!r} aus, erwartet war ein ZyklusFehler mit module ['a']."
)

# stufen im Beispiel
ergebnis = aufruf(stufen, BEISPIEL)
assert ergebnis == [["konfiguration", "protokoll"], ["datenbank", "oberflaeche"], ["app"]], (
    f"stufen(abhaengigkeiten) ergibt {ergebnis!r},\n"
    "erwartet war [['konfiguration', 'protokoll'], ['datenbank', 'oberflaeche'], ['app']].\n"
    "Tipp: Nehmen Sie jeweils alle Module, deren Zähler 0 ist, auf einmal als eine Stufe und sortieren Sie sie."
)

# stufen mit anderen Modulen (nicht fest hinschreiben!)
ergebnis = aufruf(stufen, anders)
assert ergebnis == erwartete_stufen(anders), f"stufen({anders}) ergibt {ergebnis!r}, erwartet war {erwartete_stufen(anders)}."

# stufen: ein Modul kommt erst nach seiner spätesten Abhängigkeit
tief = {"a": [], "b": ["a"], "c": ["b"], "d": ["a", "c"]}
ergebnis = aufruf(stufen, tief)
assert ergebnis == [["a"], ["b"], ["c"], ["d"]], (
    f"stufen({tief}) ergibt {ergebnis!r}, erwartet war [['a'], ['b'], ['c'], ['d']].\n"
    "Tipp: d braucht auch c und darf erst in die Stufe nach c."
)

# stufen ohne Module
ergebnis = aufruf(stufen, {})
assert ergebnis == [], f"stufen({{}}) ergibt {ergebnis!r}, erwartet war []."

# stufen: unabhängige Module bilden eine einzige, sortierte Stufe
ergebnis = aufruf(stufen, unabhaengig)
assert ergebnis == [["a", "b", "c"]], f"stufen({unabhaengig}) ergibt {ergebnis!r}, erwartet war [['a', 'b', 'c']]."

# stufen mit Ring: ZyklusFehler mit denselben Modulen
fehler = fehler_von(stufen, RING)
assert isinstance(fehler, ZyklusFehler) and fehler.module == ["bericht", "kasse", "lager"], (
    f"stufen(ring) löst {fehler!r} aus, erwartet war ein ZyklusFehler mit module ['bericht', 'kasse', 'lager']."
)

# Ohne graphlib
assert not verwendet("TopologicalSorter"), "Ihr Code verwendet graphlib.TopologicalSorter. Bauen Sie das Verfahren von Kahn selbst."

# Die Ausgabe des Programms
zeilen = AUSGABE.splitlines()
assert len(zeilen) == 3 and vergleichbar(zeilen[1]) == vergleichbar(str(erwartete_stufen(BEISPIEL))) and vergleichbar(zeilen[2]) == vergleichbar(
    "['bericht', 'kasse', 'lager']"
), f"Ihr Programm gibt aus:\n{AUSGABE}\nerwartet waren Bauplan, Stufen und ['bericht', 'kasse', 'lager']."

# Viele zufällige Graphen ohne Ring
zufall = Zufall(4064)
for _ in range(200):
    graph = zufallsgraph(zufall, zufall.randint(1, 9), zufall.randint(0, 15), False)
    fehler = plan_fehler(aufruf(bauplan, graph), graph)
    assert fehler is None, f"Für {graph}:\n{fehler}"
    ergebnis = aufruf(stufen, graph)
    assert ergebnis == erwartete_stufen(graph), f"stufen({graph}) ergibt {ergebnis!r}, erwartet war {erwartete_stufen(graph)}."

# Viele zufällige Graphen, oft mit Ring
for _ in range(200):
    graph = zufallsgraph(zufall, zufall.randint(1, 7), zufall.randint(0, 8), True)
    betroffen = ohne_platz(graph)
    for funktion in [bauplan, stufen]:
        fehler = fehler_von(funktion, graph)
        if betroffen:
            assert isinstance(fehler, ZyklusFehler) and fehler.module == betroffen, (
                f"{funktion.__name__}({graph}) löst {fehler!r} aus, erwartet war ein ZyklusFehler mit module {betroffen}."
            )
        else:
            assert fehler is None, f"{funktion.__name__}({graph}) löst {fehler!r} aus, obwohl es keinen Ring gibt."

# Obere Grenze: 10 000 Module und 50 000 Abhängigkeiten
graph = zufallsgraph(zufall, 10000, 50000, False)
fehler = plan_fehler(aufruf(bauplan, graph), graph)
assert fehler is None, "Bei 10 000 Modulen stimmt der Bauplan nicht: " + fehler[:300]
ergebnis = aufruf(stufen, graph)
assert isinstance(ergebnis, list) and sum(len(stufe) for stufe in ergebnis) == 10000, "Bei 10 000 Modulen stimmen die Stufen nicht."

# Laufzeit: eine Kette aus 2000 Modulen in O(Module + Abhängigkeiten)
kette = {f"k{nummer}": [f"k{nummer - 1}"] for nummer in range(1999, 0, -1)}
kette["k0"] = []
try:
    _, schritte = zaehle_schritte(bauplan, kette)
except Exception as fehler:
    schritte = f"(Abbruch: {type(fehler).__name__}: {fehler})"
assert isinstance(schritte, int) and schritte <= 30 * 4000, (
    f"Für eine Kette aus 2000 Modulen braucht bauplan {schritte} Schritte, erlaubt sind 30 · (2000 + 1999) ≈ 120000.\n"
    "Tipp: Suchen Sie nicht in jeder Runde alle Module nach einem fertigen ab; senken Sie Zähler und nutzen Sie eine deque."
)

# Laufzeit: stufen bei derselben Kette
try:
    _, schritte = zaehle_schritte(stufen, kette)
except Exception as fehler:
    schritte = f"(Abbruch: {type(fehler).__name__}: {fehler})"
assert isinstance(schritte, int) and schritte <= 30 * 4000, (
    f"Für eine Kette aus 2000 Modulen braucht stufen {schritte} Schritte, erlaubt sind etwa 120000."
)
