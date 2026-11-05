# Automatisch erzeugt aus lehrkraft/muster/4_017_backlog.py - nicht von Hand ändern.
# vorlage-hash: ca8e291c457205af
# text-hash: 1a5a979f9099fc52
# thema: programmaufbau
# inhalt: TypeVar, generische Funktionen

import typing


def form(typ, namen):
    """Bringt eine Annotation in vergleichbare Form; jede TypeVar wird zu "T1", "T2", … in der Reihenfolge ihres Auftretens."""
    if isinstance(typ, typing.TypeVar):
        if typ not in namen:
            namen[typ] = f"T{len(namen) + 1}"
        return namen[typ]
    herkunft = typing.get_origin(typ)
    if herkunft is None:
        return typ
    return (herkunft, tuple(form(teil, namen) for teil in typing.get_args(typ)))


def annotationen(funktion):
    """Gibt die Annotationen der Funktion in vergleichbarer Form zurück, bei einem Fehler dessen Text."""
    try:
        hinweise = typing.get_type_hints(funktion)
    except Exception as fehler:
        return f"nicht lesbar ({fehler})"
    namen = {}
    return {name: form(typ, namen) for name, typ in hinweise.items()}


def gefunden(funktion):
    """Gibt die Annotationen lesbar zurück, so wie Python sie kennt."""
    try:
        return typing.get_type_hints(funktion)
    except Exception as fehler:
        return f"nicht lesbar ({fehler})"


# erstes_oder ist mit einer Typvariablen annotiert
ergebnis = annotationen(erstes_oder)
erwartet = {"eintraege": (list, ("T1",)), "standard": "T1", "return": "T1"}
if isinstance(ergebnis, dict) and ergebnis.get("return") is typing.Any:
    tipp = "Tipp: Mit Any geht verloren, dass derselbe Typ herauskommt; legen Sie T = TypeVar(\"T\") an."
else:
    tipp = "Tipp: Alle drei Stellen bekommen dieselbe Typvariable: list[T], T und -> T."
assert ergebnis == erwartet, (
    f"Die Annotationen von erstes_oder sind {gefunden(erstes_oder)}; erwartet war eintraege: list[T], "
    f"standard: T und Rückgabe T, mit derselben Typvariablen T = TypeVar(\"T\").\n{tipp}"
)

# in_sprints ist mit einer Typvariablen annotiert
ergebnis = annotationen(in_sprints)
erwartet = {"eintraege": (list, ("T1",)), "groesse": int, "return": (list, ((list, ("T1",)),))}
assert ergebnis == erwartet, (
    f"Die Annotationen von in_sprints sind {gefunden(in_sprints)}; erwartet war eintraege: list[T], "
    "groesse: int und Rückgabe list[list[T]], mit derselben Typvariablen T.\n"
    "Tipp: Eine Liste von Listen mit Einträgen vom Typ T schreibt man list[list[T]]."
)

# gruppiere ist mit zwei verschiedenen Typvariablen annotiert
ergebnis = annotationen(gruppiere)
erwartet = {"paare": (list, ((tuple, ("T1", "T2")),)), "return": (dict, ("T1", (list, ("T2",))))}
if isinstance(ergebnis, dict) and ergebnis.get("paare") == (list, ((tuple, ("T1", "T1")),)):
    tipp = "Tipp: Schlüssel und Werte dürfen verschiedene Typen haben; dafür braucht es zwei Typvariablen, etwa K und V."
else:
    tipp = "Tipp: paare: list[tuple[K, V]] und -> dict[K, list[V]] mit K = TypeVar(\"K\") und V = TypeVar(\"V\")."
assert ergebnis == erwartet, (
    f"Die Annotationen von gruppiere sind {gefunden(gruppiere)}; erwartet war paare: list[tuple[K, V]] "
    f"und Rückgabe dict[K, list[V]] mit zwei verschiedenen Typvariablen K und V.\n{tipp}"
)

# Jede Typvariable heißt so wie die Variable, in der sie steht
falsch_benannt = []
for funktion in [erstes_oder, in_sprints, gruppiere]:
    hinweise = gefunden(funktion)
    for typ in hinweise.values() if isinstance(hinweise, dict) else []:
        for teil in [typ, *typing.get_args(typ)] + [t for a in typing.get_args(typ) for t in typing.get_args(a)]:
            if isinstance(teil, typing.TypeVar) and globals().get(teil.__name__) is not teil:
                falsch_benannt.append(teil.__name__)
