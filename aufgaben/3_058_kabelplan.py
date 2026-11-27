"""Aufgabe 3_058 – Kabelplan                                     Stufe 3 ★★★☆☆

Im Rechenzentrum eines Hosting-Anbieters sind Switches, Server und
Speichersysteme über Netzwerkkabel verbunden. Die Dokumentation führt
jedes Kabel als Paar der beiden Geräte, die es verbindet; ein Kabel
leitet in beide Richtungen:

    kabel = [("core", "sw1"), ("core", "sw2"), ("sw1", "srv1"),
             ("sw2", "srv2"), ("srv2", "srv3"), ("sw1", "sw2"),
             ("nas", "srv9")]

Jedes Kabel, über das ein Datenpaket läuft, ist ein Sprung (englisch
hop). Je mehr Sprünge ein Gerät vom zentralen Switch "core" entfernt
ist, desto länger brauchen seine Antworten. Der Betrieb möchte wissen,
welche Geräte zu weit weg oder gar nicht angeschlossen sind. Schreiben
Sie drei Funktionen:

- `als_graph(kabel)` gibt ein Dictionary zurück, das jedem Gerät die
  Liste seiner Nachbarn zuordnet, also aller Geräte, mit denen es ein
  Kabel verbindet, in der Reihenfolge der Kabel in der Liste.
- `sprungzahlen(graph, start)` gibt ein Dictionary zurück, das jedem von
  start aus erreichbaren Gerät die kleinste Zahl von Sprüngen dorthin
  zuordnet; start selbst hat 0. Nicht erreichbare Geräte fehlen.
- `zu_weit(kabel, start, hoechstens)` gibt die alphabetisch sortierte
  Liste aller Geräte aus kabel zurück, die von start aus mehr als
  hoechstens Sprünge entfernt oder gar nicht erreichbar sind. Benutzen
  Sie dafür die beiden Funktionen oben.

    graph = als_graph(kabel)
    graph["sw1"]                  →  ["core", "srv1", "sw2"]
    graph["srv3"]                 →  ["srv2"]
    sprungzahlen(graph, "core")
    →  {"core": 0, "sw1": 1, "sw2": 1, "srv1": 2, "srv2": 2, "srv3": 3}
    zu_weit(kabel, "core", 2)     →  ["nas", "srv3", "srv9"]

Grenzen: kabel hat 0 bis 100 000 Paare aus Gerätenamen (nicht leere
Texte). Kein Kabel kommt doppelt vor, auch nicht umgedreht, und keins
verbindet ein Gerät mit sich selbst. start ist ein nicht leerer Text,
der nicht in kabel vorkommen muss; dann erreicht man nur start selbst.
hoechstens ist eine ganze Zahl von 0 bis 100 000. sprungzahlen soll
O(Geräte + Kabel) Schritte brauchen.

Hintergrund: Ein Graph besteht aus Knoten (hier den Geräten) und
Kanten zwischen ihnen (hier den Kabeln). In Python speichert man ihn
meist als Dictionary, das jedem Knoten die Liste seiner Nachbarn
zuordnet (eine Adjazenzliste). Weil ein Kabel in beide Richtungen
leitet, trägt man jedes Paar (a, b) zweimal ein: b bei den Nachbarn
von a und a bei den Nachbarn von b. Kommt ein Gerät zum ersten Mal vor,
legt man vorher eine leere Liste an (if a not in graph: graph[a] = []).

Die Breitensuche (englisch breadth-first search) findet die kürzesten
Wege von einem Startknoten, gemessen in Kanten. Sie arbeitet mit einer
Warteschlange (deque, Aufgabe 3_057): Erst kommt der Start hinein, dann
nimmt man immer den vordersten Knoten heraus und stellt alle seine
Nachbarn hinten an, die man noch nicht gesehen hat. So werden zuerst
alle Knoten im Abstand 1 besucht, dann alle im Abstand 2 und so weiter,
wie Wellen um einen Stein im Wasser:

    abstand = {start: 0}
    schlange = deque([start])
    while schlange:
        knoten = schlange.popleft()
        for nachbar in graph.get(knoten, []):
            if nachbar not in abstand:
                abstand[nachbar] = abstand[knoten] + 1
                schlange.append(nachbar)

Das Dictionary abstand merkt sich zugleich, wer schon gesehen wurde;
ohne diese Prüfung liefe die Suche bei einem Ring wie core–sw1–sw2–core
endlos im Kreis. Nachschlagen mit in kostet in einem Dictionary nur einen
Schritt (Aufgabe 3_019), in einer Liste dagegen so viele, wie sie lang ist.
graph.get(knoten, []) (Aufgabe 2_026) braucht man, weil start nicht im
Graphen stehen muss.
"""

from collections import deque


def als_graph(kabel):
    """Gibt das Dictionary Gerät → Liste der Nachbarn zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def sprungzahlen(graph, start):
    """Gibt für jedes von start aus erreichbare Gerät die kleinste Zahl von Sprüngen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zu_weit(kabel, start, hoechstens):
    """Gibt alle Geräte sortiert zurück, die mehr als hoechstens Sprünge entfernt oder unerreichbar sind."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kabel = [
    ("core", "sw1"),
    ("core", "sw2"),
    ("sw1", "srv1"),
    ("sw2", "srv2"),
    ("srv2", "srv3"),
    ("sw1", "sw2"),
    ("nas", "srv9"),
]
print(sprungzahlen(als_graph(kabel), "core"))
print(zu_weit(kabel, "core", 2))
