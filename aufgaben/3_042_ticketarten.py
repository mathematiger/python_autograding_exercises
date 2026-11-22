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


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def dringendstes(tickets):
    """Gibt das Ticket mit der kürzesten Reaktionszeit zurück, bei Gleichstand das erste, sonst None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


stoerung = Stoerung(17, "Mailserver aus", 1, 120)
anfrage = Serviceanfrage(18, "Zweiter Bildschirm", 2)
print(stoerung, "–", stoerung.reaktionszeit(), "Stunden")
print(anfrage, "–", anfrage.reaktionszeit(), "Stunden")
print("Zuerst:", dringendstes([anfrage, stoerung]))