assert falsch_benannt == [], (
    f"Die Typvariablen {sorted(set(falsch_benannt))} stehen nicht in einer Variablen gleichen Namens.\n"
    'Tipp: Schreiben Sie T = TypeVar("T"), nicht T = TypeVar("X"); mypy verlangt, dass beide Namen übereinstimmen.'
)

# erstes_oder aus dem Beispiel
ergebnis = (erstes_oder(["PRJ-17", "PRJ-4"], "leer"), erstes_oder([], 0))
assert ergebnis == ("PRJ-17", 0), (
    f'erstes_oder(["PRJ-17", "PRJ-4"], "leer") und erstes_oder([], 0) ergeben {ergebnis!r}, erwartet war ("PRJ-17", 0).'
)

# Auch Einträge wie 0, "" und None sind echte erste Einträge
for eintraege, standard, erwartet in [([0, 5], 9, 0), (["", "x"], "leer", ""), ([None], "leer", None), ([(1, 2)], (0, 0), (1, 2))]:
    ergebnis = erstes_oder(eintraege, standard)
    assert ergebnis == erwartet and type(ergebnis) is type(erwartet), (
        f"erstes_oder({eintraege!r}, {standard!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Prüfen Sie, ob die Liste leer ist, nicht ob der erste Eintrag wahr ist (eintraege[0] or standard geht nicht)."
    )

# Bei leerer Liste kommt genau das Objekt standard zurück
standard = ["Platzhalter"]
ergebnis = erstes_oder([], standard)
assert ergebnis is standard, f"erstes_oder([], standard) ergibt {ergebnis!r}; erwartet war das Objekt standard selbst."

# in_sprints aus dem Beispiel
ergebnis = in_sprints([5, 3, 8, 2, 1], 2)
assert ergebnis == [[5, 3], [8, 2], [1]], (
    f"in_sprints([5, 3, 8, 2, 1], 2) ergibt {ergebnis!r}, erwartet war [[5, 3], [8, 2], [1]].\n"
    "Tipp: Der letzte Sprint darf kürzer sein; mit eintraege[anfang : anfang + groesse] klappt das von selbst."
)

# Weitere Sprintgrößen, leeres Backlog, genau aufgehend
for eintraege, groesse, erwartet in [
    (["a", "b", "c", "d"], 2, [["a", "b"], ["c", "d"]]),
    (["a", "b", "c"], 1, [["a"], ["b"], ["c"]]),
    (["a", "b", "c"], 3, [["a", "b", "c"]]),
    (["a", "b", "c"], 10**9, [["a", "b", "c"]]),
    ([], 4, []),
    ([None, 0], 1, [[None], [0]]),
]:
    ergebnis = in_sprints(eintraege, groesse)
    assert ergebnis == erwartet, f"in_sprints({eintraege!r}, {groesse}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Eine Sprintgröße unter 1 löst ValueError aus
for groesse in [0, -1, -(10**9)]:
    try:
        in_sprints([1, 2, 3], groesse)
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    except Exception as ausnahme:
        fehler = f"stattdessen {type(ausnahme).__name__}"
    assert isinstance(fehler, ValueError), (
        f"in_sprints([1, 2, 3], {groesse}) muss einen ValueError auslösen; bekommen: {fehler!r}.\n"
        "Tipp: Prüfen Sie groesse < 1 am Anfang und lösen Sie mit raise ValueError(...) aus."
    )

# Auch bei leerem Backlog wird die Sprintgröße geprüft
try:
    in_sprints([], 0)
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
assert fehler is not None, "in_sprints([], 0) muss einen ValueError auslösen, auch wenn das Backlog leer ist."

# in_sprints ändert das Backlog nicht
backlog = [1, 2, 3]
sprints = in_sprints(backlog, 2)
sprints[0].append(99)
assert backlog == [1, 2, 3], f"Nach in_sprints und einer Änderung am Ergebnis ist das Backlog {backlog!r}; es soll [1, 2, 3] bleiben."

# gruppiere aus dem Beispiel, Schlüssel in der Reihenfolge des ersten Auftretens
ergebnis = gruppiere([("Ada", "PRJ-17"), ("Bo", "PRJ-4"), ("Ada", "PRJ-9")])
erwartet = {"Ada": ["PRJ-17", "PRJ-9"], "Bo": ["PRJ-4"]}
assert ergebnis == erwartet and list(ergebnis) == ["Ada", "Bo"], (
    f"gruppiere(...) aus dem Beispiel ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Legen Sie beim ersten Auftreten eines Schlüssels eine leere Liste an und hängen Sie jeden Wert mit append an."
)

