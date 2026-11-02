# Automatisch erzeugt aus lehrkraft/muster/2_022_reaktionsfristen.py - nicht von Hand ändern.
# vorlage-hash: 373186c9ace65a7f
# text-hash: 49cd3f4e42d7b394
# thema: kontrollfluss
# inhalt: zip

tickets = ["T-101", "T-102", "T-103", "T-104"]
fristen = [60, 240, 30, 240]
reaktion = [45, 300, 30, 250]

# anzahl_verletzt aus dem Beispiel
ergebnis = anzahl_verletzt(fristen, reaktion)
assert ergebnis == 2, (
    f"anzahl_verletzt({fristen}, {reaktion}) ergibt {ergebnis!r}, erwartet war 2.\n"
    "Tipp: Vergleichen Sie jede Reaktionszeit mit der Frist an derselben Stelle; genau die Frist ist noch eingehalten."
)

# ueberzogen aus dem Beispiel
ergebnis = ueberzogen(tickets, fristen, reaktion)
erwartet = [("T-102", 60), ("T-104", 10)]
assert ergebnis == erwartet, (
    f"ueberzogen(tickets, fristen, reaktion) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: minuten ist reaktion - frist, also wie viel zu spät reagiert wurde."
)

# Genau an der Frist und eine Minute darüber
for frist, zeit, erwartet in [(30, 30, []), (30, 31, [("A", 1)]), (0, 0, []), (0, 1, [("A", 1)]), (100000, 0, [])]:
    ergebnis = ueberzogen(["A"], [frist], [zeit])
    anzahl = anzahl_verletzt([frist], [zeit])
    assert ergebnis == erwartet and anzahl == len(erwartet), (
        f"Frist {frist}, Reaktion {zeit}: ueberzogen ergibt {ergebnis!r} und anzahl_verletzt {anzahl!r}, "
        f"erwartet waren {erwartet} und {len(erwartet)}.\nTipp: Verletzt ist das SLA nur bei reaktion > frist."
    )

# Die Reihenfolge der Argumente: erst fristen, dann reaktion
ergebnis = anzahl_verletzt([10, 100], [50, 20])
assert ergebnis == 1, (
    f"anzahl_verletzt([10, 100], [50, 20]) ergibt {ergebnis!r}, erwartet war 1 (nur das erste Ticket ist zu spät).\n"
    "Tipp: Der erste Parameter sind die Fristen, der zweite die Reaktionszeiten."
)

# Leere Listen
assert anzahl_verletzt([], []) == 0 and ueberzogen([], [], []) == [], (
    f"Ohne Tickets erwartet 0 und [], bekommen {anzahl_verletzt([], [])!r} und {ueberzogen([], [], [])!r}."
)

# Alle Tickets zu spät
ergebnis = ueberzogen(["X", "Y", "Z"], [1, 2, 3], [100000, 100000, 100000])
erwartet = [("X", 99999), ("Y", 99998), ("Z", 99997)]
assert ergebnis == erwartet, f"ueberzogen bei drei verspäteten Tickets ergibt {ergebnis!r}, erwartet war {erwartet}."

# Die Listen bleiben unverändert
kopie = (list(tickets), list(fristen), list(reaktion))
anzahl_verletzt(fristen, reaktion)
ueberzogen(tickets, fristen, reaktion)
assert (tickets, fristen, reaktion) == kopie, "anzahl_verletzt und ueberzogen sollen die Listen nicht verändern."

# zip wird benutzt
assert verwendet("zip"), "Benutzen Sie für diese Aufgabe zip."


# Vergleichslösung mit Indizes
def ueberzogen_von_hand(tickets, fristen, reaktion):
    """Geht die Positionen mit range durch."""
    gefunden = []
    for i in range(len(tickets)):
        if reaktion[i] > fristen[i]:
            gefunden.append((tickets[i], reaktion[i] - fristen[i]))
    return gefunden


# 300 zufällige Ticketlisten
zufall = Zufall(2022)
for _ in range(300):
    laenge = zufall.randint(0, 8)
    namen = [f"T-{nummer}" for nummer in zufall.sample(range(100, 1000), laenge)]
    frist_liste = [zufall.choice([0, 15, 30, 60, 240]) for _ in range(laenge)]
    zeit_liste = [zufall.randint(0, 300) for _ in range(laenge)]
    erwartet = ueberzogen_von_hand(namen, frist_liste, zeit_liste)
    ergebnis = ueberzogen(namen, frist_liste, zeit_liste)
    assert ergebnis == erwartet, f"ueberzogen({namen}, {frist_liste}, {zeit_liste}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    anzahl = anzahl_verletzt(frist_liste, zeit_liste)
    assert anzahl == len(erwartet), (
        f"anzahl_verletzt({frist_liste}, {zeit_liste}) ergibt {anzahl!r}, erwartet war {len(erwartet)}."
    )

# An der oberen Grenze: 100 000 Tickets
namen = [f"T-{nummer}" for nummer in range(100000)]
frist_liste = [(nummer * 7) % 100001 for nummer in range(100000)]
zeit_liste = [(nummer * 13) % 100001 for nummer in range(100000)]
erwartet = ueberzogen_von_hand(namen, frist_liste, zeit_liste)
ergebnis = ueberzogen(namen, frist_liste, zeit_liste)
anzahl = anzahl_verletzt(frist_liste, zeit_liste)
assert ergebnis == erwartet and anzahl == len(erwartet), (
    f"Bei 100 000 Tickets liefert ueberzogen {len(ergebnis)} Einträge, die ersten {ergebnis[:2]}, und anzahl_verletzt "
    f"{anzahl!r}; erwartet waren {len(erwartet)} Einträge, die ersten {erwartet[:2]}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "2\n[('T-102', 60), ('T-104', 10)]"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
