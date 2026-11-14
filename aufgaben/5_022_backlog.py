"""Aufgabe 5_022 – Backlog                                      Stufe 5 ★★★★★

Ein agiles Team führt sein Product Backlog als Zuordnung von
Story-Kennungen zu Story Points, der geschätzten Größe einer Anforderung.
Die Kennungen haben die Form PROJ-17, werden aber von Hand eingetippt,
einmal als "proj-17", einmal als " PROJ-17 " mit Leerzeichen. In einem
normalen Dictionary wären das drei verschiedene Stories, und die Planung des
nächsten Sprints rechnet mit doppelten Einträgen.

Vervollständigen Sie die Klasse `Backlog`, die sich wie ein Dictionary
verhält, aber jede Kennung vor dem Speichern und vor dem Nachschlagen
normalisiert: Leerzeichen am Anfang und Ende entfernen, dann alles in
Großbuchstaben. Sie erbt von collections.abc.MutableMapping.

- `__setitem__(kennung, punkte)` speichert die Story Points unter der
  normalisierten Kennung. Ist die Kennung kein Text, löst es einen
  TypeError aus; sind die Punkte keine ganze Zahl ≥ 0 (True und False
  zählen nicht als Zahl), einen ValueError. Dann bleibt alles unverändert.
- `__getitem__(kennung)` und `__delitem__(kennung)` normalisieren ebenso;
  fehlt die Kennung, lösen sie einen KeyError aus (auch, wenn sie kein Text
  ist).
- `__iter__` liefert die normalisierten Kennungen in der Reihenfolge, in der
  sie zum ersten Mal eingetragen wurden; `__len__` ihre Anzahl.
- `__init__(eintraege=())` legt den leeren Speicher an und trägt dann alle
  Einträge ein (ein Dictionary oder eine Folge von Paaren).

    backlog = Backlog({"proj-1": 5, "PROJ-2": 3})
    backlog[" Proj-1 "] = 8
    backlog["PROJ-1"]            →  8
    "proj-2" in backlog          →  True      (von MutableMapping geerbt)
    list(backlog)                →  ["PROJ-1", "PROJ-2"]
    sum(backlog.values())        →  11
    backlog.pop("proj-2")        →  3
    backlog["PROJ-9"] = -1       →  ValueError

Grenzen: Kennungen sind Texte mit 0 bis 50 Zeichen oder andere Objekte
(dann TypeError beziehungsweise KeyError, siehe oben). Ein Backlog hat bis zu
100 000 Einträge. Jeder Zugriff soll O(1) Schritte brauchen, also nicht
alle Einträge durchsuchen.

Hintergrund: Von dict zu erben ist verlockend, aber eine Falle: Die
eingebauten Methoden von dict wie get, update, setdefault, pop oder der
Konstruktor rufen das eigene __setitem__ oder __getitem__ nicht auf, weil sie
in C direkt auf den Speicher zugreifen. Eine Unterklasse, die nur
__setitem__ überschreibt, normalisiert also bei b[k] = v, aber nicht bei
b.update(...).

collections.abc.MutableMapping geht den umgekehrten Weg: Die Klasse
schreibt nur fünf Grundmethoden selbst, __getitem__, __setitem__,
__delitem__, __iter__ und __len__, und bekommt alles andere geerbt: get,
pop, popitem, setdefault, update, clear, keys, values, items, in und ==.
Diese geerbten Methoden sind in Python geschrieben und rufen ausschließlich
die fünf Grundmethoden auf, also wirkt die Normalisierung überall.

    from collections.abc import MutableMapping

    class Kleinschreibung(MutableMapping):
        def __init__(self):
            self._daten = {}
        def __getitem__(self, schluessel):
            return self._daten[schluessel.lower()]
        def __setitem__(self, schluessel, wert):
            self._daten[schluessel.lower()] = wert
        def __delitem__(self, schluessel):
            del self._daten[schluessel.lower()]
        def __iter__(self):
            return iter(self._daten)
        def __len__(self):
            return len(self._daten)

    k = Kleinschreibung()
    k.update({"ABC": 1})
    k.get("abc")      →  1

Den Speicher bildet ein ganz normales Dictionary im Attribut _daten
(Komposition statt Vererbung). Der Unterstrich sagt: Das ist ein
Implementierungsdetail, von außen nicht anfassen. Wichtig ist, dass
__getitem__ bei einem fehlenden Schlüssel einen KeyError auslöst und keinen
anderen Fehler: Die geerbten Methoden get, pop mit Standardwert und in
fangen genau den KeyError ab.
"""

from collections.abc import MutableMapping


class Backlog(MutableMapping):
    """Story-Kennung → Story Points; Kennungen werden normalisiert (strip, upper)."""

    def __init__(self, eintraege=()):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __getitem__(self, kennung):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __setitem__(self, kennung, punkte):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __delitem__(self, kennung):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __repr__(self):
        return f"Backlog({dict(self.items())!r})"


backlog = Backlog({"proj-1": 5, "PROJ-2": 3})
backlog[" Proj-1 "] = 8
print(backlog, "proj-2" in backlog, sum(backlog.values()))
