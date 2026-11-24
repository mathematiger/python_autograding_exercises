"""Aufgabe 4_085 – Störungsgruppen                               Stufe 4 ★★★★☆

Fällt am Montagmorgen der Mailserver aus, gehen beim Service-Desk in
einer Stunde Hunderte Tickets ein: „Outlook startet nicht“, „Keine
neuen Mails“, „Kalender lädt nicht“. Die Mitarbeitenden verknüpfen
Tickets, die erkennbar dieselbe Ursache haben, immer paarweise: „T-17
gehört zu T-4“. Daraus entstehen Gruppen, denn gehört T-17 zu T-4 und
T-23 zu T-17, haben alle drei dieselbe Ursache. Für jede Gruppe wird
nur eine Störung bearbeitet und alle ihre Tickets werden gemeinsam
geschlossen. Das Ticketsystem verwaltet die Gruppen mit Union-Find
(siehe Hintergrund).

Die Klasse `Stoerungsgruppen` mit `__init__` ist vorgegeben:
self.eltern ordnet jedem Ticket ein Ticket seiner Gruppe zu (am Anfang
sich selbst), self.groesse jeder Wurzel die Anzahl der Tickets ihrer
Gruppe, self.anzahl zählt die Gruppen. Vervollständigen Sie:

- `finde(ticket)` gibt die Wurzel der Gruppe von ticket zurück und
  hängt dabei jedes Ticket auf dem Weg direkt an die Wurzel
  (Pfadkompression).
- `verknuepfe(a, b)` vereinigt die Gruppen von a und b und gibt True
  zurück; waren sie schon in derselben Gruppe, ändert sie nichts und
  gibt False zurück. Die Wurzel der kleineren Gruppe kommt unter die
  Wurzel der größeren; bei gleicher Größe kommt die Wurzel von b unter
  die von a.
- `gleiche_ursache(a, b)` gibt True zurück, wenn a und b in derselben
  Gruppe sind.
- `tickets_der_gruppe(ticket)` gibt die sortierte Liste aller Tickets
  in der Gruppe von ticket zurück.
- `anzahl_stoerungen()` gibt die Anzahl der Gruppen zurück, in O(1).

    gruppen = Stoerungsgruppen(["T-1", "T-2", "T-3", "T-4", "T-5"])
    gruppen.verknuepfe("T-2", "T-1")         →  True
    gruppen.verknuepfe("T-3", "T-2")         →  True
    gruppen.verknuepfe("T-1", "T-3")         →  False
    gruppen.gleiche_ursache("T-3", "T-1")    →  True
    gruppen.gleiche_ursache("T-3", "T-4")    →  False
    gruppen.tickets_der_gruppe("T-3")        →  ["T-1", "T-2", "T-3"]
    gruppen.anzahl_stoerungen()              →  3

Grenzen: tickets hat 1 bis 100 000 verschiedene Kennungen (Texte).
Alle Methoden bekommen nur Kennungen aus tickets; a und b dürfen gleich
sein. Für m Aufrufe von finde, verknuepfe und gleiche_ursache soll
Ihre Lösung zusammen fast O(m) Schritte brauchen; tickets_der_gruppe
darf O(n) brauchen.

Hintergrund: Union-Find (auch „disjunkte Mengen“) verwaltet eine
Aufteilung in Gruppen mit zwei Operationen: finden, zu welcher Gruppe
etwas gehört, und zwei Gruppen vereinigen. Der naheliegende Weg, jedem
Ticket eine Gruppennummer zu geben, macht das Finden schnell, aber beim
Vereinigen muss man alle Tickets der einen Gruppe umnummerieren: bei
vielen Vereinigungen O(n²).

Union-Find speichert jede Gruppe stattdessen als Baum, aber anders
herum als in Aufgabe 4_083: Jedes Ticket kennt nur seinen Elternknoten,
die Wurzel zeigt auf sich selbst und vertritt die Gruppe. Ein Dictionary
reicht dafür:

    eltern = {"T-1": "T-1", "T-2": "T-1", "T-3": "T-2", "T-4": "T-4"}
    # Gruppe {T-1, T-2, T-3} mit Wurzel T-1, Gruppe {T-4}

Finden heißt, den Eltern folgen, bis man bei einem Ticket ankommt, das
auf sich selbst zeigt. Vereinigen heißt, die Wurzel der einen Gruppe
unter die Wurzel der anderen zu hängen: eine einzige Zuweisung.

Damit die Wege kurz bleiben, gibt es zwei Tricks, die zusammen jede
Operation fast O(1) machen (genauer O(α(n)), wobei α so langsam wächst,
dass es für jede vorstellbare Datenmenge höchstens 4 ist):

- Nach Größe vereinigen: Die kleinere Gruppe kommt unter die größere.
  Dann wird ein Ticket nur tiefer, wenn sich die Größe seiner Gruppe
  mindestens verdoppelt, also höchstens log₂ n-mal.
- Pfadkompression: Hat finde die Wurzel gefunden, hängt es jedes
  Ticket auf dem Weg direkt an die Wurzel. Der nächste Aufruf ist dann
  sofort fertig.

    def finde(eltern, x):
        wurzel = x
        while eltern[wurzel] != wurzel:      # erster Durchgang: Wurzel suchen
            wurzel = eltern[wurzel]
        while eltern[x] != wurzel:           # zweiter Durchgang: umhängen
            eltern[x], x = wurzel, eltern[x]
        return wurzel

(Die Zuweisung rechts wird erst ganz ausgewertet: x bekommt den alten
Elternknoten.) Rekursiv geht es kürzer, aber ohne Vereinigen nach Größe
können die Wege länger als das Rekursionslimit von etwa 1000 werden. Die
Größe merkt man sich nur für die Wurzeln; nach dem Vereinigen zählt die
neue Wurzel die Tickets beider Gruppen. Die Anzahl der Gruppen sinkt bei
jeder echten Vereinigung um 1.
"""


class Stoerungsgruppen:
    """Gruppen von Tickets mit derselben Ursache, als Union-Find."""

    def __init__(self, tickets):
        """Jedes Ticket bildet zuerst eine eigene Gruppe."""
        self.eltern = {ticket: ticket for ticket in tickets}
        self.groesse = {ticket: 1 for ticket in tickets}
        self.anzahl = len(self.eltern)

    def finde(self, ticket):
        """Gibt die Wurzel der Gruppe von ticket zurück und hängt den Weg direkt an die Wurzel."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def verknuepfe(self, a, b):
        """Vereinigt die Gruppen von a und b; False, wenn sie schon dieselbe Gruppe waren."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def gleiche_ursache(self, a, b):
        """Gibt True zurück, wenn a und b in derselben Gruppe sind."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def tickets_der_gruppe(self, ticket):
        """Gibt die sortierte Liste aller Tickets in der Gruppe von ticket zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def anzahl_stoerungen(self):
        """Gibt die Anzahl der Gruppen zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


gruppen = Stoerungsgruppen(["T-1", "T-2", "T-3", "T-4", "T-5"])
print(gruppen.verknuepfe("T-2", "T-1"), gruppen.verknuepfe("T-3", "T-2"), gruppen.verknuepfe("T-1", "T-3"))
print(gruppen.gleiche_ursache("T-3", "T-1"), gruppen.gleiche_ursache("T-3", "T-4"))
print(gruppen.tickets_der_gruppe("T-3"), gruppen.anzahl_stoerungen())
