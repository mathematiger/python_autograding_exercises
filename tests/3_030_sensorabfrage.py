# Automatisch erzeugt aus lehrkraft/muster/3_030_sensorabfrage.py - nicht von Hand ändern.
# vorlage-hash: beb2de60c472894e
# text-hash: 8225097c6e754f6c
# thema: fehler
# inhalt: Stammbaum der Ausnahmen

STOERUNG_JE_ART = [
    (OSError, "Gerät nicht erreichbar"),
    (TimeoutError, "Sensor antwortet nicht"),
    (ConnectionError, "Gerät nicht erreichbar"),
    (ConnectionRefusedError, "Gerät nicht erreichbar"),
    (ConnectionResetError, "Gerät nicht erreichbar"),
    (BrokenPipeError, "Gerät nicht erreichbar"),
    (FileNotFoundError, "Gerät nicht erreichbar"),
    (PermissionError, "Gerät nicht erreichbar"),
    (LookupError, "Konfiguration prüfen"),
    (KeyError, "Konfiguration prüfen"),
    (IndexError, "Konfiguration prüfen"),
    (ArithmeticError, "Rechenfehler"),
    (ZeroDivisionError, "Rechenfehler"),
    (OverflowError, "Rechenfehler"),
    (FloatingPointError, "Rechenfehler"),
    (Exception, "Softwarefehler: Testfehler"),
    (ValueError, "Softwarefehler: Testfehler"),
    (TypeError, "Softwarefehler: Testfehler"),
    (AttributeError, "Softwarefehler: Testfehler"),
    (NameError, "Softwarefehler: Testfehler"),
    (RuntimeError, "Softwarefehler: Testfehler"),
    (RecursionError, "Softwarefehler: Testfehler"),
    (AssertionError, "Softwarefehler: Testfehler"),
]


def wirft(art):
    """Gibt eine Lesefunktion zurück, die eine Ausnahme der Art art auslöst."""

    def lesefunktion():
        """Löst die Ausnahme aus, statt einen Messwert zu liefern."""
        raise art("Testfehler")

    return lesefunktion


def liefert(wert):
    """Gibt eine Lesefunktion zurück, die den Messwert wert liefert."""

    def lesefunktion():
        """Gibt den Messwert zurück."""
        return wert

    return lesefunktion


def ergebnis_von_frage_ab(sensoren):
    """Ruft frage_ab auf und gibt (Ergebnis, Ausnahme) zurück; eine davon ist None."""
    try:
        return frage_ab(sensoren), None
    except Exception as ausnahme:
        return None, ausnahme


def vergleichbare_stoerungen(ergebnis):
    """Macht in (werte, stoerungen) die Störungstexte mit vergleichbar unempfindlich gegen die Schreibweise; die Werte bleiben."""
    if not (isinstance(ergebnis, tuple) and len(ergebnis) == 2 and isinstance(ergebnis[1], dict)):
        return ergebnis
    texte = {}
    for name, text in ergebnis[1].items():
        texte[name] = vergleichbar(text) if isinstance(text, str) else text
    return ergebnis[0], texte


# Das Beispiel aus der Aufgabe
ergebnis, ausnahme = ergebnis_von_frage_ab(
    [("temperatur", halle_temperatur), ("tor", tor_sensor), ("kran", kran_last), ("feuchte", feuchte_sensor)]
)
erwartet = (
    {"temperatur": 21.5},
    {"tor": "Sensor antwortet nicht", "kran": "Rechenfehler", "feuchte": "Konfiguration prüfen"},
)
assert ausnahme is None and vergleichbare_stoerungen(ergebnis) == vergleichbare_stoerungen(erwartet), (
    f"frage_ab für das Beispiel aus der Aufgabe ergibt {ergebnis!r} (Ausnahme: {ausnahme!r}),\n"
    f"erwartet war {erwartet!r}.\n"
    "Tipp: Rufen Sie jede Lesefunktion in einem try-Block auf und schreiben Sie für jede Zeile der Tabelle "
    "einen eigenen except-Block."
)

# Jede Art von Ausnahme ergibt die Störung ihrer Familie im Stammbaum
for art, erwartet in STOERUNG_JE_ART:
    ergebnis, ausnahme = ergebnis_von_frage_ab([("sensor", wirft(art))])
    assert ausnahme is None and vergleichbare_stoerungen(ergebnis) == vergleichbare_stoerungen(({}, {"sensor": erwartet})), (
        f"Löst die Lesefunktion {art('Testfehler')!r} aus, ergibt frage_ab {ergebnis!r} (Ausnahme: {ausnahme!r}); "
        f"erwartet war ({{}}, {{'sensor': {erwartet!r}}}).\n"
        "Tipp: except OSError fängt auch ConnectionError und FileNotFoundError, except LookupError auch KeyError und "
        "IndexError. Die speziellere Art steht oben: except TimeoutError über except OSError, except Exception ganz "
        'unten. Beim Softwarefehler gehört die Meldung dazu: "Softwarefehler: " + str(ausnahme).'
    )

