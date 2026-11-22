# Automatisch erzeugt aus lehrkraft/muster/3_042_ticketarten.py - nicht von Hand ändern.
# vorlage-hash: 661eada23fd36c4b
# text-hash: 9267a351111081b0
# thema: klassen
# inhalt: Vererbung mit super()

def klasse_da(name):
    """True, wenn es eine Klasse dieses Namens gibt, die von Ticket erbt."""
    klasse = globals().get(name)
    return isinstance(klasse, type) and issubclass(klasse, Ticket)


def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def erwartete_zeit(ticket):
    """Vergleichslösung: die Reaktionszeit nach Art und Priorität, aus einer Tabelle."""
    grund = {1: 4, 2: 8, 3: 24}[ticket.prioritaet]
    if type(ticket).__name__ == "Stoerung" and ticket.betroffene >= 50:
        return grund // 2
    if type(ticket).__name__ == "Serviceanfrage":
        return grund * 2
    return grund


def zufallsticket(zufall, nummer):
    """Ein zufälliges Ticket: Störung, Serviceanfrage oder gewöhnliches Ticket."""
    art = zufall.randint(1, 3)
    prioritaet = zufall.randint(1, 3)
    if art == 1:
        return Stoerung(nummer, "Ausfall", prioritaet, zufall.choice([0, 49, 50, zufall.randint(0, 100000)]))
    if art == 2:
        return Serviceanfrage(nummer, "Wunsch", prioritaet)
    return Ticket(nummer, "Sonstiges", prioritaet)


# Es gibt die Klassen Stoerung und Serviceanfrage, beide erben von Ticket
assert klasse_da("Stoerung") and klasse_da("Serviceanfrage"), (
    "Erwartet waren die Klassen Stoerung und Serviceanfrage, die von Ticket erben.\n"
    "Tipp: class Stoerung(Ticket): – die Elternklasse steht in Klammern hinter dem Namen."
)

# Stoerung speichert alle vier Attribute
s = wert_von(lambda: Stoerung(17, "Mailserver aus", 1, 120))
werte = wert_von(lambda: (s.nummer, s.beschreibung, s.prioritaet, s.betroffene))
assert werte == (17, "Mailserver aus", 1, 120), (
    f'Stoerung(17, "Mailserver aus", 1, 120) hat die Attribute {werte!r}, erwartet war (17, "Mailserver aus", 1, 120).\n'
    "Tipp: super().__init__(nummer, beschreibung, prioritaet) setzt die ersten drei, self.betroffene setzen Sie selbst."
)

# Stoerung.__init__ ruft super().__init__ auf
alter_init = Ticket.__init__


def init_mit_marke(self, *argumente, **schluesselwoerter):
    """Ruft das echte Ticket.__init__ auf und merkt am Objekt, dass es aufgerufen wurde."""
    alter_init(self, *argumente, **schluesselwoerter)
    self.ueber_ticket_angelegt = True


Ticket.__init__ = init_mit_marke
try:
    angelegt = wert_von(lambda: getattr(Stoerung(17, "Mailserver aus", 1, 120), "ueber_ticket_angelegt", False))
finally:
    Ticket.__init__ = alter_init
assert angelegt is True, (
    f"Stoerung(17, ...) ruft Ticket.__init__ nicht auf (ergab {angelegt!r}).\n"
    "Tipp: Rufen Sie in Stoerung.__init__ super().__init__(nummer, beschreibung, prioritaet) auf, statt die "
    "Attribute neu zu setzen."
)

# art() der beiden Unterklassen
arten = wert_von(lambda: (Stoerung(1, "x", 2, 0).art(), Serviceanfrage(2, "y", 2).art(), Ticket(3, "z", 2).art()))
assert arten == ("Störung", "Serviceanfrage", "Ticket"), (
    f"art() ergibt für Stoerung, Serviceanfrage und Ticket {arten!r}, erwartet war ('Störung', 'Serviceanfrage', 'Ticket')."
)

# __str__ funktioniert für beide Unterklassen
texte = wert_von(lambda: (str(Stoerung(17, "Mailserver aus", 1, 120)), str(Serviceanfrage(18, "Zweiter Bildschirm", 2))))
assert texte == ("#17 Störung: Mailserver aus (Priorität 1)", "#18 Serviceanfrage: Zweiter Bildschirm (Priorität 2)"), (
    f"str(...) ergibt {texte!r}, erwartet war ('#17 Störung: Mailserver aus (Priorität 1)', "
    "'#18 Serviceanfrage: Zweiter Bildschirm (Priorität 2)').\nTipp: __str__ ist geerbt; überschreiben Sie nur art()."
)

# Serviceanfrage: doppelte Reaktionszeit
zeiten = wert_von(lambda: [Serviceanfrage(1, "x", p).reaktionszeit() for p in [1, 2, 3]])
assert zeiten == [8, 16, 48], f"Serviceanfrage mit Priorität 1, 2, 3 hat die Reaktionszeiten {zeiten!r}, erwartet war [8, 16, 48]."

# Stoerung mit wenigen Betroffenen: gewöhnliche Reaktionszeit
zeiten = wert_von(lambda: [Stoerung(1, "x", p, 3).reaktionszeit() for p in [1, 2, 3]])
assert zeiten == [4, 8, 24], f"Stoerung mit 3 Betroffenen und Priorität 1, 2, 3 hat {zeiten!r}, erwartet war [4, 8, 24]."

