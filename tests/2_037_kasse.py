# Automatisch erzeugt aus lehrkraft/muster/2_037_kasse.py - nicht von Hand ändern.
# vorlage-hash: e7383f08edd1f600
# text-hash: 1bbc1bf4e07397e7
# thema: funktionen
# inhalt: Funktionen wiederverwenden

EINGABEN = ["0"]

MENUE = """==============================
          TECH-SHOP
==============================
1 – Einkauf bearbeiten
2 – Preisanfrage berechnen
0 – Programm beenden"""


def rufe_auf(funktion, *argumente):
    """Ruft funktion(*argumente) auf; liefert Rückgabewert, Ausgabe, Zahl der input-Aufrufe und Ausnahme (sonst None)."""
    global print, input
    ausgabe = []
    fragen = []

    def merke(*werte, sep=" ", end="\n", **_):
        """Wie print, merkt sich die Ausgabe aber nur."""
        ausgabe.append(sep.join(str(wert) for wert in werte) + end)

    def keine_eingabe(aufforderung=""):
        """Wie input, merkt sich aber nur, dass gefragt wurde."""
        fragen.append(aufforderung)
        return "0"

    altes_print, altes_input = print, input
    print, input = merke, keine_eingabe
    try:
        ergebnis, fehler = funktion(*argumente), None
    except Exception as ausnahme:
        ergebnis, fehler = None, ausnahme
    finally:
        print, input = altes_print, altes_input
    return ergebnis, "".join(ausgabe), len(fragen), fehler


def ungefaehr(ergebnis, erwartet):
    """Prüft, ob ergebnis eine Zahl ist, die bis auf Rundungsfehler erwartet ist."""
    return isinstance(ergebnis, (int, float)) and abs(ergebnis - erwartet) < 1e-6


def pruefe_rechnung(aufruf, ergebnis, fehler, erwartet, tipp=""):
    """Baut die Meldung für eine berechne-Funktion: Absturz oder falscher Wert, dazu ein Tipp."""
    if fehler is not None:
        return f"{aufruf} ist mit {type(fehler).__name__}: {fehler} abgestürzt, erwartet war {erwartet!r}."
    text = f"{aufruf} ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    if ergebnis is None:
        text = text + "\nTipp: Geben Sie das Ergebnis mit return zurück, statt es auszugeben."
    elif tipp:
        text = text + "\nTipp: " + tipp
    return text


def betraege(ausgabe, wort):
    """Liefert aus jeder Zeile, die mit wort beginnt, die erste Zahl dahinter als Text."""
    gefunden = []
    for zeile in ausgabe.splitlines():
        zeile = zeile.strip()
        if not zeile.casefold().startswith(wort.casefold()):
            continue
        for teil in zeile[len(wort) :].replace("€", " ").replace(":", " ").split():
            try:
                float(teil.replace(",", "."))
            except ValueError:
                continue
            gefunden.append(teil)
            break
    return gefunden


def passt(texte, erwartet):
    """Prüft, ob die gefundenen Beträge bis auf einen halben Cent die erwarteten sind."""
    if len(texte) != len(erwartet):
        return False
    for text, wert in zip(texte, erwartet):
        if abs(float(text.replace(",", ".")) - wert) > 0.0051:
            return False
    return True


def meldung_lauf(eingaben, ausgabe, wort, gefunden, erwartet):
    """Baut die Meldung, wenn die Zeilen mit wort nicht die erwarteten Beträge enthalten."""
    return (
        f"Mit den Eingaben {list(eingaben)} erwartet: Zeilen, die mit „{wort}“ beginnen, mit den Beträgen "
        f"{[f'{wert:.2f}' for wert in erwartet]} - gefunden: {gefunden}.\nIhr Programm gibt aus:\n{ausgabe}"
    )


def anzahl_menues(ausgabe):
    """Zählt, wie oft das Menü in der Ausgabe steht."""
    return vergleichbar(ausgabe).count(vergleichbar(MENUE))


def von_hand(positionen):
    """Vergleichslösung in Cent: liefert Gesamtbetrag, Rabatt und Endbetrag eines Einkaufs in Euro."""
    gesamt_cent = 0
    for _, cent, menge in positionen:
        gesamt_cent = gesamt_cent + cent * menge
    rabatt_cent = gesamt_cent / 10 if gesamt_cent >= 5000 else 0
    return gesamt_cent / 100, rabatt_cent / 100, (gesamt_cent - rabatt_cent) / 100


