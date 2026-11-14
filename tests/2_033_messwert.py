# Automatisch erzeugt aus lehrkraft/muster/2_033_messwert.py - nicht von Hand ändern.
# vorlage-hash: 0bc0b00ae3485d7c
# text-hash: fa1b23ac17f5486e
# thema: fehler
# inhalt: try/except in einer Funktion

def rufe_auf(text):
    """Ruft als_minuten(text) auf und liefert das Ergebnis und eine aufgetretene Ausnahme (sonst None)."""
    try:
        return als_minuten(text), None
    except Exception as ausnahme:
        return None, ausnahme


def meldung(text, ergebnis, fehler, erwartet):
    """Baut die Fehlermeldung; nennt eine aufgetretene Ausnahme mit Tipp."""
    if fehler is not None:
        return (
            f"als_minuten({text!r}) ist mit {type(fehler).__name__} abgestürzt, erwartet war {erwartet!r}.\n"
            "Tipp: Fangen Sie den ValueError von float(...) mit try und except ValueError ab."
        )
    return f"als_minuten({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."


# Das Beispiel aus der Aufgabe: "42" wird 42.0
ergebnis, fehler = rufe_auf("42")
assert fehler is None and ergebnis == 42.0, meldung("42", ergebnis, fehler, 42.0)

# Weitere Zahlen, auch mit Nachkommastellen (nicht fest 42 hinschreiben!)
for text, erwartet in [("37.5", 37.5), ("120", 120.0), ("0.25", 0.25), ("7", 7.0)]:
    ergebnis, fehler = rufe_auf(text)
    hinweis = ""
    if ergebnis == -1 and "." in text:
        hinweis = "\nTipp: Wandeln Sie mit float(text) um; int(...) oder isdigit() kennen keine Kommazahlen."
    assert fehler is None and ergebnis == erwartet, meldung(text, ergebnis, fehler, erwartet) + hinweis

# Leerzeichen am Rand stören nicht
for text, erwartet in [(" 12 ", 12.0), ("  37", 37.0), ("8   ", 8.0)]:
    ergebnis, fehler = rufe_auf(text)
    assert fehler is None and ergebnis == erwartet, meldung(text, ergebnis, fehler, erwartet)

# Eine Durchlaufzeit von 0 Minuten ist brauchbar
ergebnis, fehler = rufe_auf("0")
assert fehler is None and ergebnis == 0.0, (
    meldung("0", ergebnis, fehler, 0.0) + "\nTipp: 0 ist eine echte Messung; nur unbrauchbare Texte ergeben -1."
)

# Unbrauchbare Texte ergeben -1 statt eines Absturzes
for text in ["n/a", "", "4S", "zwölf", "--", "1.2.3", "   ", "x"]:
    ergebnis, fehler = rufe_auf(text)
    assert fehler is None and ergebnis == -1, meldung(text, ergebnis, fehler, -1)

# Ein Komma statt eines Punkts ist unbrauchbar
ergebnis, fehler = rufe_auf("1,5")
assert fehler is None and ergebnis == -1, (
    meldung("1,5", ergebnis, fehler, -1) + "\nPython schreibt Kommazahlen mit Punkt, float('1,5') scheitert also."
)

# Es wird mit float umgewandelt
assert verwendet("float"), "Wandeln Sie den Text mit float(text) in eine Zahl um."


# Ein float, das nie umwandeln kann: So zeigt sich, ob der Fehlschlag wirklich abgefangen wird
def scheiterndes_float(text):
    """Tut so, als könne float den Text nicht umwandeln."""
    raise ValueError(f"could not convert string to float: {text!r}")


# Scheitert float(...), fängt die Funktion den ValueError ab
try:
    float = scheiterndes_float
    ergebnis, fehler = rufe_auf("42")
finally:
    del float
assert fehler is None and ergebnis == -1, (
    "Für diesen Test scheitert float(...) bei jedem Text mit ValueError.\n"
    + meldung("42", ergebnis, fehler, -1)
    + "\nTipp: Prüfen Sie den Text nicht vorher selbst, sondern probieren Sie float(text) in einem try-Block aus "
    "und geben Sie im Block unter except ValueError: -1 zurück."
)


# Ein float mit einem ganz anderen Fehler: Der soll nicht verschluckt werden
def kaputtes_float(text):
    """Tut so, als hätte das Programm einen Fehler, der mit dem Text nichts zu tun hat."""
    raise TypeError("ein anderer Fehler")


# Nur der ValueError wird abgefangen, andere Fehler werden weiter gemeldet
try:
    float = kaputtes_float
    ergebnis, fehler = rufe_auf("42")
finally:
    del float
assert isinstance(fehler, TypeError), (
    f"Wenn in float(...) ein TypeError auftritt, ergibt als_minuten('42') {ergebnis!r}; erwartet war, dass der "
    "TypeError weiter gemeldet wird.\n"
    "Tipp: Schreiben Sie except ValueError: statt nur except: oder except Exception:, damit Sie nur den "
    "Fehler abfangen, mit dem Sie rechnen."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("42.0\n-1"), f"Erwartete Ausgabe:\n42.0\n-1\nIhr Programm gibt aus:\n{AUSGABE}"

# Viele zufällige Messwerte, brauchbare und kaputte gemischt
zufall = Zufall(2033)
kaputte = ["", "n/a", "4S", "--", "zwölf", "1,5", "x", "?", "12 min", "3..5", "-", "."]
for _ in range(500):
    if zufall.random() < 0.4:
        text = zufall.choice(kaputte)
        erwartet = -1
    else:
        erwartet = zufall.randint(0, 40000) / 4
        zahlentext = str(erwartet).removesuffix(".0")
        text = " " * zufall.randint(0, 2) + zahlentext + " " * zufall.randint(0, 2)
    ergebnis, fehler = rufe_auf(text)
    assert fehler is None and ergebnis == erwartet, meldung(text, ergebnis, fehler, erwartet)

# Die Ränder der Grenzen: 10 000 Minuten und Texte mit 20 Zeichen
for text, erwartet in [("10000", 10000.0), ("10000.0", 10000.0), (" " * 15 + "10000", 10000.0), ("x" * 20, -1)]:
    ergebnis, fehler = rufe_auf(text)
    assert fehler is None and ergebnis == erwartet, meldung(text, ergebnis, fehler, erwartet)
