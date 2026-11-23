# Automatisch erzeugt aus lehrkraft/muster/4_069_datumsangaben.py - nicht von Hand ändern.
# vorlage-hash: 4124f5cf06dcd2f1
# text-hash: 2da6301349e37dec
# thema: texte_zahlen
# inhalt: re.sub mit Funktion, finditer

NOTIZ = "Fall 17: Antrag 3/7/2026 eingegangen, geprüft 3/12/2026, Version 2/3 freigegeben 11/23/2026."
NOTIZ_DEUTSCH = "Fall 17: Antrag 07.03.2026 eingegangen, geprüft 12.03.2026, Version 2/3 freigegeben 23.11.2026."
STELLEN = [(16, 24, "07.03.2026"), (46, 55, "12.03.2026"), (81, 91, "23.11.2026")]
TAGE = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def wert_von(funktion, text):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(text)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def kurz(wert):
    """Kürzt lange Werte für die Meldung."""
    text = repr(wert)
    return text if len(text) <= 300 else text[:150] + " … " + text[-60:]


def meldung(funktion, text, erwartet, hinweis=""):
    """Prüft funktion(text) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, text)
    nachricht = f"{funktion.__name__}({kurz(text)})\nergibt   {kurz(ergebnis)}\nerwartet {kurz(erwartet)}{hinweis}"
    return ergebnis == erwartet, nachricht


def zufallstext(zufall, stuecke):
    """Setzt einen Text aus Daten und Störstellen zusammen; liefert (text, erwarteter Text, Fundstellen)."""
    teile = []
    deutsch_teile = []
    stellen = []
    laenge = 0
    for _ in range(stuecke):
        trenner = zufall.choice([" ", ", ", " (", "): ", "\n", " am ", "-"])
        teile.append(trenner)
        deutsch_teile.append(trenner)
        laenge += len(trenner)
        if zufall.random() < 0.5:
            monat = zufall.randint(1, 12)
            tag = zufall.randint(1, TAGE[monat - 1])
            jahr = zufall.randint(1990, 2099)
            us = f"{monat:0{zufall.randint(1, 2)}d}/{tag:0{zufall.randint(1, 2)}d}/{jahr}"
            neu = f"{tag:02d}.{monat:02d}.{jahr}"
            stellen.append((laenge, laenge + len(us), neu))
        else:
            us = zufall.choice(["Version 2/3", "12/2026", "1/2/20265", "011/23/2026", "x3/4/2026", "3/4/26", "a/b/c", "Fall"])
            neu = us
        teile.append(us)
        deutsch_teile.append(neu)
        laenge += len(us)
    return "".join(teile), "".join(deutsch_teile), stellen


# vereinheitliche: das Beispiel
stimmt, text = meldung(vereinheitliche, NOTIZ, NOTIZ_DEUTSCH, "\nTipp: Ersetzen Sie mit re.sub und einer Funktion, die einen Treffer bekommt.")
assert stimmt, text

# vereinheitliche: Monat und Tag vertauscht (nicht fest hinschreiben!)
stimmt, text = meldung(
    vereinheitliche, "Lieferung am 12/10/2027", "Lieferung am 10.12.2027",
    "\nTipp: Die erste Zahl ist der Monat, die zweite der Tag; deutsch kommt der Tag zuerst.",
)
assert stimmt, text

# vereinheitliche: führende Nullen
stimmt, text = meldung(
    vereinheitliche, "Start 1/2/2026", "Start 02.01.2026", "\nTipp: f\"{int(tag):02d}\" stellt eine Null voran."
)
assert stimmt, text

# vereinheitliche: schon vorhandene führende Nullen bleiben zwei Ziffern
stimmt, text = meldung(vereinheitliche, "Ende 03/07/2026", "Ende 07.03.2026")
assert stimmt, text

# vereinheitliche: ein Datum am Anfang und eins am Ende
stimmt, text = meldung(vereinheitliche, "9/30/2026 bis 10/1/2026", "30.09.2026 bis 01.10.2026")
assert stimmt, text

# vereinheitliche: Zahlen mit nur einem Schrägstrich sind kein Datum und bleiben stehen
for unveraendert in ["Version 2/3", "Monat 12/2026"]:
    stimmt, text = meldung(
        vereinheitliche, unveraendert, unveraendert, "\nTipp: Ein Datum hat zwei Schrägstriche: Monat/Tag/Jahr."
    )
    assert stimmt, text

# vereinheitliche: das Jahr hat genau vier Ziffern, sonst bleibt der Text stehen
for unveraendert in ["Jahr 1/2/20265", "kurz 3/4/26"]:
    stimmt, text = meldung(
        vereinheitliche, unveraendert, unveraendert,
        "\nTipp: Genau vier Ziffern für das Jahr (\\d{4}) und \\b am Ende des Musters.",
    )
    assert stimmt, text

# vereinheitliche: vor dem Monat beginnt ein neues Wort, sonst bleibt der Text stehen
for unveraendert in ["Nummer 011/23/2026", "x3/4/2026"]:
    stimmt, text = meldung(
        vereinheitliche, unveraendert, unveraendert, "\nTipp: \\b auch am Anfang des Musters."
    )
    assert stimmt, text

# vereinheitliche: ein Text ohne Datum und der leere Text
for unveraendert in ["Bestellung freigegeben.", ""]:
    stimmt, text = meldung(vereinheitliche, unveraendert, unveraendert)
    assert stimmt, text

# fundstellen: das Beispiel
stimmt, text = meldung(
    fundstellen, NOTIZ, STELLEN,
    "\nTipp: treffer.start() und treffer.end() geben die Positionen im ursprünglichen Text an.",
)
assert stimmt, text

# fundstellen: ein Datum am Anfang (andere Werte)
stimmt, text = meldung(fundstellen, "12/1/2027 ab 8 Uhr", [(0, 9, "01.12.2027")])
assert stimmt, text

# fundstellen: Positionen im ursprünglichen, nicht im umgewandelten Text
stimmt, text = meldung(
    fundstellen, "1/2/2026, 1/3/2026", [(0, 8, "02.01.2026"), (10, 18, "03.01.2026")],
    "\nTipp: Suchen Sie im übergebenen Text, nicht im Ergebnis von vereinheitliche.",
)
assert stimmt, text

# fundstellen: kein Datum
stimmt, text = meldung(fundstellen, "Version 2/3", [])
assert stimmt, text

# fundstellen: der leere Text
stimmt, text = meldung(fundstellen, "", [])
assert stimmt, text

# Benutzt werden re.sub mit einer Funktion und re.finditer
fehlt = [name for name in ["sub", "finditer"] if not verwendet(name)]
assert not fehlt, f"Ihr Code verwendet {fehlt} nicht. Die Aufgabe verlangt re.sub mit einer Funktion und re.finditer."

# Die Ausgabe des Programms
erwartet = f"{NOTIZ_DEUTSCH}\n{STELLEN}"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Notizen
zufall = Zufall(4069)
for _ in range(500):
    notiz, deutsch_erwartet, stellen = zufallstext(zufall, zufall.randint(0, 6))
    stimmt, text = meldung(vereinheitliche, notiz, deutsch_erwartet)
    assert stimmt, text
    stimmt, text = meldung(fundstellen, notiz, stellen)
    assert stimmt, text

# Obere Grenze: vereinheitliche bei etwa 85 000 Zeichen
notiz, deutsch_erwartet, stellen = zufallstext(zufall, 8000)
assert wert_von(vereinheitliche, notiz) == deutsch_erwartet, f"Bei {len(notiz)} Zeichen stimmt vereinheitliche nicht."

# Obere Grenze: fundstellen bei etwa 85 000 Zeichen
assert wert_von(fundstellen, notiz) == stellen, f"Bei {len(notiz)} Zeichen stimmt fundstellen nicht."
