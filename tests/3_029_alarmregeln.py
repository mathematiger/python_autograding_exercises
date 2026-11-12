# Automatisch erzeugt aus lehrkraft/muster/3_029_alarmregeln.py - nicht von Hand ändern.
# vorlage-hash: f560d30b4cc455ce
# text-hash: caf6767e50247bdb
# thema: fehler
# inhalt: Ausnahmen über Funktionen hinweg

def float_meldung(text):
    """Gibt die Meldung zurück, die float(text) bei einem ungültigen Text ausgibt."""
    try:
        float(text)
    except ValueError as ausnahme:
        return str(ausnahme)
    return None


def ergebnis_von_lies_regel(zeile):
    """Ruft lies_regel auf und gibt (Ergebnis, Ausnahme) zurück; eine davon ist None."""
    try:
        return lies_regel(zeile), None
    except Exception as ausnahme:
        return None, ausnahme


def vergleichbare_meldungen(ergebnis):
    """Macht in (regeln, meldungen) die Meldungen mit vergleichbar unempfindlich gegen die Schreibweise; die Regeln bleiben."""
    if not (isinstance(ergebnis, tuple) and len(ergebnis) == 2 and isinstance(ergebnis[1], list)):
        return ergebnis
    return ergebnis[0], [vergleichbar(meldung) if isinstance(meldung, str) else meldung for meldung in ergebnis[1]]


# lies_regel aus dem Beispiel
for zeile, erwartet in [("cpu > 90", ("cpu", ">", 90.0))]:
    ergebnis, ausnahme = ergebnis_von_lies_regel(zeile)
    assert ausnahme is None and ergebnis == erwartet and isinstance(ergebnis[2], float), (
        f"lies_regel({zeile!r}) ergibt {ergebnis!r} (Ausnahme: {ausnahme!r}), erwartet war {erwartet!r}.\n"
        "Tipp: split() ohne Argument trennt an beliebig vielen Leerzeichen; float(...) wandelt den Schwellwert um."
    )

# Weitere richtige Regeln, der Schwellwert ist eine Kommazahl
for zeile, erwartet in [
    ("temperatur > 75.5", ("temperatur", ">", 75.5)),
    ("festplatte < 10", ("festplatte", "<", 10.0)),
    ("temperatur < -5", ("temperatur", "<", -5.0)),
]:
    ergebnis, ausnahme = ergebnis_von_lies_regel(zeile)
    assert ausnahme is None and ergebnis == erwartet and isinstance(ergebnis[2], float), (
        f"lies_regel({zeile!r}) ergibt {ergebnis!r} (Ausnahme: {ausnahme!r}), erwartet war {erwartet!r}.\n"
        "Tipp: split() ohne Argument trennt an beliebig vielen Leerzeichen; float(...) wandelt den Schwellwert um."
    )

# Richtige Regeln werden zerlegt, auch mit mehreren Leerzeichen
for zeile, erwartet in [
    ("cpu > 90", ("cpu", ">", 90.0)),
    ("temperatur > 75.5", ("temperatur", ">", 75.5)),
    ("festplatte < 10", ("festplatte", "<", 10.0)),
    ("temperatur < -5", ("temperatur", "<", -5.0)),
    ("  ram   >  80  ", ("ram", ">", 80.0)),
]:
    ergebnis, ausnahme = ergebnis_von_lies_regel(zeile)
    assert ausnahme is None and ergebnis == erwartet and isinstance(ergebnis[2], float), (
        f"lies_regel({zeile!r}) ergibt {ergebnis!r} (Ausnahme: {ausnahme!r}), erwartet war {erwartet!r}.\n"
        "Tipp: split() ohne Argument trennt an beliebig vielen Leerzeichen; float(...) wandelt den Schwellwert um."
    )

