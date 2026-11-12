# Automatisch erzeugt aus lehrkraft/muster/5_010_formularfelder.py - nicht von Hand ändern.
# vorlage-hash: 040008574c2dd39a
# text-hash: 8a17946a348f90b3
# thema: klassen
# inhalt: `__init_subclass__`

def ausnahme_bei(baue):
    """Führt baue() aus und gibt die ausgelöste Ausnahme zurück, oder None, wenn keine kam."""
    try:
        baue()
    except Exception as fehler:
        return fehler
    return None


def beschreibe(fehler):
    """Beschreibt eine Ausnahme oder ihr Fehlen für eine Meldung."""
    if fehler is None:
        return "es kam keine Ausnahme"
    return f"es kam {type(fehler).__name__}: {fehler}"


# Die drei vorgegebenen Feldtypen sind registriert
typen = getattr(Feld, "typen", None)
assert typen == {"text": Textfeld, "zahl": Zahlfeld, "email": Emailfeld}, (
    f"Feld.typen ist {typen!r}, erwartet war {{'text': Textfeld, 'zahl': Zahlfeld, 'email': Emailfeld}}.\n"
    "Tipp: Tragen Sie in __init_subclass__ die neue Klasse cls unter kuerzel in Feld.typen ein."
)

# Jede registrierte Klasse kennt ihr Kürzel
kuerzel = [getattr(klasse, "kuerzel", None) for klasse in (Textfeld, Zahlfeld, Emailfeld)]
assert kuerzel == ["text", "zahl", "email"], (
    f"Textfeld.kuerzel, Zahlfeld.kuerzel und Emailfeld.kuerzel sind {kuerzel}, erwartet war ['text', 'zahl', 'email'].\n"
    "Tipp: Setzen Sie cls.kuerzel = kuerzel, nicht Feld.kuerzel; dann hätten alle dasselbe."
)

# Eine neue Unterklasse registriert sich selbst
class Datumsfeld(Feld, kuerzel="datum"):
    beschriftung = "Datum"

    def pruefe(self, text):
        return None if text.count(".") == 2 else "Bitte geben Sie ein Datum wie 31.12.2026 ein."

assert Feld.typen.get("datum") is Datumsfeld and Datumsfeld.kuerzel == "datum", (
    f"Nach class Datumsfeld(Feld, kuerzel='datum') ist Feld.typen.get('datum') {Feld.typen.get('datum')!r} "
    f"und Datumsfeld.kuerzel {getattr(Datumsfeld, 'kuerzel', None)!r}; erwartet waren Datumsfeld und 'datum'."
)

# erzeuge liefert neue Objekte des passenden Typs
objekte = [Feld.erzeuge(name) for name in ["zahl", "email", "datum", "zahl"]]
arten = [type(objekt).__name__ for objekt in objekte]
assert arten == ["Zahlfeld", "Emailfeld", "Datumsfeld", "Zahlfeld"] and objekte[0] is not objekte[3], (
    f"Feld.erzeuge für 'zahl', 'email', 'datum', 'zahl' liefert Objekte der Klassen {arten}, "
    "erwartet waren Zahlfeld, Emailfeld, Datumsfeld und Zahlfeld, und bei jedem Aufruf ein neues Objekt."
)

# erzeuge mit unbekanntem Kürzel löst ValueError mit dem Kürzel aus
fehler = ausnahme_bei(lambda: Feld.erzeuge("farbe"))
assert isinstance(fehler, ValueError) and vergleichbar("farbe") in vergleichbar(str(fehler)), (
    f"Feld.erzeuge('farbe') muss einen ValueError auslösen, dessen Meldung 'farbe' enthält; {beschreibe(fehler)}."
)


# Ohne beschriftung: TypeError mit dem Klassennamen, nichts eingetragen
def ohne_beschriftung():
    """Definiert einen Feldtyp ohne beschriftung."""
    class Farbfeld(Feld, kuerzel="farbe"):
        def pruefe(self, text):
            return None

