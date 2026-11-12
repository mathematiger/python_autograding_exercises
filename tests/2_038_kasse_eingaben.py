# Automatisch erzeugt aus lehrkraft/muster/2_038_kasse_eingaben.py - nicht von Hand ändern.
# vorlage-hash: ffe1f97b28b9114d
# text-hash: 67aaa6b8aa33889e
# thema: fehler
# inhalt: Eingaben prüfen und wiederholen

EINGABEN = ["0"]

MENUE = """==============================
          TECH-SHOP
==============================
1 – Einkauf bearbeiten
2 – Preisanfrage berechnen
0 – Programm beenden"""


def rufe_auf(funktion, *argumente, eingaben=()):
    """Ruft funktion(*argumente) mit vorgegebenen Eingaben auf.

    Liefert Rückgabewert, Ausgabe, die Aufforderungen aller input-Aufrufe und eine Ausnahme (sonst None).
    """
    global print, input
    ausgabe = []
    fragen = []
    rest = list(eingaben)

    def merke(*werte, sep=" ", end="\n", **_):
        """Wie print, merkt sich die Ausgabe aber nur."""
        ausgabe.append(sep.join(str(wert) for wert in werte) + end)

    def antworte(aufforderung=""):
        """Wie input, liefert aber die nächste vorgegebene Eingabe."""
        fragen.append(aufforderung)
        if not rest:
            raise EOFError("Die Funktion fragt öfter nach einer Eingabe, als der Test vorsieht.")
        return rest.pop(0)

    altes_print, altes_input = print, input
    print, input = merke, antworte
    try:
        ergebnis, fehler = funktion(*argumente), None
    except Exception as ausnahme:
        ergebnis, fehler = None, ausnahme
    finally:
        print, input = altes_print, altes_input
    return ergebnis, "".join(ausgabe), fragen, fehler


def meldung_lesen(name, eingaben, ergebnis, fragen, fehler, erwartet):
    """Baut die Meldung für lies_einzelpreis/lies_anzahl: Absturz, zu oft/zu selten gefragt oder falscher Wert."""
    aufruf = f"{name}(...) mit den Eingaben {list(eingaben)}"
    if isinstance(fehler, ValueError):
        return (
            f"{aufruf} ist mit ValueError abgestürzt ({fehler}), erwartet war {erwartet!r}.\n"
            "Tipp: Wandeln Sie den Text in einem try-Block um und fangen Sie den Fehler mit except ValueError: ab."
        )
    if isinstance(fehler, EOFError):
        return (
            f"{aufruf} hat {len(fragen)}-mal gefragt und keine Zahl zurückgegeben, erwartet war {erwartet!r} nach "
            f"der {len(eingaben)}. Eingabe.\nTipp: Geben Sie die Zahl mit return zurück, sobald sie gültig ist."
        )
    if fehler is not None:
        return f"{aufruf} ist mit {type(fehler).__name__}: {fehler} abgestürzt, erwartet war {erwartet!r}."
    text = f"{aufruf} ergibt {ergebnis!r} nach {len(fragen)} Fragen, erwartet war {erwartet!r} nach {len(eingaben)}."
    if len(fragen) < len(eingaben):
        text = text + "\nTipp: Nur eine gültige Zahl beendet die Schleife; ungültige führen zur nächsten Frage."
    return text


def ungefaehr(ergebnis, erwartet):
    """Prüft, ob ergebnis eine Zahl ist, die bis auf Rundungsfehler erwartet ist."""
    return isinstance(ergebnis, (int, float)) and abs(ergebnis - erwartet) < 1e-6


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


def starte_sicher(*eingaben):
    """Wie starte, liefert bei einem Absturz aber die Meldung statt der Ausgabe."""
    try:
        return starte(*eingaben), None
    except Exception as ausnahme:
        return "", str(ausnahme)


def von_hand(positionen):
    """Vergleichslösung in Cent: liefert Gesamtbetrag, Rabatt und Endbetrag eines Einkaufs in Euro."""
    gesamt_cent = 0
    for _, cent, menge in positionen:
        gesamt_cent = gesamt_cent + cent * menge
    rabatt_cent = gesamt_cent / 10 if gesamt_cent >= 5000 else 0
    return gesamt_cent / 100, rabatt_cent / 100, (gesamt_cent - rabatt_cent) / 100


