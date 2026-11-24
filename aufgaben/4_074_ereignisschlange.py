"""Aufgabe 4_074 – Ereignisschlange                              Stufe 4 ★★★★☆

Die Oberfläche einer Lagerverwaltung ruckelt: Wer schnell tippt, sieht
die Buchstaben erst eine halbe Sekunde später. Das Entwicklungsteam
baut deshalb die Ereignisschleife um. Jede Benutzereingabe (Taste,
Mausklick), jeder abgelaufene Zeitgeber und jeder Auftrag, einen Teil
des Fensters neu zu zeichnen, wird als Ereignis in eine Warteschlange
gestellt, und die Schleife holt immer das dringendste heraus: Eingaben
vor Zeitgebern vor Neuzeichnen, denn ein Bild, das ein paar
Millisekunden später kommt, merkt niemand, eine verschluckte Taste
schon. Bei gleicher Priorität gilt die Eingangsreihenfolge, sonst
kämen zwei Tasten vertauscht an. Außerdem zeichnet die Oberfläche in
einem Messprotokoll auf, wie lange jede Aktion gedauert hat, und das
Team will daraus die langsamsten Aktionen sehen.

Schreiben Sie mit dem Modul heapq:

- `langsamste(protokoll, k)` bekommt das Messprotokoll als Liste von
  Tupeln (aktion, dauer) mit der Dauer in Millisekunden und gibt die
  k Einträge mit der größten Dauer zurück, den langsamsten zuerst.
  Haben zwei Einträge dieselbe Dauer, kommt der frühere im Protokoll
  zuerst. Hat das Protokoll weniger als k Einträge, kommen alle. Das
  Protokoll selbst bleibt unverändert.
- die Klasse `Ereignisschlange` mit den Methoden
  - `einreihen(self, ereignis, prioritaet)`: stellt ein Ereignis ein;
    ereignis ist ein Dictionary, prioritaet eine ganze Zahl, kleiner
    heißt dringender (siehe PRIORITAETEN),
  - `naechstes(self)`: entfernt das dringendste Ereignis und gibt es
    zurück, bei gleicher Priorität das zuerst eingereihte,
  - `vorschau(self)`: gibt dasselbe Ereignis zurück, ohne es zu
    entfernen,
  - `ist_leer(self)`: True, wenn kein Ereignis wartet.
  naechstes und vorschau lösen bei leerer Schlange einen IndexError aus.

    protokoll = [("Speichern", 120), ("Suche", 870), ("Menü öffnen", 35),
                 ("Bericht", 870), ("Export", 1450), ("Tippen", 12)]
    langsamste(protokoll, 3)
        →  [("Export", 1450), ("Suche", 870), ("Bericht", 870)]

    schlange = Ereignisschlange()
    schlange.einreihen({"art": "neuzeichnen", "bereich": "liste"}, 2)
    schlange.einreihen({"art": "taste", "zeichen": "a"}, 0)
    schlange.einreihen({"art": "zeitgeber", "name": "autosave"}, 1)
    schlange.einreihen({"art": "klick", "x": 40, "y": 12}, 0)
    schlange.vorschau()    →  {"art": "taste", "zeichen": "a"}
    schlange.naechstes()   →  {"art": "taste", "zeichen": "a"}
    schlange.naechstes()   →  {"art": "klick", "x": 40, "y": 12}
    schlange.naechstes()   →  {"art": "zeitgeber", "name": "autosave"}
    schlange.naechstes()   →  {"art": "neuzeichnen", "bereich": "liste"}
    schlange.ist_leer()    →  True
    schlange.naechstes()   →  IndexError

Grenzen: Das Protokoll hat 0 bis 200 000 Einträge, aktion ist ein nicht
leerer Text, dauer eine ganze Zahl mit 0 ≤ dauer ≤ 60 000; 0 ≤ k ≤ 1000.
Eine Ereignisschlange hält bis zu 100 000 Ereignisse, Ereignisse sind
Dictionaries mit beliebigem Inhalt, Prioritäten ganze Zahlen von 0 bis
9. einreihen und naechstes werden beliebig abwechselnd aufgerufen.
Laufzeit: langsamste soll nicht das ganze Protokoll sortieren, sondern
O(n log k) Vergleiche brauchen; einreihen und naechstes sollen je
O(log m) Vergleiche brauchen, wenn m Ereignisse warten, vorschau und
ist_leer O(1).

Hintergrund: Ein Heap ist eine Liste, deren Elemente so angeordnet
sind, dass heap[0] immer das kleinste ist. Der Rest ist nicht sortiert,
sondern nur so weit geordnet, dass jedes Element an der Stelle i nicht
größer ist als die an den Stellen 2*i+1 und 2*i+2 (wie ein Baum, in dem
jeder Knoten kleiner als seine Kinder ist). Das Modul heapq hält diese
Ordnung mit wenig Aufwand aufrecht:

    import heapq

    heap = []
    heapq.heappush(heap, 5)           # einfügen: O(log n)
    heapq.heappush(heap, 1)
    heapq.heappush(heap, 3)
    heap[0]                           →  1   (nur ansehen: O(1))
    heapq.heappop(heap)               →  1   (kleinstes entnehmen: O(log n))
    heapq.heappop(heap)               →  3

    werte = [7, 2, 9, 4]
    heapq.heapify(werte)              # vorhandene Liste umordnen: O(n)
    werte[0]                          →  2

heappush und heappop müssen nur einen Weg von der Wurzel bis zu einem
Blatt durchlaufen, der ist bei n Elementen etwa log2(n) lang. Eine
Liste nach jedem Einfügen neu zu sortieren oder bei jedem Entnehmen mit
min das Kleinste zu suchen, kostet dagegen jedes Mal O(n) Vergleiche.

Für „die k kleinsten“ oder „die k größten“ gibt es heapq.nsmallest und
heapq.nlargest. Sie behalten beim Durchlaufen nur einen Heap mit k
Elementen und vergleichen jedes neue Element zuerst mit dessen Wurzel;
so brauchen sie O(n log k) statt O(n log n) Vergleiche wie das
Sortieren, bei n = 200 000 und k = 10 ein großer Unterschied. Mit key
geht es wie bei sorted (Aufgabe 3_027); bei gleichem Schlüssel bleibt
die ursprüngliche Reihenfolge erhalten:

    zeiten = [("a", 30), ("b", 90), ("c", 10), ("d", 90)]
    heapq.nsmallest(2, zeiten, key=lambda eintrag: eintrag[1])  →  [("c", 10), ("a", 30)]
    heapq.nlargest(2, zeiten, key=lambda eintrag: eintrag[1])   →  [("b", 90), ("d", 90)]

heapq kennt nur Min-Heaps. Einen Max-Heap, der das größte zuerst
liefert, bekommt man, indem man die Zahlen negiert einfügt und beim
Herausholen wieder umdreht:

    groesste = []
    for dauer in [120, 870, 35]:
        heapq.heappush(groesste, -dauer)
    -heapq.heappop(groesste)          →  870

Als Prioritätswarteschlange legt man Tupel in den Heap, denn Tupel
werden Element für Element verglichen. Mit (prioritaet, daten) gäbe es
bei gleicher Priorität zwei Probleme: Python vergliche dann die Daten,
was bei Dictionaries einen TypeError auslöst, und selbst bei Texten
käme nicht die Eingangsreihenfolge heraus. Darum steht dazwischen eine
laufende Nummer, die bei jedem Einfügen um eins wächst. Sie ist nie
doppelt, also wird nach ihr nie weiter verglichen:

    aufgaben = []
    nummer = 0
    for prioritaet, daten in [(2, {"x": 1}), (1, {"y": 2}), (2, {"z": 3})]:
        heapq.heappush(aufgaben, (prioritaet, nummer, daten))
        nummer += 1
    heapq.heappop(aufgaben)          →  (1, 1, {"y": 2})
    heapq.heappop(aufgaben)[2]       →  {"x": 1}

Statt Tupeln gehen auch Objekte einer Datenklasse mit order=True
(Aufgabe 4_012 und 4_014), deren Daten-Feld mit field(compare=False)
vom Vergleich ausgenommen ist. Eine deque (Aufgabe 4_062) ist dagegen
eine Schlange ohne Prioritäten: Sie gibt immer das zuerst eingereihte
Element zurück.
"""