# Sensoren, die antworten, kommen mit ihrem Wert in werte, auch bei 0
for wert in [21.5, 0, 0.0, -40, 1013.25]:
    ergebnis, ausnahme = ergebnis_von_frage_ab([("sensor", liefert(wert))])
    assert ausnahme is None and ergebnis == ({"sensor": wert}, {}), (
        f"Liefert die Lesefunktion {wert!r}, ergibt frage_ab {ergebnis!r} (Ausnahme: {ausnahme!r}); "
        f"erwartet war ({{'sensor': {wert!r}}}, {{}})."
    )

# Ohne Sensoren sind beide Dictionaries leer
ergebnis, ausnahme = ergebnis_von_frage_ab([])
assert ausnahme is None and ergebnis == ({}, {}), f"frage_ab([]) ergibt {ergebnis!r} (Ausnahme: {ausnahme!r}), erwartet war ({{}}, {{}})."

# Jede Lesefunktion wird genau einmal aufgerufen, in der Reihenfolge der Liste
aufrufe = []


def zaehlend(name, lesefunktion):
    """Gibt eine Lesefunktion zurück, die ihren Aufruf in aufrufe vermerkt und dann lesefunktion aufruft."""

    def gezaehlt():
        """Vermerkt den Aufruf und gibt das Ergebnis von lesefunktion weiter."""
        aufrufe.append(name)
        return lesefunktion()

    return gezaehlt


sensoren = [
    ("a", zaehlend("a", liefert(1))),
    ("b", zaehlend("b", wirft(TimeoutError))),
    ("c", zaehlend("c", liefert(3))),
    ("d", zaehlend("d", wirft(ValueError))),
]
ergebnis, ausnahme = ergebnis_von_frage_ab(sensoren)
assert aufrufe == ["a", "b", "c", "d"], (
    f"frage_ab ruft die Lesefunktionen in dieser Folge auf: {aufrufe!r}; erwartet war jede genau einmal: ['a', 'b', 'c', 'd'].\n"
    "Tipp: Rufen Sie jede Lesefunktion nur einmal auf und merken Sie sich das Ergebnis."
)

# Ein Abbruch mit Strg+C (KeyboardInterrupt) wird nicht abgefangen
try:
    ergebnis = frage_ab([("temperatur", liefert(21.5)), ("abbruch", wirft(KeyboardInterrupt))])
    abgebrochen = False
except KeyboardInterrupt:
    abgebrochen = True
assert abgebrochen, (
    f"Löst eine Lesefunktion KeyboardInterrupt aus, muss frage_ab ihn durchlassen; frage_ab ergab aber {ergebnis!r}.\n"
    "Tipp: Ein nacktes except: oder except BaseException fängt auch Strg+C ab. Schreiben Sie except Exception."
)

# Viele zufällige Sensorlisten (nicht fest hinschreiben!)
zufall = Zufall(3030)
for runde in range(300):
    sensoren = []
    verhalten = []
    erwartete_werte = {}
    erwartete_stoerungen = {}
    for nummer in range(zufall.randint(0, 15)):
        name = "sensor_" + str(nummer)
        if zufall.random() < 0.4:
            wert = zufall.randint(-500, 500) / 10
            sensoren.append((name, liefert(wert)))
            verhalten.append((name, wert))
            erwartete_werte[name] = wert
        else:
            art, stoerung = zufall.choice(STOERUNG_JE_ART)
            sensoren.append((name, wirft(art)))
            verhalten.append((name, art("Testfehler")))
            erwartete_stoerungen[name] = stoerung
    ergebnis, ausnahme = ergebnis_von_frage_ab(sensoren)
    erwartet = (erwartete_werte, erwartete_stoerungen)
    assert ausnahme is None and vergleichbare_stoerungen(ergebnis) == vergleichbare_stoerungen(erwartet), (
        f"frage_ab für Sensoren, die Folgendes liefern oder auslösen: {verhalten!r}\n"
        f"ergibt {ergebnis!r} (Ausnahme: {ausnahme!r}),\nerwartet war {erwartet!r}"
    )

# 1000 Sensoren, abwechselnd mit Wert und mit Störung
sensoren = []
for nummer in range(1000):
    if nummer % 2 == 0:
        sensoren.append(("s" + str(nummer), liefert(nummer)))
    else:
        sensoren.append(("s" + str(nummer), wirft(ConnectionResetError)))
ergebnis, ausnahme = ergebnis_von_frage_ab(sensoren)
werte_gross, stoerungen_gross = ergebnis if ausnahme is None else ({}, {})
assert len(werte_gross) == 500 and len(stoerungen_gross) == 500 and werte_gross.get("s998") == 998 and vergleichbar(str(stoerungen_gross.get("s999"))) == vergleichbar("Gerät nicht erreichbar"), (
    f"Bei 1000 Sensoren ergibt frage_ab {len(werte_gross)} Werte und {len(stoerungen_gross)} Störungen "
    f"(Ausnahme: {ausnahme!r}); erwartet waren je 500, mit werte['s998'] == 998 und "
    "stoerungen['s999'] == 'Gerät nicht erreichbar'."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "Werte: {'temperatur': 21.5}\n"
    "Störungen: {'tor': 'Sensor antwortet nicht', 'kran': 'Rechenfehler', 'feuchte': 'Konfiguration prüfen'}"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
