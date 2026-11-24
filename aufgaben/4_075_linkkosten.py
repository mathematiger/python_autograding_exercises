"""Aufgabe 4_075 – Linkkosten                                    Stufe 4 ★★★★☆

Die Router eines Firmennetzes wählen ihre Wege mit dem Routingprotokoll
OSPF: Jede Leitung (englisch link) hat Kosten, die das Netzwerkteam
einstellt, meist nach der Geschwindigkeit (10 Gbit/s kostet 1, 1 Gbit/s
kostet 10, 100 Mbit/s kostet 100). Ein Paket läuft immer auf dem Weg mit
den kleinsten Gesamtkosten, nicht auf dem mit den wenigsten Sprüngen.
Bevor das Team eine Leitung umstellt, will es mit einem Skript
nachrechnen, welche Wege danach gelten.

Jeder Router stellt die Kosten für seine Richtung der Leitung selbst
ein, sie können also je Richtung verschieden sein. Das Netz ist deshalb
ein Dictionary, das jedem Router ein Dictionary seiner Nachbarn mit den
Kosten in Richtung dieses Nachbarn zuordnet. Eine Leitung, die in beide
Richtungen arbeitet, steht zweimal darin. Die Leitung zwischen lager und
zentrale ist wegen einer Wartung gerade nur in Richtung zentrale aktiv:

    netz = {
        "zentrale": {"rz": 100, "nord": 10, "sued": 10},
        "nord": {"zentrale": 10, "rz": 10, "ost": 100},
        "sued": {"zentrale": 10, "ost": 10},
        "rz": {"nord": 10, "zentrale": 100, "ost": 1},
        "ost": {"rz": 1, "sued": 10, "nord": 100},
        "lager": {"zentrale": 100},
    }

Schreiben Sie mit heapq drei Funktionen:

- `dijkstra(netz, start)` gibt ein Paar (kosten, vorgaenger) aus zwei
  Dictionaries zurück. kosten ordnet jedem von start aus erreichbaren
  Router die kleinsten Gesamtkosten dorthin zu, start selbst hat 0;
  nicht erreichbare Router fehlen. vorgaenger ordnet jedem erreichbaren
  Router außer start den Router zu, von dem aus die letzte Leitung
  eines günstigsten Wegs zu ihm kommt.
- `weg_aus(vorgaenger, start, ziel)` gibt den Weg von start nach ziel
  als Liste der Router zurück, indem sie von ziel aus den Vorgängern
  folgt, oder None, wenn ziel weder start ist noch in vorgaenger steht.
- `route(netz, start, ziel)` gibt das Paar (gesamtkosten, weg) eines
  günstigsten Wegs zurück oder None, wenn ziel nicht erreichbar ist.
  Benutzen Sie dafür die beiden Funktionen oben.

Gibt es mehrere gleich günstige Wege, ist jeder davon richtig.

    kosten, vorgaenger = dijkstra(netz, "zentrale")
    kosten      →  {"zentrale": 0, "nord": 10, "sued": 10, "rz": 20, "ost": 20}
    vorgaenger  →  {"nord": "zentrale", "sued": "zentrale", "rz": "nord", "ost": "sued"}
    weg_aus(vorgaenger, "zentrale", "ost")  →  ["zentrale", "sued", "ost"]
    route(netz, "zentrale", "rz")     →  (20, ["zentrale", "nord", "rz"])
    route(netz, "lager", "ost")       →  (120, ["lager", "zentrale", "sued", "ost"])
    route(netz, "zentrale", "lager")  →  None

Grenzen: netz hat 0 bis 10 000 Router und zusammen 0 bis 50 000
Leitungen (Einträge in den inneren Dictionaries). Ein Router kann als
Nachbar vorkommen, ohne selbst Schlüssel zu sein; dann gehen von ihm
keine Leitungen aus. Die Namen sind nicht leere Texte, kein Router ist
sein eigener Nachbar, und die Kosten sind ganze Zahlen von 1 bis
65 535. start und ziel sind nicht leere Texte, die nicht in netz
vorkommen müssen. vorgaenger ist bei weg_aus so, wie dijkstra(netz,
start) es liefert. dijkstra soll O((Router + Leitungen) · log Router)
Schritte brauchen.

Hintergrund: In Aufgabe 3_058 haben Sie einen Graphen als Dictionary
gespeichert und mit der Breitensuche die kürzesten Wege gefunden,
gemessen in Sprüngen. Bei Leitungskosten reicht das nicht: Von
"zentrale" aus findet die Breitensuche "rz" über die direkte Leitung
(ein Sprung, Kosten 100), der günstigste Weg geht aber über "nord" (zwei
Sprünge, Kosten 20). Deshalb stehen die Nachbarn hier nicht in einer
Liste, sondern in einem inneren Dictionary mit ihren Kosten, und jede
Leitung hat eine Richtung wie die Abhängigkeiten in Aufgabe 3_059.

Der Algorithmus von Edsger W. Dijkstra (1959) arbeitet wie die
Breitensuche, nimmt aber nicht den ältesten, sondern immer den
günstigsten noch offenen Router aus der Warteschlange. Dessen Kosten
sind dann endgültig: Jeder andere Weg dorthin müsste über einen offenen
Router führen, der schon mindestens so viel kostet, und jede weitere
Leitung macht ihn nur teurer. Genau dafür dürfen keine Kosten negativ
sein. Gäbe es eine Leitung mit Kosten -50, könnte ein Umweg nachträglich
billiger werden, nachdem Dijkstra sich schon festgelegt hat (dafür gibt
es den langsameren Algorithmus von Bellman und Ford).

Den günstigsten offenen Router liefert ein Heap (Aufgabe 4_074) aus
Tupeln (kosten, router): heapq.heappop gibt das Tupel mit den kleinsten
Kosten zurück, in O(log n) Schritten. Wird ein Router billiger, lässt
sich sein alter Eintrag im Heap nicht ändern. Man legt einfach einen
neuen dazu; der alte bleibt liegen und kommt später heraus. Er ist dann
veraltet, weil seine Kosten größer als die in kosten sind, und wird
übersprungen (englisch lazy deletion, „faules Löschen“):

    import heapq

    kosten = {start: 0}
    heap = [(0, start)]
    while heap:
        bisher, router = heapq.heappop(heap)
        if bisher > kosten[router]:
            continue                          # veralteter Eintrag
        for nachbar, leitung in netz.get(router, {}).items():
            neu = bisher + leitung
            if nachbar not in kosten or neu < kosten[nachbar]:
                kosten[nachbar] = neu
                heapq.heappush(heap, (neu, nachbar))

Ohne das Überspringen ginge ein Router, der oft billiger geworden ist,
jedes Mal wieder alle seine Leitungen durch. Den Weg selbst merkt man
sich in einem zweiten Dictionary vorgaenger: Immer wenn ein Nachbar
billiger wird, trägt man ein, von welchem Router aus. Für den Weg geht
man vom Ziel aus rückwärts von Vorgänger zu Vorgänger bis zum Start und
dreht die Liste am Ende um (liste.reverse() oder liste[::-1]):

    vorgaenger = {"nord": "zentrale", "rz": "nord"}
    "rz" → "nord" → "zentrale", umgedreht ["zentrale", "nord", "rz"]

Jede Leitung legt höchstens einen Eintrag in den Heap, und jedes
heappush und heappop kostet O(log Router); zusammen sind das
O((Router + Leitungen) · log Router) Schritte. Die einfache Fassung, die
in jeder Runde alle offenen Router nach dem günstigsten durchsucht,
braucht O(Router²) und ist bei großen Netzen mit wenigen Leitungen je
Router viel langsamer.
"""

import heapq


def dijkstra(netz, start):
    """Gibt (kosten, vorgaenger) der günstigsten Wege von start zu allen erreichbaren Routern zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def weg_aus(vorgaenger, start, ziel):
    """Gibt den Weg von start nach ziel über die Vorgänger zurück, oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def route(netz, start, ziel):
    """Gibt (gesamtkosten, weg) eines günstigsten Wegs von start nach ziel zurück, oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


netz = {
    "zentrale": {"rz": 100, "nord": 10, "sued": 10},
    "nord": {"zentrale": 10, "rz": 10, "ost": 100},
    "sued": {"zentrale": 10, "ost": 10},
    "rz": {"nord": 10, "zentrale": 100, "ost": 1},
    "ost": {"rz": 1, "sued": 10, "nord": 100},
    "lager": {"zentrale": 100},
}
kosten, vorgaenger = dijkstra(netz, "zentrale")
print(sorted(kosten.items()))
print(route(netz, "zentrale", "rz"))
print(route(netz, "lager", "ost"))
print(route(netz, "zentrale", "lager"))
