# Automatisch erzeugt aus lehrkraft/muster/1_046_tabellenspalte.py - nicht von Hand ändern.
# vorlage-hash: 8fa71d3fbc91c717
# text-hash: c06b799fce5788c5
# thema: datenstrukturen
# inhalt: Eintrag hinzufügen, .items()

EINGABEN = ["email", "TEXT"]

VORHER = {"id": "INTEGER", "name": "TEXT", "ort": "TEXT"}


def ausgabe_bei(spalte, typ):
    """Startet das Programm mit Spalte und Typ; ein Abbruch wird als Text zurückgegeben."""
    try:
        return starte(spalte, typ)
    except Exception as fehler:
        return f"(Abbruch: {type(fehler).__name__}: {fehler})"


def erwartet_bei(spalte, typ):
    """Die erwartete Ausgabe als Text."""
    tabelle = dict(VORHER)
    tabelle[spalte] = typ
    zeilen = ["Tabelle kunden:"] + [f"{name} {datentyp}" for name, datentyp in tabelle.items()]
    return "\n".join(zeilen)


def zeilen_von(ausgabe):
    """Die Zeilen der Ausgabe ohne leere Zeilen, jede vergleichbar gemacht."""
    return [vergleichbar(zeile) for zeile in ausgabe.splitlines() if zeile.strip()]


def meldung(spalte, typ, ausgabe):
    """Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    return f"Bei Eingabe {spalte} und {typ} erwartet:\n{erwartet_bei(spalte, typ)}\nIhr Programm:\n{ausgabe}"


# Die neue Spalte email steht in der Ausgabe
assert vergleichbar("email TEXT") in vergleichbar(AUSGABE), (
    meldung("email", "TEXT", AUSGABE) + "\nTipp: spalten[spalte] = typ trägt die neue Spalte ein."
)

# Die bisherigen Spalten stehen auch in der Ausgabe
fehlend = [f"{name} {datentyp}" for name, datentyp in VORHER.items() if vergleichbar(f"{name} {datentyp}") not in vergleichbar(AUSGABE)]
assert fehlend == [], (
    f"In der Ausgabe fehlen {fehlend}.\n{meldung('email', 'TEXT', AUSGABE)}\n"
    "Tipp: Gehen Sie mit for name, datentyp in spalten.items(): alle Einträge durch."
)

# Jede Spalte steht in einer eigenen Zeile, die neue zuletzt
assert zeilen_von(AUSGABE) == zeilen_von(erwartet_bei("email", "TEXT")), (
    meldung("email", "TEXT", AUSGABE) + "\nTipp: print(name, datentyp) in der Schleife gibt je Spalte eine Zeile aus; "
    "print(spalten) zeigt dagegen das ganze Dictionary auf einmal."
)

# Bei Eingabe kundennummer und INTEGER kommt diese Spalte dazu (nicht fest email hinschreiben!)
ausgabe = ausgabe_bei("kundennummer", "INTEGER")
assert zeilen_von(ausgabe) == zeilen_von(erwartet_bei("kundennummer", "INTEGER")), meldung("kundennummer", "INTEGER", ausgabe)

# Auch ein anderer Datentyp wird übernommen
ausgabe = ausgabe_bei("geburtstag", "DATE")
assert zeilen_von(ausgabe) == zeilen_von(erwartet_bei("geburtstag", "DATE")), meldung("geburtstag", "DATE", ausgabe)

# Eine vorhandene Spalte bekommt den neuen Datentyp und steht nicht doppelt da
ausgabe = ausgabe_bei("ort", "VARCHAR(50)")
assert zeilen_von(ausgabe) == zeilen_von(erwartet_bei("ort", "VARCHAR(50)")), (
    meldung("ort", "VARCHAR(50)", ausgabe) + "\nTipp: Gibt es den Schlüssel schon, ersetzt spalten[spalte] = typ nur den Wert; "
    "die Spalte bleibt an ihrer Stelle."
)

# Auch die erste Spalte lässt sich ändern
ausgabe = ausgabe_bei("id", "TEXT")
assert zeilen_von(ausgabe) == zeilen_von(erwartet_bei("id", "TEXT")), meldung("id", "TEXT", ausgabe)

# Viele zufällige Spalten und Datentypen
zufall = Zufall(1046)
namen = ["id", "name", "ort", "email", "plz", "telefon", "kundennummer", "rabatt", "land", "notiz"]
typen = ["INTEGER", "TEXT", "DATE", "REAL", "BOOLEAN", "VARCHAR(20)"]
for _ in range(30):
    spalte = zufall.choice(namen)
    typ = zufall.choice(typen)
    ausgabe = ausgabe_bei(spalte, typ)
    assert zeilen_von(ausgabe) == zeilen_von(erwartet_bei(spalte, typ)), meldung(spalte, typ, ausgabe)

# Genau so wie verlangt: Name, ein Leerzeichen, Datentyp (ohne Klammern und Anführungszeichen)
zeilen_genau = [zeile.strip() for zeile in AUSGABE.splitlines()]
assert "email TEXT" in zeilen_genau and "id INTEGER" in zeilen_genau, (
    f"Erwartet waren Zeilen wie \"id INTEGER\" und \"email TEXT\", Ihr Programm gibt aus:\n{AUSGABE}\n"
    "Tipp: for name, datentyp in spalten.items(): mit print(name, datentyp) gibt Name und Datentyp getrennt aus."
)