# Zeilen mit falsch vielen Teilen lösen einen ValueError mit der verlangten Meldung aus
for zeile, erwartet in [
    ("cpu > 90 %", "Erwartet: Messgröße Vergleich Schwellwert"),
    ("cpu>90", "Erwartet: Messgröße Vergleich Schwellwert"),
    ("festplatte <", "Erwartet: Messgröße Vergleich Schwellwert"),
    ("", "Erwartet: Messgröße Vergleich Schwellwert"),
]:
    ergebnis, ausnahme = ergebnis_von_lies_regel(zeile)
    assert isinstance(ausnahme, ValueError) and vergleichbar(str(ausnahme)) == vergleichbar(erwartet), (
        f"lies_regel({zeile!r}) muss einen ValueError mit der Meldung {erwartet!r} auslösen; "
        f"Ergebnis: {ergebnis!r}, Ausnahme: {ausnahme!r}.\n"
        'Tipp: raise ValueError("Unbekannte Messgröße: " + messgroesse) löst die Ausnahme mit Meldung aus.'
    )

# Eine unbekannte Messgröße löst einen ValueError mit der verlangten Meldung aus
for zeile, erwartet in [
    ("gpu > 90", "Unbekannte Messgröße: gpu"),
    ("CPU > 90", "Unbekannte Messgröße: CPU"),
]:
    ergebnis, ausnahme = ergebnis_von_lies_regel(zeile)
    assert isinstance(ausnahme, ValueError) and vergleichbar(str(ausnahme)) == vergleichbar(erwartet), (
        f"lies_regel({zeile!r}) muss einen ValueError mit der Meldung {erwartet!r} auslösen; "
        f"Ergebnis: {ergebnis!r}, Ausnahme: {ausnahme!r}.\n"
        'Tipp: raise ValueError("Unbekannte Messgröße: " + messgroesse) löst die Ausnahme mit Meldung aus.'
    )

# Ein unbekannter Vergleich löst einen ValueError mit der verlangten Meldung aus
for zeile, erwartet in [
    ("ram >= 80", "Unbekannter Vergleich: >="),
    ("cpu = 90", "Unbekannter Vergleich: ="),
]:
    ergebnis, ausnahme = ergebnis_von_lies_regel(zeile)
    assert isinstance(ausnahme, ValueError) and vergleichbar(str(ausnahme)) == vergleichbar(erwartet), (
        f"lies_regel({zeile!r}) muss einen ValueError mit der Meldung {erwartet!r} auslösen; "
        f"Ergebnis: {ergebnis!r}, Ausnahme: {ausnahme!r}.\n"
        'Tipp: raise ValueError("Unbekannte Messgröße: " + messgroesse) löst die Ausnahme mit Meldung aus.'
    )

# Ist der Schwellwert keine Zahl, kommt der ValueError von float(...) unverändert durch
for zeile in ["cpu > neunzig", "cpu > 9O", "ram < 1,5", "temperatur > 90%"]:
    erwartet = float_meldung(zeile.split()[2])
    ergebnis, ausnahme = ergebnis_von_lies_regel(zeile)
    assert isinstance(ausnahme, ValueError) and str(ausnahme) == erwartet, (
        f"lies_regel({zeile!r}) muss den ValueError von float(...) mit der Meldung {erwartet!r} durchlassen; "
        f"Ergebnis: {ergebnis!r}, Ausnahme: {ausnahme!r}.\n"
        "Tipp: Fangen Sie den Fehler von float(...) in lies_regel nicht ab, er wandert von selbst zum Aufrufer."
    )

# Die Prüfungen laufen in der verlangten Reihenfolge
for zeile, erwartet in [
    ("gpu => 90 1", "Erwartet: Messgröße Vergleich Schwellwert"),
    ("gpu => x", "Unbekannte Messgröße: gpu"),
    ("gpu > x", "Unbekannte Messgröße: gpu"),
    ("cpu => x", "Unbekannter Vergleich: =>"),
]:
    ergebnis, ausnahme = ergebnis_von_lies_regel(zeile)
    assert isinstance(ausnahme, ValueError) and vergleichbar(str(ausnahme)) == vergleichbar(erwartet), (
        f"lies_regel({zeile!r}) muss einen ValueError mit der Meldung {erwartet!r} auslösen; "
        f"Ergebnis: {ergebnis!r}, Ausnahme: {ausnahme!r}.\n"
        "Tipp: Prüfen Sie zuerst die Zahl der Teile, dann die Messgröße, dann den Vergleich und wandeln Sie erst "
        "zum Schluss den Schwellwert um."
    )

