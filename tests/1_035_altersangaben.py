# Automatisch erzeugt aus lehrkraft/muster/1_035_altersangaben.py - nicht von Hand ändern.
# vorlage-hash: 0f78d4b22971d95c
# text-hash: 79a0abdc6d97158b
# thema: kontrollfluss
# inhalt: Übung: while

EINGABEN = ["34", "130", "51", "-2", "27", "stop"]


def erwartete_ausgabe(werte):
    """Baut die erwartete Ausgabe mit for und Listen statt einer while-Schleife."""
    zeilen = []
    gute = []
    for wert in werte:
        if 0 <= wert <= 120:
            gute.append(wert)
        else:
            zeilen.append(f"Ungültiger Wert: {wert}")
    zeilen.append(f"Gültig: {len(gute)}, ungültig: {len(werte) - len(gute)}")
    if gute:
        zeilen.append(f"Durchschnittsalter: {sum(gute) / len(gute):.1f} Jahre")
    return "\n".join(zeilen)


def lauf(werte):
    """Startet das Programm mit diesen Werten und stop; liefert die Ausgabe oder eine Beschreibung des Abbruchs."""
    try:
        return starte(*[str(wert) for wert in werte], "stop")
    except Exception as fehler:
        return f"(Abbruch: {fehler})"


def hinweis_zu(ausgabe, werte):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if "stop" in ausgabe and "int" in ausgabe:
        return (
            "\nTipp: Das Wort stop darf nicht mit int(...) umgewandelt werden. Lesen Sie die nächste Eingabe "
            "als letzte Zeile im Block, dann prüft die Bedingung sie, bevor gerechnet wird."
        )
    if "öfter nach einer Eingabe" in ausgabe:
        return '\nTipp: Die Schleife soll enden, sobald die Eingabe stop ist: while eingabe != "stop":'
    for grenze in [0, 120]:
        if grenze in werte and f"Ungültiger Wert: {grenze}" in ausgabe:
            return f"\nTipp: {grenze} ist noch gültig. Benutzen Sie >= und <=, nicht > und <."
    for grenze in [-1, 121]:
        if grenze in werte and f"Ungültiger Wert: {grenze}" not in ausgabe:
            return f"\nTipp: {grenze} liegt außerhalb von 0 bis 120 und ist ungültig."
    return ""


def meldung(werte, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    eingaben = ", ".join([str(wert) for wert in werte] + ["stop"])
    return (
        f"Bei den Eingaben {eingaben} erwartet:\n{erwartete_ausgabe(werte)}\nIhr Programm gibt aus:\n{ausgabe}"
        f"{hinweis_zu(ausgabe, werte)}"
    )


BEISPIEL = [34, 130, 51, -2, 27]

# Im Beispiel: drei gültige und zwei ungültige Werte gezählt
assert vergleichbar("Gültig: 3, ungültig: 2") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 34, 130, 51, -2, 27, stop erwartet die Zeile "Gültig: 3, ungültig: 2"\n'
    f"Ihr Programm gibt aus:\n{AUSGABE}{hinweis_zu(AUSGABE, BEISPIEL)}"
)

# Im Beispiel: der Durchschnitt der gültigen Werte ist 37.3
assert vergleichbar("Durchschnittsalter: 37.3 Jahre") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 34, 130, 51, -2, 27, stop erwartet die Zeile "Durchschnittsalter: 37.3 Jahre"\n'
    f"Ihr Programm gibt aus:\n{AUSGABE}\n"
    "Tipp: In summe gehören nur die gültigen Werte: summe = summe + alter im if-Zweig."
)

# Im Beispiel: die ungültigen Werte werden gemeldet
assert vergleichbar("Ungültiger Wert: 130") in vergleichbar(AUSGABE) and vergleichbar("Ungültiger Wert: -2") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 34, 130, 51, -2, 27, stop erwartet die Zeilen "Ungültiger Wert: 130" und "Ungültiger Wert: -2"\n'
    f"Ihr Programm gibt aus:\n{AUSGABE}\n"
    'Tipp: Geben Sie im else-Zweig print(f"Ungültiger Wert: {alter}") aus.'
)

# Das ganze Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(BEISPIEL)), meldung(BEISPIEL, AUSGABE)

# Andere Werte (nicht fest hinschreiben!)
ausgabe = lauf([80, 999, 20])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([80, 999, 20])), meldung([80, 999, 20], ausgabe)

# Nur gültige Werte
ausgabe = lauf([18, 19, 45, 62])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([18, 19, 45, 62])), meldung([18, 19, 45, 62], ausgabe)

# Gleich stop: nichts gezählt, kein Durchschnitt
ausgabe = lauf([])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([])), (
    meldung([], ausgabe) + "\nTipp: Ist die erste Eingabe schon stop, läuft die Schleife gar nicht."
)

# Nur ungültige Werte: kein Durchschnitt
ausgabe = lauf([-5, 500])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([-5, 500])), meldung([-5, 500], ausgabe)

# 0 und 120 sind noch gültig
ausgabe = lauf([0, 120])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([0, 120])), meldung([0, 120], ausgabe)

# -1 und 121 sind schon ungültig
ausgabe = lauf([-1, 121, 60])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([-1, 121, 60])), meldung([-1, 121, 60], ausgabe)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# 40 zufällige Wertereihen
zufall = Zufall(1035)
for _ in range(40):
    werte = [zufall.choice([zufall.randint(-999, 999), zufall.randint(-3, 123)]) for _ in range(zufall.randint(0, 10))]
    ausgabe = lauf(werte)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(werte)), meldung(werte, ausgabe)

# Obere Grenze: 100 Werte
werte = [(nummer * 37) % 1999 - 999 for nummer in range(100)]
ausgabe = lauf(werte)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(werte)), meldung(werte, ausgabe)
