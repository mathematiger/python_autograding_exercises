# Automatisch erzeugt aus lehrkraft/muster/1_034_portliste.py - nicht von Hand ändern.
# vorlage-hash: 0e9a41750e601ff4
# text-hash: 70f89d4f93885760
# thema: kontrollfluss
# inhalt: Eingabeschleife bis stop

EINGABEN = ["22", "443", "8080", "3306", "stop"]


def erwartete_ausgabe(ports):
    """Zählt mit for statt while, wie viele Ports es sind und wie viele davon unter 1024 liegen."""
    unter = 0
    for port in ports:
        if port <= 1023:
            unter = unter + 1
    return f"{len(ports)} Ports eingegeben, davon {unter} Well-known-Ports."


def lauf(ports):
    """Startet das Programm mit diesen Ports und stop; liefert die Ausgabe oder eine Beschreibung des Abbruchs."""
    try:
        return starte(*[str(port) for port in ports], "stop")
    except Exception as fehler:
        return f"(Abbruch: {fehler})"


def hinweis_zu(ausgabe, ports):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if "Abbruch" in ausgabe and "ValueError" in ausgabe:
        return '\nTipp: Prüfen Sie in der Bedingung, ob die Eingabe "stop" ist, bevor Sie sie mit int(...) umwandeln.'
    if "Abbruch" in ausgabe:
        return "\nTipp: Lesen Sie am Ende des Schleifenblocks die nächste Eingabe, und beenden Sie die Schleife bei stop."
    if ausgabe.count("Ports eingegeben") > 1:
        return "\nTipp: Die Ergebniszeile steht schon unter der Schleife; rücken Sie in die Schleife nur ein, was sich wiederholen soll."
    if 1023 in ports or 1024 in ports:
        return "\nTipp: Well-known sind die Ports 0 bis 1023, also port < 1024 (1023 zählt mit, 1024 nicht)."
    return ""


def meldung(ports, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    eingaben = ", ".join([str(port) for port in ports] + ["stop"])
    return (
        f"Bei den Eingaben {eingaben} erwartet:\n{erwartete_ausgabe(ports)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, ports)}"
    )


# Im Beispiel werden 4 Ports gezählt (die Well-known-Ports zählen hier noch nicht)
assert vergleichbar("4 Ports eingegeben") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 22, 443, 8080, 3306, stop erwartet: "4 Ports eingegeben, …" – Ihr Programm: "{AUSGABE}"\n'
    "Tipp: Zählen Sie anzahl in der Schleife bei jedem Port um 1 hoch."
)

# Das Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe([22, 443, 8080, 3306])), meldung([22, 443, 8080, 3306], AUSGABE)

# Andere Ports (nicht fest hinschreiben!)
ports = [80, 25, 53, 5432, 110, 27017]
ausgabe = lauf(ports)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(ports)), meldung(ports, ausgabe)

# Nur ein einziger Port
ports = [8443]
ausgabe = lauf(ports)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(ports)), meldung(ports, ausgabe)

# Gleich stop: keine Ports
ausgabe = lauf([])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([])), meldung([], ausgabe)

# Grenze der Well-known-Ports: 1023 zählt mit, 1024 nicht
ports = [1023, 1024]
ausgabe = lauf(ports)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(ports)), meldung(ports, ausgabe)

# Ränder des Wertebereichs: Port 0 und Port 65535
ports = [0, 65535]
ausgabe = lauf(ports)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(ports)), meldung(ports, ausgabe)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# 40 zufällige Portlisten
zufall = Zufall(1034)
for _ in range(40):
    ports = [zufall.choice([zufall.randint(0, 1023), zufall.randint(1024, 65535)]) for _ in range(zufall.randint(0, 12))]
    ausgabe = lauf(ports)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(ports)), meldung(ports, ausgabe)

# Obere Grenze: 50 Ports
ports = [(nummer * 1999) % 65536 for nummer in range(50)]
ausgabe = lauf(ports)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(ports)), meldung(ports, ausgabe)
