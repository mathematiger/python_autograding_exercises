# Automatisch erzeugt aus lehrkraft/muster/2_034_portfreigaben.py - nicht von Hand ändern.
# vorlage-hash: 8f73c2c4eec9e5d9
# text-hash: 4e876d0404ae933d
# thema: fehler
# inhalt: try/except in einer Schleife

def rufe_auf(eintraege):
    """Ruft gueltige_ports mit einer Kopie von eintraege auf; liefert Ergebnis und Ausnahme (sonst None)."""
    try:
        return gueltige_ports(list(eintraege)), None
    except Exception as ausnahme:
        return None, ausnahme


def meldung(eintraege, ergebnis, fehler, erwartet):
    """Baut die Fehlermeldung; nennt eine aufgetretene Ausnahme mit Tipp."""
    if fehler is not None:
        return (
            f"gueltige_ports({eintraege!r}) ist mit {type(fehler).__name__} abgestürzt, erwartet war {erwartet!r}.\n"
            "Tipp: Wandeln Sie jeden Eintrag in einem try-Block um und fangen Sie den ValueError mit "
            "except ValueError: ab."
        )
    return f"gueltige_ports({eintraege!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."


def von_hand(eintraege):
    """Vergleichslösung ohne try: prüft jedes Zeichen selbst."""
    ergebnis = []
    for eintrag in eintraege:
        ziffern = eintrag.strip()
        if ziffern.startswith("-"):
            continue
        if ziffern == "" or not all(zeichen in "0123456789" for zeichen in ziffern):
            continue
        if 1 <= int(ziffern) <= 65535:
            ergebnis.append(int(ziffern))
    return ergebnis


# Das Beispiel aus der Aufgabe
eintraege = ["443", "https", " 22 ", "70000", "", "8080"]
ergebnis, fehler = rufe_auf(eintraege)
assert fehler is None and ergebnis == [443, 22, 8080], meldung(eintraege, ergebnis, fehler, [443, 22, 8080])

# Andere Ports (nicht fest hinschreiben!)
for eintraege, erwartet in [(["22"], [22]), (["80", "25", "3389"], [80, 25, 3389]), (["5432", "x", "53"], [5432, 53])]:
    ergebnis, fehler = rufe_auf(eintraege)
    assert fehler is None and ergebnis == erwartet, meldung(eintraege, ergebnis, fehler, erwartet)

# Ohne Einträge ist das Ergebnis leer
ergebnis, fehler = rufe_auf([])
assert fehler is None and ergebnis == [], meldung([], ergebnis, fehler, [])

# Ein kaputter Eintrag bricht die Schleife nicht ab: Die Einträge danach zählen auch
eintraege = ["https", "443", "8080/tcp", "22", "", "53"]
ergebnis, fehler = rufe_auf(eintraege)
assert fehler is None and ergebnis == [443, 22, 53], (
    meldung(eintraege, ergebnis, fehler, [443, 22, 53])
    + "\nTipp: Überspringen Sie nur den kaputten Eintrag (continue), nicht den Rest der Liste (break oder return)."
)

# Unbrauchbare Einträge, die int nicht umwandeln kann
eintraege = ["https", "", "   ", "8080/tcp", "4.43", "1,5", "22:", "ssh", "--", "4-4"]
ergebnis, fehler = rufe_auf(eintraege)
assert fehler is None and ergebnis == [], meldung(eintraege, ergebnis, fehler, [])

# Leerzeichen am Rand stören nicht
eintraege = [" 22 ", "  443", "8080   "]
ergebnis, fehler = rufe_auf(eintraege)
assert fehler is None and ergebnis == [22, 443, 8080], (
    meldung(eintraege, ergebnis, fehler, [22, 443, 8080])
    + "\nTipp: int(' 22 ') ergibt 22. Prüfen Sie den Text nicht vorher mit isdigit(), sondern probieren Sie int(...)."
)

# Die Grenzen 1 und 65535 gehören dazu
eintraege = ["1", "65535"]
ergebnis, fehler = rufe_auf(eintraege)
assert fehler is None and ergebnis == [1, 65535], (
    meldung(eintraege, ergebnis, fehler, [1, 65535])
    + "\nTipp: Ein Port reicht von 1 bis 65535, beide Grenzen eingeschlossen: 1 <= port <= 65535."
)

# 0, 65536 und negative Zahlen sind keine Ports
eintraege = ["0", "65536", "-1", "-443", "99999"]
ergebnis, fehler = rufe_auf(eintraege)
assert fehler is None and ergebnis == [], (
    meldung(eintraege, ergebnis, fehler, [])
    + "\nTipp: Ein Port reicht von 1 bis 65535, beide Grenzen eingeschlossen: 1 <= port <= 65535."
)

# Doppelte Ports bleiben erhalten, die Reihenfolge auch
eintraege = ["443", "22", "443", "x", "22"]
ergebnis, fehler = rufe_auf(eintraege)
assert fehler is None and ergebnis == [443, 22, 443, 22], (
    meldung(eintraege, ergebnis, fehler, [443, 22, 443, 22])
    + "\nTipp: Prüfen Sie nicht, ob ein Port schon in der Liste steht; doppelte Anträge prüft ein späterer Schritt."
)

