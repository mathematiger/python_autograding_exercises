"""Aufgabe 4_070 – Wartungsplan                                  Stufe 4 ★★★★☆

Der IT-Service eines Krankenhauses plant die regelmäßige Wartung seiner
Geräte: Die USV im Serverraum wird alle 180 Tage geprüft, die
Klimageräte alle 90 Tage, und für jede Wartung sind bestimmte
Kolleginnen und Kollegen zuständig. Das Planungsprogramm hält jede
Wartung als Objekt der vorgegebenen Klasse Wartung mit einem Status aus
der Enum Status. Der Plan soll künftig als JSON-Datei gespeichert
werden, damit ihn auch das neue Ticketsystem lesen kann, und beim
nächsten Start wieder genau so geladen werden.

Ein Plan ist ein Dictionary wie dieses:

    plan = {
        "stand": "2026-11-23",
        "wartungen": [
            Wartung("USV Serverraum", 180, {"Kaya", "Berg"}, Status.GEPLANT),
            Wartung("Klimagerät Büro 2", 90, set()),
        ],
    }

Schreiben Sie vier Funktionen:

- `als_dict(objekt)` ist der Helfer für default= von json: Für eine
  Wartung gibt sie ein Dictionary mit den Schlüsseln "typ" (immer
  "Wartung"), "geraet", "intervall_tage", "zustaendig" (die Namen als
  alphabetisch sortierte Liste) und "status" (der Name des Status, etwa
  "GEPLANT") zurück. Für jedes andere Objekt löst sie einen TypeError
  aus, wie json es von einem solchen Helfer erwartet.
- `aus_dict(daten)` ist der Helfer für object_hook=: Hat das Dictionary
  daten den Eintrag "typ": "Wartung", gibt sie das passende
  Wartung-Objekt zurück (zustaendig wieder als Menge, status als
  Status), sonst daten unverändert.
- `speichern(plan, pfad)` schreibt den Plan als JSON in die Datei pfad
  (UTF-8, Umlaute lesbar statt als \\u-Folgen, eingerückt mit zwei
  Leerzeichen).
- `laden(pfad)` liest die Datei und gibt den Plan zurück, mit
  Wartung-Objekten statt Dictionaries.

    json.dumps(Wartung("USV", 180, {"Kaya", "Berg"}, Status.GEPLANT), default=als_dict)
    →  '{"typ": "Wartung", "geraet": "USV", "intervall_tage": 180,
         "zustaendig": ["Berg", "Kaya"], "status": "GEPLANT"}'
    speichern(plan, "plan.json")
    laden("plan.json") == plan   →  True

Grenzen: Ein Plan ist ein Dictionary mit Texten als Schlüsseln. Seine
Werte sind Texte, ganze Zahlen, Kommazahlen, True, False, None, Listen
und Dictionaries mit Texten als Schlüsseln, beliebig verschachtelt,
dazwischen 0 bis 1000 Wartung-Objekte. Kein anderes Dictionary hat einen
Schlüssel "typ". geraet und die Namen sind nicht leere Texte, auch mit
Umlauten, Anführungszeichen oder Backslashes; intervall_tage ist eine
ganze Zahl von 1 bis 3650, zustaendig hat 0 bis 10 Namen.

Hintergrund: JSON („JavaScript Object Notation“) ist ein Textformat für
Daten, das fast jede Programmiersprache lesen kann. Es kennt nur wenige
Arten von Werten, und das Modul json übersetzt sie so:

    Python                      JSON
    dict (Schlüssel: Texte)     {"a": 1}       Objekt
    list, tuple                 [1, 2]         Array
    str                         "Text"
    int, float                  3, 2.5
    True, False, None           true, false, null

json.dumps(wert) macht daraus einen Text, json.loads(text) wieder
Python-Werte; json.dump(wert, datei) und json.load(datei) arbeiten
direkt mit einer geöffneten Datei (Aufgabe 3_048):

    import json

    text = json.dumps({"name": "Gerät", "werte": (1, 2)})
    text                  →  '{"name": "Ger\\u00e4t", "werte": [1, 2]}'
    json.loads(text)      →  {"name": "Gerät", "werte": [1, 2]}

    with open(pfad, "w", encoding="utf-8") as datei:
        json.dump(daten, datei, ensure_ascii=False, indent=2)

Zwei Dinge gehen dabei verloren: Aus dem Tupel wird eine Liste, und
Schlüssel, die Zahlen sind, kommen als Texte zurück. ensure_ascii=False
schreibt Umlaute als Umlaute statt als \\u00e4, indent=2 setzt jeden
Eintrag auf eine eigene, eingerückte Zeile.

Eigene Objekte, Mengen oder Enums kennt JSON gar nicht; json.dumps
bricht mit einem TypeError ab. Dafür gibt es zwei Haken. default=f ruft
f mit jedem Objekt auf, das json nicht kennt, und schreibt stattdessen,
was f zurückgibt; kann f nichts damit anfangen, löst es selbst einen
TypeError aus. object_hook=g ruft beim Lesen g mit jedem JSON-Objekt auf,
das gerade als Dictionary fertig geworden ist (die inneren zuerst), und
setzt ein, was g zurückgibt:

    def schreiben(objekt):
        if isinstance(objekt, Punkt):
            return {"typ": "Punkt", "x": objekt.x, "y": objekt.y}
        raise TypeError(f"{type(objekt).__name__} kennt JSON nicht")

    def lesen(daten):
        if daten.get("typ") == "Punkt":
            return Punkt(daten["x"], daten["y"])
        return daten

    text = json.dumps([Punkt(1, 2)], default=schreiben)
    json.loads(text, object_hook=lesen)   →  [Punkt(x=1, y=2)]

Der Eintrag "typ" zeigt beim Lesen, welche Dictionaries Objekte waren.
Den Namen eines Enum-Mitglieds liefert status.name, zurück kommt man
mit Status["GEPLANT"] (Aufgabe 4_015). Anders als pickle (kommt in Aufgabe
5_037) kann JSON beim Laden keinen fremden Code ausführen und bleibt für
Menschen lesbar; dafür muss man eigene Typen selbst übersetzen.
"""

import json
from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    """Bearbeitungsstand einer Wartung."""

    OFFEN = "offen"
    GEPLANT = "geplant"
    ERLEDIGT = "erledigt"


@dataclass
class Wartung:
    """Eine regelmäßige Wartung eines Geräts."""

    geraet: str
    intervall_tage: int
    zustaendig: set = field(default_factory=set)
    status: Status = Status.OFFEN


def als_dict(objekt):
    """Übersetzt eine Wartung in ein Dictionary für JSON; andere Objekte ergeben einen TypeError."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def aus_dict(daten):
    """Macht aus einem Dictionary mit "typ": "Wartung" wieder eine Wartung, sonst bleibt es."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def speichern(plan, pfad):
    """Schreibt den Plan als JSON (UTF-8, lesbare Umlaute, Einrückung 2) in die Datei pfad."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def laden(pfad):
    """Liest den Plan aus der Datei pfad, mit Wartung-Objekten."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


usv = Wartung("USV", 180, {"Kaya", "Berg"}, Status.GEPLANT)
print(json.dumps(usv, default=als_dict))
