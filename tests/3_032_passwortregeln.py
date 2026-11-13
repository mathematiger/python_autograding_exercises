# Automatisch erzeugt aus lehrkraft/muster/3_032_passwortregeln.py - nicht von Hand ändern.
# vorlage-hash: c99812482c31ef48
# text-hash: 858ee3c7a85e5f48
# thema: funktionen
# inhalt: Funktion baut Funktion

def ist_funktion(wert):
    """True, wenn man wert wie eine Funktion aufrufen kann."""
    return callable(wert)


# mindestlaenge liefert eine Funktion
regel = mindestlaenge(10)
assert ist_funktion(regel), (
    f"mindestlaenge(10) liefert {regel!r}, erwartet war eine Funktion.\n"
    "Tipp: Definieren Sie in mindestlaenge eine innere Funktion und geben Sie sie mit return zurück, ohne () dahinter."
)

# Das Beispiel aus der Aufgabe: "Sommer2024" hat 10 Zeichen, "kurz" nicht
regel = mindestlaenge(10)
assert regel("Sommer2024") is True and regel("kurz") is False, (
    f"Mit regel = mindestlaenge(10) ergibt regel('Sommer2024') {regel('Sommer2024')!r} und regel('kurz') "
    f"{regel('kurz')!r}, erwartet waren True und False."
)

# Genau anzahl Zeichen reichen, eines weniger nicht
regel = mindestlaenge(5)
assert regel("abcde") is True and regel("abcd") is False, (
    f"Mit regel = mindestlaenge(5) ergibt regel('abcde') {regel('abcde')!r} und regel('abcd') {regel('abcd')!r}, "
    "erwartet waren True und False.\nTipp: „Mindestens“ heißt >=."
)

# Zwei gebaute Regeln behalten jede ihre eigene Länge
kurz = mindestlaenge(4)
lang = mindestlaenge(12)
ergebnis = (kurz("Passwort"), lang("Passwort"))
assert ergebnis == (True, False), (
    "Nach kurz = mindestlaenge(4) und lang = mindestlaenge(12) ergibt kurz('Passwort'), lang('Passwort') "
    f"{ergebnis!r}, erwartet war (True, False).\n"
    "Tipp: Die innere Funktion soll den Parameter anzahl der äußeren benutzen, keine globale Variable."
)

# Mindestlänge 0: auch das leere Passwort reicht
regel = mindestlaenge(0)
assert regel("") is True, f"mindestlaenge(0)('') ergibt {regel('')!r}, erwartet war True."

# enthaelt_eines liefert eine Funktion
regel = enthaelt_eines("0123456789")
assert ist_funktion(regel), f"enthaelt_eines('0123456789') liefert {regel!r}, erwartet war eine Funktion."

# Das Beispiel aus der Aufgabe: Ziffer vorhanden oder nicht
regel = enthaelt_eines("0123456789")
assert regel("Sommer2024") is True and regel("ohneZiffer") is False, (
    f"Mit regel = enthaelt_eines('0123456789') ergibt regel('Sommer2024') {regel('Sommer2024')!r} und "
    f"regel('ohneZiffer') {regel('ohneZiffer')!r}, erwartet waren True und False."
)

# Ein einziges passendes Zeichen genügt, egal an welcher Stelle
regel = enthaelt_eines("!?#")
ergebnis = (regel("#abc"), regel("ab?c"), regel("abc!"), regel("abc"))
assert ergebnis == (True, True, True, False), (
    f"Mit regel = enthaelt_eines('!?#') ergeben '#abc', 'ab?c', 'abc!', 'abc' {ergebnis!r}, "
    "erwartet war (True, True, True, False).\n"
    "Tipp: Prüfen Sie jedes Zeichen aus zeichen einzeln, nicht den ganzen Text zeichen auf einmal."
)

# Das leere Passwort enthält keines der Zeichen
regel = enthaelt_eines("abc")
assert regel("") is False, f"enthaelt_eines('abc')('') ergibt {regel('')!r}, erwartet war False."

