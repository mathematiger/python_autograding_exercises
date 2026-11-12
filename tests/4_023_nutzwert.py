# Automatisch erzeugt aus lehrkraft/muster/4_023_nutzwert.py - nicht von Hand ändern.
# vorlage-hash: 0c3f3907e236a84e
# text-hash: d182c2e2599f7a79
# thema: funktionen
# inhalt: Dekoratoren mit Argumenten

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "300 600 640\n['Energie', 'Preis', 'Support']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"

# Jedes Kriterium gewichtet mit seinem eigenen Gewicht
ergebnis = (preis(angebot_b), support(angebot_b), energie(angebot_b), support(angebot_a))
assert ergebnis == (200, 300, 140, 180), (
    f"preis, support und energie für angebot_b und support für angebot_a ergeben {ergebnis!r}, erwartet war "
    "(200, 300, 140, 180), also 4·50, 10·30, 7·20 und 6·30.\n"
    "Tipp: Die Hülle muss das Gewicht aus ihrem eigenen Aufruf von kriterium benutzen, nicht eine globale Variable."
)

# Die Kriterien des Programms stehen unter ihrem Namen in KRITERIEN
eintraege = {name: KRITERIEN.get(name) for name in ["Preis", "Support", "Energie"]}
assert eintraege == {"Preis": preis, "Support": support, "Energie": energie} and len(KRITERIEN) == 3, (
    f"KRITERIEN enthält {KRITERIEN!r}; erwartet waren genau die Schlüssel 'Preis', 'Support' und 'Energie' mit den "
    "dekorierten Funktionen preis, support und energie als Werten.\n"
    "Tipp: Tragen Sie im Dekorator dieselbe Hüllfunktion in KRITERIEN ein, die Sie auch zurückgeben."
)

# functools.wraps übernimmt Name, Docstring und __wrapped__
angaben = (preis.__name__, energie.__doc__, getattr(support, "__wrapped__", None) is not None)
assert angaben == ("preis", "10 Punkte für ein sparsames Gerät, je 10 Watt einen weniger.", True), (
    f"Die dekorierte Funktion preis heißt {angaben[0]!r}, energie hat den Docstring {angaben[1]!r}, __wrapped__ "
    f"vorhanden: {angaben[2]}; erwartet waren Name und Docstring der Bewertungsfunktion und __wrapped__.\n"
    "Tipp: Schreiben Sie @functools.wraps(bewertung) über die Hüllfunktion."
)

# __wrapped__ ist die ungewichtete Bewertungsfunktion
ergebnis = (preis.__wrapped__(angebot_a), support.__wrapped__(angebot_b))
assert ergebnis == (6, 10), f"preis.__wrapped__(angebot_a) und support.__wrapped__(angebot_b) ergeben {ergebnis!r}, erwartet war (6, 10)."

# Ein Name, den es schon gibt, löst sofort einen ValueError aus und ändert nichts
eintrag_vorher = KRITERIEN.get("Preis")
try:
    kriterium("Preis", gewicht=10)
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
if KRITERIEN.get("Preis") is eintrag_vorher:
    veraendert = ""
else:
    veraendert = f", KRITERIEN['Preis'] ist danach {KRITERIEN.get('Preis')!r} statt {eintrag_vorher!r}"
assert fehler is not None and KRITERIEN.get("Preis") is eintrag_vorher and preis(angebot_a) == 300, (
    f"kriterium('Preis', gewicht=10) muss sofort einen ValueError auslösen, weil es 'Preis' schon gibt, und "
    f"KRITERIEN['Preis'] unverändert lassen; bekommen: {'kein ValueError' if fehler is None else repr(fehler)}"
    f"{veraendert}.\nTipp: Prüfen Sie name in KRITERIEN in kriterium selbst, bevor Sie den Dekorator "
    "zurückgeben."
)

# Zu kleine Gewichte lösen sofort einen ValueError aus
for gewicht in [0, -5, -1000]:
    anzahl_vorher = len(KRITERIEN)
    try:
        kriterium("Lärm", gewicht)
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    assert fehler is not None and len(KRITERIEN) == anzahl_vorher, (
        f"kriterium('Lärm', {gewicht}) muss sofort einen ValueError auslösen; bekommen: "
        f"{'kein ValueError' if fehler is None else repr(fehler)}.\n"
        "Tipp: Erlaubt sind nur Gewichte von 1 bis 100; prüfen Sie das in kriterium, nicht erst in der Hülle."
    )

# Gewichte außerhalb von 1 bis 100 lösen sofort einen ValueError aus
for gewicht in [0, 101, -5, 1000, -1000]:
    anzahl_vorher = len(KRITERIEN)
    try:
        kriterium("Lärm", gewicht)
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    assert fehler is not None and len(KRITERIEN) == anzahl_vorher, (
        f"kriterium('Lärm', {gewicht}) muss sofort einen ValueError auslösen; bekommen: "
        f"{'kein ValueError' if fehler is None else repr(fehler)}.\n"
        "Tipp: Erlaubt sind nur Gewichte von 1 bis 100; prüfen Sie das in kriterium, nicht erst in der Hülle."
    )

# Die Gewichte 1 und 100 an den Rändern sind erlaubt
KRITERIEN.clear()
try:

    @kriterium("Ergonomie", 1)
    def ergonomie(angebot):
        """Punkte für die Tastatur."""
        return angebot["tastatur"]

    @kriterium("Display", 100)
    def display(angebot):
        """Punkte für das Display."""
        return angebot["display"]

    fehler = None
    ergebnis = nutzwert({"tastatur": 7, "display": 3})
except ValueError as ausnahme:
    fehler = ausnahme
    ergebnis = None
