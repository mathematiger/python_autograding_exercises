"""Aufgabe 4_088 – Sicherheitsaudit                              Stufe 4 ★★★★☆

Eine mittelständische Firma lässt ihr Netz von einem Sicherheitsteam
prüfen. Im Abschlussbericht sollen drei Fragen beantwortet werden, und
alle drei sind Fragen an einen Graphen:

1. Welche Rechner (Hosts) bilden zusammen ein Segment? Die Firewall
   erlaubt Verbindungen zwischen bestimmten Paaren von Hosts in beide
   Richtungen (eine Freigabe). Wer über eine Kette von Freigaben
   erreichbar ist, gehört zum selben Segment: Wird ein Host darin
   übernommen, sind alle anderen gefährdet.
2. Welcher Angriffsweg vom Internet zu einem wichtigen Server ist am
   billigsten? Das Team hat für jede Verbindung geschätzt, wie viel
   Aufwand (in Personenstunden) ein Angreifer braucht, um von einem
   Host aus den nächsten zu übernehmen. Der Weg mit dem kleinsten
   Gesamtaufwand muss zuerst geschlossen werden.
3. In welcher Reihenfolge werden die fälligen Sicherheitsupdates
   eingespielt? Manche Updates setzen andere voraus. Unter den Updates,
   die gerade an der Reihe sein dürfen, nimmt das Team immer das
   alphabetisch erste, damit der Plan eindeutig ist.

Schreiben Sie mit heapq:

- `segmente(hosts, freigaben)` gibt alle Segmente als Liste zurück.
  Jedes Segment ist eine alphabetisch sortierte Liste seiner Hosts, die
  Segmente sind nach ihrem ersten Host sortiert. Ein Host ohne Freigabe
  ist ein Segment für sich. Benutzen Sie Union-Find.
- `billigster_angriff(netz, start, ziel)` gibt das Paar (aufwand, weg)
  eines Wegs mit dem kleinsten Gesamtaufwand von start nach ziel
  zurück; weg ist die Liste der Hosts von start bis ziel. Ist ziel nicht
  erreichbar, gibt sie None zurück. netz ordnet jedem Host ein
  Dictionary Nachbar → Aufwand zu; eine Verbindung gilt nur in dieser
  Richtung. Gibt es mehrere gleich billige Wege, ist jeder richtig.
- `einspielreihenfolge(updates)` bekommt ein Dictionary Update → Liste
  der Updates, die vorher eingespielt sein müssen, und gibt die Liste
  aller Updates in der Reihenfolge zurück, in der sie eingespielt
  werden: Jedes steht hinter allen, die es voraussetzt, und unter den
  Updates, die als nächstes dürften, kommt immer das alphabetisch
  erste. Gibt es einen Ring, löst sie einen ValueError aus, dessen
  Meldung alle Updates nennt, die deshalb keinen Platz bekommen.

Die übergebenen Listen und Dictionaries bleiben unverändert.

    hosts = ["web", "db", "mail", "pc-01", "pc-02", "drucker", "backup"]
    freigaben = [("web", "db"), ("pc-01", "mail"), ("pc-02", "pc-01"), ("db", "backup")]
    segmente(hosts, freigaben)
        →  [["backup", "db", "web"], ["drucker"], ["mail", "pc-01", "pc-02"]]

    netz = {
        "internet": {"web": 3, "mail": 5, "vpn": 8},
        "web": {"db": 6, "mail": 2},
        "mail": {"pc-01": 1},
        "pc-01": {"db": 4, "backup": 9},
        "vpn": {"db": 2},
        "db": {"backup": 1},
    }
    billigster_angriff(netz, "internet", "db")      →  (9, ["internet", "web", "db"])
    billigster_angriff(netz, "internet", "backup")  →  (10, ["internet", "web", "db", "backup"])
    billigster_angriff(netz, "db", "internet")      →  None

    updates = {
        "kernel-6.8": [],
        "openssl-3.2": ["kernel-6.8"],
        "openssh-9.6": ["openssl-3.2"],
        "nginx-1.25": ["openssl-3.2"],
        "firmware-2.1": [],
    }
    einspielreihenfolge(updates)
        →  ["firmware-2.1", "kernel-6.8", "openssl-3.2", "nginx-1.25", "openssh-9.6"]
    einspielreihenfolge({"a": ["b"], "b": ["a"], "c": []})  →  ValueError (nennt a und b)

Grenzen: hosts hat 1 bis 100 000 verschiedene, nicht leere Namen,
freigaben 0 bis 200 000 Paare (a, b) mit a und b aus hosts; a und b
dürfen gleich sein. netz hat 0 bis 10 000 Hosts und zusammen 0 bis
50 000 Verbindungen mit einem ganzzahligen Aufwand von 1 bis 1000; kein
Host ist sein eigener Nachbar, und ein Host kann als Nachbar vorkommen,
ohne selbst Schlüssel zu sein. start und ziel sind nicht leere Namen,
die nicht in netz vorkommen müssen; ist start gleich ziel, ist die
Antwort (0, [start]). updates hat 0 bis 10 000 Updates und zusammen
0 bis 50 000 Voraussetzungen; jedes Update in einer Liste ist selbst
ein Schlüssel, keine Liste enthält eines doppelt, und ein Update kann
sich selbst voraussetzen (ein Ring aus einem Update). Laufzeit:
segmente fast O(Hosts + Freigaben) und dazu das Sortieren,
billigster_angriff O((Hosts + Verbindungen) · log Hosts),
einspielreihenfolge O((Updates + Voraussetzungen) · log Updates).

Hintergrund: Diese Übung führt nichts Neues ein, sondern verbindet drei
Verfahren auf Graphen, die Sie schon kennen.

Union-Find (Aufgabe 4_085) verwaltet Gruppen: Jeder Host kennt einen
Elternknoten, die Wurzel zeigt auf sich selbst und vertritt das Segment.
Für jede Freigabe sucht man beide Wurzeln und hängt die kleinere Gruppe
unter die größere; Pfadkompression hält die Wege kurz. Am Ende sammelt
man die Hosts nach ihrer Wurzel, etwa mit setdefault oder defaultdict
(Aufgabe 4_060). Hier reichen zwei Dictionaries und eine innere
Funktion:

    eltern = {host: host for host in hosts}
    def finde(host):
        while eltern[host] != host:
            eltern[host] = eltern[eltern[host]]    # Weg halbieren, eine Form der Pfadkompression
            host = eltern[host]
        return host

Dijkstra (Aufgabe 4_075) findet den billigsten Weg, wenn kein Aufwand
negativ ist: Ein Heap (Aufgabe 4_074) aus Paaren (aufwand, host) liefert
immer den billigsten offenen Host; dessen Aufwand ist dann endgültig.
Wird ein Nachbar billiger, legt man einen neuen Eintrag in den Heap und
überspringt später die veralteten. In einem Dictionary vorgaenger merkt
man sich, von wo aus jeder Host am billigsten erreicht wurde, und baut
den Weg am Ende rückwärts vom Ziel aus zusammen. Ist das Ziel aus dem
Heap gekommen, darf man aufhören.

Die topologische Sortierung nach Kahn (Aufgabe 4_064) zählt für jedes
Update, wie viele Voraussetzungen noch fehlen, und stellt die Updates
mit Zähler 0 bereit. Dort war die Warteschlange eine deque; hier soll
aber immer das alphabetisch erste bereite Update drankommen. Das liefert
ein Heap aus Texten, denn Texte vergleicht Python alphabetisch:

    bereit = ["openssl-3.2", "firmware-2.1", "kernel-6.8"]
    heapq.heapify(bereit)
    heapq.heappop(bereit)      →  "firmware-2.1"
    heapq.heappush(bereit, "apache-2.4")
    heapq.heappop(bereit)      →  "apache-2.4"

Jedes Update kommt einmal in den Heap und einmal heraus, also
O(log Updates) Schritte je Update statt O(Updates), wenn man jedes Mal
mit min sucht. Bleiben am Ende Updates übrig, deren Zähler nie 0 wurde,
gibt es einen Ring.
"""

