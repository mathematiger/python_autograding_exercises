# Automatisch erzeugt aus lehrkraft/muster/1_027_meilensteine.py - nicht von Hand ändern.
# vorlage-hash: 13e90035cb2c83e3
# text-hash: c6f36e948c61bfff
# thema: datenstrukturen
# inhalt: Listen: Index und len

EINGABEN = ["Kickoff;Anforderungen;Prototyp;Abnahme", "3"]


def erwartete_ausgabe(namen, nummer):
    """Baut die erwartete Ausgabe, ohne len und ohne negativen Index."""
    anzahl = 0
    for name in namen:
        anzahl = anzahl + 1
        letzter = name
    return (
        f"Der Plan hat {anzahl} Meilensteine.\n"
        f"Erster: {namen[0]}, letzter: {letzter}\n"
        f"Als Nächstes: Meilenstein {nummer}, {namen[nummer - 1]}"
    )


def hinweis_zu(ausgabe, namen, nummer):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if not ausgabe:
        # Ohne Ausgabe ist das Programm abgebrochen; die Fehlermeldung von Python sagt dann mehr als ein Tipp.
        return ""
    if nummer < len(namen) and ausgabe.endswith(f"Meilenstein {nummer}, {namen[nummer]}"):
        return (
            f"\nTipp: Sie holen den Meilenstein nach Nummer {nummer}. Die Liste zählt ab 0, die Nummer ab 1: "
            "Meilenstein Nummer 1 ist meilensteine[0]."
        )
    if f"Der Plan hat {len(namen)} Meilensteine." not in ausgabe:
        return "\nTipp: Die Anzahl der Elemente einer Liste liefert len(meilensteine)."
    if f"letzter: {namen[-1]}\n" not in ausgabe:
        return "\nTipp: Das letzte Element einer Liste holt meilensteine[-1]."
    return ""


def pruefe_plan(namen, nummer):
    """Startet das Programm mit diesem Plan; liefert die Ausgabe oder eine Beschreibung des Abbruchs und einen Tipp."""
    try:
        return starte(";".join(namen), str(nummer)), ""
    except Exception as fehler:
        if "IndexError" not in str(fehler):
            raise
        # meilensteine[nummer] statt meilensteine[nummer - 1] bricht beim letzten Meilenstein ab
        return f"(Abbruch: {fehler})", (
            "\nTipp: IndexError heißt, der Index ist zu groß. Bei n Elementen gehen die Indizes von 0 bis n - 1; "
            "Meilenstein Nummer 1 ist meilensteine[0], der letzte ist meilensteine[-1]."
        )


def meldung(namen, nummer, ausgabe, hinweis=""):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei den Eingaben {';'.join(namen)} und {nummer} erwartet:\n{erwartete_ausgabe(namen, nummer)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis or hinweis_zu(ausgabe, namen, nummer)}"
    )


# Das Beispiel aus der Aufgabe: vier Meilensteine, Nummer 3
BEISPIEL = ["Kickoff", "Anforderungen", "Prototyp", "Abnahme"]
assert AUSGABE == erwartete_ausgabe(BEISPIEL, 3), meldung(BEISPIEL, 3, AUSGABE)

# Anderer Plan mit sechs Meilensteinen (nicht fest hinschreiben!)
plan = ["Start", "Entwurf", "Datenbank", "Oberfläche", "Test", "Go-live"]
ausgabe, hinweis = pruefe_plan(plan, 2)
assert ausgabe == erwartete_ausgabe(plan, 2), meldung(plan, 2, ausgabe, hinweis)

# Nummer 1 ist der erste Meilenstein
plan = ["Angebot", "Auftrag", "Lieferung"]
ausgabe, hinweis = pruefe_plan(plan, 1)
assert ausgabe == erwartete_ausgabe(plan, 1), meldung(plan, 1, ausgabe, hinweis)

# Die höchste Nummer ist der letzte Meilenstein
plan = ["Analyse", "Konzept", "Umsetzung", "Schulung", "Abschluss"]
ausgabe, hinweis = pruefe_plan(plan, 5)
assert ausgabe == erwartete_ausgabe(plan, 5), meldung(plan, 5, ausgabe, hinweis)

# Der kleinste Plan: zwei Meilensteine
plan = ["Beginn", "Ende"]
ausgabe, hinweis = pruefe_plan(plan, 2)
assert ausgabe == erwartete_ausgabe(plan, 2), meldung(plan, 2, ausgabe, hinweis)

# 40 zufällige Pläne
VORRAT = ["Kickoff", "Lastenheft", "Pflichtenheft", "Entwurf", "Prototyp", "Betatest", "Schulung", "Rollout",
          "Abnahme", "Review", "Datenmigration", "Go-live", "Pilotphase", "Dokumentation", "Projektende"]
zufall = Zufall(1027)
for _ in range(40):
    plan = zufall.sample(VORRAT, zufall.randint(2, len(VORRAT)))
    nummer = zufall.randint(1, len(plan))
    ausgabe, hinweis = pruefe_plan(plan, nummer)
    assert ausgabe == erwartete_ausgabe(plan, nummer), meldung(plan, nummer, ausgabe, hinweis)

# Obere Grenze: 20 Meilensteine, Nummer 20
plan = [f"M{zahl}" for zahl in range(1, 21)]
ausgabe, hinweis = pruefe_plan(plan, 20)
assert ausgabe == erwartete_ausgabe(plan, 20), meldung(plan, 20, ausgabe, hinweis)
