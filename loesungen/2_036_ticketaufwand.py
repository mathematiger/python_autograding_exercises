# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_036_ticketaufwand.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_036_ticketaufwand

"""Aufgabe 2_036 – Ticketaufwand                                 Stufe 2 ★★☆☆☆

Der IT-Support einer Firma will wissen, in welchen Bereichen die meiste
Arbeitszeit steckt. Das Ticketsystem exportiert dafür alle erledigten
Tickets eines Monats als Liste von Dictionaries. Ein Ticket hat
normalerweise eine Kategorie und den Aufwand in ganzen Minuten. Der Export
schreibt alle Werte als Text und lässt leere Felder ganz weg:

    tickets = [
        {"nummer": "T-101", "kategorie": "Drucker", "minuten": "35"},
        {"nummer": "T-102", "kategorie": "Netzwerk", "minuten": "50"},
        {"nummer": "T-103", "kategorie": "Drucker", "minuten": "ca. 20"},
        {"nummer": "T-104", "kategorie": "Drucker", "minuten": "15"},
        {"nummer": "T-105", "minuten": "40"},
    ]

Der Export ist nicht sauber: Mal steht im Aufwand keine ganze Zahl
("ca. 20", "1,5 h", ein leerer Text), mal fehlt ein Feld ganz, wie die
Kategorie bei T-105. Solche unbrauchbaren Tickets werden nicht
mitgerechnet, sondern nur gezählt, damit jemand sie nachpflegt.

Vervollständigen Sie die Funktion `aufwand_je_kategorie(tickets)`. Sie gibt
ein Tupel aus zwei Werten zurück:

- ein Dictionary, das jeder Kategorie die Summe der Minuten ihrer
  brauchbaren Tickets zuordnet. Eine Kategorie, die nur in unbrauchbaren
  Tickets vorkommt, steht nicht darin.
- die Zahl der unbrauchbaren Tickets: Tickets ohne "kategorie" oder ohne
  "minuten" und Tickets, deren Minuten int(...) nicht umwandeln kann.

    aufwand_je_kategorie(tickets)  →  ({"Drucker": 50, "Netzwerk": 50}, 2)
    aufwand_je_kategorie([])       →  ({}, 0)

Die übergebene Liste und ihre Dictionaries bleiben unverändert.

Grenzen: 0 ≤ len(tickets) ≤ 10 000. Jedes Ticket ist ein Dictionary, dessen
Schlüssel und Werte Texte mit höchstens 30 Zeichen sind; außer "kategorie"
und "minuten" kann es weitere Felder haben. Eine vorhandene Kategorie ist
nicht leer. Lassen sich die Minuten umwandeln, sind sie eine ganze Zahl von
0 bis 10 000; sonst bestehen sie aus den Ziffern 0 bis 9, Buchstaben,
Leerzeichen und den Zeichen ".", "," und "-".

Hintergrund: Diese Übung verbindet die letzten Aufgaben.

tickets ist eine Tabelle als Liste von Dictionaries (Aufgabe 2_032). Fehlt
beim Lesen eines Felds der Schlüssel, löst das einen KeyError aus (Aufgabe
2_025).

Mit try und except fangen Sie Fehler ab (Aufgabe 2_033). Steht das try in
der Schleife, gilt es für jedes Ticket einzeln (Aufgabe 2_034). Mehrere
Arten von Ausnahmen fangen Sie mit einem einzigen except ab (Aufgabe
2_035).

Summen je Schlüssel sammeln Sie in einem Dictionary wie beim Zählen
(Aufgaben 2_025 und 2_026), und zwei Werte geben Sie als Tupel zurück
(Aufgabe 2_010).
"""


def aufwand_je_kategorie(tickets):
    """Gibt die Minuten je Kategorie und die Zahl der unbrauchbaren Tickets zurück."""
    summen = {}
    unbrauchbar = 0
    for ticket in tickets:
        try:
            kategorie = ticket["kategorie"]
            minuten = int(ticket["minuten"])
        except (KeyError, ValueError):
            unbrauchbar = unbrauchbar + 1
            continue
        summen[kategorie] = summen.get(kategorie, 0) + minuten
    return summen, unbrauchbar


tickets = [
    {"nummer": "T-101", "kategorie": "Drucker", "minuten": "35"},
    {"nummer": "T-102", "kategorie": "Netzwerk", "minuten": "50"},
    {"nummer": "T-103", "kategorie": "Drucker", "minuten": "ca. 20"},
    {"nummer": "T-104", "kategorie": "Drucker", "minuten": "15"},
    {"nummer": "T-105", "minuten": "40"},
]
print(aufwand_je_kategorie(tickets))


# Idee: Die Funktion geht alle Tickets durch. Im try-Block liest sie die Kategorie und wandelt die
# Minuten mit int(...) um; fehlt ein Feld (KeyError) oder ist der Aufwand keine ganze Zahl
# (ValueError), zählt der except-Block das Ticket als unbrauchbar, und continue geht zum nächsten. Erst
# danach addiert sie die Minuten mit summen.get(kategorie, 0) + minuten zur Summe ihrer Kategorie.
#
# Anderer Weg: vorher mit if "kategorie" in ticket and "minuten" in ticket prüfen, ob beide Felder
# da sind, und nur die Umwandlung in ein try mit except ValueError setzen. Statt continue geht auch
# ein else-Block hinter dem except (Aufgabe 3_008).
#
# Typische Fehler: summen[kategorie] schon vor der Umwandlung anlegen (dann steht eine Kategorie mit
# lauter kaputten Tickets mit 0 darin), nur den ValueError abfangen (ein fehlendes Feld bricht dann
# ab), kaputt = 0 in die Schleife schreiben (dann zählt nur das letzte Ticket), die Minuten als Text
# aneinanderhängen statt als Zahlen zu addieren und except ohne Ausnahmen.
