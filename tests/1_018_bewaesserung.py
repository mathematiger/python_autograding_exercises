# Automatisch erzeugt aus lehrkraft/muster/1_018_bewaesserung.py - nicht von Hand ändern.
# vorlage-hash: 45e9eac0d1dd1ce7
# text-hash: 67d8ac71ace90290
# thema: kontrollfluss
# inhalt: if/else

EINGABEN = ["25"]


def erwartete_ausgabe(prozent):
    """Baut die Ausgabe, die bei der Feuchte prozent erwartet wird."""
    ventil = "zu"
    if prozent < 30:
        ventil = "offen"
    return f"Feuchte: {prozent} Prozent\nVentil: {ventil}\nNächste Messung in 10 Minuten."


# Das Beispiel aus der Aufgabe: trocken, das Ventil geht auf
assert AUSGABE == erwartete_ausgabe(25), (
    f"Bei Eingabe 25 erwartet:\n{erwartete_ausgabe(25)}\nIhr Programm gibt aus:\n{AUSGABE}"
)

# Feucht genug: das Ventil geht zu (nicht fest hinschreiben!)
ausgabe = starte("45")
if "Ventil: offen" in ausgabe and "Ventil: zu" in ausgabe:
    hinweis = "\nTipp: Es darf nur eine der beiden Zeilen erscheinen; die zweite gehört unter else."
else:
    hinweis = ""
assert ausgabe == erwartete_ausgabe(45), (
    f"Bei Eingabe 45 erwartet:\n{erwartete_ausgabe(45)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"
)

# Am Grenzwert: 29 ist zu trocken, 30 ist genug
for prozent in [29, 30]:
    ausgabe = starte(str(prozent))
    if prozent == 30 and "Ventil: offen" in ausgabe:
        hinweis = "\nTipp: Bei genau 30 Prozent bleibt das Ventil zu; vergleichen Sie mit < statt <=."
    else:
        hinweis = ""
    assert ausgabe == erwartete_ausgabe(prozent), (
        f"Bei Eingabe {prozent} erwartet:\n{erwartete_ausgabe(prozent)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"
    )

# Ränder: ganz trocken und ganz nass
for prozent in [0, 100]:
    ausgabe = starte(str(prozent))
    assert ausgabe == erwartete_ausgabe(prozent), (
        f"Bei Eingabe {prozent} erwartet:\n{erwartete_ausgabe(prozent)}\nIhr Programm gibt aus:\n{ausgabe}"
    )

# Ein if wird benutzt
assert verwendet("if"), "Benutzen Sie für die Entscheidung if und else."

# 40 zufällige Messungen von 0 bis 100 Prozent
zufall = Zufall(1018)
for _ in range(40):
    prozent = zufall.randint(0, 100)
    ausgabe = starte(str(prozent))
    assert ausgabe == erwartete_ausgabe(prozent), (
        f"Bei Eingabe {prozent} erwartet:\n{erwartete_ausgabe(prozent)}\nIhr Programm gibt aus:\n{ausgabe}"
    )
