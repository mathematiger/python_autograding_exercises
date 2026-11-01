# Automatisch erzeugt aus lehrkraft/muster/4_018_abfragen.py - nicht von Hand ändern.
# vorlage-hash: 879ccf46ff900c90
# text-hash: a8f5bf506c16f84a
# thema: funktionen
# inhalt: `*args` und `**kwargs`

def neue_kunden():
    """Gibt eine frische Kopie der Beispieltabelle zurück."""
    return [
        {"nr": 1, "name": "Ada", "ort": "Paderborn", "aktiv": True},
        {"nr": 2, "name": "Alan", "ort": "Bielefeld", "aktiv": True},
        {"nr": 3, "name": "Grace", "ort": "Paderborn", "aktiv": False},
    ]


kunden = neue_kunden()

# waehle aus dem Beispiel: eine Spalte, eine Bedingung
ergebnis = waehle(kunden, "name", ort="Paderborn")
assert ergebnis == [{"name": "Ada"}, {"name": "Grace"}], (
    f"waehle(kunden, 'name', ort='Paderborn') ergibt {ergebnis!r}, erwartet war [{{'name': 'Ada'}}, {{'name': 'Grace'}}].\n"
    "Tipp: spalten ist ein Tupel der Spaltennamen, bedingungen ein Dictionary von Spalte auf Wert."
)

# Mehrere Spalten in der angegebenen Reihenfolge, mehrere Bedingungen zugleich
ergebnis = waehle(kunden, "name", "nr", ort="Paderborn", aktiv=True)
assert ergebnis == [{"name": "Ada", "nr": 1}] and list(ergebnis[0]) == ["name", "nr"], (
    f"waehle(kunden, 'name', 'nr', ort='Paderborn', aktiv=True) ergibt {ergebnis!r}, erwartet war "
    "[{'name': 'Ada', 'nr': 1}] mit den Spalten in der Reihenfolge name, nr.\n"
    "Tipp: Ein Datensatz passt nur, wenn alle Bedingungen erfüllt sind."
)

# Ohne Spaltenangabe alle Spalten
ergebnis = waehle(kunden, aktiv=False)
assert ergebnis == [{"nr": 3, "name": "Grace", "ort": "Paderborn", "aktiv": False}], (
    f"waehle(kunden, aktiv=False) ergibt {ergebnis!r}, erwartet war der ganze Datensatz von Grace.\n"
    "Tipp: Ist spalten leer, nehmen Sie alle Spalten des Datensatzes."
)

# Ohne Bedingungen passt jeder Datensatz
for argumente, erwartet in [
    (("nr",), [{"nr": 1}, {"nr": 2}, {"nr": 3}]),
    ((), neue_kunden()),
    (("ort", "nr"), [{"ort": "Paderborn", "nr": 1}, {"ort": "Bielefeld", "nr": 2}, {"ort": "Paderborn", "nr": 3}]),
]:
    ergebnis = waehle(kunden, *argumente)
    assert ergebnis == erwartet, f"waehle(kunden, {', '.join(map(repr, argumente))}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Keine Treffer und leere Tabelle
for tabelle, argumente, bedingungen, erwartet in [
    (kunden, ("name",), {"ort": "Berlin"}, []),
    (kunden, ("name",), {"ort": "Paderborn", "nr": 2}, []),
    ([], ("name",), {"ort": "Paderborn"}, []),
    ([], (), {}, []),
]:
    ergebnis = waehle(tabelle, *argumente, **bedingungen)
    assert ergebnis == erwartet, f"waehle({tabelle}, *{argumente}, **{bedingungen}) ergibt {ergebnis!r}, erwartet war []."

# Die Ergebnisse sind neue Dictionaries, die Tabelle bleibt unverändert
kunden = neue_kunden()
ergebnis = waehle(kunden, ort="Bielefeld")
ergebnis[0]["name"] = "geändert"
assert kunden == neue_kunden(), (
    "Nach waehle(kunden, ort='Bielefeld') und einer Änderung am Ergebnis hat sich auch die Tabelle kunden geändert.\n"
    "Tipp: Bauen Sie für jeden Treffer ein neues Dictionary, auch wenn alle Spalten gewählt sind."
)

# mit_protokoll aus dem Beispiel
kunden = neue_kunden()
protokoll = []
ergebnis = mit_protokoll(protokoll, waehle, kunden, "name", ort="Bielefeld")
assert ergebnis == [{"name": "Alan"}] and protokoll == ["waehle: 2 Positionsargumente, Schlüsselwörter: ort"], (
    f"mit_protokoll(protokoll, waehle, kunden, 'name', ort='Bielefeld') ergibt {ergebnis!r} und das Protokoll "
    f"{protokoll!r}; erwartet waren [{{'name': 'Alan'}}] und ['waehle: 2 Positionsargumente, Schlüsselwörter: ort'].\n"
    "Tipp: Reichen Sie mit funktion(*args, **kwargs) alles unverändert weiter."
)


def bericht(titel, *zeilen, trenner="-", breite=3):
    """Eine Beispielfunktion mit Standardwerten, an der mit_protokoll getestet wird."""
    return f"{titel}|{'|'.join(zeilen)}|{trenner * breite}"


