# Automatisch erzeugt aus lehrkraft/muster/2_035_schrittdauer.py - nicht von Hand ändern.
# vorlage-hash: 5b2f578c02d6f32b
# text-hash: e6a9adebe1a97e61
# thema: fehler
# inhalt: Mehrere Ausnahmen in einem except

def rufe_auf(zeile):
    """Ruft dauer(zeile) auf und liefert das Ergebnis und eine aufgetretene Ausnahme (sonst None)."""
    try:
        return dauer(zeile), None
    except Exception as ausnahme:
        return None, ausnahme


def meldung(zeile, ergebnis, fehler, erwartet):
    """Baut die Fehlermeldung; nennt eine aufgetretene Ausnahme mit einem passenden Tipp."""
    if isinstance(fehler, IndexError):
        return (
            f"dauer({zeile!r}) ist mit IndexError abgestürzt, erwartet war {erwartet!r}.\n"
            "Tipp: Ohne Semikolon hat die Liste von split nur ein Element, teile[1] gibt es dann nicht. "
            "Fangen Sie auch den IndexError ab: except (IndexError, ValueError):"
        )
    if fehler is not None:
        return (
            f"dauer({zeile!r}) ist mit {type(fehler).__name__} abgestürzt, erwartet war {erwartet!r}.\n"
            "Tipp: Wandeln Sie das zweite Feld in einem try-Block um und fangen Sie den Fehler mit "
            "except (IndexError, ValueError): ab."
        )
    return f"dauer({zeile!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."


def von_hand(zeile):
    """Vergleichslösung ohne try: prüft Feldzahl und Ziffern selbst."""
    teile = zeile.split(";")
    if len(teile) < 2:
        return -1
    feld = teile[1].strip()
    if feld == "" or not all(zeichen in "0123456789" for zeichen in feld.removeprefix("-")):
        return -1
    if feld.removeprefix("-") == "":
        return -1
    return int(feld)


# Das Beispiel aus der Aufgabe: "Angebot prüfen;45" ergibt 45
ergebnis, fehler = rufe_auf("Angebot prüfen;45")
assert fehler is None and ergebnis == 45, meldung("Angebot prüfen;45", ergebnis, fehler, 45)

# Andere Zeilen (nicht fest hinschreiben!)
for zeile, erwartet in [("Test;30", 30), ("Abnahme;7", 7), ("Rechnung schreiben;1500", 1500), ("Kickoff;0", 0)]:
    ergebnis, fehler = rufe_auf(zeile)
    assert fehler is None and ergebnis == erwartet, meldung(zeile, ergebnis, fehler, erwartet)

# Ein Kommentar hinter der Dauer stört nicht
for zeile, erwartet in [("Freigabe;120;Rückfrage beim Kunden", 120), ("Test;15;", 15), ("Test;5;a;b;c", 5)]:
    ergebnis, fehler = rufe_auf(zeile)
    hinweis = ""
    if ergebnis == -1:
        hinweis = "\nTipp: Die Dauer ist immer das zweite Feld, teile[1]; weitere Felder werden nicht beachtet."
    assert fehler is None and ergebnis == erwartet, meldung(zeile, ergebnis, fehler, erwartet) + hinweis

# Leerzeichen um die Zahl stören nicht
for zeile, erwartet in [("Test; 30 ", 30), ("Test;   8", 8), ("Test;12  ;Kommentar", 12)]:
    ergebnis, fehler = rufe_auf(zeile)
    assert fehler is None and ergebnis == erwartet, meldung(zeile, ergebnis, fehler, erwartet)

# Fehlt das zweite Feld, ergibt sich -1 statt eines IndexError
for zeile in ["Freigabe", "", "Angebot prüfen 45", "   "]:
    ergebnis, fehler = rufe_auf(zeile)
    assert fehler is None and ergebnis == -1, meldung(zeile, ergebnis, fehler, -1)

# Lässt sich das zweite Feld nicht umwandeln, ergibt sich -1 statt eines ValueError
for zeile in ["Freigabe;zwei Stunden", "Freigabe;", "Test;4.5", "Test;1,5;Kommentar", "Test; ", ";", ";;45", "Test;-"]:
    ergebnis, fehler = rufe_auf(zeile)
    assert fehler is None and ergebnis == -1, meldung(zeile, ergebnis, fehler, -1)

# Das Ergebnis ist eine ganze Zahl, kein Text
ergebnis, fehler = rufe_auf("Test;30")
assert fehler is None and type(ergebnis) is int, (
    f"dauer('Test;30') ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war die ganze Zahl 30.\n"
    "Tipp: Wandeln Sie das Feld mit int(...) um."
)

# Es wird mit try und except gearbeitet
assert verwendet("try"), "Wandeln Sie das zweite Feld in einem try-Block um und fangen Sie die Fehler mit except ab."


# Ein int mit einem ganz anderen Fehler: Der soll nicht verschluckt werden
def kaputtes_int(text):
    """Tut so, als hätte das Programm einen Fehler, der mit der Zeile nichts zu tun hat."""
    raise TypeError("ein anderer Fehler")


# Nur IndexError und ValueError werden abgefangen, andere Fehler werden weitergemeldet
try:
    int = kaputtes_int
    ergebnis, fehler = rufe_auf("Test;30")
finally:
    del int
assert isinstance(fehler, TypeError), (
    f"Wenn in int(...) ein TypeError auftritt, ergibt dauer('Test;30') {ergebnis!r}; erwartet war, dass der "
    "TypeError weitergemeldet wird.\n"
    "Tipp: Schreiben Sie except (IndexError, ValueError): statt nur except: oder except Exception:, damit Sie "
    "nur die Fehler abfangen, mit denen Sie rechnen."
)

# Die Ausgabe des Programms stimmt
assert AUSGABE == "45\n-1", f"Erwartete Ausgabe:\n45\n-1\nIhr Programm gibt aus:\n{AUSGABE}"

# 500 zufällige Protokollzeilen, brauchbare und kaputte gemischt
zufall = Zufall(2035)
schritte = ["Angebot prüfen", "Freigabe", "Test", "Abnahme", "", "Rechnung"]
kaputte_felder = ["", " ", "zwei Stunden", "4.5", "1,5", "-", "x", "30 min", "ca. 20"]
for _ in range(500):
    wahl = zufall.random()
    if wahl < 0.2:
        zeile = zufall.choice(schritte)
    elif wahl < 0.4:
        zeile = zufall.choice(schritte) + ";" + zufall.choice(kaputte_felder)
    else:
        zeile = zufall.choice(schritte) + ";" + " " * zufall.randint(0, 2) + str(zufall.randint(0, 10000))
    if zufall.random() < 0.3:
        zeile = zeile + ";Kommentar " + str(zufall.randint(0, 9))
    ergebnis, fehler = rufe_auf(zeile)
    erwartet = von_hand(zeile)
    assert fehler is None and ergebnis == erwartet, meldung(zeile, ergebnis, fehler, erwartet)

# An der oberen Grenze: 10 000 Minuten und Zeilen mit 100 Zeichen
for zeile, erwartet in [("Test;10000", 10000), ("x" * 94 + ";10000", 10000), ("Test;" + "x" * 95, -1), ("x" * 100, -1)]:
    ergebnis, fehler = rufe_auf(zeile)
    assert fehler is None and ergebnis == erwartet, meldung(zeile, ergebnis, fehler, erwartet)
