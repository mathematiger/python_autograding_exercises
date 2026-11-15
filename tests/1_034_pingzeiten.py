# Automatisch erzeugt aus lehrkraft/muster/1_034_pingzeiten.py - nicht von Hand ändern.
# vorlage-hash: caebd7310f11ab36
# text-hash: b3855dfcaad9a635
# thema: kontrollfluss
# inhalt: Eingabeschleife bis stop

EINGABEN = ["23", "41", "18", "stop"]


def erwartete_ausgabe(zeiten):
    """Baut die erwartete Ausgabe mit sum und len statt einer Schleife."""
    if not zeiten:
        return "Keine Messungen."
    return f"{len(zeiten)} Messungen, Durchschnitt: {sum(zeiten) / len(zeiten):.1f} ms"


def lauf(zeiten):
    """Startet das Programm mit diesen Zeiten und stop; liefert die Ausgabe oder eine Beschreibung des Abbruchs."""
    try:
        return starte(*[str(zeit) for zeit in zeiten], "stop")
    except Exception as fehler:
        return f"(Abbruch: {fehler})"


def hinweis_zu(ausgabe, zeiten):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if "stop" in ausgabe and "int" in ausgabe:
        return (
            "\nTipp: Das Wort stop darf nicht mit int(...) umgewandelt werden. Lesen Sie die nächste Eingabe "
            "als letzte Zeile im Block, dann prüft die Bedingung sie, bevor gerechnet wird."
        )
    if "öfter nach einer Eingabe" in ausgabe:
        return "\nTipp: Die Schleife soll enden, sobald die Eingabe stop ist: while eingabe != \"stop\":"
    if zeiten and f"{len(zeiten) + 1} Messungen" in ausgabe:
        return "\nTipp: stop ist keine Messung. Zählen Sie erst, nachdem die Bedingung die Eingabe geprüft hat."
    if len(zeiten) > 1 and f"{len(zeiten)} Messungen, Durchschnitt: {zeiten[-1] / len(zeiten):.1f} ms" in ausgabe:
        return "\nTipp: In summe gehören alle Zeiten, nicht nur die letzte: summe = summe + int(eingabe)."
    return ""


def meldung(zeiten, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    eingaben = ", ".join([str(zeit) for zeit in zeiten] + ["stop"])
    return (
        f"Bei den Eingaben {eingaben} erwartet:\n{erwartete_ausgabe(zeiten)}\nIhr Programm gibt aus:\n{ausgabe}"
        f"{hinweis_zu(ausgabe, zeiten)}"
    )


# Im Beispiel: anzahl zählt drei Messungen
assert vergleichbar("3 Messungen") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 23, 41, 18, stop erwartet: "3 Messungen, …"\nIhr Programm gibt aus:\n{AUSGABE}'
    f"{hinweis_zu(AUSGABE, [23, 41, 18])}"
)

# Das Beispiel aus der Aufgabe: Durchschnitt 27.3 ms
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe([23, 41, 18])), meldung([23, 41, 18], AUSGABE)

# Andere Zeiten (nicht fest hinschreiben!)
ausgabe = lauf([100, 250])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([100, 250])), meldung([100, 250], ausgabe)

# Fünf Messungen
ausgabe = lauf([5, 7, 6, 12, 9])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([5, 7, 6, 12, 9])), meldung([5, 7, 6, 12, 9], ausgabe)

# Gleich stop: keine Messung
ausgabe = lauf([])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([])), (
    meldung([], ausgabe) + "\nTipp: Ist die erste Eingabe schon stop, läuft die Schleife gar nicht."
)

# Eine einzige Messung
ausgabe = lauf([2000])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([2000])), meldung([2000], ausgabe)

# Auch 0 ms ist eine Messung
ausgabe = lauf([0, 0])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([0, 0])), meldung([0, 0], ausgabe)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# 40 zufällige Messreihen
zufall = Zufall(1034)
for _ in range(40):
    zeiten = [zufall.randint(0, 2000) for _ in range(zufall.randint(0, 12))]
    ausgabe = lauf(zeiten)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(zeiten)), meldung(zeiten, ausgabe)

# Obere Grenze: 100 Messungen
zeiten = [(nummer * 37) % 2001 for nummer in range(100)]
ausgabe = lauf(zeiten)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(zeiten)), meldung(zeiten, ausgabe)
