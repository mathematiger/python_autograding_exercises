# Automatisch erzeugt aus lehrkraft/muster/1_033_lupe.py - nicht von Hand ändern.
# vorlage-hash: bd91203fac3c36b6
# text-hash: a13f79404dfb4c78
# thema: kontrollfluss
# inhalt: while-Schleife

EINGABEN = ["140"]


def erwartete_ausgabe(ziel_test):
    """Baut die erwartete Ausgabe mit einer for-Schleife statt while."""
    zeilen = []
    stufe = 100
    for _ in range(40):
        if stufe >= ziel_test:
            break
        stufe = stufe + 25
        zeilen.append(f"Zoom: {stufe} %")
    zeilen.append(f"Fertig nach {len(zeilen)} Klicks: {stufe} %")
    return "\n".join(zeilen)


def lauf(ziel_test):
    """Startet das Programm mit dieser Eingabe; liefert die Ausgabe oder eine Beschreibung des Abbruchs."""
    try:
        return starte(str(ziel_test))
    except Exception as fehler:
        return f"(Abbruch: {fehler})"


def hinweis_zu(ausgabe, ziel_test):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if ausgabe.count("Fertig") > 1:
        return "\nTipp: Die Zeile „Fertig nach …“ steht schon unter der Schleife; rücken Sie in die Schleife nur ein, was sich wiederholen soll."
    if vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(ziel_test + 1)):
        return "\nTipp: Ist das Ziel genau erreicht, ist Schluss. Wiederholen Sie nur, solange zoom < ziel ist."
    if "Zoom" not in ausgabe and ziel_test > 100:
        return '\nTipp: Geben Sie in der Schleife nach jedem Klick die neue Stufe aus: print(f"Zoom: {zoom} %").'
    return ""


def meldung(ziel_test, ausgabe):
    """Baut die Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei Eingabe {ziel_test} erwartet:\n{erwartete_ausgabe(ziel_test)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, ziel_test)}"
    )


# Bei Eingabe 140 endet die Lupe bei 150 % nach 2 Klicks (die Zeilen „Zoom: …“ zählen hier noch nicht)
letzte_zeile = AUSGABE.split("\n")[-1]
assert vergleichbar(letzte_zeile) == vergleichbar("Fertig nach 2 Klicks: 150 %"), (
    f'Bei Eingabe 140 erwartet als letzte Zeile: "Fertig nach 2 Klicks: 150 %" – Ihr Programm: "{letzte_zeile}"\n'
    "Tipp: Erhöhen Sie in der Schleife zoom um 25 und klicks um 1, solange zoom < ziel ist."
)

# Das Beispiel aus der Aufgabe, mit den Zwischenstufen
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(140)), meldung(140, AUSGABE)

# Eine andere Vergrößerung: 300 % (nicht fest hinschreiben!)
ausgabe = lauf(300)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(300)), meldung(300, ausgabe)

# Genau eine Zoomstufe getroffen: bei 150 % ist nach 2 Klicks Schluss, nicht erst bei 175 %
ausgabe = lauf(150)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(150)), meldung(150, ausgabe)

# Knapp über 100 %: schon ein Klick reicht
ausgabe = lauf(101)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(101)), meldung(101, ausgabe)

# 100 % sind schon erreicht: kein Klick, nur die Schlusszeile
ausgabe = lauf(100)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(100)), meldung(100, ausgabe)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# 40 zufällige Vergrößerungen zwischen 100 und 1000
zufall = Zufall(1033)
for ziel_test in sorted(zufall.sample(range(100, 1001), 40)):
    # Aufsteigend sortiert, damit eine Fehlermeldung die kleinste fehlerhafte Eingabe zeigt
    ausgabe = lauf(ziel_test)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(ziel_test)), meldung(ziel_test, ausgabe)

# Obere Grenze: 1000 % nach 36 Klicks
ausgabe = lauf(1000)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(1000)), meldung(1000, ausgabe)