# Schlüsselwörter in Aufrufreihenfolge, keine Schlüsselwörter, keine Positionsargumente
protokoll = []
ergebnisse = [
    mit_protokoll(protokoll, bericht, "T", "a", "b", breite=2, trenner="="),
    mit_protokoll(protokoll, bericht, "T"),
    mit_protokoll(protokoll, bericht, titel="X"),
]
erwartet_ergebnisse = ["T|a|b|==", "T||---", "X||---"]
erwartet_protokoll = [
    "bericht: 3 Positionsargumente, Schlüsselwörter: breite, trenner",
    "bericht: 1 Positionsargumente, Schlüsselwörter: keine",
    "bericht: 0 Positionsargumente, Schlüsselwörter: titel",
]
assert ergebnisse == erwartet_ergebnisse and protokoll == erwartet_protokoll, (
    f"Drei Aufrufe von mit_protokoll mit der Funktion bericht ergeben {ergebnisse!r} und das Protokoll\n{protokoll!r};\n"
    f"erwartet waren {erwartet_ergebnisse!r} und\n{erwartet_protokoll!r}.\n"
    "Tipp: Die Namen der Schlüsselwörter sind die Schlüssel von kwargs, ', '.join(kwargs) verbindet sie."
)

# Das Protokoll wird fortgeschrieben, nicht ersetzt
protokoll = ["alter Eintrag"]
mit_protokoll(protokoll, len, [1, 2, 3])
assert protokoll == ["alter Eintrag", "len: 1 Positionsargumente, Schlüsselwörter: keine"], (
    f"Nach mit_protokoll(protokoll, len, [1, 2, 3]) ist das Protokoll {protokoll!r}; erwartet war, dass der neue "
    "Eintrag an den alten angehängt wird."
)


def scheitert(wert):
    """Löst immer einen ValueError aus."""
    raise ValueError(f"kaputt: {wert}")


# Bei einer Ausnahme steht der Eintrag im Protokoll, und die Ausnahme kommt an
protokoll = []
try:
    mit_protokoll(protokoll, scheitert, wert=7)
    art = None
except Exception as fehler:
    art = f"{type(fehler).__name__}: {fehler}"
assert art == "ValueError: kaputt: 7" and protokoll == ["scheitert: 0 Positionsargumente, Schlüsselwörter: wert"], (
    f"mit_protokoll(protokoll, scheitert, wert=7) löst {art} aus, das Protokoll ist {protokoll!r}; erwartet waren "
    "ValueError: kaputt: 7 und der Eintrag 'scheitert: 0 Positionsargumente, Schlüsselwörter: wert'.\n"
    "Tipp: Schreiben Sie den Eintrag vor dem Aufruf und fangen Sie die Ausnahme nicht ab."
)


# Vergleichslösung: über die Indizes, Bedingungen einzeln
def waehle_von_hand(tabelle, spalten, bedingungen):
    """Prüft jede Bedingung mit einer Schleife und kopiert die gewünschten Spalten."""
    treffer = []
    for datensatz in tabelle:
        passt = True
        for spalte in bedingungen:
            if datensatz[spalte] != bedingungen[spalte]:
                passt = False
        if passt:
            neu = {}
            for spalte in spalten if spalten else list(datensatz.keys()):
                neu[spalte] = datensatz[spalte]
            treffer.append(neu)
    return treffer


# 300 zufällige Abfragen
zufall = Zufall(4018)
SPALTEN = ["nr", "ort", "aktiv", "stufe"]
for _ in range(300):
    tabelle = [
        {"nr": nummer, "ort": zufall.choice(["PB", "BI", "GT"]), "aktiv": zufall.choice([True, False]), "stufe": zufall.randint(0, 2)}
        for nummer in range(zufall.randint(0, 8))
    ]
    spalten = tuple(zufall.sample(SPALTEN, zufall.randint(0, 4)))
    bedingungen = {spalte: zufall.choice(["PB", "BI", True, False, 0, 1, 2]) for spalte in zufall.sample(SPALTEN[1:], zufall.randint(0, 3))}
    erwartet = waehle_von_hand(tabelle, spalten, bedingungen)
    protokoll = []
    ergebnis = mit_protokoll(protokoll, waehle, tabelle, *spalten, **bedingungen)
    eintrag = f"waehle: {1 + len(spalten)} Positionsargumente, Schlüsselwörter: {', '.join(bedingungen) or 'keine'}"
    assert ergebnis == erwartet and [list(d) for d in ergebnis] == [list(d) for d in erwartet], (
        f"waehle({tabelle}, *{spalten}, **{bedingungen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )
    assert protokoll == [eintrag], f"Das Protokoll ist {protokoll!r}, erwartet war {[eintrag]!r}."

# An der oberen Grenze: 100 000 Kunden
gross = [{"nr": nummer, "ort": ["PB", "BI", "GT", "HX"][nummer % 4], "aktiv": nummer % 3 == 0} for nummer in range(100000)]
ergebnis = waehle(gross, "nr", ort="HX", aktiv=True)
alle = waehle(gross)
assert len(ergebnis) == len(range(3, 100000, 12)) and ergebnis[:2] == [{"nr": 3}, {"nr": 15}] and len(alle) == 100000, (
    f"Bei 100 000 Kunden ergibt waehle(gross, 'nr', ort='HX', aktiv=True) {len(ergebnis)} Treffer, beginnend mit "
    f"{ergebnis[:2]}, und waehle(gross) {len(alle)}; erwartet waren {len(range(3, 100000, 12))} Treffer, beginnend "
    "mit [{'nr': 3}, {'nr': 15}], und 100000."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "[{'name': 'Ada'}, {'name': 'Grace'}]\n"
    "[{'name': 'Ada', 'nr': 1}]\n"
    "[{'name': 'Alan'}]\n"
    "['waehle: 2 Positionsargumente, Schlüsselwörter: ort']"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
