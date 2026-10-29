# Automatisch erzeugt aus lehrkraft/muster/4_008_testfaelle.py - nicht von Hand ändern.
# vorlage-hash: 416575947501a4ef
# text-hash: 4af67f0414eec938
# thema: klassen
# inhalt: Klassenattribute als Zähler und Registry

# Die Nummern werden fortlaufend vergeben
Testfall.zuruecksetzen()
a = Testfall(1, "eins")
b = Testfall(2, "zwei")
c = Testfall(3, "drei")
nummern = (getattr(a, "nummer", None), getattr(b, "nummer", None), getattr(c, "nummer", None))
if nummern == ("TF001", "TF001", "TF001"):
    hinweis = (
        "\nTipp: Alle bekommen TF001. self.anzahl += 1 legt ein Attribut im Objekt an; "
        "zählen Sie mit Testfall.anzahl += 1."
    )
else:
    hinweis = ""
assert nummern == ("TF001", "TF002", "TF003"), (
    f"Nach zuruecksetzen() und drei Testfällen sind die Nummern {nummern!r}, "
    f'erwartet waren ("TF001", "TF002", "TF003").{hinweis}'
)

# Eingabe und erwartetes Ergebnis werden gespeichert
assert (b.eingabe, b.erwartet) == (2, "zwei"), (
    f'Testfall(2, "zwei") hat eingabe={getattr(b, "eingabe", None)!r} und erwartet={getattr(b, "erwartet", None)!r}, '
    'erwartet waren 2 und "zwei".'
)

# Der Zähler steht in der Klasse
assert Testfall.anzahl == 3, (
    f"Nach drei Testfällen ist Testfall.anzahl {Testfall.anzahl!r}, erwartet war 3.\n"
    "Tipp: Zählen Sie mit Testfall.anzahl += 1, nicht mit self.anzahl += 1."
)

# Die Objekte haben kein eigenes Attribut anzahl
assert "anzahl" not in vars(a), (
    "Das Objekt hat ein eigenes Attribut anzahl. Der Zähler soll nur in der Klasse stehen.\n"
    "Tipp: self.anzahl += 1 legt ein neues Attribut im Objekt an. Schreiben Sie Testfall.anzahl += 1."
)

# Alle Testfälle stehen unter ihrer Nummer im gemeinsamen Verzeichnis
assert Testfall.alle == {"TF001": a, "TF002": b, "TF003": c}, (
    f"Testfall.alle ist {Testfall.alle!r}, erwartet waren die drei Testfälle unter TF001, TF002 und TF003."
)

# finde liefert den Testfall zur Nummer
for nummer, erwartet in [("TF001", a), ("TF003", c)]:
    ergebnis = Testfall.finde(nummer)
    assert ergebnis is erwartet, f"Testfall.finde({nummer!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# finde liefert None für unbekannte Nummern
for nummer in ["TF004", "TF000", "XYZ"]:
    ergebnis = Testfall.finde(nummer)
    assert ergebnis is None, f"Testfall.finde({nummer!r}) ergibt {ergebnis!r}, erwartet war None."

# zuruecksetzen beginnt eine neue Testreihe bei TF001
Testfall.zuruecksetzen()
d = Testfall(10, 20)
assert (Testfall.anzahl, d.nummer, Testfall.alle) == (1, "TF001", {"TF001": d}), (
    f"Nach zuruecksetzen() und einem neuen Testfall sind anzahl={Testfall.anzahl!r}, nummer={d.nummer!r} "
    f"und alle={Testfall.alle!r}; erwartet waren 1, 'TF001' und nur dieser eine Testfall.\n"
    "Tipp: Setzen Sie in zuruecksetzen cls.anzahl auf 0 und leeren Sie cls.alle."
)

# Die Nummer ist immer dreistellig, auch ab dem zehnten Testfall
Testfall.zuruecksetzen()
for zahl in range(12):
    letzter = Testfall(zahl, zahl)
