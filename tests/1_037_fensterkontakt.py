# Automatisch erzeugt aus lehrkraft/muster/1_037_fensterkontakt.py - nicht von Hand ändern.
# vorlage-hash: 19376bb9382784a7
# text-hash: 199a705e9f35f05f
# thema: funktionen
# inhalt: Eigene Funktion ohne Rückgabe

EINGABEN = ["Büro 2", "Labor"]


def erwartete_ausgabe(raum_1, raum_2):
    """Baut die erwartete Ausgabe für zwei Räume."""
    return (
        f"Fenster offen: {raum_1}\nHeizventil in {raum_1} wird geschlossen.\n"
        f"Fenster offen: {raum_2}\nHeizventil in {raum_2} wird geschlossen.\n"
        "Alle Meldungen verschickt."
    )


def meldung(raum_1, raum_2, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    return (
        f'Bei den Eingaben "{raum_1}" und "{raum_2}" erwartet:\n{erwartete_ausgabe(raum_1, raum_2)}\n'
        f"Ihr Programm gibt aus:\n{ausgabe}"
    )


# Die Funktion warnung ist mit def angelegt
assert verwendet("def"), (
    "Im Programm fehlt noch die Funktion warnung. Legen Sie sie mit def warnung(raum): an und schreiben Sie "
    "den Rumpf eingerückt darunter."
)

# Im Beispiel: die erste Zeile für Büro 2
assert vergleichbar("Fenster offen: Büro 2") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben "Büro 2" und "Labor" erwartet die Zeile "Fenster offen: Büro 2" – Ihr Programm gibt aus:\n'
    f"{AUSGABE}\n"
    'Tipp: print(f"Fenster offen: {raum}") im Rumpf der Funktion setzt den Raum ein.'
)

# Im Beispiel: die zweite Zeile für Büro 2
assert vergleichbar("Heizventil in Büro 2 wird geschlossen.") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben "Büro 2" und "Labor" erwartet die Zeile "Heizventil in Büro 2 wird geschlossen." – '
    f"Ihr Programm gibt aus:\n{AUSGABE}\nTipp: Die Funktion gibt zwei Zeilen aus, also zweimal print(...)."
)

# Im Beispiel: der zweite Aufruf meldet das Labor
if AUSGABE.count("Büro 2") == 4:
    hinweis = (
        "\nTipp: Bei beiden Aufrufen erscheint Büro 2. Benutzen Sie in der Funktion den Parameter raum, "
        "nicht die Variable fenster_1."
    )
else:
    hinweis = ""
assert vergleichbar("Fenster offen: Labor") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben "Büro 2" und "Labor" erwartet die Zeile "Fenster offen: Labor" – Ihr Programm gibt aus:\n'
    f"{AUSGABE}{hinweis}"
)

# Das ganze Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe("Büro 2", "Labor")), meldung(
    "Büro 2", "Labor", AUSGABE
)

# Andere Räume (nicht fest hinschreiben!)
ausgabe = starte("Serverraum", "Flur")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe("Serverraum", "Flur")), meldung(
    "Serverraum", "Flur", ausgabe
)

# Zweimal derselbe Raum
ausgabe = starte("Küche", "Küche")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe("Küche", "Küche")), meldung("Küche", "Küche", ausgabe)

# Der Raumname wird genau so übernommen, wie er eingegeben wurde
ausgabe = starte("Raum 3.14", "EG-West")
assert "Raum 3.14" in ausgabe and "in EG-West wird" in ausgabe, (
    meldung("Raum 3.14", "EG-West", ausgabe) + "\nTipp: Setzen Sie raum unverändert in den Text ein."
)

# Viele zufällige Räume
zufall = Zufall(1037)
raeume = ["Büro 1", "Büro 2", "Labor", "Werkstatt", "Lager", "Serverraum", "Flur", "Aula", "Raum 101", "Küche"]
for _ in range(30):
    raum_1 = zufall.choice(raeume)
    raum_2 = zufall.choice(raeume)
    ausgabe = starte(raum_1, raum_2)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(raum_1, raum_2)), meldung(raum_1, raum_2, ausgabe)
