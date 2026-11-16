# Automatisch erzeugt aus lehrkraft/muster/1_035_altersangaben.py - nicht von Hand ändern.
# vorlage-hash: fc847d035b865977
# text-hash: 2060fcd8e1471d91
# thema: kontrollfluss
# inhalt: Übung: while

EINGABEN = ["34", "250", "17", "-3", "52", "stop"]


def erwartete_ausgabe(werte):
    """Baut die erwartete Ausgabe mit einer Liste der gültigen Werte statt mit Zählern."""
    gut = [wert for wert in werte if 0 <= wert <= 120]
    if gut:
        erste = f"{len(gut)} gültige Angaben, Durchschnittsalter: {sum(gut) / len(gut):.1f} Jahre"
    else:
        erste = "Keine gültigen Angaben."
    return f"{erste}\n{len(werte) - len(gut)} Angaben zur Prüfung zurückgestellt."


def lauf(werte):
    """Startet das Programm mit diesen Angaben und stop; liefert die Ausgabe oder eine Beschreibung des Abbruchs."""
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
    if f"{len(werte)} gültige" in ausgabe and len(werte) > 0:
        return "\nTipp: Nur ein Alter von 0 bis 120 ist gültig; prüfen Sie es mit if, bevor Sie zählen."
    return ""


def meldung(werte, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    eingaben = ", ".join([str(wert) for wert in werte] + ["stop"])
    return (
        f"Bei den Eingaben {eingaben} erwartet:\n{erwartete_ausgabe(werte)}\nIhr Programm gibt aus:\n{ausgabe}"
        f"{hinweis_zu(ausgabe, werte)}"
    )


def zeilen_von(ausgabe):
    """Teilt die Ausgabe in vergleichbare Zeilen."""
    return [vergleichbar(zeile) for zeile in ausgabe.split("\n")]


BEISPIEL = [34, 250, 17, -3, 52]

# Im Beispiel: drei gültige Angaben
assert vergleichbar("3 gültige Angaben") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 34, 250, 17, -3, 52, stop erwartet: "3 gültige Angaben, …"\nIhr Programm gibt aus:\n{AUSGABE}'
    f"{hinweis_zu(AUSGABE, BEISPIEL)}"
)

# Im Beispiel: zwei Angaben zurückgestellt
assert vergleichbar("2 Angaben zur Prüfung zurückgestellt.") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 34, 250, 17, -3, 52, stop erwartet: "2 Angaben zur Prüfung zurückgestellt."\n'
    f"Ihr Programm gibt aus:\n{AUSGABE}\nTipp: Erhöhen Sie ungueltig im else-Zweig um 1."
)

# Das Beispiel aus der Aufgabe: Durchschnitt 34.3 Jahre
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(BEISPIEL)), meldung(BEISPIEL, AUSGABE) + (
    "\nTipp: In summe gehören nur die gültigen Angaben." if "Durchschnittsalter: 116" in AUSGABE else ""
)

# Andere Angaben (nicht fest hinschreiben!)
ausgabe = lauf([8, 9, 300])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([8, 9, 300])), meldung([8, 9, 300], ausgabe)

# Nur gültige Angaben
ausgabe = lauf([40, 60, 20, 33])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([40, 60, 20, 33])), meldung([40, 60, 20, 33], ausgabe)

# Gleich stop: keine Angabe
ausgabe = lauf([])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([])), (
    meldung([], ausgabe) + "\nTipp: Ist die erste Eingabe schon stop, läuft die Schleife gar nicht."
)

# Nur ungültige Angaben
ausgabe = lauf([-1, 121, 999])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([-1, 121, 999])), meldung([-1, 121, 999], ausgabe)

# Grenze 0 Jahre gehört dazu
ausgabe = lauf([0, 10])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([0, 10])), (
    meldung([0, 10], ausgabe) + "\nTipp: Ein Alter von genau 0 ist gültig: alter >= 0, nicht alter > 0."
)

# Grenze 120 Jahre gehört dazu
ausgabe = lauf([120])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([120])), (
    meldung([120], ausgabe) + "\nTipp: Ein Alter von genau 120 ist gültig: alter <= 120, nicht alter < 120."
)

# Knapp daneben: -1 und 121 sind ungültig
ausgabe = lauf([-1, 50, 121])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([-1, 50, 121])), meldung([-1, 50, 121], ausgabe)

# Kleinster und größter Wert der Grenzen: -999 und 999
ausgabe = lauf([-999, 999, 1])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([-999, 999, 1])), meldung([-999, 999, 1], ausgabe)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# 40 zufällige Eingabereihen
zufall = Zufall(1035)
for _ in range(40):
    werte = [zufall.randint(-150, 250) for _ in range(zufall.randint(0, 12))]
    ausgabe = lauf(werte)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(werte)), meldung(werte, ausgabe)

# Obere Grenze: 100 Angaben
werte = [(nummer * 37) % 1999 - 999 for nummer in range(100)]
ausgabe = lauf(werte)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(werte)), meldung(werte, ausgabe)