import heapq

PRIORITAETEN = {"eingabe": 0, "zeitgeber": 1, "neuzeichnen": 2}


def langsamste(protokoll, k):
    """Gibt die k Protokolleinträge mit der größten Dauer zurück, den langsamsten zuerst."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Ereignisschlange:
    """Warteschlange für Oberflächenereignisse: das dringendste zuerst, bei Gleichstand das ältere."""

    def __init__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def einreihen(self, ereignis, prioritaet):
        """Stellt ereignis mit der gegebenen Priorität ein (kleiner ist dringender)."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def naechstes(self):
        """Entfernt das dringendste, bei Gleichstand das älteste Ereignis und gibt es zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def vorschau(self):
        """Gibt das Ereignis zurück, das naechstes liefern würde, ohne es zu entfernen."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def ist_leer(self):
        """Gibt True zurück, wenn kein Ereignis wartet."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokoll = [("Speichern", 120), ("Suche", 870), ("Menü öffnen", 35), ("Bericht", 870), ("Export", 1450), ("Tippen", 12)]
print(langsamste(protokoll, 3))

schlange = Ereignisschlange()
schlange.einreihen({"art": "neuzeichnen", "bereich": "liste"}, PRIORITAETEN["neuzeichnen"])
schlange.einreihen({"art": "taste", "zeichen": "a"}, PRIORITAETEN["eingabe"])
schlange.einreihen({"art": "zeitgeber", "name": "autosave"}, PRIORITAETEN["zeitgeber"])
schlange.einreihen({"art": "klick", "x": 40, "y": 12}, PRIORITAETEN["eingabe"])
for _ in range(4):
    print(schlange.naechstes())