fehler = ausnahme_bei(ohne_beschriftung)
assert isinstance(fehler, TypeError) and vergleichbar("Farbfeld") in vergleichbar(str(fehler)) and "farbe" not in Feld.typen, (
    "class Farbfeld(Feld, kuerzel='farbe') ohne beschriftung muss einen TypeError mit 'Farbfeld' in der Meldung "
    f"auslösen und nichts eintragen; {beschreibe(fehler)}, 'farbe' in Feld.typen: {'farbe' in Feld.typen}.\n"
    "Tipp: getattr(cls, 'beschriftung', None) liefert None, wenn das Attribut fehlt; cls.__name__ ist der Klassenname."
)

# Beschriftung, die kein nicht leerer Text ist
for wert in ["", None, 42]:
    def falsche_beschriftung():
        """Definiert einen Feldtyp mit ungültiger beschriftung."""
        class Schieber(Feld, kuerzel="schieber"):
            beschriftung = wert

            def pruefe(self, text):
                return None

    fehler = ausnahme_bei(falsche_beschriftung)
    assert isinstance(fehler, TypeError) and vergleichbar("Schieber") in vergleichbar(str(fehler)) and "schieber" not in Feld.typen, (
        f"Ein Feldtyp Schieber mit beschriftung = {wert!r} muss einen TypeError mit 'Schieber' in der Meldung auslösen "
        f"und nichts eintragen; {beschreibe(fehler)}, 'schieber' in Feld.typen: {'schieber' in Feld.typen}.\n"
        "Tipp: Prüfen Sie mit isinstance(…, str) und auf den leeren Text, bevor Sie etwas eintragen."
    )


# Ohne eigene pruefe: TypeError mit dem Klassennamen
def ohne_pruefe():
    """Definiert einen Feldtyp, der pruefe von Feld erbt."""
    class Anzeige(Feld, kuerzel="anzeige"):
        beschriftung = "Nur Anzeige"

fehler = ausnahme_bei(ohne_pruefe)
assert isinstance(fehler, TypeError) and vergleichbar("Anzeige") in vergleichbar(str(fehler)) and "anzeige" not in Feld.typen, (
    "class Anzeige(Feld, kuerzel='anzeige') mit beschriftung, aber ohne pruefe, muss einen TypeError mit 'Anzeige' "
    f"in der Meldung auslösen und nichts eintragen; {beschreibe(fehler)}, 'anzeige' in Feld.typen: {'anzeige' in Feld.typen}.\n"
    "Tipp: cls.pruefe is Feld.pruefe ist True, wenn niemand pruefe überschrieben hat."
)

# Erst die Beschriftung prüfen, dann pruefe: ohne beides kommt der TypeError wegen der Beschriftung
def ohne_alles():
    """Definiert einen Feldtyp ganz ohne Inhalt."""
    class Leer(Feld, kuerzel="leer"):
        pass

fehler = ausnahme_bei(ohne_alles)
assert isinstance(fehler, TypeError) and vergleichbar("Leer") in vergleichbar(str(fehler)) and "leer" not in Feld.typen, (
    f"class Leer(Feld, kuerzel='leer'): pass muss einen TypeError mit 'Leer' in der Meldung auslösen und nichts "
    f"eintragen; {beschreibe(fehler)}, 'leer' in Feld.typen: {'leer' in Feld.typen}."
)


# Geerbte beschriftung und geerbte pruefe reichen
def kurztext():
    """Definiert einen Feldtyp, der beschriftung und pruefe von Textfeld erbt."""
    class Kurztext(Textfeld, kuerzel="kurz"):
        pass

fehler = ausnahme_bei(kurztext)
kurz = Feld.typen.get("kurz")
assert fehler is None and getattr(kurz, "__name__", None) == "Kurztext" and Feld.erzeuge("kurz").pruefe("") == "Bitte füllen Sie dieses Feld aus.", (
    "class Kurztext(Textfeld, kuerzel='kurz'): pass erbt beschriftung und pruefe von Textfeld und muss sich "
    f"ohne Fehler registrieren; {beschreibe(fehler)}, Feld.typen.get('kurz') ist {kurz!r}."
)

# Doppeltes Kürzel: ValueError mit dem Kürzel, der erste Eintrag bleibt
def doppelt():
    """Definiert einen zweiten Feldtyp mit dem Kürzel text."""
    class Langtext(Textfeld, kuerzel="text"):
        beschriftung = "Langer Text"

