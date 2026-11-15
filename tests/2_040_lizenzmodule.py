# Automatisch erzeugt aus lehrkraft/muster/2_040_lizenzmodule.py - nicht von Hand ändern.
# vorlage-hash: 1b466339d7a22809
# text-hash: 9656dfd0fe4924d9
# thema: algorithmen
# inhalt: Binärdarstellung von Hand

def vergleich_binaer(zahl):
    """Vergleichslösung, die die Stellenwerte von oben nach unten abzieht."""
    if zahl == 0:
        return "0"
    wert = 1
    while wert * 2 <= zahl:
        wert = wert * 2
    text = ""
    while wert >= 1:
        if zahl >= wert:
            text = text + "1"
            zahl = zahl - wert
        else:
            text = text + "0"
        wert = wert // 2
    return text


def pruefe_binaer(zahl):
    """Vergleicht binaer(zahl) mit der Vergleichslösung und gibt (stimmt, Meldung) zurück."""
    ergebnis = binaer(zahl)
    erwartet = vergleich_binaer(zahl)
    text = f'binaer({zahl}) ergibt {ergebnis!r}, erwartet war "{erwartet}".'
    if isinstance(ergebnis, str) and ergebnis == erwartet[::-1] and erwartet != erwartet[::-1]:
        text += "\nTipp: Die Ziffern stehen verkehrt herum. Setzen Sie jede neue Ziffer vorn an: text = str(rest) + text."
    elif isinstance(ergebnis, int):
        text += "\nTipp: binaer soll einen Text zurückgeben, zum Beispiel \"1101\", keine Zahl."
    elif ergebnis == "" and zahl == 0:
        text += '\nTipp: Bei 0 läuft die while-Schleife gar nicht; die Binärdarstellung von 0 ist aber "0".'
    return ergebnis == erwartet, text


def pruefe_anzahl(zahl):
    """Vergleicht anzahl_module(zahl) mit der Vergleichslösung und gibt (stimmt, Meldung) zurück."""
    ergebnis = anzahl_module(zahl)
    erwartet = vergleich_binaer(zahl).count("1")
    text = f"anzahl_module({zahl}) ergibt {ergebnis!r}, erwartet war {erwartet} (binär {vergleich_binaer(zahl)})."
    return ergebnis == erwartet, text


# Das Beispiel: binaer(13) enthält drei Einsen und eine Null (Reihenfolge zählt hier noch nicht)
ergebnis = binaer(13)
assert isinstance(ergebnis, str) and sorted(ergebnis) == ["0", "1", "1", "1"], (
    f'binaer(13) ergibt {ergebnis!r}, erwartet war ein Text aus den Ziffern 1, 1, 0 und 1.\n'
    "Tipp: zahl % 2 ist die letzte Binärziffer, zahl // 2 schneidet sie ab; wiederholen Sie das, bis zahl 0 ist."
)

# Das Beispiel: binaer(13) ist "1101"
stimmt, text = pruefe_binaer(13)
assert stimmt, text

# Andere Zahlen (nicht fest hinschreiben!)
for zahl in [1, 2, 5, 6, 100]:
    stimmt, text = pruefe_binaer(zahl)
    assert stimmt, text

# Zweierpotenzen: eine 1 und lauter Nullen
for zahl in [8, 64, 1024]:
    stimmt, text = pruefe_binaer(zahl)
    assert stimmt, text

# Die Zahl 0
stimmt, text = pruefe_binaer(0)
assert stimmt, text

# Das Beispiel: anzahl_module(13) ist 3
stimmt, text = pruefe_anzahl(13)
assert stimmt, text

# anzahl_module für andere Zahlen
for zahl in [1, 8, 255, 1000]:
    stimmt, text = pruefe_anzahl(zahl)
    assert stimmt, text

# anzahl_module(0) ist 0: kein Modul gebucht
stimmt, text = pruefe_anzahl(0)
assert stimmt, text

# Ohne die fertigen Werkzeuge
assert not verwendet("bin") and not verwendet("format"), (
    "Ihr Code benutzt bin(...) oder format(...). Rechnen Sie die Binärziffern selbst mit // 2 und % 2 aus."
)

# Viele zufällige Lizenzen
zufall = Zufall(2040)
for _ in range(500):
    zahl = zufall.choice([zufall.randint(0, 64), zufall.randint(0, 2**20), zufall.randint(0, 2**64)])
    stimmt, text = pruefe_binaer(zahl)
    assert stimmt, text
    stimmt, text = pruefe_anzahl(zahl)
    assert stimmt, text

# Obere Grenze: 2**64 und 2**64 - 1 (alle 64 Module gebucht)
for zahl in [2**64, 2**64 - 1]:
    stimmt, text = pruefe_binaer(zahl)
    assert stimmt, text
    stimmt, text = pruefe_anzahl(zahl)
    assert stimmt, text
