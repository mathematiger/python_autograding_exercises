# Automatisch erzeugt aus lehrkraft/muster/3_007_durchlaufzeiten.py - nicht von Hand ändern.
# vorlage-hash: 53787528bee58fc5

# Ganze Zahlen und Kommazahlen werden umgewandelt
for text, erwartet in [("42", 42.0), ("37.5", 37.5), ("0", 0.0), ("120", 120.0)]:
    try:
        ergebnis = als_minuten(text)
        fehler = None
    except Exception as ausnahme:
        ergebnis = None
        fehler = ausnahme
    assert fehler is None and ergebnis == erwartet, (
        f"als_minuten({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}; aufgetretene Ausnahme: {fehler!r}.\n"
        "Tipp: Wandeln Sie mit float(text) um. Eine Prüfung mit isdigit() erkennt keine Zahlen mit Punkt."
    )

# Leerzeichen am Rand stören nicht
ergebnis = als_minuten(" 37.5 ")
assert ergebnis == 37.5, f'als_minuten(" 37.5 ") ergibt {ergebnis!r}, erwartet war 37.5.'

# Unbrauchbare Texte ergeben None statt eines Absturzes
for text in ["n/a", "", "4S", "zwölf", "--"]:
    try:
        ergebnis = als_minuten(text)
        fehler = None
    except Exception as ausnahme:
        ergebnis = None
        fehler = ausnahme
    assert fehler is None and ergebnis is None, (
        f"als_minuten({text!r}) muss None zurückgeben; Ergebnis: {ergebnis!r}, aufgetretene Ausnahme: {fehler!r}.\n"
        "Tipp: Fangen Sie den ValueError von float(...) mit try und except ValueError ab."
    )

# Das Beispiel aus der Aufgabe
try:
    ergebnis = auswerten(["40", "n/a", "50", "", "45"])
    fehler = None
except Exception as ausnahme:
    ergebnis = None
    fehler = ausnahme
assert fehler is None and ergebnis == (45.0, 2), (
    f'auswerten(["40", "n/a", "50", "", "45"]) ergibt {ergebnis!r}, erwartet war (45.0, 2); '
    f"aufgetretene Ausnahme: {fehler!r}.\n"
    "Tipp: Der Mittelwert ist die Summe der brauchbaren Werte geteilt durch deren Anzahl, nicht durch alle Werte."
)

# Weitere Messreihen (nicht fest hinschreiben!)
for werte, erwartet in [
    (["10", "20"], (15.0, 0)),
    (["12.5", "x", "7.5", "y", "z"], (10.0, 3)),
    (["90"], (90.0, 0)),
    (["0", "0", "30"], (10.0, 0)),
]:
    ergebnis = auswerten(werte)
    assert ergebnis == erwartet, f"auswerten({werte}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ohne brauchbaren Wert ist der Mittelwert None
for werte, erwartet in [(["n/a"], (None, 1)), (["", "-"], (None, 2)), ([], (None, 0))]:
    try:
        ergebnis = auswerten(werte)
        fehler = None
    except ZeroDivisionError as ausnahme:
        ergebnis = None
        fehler = ausnahme
    assert fehler is None and ergebnis == erwartet, (
        f"auswerten({werte}) ergibt {ergebnis!r}, erwartet war {erwartet}; aufgetretene Ausnahme: {fehler!r}.\n"
        "Tipp: Ohne brauchbaren Wert dürfen Sie nicht teilen. Geben Sie dann None als Mittelwert zurück."
    )

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Mittlere Durchlaufzeit: 45.0 Minuten\nUnbrauchbare Werte: 2"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
