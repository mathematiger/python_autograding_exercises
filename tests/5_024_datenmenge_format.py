# Automatisch erzeugt aus lehrkraft/muster/5_024_datenmenge_format.py - nicht von Hand ändern.
# vorlage-hash: 4afb3c719c9c2ae4
# text-hash: a969e00ead228387
# thema: klassen
# inhalt: __format__ mit eigener Spec

def formatiert(byte, spec):
    """Liefert format(Datenmenge(byte), spec) oder eine Beschreibung der Ausnahme."""
    try:
        return format(Datenmenge(byte), spec)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def ausnahme_bei(byte, spec):
    """Liefert die Ausnahme von format(Datenmenge(byte), spec) oder None, wenn keine kam."""
    try:
        format(Datenmenge(byte), spec)
    except Exception as fehler:
        return fehler
    return None


def erwartet_text(byte, spec):
    """Vergleichslösung: zerlegt die spec mit Indizes von hinten statt mit endswith; None heißt ungültig."""
    faktoren = {"B": 1, "kB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12}
    if spec == "":
        return f"{byte} B"
    einheit = None
    for laenge in (4, 2, 1):
        if spec[-laenge:] in list(faktoren) + ["auto"]:
            einheit = spec[-laenge:]
            break
    if einheit is None:
        return None
    vorne = spec[: len(spec) - len(einheit)]
    teile = vorne.split(".")
    if len(teile) > 2 or (teile[0] and not teile[0].isdigit()) or (len(teile) == 2 and not teile[1].isdigit()):
        return None
    if einheit == "auto":
        einheit = max([name for name in faktoren if faktoren[name] <= byte] or ["B"], key=lambda name: faktoren[name])
    stellen = int(teile[1]) if len(teile) == 2 else (0 if einheit == "B" else 1)
    text = format(byte / faktoren[einheit], f".{stellen}f") + " " + einheit
    return text.rjust(int(teile[0])) if teile[0] else text


def pruefe_genau(byte, spec, hinweis=""):
    """Baut die Meldung für einen Vergleich Zeichen für Zeichen."""
    return (
        f"format(Datenmenge({byte}), {spec!r}) ergibt {formatiert(byte, spec)!r}, erwartet war {erwartet_text(byte, spec)!r}.{hinweis}"
    )


# Leere spec: wie str(menge), auch in f"{menge}"
ergebnis = formatiert(1536000, "")
assert ergebnis == "1536000 B", (
    f'f"{{Datenmenge(1536000)}}" ergibt {ergebnis!r}, erwartet war "1536000 B".\n'
    'Tipp: Auch f"{menge}" ohne Doppelpunkt ruft __format__ auf, mit spec = "". Geben Sie dann str(self) zurück.'
)

# Eine feste Einheit: MB mit einer Nachkommastelle
assert formatiert(1536000, "MB") == "1.5 MB", pruefe_genau(
    1536000, "MB", "\nTipp: Teilen Sie durch 10**6 und formatieren Sie mit format(zahl, '.1f'); dann ' MB' anhängen."
)

# Die anderen Einheiten
for spec in ["kB", "GB", "TB"]:
    assert formatiert(1536000, spec) == erwartet_text(1536000, spec), pruefe_genau(1536000, spec)

# B ohne Nachkommastellen
assert formatiert(1536000, "B") == "1536000 B", pruefe_genau(
    1536000, "B", "\nTipp: Bei B ist die Standardzahl der Nachkommastellen 0, nicht 1."
)

# Andere Mengen (nicht fest hinschreiben!)
for byte, spec in [(2500, "kB"), (999, "B"), (7 * 10**12, "TB"), (123456789, "GB")]:
    assert formatiert(byte, spec) == erwartet_text(byte, spec), pruefe_genau(byte, spec)

# Nachkommastellen mit .stellen
for byte, spec in [(1536000, ".3MB"), (1536000, ".0MB"), (1536, ".2B"), (1, ".10kB")]:
    assert formatiert(byte, spec) == erwartet_text(byte, spec), pruefe_genau(
        byte, spec, "\nTipp: Die Ziffern nach dem Punkt sind die Nachkommastellen: format(zahl, f'.{stellen}f')."
    )

# auto wählt die größte passende Einheit
for byte in [1536000, 2500, 999, 0, 10**9, 10**15]:
    assert formatiert(byte, "auto") == erwartet_text(byte, "auto"), pruefe_genau(
        byte, "auto", "\nTipp: Nehmen Sie die größte Einheit, deren Faktor höchstens so groß ist wie self.byte."
    )

# auto an den Grenzen der Einheiten: 999 999 Byte bleiben kB, 10**6 Byte sind MB
for byte in [999999, 10**6, 1000, 10**12 - 1, 10**12]:
    assert formatiert(byte, "auto") == erwartet_text(byte, "auto"), pruefe_genau(
        byte, "auto", "\nTipp: Die Einheit hängt von der ungerundeten Byte-Zahl ab: faktor <= self.byte."
    )

# auto mit Nachkommastellen
for byte, spec in [(1536000, ".3auto"), (512, ".1auto")]:
    assert formatiert(byte, spec) == erwartet_text(byte, spec), pruefe_genau(byte, spec)

# breite richtet rechtsbündig aus
for byte, spec in [(1536000, "10MB"), (1536000, "10.2GB"), (5, "6B")]:
    assert formatiert(byte, spec) == erwartet_text(byte, spec), pruefe_genau(
        byte, spec, "\nTipp: Die Ziffern vor dem Punkt sind die Breite des ganzen Textes samt Einheit: text.rjust(breite)."
    )

# breite kürzer als der Text und breite 0 lassen ihn unverändert
for byte, spec in [(1536000, "3MB"), (1536000, "0kB"), (10**15, "40.10auto")]:
    assert formatiert(byte, spec) == erwartet_text(byte, spec), pruefe_genau(byte, spec)

# Breite in einer Tabelle mit f-String
try:
    zeilen = [f"{name:<6}|{Datenmenge(byte):9auto}|" for name, byte in [("web1", 1536000), ("db", 42), ("backup", 3 * 10**12)]]
except Exception as fehler:
    zeilen = [f"{type(fehler).__name__}: {fehler}"]
assert zeilen == ["web1  |   1.5 MB|", "db    |     42 B|", "backup|   3.0 TB|"], (
    f"Tabelle mit {{menge:9auto}} ergibt {zeilen!r}, erwartet war ['web1  |   1.5 MB|', 'db    |     42 B|', 'backup|   3.0 TB|']."
)

# Unbekannte Einheit löst ValueError aus, mit der spec in der Meldung
fehler = ausnahme_bei(1536000, "MiB")
assert isinstance(fehler, ValueError) and "MiB" in str(fehler), (
    f"format(Datenmenge(1536000), 'MiB') soll einen ValueError auslösen, dessen Meldung 'MiB' enthält; bekommen: {fehler!r}.\n"
    "Tipp: Was Ihre Formatsprache nicht kennt, beenden Sie mit raise ValueError(f'Unbekannte Formatangabe {spec!r}')."
)

# Groß- und Kleinschreibung der Einheit zählt
for spec in ["mb", "kb", "KB", "Auto", "b"]:
    fehler = ausnahme_bei(1536000, spec)
    assert isinstance(fehler, ValueError) and spec in str(fehler), (
        f"format(Datenmenge(1536000), {spec!r}) soll einen ValueError auslösen, dessen Meldung {spec!r} enthält; "
        f"bekommen: {fehler!r} (Ergebnis {formatiert(1536000, spec)!r})."
    )

# Kaputte Breite oder Stellen lösen ValueError aus
for spec in [">10MB", "MB10", "1.2.3MB", ".MB", "M B", "x", "+5MB", "-3kB", " 5MB", "5.B "]:
    fehler = ausnahme_bei(1536000, spec)
    assert isinstance(fehler, ValueError) and spec in str(fehler), (
        f"format(Datenmenge(1536000), {spec!r}) soll einen ValueError auslösen, dessen Meldung {spec!r} enthält; "
        f"bekommen: {fehler!r} (Ergebnis {formatiert(1536000, spec)!r}).\n"
        "Tipp: Vor der Einheit sind nur Ziffern erlaubt, dann höchstens ein Punkt mit mindestens einer Ziffer dahinter."
    )

# __format__ gibt einen Text zurück, gibt nichts aus
ergebnis = Datenmenge(2000).__format__("kB")
assert type(ergebnis) is str, (
    f"Datenmenge(2000).__format__('kB') ergibt {ergebnis!r}; erwartet war ein Text. Geben Sie ihn mit return zurück, nicht mit print."
)

# Viele zufällige Mengen und Formatangaben
zufall = Zufall(5024)
for runde in range(1500):
    byte = zufall.choice([zufall.randint(0, 2000), zufall.randint(0, 10**7), zufall.randint(0, 10**15), 10 ** zufall.randint(0, 15)])
    breite = zufall.choice(["", str(zufall.randint(0, 40))])
    stellen = zufall.choice(["", "." + str(zufall.randint(0, 10))])
    einheit = zufall.choice(["B", "kB", "MB", "GB", "TB", "auto", "auto", "Mb", "KiB", ""])
    spec = zufall.choice([breite + stellen + einheit, breite + stellen + einheit, zufall.choice(["..MB", "1.MB", "MB.", "a" + einheit])])
    erwartet = erwartet_text(byte, spec)
    if erwartet is None:
        fehler = ausnahme_bei(byte, spec)
        assert isinstance(fehler, ValueError), (
            f"format(Datenmenge({byte}), {spec!r}) soll einen ValueError auslösen; bekommen: {fehler!r} (Ergebnis {formatiert(byte, spec)!r})."
        )
    else:
        assert formatiert(byte, spec) == erwartet, pruefe_genau(byte, spec)

# Die Ausgabe des Programms stimmt
assert AUSGABE == "1536000 B | 1.5 MB | 1.536 MB | 1.5 MB", (
    f'Erwartete Ausgabe: "1536000 B | 1.5 MB | 1.536 MB | 1.5 MB" – Ihr Programm: "{AUSGABE}"'
)
