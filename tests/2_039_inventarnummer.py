# Automatisch erzeugt aus lehrkraft/muster/2_039_inventarnummer.py - nicht von Hand ändern.
# vorlage-hash: 2368df1a2dbaacc0
# text-hash: 93ce3b90a52b94ae
# thema: algorithmen
# inhalt: Ziffern mit // und %

def vergleich_ziffern(nummer):
    """Langsame Vergleichslösung über den Text der Zahl."""
    return [int(zeichen) for zeichen in f"{nummer}"]


def hinweis_ziffern(ergebnis, nummer):
    """Gibt einen Tipp zu häufigen Fehlern bei ziffern, sonst einen leeren Text."""
    richtig = vergleich_ziffern(nummer)
    if ergebnis is None:
        return "\nTipp: Ihre Funktion gibt nichts zurück; fehlt das return?"
    if isinstance(ergebnis, tuple):
        return "\nTipp: Geben Sie eine Liste zurück (eckige Klammern), kein Tupel."
    if isinstance(ergebnis, list) and ergebnis == richtig[::-1] and richtig != richtig[::-1]:
        return "\nTipp: Die Ziffern stehen verkehrt herum. Fügen Sie vorn an (insert(0, …)) oder drehen Sie die Liste am Ende um."
    if ergebnis == [] and nummer == 0:
        return "\nTipp: Bei 0 läuft die while-Schleife gar nicht; die Zahl 0 hat aber eine Ziffer, nämlich 0."
    return ""


def pruefe_ziffern(nummer):
    """Vergleicht ziffern(nummer) mit der Vergleichslösung und gibt (stimmt, Meldung) zurück."""
    ergebnis = ziffern(nummer)
    erwartet = vergleich_ziffern(nummer)
    text = f"ziffern({nummer}) ergibt {ergebnis!r}, erwartet war {erwartet}.{hinweis_ziffern(ergebnis, nummer)}"
    return ergebnis == erwartet, text


def pruefe_pruefziffer(nummer):
    """Vergleicht pruefziffer(nummer) mit der Vergleichslösung und gibt (stimmt, Meldung) zurück."""
    ergebnis = pruefziffer(nummer)
    quersumme = sum(vergleich_ziffern(nummer))
    erwartet = quersumme % 10
    text = f"pruefziffer({nummer}) ergibt {ergebnis!r}, erwartet war {erwartet} (Quersumme {quersumme})."
    if ergebnis == quersumme and quersumme != erwartet:
        text += "\nTipp: Gefragt ist nur die letzte Stelle der Quersumme: quersumme % 10."
    return ergebnis == erwartet, text


# Das Beispiel: ziffern(40715) enthält die richtigen Ziffern (Reihenfolge zählt hier noch nicht)
ergebnis = ziffern(40715)
if ergebnis is None:
    hinweis = hinweis_ziffern(ergebnis, 40715)
else:
    hinweis = "\nTipp: nummer % 10 ist die letzte Ziffer, nummer // 10 schneidet sie ab; wiederholen Sie das, bis nummer 0 ist."
assert isinstance(ergebnis, (list, tuple)) and sorted(ergebnis) == [0, 1, 4, 5, 7], (
    f"ziffern(40715) ergibt {ergebnis!r}, erwartet waren die Ziffern 4, 0, 7, 1 und 5.{hinweis}"
)

# Das Beispiel: ziffern(40715) in der richtigen Reihenfolge
stimmt, text = pruefe_ziffern(40715)
assert stimmt, text

# Andere Nummern (nicht fest hinschreiben!)
for nummer in [9, 12, 3008, 987654321]:
    stimmt, text = pruefe_ziffern(nummer)
    assert stimmt, text

# Nullen am Ende und in der Mitte bleiben erhalten
for nummer in [10, 1000, 20304]:
    stimmt, text = pruefe_ziffern(nummer)
    assert stimmt, text

# Die Nummer 0 hat eine Ziffer
stimmt, text = pruefe_ziffern(0)
assert stimmt, text

# Das Beispiel: pruefziffer(40715) ist 7
stimmt, text = pruefe_pruefziffer(40715)
assert stimmt, text

# pruefziffer für andere Nummern, auch mit Quersumme unter 10 und genau 10
for nummer in [12, 55, 19, 99999]:
    stimmt, text = pruefe_pruefziffer(nummer)
    assert stimmt, text

# pruefziffer(0) ist 0
stimmt, text = pruefe_pruefziffer(0)
assert stimmt, text

# Ohne Umweg über einen Text
assert not verwendet("str") and not verwendet("repr"), (
    "Ihr Code wandelt die Zahl in einen Text um. Rechnen Sie stattdessen mit // 10 und % 10."
)

# Viele zufällige Nummern
zufall = Zufall(2039)
for _ in range(500):
    nummer = zufall.choice([zufall.randint(0, 999), zufall.randint(0, 10**9), zufall.randint(0, 10**18)])
    stimmt, text = pruefe_ziffern(nummer)
    assert stimmt, text
    stimmt, text = pruefe_pruefziffer(nummer)
    assert stimmt, text

# Obere Grenze: 10**18 und 10**18 - 1
for nummer in [10**18, 10**18 - 1]:
    stimmt, text = pruefe_ziffern(nummer)
    assert stimmt, text
    stimmt, text = pruefe_pruefziffer(nummer)
    assert stimmt, text