def mit_fehlern(richtig, falsche, zufall):
    """Liefert die Eingaben für eine Frage: null bis zwei zufällige falsche, dann die richtige."""
    eingaben = []
    for _ in range(zufall.randint(0, 2)):
        eingaben.append(zufall.choice(falsche))
    return eingaben + [richtig]


# lies_einzelpreis: eine gültige Eingabe wird sofort als Zahl zurückgegeben
eingaben = ["15"]
ergebnis, _, fragen, fehler = rufe_auf(lies_einzelpreis, "Einzelpreis: ", eingaben=eingaben)
assert fehler is None and ungefaehr(ergebnis, 15) and len(fragen) == 1, meldung_lesen(
    "lies_einzelpreis", eingaben, ergebnis, fragen, fehler, 15.0
)

# lies_einzelpreis fragt mit der übergebenen Aufforderung
_, _, fragen, _ = rufe_auf(lies_einzelpreis, "Einzelpreis: ", eingaben=["15"])
assert fragen == ["Einzelpreis: "], (
    f'lies_einzelpreis("Einzelpreis: ") fragt mit {fragen!r}, erwartet war ["Einzelpreis: "].\n'
    "Tipp: Geben Sie den Parameter an input weiter: input(aufforderung)."
)

# lies_einzelpreis gibt einen float zurück, auch bei 8.5
eingaben = ["8.5"]
ergebnis, _, fragen, fehler = rufe_auf(lies_einzelpreis, "Preis: ", eingaben=eingaben)
assert fehler is None and ungefaehr(ergebnis, 8.5), meldung_lesen("lies_einzelpreis", eingaben, ergebnis, fragen, fehler, 8.5)

# lies_einzelpreis: Buchstaben als Preis führen zu einer Meldung und einer neuen Frage
eingaben = ["acht", "8.5"]
ergebnis, ausgabe, fragen, fehler = rufe_auf(lies_einzelpreis, "Preis: ", eingaben=eingaben)
assert fehler is None and ungefaehr(ergebnis, 8.5) and len(fragen) == 2, meldung_lesen(
    "lies_einzelpreis", eingaben, ergebnis, fragen, fehler, 8.5
)

# lies_einzelpreis: Bei Buchstaben erscheint eine Meldung
assert ausgabe.strip() != "", (
    f"lies_einzelpreis(...) mit den Eingaben {eingaben} gibt nichts aus. Erwartet war eine Meldung, dass „acht“ "
    "keine Zahl ist.\nTipp: Geben Sie im except-Block mit print eine Meldung aus."
)

# lies_einzelpreis: 0 und negative Preise werden abgelehnt
eingaben = ["0", "-3", "12.99"]
ergebnis, ausgabe, fragen, fehler = rufe_auf(lies_einzelpreis, "Preis: ", eingaben=eingaben)
assert fehler is None and ungefaehr(ergebnis, 12.99) and len(fragen) == 3 and len(ausgabe.strip().splitlines()) >= 2, (
    meldung_lesen("lies_einzelpreis", eingaben, ergebnis, fragen, fehler, 12.99)
    + f"\nAusgabe:\n{ausgabe}\nTipp: Prüfen Sie nach der Umwandlung mit if, ob der Preis größer als 0 ist, und "
    "geben Sie sonst eine Meldung aus."
)

# lies_anzahl: eine gültige Eingabe wird sofort als int zurückgegeben
eingaben = ["3"]
ergebnis, _, fragen, fehler = rufe_auf(lies_anzahl, "Menge: ", eingaben=eingaben)
assert fehler is None and ergebnis == 3 and type(ergebnis) is int and fragen == ["Menge: "], (
    meldung_lesen("lies_anzahl", eingaben, ergebnis, fragen, fehler, 3)
    + "\nTipp: lies_anzahl wandelt mit int(...) um und fragt mit input(aufforderung)."
)