assert fehler is None and ergebnis == 307, (
    f"Mit den Gewichten 1 und 100 kam {'keine Ausnahme' if fehler is None else repr(fehler)}, und nutzwert für 7 "
    f"und 3 Punkte ergibt {ergebnis!r}; erwartet war keine Ausnahme und 7·1 + 3·100 = 307.\n"
    "Tipp: Beide Grenzen gehören dazu, 1 <= gewicht <= 100; KRITERIEN muss die gewichteten Hüllen enthalten."
)

# Punkte 0 und 10 an den Rändern sind erlaubt
ergebnis = (display({"display": 0}), display({"display": 10}), ergonomie({"tastatur": 10}))
assert ergebnis == (0, 1000, 10), (
    f"Bewertungen mit 0 und 10 Punkten ergeben {ergebnis!r}, erwartet war (0, 1000, 10).\n"
    "Tipp: Erlaubt sind die Punkte 0 bis 10, beide eingeschlossen."
)

# Punkte außerhalb von 0 bis 10 lösen einen ValueError aus
falsche_punkte = []
for punkte in [11, -1, 100, -100]:
    try:
        display({"display": punkte})
        meldung = None
    except ValueError as ausnahme:
        meldung = str(ausnahme)
    falsche_punkte.append((punkte, meldung))
for punkte, meldung in falsche_punkte:
    assert meldung is not None, (
        f"Eine Bewertung mit {punkte} Punkten für das Kriterium 'Display' muss einen ValueError auslösen, "
        "hat aber keinen ausgelöst.\nTipp: Prüfen Sie in der Hülle, ob die Punkte zwischen 0 und 10 liegen."
    )

# Punkte außerhalb von 0 bis 10 lösen einen ValueError mit Name und Punkten aus
for punkte, meldung in falsche_punkte:
    assert meldung is not None and vergleichbar("Display") in vergleichbar(meldung) and str(punkte) in meldung, (
        f"Eine Bewertung mit {punkte} Punkten für das Kriterium 'Display' muss einen ValueError auslösen, dessen "
        f"Meldung 'Display' und {punkte} enthält; bekommen: {'kein ValueError' if meldung is None else repr(meldung)}."
        "\nTipp: Die Hülle kennt name aus der Closure und kann ihn in die Meldung schreiben."
    )

# Die Bewertungsfunktion läuft genau einmal je Aufruf
aufrufe = []
KRITERIEN.clear()


@kriterium("Akku", 40)
def akku(angebot):
    """Merkt sich jeden Aufruf."""
    aufrufe.append(angebot)
    return 5


ergebnis = (akku("A"), akku("B"))
assert ergebnis == (200, 200) and aufrufe == ["A", "B"], (
    f"Zwei Aufrufe von akku ergeben {ergebnis!r} und rufen die Bewertungsfunktion mit {aufrufe!r} auf; erwartet war "
    "(200, 200) und genau ein Aufruf je Aufruf.\nTipp: Rufen Sie bewertung(angebot) einmal auf und merken Sie sich "
    "die Punkte, bevor Sie sie prüfen und multiplizieren."
)

# Viele zufällige Kriterien und Angebote gegen eine Nachrechnung
zufall = Zufall(4023)
for runde in range(100):
    KRITERIEN.clear()
    gewichte = {}
    for nummer in range(zufall.randint(1, 8)):
        name = f"K{nummer}"
        gewichte[name] = zufall.randint(1, 100)
        kriterium(name, gewichte[name])(lambda angebot, name=name: angebot[name])
    angebot = {name: zufall.randint(0, 10) for name in gewichte}
    erwartet = sum(angebot[name] * gewichte[name] for name in gewichte)
    ergebnis = nutzwert(angebot)
    assert ergebnis == erwartet and sorted(KRITERIEN) == sorted(gewichte), (
        f"Mit den Gewichten {gewichte} und den Punkten {angebot} ergibt nutzwert {ergebnis!r} und KRITERIEN hat die "
        f"Schlüssel {sorted(KRITERIEN)}; erwartet war {erwartet} und die Schlüssel {sorted(gewichte)}."
    )

# Zufällige Gewichte und Punkte innerhalb der Grenzen: ValueError genau dann, wenn außerhalb des erlaubten Bereichs
for _ in range(300):
    KRITERIEN.clear()
    gewicht = zufall.choice([zufall.randint(-1000, 1000), zufall.randint(-2, 3), zufall.randint(98, 103)])
    punkte = zufall.choice([zufall.randint(-100, 100), zufall.randint(-2, 12)])
    try:
        gewichtet = kriterium("Test", gewicht)(lambda angebot: punkte)
        ergebnis = gewichtet(None)
    except ValueError:
        ergebnis = "ValueError"
    erwartet = punkte * gewicht if 1 <= gewicht <= 100 and 0 <= punkte <= 10 else "ValueError"
    assert ergebnis == erwartet, (
        f"kriterium('Test', {gewicht}) mit einer Bewertung von {punkte} Punkten ergibt {ergebnis!r}, erwartet war "
        f"{erwartet!r}."
    )

# An der oberen Grenze: 1000 Kriterien
KRITERIEN.clear()
for nummer in range(1000):
    kriterium(f"K{nummer}", nummer % 100 + 1)(lambda angebot, nummer=nummer: (angebot + nummer) % 11)
erwartet = sum(((7 + nummer) % 11) * (nummer % 100 + 1) for nummer in range(1000))
ergebnis = nutzwert(7)
assert len(KRITERIEN) == 1000 and ergebnis == erwartet, (
    f"Mit 1000 Kriterien hat KRITERIEN {len(KRITERIEN)} Einträge und nutzwert(7) ergibt {ergebnis!r}; erwartet waren "
    f"1000 Einträge und {erwartet}."
)
