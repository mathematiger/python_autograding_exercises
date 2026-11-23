"""Aufgabe 4_064 – Bauplan                                       Stufe 4 ★★★★☆

Eine Software besteht aus Modulen, und viele Module brauchen andere: Die
Oberfläche liest die Konfiguration, die Datenbankschicht braucht die
Konfiguration und das Protokoll. Ein Werkzeug soll die Module bauen und
testen, und zwar jedes erst, wenn alle Module fertig sind, die es
braucht. Die Abhängigkeiten stehen in einem Dictionary Modul → Liste der
Module, die es braucht:

    abhaengigkeiten = {
        "app": ["datenbank", "oberflaeche"],
        "oberflaeche": ["konfiguration"],
        "datenbank": ["konfiguration", "protokoll"],
        "konfiguration": [],
        "protokoll": [],
    }

Ein guter Entwurf hat keine Ringe, in denen ein Modul über andere
wieder sich selbst braucht; dann lässt sich keines davon zuerst bauen.
Schreiben Sie:

- `ZyklusFehler`, eine Unterklasse von Exception. Ihr Attribut module ist
  die alphabetisch sortierte Liste aller Module, die wegen eines Rings
  keinen Platz bekommen: die im Ring und alle, die davon abhängen. Die
  Meldung nennt diese Module.
- `bauplan(abhaengigkeiten)` gibt eine Liste aller Module zurück, in der
  jedes Modul hinter allen Modulen steht, die es braucht. Gibt es mehrere
  solche Reihenfolgen, ist jede richtig.
- `stufen(abhaengigkeiten)` teilt die Module in Stufen, die der
  Bauserver jeweils gleichzeitig bauen kann: Stufe 0 sind die Module ohne
  Abhängigkeit, Stufe 1 die, deren Abhängigkeiten alle in Stufe 0 liegen,
  Stufe k die, deren Abhängigkeiten alle in früheren Stufen liegen, mit
  mindestens einer in Stufe k - 1. Jede Stufe ist eine alphabetisch
  sortierte Liste.

Gibt es einen Ring, lösen bauplan und stufen einen ZyklusFehler aus.

    bauplan(abhaengigkeiten)  →  ["konfiguration", "protokoll", "oberflaeche", "datenbank", "app"]
                                 (eine von mehreren richtigen Antworten)
    stufen(abhaengigkeiten)   →  [["konfiguration", "protokoll"], ["datenbank", "oberflaeche"], ["app"]]

    ring = {"kasse": ["lager"], "lager": ["kasse"], "bericht": ["kasse"], "hilfe": []}
    bauplan(ring)             →  ZyklusFehler, fehler.module == ["bericht", "kasse", "lager"]

Benutzen Sie dafür nicht das Modul graphlib, und das Dictionary bleibt
unverändert.

Grenzen: 0 bis 10 000 Module mit verschiedenen, nicht leeren Namen,
zusammen 0 bis 50 000 Abhängigkeiten. Jedes Modul in einer Liste ist
selbst ein Schlüssel, keine Liste enthält ein Modul doppelt, und ein
Modul kann auch sich selbst brauchen (ein Ring aus einem Modul). Ihre
Lösung soll O(Module + Abhängigkeiten) Schritte brauchen.

Hintergrund: Module und Abhängigkeiten bilden einen Graphen: Die Module
sind die Knoten, jede Abhängigkeit ist ein Pfeil vom gebrauchten zum
brauchenden Modul. Ein Dictionary Knoten → Liste seiner Nachbarn ist die
übliche Art, einen Graphen in Python zu speichern. Eine Reihenfolge, in
der jeder Pfeil nach vorn zeigt, heißt topologische Sortierung. Das
Verfahren von Kahn findet sie so:

1. Für jedes Modul zählen, wie viele Module es noch braucht (der
   Eingangsgrad), und umgekehrt notieren, wer es braucht.
2. Alle Module mit Zähler 0 in eine Warteschlange legen.
3. Solange die Warteschlange nicht leer ist: vorn eines herausnehmen und
   an den Plan hängen; bei jedem Modul, das es braucht, den Zähler um
   eins senken und es hinten anstellen, sobald er 0 wird.

    from collections import deque

    braucht = {"b": ["a"], "c": ["a", "b"], "a": []}
    zaehler = {modul: len(liste) for modul, liste in braucht.items()}
    gebraucht_von = {modul: [] for modul in braucht}
    for modul, liste in braucht.items():
        for vorher in liste:
            gebraucht_von[vorher].append(modul)
    warteschlange = deque(m for m in braucht if zaehler[m] == 0)    # deque(['a'])
    while warteschlange:
        modul = warteschlange.popleft()
        ...

Als Warteschlange dient eine deque (Aufgabe 4_062), weil popleft einen
Schritt kostet, liste.pop(0) dagegen so viele, wie die Liste lang ist.
Jedes Modul kommt einmal in die Warteschlange, jede Abhängigkeit wird
einmal angefasst; das sind O(Module + Abhängigkeiten) Schritte. Gehört
ein Modul zu einem Ring, sinkt sein Zähler nie auf 0: Ist die
Warteschlange leer, bevor alle Module im Plan stehen, sind genau die
übrigen die, die wegen eines Rings keinen Platz bekommen. Für die Stufen
nimmt man nicht ein Modul nach dem anderen heraus, sondern immer die
ganze Warteschlange auf einmal: Alles, was gerade darin steht, ist eine
Stufe. Eigene Ausnahmen mit Attributen kennen Sie aus Aufgabe 4_056. Die
Standardbibliothek hat für diese Aufgabe graphlib.TopologicalSorter;
hier bauen Sie es selbst, um zu sehen, wie es geht.
"""

from collections import deque


class ZyklusFehler(Exception):
    """Wird ausgelöst, wenn Module wegen eines Rings von Abhängigkeiten keinen Platz bekommen."""

    def __init__(self, module):
        """Merkt sich die betroffenen Module alphabetisch sortiert und nennt sie in der Meldung."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bauplan(abhaengigkeiten):
    """Gibt alle Module in einer Reihenfolge zurück, in der jedes hinter seinen Abhängigkeiten steht."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def stufen(abhaengigkeiten):
    """Teilt die Module in Stufen, die gleichzeitig gebaut werden können, jede alphabetisch sortiert."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


abhaengigkeiten = {
    "app": ["datenbank", "oberflaeche"],
    "oberflaeche": ["konfiguration"],
    "datenbank": ["konfiguration", "protokoll"],
    "konfiguration": [],
    "protokoll": [],
}
print(bauplan(abhaengigkeiten))
print(stufen(abhaengigkeiten))
try:
    bauplan({"kasse": ["lager"], "lager": ["kasse"], "bericht": ["kasse"], "hilfe": []})
except ZyklusFehler as fehler:
    print(fehler.module)
