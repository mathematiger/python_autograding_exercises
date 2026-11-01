# Automatisch erzeugt aus lehrkraft/muster/1_021_angebotspruefung.py - nicht von Hand ändern.
# vorlage-hash: c5033e72e633f112
# text-hash: 538fc32767378554
# thema: kontrollfluss
# inhalt: Übung: Bedingungen

EINGABEN = ["1200", "3", "ja"]


def erwartete_ausgabe(preis, garantie, siegel):
    """Baut die Ausgabe für die drei Eingaben (siegel ist "ja" oder "nein")."""
    bewertung = "ungenügend"
    if garantie >= 2 or siegel == "ja":
        bewertung = "gut"
    if garantie >= 3 and siegel == "ja":
        bewertung = "sehr gut"
    if preis > 1500:
        bewertung = "zu teuer"
    return f"Angebot: {preis} Euro, {garantie} Jahre Garantie\nBewertung: {bewertung}"


def meldung(preis, garantie, siegel, ausgabe, tipp=""):
    """Baut die Fehlermeldung für einen Fall."""
    erwartet = erwartete_ausgabe(preis, garantie, siegel)
    hinweis = tipp
    if ausgabe.count("Bewertung:") > 1:
        hinweis = "\nTipp: Es darf nur eine Bewertung erscheinen. Verbinden Sie die Fälle mit elif und else statt mit mehreren if."
    return f"Bei den Eingaben {preis}, {garantie} und {siegel} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"


# Das Beispiel aus der Aufgabe: sehr gut
assert AUSGABE == erwartete_ausgabe(1200, 3, "ja"), meldung(1200, 3, "ja", AUSGABE)

# Ohne Siegel ist dasselbe Angebot nur gut (nicht fest hinschreiben!)
ausgabe = starte("1200", "3", "nein")
assert ausgabe == erwartete_ausgabe(1200, 3, "nein"), meldung(
    1200, 3, "nein", ausgabe, "\nTipp: „sehr gut“ verlangt beides, lange Garantie und Siegel; das ist ein and."
)

# Zu teuer schlägt alles andere
for preis, garantie, siegel in [(1600, 5, "ja"), (5000, 10, "ja"), (1501, 0, "nein")]:
    ausgabe = starte(str(preis), str(garantie), siegel)
    assert ausgabe == erwartete_ausgabe(preis, garantie, siegel), meldung(
        preis, garantie, siegel, ausgabe, "\nTipp: Prüfen Sie den Preis zuerst, im if ganz oben."
    )

# Gut reicht eine der beiden Bedingungen
for preis, garantie, siegel in [(800, 2, "nein"), (800, 0, "ja"), (800, 1, "ja"), (800, 2, "ja")]:
    ausgabe = starte(str(preis), str(garantie), siegel)
    assert ausgabe == erwartete_ausgabe(preis, garantie, siegel), meldung(
        preis, garantie, siegel, ausgabe, "\nTipp: Für „gut“ genügt Garantie ab 2 Jahren oder das Siegel; das ist ein or."
    )

# Ungenügend, wenn weder Garantie noch Siegel reichen
for preis, garantie, siegel in [(900, 1, "nein"), (0, 0, "nein")]:
    ausgabe = starte(str(preis), str(garantie), siegel)
    assert ausgabe == erwartete_ausgabe(preis, garantie, siegel), meldung(preis, garantie, siegel, ausgabe)

# An den Grenzen: genau 1500 Euro ist nicht zu teuer, genau 3 und genau 2 Jahre reichen
for preis, garantie, siegel in [(1500, 3, "ja"), (1500, 2, "nein"), (1500, 1, "nein"), (1501, 3, "ja")]:
    ausgabe = starte(str(preis), str(garantie), siegel)
    assert ausgabe == erwartete_ausgabe(preis, garantie, siegel), meldung(
        preis, garantie, siegel, ausgabe,
        "\nTipp: „mehr als 1500 Euro“ heißt preis > 1500, „mindestens 3 Jahre“ heißt garantie >= 3.",
    )

# 40 zufällige Angebote
zufall = Zufall(1021)
for _ in range(40):
    preis = zufall.choice([zufall.randint(0, 5000), zufall.randint(1400, 1600)])
    garantie = zufall.randint(0, 10)
    siegel = zufall.choice(["ja", "nein"])
    ausgabe = starte(str(preis), str(garantie), siegel)
    assert ausgabe == erwartete_ausgabe(preis, garantie, siegel), meldung(preis, garantie, siegel, ausgabe)