# lies_anzahl: Buchstaben führen zu einer Meldung und einer neuen Frage
eingaben = ["zwei", "2"]
ergebnis, ausgabe, fragen, fehler = rufe_auf(lies_anzahl, "Menge: ", eingaben=eingaben)
assert fehler is None and ergebnis == 2 and len(fragen) == 2 and ausgabe.strip() != "", (
    meldung_lesen("lies_anzahl", eingaben, ergebnis, fragen, fehler, 2) + f"\nAusgabe:\n{ausgabe}"
)

# lies_anzahl: 0 als Menge wird abgelehnt
eingaben = ["0", "4"]
ergebnis, ausgabe, fragen, fehler = rufe_auf(lies_anzahl, "Menge: ", eingaben=eingaben)
assert fehler is None and ergebnis == 4 and len(fragen) == 2 and ausgabe.strip() != "", (
    meldung_lesen("lies_anzahl", eingaben, ergebnis, fragen, fehler, 4)
    + f"\nAusgabe:\n{ausgabe}\nTipp: 0 lässt sich umwandeln; prüfen Sie danach mit if, ob die Zahl größer als 0 ist."
)

# lies_anzahl: negative Zahlen und Kommazahlen werden abgelehnt
eingaben = ["-2", "2.5", "1"]
ergebnis, ausgabe, fragen, fehler = rufe_auf(lies_anzahl, "Anzahl: ", eingaben=eingaben)
assert fehler is None and ergebnis == 1 and len(fragen) == 3 and len(ausgabe.strip().splitlines()) >= 2, (
    meldung_lesen("lies_anzahl", eingaben, ergebnis, fragen, fehler, 1) + f"\nAusgabe:\n{ausgabe}"
)

# Die Rechenfunktionen aus 2_037
fehlerhaft = []
for aufruf, ergebnis, erwartet in [
    ("berechne_positionsbetrag(8.5, 3)", rufe_auf(berechne_positionsbetrag, 8.5, 3)[0], 25.5),
    ("berechne_rabatt(54.0)", rufe_auf(berechne_rabatt, 54.0)[0], 5.4),
    ("berechne_rabatt(50.0)", rufe_auf(berechne_rabatt, 50.0)[0], 5.0),
    ("berechne_rabatt(49.99)", rufe_auf(berechne_rabatt, 49.99)[0], 0),
    ("berechne_endbetrag(54.0, 5.4)", rufe_auf(berechne_endbetrag, 54.0, 5.4)[0], 48.6),
]:
    if not ungefaehr(ergebnis, erwartet):
        fehlerhaft.append(f"{aufruf} ergibt {ergebnis!r}, erwartet war {erwartet!r}")
assert fehlerhaft == [], (
    "\n".join(fehlerhaft) + "\nTipp: Die Regeln stehen in Aufgabe 2_037; dort gibt es zu jeder Funktion einen "
    "eigenen Test."
)

# Beim Start erscheint das Menü
assert vergleichbar(MENUE) in vergleichbar(AUSGABE), f"Beim Start erwartet:\n{MENUE}\nIhr Programm gibt aus:\n{AUSGABE}"

# Ein Einkauf mit gültigen Eingaben wie in 2_037: 3 USB-Kabel zu je 8 € und 2 Mäuse zu je 15 €
eingaben = ["1", "2", "USB-Kabel", "8", "3", "Maus", "15", "2", "0"]
ausgabe, absturz = starte_sicher(*eingaben)
gefunden = betraege(ausgabe, "Gesamtbetrag") + betraege(ausgabe, "Rabatt") + betraege(ausgabe, "Endbetrag")
assert absturz is None and gefunden == ["54.00", "5.40", "48.60"], (
    absturz or meldung_lauf(eingaben, ausgabe, "Gesamtbetrag“, „Rabatt“ und „Endbetrag", gefunden, [54, 5.4, 48.6])
)

