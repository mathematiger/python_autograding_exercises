# Automatisch erzeugt aus lehrkraft/muster/1_033_schriftgroesse.py - nicht von Hand ändern.
# vorlage-hash: 0a46e7c654f0f5f4
# text-hash: fe6f4448f6c43541
# thema: kontrollfluss
# inhalt: while-Schleife

EINGABEN = ["20", "150"]


def erwartete_groesse(anzahl, platz):
    """Sucht die größte passende Schriftgröße von oben mit einer for-Schleife statt while."""
    for groesse in range(24, 0, -1):
        if anzahl * groesse // 2 <= platz:
            return groesse
    return 0


def erwartete_ausgabe(anzahl, platz):
    """Baut die erwartete Ausgabe für diese Eingaben."""
    groesse = erwartete_groesse(anzahl, platz)
    return f"Schriftgröße: {groesse}, Textbreite: {anzahl * groesse // 2} Pixel"


def hinweis_zu(ausgabe, anzahl, platz):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    eins_zu_klein = erwartete_groesse(anzahl, platz) - 1
    zu_klein = f"Schriftgröße: {eins_zu_klein}, Textbreite: {anzahl * eins_zu_klein // 2} Pixel"
    if vergleichbar(ausgabe) == vergleichbar(zu_klein):
        return "\nTipp: Ein Text, der genau so breit ist wie die Schaltfläche, passt; verkleinern Sie nur bei >."
    if vergleichbar(ausgabe) == vergleichbar(f"Schriftgröße: 23, Textbreite: {anzahl * 23 // 2} Pixel"):
        return "\nTipp: if verkleinert nur einmal; while wiederholt, bis der Text passt."
    return ""


def pruefe_lauf(anzahl, platz):
    """Startet das Programm; liefert die Ausgabe oder eine Beschreibung des Abbruchs."""
    try:
        return starte(str(anzahl), str(platz))
    except Exception as fehler:
        return f"(Abbruch: {fehler})"


def meldung(anzahl, platz, ausgabe):
    """Baut die Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei {anzahl} Zeichen und Breite {platz} erwartet:\n{erwartete_ausgabe(anzahl, platz)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, anzahl, platz)}"
    )


# Im Beispiel wird die Schrift kleiner als 24
assert "24" not in AUSGABE.split(",")[0], (
    f"Bei 20 Zeichen und Breite 150 passt der Text mit Schriftgröße 24 nicht (240 Pixel). Ihr Programm gibt aus:\n{AUSGABE}\n"
    "Tipp: Schreiben Sie zwischen Eingabe und Ausgabe eine while-Schleife, die schriftgroesse verkleinert."
)

# Das Beispiel aus der Aufgabe: 20 Zeichen, Breite 150
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(20, 150)), meldung(20, 150, AUSGABE)

# Andere Eingaben: 30 Zeichen, Breite 200 (nicht fest hinschreiben!)
ausgabe = pruefe_lauf(30, 200)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(30, 200)), meldung(30, 200, ausgabe)

# Kurzer Text: Er passt schon, die Schrift bleibt bei 24
ausgabe = pruefe_lauf(5, 300)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(5, 300)), meldung(5, 300, ausgabe)

# Text genau so breit wie die Schaltfläche: 10 Zeichen bei Schrift 24 sind 120 Pixel
ausgabe = pruefe_lauf(10, 120)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(10, 120)), meldung(10, 120, ausgabe)

# Passt erst nach mehreren Schritten genau: 16 Zeichen bei Schrift 15 sind 120 Pixel
ausgabe = pruefe_lauf(16, 120)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(16, 120)), meldung(16, 120, ausgabe)

# Ungerade Schriftgröße: 7 Zeichen bei Schrift 15 sind 52 Pixel (// rundet ab)
ausgabe = pruefe_lauf(7, 52)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(7, 52)), meldung(7, 52, ausgabe)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# 40 zufällige Beschriftungen
zufall = Zufall(1033)
for _ in range(40):
    anzahl = zufall.randint(1, 100)
    platz = zufall.randint(anzahl, 1300)
    ausgabe = pruefe_lauf(anzahl, platz)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(anzahl, platz)), meldung(anzahl, platz, ausgabe)

# Ränder: 100 Zeichen auf 100 Pixeln (kleinste Schrift) und 1 Zeichen auf 2000 Pixeln
for anzahl, platz in [(100, 100), (1, 1), (1, 2000), (100, 2000)]:
    ausgabe = pruefe_lauf(anzahl, platz)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(anzahl, platz)), meldung(anzahl, platz, ausgabe)
