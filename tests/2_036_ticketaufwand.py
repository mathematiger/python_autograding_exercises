# Automatisch erzeugt aus lehrkraft/muster/2_036_ticketaufwand.py - nicht von Hand ändern.
# vorlage-hash: 53893d32df443ea6
# text-hash: 4e8e06dfeded82be
# thema: fehler
# inhalt: Übung: Fehler abfangen

def beispiel():
    """Baut die Tickets aus der Aufgabe neu."""
    return [
        {"nummer": "T-101", "kategorie": "Drucker", "minuten": "35"},
        {"nummer": "T-102", "kategorie": "Netzwerk", "minuten": "50"},
        {"nummer": "T-103", "kategorie": "Drucker", "minuten": "ca. 20"},
        {"nummer": "T-104", "kategorie": "Drucker", "minuten": "15"},
        {"nummer": "T-105", "minuten": "40"},
    ]


def rufe_auf(tickets):
    """Ruft aufwand_je_kategorie(tickets) auf und liefert das Ergebnis und eine aufgetretene Ausnahme (sonst None)."""
    try:
        return aufwand_je_kategorie(tickets), None
    except Exception as ausnahme:
        return None, ausnahme


def meldung(tickets, ergebnis, fehler, erwartet):
    """Baut die Fehlermeldung; nennt eine aufgetretene Ausnahme mit einem passenden Tipp."""
    if isinstance(fehler, KeyError):
        return (
            f"aufwand_je_kategorie({tickets!r}) ist mit KeyError {fehler} abgestürzt, erwartet war {erwartet!r}.\n"
            "Tipp: Fehlt ein Feld, löst ticket[...] einen KeyError aus. Fangen Sie ihn zusammen mit dem ValueError "
            "ab: except (KeyError, ValueError):"
        )
    if fehler is not None:
        return (
            f"aufwand_je_kategorie({tickets!r}) ist mit {type(fehler).__name__} abgestürzt, erwartet war "
            f"{erwartet!r}.\nTipp: Lesen Sie die Felder jedes Tickets in der Schleife in einem try-Block, wandeln "
            "Sie die Minuten mit int(...) um und fangen Sie die Fehler mit except (KeyError, ValueError): ab."
        )
    text = f"aufwand_je_kategorie({tickets!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    if type(ergebnis) is tuple and len(ergebnis) == 2 and ergebnis[0] == erwartet[0]:
        text = text + "\nTipp: Tickets ohne 'kategorie' oder ohne 'minuten' zählen auch als unbrauchbar."
    return text


def von_hand(tickets):
    """Vergleichslösung ohne try: prüft Felder und Ziffern selbst, sammelt erst alle Kategorien."""
    brauchbare = []
    for ticket in tickets:
        if "kategorie" not in ticket or "minuten" not in ticket:
            continue
        # "-0" ist für int die Zahl 0
        ziffern = ticket["minuten"].strip().removeprefix("-")
        if ziffern != "" and all(zeichen in "0123456789" for zeichen in ziffern):
            brauchbare.append((ticket["kategorie"], int(ziffern)))
    summen = {}
    for kategorie in sorted(set(kategorie for kategorie, _ in brauchbare)):
        summen[kategorie] = sum(minuten for name, minuten in brauchbare if name == kategorie)
    return summen, len(tickets) - len(brauchbare)


# Das Beispiel aus der Aufgabe
ergebnis, fehler = rufe_auf(beispiel())
erwartet = ({"Drucker": 50, "Netzwerk": 50}, 2)
assert fehler is None and ergebnis == erwartet, meldung(beispiel(), ergebnis, fehler, erwartet)

# Ohne Tickets
ergebnis, fehler = rufe_auf([])
assert fehler is None and ergebnis == ({}, 0), meldung([], ergebnis, fehler, ({}, 0))

# Nur brauchbare Tickets (nicht fest hinschreiben!)
tickets = [
    {"kategorie": "Software", "minuten": "10"},
    {"kategorie": "Hardware", "minuten": "25"},
    {"kategorie": "Software", "minuten": "5"},
    {"kategorie": "Software", "minuten": "0"},
]
erwartet = ({"Software": 15, "Hardware": 25}, 0)
ergebnis, fehler = rufe_auf(tickets)
assert fehler is None and ergebnis == erwartet, meldung(tickets, ergebnis, fehler, erwartet)

# Minuten, die int nicht umwandeln kann, machen ein Ticket unbrauchbar
tickets = [
    {"kategorie": "Drucker", "minuten": "ca. 20"},
    {"kategorie": "Drucker", "minuten": "1,5 h"},
    {"kategorie": "Drucker", "minuten": ""},
    {"kategorie": "Drucker", "minuten": "12.5"},
    {"kategorie": "Drucker", "minuten": "30"},
]
erwartet = ({"Drucker": 30}, 4)
ergebnis, fehler = rufe_auf(tickets)
assert fehler is None and ergebnis == erwartet, meldung(tickets, ergebnis, fehler, erwartet)

# Ein fehlendes Feld macht ein Ticket unbrauchbar, statt die Auswertung abzubrechen
tickets = [
    {"nummer": "T-1", "minuten": "40"},
    {"nummer": "T-2", "kategorie": "Netzwerk"},
    {"nummer": "T-3"},
    {"nummer": "T-4", "kategorie": "Netzwerk", "minuten": "20"},
]
erwartet = ({"Netzwerk": 20}, 3)
ergebnis, fehler = rufe_auf(tickets)
assert fehler is None and ergebnis == erwartet, meldung(tickets, ergebnis, fehler, erwartet)

