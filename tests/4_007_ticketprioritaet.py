# Automatisch erzeugt aus lehrkraft/muster/4_007_ticketprioritaet.py - nicht von Hand ändern.
# vorlage-hash: c53d26a2e4c6c04f
# thema: klassen
# inhalt: `staticmethod` als Hilfsfunktion

# berechne_prioritaet folgt der Prioritätenmatrix
matrix = {
    (1, 1): 1, (1, 2): 2, (1, 3): 3,
    (2, 1): 2, (2, 2): 3, (2, 3): 4,
    (3, 1): 3, (3, 2): 4, (3, 3): 5,
}
for (auswirkung, dringlichkeit), erwartet in matrix.items():
    ergebnis = Ticket.berechne_prioritaet(auswirkung, dringlichkeit)
    assert ergebnis == erwartet, (
        f"Ticket.berechne_prioritaet({auswirkung}, {dringlichkeit}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    )

# Werte außerhalb von 1 bis 3 lösen ValueError aus
for auswirkung, dringlichkeit in [(0, 2), (2, 0), (4, 1), (1, 4), (-1, 3)]:
    try:
        ergebnis = Ticket.berechne_prioritaet(auswirkung, dringlichkeit)
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    assert fehler is not None, (
        f"Ticket.berechne_prioritaet({auswirkung}, {dringlichkeit}) muss einen ValueError auslösen, ergab aber {ergebnis!r}.\n"
        "Tipp: Prüfen Sie beide Werte, bevor Sie rechnen."
    )

# ist_ticketnummer ist eine statische Methode
assert isinstance(Ticket.__dict__.get("ist_ticketnummer"), staticmethod), (
    "In der Klasse Ticket gibt es keine statische Methode ist_ticketnummer.\n"
    "Tipp: Schreiben Sie @staticmethod in die Zeile über def ist_ticketnummer(text):"
)

# Gültige Ticketnummern werden erkannt
for text in ["INC004711", "INC000000", "INC999999"]:
    ergebnis = Ticket.ist_ticketnummer(text)
    assert ergebnis is True, f"Ticket.ist_ticketnummer({text!r}) ergibt {ergebnis!r}, erwartet war True."

# Ungültige Ticketnummern werden erkannt
for text in ["INC4711", "INC0047110", "REQ004711", "inc004711", "INC00471A", "INC-04711", "INC", "", "004711INC"]:
    ergebnis = Ticket.ist_ticketnummer(text)
    assert ergebnis is False, (
        f"Ticket.ist_ticketnummer({text!r}) ergibt {ergebnis!r}, erwartet war False.\n"
        "Tipp: Gültig ist nur INC mit genau sechs Ziffern dahinter, also neun Zeichen insgesamt."
    )

# Statische Methoden lassen sich auch über ein Objekt aufrufen
ticket = Ticket("INC000123", 3, 2)
try:
    ergebnis = (ticket.ist_ticketnummer("INC000001"), ticket.berechne_prioritaet(2, 2))
    fehler = None
except TypeError as ausnahme:
    ergebnis = None
    fehler = ausnahme
assert fehler is None and ergebnis == (True, 3), (
    "ticket.ist_ticketnummer('INC000001') und ticket.berechne_prioritaet(2, 2) müssen True und 3 ergeben; "
    f"Ergebnis: {ergebnis!r}, aufgetretene Ausnahme: {fehler!r}.\n"
    "Tipp: Ohne @staticmethod übergibt Python das Objekt als ersten Parameter."
)

# __init__ speichert Nummer und Priorität
for nummer, auswirkung, dringlichkeit, prioritaet in [
    ("INC004711", 2, 1, 2),
    ("INC000123", 3, 2, 4),
    ("INC555555", 1, 1, 1),
    ("INC100000", 3, 3, 5),
]:
    ticket = Ticket(nummer, auswirkung, dringlichkeit)
    assert (ticket.nummer, ticket.prioritaet) == (nummer, prioritaet), (
        f"Ticket({nummer!r}, {auswirkung}, {dringlichkeit}) hat nummer={getattr(ticket, 'nummer', None)!r} "
        f"und prioritaet={getattr(ticket, 'prioritaet', None)!r}, erwartet waren {nummer!r} und {prioritaet}."
    )

# Die vorgegebene Reaktionszeit passt zur Priorität
ticket = Ticket("INC000042", 1, 3)
assert ticket.reaktionszeit() == 8, (
    f"Ticket('INC000042', 1, 3).reaktionszeit() ergibt {ticket.reaktionszeit()!r}, erwartet war 8 (Priorität 3)."
)

# Eine ungültige Ticketnummer löst im Konstruktor ValueError aus
for nummer in ["REQ004711", "INC47"]:
    try:
        ticket = Ticket(nummer, 2, 1)
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    assert fehler is not None, (
        f"Ticket({nummer!r}, 2, 1) muss einen ValueError auslösen, ergab aber ein Ticket.\n"
        "Tipp: Prüfen Sie die Nummer in __init__ mit self.ist_ticketnummer(nummer)."
    )

# Ungültige Auswirkung oder Dringlichkeit lösen im Konstruktor ValueError aus
try:
    ticket = Ticket("INC004711", 2, 7)
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
assert fehler is not None, (
    "Ticket('INC004711', 2, 7) muss einen ValueError auslösen, weil die Dringlichkeit 7 nicht erlaubt ist.\n"
    "Tipp: Berechnen Sie die Priorität in __init__ mit self.berechne_prioritaet(...)."
)

# Werte an den Rändern der Grenzen
ergebnisse = []
for auswirkung, dringlichkeit in [(-100, 1), (1, 100), (100, -100)]:
    try:
        ergebnisse.append(Ticket.berechne_prioritaet(auswirkung, dringlichkeit))
    except ValueError:
        ergebnisse.append("ValueError")
nummer_lang = Ticket.ist_ticketnummer("INC" + "0" * 17)
assert ergebnisse == ["ValueError"] * 3 and nummer_lang is False, (
    "berechne_prioritaet(-100, 1), (1, 100) und (100, -100) sollen ValueError auslösen und "
    f"ist_ticketnummer('INC' + 17 Nullen) False ergeben; bekommen {ergebnisse} und {nummer_lang!r}."
)

# Viele zufällige Paare: Priorität aus der Matrix oder ValueError
zufall = Zufall(4007)
matrix = {(a, d): a + d - 1 for a in (1, 2, 3) for d in (1, 2, 3)}
fehlerfall = None
for versuch in range(500):
    auswirkung, dringlichkeit = zufall.randint(-3, 6), zufall.randint(-3, 6)
    try:
        bekommen = Ticket.berechne_prioritaet(auswirkung, dringlichkeit)
    except ValueError:
        bekommen = "ValueError"
    erwartet = matrix.get((auswirkung, dringlichkeit), "ValueError")
    if bekommen != erwartet:
        fehlerfall = f"Ticket.berechne_prioritaet({auswirkung}, {dringlichkeit}) ergibt {bekommen!r}, erwartet war {erwartet!r}."
        break
assert fehlerfall is None, fehlerfall

# Viele zufällige Texte, die fast wie Ticketnummern aussehen
zufall = Zufall(40072)
fehlerfall = None
for versuch in range(1000):
    anfang = zufall.choice(["INC", "INC", "INC", "inc", "IN", "REQ", "INCC", ""])
    rest = "".join(zufall.choice("0123456789" * 5 + "A -") for _ in range(zufall.randint(4, 8)))
    text = anfang + rest
    erwartet = len(text) == 9 and text.startswith("INC") and all(zeichen in "0123456789" for zeichen in text[3:])
    bekommen = Ticket.ist_ticketnummer(text)
    if bekommen is not erwartet:
        fehlerfall = f"Ticket.ist_ticketnummer({text!r}) ergibt {bekommen!r}, erwartet war {erwartet}."
        break
assert fehlerfall is None, fehlerfall

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "2\nTrue False\nTicket('INC004711', Priorität 2) 4"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