import heapq


def segmente(hosts, freigaben):
    """Gibt die Segmente als sortierte Listen von Hosts zurück, sortiert nach ihrem ersten Host."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def billigster_angriff(netz, start, ziel):
    """Gibt (aufwand, weg) eines billigsten Wegs von start nach ziel zurück, oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def einspielreihenfolge(updates):
    """Gibt die Updates in Einspielreihenfolge zurück; ValueError bei einem Ring."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


hosts = ["web", "db", "mail", "pc-01", "pc-02", "drucker", "backup"]
freigaben = [("web", "db"), ("pc-01", "mail"), ("pc-02", "pc-01"), ("db", "backup")]
print(segmente(hosts, freigaben))
netz = {
    "internet": {"web": 3, "mail": 5, "vpn": 8},
    "web": {"db": 6, "mail": 2},
    "mail": {"pc-01": 1},
    "pc-01": {"db": 4, "backup": 9},
    "vpn": {"db": 2},
    "db": {"backup": 1},
}
print(billigster_angriff(netz, "internet", "db"), billigster_angriff(netz, "db", "internet"))
updates = {
    "kernel-6.8": [],
    "openssl-3.2": ["kernel-6.8"],
    "openssh-9.6": ["openssl-3.2"],
    "nginx-1.25": ["openssl-3.2"],
    "firmware-2.1": [],
}
print(einspielreihenfolge(updates))