# Eine Kategorie, die nur in kaputten Tickets vorkommt, fehlt im Dictionary
tickets = [{"kategorie": "Telefon", "minuten": "n/a"}, {"kategorie": "Mail", "minuten": "7"}]
erwartet = ({"Mail": 7}, 1)
ergebnis, fehler = rufe_auf(tickets)
assert fehler is None and ergebnis == erwartet, (
    meldung(tickets, ergebnis, fehler, erwartet)
    + "\nTipp: Tragen Sie eine Kategorie erst ein, wenn ihre Minuten sich umwandeln ließen."
)

# Lauter kaputte Tickets
tickets = [{"minuten": "5"}, {"kategorie": "Drucker", "minuten": "fünf"}, {}]
ergebnis, fehler = rufe_auf(tickets)
assert fehler is None and ergebnis == ({}, 3), meldung(tickets, ergebnis, fehler, ({}, 3))

# Leerzeichen um die Minuten stören nicht
tickets = [{"kategorie": "VPN", "minuten": " 30 "}, {"kategorie": "VPN", "minuten": "  5"}]
ergebnis, fehler = rufe_auf(tickets)
assert fehler is None and ergebnis == ({"VPN": 35}, 0), meldung(tickets, ergebnis, fehler, ({"VPN": 35}, 0))

# Die Summen sind ganze Zahlen
ergebnis, fehler = rufe_auf([{"kategorie": "VPN", "minuten": "30"}])
assert fehler is None and ergebnis == ({"VPN": 30}, 0) and type(ergebnis[0]["VPN"]) is int, (
    meldung([{"kategorie": "VPN", "minuten": "30"}], ergebnis, fehler, ({"VPN": 30}, 0))
    + "\nTipp: Wandeln Sie die Minuten mit int(...) um, bevor Sie sie addieren."
)

# Die Tickets bleiben unverändert
tickets = beispiel()
aufwand_je_kategorie(tickets)
assert tickets == beispiel(), (
    f"Nach dem Aufruf sind die Tickets {tickets!r}; sie sollen unverändert bleiben.\n"
    "Tipp: Lesen Sie die Felder nur, statt Tickets aus der Liste zu entfernen oder Felder zu ändern."
)

# Es wird mit try und except gearbeitet
assert verwendet("try"), (
    "Lesen Sie die Felder in einem try-Block, wandeln Sie die Minuten um und fangen Sie die Fehler mit except ab."
)


# Ein int mit einem ganz anderen Fehler: Der soll nicht verschluckt werden
def kaputtes_int(text):
    """Tut so, als hätte das Programm einen Fehler, der mit den Tickets nichts zu tun hat."""
    raise TypeError("ein anderer Fehler")


# Nur KeyError und ValueError werden abgefangen, andere Fehler werden weitergemeldet
try:
    int = kaputtes_int
    ergebnis, fehler = rufe_auf([{"kategorie": "VPN", "minuten": "30"}])
finally:
    del int
assert isinstance(fehler, TypeError), (
    f"Wenn in int(...) ein TypeError auftritt, ergibt die Auswertung {ergebnis!r}; erwartet war, dass der "
    "TypeError weitergemeldet wird.\n"
    "Tipp: Schreiben Sie except (KeyError, ValueError): statt nur except: oder except Exception:, damit Sie "
    "nur die Fehler abfangen, mit denen Sie rechnen."
)

# Die Ausgabe des Programms stimmt (die Reihenfolge der Kategorien legt die Aufgabe nicht fest)
erlaubte_ausgaben = ["({'Drucker': 50, 'Netzwerk': 50}, 2)", "({'Netzwerk': 50, 'Drucker': 50}, 2)"]
assert vergleichbar(AUSGABE) in [vergleichbar(ausgabe) for ausgabe in erlaubte_ausgaben], f"Erwartete Ausgabe:\n{erlaubte_ausgaben[0]}\nIhr Programm gibt aus:\n{AUSGABE}"

# 300 zufällige Monate, brauchbare und kaputte Tickets gemischt
zufall = Zufall(2036)
kategorien = ["Drucker", "Netzwerk", "Software", "Hardware", "Konto"]
kaputte_minuten = ["", " ", "ca. 20", "1,5 h", "12.5", "n/a", "-", "zehn", "30 min"]
for _ in range(300):
    tickets = []
    for nummer in range(zufall.randint(0, 8)):
        ticket = {"nummer": f"T-{nummer}"}
        if zufall.random() < 0.9:
            ticket["kategorie"] = zufall.choice(kategorien)
        wahl = zufall.random()
        if wahl < 0.15:
            ticket["minuten"] = zufall.choice(kaputte_minuten)
        elif wahl < 0.9:
            ticket["minuten"] = " " * zufall.randint(0, 1) + str(zufall.randint(0, 10000))
        tickets.append(ticket)
    ergebnis, fehler = rufe_auf(tickets)
    erwartet = von_hand(tickets)
    assert fehler is None and ergebnis == erwartet, meldung(tickets, ergebnis, fehler, erwartet)

# An der oberen Grenze: 10 000 Tickets mit je 10 000 Minuten
tickets = []
for nummer in range(10000):
    if nummer % 4 == 0:
        tickets.append({"kategorie": kategorien[nummer % 5], "minuten": "x" * 30})
    else:
        tickets.append({"kategorie": kategorien[nummer % 5], "minuten": "10000"})
ergebnis, fehler = rufe_auf(tickets)
erwartet = von_hand(tickets)
assert fehler is None and ergebnis == erwartet, (
    f"Bei 10 000 Tickets ergibt sich {ergebnis!r}, erwartet war {erwartet!r}."
    + ("" if fehler is None else f"\nDie Funktion ist mit {type(fehler).__name__} abgestürzt.")
)
