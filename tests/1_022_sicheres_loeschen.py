# Automatisch erzeugt aus lehrkraft/muster/1_022_sicheres_loeschen.py - nicht von Hand ändern.
# vorlage-hash: 3df91c58c03cff3c
# text-hash: 02c8443594ffbe49
# thema: kontrollfluss
# inhalt: for über range(n)

EINGABEN = ["3"]


def erwartete_ausgabe(anzahl):
    """Baut die Ausgabe für anzahl Durchgänge."""
    zeilen = [f"Sicheres Löschen mit {anzahl} Durchgängen"]
    nummer = 1
    while nummer <= anzahl:
        zeilen.append(f"Durchgang {nummer} von {anzahl}: Platte wird überschrieben")
        nummer = nummer + 1
    zeilen.append("Löschen abgeschlossen.")
    return "\n".join(zeilen)


def tipp_zu(ausgabe):
    """Gibt einen Tipp passend zur falschen Ausgabe, sonst einen leeren Text."""
    if "Durchgang 0 " in ausgabe:
        return "\nTipp: range(n) beginnt bei 0; schreiben Sie durchgang + 1 in die Ausgabe."
    if ausgabe.count("Löschen abgeschlossen.") > 1:
        return "\nTipp: Die Zeile „Löschen abgeschlossen.“ steht schon unter der Schleife; sie gehört nicht hinein."
    return ""


# Das Beispiel aus der Aufgabe: 3 Durchgänge
assert AUSGABE == erwartete_ausgabe(3), (
    f"Bei Eingabe 3 erwartet:\n{erwartete_ausgabe(3)}\nIhr Programm gibt aus:\n{AUSGABE}{tipp_zu(AUSGABE)}"
)

# Andere Anzahlen (nicht fest dreimal hinschreiben!)
for anzahl in [7, 2]:
    ausgabe = starte(str(anzahl))
    assert ausgabe == erwartete_ausgabe(anzahl), (
        f"Bei Eingabe {anzahl} erwartet:\n{erwartete_ausgabe(anzahl)}\nIhr Programm gibt aus:\n{ausgabe}"
        f"{tipp_zu(ausgabe)}\nTipp: Benutzen Sie range(anzahl), damit die Schleife so oft läuft wie eingegeben."
    )

# Ränder: 0, 1 und 35 Durchgänge
for anzahl in [0, 1, 35]:
    ausgabe = starte(str(anzahl))
    assert ausgabe == erwartete_ausgabe(anzahl), (
        f"Bei Eingabe {anzahl} erwartet:\n{erwartete_ausgabe(anzahl)}\nIhr Programm gibt aus:\n{ausgabe}{tipp_zu(ausgabe)}"
    )

# Eine for-Schleife wird benutzt
assert verwendet("for") and verwendet("range"), "Benutzen Sie für die Wiederholung for und range(...)."

# 40 zufällige Anzahlen von 0 bis 35
zufall = Zufall(1022)
for _ in range(40):
    anzahl = zufall.randint(0, 35)
    ausgabe = starte(str(anzahl))
    assert ausgabe == erwartete_ausgabe(anzahl), (
        f"Bei Eingabe {anzahl} erwartet:\n{erwartete_ausgabe(anzahl)}\nIhr Programm gibt aus:\n{ausgabe}{tipp_zu(ausgabe)}"
    )
