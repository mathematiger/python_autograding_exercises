"""Aufgabe 5_032 – Schnittstellentypen                           Stufe 5 ★★★★★

Ein Team dokumentiert die Webschnittstelle seiner Anwendung. Zu jeder
Antwort der Schnittstelle soll in der Dokumentation eine kurze
Typbeschreibung stehen, die aus einer Beispielantwort automatisch
erzeugt wird. Die Beispielantwort ist ein verschachtelter Python-Wert,
wie er aus json.loads kommt, und die Beschreibung benutzt die Namen aus
JSON:

    None   →  "null"          True / False  →  "boolean"
    3      →  "integer"       2.5           →  "number"
    "abc"  →  "string"

Eine Liste (oder ein Tupel) wird zu "array<…>" mit der Beschreibung
ihrer Elemente in den spitzen Klammern; haben die Elemente verschiedene
Beschreibungen, stehen alle verschiedenen durch | getrennt in der
Reihenfolge ihres ersten Auftretens. Eine leere Liste ist "array<>".
Ein Dictionary wird zu "object{schlüssel: beschreibung, …}" in der
Reihenfolge seiner Schlüssel, ein leeres zu "object{}". Für jeden
anderen Typ gibt es einen TypeError, dessen Meldung den Namen des Typs
nennt.

Schreiben Sie `beschreibe(wert)` mit functools.singledispatch: Die
Grundfunktion löst den TypeError aus, und für jeden Typ registrieren
Sie eine eigene Fassung. So können andere Teams später mit
beschreibe.register eigene Typen ergänzen, ohne Ihren Code zu ändern.

    beschreibe({"id": 7, "tags": ["a", "b"], "aktiv": True})
        →  "object{id: integer, tags: array<string>, aktiv: boolean}"
    beschreibe([1, 2.5, None, 3])     →  "array<integer|number|null>"
    beschreibe(())                    →  "array<>"
    beschreibe({1, 2})                →  TypeError, Meldung enthält "set"

Grenzen: Werte sind bis zu 50 Ebenen tief verschachtelt und haben
zusammen bis zu 100 000 Bestandteile. Schlüssel von Dictionaries sind
Texte. Unterklassen der genannten Typen werden wie ihr Grundtyp
beschrieben, außer es ist für sie eine eigene Fassung registriert.

Hintergrund: In anderen Sprachen kann man mehrere Funktionen gleichen
Namens schreiben, die sich nur im Typ des Parameters unterscheiden
(Überladen). In Python macht das functools.singledispatch: Man schreibt
eine Grundfunktion und hängt mit register Fassungen für einzelne Typen
an. Beim Aufruf schaut singledispatch auf den Typ des ersten Arguments
und ruft die passende Fassung auf:

    from functools import singledispatch

    @singledispatch
    def groesse(wert):
        raise TypeError(f"unbekannt: {type(wert).__name__}")

    @groesse.register
    def _(wert: str):
        return len(wert)

    @groesse.register(list)
    @groesse.register(tuple)
    def _(wert):
        return sum(groesse(teil) for teil in wert)

    groesse(["ab", ("c", "def")])   →  6

Die Fassung findet register entweder über die Typannotation des ersten
Parameters (wert: str) oder über den Typ in Klammern; mehrere register
übereinander melden dieselbe Fassung für mehrere Typen an. Der Name der
Fassungen ist egal, üblich ist _. Gibt es für einen Typ keine eigene
Fassung, sucht singledispatch entlang der Elternklassen (Aufgabe 3_042)
und nimmt die nächste registrierte, am Ende die Grundfunktion für
object. Das ist hier wichtig: bool ist eine Unterklasse von int, True
ist also auch ein int. Wer nur int registriert, bekommt für True die
Beschreibung "integer". Registriert man bool zusätzlich, gewinnt diese
speziellere Fassung. Für None registriert man dessen Typ, type(None).

Mit beschreibe.registry sieht man alle registrierten Typen, mit
beschreibe.dispatch(typ) die Fassung, die für einen Typ gewählt würde.
Die Fassungen dürfen beschreibe selbst aufrufen, für die Teile eines
Werts.
"""

from functools import singledispatch


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(beschreibe({"id": 7, "tags": ["a", "b"], "aktiv": True}))
print(beschreibe([1, 2.5, None, 3]))