fehler = ausnahme_bei(doppelt)
assert isinstance(fehler, ValueError) and vergleichbar("text") in vergleichbar(str(fehler)) and Feld.typen["text"] is Textfeld, (
    "class Langtext(Textfeld, kuerzel='text') muss einen ValueError mit 'text' in der Meldung auslösen, "
    f"und Feld.typen['text'] bleibt Textfeld; {beschreibe(fehler)}, Feld.typen['text'] ist {Feld.typen['text']!r}."
)

# Doppeltes Kürzel bei sonst fehlerhafter Klasse: zuerst kommt der TypeError
def doppelt_und_leer():
    """Definiert einen Feldtyp mit vergebenem Kürzel und ohne Beschriftung."""
    class Ohne(Feld, kuerzel="zahl"):
        pass

fehler = ausnahme_bei(doppelt_und_leer)
assert isinstance(fehler, TypeError) and Feld.typen.get("zahl") is Zahlfeld, (
    f"class Ohne(Feld, kuerzel='zahl'): pass verstößt gegen zwei Regeln; erwartet war zuerst der TypeError wegen "
    f"der fehlenden Beschriftung, und Feld.typen['zahl'] bleibt Zahlfeld; {beschreibe(fehler)}, "
    f"Feld.typen['zahl'] ist {Feld.typen.get('zahl')!r}.\nTipp: Prüfen Sie in der Reihenfolge aus der Aufgabe."
)

# Ohne Kürzel: Zwischenstufe, keine Prüfung, kein Eintrag
anzahl_vorher = len(Feld.typen)

class Auswahlbasis(Feld):
    pass

class Ampel(Auswahlbasis, kuerzel="ampel"):
    beschriftung = "Ampel"

    def pruefe(self, text):
        return None if text in ("rot", "gelb", "gruen") else "Bitte wählen Sie rot, gelb oder gruen."

assert len(Feld.typen) == anzahl_vorher + 1 and Feld.typen.get("ampel") is Ampel and Auswahlbasis not in Feld.typen.values(), (
    "class Auswahlbasis(Feld) ohne Kürzel darf weder geprüft noch eingetragen werden, die Unterklasse Ampel mit "
    f"kuerzel='ampel' schon; Feld.typen enthält jetzt {sorted(Feld.typen)}."
)

# Weitere Schlüsselwörter gehen an die nächste Basisklasse weiter
gesehen = []

class Merker:
    def __init_subclass__(cls, gruppe="allgemein", **kwargs):
        super().__init_subclass__(**kwargs)
        gesehen.append((cls.__name__, gruppe))

class Farbwahl(Feld, Merker, kuerzel="farbwahl", gruppe="design"):
    beschriftung = "Farbe"

    def pruefe(self, text):
        return None

assert gesehen == [("Farbwahl", "design")] and Feld.typen.get("farbwahl") is Farbwahl, (
    "Bei class Farbwahl(Feld, Merker, kuerzel='farbwahl', gruppe='design') muss auch Merker.__init_subclass__ "
    f"mit gruppe='design' laufen; Merker hat {gesehen} gesehen, erwartet war [('Farbwahl', 'design')].\n"
    "Tipp: Rufen Sie super().__init_subclass__(**kwargs) auf und reichen Sie die übrigen Schlüsselwörter weiter."
)

# Ein Tippfehler im Schlüsselwort fällt auf
def tippfehler():
    """Definiert einen Feldtyp mit falsch geschriebenem Schlüsselwort."""
    class Telefon(Feld, kuerzl="telefon"):
        beschriftung = "Telefon"

        def pruefe(self, text):
            return None

fehler = ausnahme_bei(tippfehler)
assert isinstance(fehler, TypeError) and "telefon" not in Feld.typen, (
    f"class Telefon(Feld, kuerzl='telefon') (Tippfehler) muss einen TypeError auslösen; {beschreibe(fehler)}.\n"
    "Tipp: Reichen Sie **kwargs an super().__init_subclass__ weiter; object.__init_subclass__ lehnt unbekannte Schlüsselwörter ab."
)

