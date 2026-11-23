# Automatisch erzeugt aus lehrkraft/muster/4_067_funkknoten.py - nicht von Hand ändern.
# vorlage-hash: bd924ea912083088
# text-hash: 467efb56696c2c05
# thema: texte_zahlen
# inhalt: re: Muster suchen, Gruppen

def wert_von(funktion, text):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(text)
    except Exception as fehler_:
        return f"{type(fehler_).__name__}: {fehler_}"


def ist_wortzeichen(zeichen):
    """True für Buchstaben, Ziffern und _ (wie \\w bei ASCII)."""
    return zeichen.isalnum() or zeichen == "_"


def vergleich_knoten(text):
    """Vergleichslösung ohne re: zerlegt den Text in Wörter und behält die passenden."""
    woerter = []
    wort = ""
    for zeichen in text + " ":
        if ist_wortzeichen(zeichen):
            wort += zeichen
        else:
            woerter.append(wort)
            wort = ""
    return [wort for wort in woerter if wort[:1] == "K" and 2 <= len(wort) <= 5 and wort[1:].isdigit()]


def meldung(funktion, text, erwartet, hinweis=""):
    """Vergleicht funktion(text) mit erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, text)
    gezeigt = text if len(text) <= 100 else text[:60] + " … " + f"({len(text)} Zeichen)"
    return ergebnis == erwartet, f"{funktion.__name__}({gezeigt!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"


# knoten: ein einzelner Name
stimmt, text = meldung(knoten, "Messung von K17", ["K17"], "\nTipp: re.findall(r'K\\d+', text) findet alle Stellen.")
assert stimmt, text

# knoten: mehrere Namen in ihrer Reihenfolge
stimmt, text = meldung(knoten, "K3 vor K17 vor K3", ["K3", "K17", "K3"])
assert stimmt, text

# knoten: das Beispiel mit Satzzeichen und falschen Kandidaten
stimmt, text = meldung(
    knoten, "K17 an K3: (K0042) XK9 K12345", ["K17", "K3", "K0042"],
    "\nTipp: \\b am Anfang und am Ende verlangt, dass der Name ein eigenes Wort ist; {1,4} begrenzt die Ziffern.",
)
assert stimmt, text

# knoten: Buchstaben oder _ direkt dahinter
stimmt, text = meldung(knoten, "K17a K18_b K19-c", ["K19"], "\nTipp: Auch am Ende braucht es \\b.")
assert stimmt, text

# knoten: ein kleines k und ein K ohne Ziffer zählen nicht
stimmt, text = meldung(knoten, "k17 K Kx K5", ["K5"])
assert stimmt, text

# knoten: leerer Text
stimmt, text = meldung(knoten, "", [])
assert stimmt, text

# messung: das Beispiel
zeile = "[09:35:12] knoten=K17   temp=21.5C feuchte=48%"
ergebnis = wert_von(messung, zeile)
assert isinstance(ergebnis, dict) and ergebnis.get("knoten") == "K17", (
    f"messung({zeile!r}) ergibt {ergebnis!r}, erwartet war ein Dictionary mit 'knoten': 'K17'.\n"
    "Tipp: Suchen Sie mit re.search und benannten Gruppen (?P<knoten>...), dann liefert groupdict() die Texte."
)

# messung: Zahlen umgewandelt
stimmt, text = meldung(
    messung, zeile, {"knoten": "K17", "temp": 21.5, "feuchte": 48},
    "\nTipp: groupdict() liefert Texte; wandeln Sie temp mit float und feuchte mit int um.",
)
assert stimmt, text

# messung: negative ganze Temperatur, Text dahinter
stimmt, text = meldung(
    messung, "[09:35:14] knoten=K3 temp=-2C feuchte=100%  (Kühlraum)", {"knoten": "K3", "temp": -2.0, "feuchte": 100},
    "\nTipp: -? erlaubt ein Minus, (?:\\.\\d+)? macht die Nachkommastellen freiwillig.",
)
assert stimmt, text

# messung: Tabulator statt Leerzeichen
stimmt, text = meldung(messung, "knoten=K0042\ttemp=0.25C\tfeuchte=0%", {"knoten": "K0042", "temp": 0.25, "feuchte": 0})
assert stimmt, text

# messung: fehlende Angabe ergibt None
stimmt, text = meldung(messung, "[09:35:13] knoten=K17 temp=?C", None, "\nTipp: re.search gibt None zurück, wenn nichts passt.")
assert stimmt, text

# messung: ohne Leerzeichen zwischen den Angaben ergibt None
stimmt, text = meldung(messung, "knoten=K1temp=20C feuchte=50%", None)
assert stimmt, text

# messung: Feuchte mit vier Ziffern ergibt None
stimmt, text = meldung(messung, "knoten=K1 temp=20C feuchte=1000%", None, "\nTipp: Die Feuchte hat höchstens drei Ziffern: \\d{1,3}.")
assert stimmt, text

# messung: ein anderes Zeichen statt des Punkts ergibt None
stimmt, text = meldung(messung, "knoten=K1 temp=20x5C feuchte=50%", None, "\nTipp: \\. ist ein echter Punkt, . dagegen jedes Zeichen.")
assert stimmt, text

# fehler: das Beispiel
stimmt, text = meldung(
    fehler, "09:35:20 Gateway: K17 meldet Fehler E42, K3 meldet Fehler E7", [("K17", 42), ("K3", 7)],
    "\nTipp: Mit zwei Gruppen liefert findall Tupel; wandeln Sie die Nummer mit int um.",
)
assert stimmt, text

# fehler: führende Nullen und fünf Ziffern
stimmt, text = meldung(fehler, "K0001 meldet Fehler E00012 und K2 meldet Fehler E99999", [("K0001", 12), ("K2", 99999)])
assert stimmt, text

# fehler: XK9 ist kein Knoten
stimmt, text = meldung(fehler, "XK9 meldet Fehler E1; K9 meldet Fehler E2", [("K9", 2)])
assert stimmt, text

# fehler: ohne Fehler eine leere Liste
stimmt, text = meldung(fehler, "K17 meldet: alles gut", [])
assert stimmt, text

# Mit dem Modul re
funktionen_von_re = ["findall", "search", "fullmatch", "match", "finditer"]
assert any(verwendet(name) for name in funktionen_von_re), "Ihr Code verwendet das Modul re nicht. Suchen Sie mit re.findall und re.search."

# Die Ausgabe des Programms
erwartet = "['K17', 'K3', 'K0042']\n{'knoten': 'K17', 'temp': 21.5, 'feuchte': 48}\n[('K17', 42), ('K3', 7)]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Texte für knoten
zufall = Zufall(4067)
bausteine = ["K", "K1", "K17", "K0042", "K12345", "XK3", "k5", "K7a", "K_8", "Ka", "9", "an", "", "K99"]
for _ in range(1000):
    text = "".join(zufall.choice(bausteine) + zufall.choice(["", " ", ",", "(", ")", ":", "-", "=", "_", "x"]) for _ in range(zufall.randint(0, 6)))
    stimmt, text = meldung(knoten, text, vergleich_knoten(text))
    assert stimmt, text

# Viele zufällige Messzeilen
for _ in range(1000):
    name = "K" + str(zufall.randint(0, 9999)).zfill(zufall.randint(1, 4))
    temp_text = zufall.choice(["", "-"]) + str(zufall.randint(0, 60)) + zufall.choice(["", "." + str(zufall.randint(0, 99))])
    feuchte = zufall.randint(0, 100)
    luecke = [zufall.choice([" ", "  ", "\t"]) for _ in range(2)]
    zeile = f"[{zufall.randint(0, 23):02d}:00] knoten={name}{luecke[0]}temp={temp_text}C{luecke[1]}feuchte={feuchte}%"
    erwartet = {"knoten": name, "temp": float(temp_text), "feuchte": feuchte}
    kaputt = zufall.randint(0, 3)
    if kaputt == 1:
        zeile = zeile.replace("C", "", 1)
        erwartet = None
    elif kaputt == 2:
        zeile = zeile.replace(luecke[1] + "feuchte", "feuchte")
        erwartet = None
    stimmt, text = meldung(messung, zeile, erwartet)
    assert stimmt, text

# Obere Grenze: fehler bei 100 000 Zeichen
text = "K17 meldet Fehler E42, " * 4000 + "K5 "
assert len(text) <= 100000 and wert_von(fehler, text) == [("K17", 42)] * 4000, "Bei 100 000 Zeichen stimmt fehler nicht."

# Obere Grenze: knoten bei 100 000 Zeichen
assert wert_von(knoten, text) == vergleich_knoten(text), "Bei 100 000 Zeichen stimmt knoten nicht."
