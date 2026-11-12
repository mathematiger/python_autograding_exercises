# Automatisch erzeugt aus lehrkraft/muster/1_033_importpakete.py - nicht von Hand ändern.
# vorlage-hash: 5e7e8b0d2d2818d5
# text-hash: 87a55b57e038eba6
# thema: kontrollfluss
# inhalt: while-Schleife

EINGABEN = ["1200"]


def erwartete_ausgabe(anzahl):
    """Baut die erwartete Ausgabe mit einer for-Schleife über die vollen Pakete statt mit while."""
    zeilen = []
    volle = anzahl // 500
    for nummer in range(1, volle + 1):
        zeilen.append(f"Paket {nummer}: 500 Datensätze")
    if anzahl % 500 > 0:
        zeilen.append(f"Paket {volle + 1}: {anzahl % 500} Datensätze")
    zeilen.append(f"Pakete insgesamt: {len(zeilen)}")
    return "\n".join(zeilen)


def lauf(anzahl):
    """Startet das Programm mit dieser Anzahl; liefert die Ausgabe oder eine Beschreibung des Abbruchs."""
    try:
        return starte(str(anzahl))
    except Exception as fehler:
        return f"(Abbruch: {fehler})"


def hinweis_zu(ausgabe):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if ": 0 Datensätze" in ausgabe or ": -" in ausgabe:
        return "\nTipp: Die Schleife soll nur laufen, solange rest größer als 0 ist: while rest > 0:"
    if ausgabe.count("Pakete insgesamt") > 1:
        return "\nTipp: Die letzte Zeile steht schon unter der Schleife; geben Sie in der Schleife nur die Paketzeile aus."
    return ""


def meldung(anzahl, ausgabe):
    """Baut die Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei Eingabe {anzahl} erwartet:\n{erwartete_ausgabe(anzahl)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe)}"
    )


# Das Beispiel aus der Aufgabe: 1200 Datensätze
assert AUSGABE == erwartete_ausgabe(1200), meldung(1200, AUSGABE)

# 1700 Datensätze: vier Pakete (nicht fest hinschreiben!)
ausgabe = lauf(1700)
assert ausgabe == erwartete_ausgabe(1700), meldung(1700, ausgabe)

# Weniger als 500 Datensätze: ein einziges kleines Paket
ausgabe = lauf(37)
assert ausgabe == erwartete_ausgabe(37), meldung(37, ausgabe)

# Genau 500 und genau 1000 Datensätze: nur volle Pakete, kein leeres Paket hinterher
for anzahl in [500, 1000]:
    ausgabe = lauf(anzahl)
    assert ausgabe == erwartete_ausgabe(anzahl), meldung(anzahl, ausgabe)

# 501 Datensätze: ein volles Paket und eines mit einem Datensatz
ausgabe = lauf(501)
assert ausgabe == erwartete_ausgabe(501), (
    meldung(501, ausgabe) + "\nTipp: Das letzte Paket ist nur so groß wie der Rest: min(rest, 500)."
)

# Ein einziger Datensatz
ausgabe = lauf(1)
assert ausgabe == erwartete_ausgabe(1), meldung(1, ausgabe)

# Keine Datensätze: kein Paket
ausgabe = lauf(0)
assert ausgabe == "Pakete insgesamt: 0", (
    f"Bei Eingabe 0 erwartet nur: Pakete insgesamt: 0\nIhr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe)}"
)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# 40 zufällige Anzahlen
zufall = Zufall(1033)
for anzahl in sorted(zufall.sample(range(0, 5001), 40)):
    # Aufsteigend sortiert, damit die Meldung die kleinste fehlerhafte Anzahl zeigt
    ausgabe = lauf(anzahl)
    assert ausgabe == erwartete_ausgabe(anzahl), meldung(anzahl, ausgabe)

# Obere Grenze: 100000 Datensätze sind 200 volle Pakete
ausgabe = lauf(100000)
zeilen = ausgabe.split("\n")
assert ausgabe == erwartete_ausgabe(100000), (
    f"Bei Eingabe 100000 erwartet: 200 Zeilen „Paket …: 500 Datensätze“ und dann „Pakete insgesamt: 200“. "
    f"Ihr Programm gibt {len(zeilen)} Zeilen aus, die ersten: {zeilen[:2]}, die letzten: {zeilen[-2:]}"
)
