"""Aufgabe 5_022 – Backlog                                       Stufe 5 ★★★★★

Ein Entwicklungsteam schätzt die Einträge seines Product Backlogs (der
geordneten Liste aller offenen Anforderungen) in Story Points, einer
Punkteskala für den Aufwand. Jeder Eintrag hat einen Schlüssel wie "WEB-12".
In den Planungsrunden werden die Schlüssel aber mal klein, mal mit
Leerzeichen eingetippt: "web-12", " WEB-12 ", "Web-12" meinen alle denselben
Eintrag. Außerdem sind als Schätzung nur die Werte der Skala erlaubt. Das
Team will ein Objekt, das sich wie ein Dictionary benutzen lässt, mit [],
in, len, for, get, update, pop, setdefault, items und dict(...), dabei aber
jeden Schlüssel normalisiert (Leerzeichen am Rand weg, Großbuchstaben) und
jede Schätzung prüft. Vervollständigen Sie die Klasse `Schaetzungen`, die
von collections.abc.MutableMapping erbt:

- `__init__(self, daten=(), **weitere)` legt ein leeres internes Dictionary
  an und übernimmt dann daten und weitere mit self.update(...).
- `__getitem__`, `__setitem__` und `__delitem__` normalisieren den Schlüssel
  mit der vorgegebenen Funktion `normalisiere`. `__setitem__` löst einen
  ValueError aus, wenn der Wert nicht in `SKALA` steht (auch bei True, False
  oder 3.0); dann bleibt alles, wie es war. Ein fehlender Schlüssel löst
  bei [] und del einen KeyError aus.
- `__iter__` liefert die normalisierten Schlüssel in der Reihenfolge, in der
  sie zum ersten Mal eingetragen wurden; `__len__` ihre Anzahl.

    punkte = Schaetzungen({"web-12": 5}, app_3=8)
    punkte[" WEB-12 "]        →  5
    punkte["Web-12"] = 13
    "web-12" in punkte        →  True
    dict(punkte)              →  {"WEB-12": 13, "APP_3": 8}
    punkte.get("api-1", 0)    →  0
    punkte["api-1"] = 4       →  ValueError (4 ist kein Wert der Skala)

Grenzen: Schlüssel sind Texte mit 1 bis 30 Zeichen (Buchstaben, Ziffern,
Bindestrich, Unterstrich, am Rand auch Leerzeichen). Werte sind beliebige
Objekte; gültig sind nur die ganzen Zahlen aus SKALA (int, nicht bool). Es
gibt bis zu 100 000 Einträge, und [], in, get und Zuweisung sollen jeweils
O(1) Schritte brauchen.

Hintergrund: Wer ein eigenes Dictionary braucht, denkt zuerst an class
Schaetzungen(dict) und ein überschriebenes __setitem__. Das geht schief:
Die eingebauten Methoden von dict sind in C geschrieben und rufen Ihr
__setitem__ nicht auf. dict.update, dict.setdefault und dict(...) im
Konstruktor tragen die Werte an der Prüfung vorbei ein, und get und in
normalisieren den Schlüssel nicht:

    class Laut(dict):
        def __setitem__(self, k, v):
            super().__setitem__(k.upper(), v)

    d = Laut()
    d["a"] = 1; d.update(b=2)
    d                         →  {'A': 1, 'b': 2}

Die abstrakte Basisklasse collections.abc.MutableMapping ist der saubere
Weg. Sie verlangt genau fünf Methoden, __getitem__, __setitem__,
__delitem__, __iter__ und __len__, und baut alle anderen daraus in Python:
get, __contains__, keys, items, values, __eq__, pop, popitem, clear, update
und setdefault. Weil diese Mixin-Methoden immer über Ihre fünf Methoden
gehen, gelten Normalisierung und Prüfung überall, ohne dass man sie
mehrfach schreibt. Die Daten selbst hält man in einem gewöhnlichen
Dictionary als Attribut (Komposition statt Vererbung):

    from collections.abc import MutableMapping

    class Klein(MutableMapping):
        def __init__(self):
            self._daten = {}
        def __getitem__(self, k):
            return self._daten[k.lower()]
        def __setitem__(self, k, v):
            self._daten[k.lower()] = v
        def __delitem__(self, k):
            del self._daten[k.lower()]
        def __iter__(self):
            return iter(self._daten)
        def __len__(self):
            return len(self._daten)

get und in funktionieren, weil die Mixin-Methoden __getitem__ aufrufen und
einen KeyError als „nicht vorhanden“ deuten; darum muss ein fehlender
Schlüssel genau einen KeyError auslösen. Ein Python-Dictionary merkt sich
die Reihenfolge des ersten Eintragens; überschreibt man einen Wert, bleibt
der Schlüssel an seiner Stelle.
"""

from collections.abc import MutableMapping

SKALA = (0, 1, 2, 3, 5, 8, 13, 21)


def normalisiere(schluessel):
    """Entfernt Leerzeichen am Rand und schreibt den Schlüssel groß."""
    return schluessel.strip().upper()


class Schaetzungen(MutableMapping):
    """Story-Point-Schätzungen je Backlog-Eintrag mit normalisierten Schlüsseln."""

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
        return f"Schaetzungen({dict(self.items())!r})"


punkte = Schaetzungen({"web-12": 5}, app_3=8)
punkte["Web-12"] = 13
print(punkte["web-12"])
