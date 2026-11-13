"""Aufgabe 5_022 – Backlog mit Ticketschlüsseln                  Stufe 5 ★★★★★

Ein agiles Team schätzt jede Aufgabe im Product Backlog in Story Points,
einer groben Zahl für den Aufwand. Die Aufgaben heißen nach ihrem
Ticketschlüssel, etwa PROJ-42: ein Projektkürzel aus Buchstaben, ein
Bindestrich, eine Nummer. In Mails, Commit-Nachrichten und Tabellen wird
derselbe Schlüssel aber ganz verschieden geschrieben: "proj-42",
" PROJ-042 ", "Proj-42". Ein Werkzeug für die Sprintplanung soll alle
diese Schreibweisen als denselben Schlüssel behandeln.

Vervollständigen Sie die Klasse `Backlog`, ein Dictionary von
Ticketschlüsseln auf Story Points, das jeden Schlüssel mit der vorgegebenen
Funktion `normalisiere` vereinheitlicht. Sie erbt von
collections.abc.MutableMapping. Schreiben Sie:

- `__init__(self, daten=(), **weitere)` legt ein leeres Dictionary an und
  übernimmt daten (ein Dictionary oder eine Folge von Paaren) und weitere
  mit self.update(daten, **weitere).
- `__setitem__(self, schluessel, wert)` speichert wert unter dem
  normalisierten Schlüssel. Ein ungültiger Schlüssel löst den ValueError
  aus normalisiere aus.
- `__getitem__(self, schluessel)` und `__delitem__(self, schluessel)`
  arbeiten mit dem normalisierten Schlüssel. Fehlt er oder ist er
  ungültig, lösen beide einen KeyError aus (keinen ValueError), damit get,
  in, pop und setdefault wie bei einem Dictionary funktionieren.
- `__iter__(self)` liefert die normalisierten Schlüssel in der Reihenfolge,
  in der sie zuerst eingetragen wurden, und `__len__(self)` ihre Anzahl.

    backlog = Backlog({"proj-7": 5}, WEB_3=8)
    backlog[" PROJ-007 "]         →  5
    backlog["Proj-12"] = 3
    list(backlog)                 →  ["PROJ-7", "WEB-3", "PROJ-12"]
    "proj-12" in backlog          →  True
    backlog.get("kein Ticket")    →  None
    backlog.pop("web-03")         →  8
    backlog["ohne Nummer"] = 1    →  ValueError

Grenzen: Ein gültiger Schlüssel ist ein Text aus 1 bis 10 Buchstaben A–Z
(groß oder klein), einem Bindestrich und 1 bis 9 Ziffern, außen dürfen
Leerzeichen stehen. Statt des Bindestrichs ist auch _ erlaubt, damit
Schlüsselwort-Argumente wie WEB_3=8 gehen. Alles
andere, auch Nicht-Texte wie 42 oder None, ist ungültig. Werte sind
beliebig. Es gibt bis zu 100 000 Einträge; jeder Zugriff soll O(1) im
Mittel brauchen.

Hintergrund: Ein eigenes Dictionary von dict abzuleiten liegt nahe, ist
aber eine Falle: dict ist in C geschrieben, und seine Methoden rufen sich
gegenseitig nicht über die Dunder-Methoden auf. Wer in einer Unterklasse
von dict nur __setitem__ überschreibt, hat ein Dictionary, bei dem
d["x"] = 1 normalisiert, d.update(...), d.setdefault(...) und der
Konstruktor dict(...) aber nicht:

    class Klein(dict):
        def __setitem__(self, schluessel, wert):
            super().__setitem__(schluessel.lower(), wert)

    d = Klein({"A": 1})     # __setitem__ wird NICHT aufgerufen
    d.update(B=2)           # auch nicht
    d                       →  {'A': 1, 'B': 2}

collections.abc.MutableMapping (wie Sequence in Aufgabe 5_021) dreht das
um: Man schreibt nur die fünf Grundmethoden __getitem__, __setitem__,
__delitem__, __iter__ und __len__, und alle anderen bekommt man geschenkt,
in Python geschrieben und auf genau diese fünf zurückgeführt: get,
__contains__, keys, items, values, __eq__, pop, popitem, clear, update und
setdefault. Weil update für jedes Paar self[schluessel] = wert ausführt,
läuft jede Schreibweise durch Ihr __setitem__. Die Daten selbst legt man
meist in einem gewöhnlichen dict ab, das als Attribut in der Klasse steht
(Komposition statt Vererbung):

    class Klein(MutableMapping):
        def __init__(self):
            self._daten = {}
        def __getitem__(self, schluessel):
            return self._daten[schluessel.lower()]
        ...

Die geschenkten Methoden verlassen sich auf eine Abmachung: Ein fehlender
Schlüssel meldet sich mit KeyError. get fängt KeyError ab und liefert den
Standardwert, __contains__ macht daraus False, pop und setdefault
entscheiden daran, ob es den Eintrag schon gibt. Ein ValueError würde
dagegen durchgereicht, und backlog.get("Unsinn") bräche ab. Darum fängt
__getitem__ den ValueError aus normalisiere ab und löst stattdessen einen
KeyError aus, am besten mit raise KeyError(schluessel) from None (from
None blendet den ursprünglichen Fehler in der Meldung aus). Bei
__setitem__ ist es umgekehrt richtig, den ValueError durchzulassen: Einen
ungültigen Schlüssel einzutragen ist ein echter Fehler.

Ein gewöhnliches dict merkt sich die Reihenfolge des ersten Eintrags.
Gibt __iter__ einfach iter(self._daten) zurück, übernimmt der Backlog
diese Reihenfolge, und ein späteres Überschreiben ändert sie nicht.
"""

import re
from collections.abc import MutableMapping

_SCHLUESSEL = re.compile(r"\s*([A-Za-z]{1,10})[-_](\d{1,9})\s*")


def normalisiere(schluessel):
    """Einheitliche Schreibweise eines Ticketschlüssels, z. B. ' proj-042 ' → 'PROJ-42'; sonst ValueError."""
    if not isinstance(schluessel, str):
        raise ValueError(f"Ticketschlüssel muss ein Text sein, nicht {schluessel!r}")
    treffer = _SCHLUESSEL.fullmatch(schluessel)
    if treffer is None:
        raise ValueError(f"Ungültiger Ticketschlüssel: {schluessel!r}")
    return f"{treffer.group(1).upper()}-{int(treffer.group(2))}"


class Backlog(MutableMapping):
    """Dictionary von Ticketschlüsseln auf Story Points; jede Schreibweise eines Schlüssels zählt gleich."""

    def __init__(self, daten=(), **weitere):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __getitem__(self, schluessel):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __setitem__(self, schluessel, wert):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __delitem__(self, schluessel):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __repr__(self):
        return f"Backlog({dict(self.items())!r})"


backlog = Backlog({"proj-7": 5}, WEB_3=8)
backlog["Proj-12"] = 3
print(backlog)
print(backlog[" PROJ-007 "], "proj-12" in backlog, backlog.get("kein Ticket"))
