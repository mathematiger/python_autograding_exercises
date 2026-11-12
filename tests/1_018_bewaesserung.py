# Automatisch erzeugt aus lehrkraft/muster/1_018_bewaesserung.py - nicht von Hand ändern.
# vorlage-hash: 45e9eac0d1dd1ce7
# text-hash: 0d18b81729aead19
# thema: kontrollfluss
# inhalt: if/else

EINGABEN = ["25"]


def erwartete_ausgabe(prozent):
    """Baut die Ausgabe, die bei der Feuchte prozent erwartet wird."""
    ventil = "zu"
    if prozent < 30:
        ventil = "offen"
    return f"Feuchte: {prozent} Prozent\nVentil: {ventil}\nNächste Messung in 10 Minuten."


def hinweis_zu(ausgabe, prozent):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if "Ventil: offen" in ausgabe and "Ventil: zu" in ausgabe:
        return "\nTipp: Es darf nur eine der beiden Zeilen erscheinen; die zweite gehört unter else."
    if prozent == 30 and "Ventil: offen" in ausgabe:
        return "\nTipp: Bei genau 30 Prozent bleibt das Ventil zu; vergleichen Sie mit < statt <=."
    return ""


def meldung(prozent, ausgabe):
    """Baut die Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei Eingabe {prozent} erwartet:\n{erwartete_ausgabe(prozent)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, prozent)}"
    )


# Das Beispiel aus der Aufgabe: trocken, das Ventil geht auf
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(25)), meldung(25, AUSGABE)

# Feucht genug: das Ventil geht zu (nicht fest hinschreiben!)
ausgabe = starte("45")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(45)), meldung(45, ausgabe)

# Knapp unter dem Grenzwert: 29 ist zu trocken
ausgabe = starte("29")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(29)), meldung(29, ausgabe)

# Genau am Grenzwert: 30 ist genug
ausgabe = starte("30")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(30)), meldung(30, ausgabe)

# Ränder: ganz trocken und ganz nass
for prozent in [0, 100]:
    ausgabe = starte(str(prozent))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(prozent)), meldung(prozent, ausgabe)

# Ein if wird benutzt
assert verwendet("if"), "Benutzen Sie für die Entscheidung if und else."

# 40 zufällige Messungen von 0 bis 100 Prozent
zufall = Zufall(1018)
for _ in range(40):
    prozent = zufall.randint(0, 100)
    ausgabe = starte(str(prozent))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(prozent)), meldung(prozent, ausgabe)
