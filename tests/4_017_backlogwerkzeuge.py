# Automatisch erzeugt aus lehrkraft/muster/4_017_backlogwerkzeuge.py - nicht von Hand ändern.
# vorlage-hash: 5ad8d9f6f7d0be78
# text-hash: 7c4b751034e664a0
# thema: programmaufbau
# inhalt: TypeVar, generische Funktionen

import types
import typing


def form(typ):
    """Bringt eine Annotation in eine vergleichbare Form; Typvariablen werden zu ("Typvariable", Name)."""
    if isinstance(typ, typing.TypeVar):
        return ("Typvariable", typ.__name__)
    if isinstance(typ, list):
        return ("Liste", tuple(form(teil) for teil in typ))
    herkunft = typing.get_origin(typ)
    if herkunft is None:
        return typ
    teile = [form(teil) for teil in typing.get_args(typ)]
    if herkunft in (typing.Union, types.UnionType):
        return ("oder", frozenset(teile))
    return (herkunft, tuple(teile))


def annotationen(funktion):
    """Gibt die Annotationen der Funktion in vergleichbarer Form zurück, bei einem Fehler dessen Text."""
    try:
        return {name: form(typ) for name, typ in typing.get_type_hints(funktion).items()}
    except Exception as fehler:
        return f"nicht lesbar ({fehler})"


def roh(funktion):
    """Gibt die Annotationen lesbar für eine Fehlermeldung zurück."""
    try:
        return typing.get_type_hints(funktion)
    except Exception as fehler:
        return f"nicht lesbar ({fehler})"


def typvariablen(funktion):
    """Gibt die Namen aller Typvariablen in den Annotationen der Funktion zurück."""
    try:
        hinweise = typing.get_type_hints(funktion)
    except Exception:
        return set()
    gefunden = set()
    offen = list(hinweise.values())
    while offen:
        typ = offen.pop()
        if isinstance(typ, typing.TypeVar):
            gefunden.add(typ.__name__)
        elif isinstance(typ, list):
            offen.extend(typ)
        else:
            offen.extend(typing.get_args(typ))
    return gefunden


T_ = ("Typvariable", "T")
K_ = ("Typvariable", "K")
CALLABLE = typing.get_origin(Callable[[int], int])

# T und K sind Typvariablen
ergebnis = (type(globals().get("T")).__name__, type(globals().get("K")).__name__)
assert isinstance(globals().get("T"), typing.TypeVar) and isinstance(globals().get("K"), typing.TypeVar) and T.__name__ == "T" and K.__name__ == "K", (
    f"T und K sind vom Typ {ergebnis[0]} und {ergebnis[1]}; erwartet waren zwei Typvariablen.\n"
    'Tipp: Schreiben Sie oben T = TypeVar("T") und K = TypeVar("K").'
)

# erstes_passendes ist mit T annotiert, die Rückgabe kann None sein
ergebnis = annotationen(erstes_passendes)
erwartet = {"elemente": (list, (T_,)), "bedingung": (CALLABLE, (("Liste", (T_,)), bool)), "return": ("oder", frozenset({T_, type(None)}))}
assert ergebnis == erwartet, (
    f"Die Annotationen von erstes_passendes sind {roh(erstes_passendes)}; erwartet waren "
    "elemente: list[T], bedingung: Callable[[T], bool] und die Rückgabe T | None.\n"
    "Tipp: Mit Any oder object statt T ginge die Verbindung zwischen Eingabe und Ergebnis verloren."
)

# gruppiere ist mit T und K annotiert
ergebnis = annotationen(gruppiere)
erwartet = {"elemente": (list, (T_,)), "schluessel": (CALLABLE, (("Liste", (T_,)), K_)), "return": (dict, (K_, (list, (T_,))))}
assert ergebnis == erwartet, (
    f"Die Annotationen von gruppiere sind {roh(gruppiere)}; erwartet waren elemente: list[T], "
    "schluessel: Callable[[T], K] und die Rückgabe dict[K, list[T]].\n"
    "Tipp: Schlüssel und Elemente können verschiedene Typen haben; darum braucht es zwei Typvariablen."
)

