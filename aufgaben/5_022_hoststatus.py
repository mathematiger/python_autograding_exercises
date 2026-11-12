"""Aufgabe 5_022 – Hoststatus                                    Stufe 5 ★★★★★

Ein Monitoring-System fragt regelmäßig alle Server ab und merkt sich zu
jedem Hostnamen den letzten Zustand, etwa "ok", "warnung" oder "ausfall".
Die Meldungen kommen aus verschiedenen Werkzeugen, und jedes schreibt die
Namen anders: "WEB1.firma.de", "web1.firma.de." (mit dem Punkt am Ende, den
das DNS für vollständige Namen kennt) oder " web1.firma.de" mit einem
Leerzeichen aus einer CSV-Datei. Für das DNS sind das alles derselbe Host,
denn Hostnamen unterscheiden keine Groß- und Kleinschreibung. Mit einem
gewöhnlichen Dictionary stünde derselbe Server dreimal in der Übersicht.

Vervollständigen Sie die Klasse `Hoststatus`, eine Unterklasse von
collections.abc.MutableMapping, die jeden Schlüssel vor dem Speichern und
vor dem Nachschlagen normalisiert:

- `normalisiere(name)` (eine staticmethod) entfernt Leerzeichen am Anfang
  und Ende, wandelt in Kleinbuchstaben um und entfernt dann einen
  einzelnen Punkt am Ende, falls einer da ist. Ist name kein Text, löst sie
  einen TypeError aus.
- `__init__(self, daten=())` legt ein leeres Mapping an und übernimmt dann
  die Einträge aus daten (einem Dictionary oder einer Folge von Paaren).
- `__getitem__`, `__setitem__` und `__delitem__` arbeiten mit dem
  normalisierten Schlüssel; ein unbekannter Name löst einen KeyError aus.
- `__iter__` liefert die normalisierten Namen in der Reihenfolge, in der
  sie zuerst eingetragen wurden, `__len__` ihre Anzahl.
- `__repr__` liefert z. B. "Hoststatus({'web1.firma.de': 'ok'})".

get, pop, setdefault, update, keys, items, values, in und == schreiben Sie
nicht selbst; die liefert MutableMapping.

    status = Hoststatus({"WEB1.firma.de": "ok"})
    status["web1.firma.de."] = "warnung"
    status[" Web1.Firma.DE"]          →  "warnung"
    len(status)                       →  1
    "DB2.firma.de" in status          →  False
    status.setdefault("DB2.firma.de.", "ok")  →  "ok"
    list(status)                      →  ['web1.firma.de', 'db2.firma.de']
    status == {"web1.firma.de": "warnung", "db2.firma.de": "ok"}  →  True

Grenzen: Ein Schlüssel ist ein Text aus Buchstaben, Ziffern, "." und "-",
umgeben von höchstens drei Leerzeichen auf jeder Seite, mit höchstens einem
Punkt am Ende; nach dem Normalisieren ist er nicht leer. Er kann aber auch
etwas anderes als ein Text sein (eine Zahl, None), dann gibt es einen
TypeError, auch bei in und get. Die Werte sind beliebig. Es gibt bis zu
10**5 Einträge.

Hintergrund: Wie bei Sequenzen (Aufgabe 5_021) gibt es für Mappings eine
abstrakte Basisklasse. collections.abc.Mapping verlangt __getitem__,
__iter__ und __len__ und liefert dafür __contains__, keys, items, values,
get und __eq__. MutableMapping verlangt zusätzlich __setitem__ und
__delitem__ und liefert pop, popitem, clear, update und setdefault dazu.
Alle Mixin-Methoden laufen über die fünf Grundmethoden; normalisiert man
dort, ist jede geerbte Methode automatisch richtig:

    status.get("WEB1.firma.de")
    → Mapping.get ruft self["WEB1.firma.de"] auf
    → Ihr __getitem__ normalisiert und schlägt "web1.firma.de" nach

get und in fangen dabei nur einen KeyError ab; den liefern Sie für
unbekannte Namen. Ein TypeError für einen falschen Typ geht dagegen weiter,
so wie [1] in {} bei einem echten Dictionary.

Warum nicht einfach von dict erben? Die Methoden von dict sind in C
geschrieben und rufen Ihre überschriebenen Methoden nicht auf: dict.get,
dict.update, setdefault und der Konstruktor gehen an einem eigenen
__setitem__ oder __getitem__ vorbei. Man müsste jede Methode einzeln
überschreiben und vergisst leicht eine. Mit MutableMapping speichert man die
Daten stattdessen in einem gewöhnlichen Dictionary als Attribut
(Komposition) und muss nur die fünf Grundmethoden schreiben:

    class Mapping(MutableMapping):
        def __init__(self):
            self._daten = {}

        def __getitem__(self, schluessel):
            return self._daten[...]

Ein Dictionary merkt sich die Reihenfolge, in der Schlüssel zum ersten Mal
eingetragen wurden; ein Überschreiben ändert sie nicht.
"""

from collections.abc import MutableMapping


class Hoststatus(MutableMapping):
    """Zustand je Host; Hostnamen ohne Rücksicht auf Groß- und Kleinschreibung und Punkt am Ende."""

    @staticmethod
    def normalisiere(name):
        """Gibt den Hostnamen ohne Leerzeichen außen, in Kleinbuchstaben und ohne Punkt am Ende zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __init__(self, daten=()):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __getitem__(self, name):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __setitem__(self, name, wert):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __delitem__(self, name):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __repr__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


status = Hoststatus({"WEB1.firma.de": "ok"})
status["web1.firma.de."] = "warnung"
status.setdefault("DB2.firma.de.", "ok")
print(status)
print(status[" Web1.Firma.DE"], "DB2.firma.de" in status)
