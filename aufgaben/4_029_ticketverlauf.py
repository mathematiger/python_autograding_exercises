"""Aufgabe 4_029 – Ticketverlauf                                 Stufe 4 ★★★★☆

Das Ticketsystem des IT-Supports speichert ein Ticket nicht als fertigen
Datensatz, sondern als Folge von Ereignissen: Jemand ändert den Status,
setzt die Priorität hoch, übernimmt das Ticket oder schreibt einen
Kommentar. Den aktuellen Stand eines Tickets erhält man, indem man alle
Ereignisse der Reihe nach auf den Anfangszustand anwendet. Genau so lässt
sich auch nachträglich klären, wie ein Ticket an einem bestimmten Tag
aussah: Man wendet nur die Ereignisse bis zu diesem Tag an.

Ein Zustand ist ein Dictionary wie

    {"status": "neu", "prioritaet": 3, "bearbeiter": None, "kommentare": ()}

und ein Ereignis ein Tupel (feld, wert). Vervollständigen Sie:

- `anwenden(zustand, ereignis)` liefert einen **neuen** Zustand, in dem das
  Ereignis berücksichtigt ist; zustand selbst bleibt unverändert. Bei den
  Feldern "status", "prioritaet" und "bearbeiter" ersetzt wert den alten
  Wert. Beim Feld "kommentar" wird wert hinten an das Tupel "kommentare"
  angehängt.
- `endzustand(start, ereignisse)` wendet alle Ereignisse der Reihe nach
  mit functools.reduce und anwenden auf start an und liefert das Ergebnis.
  Ohne Ereignisse ist das Ergebnis gleich start. start bleibt unverändert.

    start = {"status": "neu", "prioritaet": 3, "bearbeiter": None, "kommentare": ()}
    ereignisse = [("bearbeiter", "Kim"), ("status", "in Arbeit"),
                  ("kommentar", "Drucker neu gestartet"), ("prioritaet", 2),
                  ("status", "gelöst")]
    endzustand(start, ereignisse)
        →  {"status": "gelöst", "prioritaet": 2, "bearbeiter": "Kim",
            "kommentare": ("Drucker neu gestartet",)}
    endzustand(start, ereignisse[:2])["status"]   →  "in Arbeit"

Grenzen: Ein Zustand hat genau die vier Schlüssel aus dem Beispiel, die
Werte sind Texte, ganze Zahlen von 1 bis 5 oder None, "kommentare" ist ein
Tupel aus 0 bis 10 000 Texten. ereignisse ist eine Liste mit 0 bis 10 000
Ereignissen; feld ist immer "status", "prioritaet", "bearbeiter" oder
"kommentar".

Hintergrund: Viele Schleifen haben dieselbe Form: Man beginnt mit einem
Startwert und verrechnet ihn nacheinander mit jedem Element zu einem neuen
Zwischenergebnis.

    ergebnis = startwert
    for element in folge:
        ergebnis = funktion(ergebnis, element)

Genau diese Schleife ist functools.reduce(funktion, folge, startwert). Man
sagt, die Folge wird zu einem Wert „zusammengefaltet“. Die Funktion bekommt
immer zwei Argumente: das bisherige Zwischenergebnis und das nächste
Element.

    from functools import reduce

    reduce(lambda summe, zahl: summe + zahl, [4, 5, 6], 0)
        # ((0 + 4) + 5) + 6  →  15
    reduce(max, [3, 9, 2])
        # max(max(3, 9), 2)  →  9

Ohne Startwert nimmt reduce das erste Element als Startwert. Bei einer
leeren Folge gibt es dann keines, und reduce löst einen TypeError aus;
deshalb gibt man den Startwert fast immer an. Der Startwert muss auch nicht
dieselbe Art haben wie die Elemente: Hier ist er ein Dictionary, die
Elemente sind Tupel.

Für Zahlen gibt es fertige Faltungen wie sum, max und math.prod. reduce
lohnt sich, wenn der Schritt eine eigene Funktion ist wie hier anwenden.
Wichtig ist, dass diese Funktion den alten Zustand nicht verändert, sondern
einen neuen zurückgibt: dict(zustand) oder {**zustand} legt eine Kopie an,
und ein Tupel verlängert man mit tupel + (neues,). So bleiben alle
Zwischenstände gültig, und man kann denselben Start für verschiedene
Zeitpunkte wiederverwenden.
"""

from functools import reduce


def anwenden(zustand, ereignis):
    """Neuer Zustand nach dem Ereignis (feld, wert); zustand bleibt unverändert."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def endzustand(start, ereignisse):
    """Zustand nach allen Ereignissen, mit reduce aus start berechnet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


start = {"status": "neu", "prioritaet": 3, "bearbeiter": None, "kommentare": ()}
ereignisse = [
    ("bearbeiter", "Kim"),
    ("status", "in Arbeit"),
    ("kommentar", "Drucker neu gestartet"),
    ("prioritaet", 2),
    ("status", "gelöst"),
]
print(endzustand(start, ereignisse))