# Zwei gebaute Zeichenregeln stören sich nicht
gross = enthaelt_eines("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
klein = enthaelt_eines("abcdefghijklmnopqrstuvwxyz")
ergebnis = (gross("hallo"), klein("hallo"))
assert ergebnis == (False, True), (
    "Nach gross = enthaelt_eines(Großbuchstaben) und klein = enthaelt_eines(Kleinbuchstaben) ergeben "
    f"gross('hallo'), klein('hallo') {ergebnis!r}, erwartet war (False, True)."
)

# Das Beispiel aus der Aufgabe: verletzte_regeln
regeln = {"Länge": mindestlaenge(10), "Ziffer": enthaelt_eines("0123456789"), "Sonderzeichen": enthaelt_eines("!?#%&*")}
for passwort, erwartet in [("Sommer2024", ["Sonderzeichen"]), ("kurz!", ["Länge", "Ziffer"])]:
    ergebnis = verletzte_regeln(regeln, passwort)
    assert ergebnis == erwartet, (
        f"verletzte_regeln(regeln, {passwort!r}) mit den Regeln aus dem Beispiel ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Ein Passwort, das alle Regeln erfüllt, verletzt keine
ergebnis = verletzte_regeln(regeln, "Sommer2024!")
assert ergebnis == [], f"verletzte_regeln(regeln, 'Sommer2024!') ergibt {ergebnis!r}, erwartet war []."

# Ein leeres Passwort verletzt alle Regeln, in der Reihenfolge des Dictionarys
ergebnis = verletzte_regeln(regeln, "")
assert ergebnis == ["Länge", "Ziffer", "Sonderzeichen"], (
    f"verletzte_regeln(regeln, '') ergibt {ergebnis!r}, erwartet war ['Länge', 'Ziffer', 'Sonderzeichen']."
)

# Ohne Regeln ist nichts verletzt
ergebnis = verletzte_regeln({}, "egal")
assert ergebnis == [], f"verletzte_regeln({{}}, 'egal') ergibt {ergebnis!r}, erwartet war []."

# Auch fremde Prüffunktionen werden einfach aufgerufen
fremde = {"nicht nur Ziffern": lambda passwort: not passwort.isdigit(), "kein Leerzeichen": lambda passwort: " " not in passwort}
ergebnis = verletzte_regeln(fremde, "12 34")
assert ergebnis == ["kein Leerzeichen"], (
    f"verletzte_regeln mit den Regeln 'nicht nur Ziffern' und 'kein Leerzeichen' ergibt für '12 34' {ergebnis!r}, "
    "erwartet war ['kein Leerzeichen'].\nTipp: Rufen Sie jede Prüffunktion mit dem Passwort auf: regel(passwort)."
)

# Viele zufällige Richtlinien und Passwörter
zufall = Zufall(3032)
alphabet = "abcXYZ019!?# "
for _ in range(400):
    laengen = [zufall.randint(0, 12) for _ in range(zufall.randint(0, 3))]
    zeichensaetze = ["".join(zufall.choice(alphabet) for _ in range(zufall.randint(1, 4))) for _ in range(zufall.randint(0, 3))]
    regeln = {}
    erwartung = {}
    for nummer, anzahl in enumerate(laengen):
        regeln[f"Länge {nummer}"] = mindestlaenge(anzahl)
        erwartung[f"Länge {nummer}"] = ("länge", anzahl)
    for nummer, zeichen in enumerate(zeichensaetze):
        regeln[f"Zeichen {nummer}"] = enthaelt_eines(zeichen)
        erwartung[f"Zeichen {nummer}"] = ("zeichen", zeichen)
    passwort = "".join(zufall.choice(alphabet) for _ in range(zufall.randint(0, 14)))
    erwartet = []
    for name, (art, wert) in erwartung.items():
        erfuellt = len(passwort) >= wert if art == "länge" else bool(set(wert) & set(passwort))
        if not erfuellt:
            erwartet.append(name)
    ergebnis = verletzte_regeln(regeln, passwort)
    beschreibung = ", ".join(
        f"{name}: " + (f"mindestlaenge({wert})" if art == "länge" else f"enthaelt_eines({wert!r})")
        for name, (art, wert) in erwartung.items()
    )
    assert ergebnis == erwartet, (
        f"Regeln {{{beschreibung}}}, Passwort {passwort!r}: verletzte_regeln ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Obere Grenze: 20 Regeln, 100 Zeichen, Passwort mit 1000 Zeichen
regeln = {f"Länge {anzahl}": mindestlaenge(anzahl) for anzahl in range(0, 100, 10)}
for nummer in range(10):
    regeln[f"Zeichen {nummer}"] = enthaelt_eines("".join(chr(65 + nummer) for _ in range(100)))
passwort = "x" * 999 + "C"
erwartet = [f"Zeichen {nummer}" for nummer in range(10) if nummer != 2]
ergebnis = verletzte_regeln(regeln, passwort)
assert ergebnis == erwartet, (
    f"Mit 20 Regeln (Längen 0 bis 90, Zeichen A bis J) und dem Passwort 'x' * 999 + 'C' ergibt verletzte_regeln "
    f"{ergebnis!r}, erwartet war {erwartet!r}."
)