# lies_regeln aus dem Beispiel: die richtigen Regeln
ergebnis = lies_regeln(["cpu > 90", "", "ram >= 80", "temperatur > 75.5", "festplatte <"])
regeln = ergebnis[0] if isinstance(ergebnis, tuple) and len(ergebnis) == 2 else ergebnis
assert regeln == [("cpu", ">", 90.0), ("temperatur", ">", 75.5)], (
    f"Die Regeln von lies_regeln für das Beispiel aus der Aufgabe sind {regeln!r}, erwartet war "
    "[('cpu', '>', 90.0), ('temperatur', '>', 75.5)].\n"
    "Tipp: Rufen Sie lies_regel für jede nicht leere Zeile in einem try-Block auf und geben Sie (regeln, meldungen) zurück."
)

# Das Beispiel aus der Aufgabe
erwartet = (
    [("cpu", ">", 90.0), ("temperatur", ">", 75.5)],
    ["Zeile 3: Unbekannter Vergleich: >=", "Zeile 5: Erwartet: Messgröße Vergleich Schwellwert"],
)
ergebnis = lies_regeln(["cpu > 90", "", "ram >= 80", "temperatur > 75.5", "festplatte <"])
assert vergleichbare_meldungen(ergebnis) == vergleichbare_meldungen(erwartet), (
    f"lies_regeln für das Beispiel aus der Aufgabe ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}\n"
    "Tipp: Rufen Sie lies_regel im try-Block auf und schreiben Sie im except-Block "
    '"Zeile " + str(nummer) + ": " + str(ausnahme) in die Liste der Meldungen.'
)

# Eine leere Datei ergibt zwei leere Listen
ergebnis = lies_regeln([])
assert ergebnis == ([], []), f"lies_regeln([]) ergibt {ergebnis!r}, erwartet war ([], [])."

# Leere Zeilen werden übersprungen, zählen aber mit
ergebnis = lies_regeln(["", "   ", "gpu > 1", "", "ram > 5"])
erwartet = ([("ram", ">", 5.0)], ["Zeile 3: Unbekannte Messgröße: gpu"])
assert vergleichbare_meldungen(ergebnis) == vergleichbare_meldungen(erwartet), (
    f'lies_regeln(["", "   ", "gpu > 1", "", "ram > 5"]) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Überspringen Sie Zeilen, die nach strip() leer sind, und zählen Sie die Zeilennummer trotzdem weiter."
)

# Auch ein Fehler von float(...) landet mit Zeilennummer in der Fehlerliste
ergebnis = lies_regeln(["cpu > 90", "temperatur > heiß"])
erwartet = ([("cpu", ">", 90.0)], ["Zeile 2: " + float_meldung("heiß")])
assert vergleichbare_meldungen(ergebnis) == vergleichbare_meldungen(erwartet), (
    f'lies_regeln(["cpu > 90", "temperatur > heiß"]) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Der ValueError von float(...) wandert aus lies_regel heraus und wird im except-Block von lies_regeln gefangen."
)

# lies_regeln benutzt lies_regel und übernimmt die Meldung jeder Ausnahme
echte_lies_regel = lies_regel


def lies_regel(zeile):
    """Ersatz für diesen Test: löst immer einen ValueError mit der Zeile in der Meldung aus."""
    raise ValueError("Testmeldung zu " + zeile)


try:
    ergebnis = lies_regeln(["a", "", "b"])
    ausnahme = None
except Exception as fehler:
    ergebnis = None
    ausnahme = fehler
finally:
    lies_regel = echte_lies_regel
erwartet = ([], ["Zeile 1: Testmeldung zu a", "Zeile 3: Testmeldung zu b"])
assert ausnahme is None and vergleichbare_meldungen(ergebnis) == vergleichbare_meldungen(erwartet), (
    "Mit einem lies_regel, das immer einen ValueError mit eigener Meldung auslöst, ergibt "
    f'lies_regeln(["a", "", "b"]) {ergebnis!r} (Ausnahme: {ausnahme!r}), erwartet war {erwartet!r}.\n'
    "Tipp: Prüfen Sie die Zeile in lies_regeln nicht selbst, sondern rufen Sie lies_regel auf und übernehmen "
    "Sie mit except ValueError as ausnahme die Meldung str(ausnahme)."
)

# Andere Ausnahmen als ValueError fängt lies_regeln nicht ab
echte_lies_regel = lies_regel


