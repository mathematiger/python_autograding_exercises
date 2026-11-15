# Automatisch erzeugt aus lehrkraft/muster/1_033_schriftgroesse.py - nicht von Hand ändern.
# vorlage-hash: 75c9d6c9a1c67ebb
# text-hash: 216af1d8d00d2fe5
# thema: kontrollfluss
# inhalt: while-Schleife

EINGABEN = ["18"]


def erwartete_ausgabe(start):
    """Baut die erwartete Ausgabe mit einer for-Schleife über die nötige Anzahl Klicks."""
    noetig = 0
    if start < 24:
        noetig = (24 - start + 1) // 2
    zeilen = []
    for nummer in range(1, noetig + 1):
        zeilen.append(f"Klick {nummer}: {start + 2 * nummer} Pixel")
    zeilen.append(f"Nach {noetig} Klicks ist die Schrift {start + 2 * noetig} Pixel groß.")
    return "\n".join(zeilen)


def hinweis_zu(ausgabe, start):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    zeilen = ausgabe.split("\n")
    if start < 24 and zeilen and zeilen[0].startswith(f"Klick 0: {start} Pixel"):
        return "\nTipp: Erhöhen Sie groesse und klicks zuerst und geben Sie die Zeile erst danach aus."
    if start % 2 == 0 and start <= 24 and "Klick" in ausgabe and f"{start + 2 * ((24 - start) // 2 + 1)} Pixel groß" in ausgabe:
        return "\nTipp: Bei genau 24 Pixel ist die Schrift groß genug; die Bedingung lautet groesse < 24, nicht <= 24."
    if f"Nach 0 Klicks ist die Schrift {start + 2 * ((24 - start + 1) // 2)}" in ausgabe:
        return "\nTipp: Auch klicks muss in der Schleife wachsen: klicks = klicks + 1."
    return ""


def meldung(start, ausgabe):
    """Baut die Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei Eingabe {start} erwartet:\n{erwartete_ausgabe(start)}\nIhr Programm gibt aus:\n{ausgabe}"
        f"{hinweis_zu(ausgabe, start)}"
    )


# Bei Eingabe 18 reichen 3 Klicks bis 24 Pixel (nur die letzte Zeile)
assert vergleichbar("Nach 3 Klicks ist die Schrift 24 Pixel groß.") in vergleichbar(AUSGABE), (
    f'Bei Eingabe 18 erwartet am Ende: "Nach 3 Klicks ist die Schrift 24 Pixel groß."\n'
    f"Ihr Programm gibt aus:\n{AUSGABE}{hinweis_zu(AUSGABE, 18)}"
)

# Bei Eingabe 18 gibt jeder Klick eine Zeile aus
for zeile in ["Klick 1: 20 Pixel", "Klick 2: 22 Pixel", "Klick 3: 24 Pixel"]:
    assert vergleichbar(zeile) in vergleichbar(AUSGABE), (
        f'Bei Eingabe 18 fehlt die Zeile "{zeile}".\nIhr Programm gibt aus:\n{AUSGABE}\n'
        'Tipp: Geben Sie in der Schleife nach dem Erhöhen mit print(f"Klick {klicks}: {groesse} Pixel") aus.'
        f"{hinweis_zu(AUSGABE, 18)}"
    )

# Das Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(18)), meldung(18, AUSGABE)

# Eine andere Startgröße (nicht fest hinschreiben!)
ausgabe = starte("12")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(12)), meldung(12, ausgabe)

# Schon groß genug: kein Klick
ausgabe = starte("30")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(30)), (
    meldung(30, ausgabe) + "\nTipp: Ist die Bedingung schon beim ersten Mal falsch, läuft die Schleife gar nicht."
)

# Genau 24 Pixel sind groß genug: kein Klick
ausgabe = starte("24")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(24)), meldung(24, ausgabe)

# Ungerade Größe: 23 Pixel brauchen einen Klick und landen bei 25
ausgabe = starte("23")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(23)), meldung(23, ausgabe)

# Kleinste Größe 8 Pixel: 8 Klicks
ausgabe = starte("8")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(8)), meldung(8, ausgabe)

# Größte Größe 40 Pixel: kein Klick
ausgabe = starte("40")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(40)), meldung(40, ausgabe)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# Alle erlaubten Größen von 8 bis 40, in gemischter Reihenfolge
zufall = Zufall(1033)
groessen = list(range(8, 41))
zufall.shuffle(groessen)
for start in groessen:
    ausgabe = starte(str(start))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(start)), meldung(start, ausgabe)
