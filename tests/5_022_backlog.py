# Automatisch erzeugt aus lehrkraft/muster/5_022_backlog.py - nicht von Hand ändern.
# vorlage-hash: 184f42ed6fa6ec9a
# text-hash: e0f0b930c756131c
# thema: datenstrukturen
# inhalt: Eigenes Mapping

def versuche(funktion, *argumente, **schluesselwoerter):
    """Ruft funktion auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(*argumente, **schluesselwoerter), None
    except Exception as fehler:
        return None, fehler


def ausnahme_text(fehler):
    """Kurze Beschreibung einer Ausnahme für Meldungen."""
    return "keine Ausnahme" if fehler is None else f"{type(fehler).__name__}: {fehler}"


# Eintragen und mit derselben Schreibweise lesen
backlog = Backlog()
backlog["PROJ-12"] = 3
wert, fehler = versuche(backlog.__getitem__, "PROJ-12")
assert wert == 3, f"Nach backlog['PROJ-12'] = 3 ergibt backlog['PROJ-12'] {wert!r} ({ausnahme_text(fehler)}), erwartet war 3."

# Eintragen und mit anderer Schreibweise lesen
backlog = Backlog()
backlog["Proj-12"] = 3
ergebnis = [versuche(backlog.__getitem__, text)[0] for text in ["PROJ-12", "proj-12", " proj-0012 "]]
assert ergebnis == [3, 3, 3], (
    f"Nach backlog['Proj-12'] = 3 ergeben backlog['PROJ-12'], ['proj-12'], [' proj-0012 '] {ergebnis!r}, erwartet war [3, 3, 3].\n"
    "Tipp: Normalisieren Sie den Schlüssel in __setitem__ und in __getitem__ mit normalisiere(...)."
)

# Gespeichert wird unter dem normalisierten Schlüssel
backlog = Backlog()
backlog[" proj-007 "] = 5
assert list(backlog) == ["PROJ-7"] and len(backlog) == 1, (
    f"Nach backlog[' proj-007 '] = 5 ergibt list(backlog) {list(backlog)!r} und len {len(backlog)}, erwartet ['PROJ-7'] und 1."
)

# Überschreiben mit anderer Schreibweise ergibt keinen zweiten Eintrag
backlog = Backlog()
backlog["proj-7"] = 5
backlog["PROJ-007"] = 8
assert (len(backlog), backlog["PROJ-7"]) == (1, 8), (
    f"Nach backlog['proj-7'] = 5 und backlog['PROJ-007'] = 8 sind len und Wert {(len(backlog), backlog['PROJ-7'])!r}, erwartet (1, 8)."
)

# Fehlender Schlüssel: KeyError
backlog = Backlog()
backlog["PROJ-1"] = 2
_, fehler = versuche(backlog.__getitem__, "PROJ-2")
assert isinstance(fehler, KeyError), f"backlog['PROJ-2'] (nicht eingetragen) muss einen KeyError auslösen, bekommen: {ausnahme_text(fehler)}."

# Ungültiger Schlüssel beim Lesen: KeyError, kein ValueError
for text in ["ohne Nummer", "PROJ42", "", 42, None]:
    _, fehler = versuche(backlog.__getitem__, text)
    assert isinstance(fehler, KeyError), (
        f"backlog[{text!r}] muss einen KeyError auslösen, bekommen: {ausnahme_text(fehler)}.\n"
        "Tipp: Fangen Sie in __getitem__ den ValueError aus normalisiere ab und lösen Sie KeyError(schluessel) aus."
    )

# Ungültiger Schlüssel beim Eintragen: ValueError, nichts wird gespeichert
backlog = Backlog()
for text in ["ohne Nummer", "-12", "PROJ-", 7]:
    _, fehler = versuche(backlog.__setitem__, text, 1)
    assert isinstance(fehler, ValueError) and len(backlog) == 0, (
        f"backlog[{text!r}] = 1 muss einen ValueError auslösen und nichts speichern; bekommen: {ausnahme_text(fehler)}, "
        f"len danach {len(backlog)}."
    )

# Löschen mit anderer Schreibweise
backlog = Backlog()
backlog["WEB-3"] = 8
backlog["WEB-4"] = 1
_, fehler = versuche(backlog.__delitem__, " web-003")
assert fehler is None and list(backlog) == ["WEB-4"], (
    f"Nach del backlog[' web-003'] ({ausnahme_text(fehler)}) ist list(backlog) {list(backlog)!r}, erwartet ['WEB-4']."
)

# Löschen eines fehlenden oder ungültigen Schlüssels: KeyError
for text in ["WEB-99", "Unsinn"]:
    _, fehler = versuche(backlog.__delitem__, text)
    assert isinstance(fehler, KeyError) and list(backlog) == ["WEB-4"], (
        f"del backlog[{text!r}] muss einen KeyError auslösen und nichts löschen; bekommen: {ausnahme_text(fehler)}, "
        f"list danach {list(backlog)!r}."
    )

# Der Konstruktor übernimmt ein Dictionary und Schlüsselwörter
backlog, fehler = versuche(Backlog, {"proj-7": 5}, WEB_3=8)
assert backlog is not None and dict(backlog.items()) == {"PROJ-7": 5, "WEB-3": 8}, (
    f"Backlog({{'proj-7': 5}}, WEB_3=8) ergibt {backlog!r} ({ausnahme_text(fehler)}), erwartet die Einträge PROJ-7: 5 und WEB-3: 8.\n"
    "Tipp: Rufen Sie im __init__ self.update(daten, **weitere) auf, nachdem Sie das innere Dictionary angelegt haben."
)

# Der Konstruktor übernimmt auch eine Folge von Paaren und normalisiert dabei
backlog, fehler = versuche(Backlog, [("a-1", 1), ("A-01", 2), ("b-2", 3)])
assert backlog is not None and dict(backlog.items()) == {"A-1": 2, "B-2": 3}, (
    f"Backlog([('a-1', 1), ('A-01', 2), ('b-2', 3)]) ergibt {backlog!r} ({ausnahme_text(fehler)}), erwartet {{'A-1': 2, 'B-2': 3}}."
)

# Ein leerer Backlog
leer = Backlog()
assert (len(leer), list(leer), dict(leer.items())) == (0, [], {}), f"Backlog() ergibt len, list, items {(len(leer), list(leer))!r}."

# Reihenfolge des ersten Eintrags, auch nach Überschreiben
backlog = Backlog()
for text in ["c-3", "a-1", "b-2", "C-03"]:
    backlog[text] = text
assert list(backlog) == ["C-3", "A-1", "B-2"], (
    f"Nach dem Eintragen von c-3, a-1, b-2, C-03 ergibt list(backlog) {list(backlog)!r}, erwartet ['C-3', 'A-1', 'B-2']."
)

# Geschenkte Methoden: in, get, pop, setdefault
backlog = Backlog({"proj-7": 5}, WEB_3=8)
ergebnis = (
    "proj-7" in backlog,
    "Unsinn" in backlog,
    backlog.get("kein Ticket"),
    backlog.get("WEB-03", 0),
    backlog.pop("web-03"),
    backlog.setdefault("proj-0007", 99),
    backlog.setdefault("neu-1", 2),
)
assert ergebnis == (True, False, None, 8, 8, 5, 2) and dict(backlog.items()) == {"PROJ-7": 5, "NEU-1": 2}, (
    "in, in (ungültig), get, get mit Standardwert, pop, setdefault (vorhanden), setdefault (neu) ergeben "
    f"{ergebnis!r} mit Inhalt {dict(backlog.items())!r}; erwartet (True, False, None, 8, 8, 5, 2) und {{'PROJ-7': 5, 'NEU-1': 2}}."
)

# Vergleich mit einem gewöhnlichen Dictionary über die normalisierten Schlüssel
backlog = Backlog({"proj-7": 5})
assert backlog == {"PROJ-7": 5} and isinstance(backlog, MutableMapping), (
    "Backlog({'proj-7': 5}) == {'PROJ-7': 5} soll True sein, und der Backlog soll ein MutableMapping sein."
)

# Viele zufällige Operationen gegen ein gewöhnliches Dictionary
zufall = Zufall(5022)
schreibweisen = {}
for kuerzel in ["proj", "web", "ops"]:
    for nummer in range(1, 6):
        schreibweisen[f"{kuerzel.upper()}-{nummer}"] = [
            f"{kuerzel}-{nummer}", f"{kuerzel.upper()}-0{nummer}", f" {kuerzel.title()}-{nummer} ", f"{kuerzel}_{nummer}"
        ]
backlog = Backlog()
vergleich = {}
schritte = []
for _ in range(2000):
    richtig = zufall.choice(list(schreibweisen))
    text = zufall.choice(schreibweisen[richtig] + ["Unsinn", "x-", ""])
    gueltig = text not in ["Unsinn", "x-", ""]
    art = zufall.choice(["setzen", "lesen", "löschen", "in"])
    if art == "setzen":
        wert = zufall.randint(1, 13)
        schritte = (schritte + [f"backlog[{text!r}] = {wert}"])[-5:]
        _, fehler = versuche(backlog.__setitem__, text, wert)
        if gueltig:
            vergleich[richtig] = wert
        passt = isinstance(fehler, ValueError) != gueltig
    elif art == "lesen":
        schritte = (schritte + [f"backlog[{text!r}]"])[-5:]
        ergebnis, fehler = versuche(backlog.__getitem__, text)
        if gueltig and richtig in vergleich:
            passt = fehler is None and ergebnis == vergleich[richtig]
        else:
            passt = isinstance(fehler, KeyError)
    elif art == "löschen":
        schritte = (schritte + [f"del backlog[{text!r}]"])[-5:]
        _, fehler = versuche(backlog.__delitem__, text)
        if gueltig and richtig in vergleich:
            del vergleich[richtig]
            passt = fehler is None
        else:
            passt = isinstance(fehler, KeyError)
    else:
        schritte = (schritte + [f"{text!r} in backlog"])[-5:]
        ergebnis, fehler = versuche(backlog.__contains__, text)
        passt = ergebnis == (gueltig and richtig in vergleich)
    assert passt and dict(backlog.items()) == vergleich and list(backlog) == list(vergleich), (
        f"Nach {'; '.join(schritte)}: letzte Operation {'ok' if passt else 'falsch'} ({ausnahme_text(fehler)}), "
        f"Inhalt {dict(backlog.items())!r}, erwartet {vergleich!r}."
    )

# Obere Grenze: 100 000 Einträge, jeder Zugriff O(1)
backlog = Backlog((f"t-{nummer:06d}", nummer) for nummer in range(100000))
_, schritte_lesen = zaehle_schritte(backlog.__getitem__, "T-99999")
assert len(backlog) == 100000 and backlog["t-50000"] == 50000 and schritte_lesen <= 20, (
    f"Backlog mit 100 000 Einträgen: len {len(backlog)}, backlog['t-50000'] {backlog.get('t-50000')!r}, "
    f"ein Lesezugriff braucht {schritte_lesen} Schritte; erwartet 100000, 50000 und höchstens 20 Schritte (O(1))."
)