# Das Ergebnis sind ganze Zahlen, keine Texte
ergebnis, fehler = rufe_auf(["443", " 22"])
assert fehler is None and ergebnis == [443, 22] and all(type(port) is int for port in ergebnis), (
    meldung(["443", " 22"], ergebnis, fehler, [443, 22])
    + "\nTipp: Hängen Sie die umgewandelte Zahl an, nicht den ursprünglichen Text."
)

# Die übergebene Liste bleibt unverändert
eintraege = ["443", "https", "70000", "22"]
gueltige_ports(eintraege)
assert eintraege == ["443", "https", "70000", "22"], (
    f"Nach dem Aufruf ist die Liste {eintraege!r}, sie soll unverändert ['443', 'https', '70000', '22'] bleiben.\n"
    "Tipp: Sammeln Sie die Ports in einer neuen Liste, statt Einträge aus der übergebenen zu entfernen."
)

# Es wird mit try und except gearbeitet
assert verwendet("try"), "Wandeln Sie jeden Eintrag in einem try-Block mit int(...) um und fangen Sie den ValueError ab."


# Ein int, das keinen Text umwandeln kann: So zeigt sich, ob der Fehlschlag wirklich abgefangen wird
def scheiterndes_int(text):
    """Tut so, als könne int den Text nicht umwandeln."""
    raise ValueError(f"invalid literal for int() with base 10: {text!r}")


# Scheitert int(...), fängt die Funktion den ValueError ab und überspringt den Eintrag
try:
    int = scheiterndes_int
    ergebnis, fehler = rufe_auf(["443", "22"])
finally:
    del int
assert fehler is None and ergebnis == [], (
    "Für diesen Test scheitert int(...) bei jedem Text mit ValueError.\n"
    + meldung(["443", "22"], ergebnis, fehler, [])
    + "\nTipp: Prüfen Sie den Text nicht vorher selbst, sondern probieren Sie int(eintrag) in einem try-Block aus "
    "und überspringen Sie den Eintrag im except-Block."
)


# Ein int mit einem ganz anderen Fehler: Der soll nicht verschluckt werden
def kaputtes_int(text):
    """Tut so, als hätte das Programm einen Fehler, der mit dem Text nichts zu tun hat."""
    raise TypeError("ein anderer Fehler")


# Nur der ValueError wird abgefangen, andere Fehler werden weitergemeldet
try:
    int = kaputtes_int
    ergebnis, fehler = rufe_auf(["443"])
finally:
    del int
assert isinstance(fehler, TypeError), (
    f"Wenn in int(...) ein TypeError auftritt, ergibt gueltige_ports(['443']) {ergebnis!r}; erwartet war, dass "
    "der TypeError weitergemeldet wird.\n"
    "Tipp: Schreiben Sie except ValueError: statt nur except: oder except Exception:, damit Sie nur den "
    "Fehler abfangen, mit dem Sie rechnen."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("[443, 22, 8080]"), f"Erwartete Ausgabe:\n[443, 22, 8080]\nIhr Programm gibt aus:\n{AUSGABE}"

# 300 zufällige Anträge, brauchbare und kaputte Einträge gemischt
zufall = Zufall(2034)
kaputte = ["", "https", "ssh", "8080/tcp", "4.43", "1,5", "22:", "--", "-", "x", "  ", "rdp 3389"]
for _ in range(300):
    eintraege = []
    for _ in range(zufall.randint(0, 8)):
        wahl = zufall.random()
        if wahl < 0.3:
            eintrag = zufall.choice(kaputte)
        elif wahl < 0.5:
            eintrag = str(zufall.choice([0, -1, 65536, 70000, 99999, -zufall.randint(1, 65535)]))
        else:
            eintrag = str(zufall.randint(1, 65535))
        eintraege.append(" " * zufall.randint(0, 2) + eintrag + " " * zufall.randint(0, 2))
    ergebnis, fehler = rufe_auf(eintraege)
    erwartet = von_hand(eintraege)
    assert fehler is None and ergebnis == erwartet, meldung(eintraege, ergebnis, fehler, erwartet)

# An der oberen Grenze: 10 000 Einträge mit 20 Zeichen
eintraege = []
for nummer in range(10000):
    if nummer % 3 == 0:
        eintraege.append("x" * 20)
    else:
        eintraege.append(str(nummer * 7 % 70000).rjust(20))
ergebnis, fehler = rufe_auf(eintraege)
erwartet = von_hand(eintraege)
assert fehler is None and ergebnis == erwartet, (
    f"Bei 10 000 Einträgen liefert gueltige_ports {len(ergebnis) if ergebnis is not None else ergebnis} Ports, "
    f"erwartet waren {len(erwartet)}."
    + ("" if fehler is None else f"\nDie Funktion ist mit {type(fehler).__name__} abgestürzt.")
    + ("\nTipp: Hängen Sie die Zahl int(eintrag) an, nicht den Text." if fehler is None and ergebnis and isinstance(ergebnis[0], str) else "")
)
