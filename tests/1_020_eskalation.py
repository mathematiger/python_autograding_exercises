# Automatisch erzeugt aus lehrkraft/muster/1_020_eskalation.py - nicht von Hand ändern.
# vorlage-hash: 7326880ca624d93a
# text-hash: 575b28de517fde21
# thema: kontrollfluss
# inhalt: and, or, not

EINGABEN = ["hoch", "3", "nein"]


def erwartete_ausgabe(prioritaet, stunden, wartet):
    """Baut die Ausgabe für die drei Eingaben (wartet ist "ja" oder "nein")."""
    grenze = 24
    if prioritaet == "hoch":
        grenze = 2
    antwort = "nein"
    if wartet == "nein":
        if stunden >= grenze:
            antwort = "ja"
    return f"Priorität {prioritaet}, seit {stunden} Stunden offen\nEskalieren: {antwort}"


def meldung(prioritaet, stunden, wartet, ausgabe, tipp=""):
    """Baut die Fehlermeldung für einen Fall."""
    erwartet = erwartete_ausgabe(prioritaet, stunden, wartet)
    return f"Bei den Eingaben {prioritaet}, {stunden} und {wartet} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{tipp}"


# Das Beispiel aus der Aufgabe: hohe Priorität, seit 3 Stunden offen
assert AUSGABE == erwartete_ausgabe("hoch", 3, "nein"), meldung("hoch", 3, "nein", AUSGABE)

# Niedrige Priorität nach 3 Stunden: noch nicht (nicht fest hinschreiben!)
ausgabe = starte("niedrig", "3", "nein")
assert ausgabe == erwartete_ausgabe("niedrig", 3, "nein"), meldung(
    "niedrig", 3, "nein", ausgabe, "\nTipp: Die 2-Stunden-Regel gilt nur für Priorität hoch; verknüpfen Sie mit and."
)

# Jede Priorität wird nach 24 Stunden eskaliert
for prioritaet in ["niedrig", "mittel", "hoch"]:
    ausgabe = starte(prioritaet, "30", "nein")
    assert ausgabe == erwartete_ausgabe(prioritaet, 30, "nein"), meldung(
        prioritaet, 30, "nein", ausgabe, "\nTipp: Nach mindestens 24 Stunden wird jedes Ticket eskaliert; das ist ein or."
    )

# Wartet das Ticket auf den Kunden, wird nie eskaliert
for prioritaet, stunden in [("hoch", 3), ("mittel", 30), ("hoch", 1000)]:
    ausgabe = starte(prioritaet, str(stunden), "ja")
    assert ausgabe == erwartete_ausgabe(prioritaet, stunden, "ja"), meldung(
        prioritaet, stunden, "ja", ausgabe, "\nTipp: not wartet muss für die ganze Regel gelten; setzen Sie Klammern."
    )

# An den Grenzen: 1 und 2 Stunden bei hoch, 23 und 24 Stunden bei den anderen
for prioritaet, stunden in [("hoch", 1), ("hoch", 2), ("mittel", 23), ("mittel", 24), ("niedrig", 23), ("niedrig", 24)]:
    ausgabe = starte(prioritaet, str(stunden), "nein")
    assert ausgabe == erwartete_ausgabe(prioritaet, stunden, "nein"), meldung(
        prioritaet, stunden, "nein", ausgabe, "\nTipp: „mindestens 2 Stunden“ heißt stunden >= 2."
    )

# Ränder: 0 Stunden
for prioritaet in ["hoch", "niedrig"]:
    ausgabe = starte(prioritaet, "0", "nein")
    assert ausgabe == erwartete_ausgabe(prioritaet, 0, "nein"), meldung(prioritaet, 0, "nein", ausgabe)

# 40 zufällige Tickets
zufall = Zufall(1020)
for _ in range(40):
    prioritaet = zufall.choice(["hoch", "mittel", "niedrig"])
    stunden = zufall.choice([zufall.randint(0, 30), zufall.randint(0, 1000)])
    wartet = zufall.choice(["ja", "nein"])
    ausgabe = starte(prioritaet, str(stunden), wartet)
    assert ausgabe == erwartete_ausgabe(prioritaet, stunden, wartet), meldung(prioritaet, stunden, wartet, ausgabe)