# pruefe_formular aus dem Beispiel
ergebnis = pruefe_formular([("name", "text"), ("alter", "zahl"), ("kontakt", "email")], {"name": "Ada", "alter": "zwölf"})
erwartet = [("alter", "Bitte geben Sie eine ganze Zahl ein."), ("kontakt", "Bitte füllen Sie dieses Feld aus.")]
assert ergebnis == erwartet, (
    f"pruefe_formular(...) aus dem Beispiel ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
    "Tipp: Ein fehlender Eintrag in eingaben zählt als leerer Text: eingaben.get(name, '')."
)

# Leeres Formular, alles gültig, eigener Feldtyp
for felder, eingaben, erwartet in [
    ([], {}, []),
    ([], {"name": "x"}, []),
    ([("a", "text"), ("b", "zahl"), ("c", "email")], {"a": "x", "b": " 7 ", "c": "ada@firma.de"}, []),
    ([("start", "datum"), ("status", "ampel")], {"start": "1.2", "status": "blau"},
     [("start", "Bitte geben Sie ein Datum wie 31.12.2026 ein."), ("status", "Bitte wählen Sie rot, gelb oder gruen.")]),
    ([("z", "email"), ("y", "kurz")], {"z": "a@b@c", "y": "  "},
     [("z", "Bitte geben Sie eine gültige E-Mail-Adresse an."), ("y", "Bitte füllen Sie dieses Feld aus.")]),
]:
    ergebnis = pruefe_formular(felder, eingaben)
    assert ergebnis == erwartet, f"pruefe_formular({felder}, {eingaben}) ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"

# Unbekanntes Kürzel im Formular: ValueError
fehler = ausnahme_bei(lambda: pruefe_formular([("a", "text"), ("b", "schalter")], {"a": "x"}))
assert isinstance(fehler, ValueError) and vergleichbar("schalter") in vergleichbar(str(fehler)), (
    f"pruefe_formular mit dem unbekannten Feldtyp 'schalter' muss einen ValueError mit 'schalter' in der Meldung auslösen; {beschreibe(fehler)}."
)

# 300 zufällige Formulare, nachgerechnet mit den Klassen direkt
zufall = Zufall(5010)
KLASSEN = {"text": Textfeld, "zahl": Zahlfeld, "email": Emailfeld, "datum": Datumsfeld, "ampel": Ampel}
TEXTE = ["", " ", "Ada", "42", " 7 ", "-3", "a@b", "@b", "a@", "a@b@c", "1.2.2026", "rot", "blau"]
for _ in range(300):
    namen = zufall.sample(["name", "alter", "mail", "start", "status", "notiz"], zufall.randint(0, 6))
    felder = [(name, zufall.choice(sorted(KLASSEN))) for name in namen]
    eingaben = {name: zufall.choice(TEXTE) for name in namen if zufall.random() < 0.8}
    erwartet = []
    for name, kuerzel in felder:
        meldung = KLASSEN[kuerzel]().pruefe(eingaben.get(name, ""))
        if meldung is not None:
            erwartet.append((name, meldung))
    ergebnis = pruefe_formular(felder, eingaben)
    assert ergebnis == erwartet, f"pruefe_formular({felder}, {eingaben}) ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"

# An der oberen Grenze: 1000 Felder, jedes dritte ungültig
felder = [(f"feld{nummer}", ["text", "zahl", "email"][nummer % 3]) for nummer in range(1000)]
eingaben = {f"feld{nummer}": ("x" * 100 if nummer % 3 == 0 else "1" * 100) for nummer in range(1000)}
ergebnis = pruefe_formular(felder, eingaben)
assert len(ergebnis) == 333 and ergebnis[0][0] == "feld2" and ergebnis[-1][0] == "feld998", (
    f"Bei 1000 Feldern, von denen jedes dritte (die E-Mail-Felder) ungültig ist, liefert pruefe_formular {len(ergebnis)} "
    f"Meldungen, die erste für {ergebnis[0][0] if ergebnis else None!r}; erwartet waren 333, die erste für 'feld2'."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "['email', 'text', 'zahl']\nZahl\n"
    "[('alter', 'Bitte geben Sie eine ganze Zahl ein.'), ('kontakt', 'Bitte füllen Sie dieses Feld aus.')]"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