# Eine Preisanfrage mit gültigen Eingaben wie in 2_037: 10 USB-Kabel zu je 8 €
eingaben = ["2", "USB-Kabel", "8", "10", "0"]
ausgabe, absturz = starte_sicher(*eingaben)
gefunden = betraege(ausgabe, "Rabatt") + betraege(ausgabe, "Angebotspreis")
assert absturz is None and gefunden == ["8.00", "72.00"], (
    absturz or meldung_lauf(eingaben, ausgabe, "Rabatt“ und „Angebotspreis", gefunden, [8, 72])
)

# Die Preisanfrage zeigt Überschrift und Position mit zeige_artikel wie in 2_037
assert vergleichbar("Unverbindliches Preisangebot") in vergleichbar(ausgabe) and "80.00" in ausgabe, (
    f"Mit den Eingaben {eingaben} erwartet: die Überschrift „Unverbindliches Preisangebot“ und die Position "
    f"mit 80.00 € von zeige_artikel. Ihr Programm gibt aus:\n{ausgabe}"
)

# Der Einkauf zeigt jede Position mit zeige_artikel wie in 2_037
eingaben = ["1", "2", "USB-Kabel", "8", "3", "Maus", "15", "2", "0"]
ausgabe, absturz = starte_sicher(*eingaben)
assert absturz is None and "USB-Kabel" in ausgabe and "8.00" in ausgabe and "24.00" in ausgabe and "Maus" in ausgabe, (
    absturz
    or f"Mit den Eingaben {eingaben} erwartet: die Positionen USB-Kabel (3 x 8.00 € = 24.00 €) und Maus von "
    f"zeige_artikel. Ihr Programm gibt aus:\n{ausgabe}"
)

# Buchstaben als Preis beenden das Programm nicht
eingaben = ["1", "1", "Maus", "acht", "15", "2", "0"]
ausgabe, absturz = starte_sicher(*eingaben)
gefunden = betraege(ausgabe, "Endbetrag")
assert absturz is None and passt(gefunden, [30]), (
    f"{absturz}\nTipp: Lesen Sie den Einzelpreis mit lies_einzelpreis ein statt mit float(input(...))."
    if absturz
    else meldung_lauf(eingaben, ausgabe, "Endbetrag", gefunden, [30])
)

# 0 als Menge beendet das Programm nicht
eingaben = ["1", "1", "Maus", "15", "0", "2", "0"]
ausgabe, absturz = starte_sicher(*eingaben)
gefunden = betraege(ausgabe, "Endbetrag")
assert absturz is None and passt(gefunden, [30]), (
    f"{absturz}\nTipp: Lesen Sie die Menge mit lies_anzahl ein, dann wird 0 abgelehnt und noch einmal gefragt."
    if absturz
    else meldung_lauf(eingaben, ausgabe, "Endbetrag", gefunden, [30])
)

# Eine negative Anzahl an Artikelpositionen beendet das Programm nicht
eingaben = ["1", "-2", "1", "Maus", "15", "2", "0"]
ausgabe, absturz = starte_sicher(*eingaben)
gefunden = betraege(ausgabe, "Endbetrag")
assert absturz is None and passt(gefunden, [30]), (
    f"{absturz}\nTipp: Lesen Sie auch die Anzahl der Positionen mit lies_anzahl ein."
    if absturz
    else meldung_lauf(eingaben, ausgabe, "Endbetrag", gefunden, [30])
)

# Das Beispiel aus der Aufgabe: drei Fehler in einem Einkauf
eingaben = ["1", "-2", "1", "Maus", "acht", "15", "0", "2", "0"]
ausgabe, absturz = starte_sicher(*eingaben)
gefunden = betraege(ausgabe, "Gesamtbetrag") + betraege(ausgabe, "Rabatt") + betraege(ausgabe, "Endbetrag")
assert absturz is None and gefunden == ["30.00", "0.00", "30.00"], (
    absturz or meldung_lauf(eingaben, ausgabe, "Gesamtbetrag“, „Rabatt“ und „Endbetrag", gefunden, [30, 0, 30])
)

