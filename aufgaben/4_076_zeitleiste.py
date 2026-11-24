"""Aufgabe 4_076 – Zeitleiste                                    Stufe 4 ★★★★☆

In einem Virtualisierungscluster ist nachts der Host hv01 ausgefallen.
Die Hochverfügbarkeit hat das bemerkt und seine virtuellen Maschinen
(VMs) auf anderen Hosts neu gestartet, aber eine VM kam erst nach
einer halben Minute wieder hoch. Für den Störungsbericht will das
Betriebsteam genau nachvollziehen, was in welcher Reihenfolge geschah.
Jedes Gerät hat dazu sein eigenes Protokoll geschrieben: die Hosts, das
Speichersystem (SAN) und so weiter. Alle Uhren werden über NTP gleich
gestellt, darum passen die Zeitstempel zueinander. Jedes Protokoll ist
eine Liste von Paaren (zeitstempel, meldung), aufsteigend nach
Zeitstempel sortiert; ein ausgefallenes Gerät liefert eine leere Liste:

    protokolle = {
        "san01": [("03:11:58", "Pfad zu hv01 ausgefallen"),
                  ("03:12:09", "Sperre für web-01 an hv02 vergeben")],
        "hv02":  [("03:12:07", "Herzschlag von hv01 fehlt"),
                  ("03:12:09", "starte VM web-01 neu"),
                  ("03:12:31", "VM web-01 läuft")],
        "hv03":  [("03:12:08", "Herzschlag von hv01 fehlt")],
        "hv01":  [],
    }

Daraus soll eine gemeinsame Zeitleiste entstehen. Die Protokolle eines
ganzen Tages sind lang, und oft interessiert nur ein kurzes Fenster um
die Störung. Darum soll die Zeitleiste nicht auf einmal als Liste
entstehen, sondern Eintrag für Eintrag, und jeder Eintrag eines
Protokolls soll erst gelesen werden, wenn er gebraucht wird.

- `zeitleiste(protokolle)` ist ein Generator, der alle Einträge aller
  Protokolle als Tripel (zeitstempel, gerät, meldung) liefert,
  aufsteigend nach Zeitstempel. Bei gleichem Zeitstempel kommt zuerst
  das Gerät, das im Dictionary protokolle weiter vorn steht (nicht das
  alphabetisch erste), und innerhalb eines Protokolls bleibt die
  Reihenfolge erhalten.
- `stoerungsfenster(protokolle, von, bis)` gibt die Liste der Einträge
  der Zeitleiste mit von ≤ zeitstempel ≤ bis zurück. Benutzen Sie dafür
  zeitleiste und hören Sie auf, sobald ein Eintrag nach bis kommt.

    for eintrag in zeitleiste(protokolle):
        print(eintrag)
    →  ('03:11:58', 'san01', 'Pfad zu hv01 ausgefallen')
       ('03:12:07', 'hv02', 'Herzschlag von hv01 fehlt')
       ('03:12:08', 'hv03', 'Herzschlag von hv01 fehlt')
       ('03:12:09', 'san01', 'Sperre für web-01 an hv02 vergeben')
       ('03:12:09', 'hv02', 'starte VM web-01 neu')
       ('03:12:31', 'hv02', 'VM web-01 läuft')

    stoerungsfenster(protokolle, "03:12:08", "03:12:09")
    →  [('03:12:08', 'hv03', 'Herzschlag von hv01 fehlt'),
        ('03:12:09', 'san01', 'Sperre für web-01 an hv02 vergeben'),
        ('03:12:09', 'hv02', 'starte VM web-01 neu')]

Führen Sie die Protokolle mit einem Heap aus dem Modul heapq zusammen,
in dem höchstens ein Eintrag je Gerät liegt. Benutzen Sie weder sort()
und sorted() noch heapq.merge, und verändern Sie die Protokolle nicht.

Grenzen: protokolle hat 0 bis 1000 Geräte mit verschiedenen, nicht
leeren Namen; zusammen haben alle Protokolle 0 bis 100 000 Einträge,
einzelne Protokolle dürfen leer sein. Zeitstempel sind Texte der Form
HH:MM:SS von "00:00:00" bis "23:59:59"; weil alle gleich lang sind,
vergleicht man sie direkt als Texte. Jedes Protokoll ist aufsteigend
sortiert, gleiche Zeitstempel kommen vor, auch in einem Protokoll.
Meldungen sind beliebige Texte. Für stoerungsfenster gilt von ≤ bis.
Bei k Geräten und N Einträgen soll zeitleiste O(N log k) Schritte
brauchen und jeden Eintrag höchstens zweimal lesen, und zwar erst, wenn
er an der Reihe ist; stoerungsfenster liest nichts, was nach dem ersten
Eintrag hinter bis kommt.

Hintergrund: Zwei sortierte Listen haben Sie in Aufgabe 2_055 mit zwei
Stellen i und j zusammengeführt: Das kleinste Element, das noch fehlt,
steht immer vorn in einer der beiden Listen. Bei k Listen gilt dasselbe,
nur gibt es jetzt k Kandidaten, je einen Kopf pro Liste. Drei Wege
liegen nahe, und zwei davon sind langsam:

- Alles aneinanderhängen und sortieren kostet O(N log N) und nutzt
  nicht aus, dass die Listen schon sortiert sind. Außerdem muss dann
  jeder Eintrag gelesen sein, bevor der erste herauskommt.
- Jedes Mal das kleinste der k Köpfe suchen oder die Listen nach und
  nach paarweise wie in 2_055 zusammenführen kostet O(N · k): Bei 1000
  Geräten wird jeder Eintrag bis zu tausendmal angefasst.
- Ein Heap (Aufgabe 4_074) hält die k Köpfe so, dass heappop den
  kleinsten in O(log k) herausholt. Nach jedem heappop legt man den
  nächsten Eintrag derselben Liste mit heappush hinein. Im Heap liegt
  also nie mehr als ein Eintrag je Liste, und jeder Eintrag kostet
  O(log k), zusammen O(N log k).

In den Heap legt man Tupel (wert, listennummer, position): Tupel werden
von vorn nach hinten verglichen, bei gleichem Wert entscheidet also die
Listennummer, und weil es jede Listennummer höchstens einmal im Heap
gibt, kommt der Vergleich nie bei position an. Mit der Position weiß
man, welchen Eintrag man als Nächstes aus derselben Liste holt:

    import heapq

    listen = [[1, 4, 9], [2, 4], [], [3]]
    heap = []
    for nummer, liste in enumerate(listen):
        if liste:                             # leere Listen tragen nichts bei
            heapq.heappush(heap, (liste[0], nummer, 0))

    ergebnis = []
    while heap:
        wert, nummer, position = heapq.heappop(heap)
        ergebnis.append(wert)
        if position + 1 < len(listen[nummer]):
            naechster = listen[nummer][position + 1]
            heapq.heappush(heap, (naechster, nummer, position + 1))
    ergebnis  →  [1, 2, 3, 4, 4, 9]

Die Listennummer im Tupel ist doppelt wichtig: Sie macht die
Reihenfolge bei Gleichstand fest, und sie verhindert, dass Python bei
gleichem Wert das dritte Element vergleicht. Läge dort etwa die
Meldung, würden gleich alte Einträge alphabetisch statt in ihrer
Reihenfolge herauskommen; bei Objekten ohne < gäbe es einen TypeError.

Statt ergebnis.append schreibt Ihr Generator yield (Aufgabe 3_022).
Wie in Aufgabe 4_034 entsteht dann jeder Eintrag erst, wenn jemand
danach fragt, und wer nach dem ersten Eintrag hinter bis aufhört
(break oder return), liest den Rest der Protokolle nie. Die
Standardbibliothek hat genau dieses Verfahren schon fertig:
heapq.merge(*listen, key=…) ist ein Generator, der sortierte Listen mit
einem Heap zusammenführt. Im Betrieb nehmen Sie das; hier bauen Sie es
selbst, um zu sehen, wie es arbeitet.
"""

import heapq


def zeitleiste(protokolle):
    """Liefert alle Einträge aller Protokolle als (zeitstempel, gerät, meldung), nach Zeit sortiert."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def stoerungsfenster(protokolle, von, bis):
    """Gibt die Einträge der Zeitleiste mit von ≤ zeitstempel ≤ bis als Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokolle = {
    "san01": [("03:11:58", "Pfad zu hv01 ausgefallen"), ("03:12:09", "Sperre für web-01 an hv02 vergeben")],
    "hv02": [("03:12:07", "Herzschlag von hv01 fehlt"), ("03:12:09", "starte VM web-01 neu"), ("03:12:31", "VM web-01 läuft")],
    "hv03": [("03:12:08", "Herzschlag von hv01 fehlt")],
    "hv01": [],
}
for eintrag in zeitleiste(protokolle):
    print(eintrag)
print(stoerungsfenster(protokolle, "03:12:08", "03:12:09"))
