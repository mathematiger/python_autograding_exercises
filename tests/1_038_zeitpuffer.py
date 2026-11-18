# Automatisch erzeugt aus lehrkraft/muster/1_038_zeitpuffer.py - nicht von Hand ändern.
# vorlage-hash: 2d4a00e513e87341
# text-hash: d77535187fc4b75b
# thema: funktionen
# inhalt: Eigene Funktion mit return

EINGABEN = ["10", "6"]


def erwartete_ausgabe(a, b):
    """Baut die erwartete Ausgabe; in Vierteln gerechnet, damit kein Rundungsfehler entsteht."""
    return f"Arbeitspaket A: {a * 5 / 4} Tage\nArbeitspaket B: {b * 5 / 4} Tage\nZusammen: {(a + b) * 5 / 4} Tage"


def meldung(a, b, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    return f"Bei den Eingaben {a} und {b} erwartet:\n{erwartete_ausgabe(a, b)}\nIhr Programm gibt aus:\n{ausgabe}"


def aufruf(tage):
    """Ruft mit_puffer(tage) auf; liefert das Ergebnis oder einen Text, wenn es die Funktion nicht gibt."""
    try:
        return mit_puffer(tage)
    except NameError:
        return "(keine Funktion mit_puffer gefunden)"


# Die Funktion mit_puffer gibt bei 10 Tagen 12.5 zurück
ergebnis = aufruf(10)
if ergebnis is None:
    hinweis = (
        "\nTipp: Der Aufruf liefert None. Geben Sie den Wert mit return tage * 1.25 zurück, statt ihn mit print "
        "auszugeben."
    )
else:
    hinweis = ""
assert ergebnis == 12.5, f"mit_puffer(10) ergibt {ergebnis!r}, erwartet war 12.5.{hinweis}"

# Andere Schätzung: 4 Tage werden zu 5 Tagen (nicht fest hinschreiben!)
ergebnis = aufruf(4)
assert ergebnis == 5, f"mit_puffer(4) ergibt {ergebnis!r}, erwartet war 5.0 (4 * 1.25)."

# Keine Arbeit: 0 Tage bleiben 0 Tage
ergebnis = aufruf(0)
assert ergebnis == 0, (
    f"mit_puffer(0) ergibt {ergebnis!r}, erwartet war 0.\nTipp: Der Puffer wird malgenommen, nicht addiert."
)

# Ein Tag Schätzung, ein Viertel Tag Puffer
ergebnis = aufruf(1)
assert ergebnis == 1.25, f"mit_puffer(1) ergibt {ergebnis!r}, erwartet war 1.25."

# Im Beispiel: die Zeile für Arbeitspaket A
assert vergleichbar("Arbeitspaket A: 12.5 Tage") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 10 und 6 erwartet die Zeile "Arbeitspaket A: 12.5 Tage" – Ihr Programm gibt aus:\n{AUSGABE}'
)

# Das ganze Beispiel aus der Aufgabe, mit der Summe
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(10, 6)), meldung(10, 6, AUSGABE) + (
    "\nTipp: Ohne return liefert mit_puffer None, und None + None geht nicht." if aufruf(10) is None else ""
)

# Andere Eingaben im ganzen Programm
ausgabe = starte("8", "3")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(8, 3)), meldung(8, 3, ausgabe)

# Beide Schätzungen 0
ausgabe = starte("0", "0")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(0, 0)), meldung(0, 0, ausgabe)

# Viele zufällige Schätzungen
zufall = Zufall(1038)
for _ in range(40):
    a = zufall.randint(0, 1000)
    b = zufall.randint(0, 1000)
    ausgabe = starte(str(a), str(b))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(a, b)), meldung(a, b, ausgabe)

# Obere Grenze: zweimal 1000 Tage
ausgabe = starte("1000", "1000")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(1000, 1000)), meldung(1000, 1000, ausgabe)
