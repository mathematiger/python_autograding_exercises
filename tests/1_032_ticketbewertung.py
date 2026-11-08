# Automatisch erzeugt aus lehrkraft/muster/1_032_ticketbewertung.py - nicht von Hand ändern.
# vorlage-hash: c0384a70363299dc
# text-hash: 1ef24fbcf69b2991
# thema: datenstrukturen
# inhalt: Übung: Listen

EINGABEN = ["5,2,4,1,5,3"]


def erwartete_ausgabe(werte):
    """Baut die erwartete Ausgabe mit einer while-Schleife statt for."""
    schlechte = []
    summe = 0
    nummer = 1
    while nummer <= len(werte):
        summe = summe + werte[nummer - 1]
        if werte[nummer - 1] < 3:
            schlechte.append(nummer)
        nummer = nummer + 1
    return (
        f"{len(werte)} Bewertungen, Durchschnitt: {summe / len(werte):.2f}\n"
        f"Schlechteste: {min(werte)}, beste: {max(werte)}\n"
        f"Nachfassen bei Ticket: {schlechte}"
    )


def hinweis_zu(ausgabe, werte):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    ab_null = [stelle for stelle in range(len(werte)) if werte[stelle] <= 2]
    nur_eins = [stelle + 1 for stelle in range(len(werte)) if werte[stelle] < 2]
    schlechte_werte = [wert for wert in werte if wert <= 2]
    zeile = ausgabe.split("\n")[-1]
    if ab_null and zeile == f"Nachfassen bei Ticket: {ab_null}":
        return "\nTipp: Die Tickets zählen ab 1, die Liste ab 0. Hängen Sie stelle + 1 an, nicht stelle."
    if 2 in werte and zeile == f"Nachfassen bei Ticket: {nur_eins}":
        return "\nTipp: Auch eine Bewertung von genau 2 heißt nachfassen; vergleichen Sie mit <= 2."
    if schlechte_werte and zeile == f"Nachfassen bei Ticket: {schlechte_werte}":
        return "\nTipp: In die Liste gehören die Nummern der Tickets, nicht die Bewertungen selbst."
    if "'" in ausgabe:
        return "\nTipp: Hängen Sie int(teil) an, nicht den Text teil; sonst rechnet Python mit Texten."
    return ""


def meldung(werte, ausgabe):
    """Baut die Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    text = ",".join(str(wert) for wert in werte)
    return (
        f"Bei der Eingabe {text} erwartet:\n{erwartete_ausgabe(werte)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, werte)}"
    )


def pruefe_lauf(werte):
    """Startet das Programm mit diesen Bewertungen; liefert die Ausgabe oder eine Beschreibung des Abbruchs."""
    try:
        return starte(",".join(str(wert) for wert in werte))
    except Exception as fehler:
        return f"(Abbruch: {fehler})"


# Das Beispiel aus der Aufgabe
BEISPIEL = [5, 2, 4, 1, 5, 3]
assert AUSGABE == erwartete_ausgabe(BEISPIEL), meldung(BEISPIEL, AUSGABE)

# Andere Bewertungen (nicht fest hinschreiben!)
werte = [1, 4, 4, 2, 2, 5, 3]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# Alle zufrieden: niemand zum Nachfassen
werte = [5, 4, 3, 5]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# Alle unzufrieden, auch das erste und das letzte Ticket
werte = [2, 1, 1, 2]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# Nur ein einziges Ticket
werte = [1]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# append wird benutzt
assert verwendet("append"), "Bauen Sie die Listen bewertungen und nachfassen mit append auf."

# 40 zufällige Wochen
zufall = Zufall(1032)
for _ in range(40):
    werte = [zufall.randint(1, 5) for _ in range(zufall.randint(1, 15))]
    ausgabe = pruefe_lauf(werte)
    assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# Obere Grenze: 50 Bewertungen
werte = [(zahl * 3) % 5 + 1 for zahl in range(50)]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)