# Andere Typen, doppelte Paare und leere Liste
for paare, erwartet in [
    ([], {}),
    ([(3, "x"), (1, "y"), (3, "x")], {3: ["x", "x"], 1: ["y"]}),
    ([((1, 2), None), ((1, 2), 0)], {(1, 2): [None, 0]}),
    ([("Bo", 8), ("Ada", 5), ("Bo", 3)], {"Bo": [8, 3], "Ada": [5]}),
]:
    ergebnis = gruppiere(paare)
    assert ergebnis == erwartet and list(ergebnis) == list(erwartet), (
        f"gruppiere({paare!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r} (Schlüssel in dieser Reihenfolge)."
    )

# gruppiere ändert die Eingabe nicht
paare = [("a", 1), ("a", 2)]
gruppiere(paare)
assert paare == [("a", 1), ("a", 2)], f"Nach gruppiere(paare) ist paare {paare!r}; es soll unverändert bleiben."


# Vergleichslösungen: mit Zählern statt Slices und Hilfslisten
def sprints_von_hand(eintraege, groesse):
    """Verteilt die Einträge einzeln auf Sprints, indem es mitzählt."""
    sprints = []
    for nummer, eintrag in enumerate(eintraege):
        if nummer % groesse == 0:
            sprints.append([])
        sprints[-1].append(eintrag)
    return sprints


def gruppen_von_hand(paare):
    """Sucht erst alle Schlüssel in Reihenfolge und sammelt dann die Werte je Schlüssel."""
    schluessel = []
    for links, _ in paare:
        if links not in schluessel:
            schluessel.append(links)
    return {s: [rechts for links, rechts in paare if links == s] for s in schluessel}


# 300 zufällige Backlogs
zufall = Zufall(4017)
for _ in range(300):
    eintraege = [zufall.choice([zufall.randint(0, 13), f"PRJ-{zufall.randint(1, 99)}", None, ""]) for _ in range(zufall.randint(0, 12))]
    groesse = zufall.randint(1, 6)
    standard = zufall.choice([-1, "leer"])
    erwartet = eintraege[0] if eintraege else standard
    ergebnis = erstes_oder(eintraege, standard)
    assert ergebnis == erwartet, f"erstes_oder({eintraege!r}, {standard!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    erwartet = sprints_von_hand(eintraege, groesse)
    ergebnis = in_sprints(eintraege, groesse)
    assert ergebnis == erwartet, f"in_sprints({eintraege!r}, {groesse}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    paare = [(zufall.choice(["Ada", "Bo", "Cem"]), zufall.randint(1, 13)) for _ in range(zufall.randint(0, 10))]
    erwartet = gruppen_von_hand(paare)
    ergebnis = gruppiere(paare)
    assert ergebnis == erwartet and list(ergebnis) == list(erwartet), (
        f"gruppiere({paare!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r} (Schlüssel in dieser Reihenfolge)."
    )

# An der oberen Grenze: 100 000 Einträge
gross = list(range(100000))
sprints = in_sprints(gross, 7)
gruppen = gruppiere([(nummer % 1000, nummer) for nummer in gross])
ok = (
    erstes_oder(gross, -1) == 0
    and len(sprints) == 14286
    and sprints[-1] == [99995, 99996, 99997, 99998, 99999]
    and sum(len(sprint) for sprint in sprints) == 100000
    and list(gruppen) == list(range(1000))
    and len(gruppen[1]) == 100
    and gruppen[2][:2] == [2, 1002]
)
assert ok, (
    "Bei 100 000 Einträgen erwartet: erstes_oder liefert 0, in_sprints(…, 7) 14286 Sprints mit dem letzten "
    "[99995, …, 99999], gruppiere nach Rest durch 1000 die Schlüssel 0 bis 999 mit 100 Werten für 1; "
    f"bekommen: {erstes_oder(gross, -1)!r}, {len(sprints)} Sprints, der letzte {sprints[-1] if sprints else None!r}, "
    f"Schlüssel {list(gruppen)[:5]!r} … ({len(gruppen)} Stück)."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "PRJ-17 0\n[[5, 3], [8, 2], [1]]\n{'Ada': ['PRJ-17', 'PRJ-9'], 'Bo': ['PRJ-4']}"
# Auch ein defaultdict ist ein Dictionary; print zeigt es nur mit anderem Rahmen
mit_defaultdict = erwartete_ausgabe.replace("\n{", "\ndefaultdict(<class 'list'>, {") + ")"
assert AUSGABE in (erwartete_ausgabe, mit_defaultdict), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