# Auch die Preisanfrage prüft Preis und Menge
eingaben = ["2", "USB-Kabel", "-8", "8", "zehn", "10", "0"]
ausgabe, absturz = starte_sicher(*eingaben)
gefunden = betraege(ausgabe, "Rabatt") + betraege(ausgabe, "Angebotspreis")
assert absturz is None and passt(gefunden, [8, 72]), (
    f"{absturz}\nTipp: Benutzen Sie lies_einzelpreis und lies_anzahl auch im Zweig für die Preisanfrage."
    if absturz
    else meldung_lauf(eingaben, ausgabe, "Rabatt“ und „Angebotspreis", gefunden, [8, 72])
)

# Eine ungültige Menüauswahl gibt einen Hinweis und zeigt das Menü erneut
nur_ende = vergleichbar(starte_sicher("0")[0]).replace(vergleichbar(MENUE), "")
ausgabe, absturz = starte_sicher("abc", "0")
rest = vergleichbar(ausgabe).replace(vergleichbar(MENUE), "")
assert absturz is None and vergleichbar(ausgabe).count(vergleichbar(MENUE)) == 2 and len(rest) > len(nur_ende), (
    absturz or f"Mit den Eingaben ['abc', '0'] erwartet: Menü, ein Hinweis, Menü. Ihr Programm gibt aus:\n{ausgabe}"
)

# Das Hauptprogramm benutzt lies_einzelpreis und lies_anzahl, die Funktionen fangen den ValueError ab
assert verwendet("lies_einzelpreis") and verwendet("lies_anzahl") and verwendet("try"), (
    "Rufen Sie lies_einzelpreis und lies_anzahl im Hauptprogramm auf und fangen Sie in ihnen den ValueError mit "
    "try/except ab."
)

# 150 zufällige Einkäufe mit falschen Eingaben dazwischen
zufall = Zufall(2038)
namen = ["Maus", "Tastatur", "USB-Kabel", "Monitor", "SSD", "Headset", "Webcam"]
falsche_preise = ["", "acht", "8,50", "-1", "0", "-0.5", "1e", "€"]
falsche_anzahlen = ["", "zwei", "2.5", "-3", "0", "1,0", "x"]
for _ in range(150):
    positionen = []
    for _ in range(zufall.randint(1, 4)):
        positionen.append((zufall.choice(namen), zufall.randint(1, 4000), zufall.randint(1, 5)))
    gesamt, rabatt, end = von_hand(positionen)
    if gesamt == 50:
        # Genau 50 € prüft 2_037; hier könnte die Summe der Kommazahlen knapp daneben liegen.
        continue
    eingaben = ["1"] + mit_fehlern(str(len(positionen)), falsche_anzahlen, zufall)
    for name, cent, menge in positionen:
        preis = str(cent // 100) if cent % 100 == 0 else f"{cent / 100:.2f}"
        eingaben = eingaben + [name] + mit_fehlern(preis, falsche_preise, zufall)
        eingaben = eingaben + mit_fehlern(str(menge), falsche_anzahlen, zufall)
    eingaben.append("0")
    ausgabe, absturz = starte_sicher(*eingaben)
    gefunden = betraege(ausgabe, "Gesamtbetrag") + betraege(ausgabe, "Rabatt") + betraege(ausgabe, "Endbetrag")
    assert absturz is None and passt(gefunden, [gesamt, rabatt, end]), absturz or meldung_lauf(
        eingaben, ausgabe, "Gesamtbetrag“, „Rabatt“ und „Endbetrag", gefunden, [gesamt, rabatt, end]
    )

# An der oberen Grenze: 100 Positionen mit je 1000 Stück zu 10 000 €, jede mit einer falschen Menge davor
eingaben = ["1", "100"]
for nummer in range(100):
    eingaben = eingaben + [f"Server {nummer}", "10000", "0", "1000"]
eingaben.append("0")
ausgabe, absturz = starte_sicher(*eingaben)
gefunden = betraege(ausgabe, "Endbetrag")
assert absturz is None and passt(gefunden, [900_000_000]), (
    absturz
    or f"Bei 100 Positionen mit je 1000 Stück zu 10 000 € erwartet: Endbetrag 900000000.00 - gefunden: {gefunden}."
)