# in_bloecke ist mit T annotiert
ergebnis = annotationen(in_bloecke)
erwartet = {"elemente": (list, (T_,)), "groesse": int, "return": (list, ((list, (T_,)),))}
assert ergebnis == erwartet, (
    f"Die Annotationen von in_bloecke sind {roh(in_bloecke)}; erwartet waren elemente: list[T], groesse: int "
    "und die Rückgabe list[list[T]]."
)

# Keine Funktion benutzt Any
benutzt_any = [f.__name__ for f in (erstes_passendes, gruppiere, in_bloecke) if "Any" in str(roh(f))]
assert benutzt_any == [], f"{benutzt_any} benutzen Any; verwenden Sie stattdessen die Typvariablen T und K."

backlog = [("Login", 5), ("Suche", 8), ("Export", 3), ("Hilfe", 1)]

# erstes_passendes aus dem Beispiel
ergebnis = (erstes_passendes(backlog, lambda story: story[1] >= 8), erstes_passendes(backlog, lambda story: story[1] > 13))
assert ergebnis == (("Suche", 8), None), (
    f"erstes_passendes(backlog, …) ergibt {ergebnis!r} für die beiden Beispiele, erwartet war (('Suche', 8), None)."
)

# erstes_passendes mit anderen Typen und am Rand
for elemente, bedingung, erwartet in [
    ([], lambda x: True, None),
    ([0, 0, 3], lambda x: x == 0, 0),
    (["", "b", "c"], lambda x: x == "", ""),
    ([1, 2, 3], lambda x: x > 2, 3),
    ([[], [1]], lambda x: len(x) == 1, [1]),
]:
    ergebnis = erstes_passendes(elemente, bedingung)
    assert ergebnis == erwartet and type(ergebnis) is type(erwartet), (
        f"erstes_passendes({elemente}, …) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Auch 0 oder ein leerer Text können das gesuchte Element sein; geben Sie das Element selbst zurück."
    )

# bedingung wird nach dem ersten Treffer nicht mehr aufgerufen
aufrufe = []
erstes_passendes([4, 7, 9, 11], lambda x: aufrufe.append(x) or x > 5)
assert aufrufe == [4, 7], (
    f"Bei erstes_passendes([4, 7, 9, 11], x > 5) wurde bedingung mit {aufrufe} aufgerufen, erwartet war nur mit [4, 7].\n"
    "Tipp: Geben Sie das Element zurück, sobald bedingung True liefert."
)

# gruppiere aus dem Beispiel, mit Reihenfolge der Schlüssel
ergebnis = gruppiere(["Analyse", "Entwurf", "Abnahme", "Einführung"], lambda text: text[0])
erwartet = {"A": ["Analyse", "Abnahme"], "E": ["Entwurf", "Einführung"]}
assert ergebnis == erwartet and list(ergebnis) == ["A", "E"], f"gruppiere(...) aus dem Beispiel ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# gruppiere nach Story Points, Schlüssel in der Reihenfolge ihres ersten Vorkommens
ergebnis = gruppiere(backlog + [("Druck", 5)], lambda story: story[1] % 2)
erwartet = {1: [("Login", 5), ("Export", 3), ("Hilfe", 1), ("Druck", 5)], 0: [("Suche", 8)]}
assert ergebnis == erwartet and list(ergebnis) == [1, 0], (
    f"gruppiere(backlog + [('Druck', 5)], Story Points % 2) ergibt {ergebnis!r}, erwartet war {erwartet!r} "
    "mit den Schlüsseln in der Reihenfolge [1, 0]."
)

# gruppiere ohne Elemente
ergebnis = gruppiere([], lambda x: x)
assert ergebnis == {}, f"gruppiere([], …) ergibt {ergebnis!r}, erwartet war {{}}."

