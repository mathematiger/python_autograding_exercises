# Automatisch erzeugt aus lehrkraft/muster/1_031_auftragszeiten.py - nicht von Hand ändern.
# vorlage-hash: 19c93f465b3df78e
# text-hash: 59290e3f918468bd
# thema: datenstrukturen
# inhalt: min, max, sum, sorted

EINGABEN = ["12,7,30,7,18"]


def aufsteigend(werte):
    """Sortiert eine Kopie durch wiederholtes Herausnehmen des kleinsten Werts, ohne sorted."""
    rest = list(werte)
    ergebnis = []
    while rest:
        kleinster = rest[0]
        for wert in rest:
            if wert < kleinster:
                kleinster = wert
        rest.remove(kleinster)
        ergebnis.append(kleinster)
    return ergebnis


def erwartete_ausgabe(werte):
    """Baut die erwartete Ausgabe; min, max und Summe kommen aus der selbst sortierten Liste."""
    geordnet = aufsteigend(werte)
    gesamt = 0
    for wert in werte:
        gesamt = gesamt + wert
    return (
        f"Gemessen: {werte}\nSortiert: {geordnet}\n"
        f"Kürzeste: {geordnet[0]} min, längste: {geordnet[-1]} min\n"
        f"Gesamt: {gesamt} min für {len(werte)} Aufträge"
    )


def hinweis_zu(ausgabe, werte):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    geordnet = aufsteigend(werte)
    if "Sortiert: None" in ausgabe:
        return (
            "\nTipp: zeiten.sort() sortiert die Liste selbst und gibt None zurück. "
            "Benutzen Sie sortiert = sorted(zeiten), das liefert eine neue Liste."
        )
    if geordnet != werte and ausgabe.startswith(f"Gemessen: {geordnet}\n"):
        return (
            "\nTipp: Die gemessene Reihenfolge ist verloren gegangen. sorted(zeiten) lässt zeiten unverändert "
            "und liefert eine neue, sortierte Liste."
        )
    if min(werte) != max(werte) and f"Kürzeste: {max(werte)} min, längste: {min(werte)} min" in ausgabe:
        return "\nTipp: Kürzeste und längste Zeit sind vertauscht: min liefert die kleinste, max die größte."
    return ""


def meldung(werte, ausgabe):
    """Baut die Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    text = ",".join(str(wert) for wert in werte)
    return (
        f"Bei der Eingabe {text} erwartet:\n{erwartete_ausgabe(werte)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, werte)}"
    )


def pruefe_lauf(werte):
    """Startet das Programm mit diesen Zeiten und liefert die Ausgabe."""
    return starte(",".join(str(wert) for wert in werte))


# Das Beispiel aus der Aufgabe
BEISPIEL = [12, 7, 30, 7, 18]
assert AUSGABE == erwartete_ausgabe(BEISPIEL), meldung(BEISPIEL, AUSGABE)

# Andere Zeiten (nicht fest hinschreiben!)
werte = [45, 3, 22, 9]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# Die Zeiten sind schon absteigend sortiert
werte = [90, 60, 30, 10]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# Nur ein einziger Auftrag
werte = [15]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# Alle Zeiten gleich
werte = [8, 8, 8]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# Ränder: 1 und 1000 Minuten
werte = [1000, 1, 500]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# min, max, sum und sorted werden benutzt
fehlend = [name for name in ["min", "max", "sum", "sorted"] if not verwendet(name)]
assert not fehlend, f"Benutzen Sie die fertigen Funktionen; es fehlt: {', '.join(fehlend)}."

# 40 zufällige Messreihen
zufall = Zufall(1031)
for _ in range(40):
    werte = [zufall.randint(1, 1000) for _ in range(zufall.randint(1, 12))]
    ausgabe = pruefe_lauf(werte)
    assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)

# Obere Grenze: 30 Zeiten
werte = [(zahl * 337) % 1000 + 1 for zahl in range(30)]
ausgabe = pruefe_lauf(werte)
assert ausgabe == erwartete_ausgabe(werte), meldung(werte, ausgabe)
