# Automatisch erzeugt aus lehrkraft/muster/4_008_testfaelle.py - nicht von Hand ändern.
# vorlage-hash: 143d9560373f6e6e

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

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "4 Testfälle: [Testfall('TF001', 0 → 4.9), Testfall('TF002', 1999 → 4.9), "
    "Testfall('TF003', 2000 → 4.9), Testfall('TF004', 2001 → 6.9)]\n"
    "Fehlgeschlagen: ['TF003']"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
