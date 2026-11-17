"""Aufgabe 5_023 – Wahrheitswert                                 Stufe 5 ★★★★★

Ein Support-Team arbeitet mit zwei kleinen Klassen. Eine `Ticketliste`
merkt sich zu jeder Ticketnummer, ob das Ticket offen oder geschlossen ist;
geschlossene Tickets bleiben für die Statistik in der Liste. Eine
`SlaAuswertung` sammelt, wie viele Stunden die Lösung jedes Tickets
gedauert hat, und prüft, ob die vereinbarte Servicequalität (SLA, Service
Level Agreement) eingehalten wurde: Mindestens zielprozent Prozent der
Tickets müssen innerhalb der Frist gelöst sein. Die Leitstelle will beide
Objekte direkt in Bedingungen verwenden: `if liste:` soll heißen „es gibt
offene Tickets“, `if auswertung:` soll heißen „das SLA ist eingehalten“.
Vervollständigen Sie:

- `Ticketliste.__len__(self)` liefert die Anzahl der **offenen** Tickets.
  Schreiben Sie für Ticketliste **kein** `__bool__`: Python leitet den
  Wahrheitswert hier selbst aus `__len__` ab.
- `SlaAuswertung.__len__(self)` liefert die Anzahl der erfassten Tickets.
- `SlaAuswertung.__bool__(self)` liefert True, wenn mindestens zielprozent
  Prozent der erfassten Tickets eine Dauer ≤ frist haben, sonst False. Ohne
  erfasste Tickets ist nichts verletzt, das Ergebnis ist True, obwohl
  `len(auswertung)` dann 0 ist.

    liste = Ticketliste()
    liste.oeffnen(101)
    liste.oeffnen(102)
    liste.schliessen(101)
    len(liste), bool(liste)          →  1, True
    liste.schliessen(102)
    len(liste), not liste            →  0, True

    sla = SlaAuswertung(frist=8, zielprozent=90)
    len(sla), bool(sla)              →  0, True
    for dauer in [2, 5, 12]:
        sla.erfassen(dauer)
    len(sla), bool(sla)              →  3, False    (nur 2 von 3 in der Frist)

Grenzen: Ticketnummern sind ganze Zahlen von 1 bis 10**9; oeffnen und
schliessen dürfen dieselbe Nummer beliebig oft und in beliebiger Reihenfolge
bekommen (schliessen einer unbekannten Nummer legt sie als geschlossen an).
Eine Liste hat bis zu 100 000 Tickets. frist ist eine ganze Zahl von 1 bis
720, zielprozent eine ganze Zahl von 0 bis 100, jede Dauer eine ganze Zahl
oder Kommazahl von 0 bis 10 000; es gibt bis zu 100 000 Dauern. Eine Dauer
genau gleich der Frist gilt als eingehalten. Rechnen Sie den Anteil ohne
Kommazahlen (100 · in_frist ≥ zielprozent · anzahl), damit 90 % nicht an
einer Rundung scheitern.

Hintergrund: Jedes Objekt in Python hat einen Wahrheitswert. Ihn fragen
if, while, not, and, or und bool() ab. Für eigene Klassen geht Python dabei
so vor:

1. Hat die Klasse `__bool__`, wird es aufgerufen. Es muss genau True oder
   False liefern; gibt es etwa 1 oder None zurück, bricht bool() mit einem
   TypeError ab („__bool__ should return bool“).
2. Sonst: Hat die Klasse `__len__`, gilt das Objekt als falsch, wenn
   `__len__` 0 liefert, und sonst als wahr. `__len__` muss eine ganze Zahl
   ≥ 0 liefern, sonst gibt es einen TypeError oder ValueError.
3. Hat die Klasse keines von beiden, ist jedes Objekt wahr.

    class Korb:
        def __init__(self):
            self.teile = []
        def __len__(self):
            return len(self.teile)

    k = Korb()
    len(k), bool(k)          →  0, False      (Regel 2)
    k.teile.append("Maus")
    bool(k)                  →  True

So verhalten sich auch list, dict, str und set: leer heißt falsch. Für
einen Container genügt deshalb `__len__`; ein zusätzliches `__bool__`, das
nur `len(self) > 0` wiederholt, wäre doppelte Logik. `__bool__` lohnt sich,
wenn der Wahrheitswert etwas anderes bedeutet als „nicht leer“. Weil Regel 1
vor Regel 2 kommt, gewinnt `__bool__` dann immer, auch wenn `__len__` 0
liefert:

    class Pruefung:
        def __init__(self):
            self.fehler = []
        def __len__(self):
            return len(self.fehler)
        def __bool__(self):
            return len(self.fehler) == 0     # bestanden, wenn kein Fehler

    p = Pruefung()
    len(p), bool(p)          →  0, True

`__bool__` sollte mit einem Vergleich enden (`== 0`, `>=` …), dann ist das
Ergebnis von selbst ein bool. Ein Fallstrick ist `if not x:` für „x fehlt“:
Ist x ein leeres Objekt mit `__len__`, gilt es auch als falsch. Ob ein
Argument fehlt, prüft man darum mit `if x is None:`.
"""


class Ticketliste:
    """Tickets mit Status offen oder geschlossen; wahr, solange ein Ticket offen ist."""

    def __init__(self):
        self._status = {}

    def oeffnen(self, nummer):
        """Setzt das Ticket auf offen."""
        self._status[nummer] = "offen"

    def schliessen(self, nummer):
        """Setzt das Ticket auf geschlossen."""
        self._status[nummer] = "geschlossen"

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class SlaAuswertung:
    """Lösungsdauern von Tickets; wahr, wenn das SLA eingehalten ist."""

    def __init__(self, frist, zielprozent):
        self.frist = frist
        self.zielprozent = zielprozent
        self._dauern = []

    def erfassen(self, dauer):
        """Nimmt die Lösungsdauer eines Tickets in Stunden auf."""
        self._dauern.append(dauer)

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __bool__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


liste = Ticketliste()
liste.oeffnen(101)
liste.oeffnen(102)
liste.schliessen(101)
print(len(liste), bool(liste))

sla = SlaAuswertung(frist=8, zielprozent=90)
for dauer in [2, 5, 12]:
    sla.erfassen(dauer)
print(len(sla), bool(sla))
