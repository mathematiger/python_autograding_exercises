# Automatisch erzeugt aus lehrkraft/muster/2_059_displaysymbole.py - nicht von Hand ändern.
# vorlage-hash: 454cef9a8051c557
# text-hash: 028a586c9c2bb8cf
# thema: kontrollfluss
# inhalt: Dreieck und Raute aus Sternchen

def aufruf(funktion, zahl):
    """Ruft funktion(zahl) auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(zahl)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def ist_zeilenliste(ergebnis):
    """True, wenn ergebnis eine Liste ist, die nur Texte enthält."""
    if not isinstance(ergebnis, list):
        return False
    for zeile in ergebnis:
        if not isinstance(zeile, str):
            return False
    return True


def sternchen_je_zeile(zeilen):
    """Gibt für jede Zeile die Zahl ihrer Sternchen zurück."""
    anzahlen = []
    for zeile in zeilen:
        anzahlen.append(zeile.count("*"))
    return anzahlen


def leerzeichen_links(zeilen):
    """Gibt für jede Zeile die Zahl der Leerzeichen vor dem ersten anderen Zeichen zurück."""
    anzahlen = []
    for zeile in zeilen:
        anzahlen.append(len(zeile) - len(zeile.lstrip(" ")))
    return anzahlen


def bild(zeilen):
    """Zeigt Zeilen als eingerückte Figur, jede Zeile zwischen | und |, damit Leerzeichen sichtbar sind."""
    if not ist_zeilenliste(zeilen):
        return f"    {zeilen!r}"
    if not zeilen:
        return "    (leere Liste)"
    gezeigt = []
    for zeile in zeilen:
        gezeigt.append(f"    |{zeile}|")
    return "\n".join(gezeigt)


def kleines_bild(zeilen):
    """Zeigt das Bild nur bei höchstens 9 Zeilen, damit die Meldung kurz bleibt."""
    if ist_zeilenliste(zeilen) and len(zeilen) > 9:
        return f"    (Bild mit {len(zeilen)} Zeilen ausgelassen)"
    return bild(zeilen)


def vergleich_dreieck(hoehe):
    """Vergleichslösung: jede Zeile rechtsbündig auf die Breite hoehe + nummer gebracht."""
    zeilen = []
    for nummer in range(hoehe):
        sterne = "*" * (2 * nummer + 1)
        zeilen.append(f"{sterne:>{hoehe + nummer}}")
    return zeilen


def vergleich_raute(breite):
    """Vergleichslösung: jede Zeile in der Breite zentriert, Leerzeichen rechts abgeschnitten."""
    zeilen = []
    for nummer in range(breite):
        abstand = abs(nummer - breite // 2)
        sterne = "*" * (breite - 2 * abstand)
        zeilen.append(f"{sterne:^{breite}}".rstrip())
    return zeilen


def hinweis_zeilenende(ergebnis, erwartet):
    """Gibt einen Tipp zurück, wenn ergebnis nur durch Leerzeichen am Zeilenende falsch ist, sonst ""."""
    if not ist_zeilenliste(ergebnis) or ergebnis == erwartet:
        return ""
    gekuerzt = []
    for zeile in ergebnis:
        gekuerzt.append(zeile.rstrip())
    if gekuerzt != erwartet:
        return ""
    return "\nTipp: Am Zeilenende stehen Leerzeichen; die Zeile soll mit dem letzten Sternchen aufhören."


def meldung(aufruf_text, ergebnis, erwartet, hinweis=""):
    """Baut die Meldung mit erwartetem und erhaltenem Symbol."""
    tipp = hinweis_zeilenende(ergebnis, erwartet) or hinweis
    return f"{aufruf_text} ergibt:\n{bild(ergebnis)}\nerwartet war:\n{bild(erwartet)}{tipp}"


def kurze_meldung(aufruf_text, ergebnis, erwartet):
    """Meldung für große Symbole: nennt nur die erste falsche Zeile statt das ganze Bild."""
    if not ist_zeilenliste(ergebnis):
        return f"{aufruf_text} ergibt {ergebnis!r}; erwartet war eine Liste mit {len(erwartet)} Zeilen."
    if len(ergebnis) != len(erwartet):
        return f"{aufruf_text} hat {len(ergebnis)} Zeilen, erwartet waren {len(erwartet)}."
    nummer = 0
    while ergebnis[nummer] == erwartet[nummer]:
        nummer = nummer + 1
    return (
        f"{aufruf_text}: Zeile {nummer} ist {ergebnis[nummer]!r},\nerwartet war {erwartet[nummer]!r}."
        + hinweis_zeilenende(ergebnis, erwartet)
    )


def form_fehler(ergebnis, sternchen, links):
    """Prüft Zeilenzahl, Zeichen, Sternchen und Leerzeichen jeder Zeile; liefert eine Beschreibung oder None."""
    if not ist_zeilenliste(ergebnis):
        return "Das Ergebnis ist keine Liste von Texten."
    if len(ergebnis) != len(sternchen):
        return f"Das Symbol hat {len(ergebnis)} Zeilen, erwartet waren {len(sternchen)}."
    for nummer in range(len(sternchen)):
        zeile = ergebnis[nummer]
        if zeile != " " * links[nummer] + "*" * sternchen[nummer]:
            return (
                f"Zeile {nummer} ist {zeile!r}; erwartet waren {links[nummer]} Leerzeichen und dann "
                f"{sternchen[nummer]} Sternchen, sonst nichts."
            )
    return None


# dreieck(3) gibt eine Liste von Texten zurück
ergebnis = aufruf(dreieck, 3)
assert ist_zeilenliste(ergebnis), (
    f"dreieck(3) ergibt {ergebnis!r}; erwartet war eine Liste mit einem Text je Zeile.\n"
    "Tipp: Beginnen Sie mit zeilen = [], hängen Sie jede Zeile mit append an und geben Sie zeilen zurück."
)

# dreieck(3): 1, 3 und 5 Sternchen
ergebnis = aufruf(dreieck, 3)
anzahlen = sternchen_je_zeile(ergebnis) if ist_zeilenliste(ergebnis) else ergebnis
assert anzahlen == [1, 3, 5], (
    f"dreieck(3) hat {anzahlen} Sternchen in den Zeilen, erwartet waren [1, 3, 5].\n{bild(ergebnis)}\n"
    "Tipp: In Zeile nummer (ab 0) stehen 2 * nummer + 1 Sternchen."
)

# dreieck(3): Leerzeichen links rücken die Spitze in die Mitte
ergebnis = aufruf(dreieck, 3)
anzahlen = leerzeichen_links(ergebnis) if ist_zeilenliste(ergebnis) else ergebnis
assert anzahlen == [2, 1, 0], (
    f"dreieck(3) hat {anzahlen} Leerzeichen am Anfang der Zeilen, erwartet waren [2, 1, 0].\n{bild(ergebnis)}\n"
    "Tipp: Die unterste Zeile beginnt ganz links, jede Zeile darüber ein Leerzeichen weiter rechts."
)

# dreieck(3): genau die Zeilen, ohne Leerzeichen am Zeilenende
ergebnis = aufruf(dreieck, 3)
erwartet = ["  *", " ***", "*****"]
assert ergebnis == erwartet, meldung("dreieck(3)", ergebnis, erwartet)

# dreieck(5) (nicht fest hinschreiben!)
ergebnis = aufruf(dreieck, 5)
erwartet = ["    *", "   ***", "  *****", " *******", "*********"]
assert ergebnis == erwartet, meldung(
    "dreieck(5)", ergebnis, erwartet, "\nTipp: Die Zahl der Leerzeichen hängt von hoehe und von der Zeilennummer ab."
)

# dreieck(2)
ergebnis = aufruf(dreieck, 2)
erwartet = [" *", "***"]
assert ergebnis == erwartet, meldung("dreieck(2)", ergebnis, erwartet)

# dreieck(1): ein einziges Sternchen
ergebnis = aufruf(dreieck, 1)
erwartet = ["*"]
assert ergebnis == erwartet, meldung("dreieck(1)", ergebnis, erwartet)

# dreieck(0): ausgeschaltet, die leere Liste
ergebnis = aufruf(dreieck, 0)
assert ergebnis == [], meldung("dreieck(0)", ergebnis, [], "\nTipp: Bei hoehe 0 läuft die Schleife kein einziges Mal.")

# raute(5): 1, 3, 5, 3 und 1 Sternchen
ergebnis = aufruf(raute, 5)
anzahlen = sternchen_je_zeile(ergebnis) if ist_zeilenliste(ergebnis) else ergebnis
if isinstance(anzahlen, list) and anzahlen.count(5) > 1:
    hinweis = "\nTipp: Die breiteste Zeile kommt nur einmal vor; die untere Hälfte beginnt mit der Zeile darüber."
else:
    hinweis = "\nTipp: Bis zur Mitte wachsen die Zeilen um zwei Sternchen, danach nehmen sie ebenso wieder ab."
assert anzahlen == [1, 3, 5, 3, 1], (
    f"raute(5) hat {anzahlen} Sternchen in den Zeilen, erwartet waren [1, 3, 5, 3, 1].\n{bild(ergebnis)}{hinweis}"
)

# raute(5): genau die Zeilen mit den Leerzeichen links
ergebnis = aufruf(raute, 5)
erwartet = ["  *", " ***", "*****", " ***", "  *"]
assert ergebnis == erwartet, meldung("raute(5)", ergebnis, erwartet)

# raute(7) (nicht fest hinschreiben!)
ergebnis = aufruf(raute, 7)
erwartet = ["   *", "  ***", " *****", "*******", " *****", "  ***", "   *"]
assert ergebnis == erwartet, meldung("raute(7)", ergebnis, erwartet)

# raute(3)
ergebnis = aufruf(raute, 3)
erwartet = [" *", "***", " *"]
assert ergebnis == erwartet, meldung("raute(3)", ergebnis, erwartet)

# raute(1): ein einziges Sternchen
ergebnis = aufruf(raute, 1)
erwartet = ["*"]
assert ergebnis == erwartet, meldung("raute(1)", ergebnis, erwartet)

# Die Zeilen werden mit einer Schleife aufgebaut
assert verwendet("for") or verwendet("while"), "Bauen Sie die Zeilen mit einer for- oder while-Schleife auf."

zufall = Zufall(2059)

# dreieck: viele zufällige Höhen
for hoehe in sorted(zufall.sample(range(41), 20)):
    ergebnis = aufruf(dreieck, hoehe)
    sternchen = []
    links = []
    for nummer in range(hoehe):
        sternchen.append(2 * nummer + 1)
        links.append(hoehe - 1 - nummer)
    fehler = form_fehler(ergebnis, sternchen, links)
    assert fehler is None, f"dreieck({hoehe}): {fehler}\n{kleines_bild(ergebnis)}"

# raute: viele zufällige Breiten, oben und unten gleich
for breite in sorted(zufall.sample(range(1, 80, 2), 20)):
    ergebnis = aufruf(raute, breite)
    sternchen = []
    links = []
    for nummer in range(breite):
        abstand = abs(nummer - breite // 2)
        sternchen.append(breite - 2 * abstand)
        links.append(abstand)
    fehler = form_fehler(ergebnis, sternchen, links)
    if fehler is None and ergebnis != ergebnis[::-1]:
        fehler = "Die Raute ist nicht oben und unten gleich."
    assert fehler is None, f"raute({breite}): {fehler}\n{kleines_bild(ergebnis)}"

# Obere Grenze: dreieck(40) füllt die Anzeige fast ganz aus
ergebnis = aufruf(dreieck, 40)
erwartet = vergleich_dreieck(40)
assert ergebnis == erwartet, kurze_meldung("dreieck(40)", ergebnis, erwartet)

# Obere Grenze: raute(79)
ergebnis = aufruf(raute, 79)
erwartet = vergleich_raute(79)
assert ergebnis == erwartet, kurze_meldung("raute(79)", ergebnis, erwartet)
