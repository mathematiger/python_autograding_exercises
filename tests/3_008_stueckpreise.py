# Automatisch erzeugt aus lehrkraft/muster/3_008_stueckpreise.py - nicht von Hand ändern.
# vorlage-hash: 620b8f203d1890bf
# text-hash: 034a408886943783
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
    assert fehler is None and vergleichbar(str(ergebnis)) == vergleichbar("Formatfehler"), (
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
    assert fehler is None and vergleichbar(str(ergebnis)) == vergleichbar("Menge ist 0"), (
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

class Position(dict):
    """Ein Dictionary, das sich merkt, welche Felder gelesen wurden (auch fehlende)."""

    def __getitem__(self, schluessel):
        """Merkt sich den Schlüssel und liest dann wie ein gewöhnliches Dictionary."""
        gelesen.append(schluessel)
        return dict.__getitem__(self, schluessel)


class Protokoll(list):
    """Eine Liste, die sich bei jedem append merkt, welche Felder bis dahin gelesen waren."""

    def append(self, wert):
        """Merkt sich den Stand der gelesenen Felder und hängt dann an."""
        stand_beim_anhaengen.append(list(gelesen))
        list.append(self, wert)


# Protokolliert wird erst nach der Bearbeitung, in jedem Fall
for felder, art in [
    ({"artikel": "Maus", "gesamt": "59.70", "menge": "3"}, "einer gültigen Position"),
    ({"artikel": "Kabel", "gesamt": "12,50", "menge": "5"}, "einem Formatfehler"),
    ({"artikel": "Dock", "gesamt": "149.00", "menge": "0"}, "Menge 0"),
    ({"artikel": "Monitor", "gesamt": "199.00"}, "einem fehlenden Feld"),
]:
    gelesen = []
    stand_beim_anhaengen = []
    protokoll = Protokoll()
    try:
        stueckpreis(Position(felder), protokoll)
    except KeyError:
        pass
    vorher = stand_beim_anhaengen[0] if stand_beim_anhaengen else None
    assert vorher is not None and "gesamt" in vorher, (
        f"Bei {art} hängt stueckpreis den Artikel an, als erst diese Felder gelesen waren: {vorher!r}; "
        'erwartet war, dass "gesamt" schon gelesen ist.\n'
        "Tipp: Das Protokoll gehört nicht an den Anfang der Funktion, sondern in den finally-Block: "
        "Er läuft nach der Bearbeitung, egal ob sie geklappt hat."
    )

# Viele zufällige Positionen: gültig, mit Formatfehler oder mit Menge 0 (nicht fest hinschreiben!)
zufall = Zufall(3008)
zufaellige = []
for runde in range(400):
    cent = zufall.randint(0, 10000000)
    stueck = zufall.randint(1, 10000)
    gesamt = str(cent // 100) + "." + str(cent % 100).zfill(2)
    art = zufall.choice(["gültig", "gültig", "Komma", "Wort", "Menge 0"])
    if art == "Komma":
        gesamt = gesamt.replace(".", ",")
    if art == "Wort":
        gesamt = zufall.choice(["zehn", "", "EUR 5", "n/a"])
    if art == "Menge 0":
        stueck = 0
    position = {"artikel": "Artikel " + str(runde), "gesamt": gesamt, "menge": str(stueck)}
    zufaellige.append((position, art, cent, stueck))
for position, art, cent, stueck in zufaellige:
    protokoll = []
    ergebnis = stueckpreis(position, protokoll)
    if art == "gültig":
        erwartet = round(cent / 100 / stueck, 2)
        richtig = isinstance(ergebnis, (int, float)) and abs(ergebnis - cent / 100 / stueck) <= 0.00501 and ergebnis == round(ergebnis, 2)
    elif art == "Menge 0":
        erwartet = "Menge ist 0"
        richtig = vergleichbar(str(ergebnis)) == vergleichbar(erwartet)
    else:
        erwartet = "Formatfehler"
        richtig = vergleichbar(str(ergebnis)) == vergleichbar(erwartet)
    assert richtig, f"stueckpreis({position}, protokoll) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Bei denselben zufälligen Positionen landet jede genau einmal im Protokoll
for position, _, _, _ in zufaellige:
    protokoll = []
    ergebnis = stueckpreis(position, protokoll)
    assert protokoll == [position["artikel"]], (
        f"stueckpreis({position}, protokoll) ergibt {ergebnis!r} mit protokoll {protokoll!r}; "
        f"erwartet war protokoll {[position['artikel']]!r}."
    )

# Gesamtpreise und Mengen an den Grenzen
for gesamt, menge, erwartet in [("100000.00", "10000", 10.0), ("100000.00", "3", 33333.33), ("0.01", "10000", 0.0), ("100000", "1", 100000.0)]:
    ergebnis = stueckpreis({"artikel": "Server", "gesamt": gesamt, "menge": menge}, [])
    assert ergebnis == erwartet, f"Für Gesamtpreis {gesamt!r} und Menge {menge!r} ergibt stueckpreis {ergebnis!r}, erwartet war {erwartet}."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Maus 19.9\nKabel Formatfehler\nDock Menge ist 0\nBearbeitet: ['Maus', 'Kabel', 'Dock']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
