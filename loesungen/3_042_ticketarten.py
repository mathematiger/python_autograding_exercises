# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_042_ticketarten.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_042_ticketarten

"""Aufgabe 3_042 – Ticketarten                                   Stufe 3 ★★★☆☆

Im Service-Desk einer IT-Abteilung landen zwei Arten von Tickets. Eine
Störung meldet, dass etwas nicht mehr funktioniert, etwa der Drucker im
dritten Stock oder das ganze E-Mail-System. Eine Serviceanfrage ist ein
Wunsch, etwa ein neuer Zugang oder ein zweiter Bildschirm. Beide haben
eine Nummer, eine Beschreibung und eine Priorität von 1 (hoch) bis 3
(niedrig), und für beide gilt eine Reaktionszeit: So viele Stunden darf
es höchstens dauern, bis sich jemand meldet. Die vereinbarten Zeiten
stehen in der vorgegebenen Klasse `Ticket`: 4, 8 und 24 Stunden für die
Prioritäten 1, 2 und 3.

Schreiben Sie zwei Unterklassen von Ticket und eine Funktion:

- `Stoerung(nummer, beschreibung, prioritaet, betroffene)` hat
  zusätzlich das Attribut betroffene, die Zahl der Personen, die nicht
  arbeiten können. Rufen Sie für die übrigen Attribute
  super().__init__(...) auf. art() gibt "Störung" zurück. Sind
  mindestens 50 Personen betroffen, gilt nur die halbe Reaktionszeit
  eines gewöhnlichen Tickets (ganzzahlig geteilt mit //), sonst die
  gewöhnliche.
- `Serviceanfrage(nummer, beschreibung, prioritaet)` braucht kein
  eigenes __init__. art() gibt "Serviceanfrage" zurück, und die
  Reaktionszeit ist doppelt so lang wie bei einem gewöhnlichen Ticket.
- `dringendstes(tickets)` gibt aus einer Liste von Tickets das mit der
  kürzesten Reaktionszeit zurück; bei Gleichstand das, das zuerst in der
  Liste steht, bei einer leeren Liste None.

Holen Sie die gewöhnliche Reaktionszeit in den Unterklassen mit
super().reaktionszeit(), statt die Zahlen 4, 8 und 24 noch einmal
hinzuschreiben. Das vorgegebene __str__ benutzt art() und funktioniert
dann von selbst für beide Unterklassen.

    s = Stoerung(17, "Mailserver aus", 1, 120)
    a = Serviceanfrage(18, "Zweiter Bildschirm", 2)
    s.reaktionszeit()           →  2
    a.reaktionszeit()           →  16
    str(s)                      →  "#17 Störung: Mailserver aus (Priorität 1)"
    dringendstes([a, s]) is s   →  True

Grenzen: Die Liste hat 0 bis 10 000 Tickets, prioritaet ist 1, 2 oder 3,
betroffene eine ganze Zahl von 0 bis 100 000. In der Liste dürfen
Störungen, Serviceanfragen und gewöhnliche Tickets gemischt sein.

Hintergrund: Eine Klasse kann von einer anderen erben: class Kind(Eltern):
übernimmt alle Methoden von Eltern, auch __init__: Schreibt Kind kein
eigenes __init__, gilt das der Elternklasse. Was man in Kind neu
schreibt, ersetzt die geerbte Methode gleichen Namens (man sagt, es
überschreibt sie); alles andere bleibt, wie es geerbt wurde. Mit super().methode(...) ruft
man in Kind die Fassung der Elternklasse auf, um sie zu ergänzen statt
sie ganz neu zu schreiben:

    class Geraet:
        def __init__(self, name):
            self.name = name

        def leistung(self):
            return 100

    class Server(Geraet):
        def __init__(self, name, netzteile):
            super().__init__(name)          # setzt self.name
            self.netzteile = netzteile

        def leistung(self):
            return super().leistung() * self.netzteile

Server("db1", 2).leistung() ist 200, und ein Server ist zugleich ein
Geraet: isinstance(Server("db1", 2), Geraet) ist True. Darum kann eine
Funktion wie dringendstes alle Tickets gleich behandeln; welche
reaktionszeit dabei läuft, entscheidet Python bei jedem Aufruf nach der
Klasse des Objekts.
"""