def als_eingaben(positionen):
    """Macht aus Positionen (Name, Preis in Cent, Menge) die Eingaben für einen Einkauf, mit Punkt im Preis."""
    eingaben = ["1", str(len(positionen))]
    for name, cent, menge in positionen:
        preis = str(cent // 100) if cent % 100 == 0 else f"{cent / 100:.2f}"
        eingaben = eingaben + [name, preis, str(menge)]
    return eingaben


# berechne_positionsbetrag(15.0, 2) aus der Aufgabe
ergebnis, _, _, fehler = rufe_auf(berechne_positionsbetrag, 15.0, 2)
assert ungefaehr(ergebnis, 30), pruefe_rechnung("berechne_positionsbetrag(15.0, 2)", ergebnis, fehler, 30.0)

# berechne_positionsbetrag(8.5, 3) (nicht fest hinschreiben!)
ergebnis, _, _, fehler = rufe_auf(berechne_positionsbetrag, 8.5, 3)
assert ungefaehr(ergebnis, 25.5), pruefe_rechnung(
    "berechne_positionsbetrag(8.5, 3)", ergebnis, fehler, 25.5, "Rechnen Sie mit den Parametern einzelpreis und menge."
)

# berechne_rabatt(54.0) aus der Aufgabe: 10 %
ergebnis, _, _, fehler = rufe_auf(berechne_rabatt, 54.0)
assert ungefaehr(ergebnis, 5.4), pruefe_rechnung(
    "berechne_rabatt(54.0)", ergebnis, fehler, 5.4, "Der Rabatt ist 10 % des Gesamtbetrags, also gesamtbetrag * 0.1."
)

# berechne_rabatt(49.0) aus der Aufgabe: unter 50 € kein Rabatt
ergebnis, _, _, fehler = rufe_auf(berechne_rabatt, 49.0)
assert ungefaehr(ergebnis, 0), pruefe_rechnung("berechne_rabatt(49.0)", ergebnis, fehler, 0)

# berechne_rabatt(1234.5): 10 % von einem anderen Betrag
ergebnis, _, _, fehler = rufe_auf(berechne_rabatt, 1234.5)
assert ungefaehr(ergebnis, 123.45), pruefe_rechnung("berechne_rabatt(1234.5)", ergebnis, fehler, 123.45)

# berechne_rabatt(50.0): genau 50 € bekommen schon Rabatt
ergebnis, _, _, fehler = rufe_auf(berechne_rabatt, 50.0)
assert ungefaehr(ergebnis, 5), pruefe_rechnung(
    "berechne_rabatt(50.0)", ergebnis, fehler, 5.0, "„Ab 50 € einschließlich“ heißt >= 50, nicht > 50."
)

# berechne_rabatt(49.99): knapp unter der Grenze kein Rabatt
ergebnis, _, _, fehler = rufe_auf(berechne_rabatt, 49.99)
assert ungefaehr(ergebnis, 0), pruefe_rechnung("berechne_rabatt(49.99)", ergebnis, fehler, 0)

# berechne_endbetrag(54.0, 5.4) aus der Aufgabe
ergebnis, _, _, fehler = rufe_auf(berechne_endbetrag, 54.0, 5.4)
assert ungefaehr(ergebnis, 48.6), pruefe_rechnung(
    "berechne_endbetrag(54.0, 5.4)", ergebnis, fehler, 48.6, "Ziehen Sie den Rabattbetrag vom Gesamtbetrag ab."
)

# berechne_endbetrag(80.0, 8.0) und (30.0, 0) (nicht fest hinschreiben!)
ergebnis, _, _, fehler = rufe_auf(berechne_endbetrag, 80.0, 8.0)
zweites, _, _, zweiter_fehler = rufe_auf(berechne_endbetrag, 30.0, 0)
assert ungefaehr(ergebnis, 72) and ungefaehr(zweites, 30), (
    pruefe_rechnung("berechne_endbetrag(80.0, 8.0)", ergebnis, fehler, 72.0)
    + "\n"
    + pruefe_rechnung("berechne_endbetrag(30.0, 0)", zweites, zweiter_fehler, 30.0)
)

# Die berechne-Funktionen fragen nichts und geben nichts aus
stoerungen = []
for name, funktion, argumente in [
    ("berechne_positionsbetrag", berechne_positionsbetrag, (15.0, 2)),
    ("berechne_rabatt", berechne_rabatt, (54.0,)),
    ("berechne_endbetrag", berechne_endbetrag, (54.0, 5.4)),
]:
    _, ausgabe, fragen, _ = rufe_auf(funktion, *argumente)
    if ausgabe or fragen:
        stoerungen.append(name)
assert stoerungen == [], (
    f"Diese Funktionen benutzen print oder input: {', '.join(stoerungen)}.\n"
    "Tipp: Die berechne-Funktionen bekommen alles über ihre Parameter und liefern das Ergebnis mit return. "
    "Fragen und Ausgeben gehört ins Hauptprogramm bzw. nach zeige_artikel."
)

# zeige_artikel("Maus", 15.0, 2, 30.0) gibt Name, Menge und Beträge aus
_, ausgabe, _, fehler = rufe_auf(zeige_artikel, "Maus", 15.0, 2, 30.0)
assert fehler is None and "Maus" in ausgabe and "2" in ausgabe and "15" in ausgabe and "30" in ausgabe, (
    f'zeige_artikel("Maus", 15.0, 2, 30.0) gibt aus:\n{ausgabe}\n'
    "Erwartet war eine Ausgabe mit Artikelname, Menge, Einzelpreis und Positionsbetrag, z. B. "
    "Maus: 2 x 15.00 € = 30.00 €" + ("" if fehler is None else f"\nDie Funktion ist mit {fehler!r} abgestürzt.")
)

# zeige_artikel zeigt die Geldbeträge mit zwei Nachkommastellen
_, ausgabe, _, fehler = rufe_auf(zeige_artikel, "Netzteil", 12.5, 3, 37.5)
assert fehler is None and "Netzteil" in ausgabe and "12.50" in ausgabe and "37.50" in ausgabe, (
    f'zeige_artikel("Netzteil", 12.5, 3, 37.5) gibt aus:\n{ausgabe}\n'
    "Erwartet waren Einzelpreis 12.50 und Positionsbetrag 37.50 mit zwei Nachkommastellen.\n"
    'Tipp: f"{einzelpreis:.2f}"'
)

# Beim Start erscheint das Menü
assert vergleichbar(MENUE) in vergleichbar(AUSGABE), (
    f"Beim Start erwartet:\n{MENUE}\nIhr Programm gibt aus:\n{AUSGABE}"
)

# Bei 0 endet das Programm sofort
ausgabe = starte("0")
assert anzahl_menues(ausgabe) == 1, (
    f"Mit der Eingabe 0 soll das Menü genau einmal erscheinen, dann endet das Programm. Ihr Programm gibt aus:\n"
    f"{ausgabe}"
)

# Einkauf ohne Rabatt: 2 Mäuse zu je 15 €
eingaben = ["1", "1", "Maus", "15", "2", "0"]
ausgabe = starte(*eingaben)
gefunden = betraege(ausgabe, "Endbetrag")
assert passt(gefunden, [30]), meldung_lauf(eingaben, ausgabe, "Endbetrag", gefunden, [30])

# Einkauf ohne Rabatt: Gesamtbetrag und Rabatt stehen auch da
gefunden = betraege(ausgabe, "Gesamtbetrag") + betraege(ausgabe, "Rabatt")
assert passt(gefunden, [30, 0]), meldung_lauf(eingaben, ausgabe, "Gesamtbetrag“ und „Rabatt", gefunden, [30, 0])

# Die Position erscheint mit zeige_artikel
assert "Maus" in ausgabe and "30" in ausgabe, (
    f"Mit den Eingaben {eingaben} erwartet: eine Zeile von zeige_artikel mit Maus und 30.00 €. "
    f"Ihr Programm gibt aus:\n{ausgabe}\nTipp: Rufen Sie zeige_artikel in der for-Schleife für jede Position auf."
)

# Mehrere Positionen: 3 USB-Kabel zu je 8 € und 2 Mäuse zu je 15 €
eingaben = ["1", "2", "USB-Kabel", "8", "3", "Maus", "15", "2", "0"]
ausgabe = starte(*eingaben)
gefunden = betraege(ausgabe, "Gesamtbetrag") + betraege(ausgabe, "Rabatt") + betraege(ausgabe, "Endbetrag")
if passt(gefunden, [54, 0, 54]):
    tipp = "\nTipp: Der Rabatt gilt für den ganzen Einkauf. Berechnen Sie ihn erst nach der Schleife."
elif passt(gefunden, [30, 0, 30]):
    tipp = "\nTipp: Addieren Sie jeden Positionsbetrag zum Gesamtbetrag, statt ihn zu überschreiben."
else:
    tipp = ""
assert passt(gefunden, [54, 5.4, 48.6]), (
    meldung_lauf(eingaben, ausgabe, "Gesamtbetrag“, „Rabatt“ und „Endbetrag", gefunden, [54, 5.4, 48.6]) + tipp
)

# Die Beträge stehen mit zwei Nachkommastellen da
assert gefunden == ["54.00", "5.40", "48.60"], (
    f"Mit den Eingaben {eingaben} erwartet: 54.00, 5.40 und 48.60 - gefunden: {gefunden}.\n"
    'Tipp: f"{endbetrag:.2f}" zeigt immer zwei Nachkommastellen.'
)

# Rabattgrenze: 5 Stück zu je 10 € ergeben genau 50 €
eingaben = ["1", "1", "Lüfter", "10", "5", "0"]
ausgabe = starte(*eingaben)
gefunden = betraege(ausgabe, "Rabatt") + betraege(ausgabe, "Endbetrag")
assert passt(gefunden, [5, 45]), meldung_lauf(eingaben, ausgabe, "Rabatt“ und „Endbetrag", gefunden, [5, 45])

# Knapp unter der Rabattgrenze: 49.99 €
eingaben = ["1", "1", "Headset", "49.99", "1", "0"]
ausgabe = starte(*eingaben)
gefunden = betraege(ausgabe, "Rabatt") + betraege(ausgabe, "Endbetrag")
assert passt(gefunden, [0, 49.99]), meldung_lauf(eingaben, ausgabe, "Rabatt“ und „Endbetrag", gefunden, [0, 49.99])

# Zwei Einkäufe nacheinander: der Gesamtbetrag beginnt jedes Mal bei 0
eingaben = ["1", "1", "Monitor", "60", "1", "1", "1", "Kabel", "20", "1", "0"]
ausgabe = starte(*eingaben)
gefunden = betraege(ausgabe, "Endbetrag")
assert passt(gefunden, [54, 20]), meldung_lauf(eingaben, ausgabe, "Endbetrag", gefunden, [54, 20]) + (
    "\nTipp: Setzen Sie gesamtbetrag = 0.0 bei jedem Einkauf, also im Zweig für die Auswahl 1."
    if passt(gefunden, [54, 72])
    else ""
)

# Preisanfrage: 10 USB-Kabel zu je 8 €
eingaben = ["2", "USB-Kabel", "8", "10", "0"]
ausgabe = starte(*eingaben)
gefunden = betraege(ausgabe, "Rabatt") + betraege(ausgabe, "Angebotspreis")
assert passt(gefunden, [8, 72]), meldung_lauf(eingaben, ausgabe, "Rabatt“ und „Angebotspreis", gefunden, [8, 72])

# Preisanfrage: Überschrift und Position mit zeige_artikel
assert vergleichbar("Unverbindliches Preisangebot") in vergleichbar(ausgabe) and "80" in ausgabe, (
    f"Mit den Eingaben {eingaben} erwartet: die Überschrift „Unverbindliches Preisangebot“ und die Position "
    f"mit 80.00 € von zeige_artikel. Ihr Programm gibt aus:\n{ausgabe}"
)

# Preisanfrage ohne Rabatt: 1 Maus zu 15 €, mit zwei Nachkommastellen
eingaben = ["2", "Maus", "15", "1", "0"]
ausgabe = starte(*eingaben)
gefunden = betraege(ausgabe, "Rabatt") + betraege(ausgabe, "Angebotspreis")
assert gefunden == ["0.00", "15.00"], (
    meldung_lauf(eingaben, ausgabe, "Rabatt“ und „Angebotspreis", gefunden, [0, 15])
    + '\nTipp: f"{rabattbetrag:.2f}" zeigt auch 0 als 0.00.'
)

# Nach jeder Aktion erscheint das Menü wieder
eingaben = ["1", "1", "Maus", "15", "2", "2", "Maus", "15", "1", "0"]
ausgabe = starte(*eingaben)
assert anzahl_menues(ausgabe) == 3, (
    f"Mit den Eingaben {eingaben} soll das Menü dreimal erscheinen (vor dem Einkauf, vor der Preisanfrage, "
    f"vor der 0). Ihr Programm gibt aus:\n{ausgabe}"
)

# Bei einer ungültigen Auswahl (9 oder abc) gibt es einen Hinweis, dann wieder das Menü
nur_ende = vergleichbar(starte("0")).replace(vergleichbar(MENUE), "")
for falsch in ["9", "abc"]:
    ausgabe = starte(falsch, "0")
    rest = vergleichbar(ausgabe).replace(vergleichbar(MENUE), "")
    assert anzahl_menues(ausgabe) == 2 and len(rest) > len(nur_ende), (
        f"Mit den Eingaben {[falsch, '0']} erwartet: Menü, ein Hinweis, Menü. Ihr Programm gibt aus:\n{ausgabe}\n"
        "Tipp: Fangen Sie alle anderen Eingaben mit else ab und geben Sie dort einen Hinweis aus."
    )

# Das Hauptprogramm benutzt die vier Funktionen
fehlend = []
for name in ["berechne_positionsbetrag", "berechne_rabatt", "berechne_endbetrag", "zeige_artikel"]:
    if not verwendet(name):
        fehlend.append(name)
assert fehlend == [], (
    f"Diese Funktionen ruft Ihr Programm nicht auf: {', '.join(fehlend)}.\n"
    "Tipp: Rechnen Sie im Hauptprogramm nicht selbst, sondern rufen Sie die Funktionen auf - in beiden Zweigen."
)

# Das Menü ist eine while-Schleife, die Positionen laufen mit for
assert verwendet("while") and verwendet("for"), (
    "Benutzen Sie für das Menü eine while-Schleife und für die Positionen eines Einkaufs eine for-Schleife."
)

# 150 zufällige Einkäufe und Preisanfragen
zufall = Zufall(2037)
namen = ["Maus", "Tastatur", "USB-Kabel", "Monitor", "SSD", "Headset", "Webcam"]
for _ in range(150):
    positionen = []
    for _ in range(zufall.randint(1, 5)):
        positionen.append((zufall.choice(namen), zufall.randint(1, 4000), zufall.randint(1, 5)))
    gesamt, rabatt, end = von_hand(positionen)
    if gesamt == 50:
        # Genau 50 € prüft der Test zur Rabattgrenze; hier könnte die Summe der Kommazahlen knapp daneben liegen.
        continue
    eingaben = als_eingaben(positionen)
    if len(positionen) == 1 and zufall.random() < 0.5:
        eingaben[0:2] = ["2"]
        woerter, erwartet = ["Rabatt", "Angebotspreis"], [rabatt, end]
    else:
        woerter, erwartet = ["Gesamtbetrag", "Rabatt", "Endbetrag"], [gesamt, rabatt, end]
    eingaben.append("0")
    ausgabe = starte(*eingaben)
    gefunden = []
    for wort in woerter:
        gefunden = gefunden + betraege(ausgabe, wort)
    assert passt(gefunden, erwartet), meldung_lauf(eingaben, ausgabe, "“, „".join(woerter), gefunden, erwartet)

# An der oberen Grenze: 100 Positionen mit je 1000 Stück zu 10 000 €
eingaben = ["1", "100"]
for nummer in range(100):
    eingaben = eingaben + [f"Server {nummer}", "10000", "1000"]
eingaben.append("0")
ausgabe = starte(*eingaben)
gefunden = betraege(ausgabe, "Endbetrag")
assert passt(gefunden, [900_000_000]), (
    f"Bei 100 Positionen mit je 1000 Stück zu 10 000 € erwartet: Endbetrag 900000000.00 - gefunden: {gefunden}."
)