# in_bloecke aus dem Beispiel und weitere Größen
for elemente, groesse, erwartet in [
    (backlog, 3, [backlog[:3], backlog[3:]]),
    (backlog, 4, [backlog]),
    (backlog, 10**6, [backlog]),
    (backlog, 1, [[story] for story in backlog]),
    (backlog, 2, [backlog[:2], backlog[2:]]),
    ([], 3, []),
]:
    ergebnis = in_bloecke(elemente, groesse)
    assert ergebnis == erwartet, f"in_bloecke({elemente}, {groesse}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# in_bloecke mit groesse unter 1: ValueError
for groesse in [0, -1, -10]:
    try:
        in_bloecke([1, 2], groesse)
        art = None
    except Exception as fehler:
        art = type(fehler).__name__
    assert art == "ValueError", f"in_bloecke([1, 2], {groesse}) soll einen ValueError auslösen; ausgelöst wurde {art}."

# Die Eingaben bleiben unverändert
liste = [3, 1, 2]
erstes_passendes(liste, lambda x: x < 2)
gruppiere(liste, lambda x: x % 2)
bloecke = in_bloecke(liste, 2)
bloecke[0].append(99)
assert liste == [3, 1, 2], f"Nach den Aufrufen ist die Liste {liste!r}; sie soll unverändert [3, 1, 2] sein."

# 300 zufällige Listen, verglichen mit einfachen Vergleichslösungen
zufall = Zufall(4017)
for _ in range(300):
    elemente = [zufall.randint(-5, 5) for _ in range(zufall.randint(0, 12))]
    grenze = zufall.randint(-6, 6)
    treffer = [x for x in elemente if x > grenze]
    erwartet = treffer[0] if treffer else None
    ergebnis = erstes_passendes(elemente, lambda x: x > grenze)
    assert ergebnis == erwartet, f"erstes_passendes({elemente}, x > {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    teiler = zufall.randint(1, 4)
    erwartet = {}
    for x in elemente:
        if x % teiler not in erwartet:
            erwartet[x % teiler] = [y for y in elemente if y % teiler == x % teiler]
    ergebnis = gruppiere(elemente, lambda x: x % teiler)
    assert ergebnis == erwartet and list(ergebnis) == list(erwartet), (
        f"gruppiere({elemente}, x % {teiler}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )
    groesse = zufall.randint(1, 5)
    ergebnis = in_bloecke(elemente, groesse)
    zusammen = [x for block in ergebnis for x in block]
    laengen_ok = all(len(block) == groesse for block in ergebnis[:-1]) and (not ergebnis or 1 <= len(ergebnis[-1]) <= groesse)
    assert zusammen == elemente and laengen_ok, (
        f"in_bloecke({elemente}, {groesse}) ergibt {ergebnis!r}; erwartet waren Blöcke mit je {groesse} Elementen "
        "(der letzte darf kürzer sein), die hintereinander wieder die Liste ergeben."
    )

# An der oberen Grenze: 100 000 Stories
gross = [(f"Story {nummer}", nummer % 13) for nummer in range(100000)]
ergebnis_erstes = erstes_passendes(gross, lambda story: story[0] == "Story 99999")
ergebnis_gruppen = gruppiere(gross, lambda story: story[1])
ergebnis_bloecke = in_bloecke(gross, 30)
assert (
    ergebnis_erstes == ("Story 99999", 99999 % 13)
    and list(ergebnis_gruppen) == list(range(13))
    and len(ergebnis_gruppen[0]) == len(range(0, 100000, 13))
    and len(ergebnis_bloecke) == 3334
    and len(ergebnis_bloecke[-1]) == 10
), (
    f"Bei 100 000 Stories ergibt erstes_passendes {ergebnis_erstes!r}, gruppiere {len(ergebnis_gruppen)} Gruppen und "
    f"in_bloecke(…, 30) {len(ergebnis_bloecke)} Blöcke; erwartet waren ('Story 99999', {99999 % 13}), 13 Gruppen und 3334 Blöcke."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "('Suche', 8)\n"
    "{'A': ['Analyse', 'Abnahme'], 'E': ['Entwurf', 'Einführung']}\n"
    "[[('Login', 5), ('Suche', 8), ('Export', 3)], [('Hilfe', 1)]]"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
