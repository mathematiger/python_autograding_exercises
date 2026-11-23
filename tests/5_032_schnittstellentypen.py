# Automatisch erzeugt aus lehrkraft/muster/5_032_schnittstellentypen.py - nicht von Hand ändern.
# vorlage-hash: 24c59a5f9989f9bb
# text-hash: 504109b1392b8933
# thema: funktionen
# inhalt: functools.singledispatch

import collections
import json


def ergebnis_von(wert):
    """Ruft beschreibe auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return beschreibe(wert)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich(wert):
    """Vergleichslösung mit isinstance-Abfragen statt singledispatch."""
    if wert is None:
        return "null"
    if isinstance(wert, bool):
        return "boolean"
    if isinstance(wert, int):
        return "integer"
    if isinstance(wert, float):
        return "number"
    if isinstance(wert, str):
        return "string"
    if isinstance(wert, (list, tuple)):
        teile = list(dict.fromkeys(vergleich(element) for element in wert))
        return "array<" + "|".join(teile) + ">"
    if isinstance(wert, dict):
        return "object{" + ", ".join(f"{k}: {vergleich(v)}" for k, v in wert.items()) + "}"
    raise TypeError(type(wert).__name__)


def zufallswert(zufall, tiefe):
    """Ein zufälliger JSON-artiger Wert mit höchstens tiefe Ebenen."""
    art = zufall.randint(0, 7 if tiefe > 0 else 4)
    if art == 0:
        return None
    if art == 1:
        return zufall.choice([True, False])
    if art == 2:
        return zufall.randint(-5, 5)
    if art == 3:
        return zufall.choice([0.5, -1.25, 3.0])
    if art == 4:
        return zufall.choice(["", "x", "Name"])
    if art in (5, 6):
        liste = [zufallswert(zufall, tiefe - 1) for _ in range(zufall.randint(0, 4))]
        return tuple(liste) if zufall.random() < 0.3 else liste
    return {f"f{nummer}": zufallswert(zufall, tiefe - 1) for nummer in range(zufall.randint(0, 3))}


# beschreibe ist eine singledispatch-Funktion
assert callable(getattr(beschreibe, "register", None)) and hasattr(beschreibe, "registry"), (
    "beschreibe hat kein register; erwartet war eine Funktion mit @functools.singledispatch darüber."
)

# Die einfachen Typen: Text, ganze Zahl, Kommazahl
ergebnis = [ergebnis_von("abc"), ergebnis_von(3), ergebnis_von(2.5)]
assert ergebnis == ["string", "integer", "number"], (
    f'beschreibe("abc"), beschreibe(3) und beschreibe(2.5) ergeben {ergebnis!r}, erwartet war ["string", "integer", "number"].'
)

# None ist "null"
ergebnis = ergebnis_von(None)
assert ergebnis == "null", f"beschreibe(None) ergibt {ergebnis!r}, erwartet war 'null'.\nTipp: Registrieren Sie type(None)."

# True und False sind "boolean", nicht "integer"
ergebnis = [ergebnis_von(True), ergebnis_von(False)]
assert ergebnis == ["boolean", "boolean"], (
    f"beschreibe(True) und beschreibe(False) ergeben {ergebnis!r}, erwartet war ['boolean', 'boolean'].\n"
    "Tipp: bool ist eine Unterklasse von int; registrieren Sie für bool eine eigene Fassung."
)

# Ein Array mit lauter gleichen Elementen
ergebnis = ergebnis_von(["a", "b", "c"])
assert ergebnis == "array<string>", f'beschreibe(["a", "b", "c"]) ergibt {ergebnis!r}, erwartet war "array<string>".'

# Ein Array mit verschiedenen Elementen: jede Beschreibung einmal, in der Reihenfolge des ersten Auftretens
ergebnis = ergebnis_von([1, 2.5, None, 3, 2.5])
assert ergebnis == "array<integer|number|null>", (
    f"beschreibe([1, 2.5, None, 3, 2.5]) ergibt {ergebnis!r}, erwartet war 'array<integer|number|null>'.\n"
    "Tipp: Hängen Sie eine Beschreibung nur an, wenn sie noch nicht in der Liste steht."
)

# Tupel werden wie Listen beschrieben
ergebnis = ergebnis_von((1, "x"))
assert ergebnis == "array<integer|string>", f'beschreibe((1, "x")) ergibt {ergebnis!r}, erwartet war "array<integer|string>".'

# Leere Liste und leeres Tupel
ergebnis = [ergebnis_von([]), ergebnis_von(())]
assert ergebnis == ["array<>", "array<>"], f"beschreibe([]) und beschreibe(()) ergeben {ergebnis!r}, erwartet war ['array<>', 'array<>']."

# Ein Dictionary im Beispiel
ergebnis = ergebnis_von({"id": 7, "tags": ["a", "b"], "aktiv": True})
assert ergebnis == "object{id: integer, tags: array<string>, aktiv: boolean}", (
    f"beschreibe im Beispiel ergibt {ergebnis!r}, erwartet war 'object{{id: integer, tags: array<string>, aktiv: boolean}}'."
)

# Ein leeres Dictionary
ergebnis = ergebnis_von({})
assert ergebnis == "object{}", f"beschreibe({{}}) ergibt {ergebnis!r}, erwartet war 'object{{}}'."

# Verschachtelt: Arrays aus Objekten, Objekte in Arrays in Objekten
wert = {"kunden": [{"name": "A", "nr": 1}, {"name": "B", "nr": 2}], "seite": {"von": 1, "gesamt": None}, "listen": [[], [1]]}
erwartet = "object{kunden: array<object{name: string, nr: integer}>, seite: object{von: integer, gesamt: null}, listen: array<array<>|array<integer>>}"
ergebnis = ergebnis_von(wert)
assert ergebnis == erwartet, f"beschreibe({wert!r})\n  ergibt   {ergebnis!r}\n  erwartet {erwartet!r}"

# Unbekannte Typen: TypeError mit dem Namen des Typs
meldungen = []
for wert in [{1, 2}, b"bytes", 1 + 2j]:
    try:
        beschreibe(wert)
        meldungen.append(None)
    except TypeError as fehler:
        meldungen.append(str(fehler))
    except Exception as fehler:
        meldungen.append(f"{type(fehler).__name__} statt TypeError")
assert all(m is not None and name in m for m, name in zip(meldungen, ["set", "bytes", "complex"])), (
    f"beschreibe({{1, 2}}), beschreibe(b'bytes') und beschreibe(1 + 2j) ergeben die Meldungen {meldungen!r}; erwartet war "
    "jeweils ein TypeError, dessen Meldung set, bytes bzw. complex enthält.\nTipp: type(wert).__name__ ist der Name des Typs."
)

# Ein unbekannter Typ tief im Inneren löst ebenfalls TypeError aus
try:
    beschreibe({"a": [1, {"b": {3}}]})
    ergebnis = "kein Fehler"
except TypeError as fehler:
    ergebnis = "TypeError"
except Exception as fehler:
    ergebnis = type(fehler).__name__
assert ergebnis == "TypeError", f'beschreibe({{"a": [1, {{"b": {{3}}}}]}}) ergibt {ergebnis}, erwartet war ein TypeError.'

# Für jeden Typ ist eine eigene Fassung registriert
fehlt = [typ.__name__ for typ in [type(None), bool, int, float, str, list, tuple, dict] if typ not in beschreibe.registry]
assert fehlt == [], (
    f"Für {fehlt} ist keine eigene Fassung registriert. Melden Sie jede mit @beschreibe.register an, statt im Rumpf mit "
    "isinstance zu unterscheiden."
)

# Unterklassen werden wie ihr Grundtyp beschrieben
ergebnis = [ergebnis_von(collections.OrderedDict([("x", 1)])), ergebnis_von(collections.namedtuple("Punkt", "x y")(1, 2))]
assert ergebnis == ["object{x: integer}", "array<integer>"], (
    f"beschreibe(OrderedDict(x=1)) und beschreibe(Punkt(1, 2)) ergeben {ergebnis!r}, erwartet war "
    "['object{x: integer}', 'array<integer>']."
)

# Andere Teams können eigene Typen ergänzen, auch in verschachtelten Werten
class Zeitstempel:
    """Ein eigener Typ eines anderen Teams."""


beschreibe.register(Zeitstempel, lambda wert: "string(date-time)")
ergebnis = ergebnis_von({"erstellt": Zeitstempel(), "werte": [Zeitstempel(), 1]})
assert ergebnis == "object{erstellt: string(date-time), werte: array<string(date-time)|integer>}", (
    f"Nach beschreibe.register(Zeitstempel, …) ergibt beschreibe mit Zeitstempeln {ergebnis!r}; erwartet war "
    "'object{erstellt: string(date-time), werte: array<string(date-time)|integer>}'.\n"
    "Tipp: Rufen Sie für die Teile beschreibe(...) selbst auf, nicht eine Ihrer Fassungen direkt."
)

# Die Ausgabe des Programms
erwartet = "object{id: integer, tags: array<string>, aktiv: boolean}\narray<integer|number|null>"
assert AUSGABE == erwartet, f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Werte, verglichen mit einer Lösung aus isinstance-Abfragen
zufall = Zufall(5032)
for runde in range(300):
    wert = zufallswert(zufall, zufall.randint(0, 4))
    ergebnis = ergebnis_von(wert)
    erwartet = vergleich(wert)
    assert ergebnis == erwartet, f"beschreibe({wert!r})\n  ergibt   {ergebnis!r}\n  erwartet {erwartet!r}"

# Werte aus json.loads
text = '{"ok": true, "daten": [{"id": 1, "preis": 9.5, "notiz": null}], "fehler": []}'
ergebnis = ergebnis_von(json.loads(text))
erwartet = "object{ok: boolean, daten: array<object{id: integer, preis: number, notiz: null}>, fehler: array<>}"
assert ergebnis == erwartet, f"beschreibe(json.loads({text!r}))\n  ergibt   {ergebnis!r}\n  erwartet {erwartet!r}"

# Obere Grenze: 50 Ebenen tief
wert = 1
for ebene in range(50):
    wert = [wert] if ebene % 2 else {"x": wert}
ergebnis = ergebnis_von(wert)
erwartet = vergleich(wert)
assert ergebnis == erwartet, f"Bei 50 Ebenen ergibt beschreibe {str(ergebnis)[:80]!r}…, erwartet war {erwartet[:80]!r}…"

# Obere Grenze: 100 000 Bestandteile
wert = [{"id": nummer, "name": "x", "wert": nummer / 2} for nummer in range(25000)]
ergebnis = ergebnis_von(wert)
assert ergebnis == "array<object{id: integer, name: string, wert: number}>", (
    f"Bei 25 000 Objekten mit je drei Feldern ergibt beschreibe {str(ergebnis)[:100]!r}, erwartet war "
    "'array<object{id: integer, name: string, wert: number}>'."
)
