# Automatisch erzeugt aus lehrkraft/muster/3_008_stueckpreise.py - nicht von Hand ändern.
# vorlage-hash: 151686557989e347
# thema: fehler
# inhalt: Mehrere except, else und finally

# Ein gültiger Stückpreis wird berechnet
protokoll = []
ergebnis = stueckpreis({"artikel": "Maus", "gesamt": "59.70", "menge": "3"}, protokoll)
assert ergebnis == 19.9, f'Für Gesamtpreis "59.70" und Menge "3" ergibt stueckpreis {ergebnis!r}, erwartet war 19.9.'

# Weitere gültige Positionen, auf zwei Nachkommastellen gerundet (nicht fest hinschreiben!)
for gesamt, menge, erwartet in [("100", "4", 25.0), ("10.00", "3", 3.33), ("2.5", "1", 2.5), ("0", "7", 0.0)]:
    ergebnis = stueckpreis({"artikel": "Test", "gesamt": gesamt, "menge": menge}, [])
    assert ergebnis == erwartet, (
        f"Für Gesamtpreis {gesamt!r} und Menge {menge!r} ergibt stueckpreis {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Teilen Sie den Gesamtpreis durch die Menge und runden Sie mit round(..., 2)."
    )

# Nicht umwandelbare Werte ergeben "Formatfehler"
for gesamt, menge in [("12,50", "5"), ("zehn", "2"), ("", "1"), ("20.00", "2.5"), ("20.00", "drei")]:
    try:
        ergebnis = stueckpreis({"artikel": "Test", "gesamt": gesamt, "menge": menge}, [])
        fehler = None
    except Exception as ausnahme:
        ergebnis = None
        fehler = ausnahme
    assert fehler is None and ergebnis == "Formatfehler", (
        f"Für Gesamtpreis {gesamt!r} und Menge {menge!r} muss stueckpreis \"Formatfehler\" zurückgeben; "
        f"Ergebnis: {ergebnis!r}, aufgetretene Ausnahme: {fehler!r}.\n"
        "Tipp: float(...) und int(...) lösen bei einem ungültigen Text einen ValueError aus."
    )

# Menge 0 ergibt "Menge ist 0"
for gesamt in ["149.00", "0"]:
    try:
        ergebnis = stueckpreis({"artikel": "Dock", "gesamt": gesamt, "menge": "0"}, [])
        fehler = None
    except Exception as ausnahme:
        ergebnis = None
        fehler = ausnahme
    assert fehler is None and ergebnis == "Menge ist 0", (
        f'Für Gesamtpreis {gesamt!r} und Menge "0" muss stueckpreis "Menge ist 0" zurückgeben; '
        f"Ergebnis: {ergebnis!r}, aufgetretene Ausnahme: {fehler!r}.\n"
        "Tipp: Eine Division durch 0 löst einen ZeroDivisionError aus. Fangen Sie ihn in einem eigenen except-Block ab."
    )

# Jede Position landet im Protokoll, auch die fehlerhaften
protokoll = []
for position in [
    {"artikel": "Maus", "gesamt": "59.70", "menge": "3"},
    {"artikel": "Kabel", "gesamt": "12,50", "menge": "5"},
    {"artikel": "Dock", "gesamt": "149.00", "menge": "0"},
    {"artikel": "Headset", "gesamt": "80", "menge": "2"},
]:
    try:
        stueckpreis(position, protokoll)
    except Exception:
        pass
assert protokoll == ["Maus", "Kabel", "Dock", "Headset"], (
    f'Nach vier Positionen ist das Protokoll {protokoll!r}, erwartet war ["Maus", "Kabel", "Dock", "Headset"].\n'
    "Tipp: Ein return beendet die Funktion sofort. Was immer passieren soll, gehört in den finally-Block."
)

# Ein fehlendes Feld wird nicht abgefangen
try:
    ergebnis = stueckpreis({"artikel": "Monitor", "gesamt": "199.00"}, [])
    fehler = None
except KeyError as ausnahme:
    fehler = ausnahme
assert fehler is not None, (
    f"Bei einer Position ohne Feld \"menge\" muss ein KeyError auftreten, stueckpreis ergab aber {ergebnis!r}.\n"
    "Tipp: Fangen Sie nur ValueError und ZeroDivisionError ab, nicht alle Ausnahmen."
)

# Auch bei einem fehlenden Feld wird die Position protokolliert
protokoll = []
try:
    stueckpreis({"artikel": "Monitor", "gesamt": "199.00"}, protokoll)
except KeyError:
    pass
assert protokoll == ["Monitor"], (
    f'Nach einer Position ohne Feld "menge" ist das Protokoll {protokoll!r}, erwartet war ["Monitor"].\n'
    "Tipp: Der finally-Block läuft auch dann, wenn eine Ausnahme nicht abgefangen wird."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Maus 19.9\nKabel Formatfehler\nDock Menge ist 0\nBearbeitet: ['Maus', 'Kabel', 'Dock']"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