assert (letzter.nummer, Testfall.finde("TF010").eingabe) == ("TF012", 9), (
    f"Nach zwölf Testfällen hat der letzte die Nummer {letzter.nummer!r}, erwartet war 'TF012'; "
    "TF010 muss der zehnte Testfall sein.\n"
    'Tipp: f"TF{zahl:03d}" schreibt die Zahl dreistellig mit führenden Nullen.'
)


def verdoppeln_falsch(zahl):
    """Verdoppelt richtig, außer bei 3 und 0."""
    if zahl in (3, 0):
        return -1
    return 2 * zahl


Testfall.zuruecksetzen()
for zahl in [5, 3, 1, 0, 7]:
    Testfall(zahl, 2 * zahl)

# Fehlgeschlagene Testfälle werden in der Reihenfolge der Anlage gemeldet
ergebnis = Testfall.fehlgeschlagen(verdoppeln_falsch)
assert ergebnis == ["TF002", "TF004"], (
    f"Testfall.fehlgeschlagen(...) ergibt {ergebnis!r}, erwartet war ['TF002', 'TF004'] "
    "(die Eingaben 3 und 0 werden falsch verdoppelt)."
)

# Eine fehlerfreie Funktion besteht alle Testfälle
ergebnis = Testfall.fehlgeschlagen(lambda zahl: zahl + zahl)
assert ergebnis == [], f"Bei einer richtigen Funktion ergibt Testfall.fehlgeschlagen(...) {ergebnis!r}, erwartet war []."

# Ohne Testfälle schlägt nichts fehl
Testfall.zuruecksetzen()
ergebnis = Testfall.fehlgeschlagen(verdoppeln_falsch)
assert ergebnis == [], f"Ohne Testfälle ergibt Testfall.fehlgeschlagen(...) {ergebnis!r}, erwartet war []."

# Obere Grenze: 999 Testfälle in einer Testreihe
Testfall.zuruecksetzen()
for zahl in range(999):
    letzter = Testfall(zahl, 2 * zahl)
gefunden = Testfall.finde("TF999")
assert (Testfall.anzahl, letzter.nummer, len(Testfall.alle), gefunden is letzter) == (999, "TF999", 999, True), (
    "Nach 999 Testfällen erwartet anzahl 999, letzte Nummer 'TF999', 999 Einträge in alle und finde('TF999') "
    f"liefert den letzten; bekommen {Testfall.anzahl!r}, {letzter.nummer!r}, {len(Testfall.alle)} und {gefunden!r}."
)

# Viele zufällige Testreihen: Zähler, Nummern und fehlgeschlagene Fälle stimmen
zufall = Zufall(4008)
fehlerfall = None
for versuch in range(200):
    Testfall.zuruecksetzen()
    eingaben = [zufall.randint(-50, 50) for _ in range(versuch // 5)]  # erst kurze Reihen, damit die Meldung klein bleibt
    falsch = set()
    for position, zahl in enumerate(eingaben, start=1):
        if zufall.random() < 0.3:
            Testfall(zahl, 2 * zahl + 1)
            falsch.add(position)
        else:
            Testfall(zahl, 2 * zahl)
    erwartet = (len(eingaben), [f"TF{position:03d}" for position in range(1, len(eingaben) + 1)],
                [f"TF{position:03d}" for position in sorted(falsch)])
    bekommen = (Testfall.anzahl, list(Testfall.alle), Testfall.fehlgeschlagen(lambda zahl: zahl * 2))
    if bekommen != erwartet:
        fehlerfall = (eingaben, sorted(falsch), erwartet, bekommen)
        break
assert fehlerfall is None, (
    f"Nach zuruecksetzen() und Testfällen mit den Eingaben {fehlerfall[0]} (falsch erwartet an den Stellen {fehlerfall[1]}) "
    f"ergeben (anzahl, Nummern in alle, fehlgeschlagen(verdoppeln))\n{fehlerfall[3]}\nerwartet war\n{fehlerfall[2]}"
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "4 Testfälle: [Testfall('TF001', 0 → 4.9), Testfall('TF002', 1999 → 4.9), "
    "Testfall('TF003', 2000 → 4.9), Testfall('TF004', 2001 → 6.9)]\n"
    "Fehlgeschlagen: ['TF003']"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
