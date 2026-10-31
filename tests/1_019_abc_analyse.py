# Automatisch erzeugt aus lehrkraft/muster/1_019_abc_analyse.py - nicht von Hand ändern.
# vorlage-hash: 3d50adc4681d21cd
# text-hash: 76ba3422e4fcee33
# thema: kontrollfluss
# inhalt: if/elif/else

EINGABEN = ["25"]


def erwartete_ausgabe(prozent):
    """Baut die Ausgabe, die beim Anteil prozent erwartet wird."""
    klasse = "C"
    if prozent >= 5:
        klasse = "B"
    if prozent >= 20:
        klasse = "A"
    return f"Anteil: {prozent} Prozent\nKlasse: {klasse}\nAnalyse beendet."


def hinweis_zu(ausgabe):
    """Gibt einen Tipp, wenn mehr als eine Klasse ausgegeben wurde, sonst einen leeren Text."""
    if ausgabe.count("Klasse:") > 1:
        return "\nTipp: Es darf nur eine Klasse erscheinen. Verbinden Sie die Fälle mit elif und else statt mit mehreren if."
    return ""


# Das Beispiel aus der Aufgabe: Klasse A
assert AUSGABE == erwartete_ausgabe(25), (
    f"Bei Eingabe 25 erwartet:\n{erwartete_ausgabe(25)}\nIhr Programm gibt aus:\n{AUSGABE}{hinweis_zu(AUSGABE)}"
)

# Klasse B und Klasse C (nicht fest hinschreiben!)
for prozent in [12, 3]:
    ausgabe = starte(str(prozent))
    assert ausgabe == erwartete_ausgabe(prozent), (
        f"Bei Eingabe {prozent} erwartet:\n{erwartete_ausgabe(prozent)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe)}"
    )

# An den Grenzen: 20 ist schon A, 19 noch B, 5 ist schon B, 4 noch C
for prozent in [20, 19, 5, 4]:
    ausgabe = starte(str(prozent))
    assert ausgabe == erwartete_ausgabe(prozent), (
        f"Bei Eingabe {prozent} erwartet:\n{erwartete_ausgabe(prozent)}\nIhr Programm gibt aus:\n{ausgabe}"
        f"{hinweis_zu(ausgabe)}\nTipp: „ab 20 Prozent“ heißt anteil >= 20, also einschließlich 20."
    )

# Ränder: 0 und 100 Prozent
for prozent in [0, 100]:
    ausgabe = starte(str(prozent))
    assert ausgabe == erwartete_ausgabe(prozent), (
        f"Bei Eingabe {prozent} erwartet:\n{erwartete_ausgabe(prozent)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe)}"
    )

# Ein if wird benutzt
assert verwendet("if"), "Benutzen Sie für die Entscheidung if, elif und else."

# 40 zufällige Anteile von 0 bis 100 Prozent
zufall = Zufall(1019)
for _ in range(40):
    prozent = zufall.randint(0, 100)
    ausgabe = starte(str(prozent))
    assert ausgabe == erwartete_ausgabe(prozent), (
        f"Bei Eingabe {prozent} erwartet:\n{erwartete_ausgabe(prozent)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe)}"
    )
