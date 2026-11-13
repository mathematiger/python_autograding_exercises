# Automatisch erzeugt aus lehrkraft/muster/2_040_anforderungen.py - nicht von Hand ändern.
# vorlage-hash: 96515b0cffa6cc0b
# text-hash: 217822654a5ac9fd
# thema: algorithmen
# inhalt: Binärdarstellung von Hand

def vergleich(zahl, stellen=1):
    """Vergleichslösung über Zweierpotenzen von links statt Reste von rechts."""
    potenz = 1
    while potenz * 2 <= zahl:
        potenz = potenz * 2
    ziffern = []
    while potenz >= 1:
        if zahl >= potenz:
            ziffern.append("1")
            zahl = zahl - potenz
        else:
            ziffern.append("0")
        potenz = potenz // 2
    text = "".join(ziffern)
    return "0" * (stellen - len(text)) + text


def aufruf(zahl, stellen=None):
    """Ruft binaer auf; liefert das Ergebnis oder eine Beschreibung des Abbruchs."""
    try:
        if stellen is None:
            return binaer(zahl)
        return binaer(zahl, stellen)
    except Exception as fehler:
        return f"(Abbruch: {type(fehler).__name__}: {fehler})"


def meldung(zahl, stellen, ergebnis):
    """Baut die Fehlermeldung mit Aufruf, Ergebnis und Erwartung."""
    if stellen is None:
        return f"binaer({zahl}) ergibt {ergebnis!r}, erwartet war {vergleich(zahl)!r}."
    return f"binaer({zahl}, {stellen}) ergibt {ergebnis!r}, erwartet war {vergleich(zahl, stellen)!r}."


# Das Beispiel aus der Aufgabe: 11 ist 1011
ergebnis = aufruf(11)
assert ergebnis == "1011", meldung(11, None, ergebnis) + (
    "\nTipp: Die Ziffern kommen von hinten; setzen Sie jede neue Ziffer vorn an den Text." if ergebnis == "1101" else ""
)

# Andere Zahlen (nicht fest hinschreiben!)
for zahl in [6, 13, 100]:
    ergebnis = aufruf(zahl)
    assert ergebnis == vergleich(zahl), meldung(zahl, None, ergebnis) + (
        "\nTipp: Die Ziffern kommen von hinten; setzen Sie jede neue Ziffer vorn an den Text."
        if ergebnis == vergleich(zahl)[::-1] else ""
    )

# Zweierpotenzen: eine 1 und dahinter Nullen
for zahl in [1, 2, 1024]:
    ergebnis = aufruf(zahl)
    assert ergebnis == vergleich(zahl), meldung(zahl, None, ergebnis)

# Das Ergebnis ist ein Text
ergebnis = aufruf(5)
assert isinstance(ergebnis, str), f"binaer(5) ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war der Text '101'."

# Mit stellen wird vorn mit Nullen aufgefüllt
ergebnis = aufruf(11, 6)
assert ergebnis == "001011", meldung(11, 6, ergebnis)

# Ist der Text schon lang genug, wird nichts aufgefüllt und nichts abgeschnitten
for zahl, stellen in [(300, 4), (11, 4), (255, 3)]:
    ergebnis = aufruf(zahl, stellen)
    assert ergebnis == vergleich(zahl, stellen), meldung(zahl, stellen, ergebnis)

# Die Zahl 0 ist "0"
ergebnis = aufruf(0)
assert ergebnis == "0", meldung(0, None, ergebnis) + "\nTipp: Bei 0 läuft die Schleife gar nicht; was steht dann im Text?"

# Die Zahl 0 mit stellen
ergebnis = aufruf(0, 4)
assert ergebnis == "0000", meldung(0, 4, ergebnis)

# Ohne bin(...) und format(...)
assert not verwendet("bin") and not verwendet("format"), (
    "Rechnen Sie die Binärziffern mit // und % selbst aus, ohne bin(...) oder format(...)."
)

# Viele zufällige Zahlen und Stellenzahlen
zufall = Zufall(2040)
for _ in range(2000):
    zahl = zufall.randrange(2 ** zufall.randint(1, 60))
    stellen = zufall.randint(1, 64)
    ergebnis = aufruf(zahl, stellen)
    assert ergebnis == vergleich(zahl, stellen), meldung(zahl, stellen, ergebnis)

# Obere Grenze: die größte erlaubte Zahl, und 64 Stellen
for zahl, stellen in [(2**60 - 1, None), (2**59, 64), (2**60 - 1, 64), (1, 64)]:
    ergebnis = aufruf(zahl, stellen)
    erwartet = vergleich(zahl) if stellen is None else vergleich(zahl, stellen)
    assert ergebnis == erwartet, meldung(zahl, stellen, ergebnis)
