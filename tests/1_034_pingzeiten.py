# Automatisch erzeugt aus lehrkraft/muster/1_034_pingzeiten.py - nicht von Hand ändern.
# vorlage-hash: 3fba0d06ad42190b
# text-hash: 1726ba1d029874c2
# thema: kontrollfluss
# inhalt: Eingabeschleife bis stop

EINGABEN = ["12", "18", "30", "stop"]


def erwartete_ausgabe(werte):
    """Baut die erwartete Ausgabe mit sum und len statt einer Schleife."""
    if not werte:
        return "Keine Messungen."
    return f"{len(werte)} Messungen, Durchschnitt: {sum(werte) / len(werte):.1f} ms"


def pruefe_lauf(werte):
    """Startet das Programm mit diesen Werten und stop; liefert die Ausgabe oder eine Beschreibung des Abbruchs."""
    try:
        return starte(*[str(wert) for wert in werte], "stop")
    except Exception as fehler:
        return f"(Abbruch: {type(fehler).__name__} {fehler})"


def hinweis_zu(ausgabe, werte):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if "KeineEingabeMehr" in ausgabe or "Endlosschleife" in ausgabe:
        return "\nTipp: Nach stop darf das Programm nicht mehr fragen; prüfen Sie die Bedingung eingabe != \"stop\"."
    if "'stop'" in ausgabe or "invalid literal" in ausgabe:
        return "\nTipp: stop ist keine Zahl. Prüfen Sie die Eingabe in der while-Bedingung, bevor Sie int(...) aufrufen."
    if "'str'" in ausgabe:
        return "\nTipp: Addieren Sie int(eingabe), nicht den Text eingabe."
    if werte and vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(werte[1:])):
        return "\nTipp: Der erste Wert fehlt. Verarbeiten Sie die Eingabe im Block, bevor Sie die nächste lesen."
    if len(werte) > 1 and vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(werte[:1])):
        return "\nTipp: Fragen Sie am Ende des Blocks mit input(...) nach dem nächsten Wert."
    return ""


def meldung(werte, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    eingaben = ", ".join([str(wert) for wert in werte] + ["stop"])
    return (
        f"Bei den Eingaben {eingaben} erwartet:\n{erwartete_ausgabe(werte)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, werte)}"
    )


# Im Beispiel werden drei Messungen gezählt
assert vergleichbar("3 Messungen") in vergleichbar(AUSGABE), (
    f"Bei den Eingaben 12, 18, 30, stop erwartet: „3 Messungen“ in der Ausgabe – Ihr Programm gibt aus:\n{AUSGABE}"
    f"{hinweis_zu(AUSGABE, [12, 18, 30])}"
)

# Das Beispiel aus der Aufgabe: 12, 18, 30, stop
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe([12, 18, 30])), meldung([12, 18, 30], AUSGABE)

# Andere Werte (nicht fest hinschreiben!)
werte = [100, 250, 40, 7, 3]
ausgabe = pruefe_lauf(werte)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(werte)), meldung(werte, ausgabe)

# Eine einzige Messung
ausgabe = pruefe_lauf([42])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([42])), meldung([42], ausgabe)

# Gleich stop: keine Messungen
ausgabe = pruefe_lauf([])
assert vergleichbar(ausgabe) == vergleichbar("Keine Messungen."), meldung([], ausgabe)

# Der Durchschnitt wird mit einer Nachkommastelle ausgegeben: 1 und 2 ergeben 1.5
ausgabe = pruefe_lauf([1, 2])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe([1, 2])), meldung([1, 2], ausgabe)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# 40 zufällige Messreihen
zufall = Zufall(1034)
for _ in range(40):
    werte = [zufall.randint(1, 2000) for _ in range(zufall.randint(0, 12))]
    ausgabe = pruefe_lauf(werte)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(werte)), meldung(werte, ausgabe)

# Obere Grenze: 50 Messungen, auch die Ränder 1 und 2000
werte = [1, 2000] + [(nummer * 37) % 2000 + 1 for nummer in range(48)]
ausgabe = pruefe_lauf(werte)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(werte)), meldung(werte, ausgabe)
