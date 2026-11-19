# Automatisch erzeugt aus lehrkraft/muster/1_038_storypoints.py - nicht von Hand ändern.
# vorlage-hash: d49e88eab74327d7
# text-hash: e9ff3ad549aa5688
# thema: funktionen
# inhalt: Funktion mit return

EINGABEN = ["3", "5"]


def erwartete_ausgabe(a, b):
    """Baut die erwartete Ausgabe für die Story Points a und b, ohne die Funktion des Programms."""
    return (
        f"Story A: {6 * a + 2} Stunden\nStory B: {6 * b + 2} Stunden\n"
        f"Zusammen: {6 * (a + b) + 4} Stunden"
    )


def meldung(a, b, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    return f"Bei den Eingaben {a} und {b} erwartet:\n{erwartete_ausgabe(a, b)}\nIhr Programm gibt aus:\n{ausgabe}"


# stunden(3) liefert 20
ergebnis = stunden(3)
if ergebnis is None:
    hinweis = "\nTipp: Die Funktion liefert None. Geben Sie das Ergebnis mit return zurück statt mit print."
else:
    hinweis = "\nTipp: 6 Stunden je Story Point und 2 Stunden für das Review: punkte * 6 + 2."
assert ergebnis == 20, f"stunden(3) ergibt {ergebnis!r}, erwartet war 20.{hinweis}"

# stunden(5) liefert 32 (nicht fest hinschreiben!)
assert stunden(5) == 32, f"stunden(5) ergibt {stunden(5)!r}, erwartet war 32."

# Eine Story mit 0 Story Points braucht nur das Review
assert stunden(0) == 2, f"stunden(0) ergibt {stunden(0)!r}, erwartet waren 2 Stunden für das Review."

# Das Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(3, 5)), meldung(3, 5, AUSGABE)

# Andere Story Points
ausgabe = starte("8", "1")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(8, 1)), meldung(8, 1, ausgabe)

# Beide Stories mit 0 Story Points
ausgabe = starte("0", "0")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(0, 0)), meldung(0, 0, ausgabe)

# Das Ergebnis kommt mit return zurück
assert verwendet("return"), "Geben Sie die Stunden in der Funktion mit return zurück."

# Viele zufällige Story Points
zufall = Zufall(1038)
for _ in range(40):
    a = zufall.randint(0, 100)
    b = zufall.choice([zufall.randint(0, 100), zufall.randint(0, 3)])
    ausgabe = starte(str(a), str(b))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(a, b)), meldung(a, b, ausgabe)

# Obere Grenze: zweimal 100 Story Points
ausgabe = starte("100", "100")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(100, 100)), meldung(100, 100, ausgabe)
