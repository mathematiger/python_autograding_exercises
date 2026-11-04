# Automatisch erzeugt aus lehrkraft/muster/1_026_formulartest.py - nicht von Hand ändern.
# vorlage-hash: d2b74754e91924ae
# text-hash: 4bf16acd789961ba
# thema: kontrollfluss
# inhalt: Übung: Schleifen

EINGABEN = ["4", "75", "120", "90", "61"]


def erwartete_ausgabe(zeiten):
    """Baut die erwartete Ausgabe mit einer while-Schleife und ohne Zählvariable."""
    zeilen = []
    nummer = 1
    while nummer <= len(zeiten):
        sekunden = zeiten[nummer - 1]
        urteil = "in der Zeit" if sekunden <= 90 else "zu langsam"
        zeilen.append(f"Person {nummer}: {sekunden} Sekunden, {urteil}")
        nummer = nummer + 1
    schnelle = len([sekunden for sekunden in zeiten if sekunden <= 90])
    zeilen.append(f"{schnelle} von {len(zeiten)} Personen waren in der Zeit.")
    zeilen.append(f"Durchschnitt: {sum(zeiten) / len(zeiten):.1f} Sekunden")
    return "\n".join(zeilen)


def hinweis_zu(ausgabe, zeiten):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if "Person 0:" in ausgabe or f"Person {len(zeiten) + 1}:" in ausgabe:
        return "\nTipp: Die Personen werden ab 1 gezählt, bis einschließlich anzahl: range(1, anzahl + 1)."
    if 90 in zeiten and "90 Sekunden, zu langsam" in ausgabe:
        return "\nTipp: Genau 90 Sekunden sind noch in der Zeit; vergleichen Sie mit <= statt mit <."
    if f"0 von {len(zeiten)} Personen" in ausgabe and min(zeiten) <= 90:
        return "\nTipp: in_der_zeit = in_der_zeit + 1 gehört eingerückt unter das if."
    if "Durchschnitt: 0.0" in ausgabe:
        return "\nTipp: Addieren Sie in der Schleife jede Zeit zu gesamt: gesamt = gesamt + sekunden."
    return ""


def meldung(zeiten, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    eingaben = ", ".join([str(len(zeiten))] + [str(sekunden) for sekunden in zeiten])
    return (
        f"Bei den Eingaben {eingaben} erwartet:\n{erwartete_ausgabe(zeiten)}\nIhr Programm gibt aus:\n{ausgabe}"
        f"{hinweis_zu(ausgabe, zeiten)}"
    )


# Das Beispiel aus der Aufgabe: vier Personen
assert AUSGABE == erwartete_ausgabe([75, 120, 90, 61]), meldung([75, 120, 90, 61], AUSGABE)

# Andere Zeiten (nicht fest hinschreiben!)
ausgabe = starte("3", "200", "45", "91")
assert ausgabe == erwartete_ausgabe([200, 45, 91]), meldung([200, 45, 91], ausgabe)

# Genau 90 Sekunden sind noch in der Zeit, 91 nicht mehr
ausgabe = starte("2", "91", "90")
assert ausgabe == erwartete_ausgabe([91, 90]), meldung([91, 90], ausgabe)

# Eine einzige Person, die zu langsam ist
ausgabe = starte("1", "600")
assert ausgabe == erwartete_ausgabe([600]), meldung([600], ausgabe)

# Eine einzige Person, die ganz schnell ist
ausgabe = starte("1", "1")
assert ausgabe == erwartete_ausgabe([1]), meldung([1], ausgabe)

# Eine for-Schleife und ein if werden benutzt
assert verwendet("for") and verwendet("if"), "Benutzen Sie für diese Aufgabe eine for-Schleife und darin ein if."

# 40 zufällige Usability-Tests
zufall = Zufall(1026)
for _ in range(40):
    zeiten = [zufall.choice([zufall.randint(1, 600), zufall.randint(80, 100)]) for _ in range(zufall.randint(1, 10))]
    ausgabe = starte(str(len(zeiten)), *[str(sekunden) for sekunden in zeiten])
    assert ausgabe == erwartete_ausgabe(zeiten), meldung(zeiten, ausgabe)

# Obere Grenze: 30 Personen mit 1 bis 600 Sekunden
zeiten = [(nummer * 97) % 600 + 1 for nummer in range(30)]
ausgabe = starte("30", *[str(sekunden) for sekunden in zeiten])
assert ausgabe == erwartete_ausgabe(zeiten), meldung(zeiten, ausgabe)
