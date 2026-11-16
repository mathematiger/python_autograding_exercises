# Automatisch erzeugt aus lehrkraft/muster/1_036_testabdeckung.py - nicht von Hand ändern.
# vorlage-hash: 15250e3dc8c3d073
# text-hash: fc7f828c8b92f5e7
# thema: funktionen
# inhalt: Funktionen aufrufen

EINGABEN = ["800", "412", "536"]


def prozent(getestet, alle):
    """Rechnet die Abdeckung wie die vorgegebene Funktion, aber unabhängig von ihr."""
    return round(100 * getestet / alle, 1)


def erwartete_ausgabe(alle, alt, neu):
    """Baut die erwartete Ausgabe."""
    erst = prozent(alt, alle)
    dann = prozent(neu, alle)
    return (
        f"Abdeckung vorher: {erst} %\nAbdeckung nachher: {dann} %\n"
        f"Verbesserung: {round(dann - erst, 1)} Prozentpunkte"
    )


def lauf(alle, alt, neu):
    """Startet das Programm mit diesen Eingaben; liefert die Ausgabe oder eine Beschreibung des Abbruchs."""
    try:
        return starte(str(alle), str(alt), str(neu))
    except Exception as fehler:
        return f"(Abbruch: {fehler})"


def hinweis_zu(ausgabe, alle, alt, neu):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if "NameError" in ausgabe or "not defined" in ausgabe:
        return "\nTipp: Legen Sie die Variablen prozent_vorher und prozent_nachher genau mit diesen Namen an."
    if alt > 0 and alle != alt and f"vorher: {prozent(alle, alt)} " in ausgabe:
        return "\nTipp: Die Reihenfolge der Argumente zählt: erst die getesteten Zeilen, dann alle Zeilen."
    if f"vorher: {prozent(neu, alle)} " in ausgabe and alt != neu:
        return "\nTipp: prozent_vorher gehört zu den Zeilen vor dem Sprint (vorher), prozent_nachher zu nachher."
    return ""


def meldung(alle, alt, neu, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei den Eingaben {alle}, {alt}, {neu} erwartet:\n{erwartete_ausgabe(alle, alt, neu)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, alle, alt, neu)}"
    )


# Im Beispiel: Abdeckung vor dem Sprint
assert vergleichbar("Abdeckung vorher: 51.5 %") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 800, 412, 536 erwartet in der ersten Zeile: "Abdeckung vorher: 51.5 %"\n'
    f"Ihr Programm gibt aus:\n{AUSGABE}{hinweis_zu(AUSGABE, 800, 412, 536)}"
)

# Im Beispiel: Abdeckung nach dem Sprint
assert vergleichbar("Abdeckung nachher: 67.0 %") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 800, 412, 536 erwartet in der zweiten Zeile: "Abdeckung nachher: 67.0 %"\n'
    f"Ihr Programm gibt aus:\n{AUSGABE}{hinweis_zu(AUSGABE, 800, 412, 536)}"
)

# Das ganze Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(800, 412, 536)), meldung(800, 412, 536, AUSGABE)

# Die Funktion abdeckung wird aufgerufen
assert verwendet("abdeckung"), (
    "Rufen Sie die vorgegebene Funktion auf, etwa prozent_vorher = abdeckung(vorher, gesamt), "
    "statt die Formel selbst hinzuschreiben."
)

# Andere Zahlen (nicht fest hinschreiben!)
ausgabe = lauf(200, 50, 150)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(200, 50, 150)), meldung(200, 50, 150, ausgabe)

# Noch andere Zahlen mit Rundung
ausgabe = lauf(3, 1, 2)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(3, 1, 2)), meldung(3, 1, 2, ausgabe)

# Keine Verbesserung: vorher und nachher gleich
ausgabe = lauf(500, 260, 260)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(500, 260, 260)), meldung(500, 260, 260, ausgabe)

# Ränder: von 0 auf alle Zeilen
ausgabe = lauf(1, 0, 1)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(1, 0, 1)), meldung(1, 0, 1, ausgabe)

# Obere Grenze: 100 000 Zeilen
ausgabe = lauf(100000, 99999, 100000)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(100000, 99999, 100000)), (
    meldung(100000, 99999, 100000, ausgabe)
)

# 40 zufällige Projekte
zufall = Zufall(1036)
for _ in range(40):
    alle = zufall.randint(1, 100000)
    alt = zufall.randint(0, alle)
    neu = zufall.randint(alt, alle)
    ausgabe = lauf(alle, alt, neu)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(alle, alt, neu)), meldung(alle, alt, neu, ausgabe)