class Ticket:
    """Ein gewöhnliches Ticket mit Nummer, Beschreibung und Priorität (vorgegeben)."""

    def __init__(self, nummer, beschreibung, prioritaet):
        self.nummer = nummer
        self.beschreibung = beschreibung
        self.prioritaet = prioritaet

    def art(self):
        """Gibt die Art des Tickets als Text zurück."""
        return "Ticket"

    def reaktionszeit(self):
        """Gibt die vereinbarte Reaktionszeit in Stunden zurück."""
        if self.prioritaet == 1:
            return 4
        if self.prioritaet == 2:
            return 8
        return 24

    def __str__(self):
        return f"#{self.nummer} {self.art()}: {self.beschreibung} (Priorität {self.prioritaet})"


class Stoerung(Ticket):
    """Eine Störung; bei vielen Betroffenen gilt die halbe Reaktionszeit."""

    def __init__(self, nummer, beschreibung, prioritaet, betroffene):
        """Legt die Störung an; die drei gemeinsamen Attribute setzt Ticket."""
        super().__init__(nummer, beschreibung, prioritaet)
        self.betroffene = betroffene

    def art(self):
        """Gibt "Störung" zurück."""
        return "Störung"

    def reaktionszeit(self):
        """Gibt die halbe Reaktionszeit zurück, wenn mindestens 50 Personen betroffen sind."""
        if self.betroffene >= 50:
            return super().reaktionszeit() // 2
        return super().reaktionszeit()


class Serviceanfrage(Ticket):
    """Eine Serviceanfrage mit doppelter Reaktionszeit."""

    def art(self):
        """Gibt "Serviceanfrage" zurück."""
        return "Serviceanfrage"

    def reaktionszeit(self):
        """Gibt die doppelte Reaktionszeit zurück."""
        return super().reaktionszeit() * 2


def dringendstes(tickets):
    """Gibt das Ticket mit der kürzesten Reaktionszeit zurück, bei Gleichstand das erste, sonst None."""
    bestes = None
    for ticket in tickets:
        if bestes is None or ticket.reaktionszeit() < bestes.reaktionszeit():
            bestes = ticket
    return bestes


stoerung = Stoerung(17, "Mailserver aus", 1, 120)
anfrage = Serviceanfrage(18, "Zweiter Bildschirm", 2)
print(stoerung, "–", stoerung.reaktionszeit(), "Stunden")
print(anfrage, "–", anfrage.reaktionszeit(), "Stunden")
print("Zuerst:", dringendstes([anfrage, stoerung]))


# Idee: Stoerung und Serviceanfrage erben von Ticket und überschreiben nur, was anders ist: art() und
# reaktionszeit(). Stoerung.__init__ lässt super().__init__ die drei gemeinsamen Attribute setzen und
# ergänzt betroffene. Beide reaktionszeit-Methoden holen die gewöhnliche Zeit mit
# super().reaktionszeit() und halbieren bzw. verdoppeln sie. dringendstes merkt sich das bisher
# dringendste Ticket und ersetzt es nur bei einer echt kürzeren Zeit; welche reaktionszeit dabei
# läuft, hängt von der Klasse des jeweiligen Tickets ab.
# Anderer Weg: dringendstes mit min(tickets, key=lambda t: t.reaktionszeit()), das bei Gleichstand
# ebenfalls das erste liefert, mit default=None für die leere Liste. Hätte man Ticket selbst
# geschrieben, könnte jede Klasse statt art() ein Klassenattribut ART = "Störung" haben, das
# __str__ liest.
# Typische Fehler: in Stoerung.__init__ super().__init__ vergessen (dann fehlt self.nummer), in den
# Unterklassen 4, 8 und 24 noch einmal abfragen (doppelte Logik, die bei einer neuen Vereinbarung
# auseinanderläuft), / statt // (2.0 statt 2), > 50 statt >= 50 oder __str__ in jeder Unterklasse
# neu schreiben.
# Laufzeit: reaktionszeit ist O(1), dringendstes geht die Liste einmal durch, O(n).
