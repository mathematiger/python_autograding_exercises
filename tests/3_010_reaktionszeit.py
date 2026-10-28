# Automatisch erzeugt aus lehrkraft/muster/3_010_reaktionszeit.py - nicht von Hand ändern.
# vorlage-hash: 4fd00dab5125d313
# thema: fehler
# inhalt: `assert` als Vertrag

# Das Beispiel aus der Aufgabe: Priorität 1 nach 20 Minuten
ergebnis = restzeit(1, 20)
assert ergebnis == 40, f"restzeit(1, 20) ergibt {ergebnis!r}, erwartet war 40."

# Restzeit für alle Prioritäten, auch überschritten (nicht fest hinschreiben!)
for prioritaet, vergangen, erwartet in [(1, 0, 60), (1, 60, 0), (1, 75, -15), (2, 100, 140), (2, 300, -60), (3, 1, 479), (3, 480, 0)]:
    ergebnis = restzeit(prioritaet, vergangen)
    assert ergebnis == erwartet, (
        f"restzeit({prioritaet}, {vergangen}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Reaktionszeit der Priorität minus vergangene Minuten."
    )

# Unbekannte Prioritäten lösen einen AssertionError mit der Priorität in der Meldung aus
for prioritaet in [0, 4, -1, 10]:
    try:
        restzeit(prioritaet, 20)
        fehler = None
    except Exception as ausnahme:
        fehler = ausnahme
    assert isinstance(fehler, AssertionError) and str(fehler) == f"Unbekannte Priorität: {prioritaet}", (
        f'restzeit({prioritaet}, 20) muss einen AssertionError mit der Meldung "Unbekannte Priorität: {prioritaet}" '
        f"auslösen; Ausnahme: {fehler!r}.\n"
        'Tipp: assert prioritaet in REAKTIONSZEIT, f"Unbekannte Priorität: {prioritaet}" löst einen AssertionError aus, '
        "raise ValueError(...) dagegen einen ValueError."
    )

# Eine negative Zeit löst einen AssertionError aus
for vergangen in [-1, -30]:
    try:
        restzeit(2, vergangen)
        fehler = None
    except Exception as ausnahme:
        fehler = ausnahme
    assert isinstance(fehler, AssertionError) and str(fehler) == "Die vergangene Zeit darf nicht negativ sein", (
        f'restzeit(2, {vergangen}) muss einen AssertionError mit der Meldung "Die vergangene Zeit darf nicht negativ sein" '
        f"auslösen; Ausnahme: {fehler!r}."
    )

# Null Minuten sind erlaubt
try:
    ergebnis = restzeit(3, 0)
except AssertionError as ausnahme:
    ergebnis = ausnahme
assert ergebnis == 480, (
    f"restzeit(3, 0) ergibt {ergebnis!r}, erwartet war 480.\n"
    "Tipp: Verboten ist nur eine negative Zeit; ein gerade eingegangenes Ticket hat 0 Minuten."
)

# Die Ampel aus dem Beispiel
for prioritaet, vergangen, erwartet in [(1, 20, "grün"), (1, 30, "gelb"), (1, 60, "rot")]:
    ergebnis = ampel(prioritaet, vergangen)
    assert ergebnis == erwartet, f"ampel({prioritaet}, {vergangen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Die Ampel an den Grenzen und für andere Prioritäten
for prioritaet, vergangen, erwartet in [
    (1, 0, "grün"),
    (1, 29, "grün"),
    (1, 59, "gelb"),
    (1, 90, "rot"),
    (2, 119, "grün"),
    (2, 120, "gelb"),
    (2, 239, "gelb"),
    (2, 240, "rot"),
    (3, 239, "grün"),
    (3, 240, "gelb"),
    (3, 481, "rot"),
]:
    ergebnis = ampel(prioritaet, vergangen)
    assert ergebnis == erwartet, (
        f"ampel({prioritaet}, {vergangen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Grün nur bei mehr als der Hälfte, gelb bei höchstens der Hälfte, rot ab 0 Minuten Restzeit."
    )

# Auch ampel meldet Programmierfehler, weil sie restzeit benutzt
try:
    ampel(5, 10)
    fehler = None
except Exception as ausnahme:
    fehler = ausnahme
assert isinstance(fehler, AssertionError) and str(fehler) == "Unbekannte Priorität: 5", (
    f'ampel(5, 10) muss einen AssertionError mit der Meldung "Unbekannte Priorität: 5" auslösen; Ausnahme: {fehler!r}.\n'
    "Tipp: Rufen Sie in ampel die Funktion restzeit auf, statt neu zu rechnen."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "Priorität 1 nach 20 Minuten: 40 Minuten übrig, grün\n"
    "Priorität 2 nach 150 Minuten: 90 Minuten übrig, gelb\n"
    "Priorität 3 nach 500 Minuten: -20 Minuten übrig, rot"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