def lies_regel(zeile):
    """Ersatz für diesen Test: hat einen Programmierfehler und löst einen KeyError aus."""
    raise KeyError(zeile)


try:
    ergebnis = lies_regeln(["cpu > 90"])
    ausnahme = None
except Exception as fehler:
    ergebnis = None
    ausnahme = fehler
finally:
    lies_regel = echte_lies_regel
assert isinstance(ausnahme, KeyError), (
    "Mit einem lies_regel, das einen KeyError auslöst, muss lies_regeln diesen KeyError durchlassen; "
    f"Ergebnis: {ergebnis!r}, Ausnahme: {ausnahme!r}.\n"
    "Tipp: Schreiben Sie except ValueError statt except: oder except Exception, sonst verschwinden echte "
    "Programmierfehler in der Liste der Meldungen."
)

# Viele zufällige Regeldateien (nicht fest hinschreiben!)
zufall = Zufall(3029)
for runde in range(300):
    zeilen = []
    erwartete_regeln = []
    erwartete_fehler = []
    for nummer in range(1, zufall.randint(0, 12) + 1):
        art = zufall.choice(["richtig", "richtig", "richtig", "leer", "teile", "messgroesse", "vergleich", "zahl"])
        messgroesse = zufall.choice(MESSGROESSEN)
        vergleich = zufall.choice(VERGLEICHE)
        zahl = zufall.randint(-100000, 100000) / 100
        schwellwert = str(zahl)
        if art == "messgroesse":
            messgroesse = zufall.choice(["gpu", "Cpu", "disk", "netz", "temp"])
        if art == "vergleich":
            vergleich = zufall.choice([">=", "<=", "=", "==", "!=", "=>"])
        if art == "zahl":
            schwellwert = zufall.choice(["neunzig", "9O", "1,5", "90%", "-", "x1"])
        zeile = messgroesse + " " + vergleich + " " + schwellwert
        if art == "teile":
            zeile = zufall.choice([messgroesse + " " + vergleich, zeile + " %", messgroesse + vergleich + schwellwert])
        if art == "leer":
            zeile = " " * zufall.randint(0, 3)
        zeilen.append(zeile)
        if art == "richtig":
            erwartete_regeln.append((messgroesse, vergleich, zahl))
        elif art == "teile":
            erwartete_fehler.append(f"Zeile {nummer}: Erwartet: Messgröße Vergleich Schwellwert")
        elif art == "messgroesse":
            erwartete_fehler.append(f"Zeile {nummer}: Unbekannte Messgröße: {messgroesse}")
        elif art == "vergleich":
            erwartete_fehler.append(f"Zeile {nummer}: Unbekannter Vergleich: {vergleich}")
        elif art == "zahl":
            erwartete_fehler.append(f"Zeile {nummer}: {float_meldung(schwellwert)}")
    ergebnis = lies_regeln(zeilen)
    erwartet = (erwartete_regeln, erwartete_fehler)
    assert vergleichbare_meldungen(ergebnis) == vergleichbare_meldungen(erwartet), f"lies_regeln({zeilen!r}) ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"

# Eine Regeldatei mit 10 000 Zeilen
zeilen = []
for nummer in range(10000):
    if nummer % 3 == 0:
        zeilen.append("cpu > " + str(nummer % 1000))
    elif nummer % 3 == 1:
        zeilen.append("gpu < 5")
    else:
        zeilen.append("")
regeln_gross, fehler_gross = lies_regeln(zeilen)
assert len(regeln_gross) == 3334 and len(fehler_gross) == 3333 and vergleichbar(str(fehler_gross[-1])) == vergleichbar("Zeile 9998: Unbekannte Messgröße: gpu"), (
    f"Bei 10 000 Zeilen ergibt lies_regeln {len(regeln_gross)} Regeln und {len(fehler_gross)} Fehler "
    f"(letzter Fehler: {fehler_gross[-1:]!r}); erwartet waren 3334 Regeln, 3333 Fehler und zuletzt "
    "'Zeile 9998: Unbekannte Messgröße: gpu'."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "2 Regeln gelesen\nZeile 3: Unbekannter Vergleich: >=\nZeile 5: Erwartet: Messgröße Vergleich Schwellwert"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