# Stoerung mit vielen Betroffenen: halbe Reaktionszeit
zeiten = wert_von(lambda: [Stoerung(1, "x", p, 120).reaktionszeit() for p in [1, 2, 3]])
assert zeiten == [2, 4, 12], f"Stoerung mit 120 Betroffenen und Priorität 1, 2, 3 hat {zeiten!r}, erwartet war [2, 4, 12]."

# Stoerung genau an der Grenze: 50 Betroffene zählen schon, 49 noch nicht
zeiten = wert_von(lambda: [Stoerung(1, "x", 2, 49).reaktionszeit(), Stoerung(1, "x", 2, 50).reaktionszeit()])
assert zeiten == [8, 4], (
    f"Stoerung mit Priorität 2 und 49 bzw. 50 Betroffenen hat {zeiten!r}, erwartet war [8, 4].\n"
    "Tipp: „mindestens 50“ heißt >= 50."
)

# Die Reaktionszeit ist eine ganze Zahl
zeit = wert_von(lambda: Stoerung(1, "x", 1, 50).reaktionszeit())
assert zeit == 2 and type(zeit) is int, f"Stoerung(1, 'x', 1, 50).reaktionszeit() ergibt {zeit!r}, erwartet war die ganze Zahl 2 (mit //)."

# Die Unterklassen holen die gewöhnliche Reaktionszeit über super(), statt 4, 8 und 24 zu wiederholen
alte_zeit = Ticket.reaktionszeit
Ticket.reaktionszeit = lambda self: 10 * self.prioritaet
try:
    zeiten = wert_von(lambda: [Stoerung(1, "x", 3, 80).reaktionszeit(), Stoerung(1, "x", 3, 0).reaktionszeit(), Serviceanfrage(1, "y", 3).reaktionszeit()])
finally:
    Ticket.reaktionszeit = alte_zeit
assert zeiten == [15, 30, 60], (
    f"Werden die Zeiten in Ticket geändert (Priorität 3 → 30 Stunden), ergeben Stoerung mit 80 und mit 0 Betroffenen "
    f"und Serviceanfrage {zeiten!r}, erwartet war [15, 30, 60].\n"
    "Tipp: Rechnen Sie mit super().reaktionszeit(), statt die Stundenzahlen noch einmal hinzuschreiben."
)

# dringendstes im Beispiel
s = Stoerung(17, "Mailserver aus", 1, 120)
a = Serviceanfrage(18, "Zweiter Bildschirm", 2)
ergebnis = wert_von(lambda: dringendstes([a, s]))
assert ergebnis is s, f"dringendstes([anfrage, stoerung]) ergibt {ergebnis}, erwartet war die Störung #17."

# dringendstes mit gemischten Tickets (nicht fest hinschreiben!)
liste = [Stoerung(1, "Drucker", 3, 2), Ticket(2, "Frage", 2), Serviceanfrage(3, "Zugang", 1), Stoerung(4, "WLAN", 3, 60)]
ergebnis = wert_von(lambda: dringendstes(liste))
assert ergebnis is liste[1], (
    f"dringendstes ergibt {ergebnis}, erwartet war #2 Ticket mit 8 Stunden (vor #3 mit 16 und #4 mit 12 Stunden)."
)

# dringendstes bei Gleichstand: das erste
liste = [Serviceanfrage(1, "Maus", 3), Stoerung(2, "Telefon", 2, 0), Ticket(3, "Frage", 2), Stoerung(4, "Netz", 3, 500)]
ergebnis = wert_von(lambda: dringendstes(liste))
assert ergebnis is liste[1], (
    f"Bei drei Tickets mit 8 Stunden ergibt dringendstes {ergebnis}, erwartet war das erste davon, #2.\n"
    "Tipp: Ersetzen Sie das bisher dringendste nur bei einer echt kürzeren Reaktionszeit."
)

# dringendstes einer leeren Liste
ergebnis = wert_von(lambda: dringendstes([]))
assert ergebnis is None, f"dringendstes([]) ergibt {ergebnis!r}, erwartet war None."

# Die Ausgabe des Programms
erwartet = (
    "#17 Störung: Mailserver aus (Priorität 1) – 2 Stunden\n#18 Serviceanfrage: Zweiter Bildschirm (Priorität 2) – 16 Stunden\n"
    "Zuerst: #17 Störung: Mailserver aus (Priorität 1)"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Tickets und Listen
zufall = Zufall(3042)
for runde in range(200):
    liste = [zufallsticket(zufall, nummer) for nummer in range(zufall.randint(0, 8))]
    for ticket in liste:
        zeit = wert_von(ticket.reaktionszeit)
        assert zeit == erwartete_zeit(ticket), (
            f"{ticket} ({type(ticket).__name__}, betroffene={getattr(ticket, 'betroffene', '–')}) hat die Reaktionszeit "
            f"{zeit!r}, erwartet war {erwartete_zeit(ticket)}."
        )
    erwartet = None
    for ticket in liste:
        if erwartet is None or erwartete_zeit(ticket) < erwartete_zeit(erwartet):
            erwartet = ticket
    ergebnis = wert_von(lambda: dringendstes(liste))
    assert ergebnis is erwartet, f"dringendstes({[str(t) for t in liste]}) ergibt {ergebnis}, erwartet war {erwartet}."

# Obere Grenze: 10 000 Tickets, das dringendste ganz hinten
liste = [Serviceanfrage(nummer, "Wunsch", zufall.randint(1, 3)) for nummer in range(9999)] + [Stoerung(9999, "Netz", 1, 100000)]
ergebnis = wert_von(lambda: dringendstes(liste))
assert ergebnis is liste[-1], f"Bei 10 000 Tickets ergibt dringendstes {ergebnis}, erwartet war die Störung #9999 ganz hinten."
