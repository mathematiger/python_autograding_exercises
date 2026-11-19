# Automatisch erzeugt aus lehrkraft/muster/1_037_heizungsventile.py - nicht von Hand ändern.
# vorlage-hash: 4cb47706f2db9b07
# text-hash: 643de0addddc90af
# thema: funktionen
# inhalt: Funktion ohne Rückgabe

EINGABEN = ["Büro", "Küche"]


def erwartete_ausgabe(a, b):
    """Baut die erwartete Ausgabe für die beiden Räume a und b."""
    return (
        f"Ventil im Raum {a} geschlossen, Heizung aus.\n"
        f"Ventil im Raum {b} geschlossen, Heizung aus.\n"
        "Alle Meldungen bearbeitet."
    )


def hinweis_zu(ausgabe, a, b):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    zeile_a = vergleichbar(f"Ventil im Raum {a} geschlossen")
    if a != b and vergleichbar(ausgabe).count(zeile_a) == 2:
        return (
            "\nTipp: Benutzen Sie im Rumpf der Funktion den Parameter raum, nicht raum_a; "
            "sonst steht bei jedem Aufruf derselbe Raum da."
        )
    if vergleichbar(f"Raum {b}") not in vergleichbar(ausgabe):
        return "\nTipp: Rufen Sie an der zweiten markierten Stelle ventil_schliessen(raum_b) auf."
    return ""


def meldung(a, b, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei den Eingaben {a} und {b} erwartet:\n{erwartete_ausgabe(a, b)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, a, b)}"
    )


# Im Beispiel: das Ventil im Büro wird geschlossen
assert vergleichbar("Ventil im Raum Büro geschlossen, Heizung aus.") in vergleichbar(AUSGABE), (
    'Bei den Eingaben Büro und Küche erwartet die Zeile "Ventil im Raum Büro geschlossen, Heizung aus." – '
    f"Ihr Programm gibt aus:\n{AUSGABE}\n"
    'Tipp: Im Rumpf der Funktion steht print(f"Ventil im Raum {raum} geschlossen, Heizung aus.").'
)

# Im Beispiel: das Ventil in der Küche wird geschlossen
assert vergleichbar("Ventil im Raum Küche geschlossen, Heizung aus.") in vergleichbar(AUSGABE), (
    'Bei den Eingaben Büro und Küche erwartet die Zeile "Ventil im Raum Küche geschlossen, Heizung aus." – '
    f"Ihr Programm gibt aus:\n{AUSGABE}{hinweis_zu(AUSGABE, 'Büro', 'Küche')}"
)

# Das ganze Beispiel aus der Aufgabe, in der richtigen Reihenfolge
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe("Büro", "Küche")), meldung("Büro", "Küche", AUSGABE)

# Andere Räume (nicht fest hinschreiben!)
ausgabe = starte("Serverraum", "Lager")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe("Serverraum", "Lager")), (
    meldung("Serverraum", "Lager", ausgabe)
)

# Die Räume vertauscht
ausgabe = starte("Küche", "Büro")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe("Küche", "Büro")), meldung("Küche", "Büro", ausgabe)

# Zweimal derselbe Raum
ausgabe = starte("Flur", "Flur")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe("Flur", "Flur")), meldung("Flur", "Flur", ausgabe)

# Eine eigene Funktion wird mit def festgelegt
assert verwendet("def"), (
    "Legen Sie oben im Programm mit def ventil_schliessen(raum): eine eigene Funktion fest, "
    "statt die Zeilen direkt auszugeben."
)

# Viele zufällige Räume
zufall = Zufall(1037)
raeume = ["Büro 1", "Büro 2", "Küche", "Flur", "Lager", "Serverraum", "Besprechung", "Empfang", "Labor"]
for _ in range(30):
    a = zufall.choice(raeume)
    b = zufall.choice(raeume)
    ausgabe = starte(a, b)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(a, b)), meldung(a, b, ausgabe)
