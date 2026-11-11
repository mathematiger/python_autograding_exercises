# Automatisch erzeugt aus lehrkraft/muster/3_031_abfrageversuche.py - nicht von Hand ändern.
# vorlage-hash: eff46e9551b63263
# text-hash: e434db978a472740
# thema: fehler
# inhalt: Ausnahme weiterreichen mit `raise`

def abfrage_nach_plan(plan):
    """Gibt (abfrage, aufrufe) zurück: Der erste Aufruf von abfrage arbeitet plan[0] ab, der zweite plan[1] usw.

    Ist der Eintrag eine Ausnahme, löst abfrage sie aus, sonst gibt sie ihn zurück. aufrufe zählt die Aufrufe mit."""
    aufrufe = []

    def abfrage():
        """Arbeitet den nächsten Schritt des Plans ab."""
        if len(aufrufe) >= len(plan):
            aufrufe.append("zu viel")
            raise RuntimeError("abfrage wurde öfter aufgerufen als erlaubt")
        schritt = plan[len(aufrufe)]
        aufrufe.append(schritt)
        if isinstance(schritt, BaseException):
            raise schritt
        return schritt

    return abfrage, aufrufe


GLEICHES_OBJEKT = (
    "Verlangt ist genau das Ausnahme-Objekt, das abfrage ausgelöst hat (geprüft mit is); eine neue Ausnahme mit "
    "derselben Meldung genügt nicht.\n"
    "Tipp: raise ohne Argument im except-Block reicht die gerade behandelte Ausnahme unverändert weiter."
)


def ergebnis_von(plan, versuche, protokoll):
    """Ruft mit_wiederholung mit einer Abfrage nach plan auf.

    Gibt (Ergebnis, Ausnahme, Zahl der Aufrufe) zurück; Ergebnis oder Ausnahme ist None."""
    abfrage, aufrufe = abfrage_nach_plan(plan)
    try:
        ergebnis = mit_wiederholung(abfrage, versuche, protokoll)
        ausnahme = None
    except Exception as fehler:
        ergebnis = None
        ausnahme = fehler
    return ergebnis, ausnahme, len(aufrufe)


# Das Beispiel aus der Aufgabe
protokoll = []
ergebnis, ausnahme, aufrufe = ergebnis_von([TimeoutError("keine Antwort nach 5 s"), ["Ada", "Ben"]], 3, protokoll)
assert ausnahme is None and ergebnis == ["Ada", "Ben"] and protokoll == ["Versuch 1: keine Antwort nach 5 s"], (
    "Scheitert der erste Aufruf mit TimeoutError und klappt der zweite, ergibt mit_wiederholung "
    f"{ergebnis!r} (Ausnahme: {ausnahme!r}) und das Protokoll {protokoll!r}; erwartet waren ['Ada', 'Ben'] "
    "und ['Versuch 1: keine Antwort nach 5 s'].\n"
    "Tipp: Rufen Sie abfrage in einer Schleife im try-Block auf und geben Sie das Ergebnis gleich mit return zurück."
)

# Klappt der erste Aufruf, kommt sein Ergebnis sofort zurück, auch wenn es [], 0 oder None ist
for wert in [42, [], 0, None, "", ["Ada"]]:
    protokoll = []
    ergebnis, ausnahme, aufrufe = ergebnis_von([wert, "zweiter Aufruf"], 3, protokoll)
    assert ausnahme is None and ergebnis == wert and aufrufe == 1 and protokoll == [], (
        f"Liefert der erste Aufruf {wert!r}, ergibt mit_wiederholung {ergebnis!r} (Ausnahme: {ausnahme!r}) "
        f"bei {aufrufe} Aufruf(en), Protokoll {protokoll!r}; erwartet war {wert!r} nach einem Aufruf, Protokoll [].\n"
        "Tipp: Prüfen Sie nicht, ob das Ergebnis wahr ist; ein Aufruf hat geklappt, wenn er keine Ausnahme auslöst."
    )

# Nach mehreren vorübergehenden Fehlern klappt es doch
plan = [ConnectionError("Verbindung unterbrochen"), TimeoutError("Zeitüberschreitung"), ConnectionRefusedError("abgelehnt"), "Daten"]
protokoll = []
ergebnis, ausnahme, aufrufe = ergebnis_von(plan, 5, protokoll)
erwartet = ["Versuch 1: Verbindung unterbrochen", "Versuch 2: Zeitüberschreitung", "Versuch 3: abgelehnt"]
assert ausnahme is None and ergebnis == "Daten" and aufrufe == 4 and protokoll == erwartet, (
    "Bei ConnectionError, TimeoutError, ConnectionRefusedError und dann Erfolg ergibt mit_wiederholung(…, 5, …) "
    f"{ergebnis!r} (Ausnahme: {ausnahme!r}) bei {aufrufe} Aufruf(en), Protokoll {protokoll!r};\n"
    f"erwartet war 'Daten' nach 4 Aufrufen, Protokoll {erwartet!r}.\n"
    "Tipp: Fangen Sie TimeoutError und ConnectionError in einem except mit Tupel ab; das fängt auch ConnectionRefusedError."
)

# Scheitert auch der letzte Versuch, kommt genau dessen Ausnahme beim Aufrufer an
fehler_je_versuch = [TimeoutError("erster"), ConnectionResetError("zweiter"), TimeoutError("dritter")]
protokoll = []
ergebnis, ausnahme, aufrufe = ergebnis_von(fehler_je_versuch + ["zu spät"], 3, protokoll)
assert ausnahme is fehler_je_versuch[2], (
    "Scheitern alle drei erlaubten Versuche, muss mit_wiederholung die Ausnahme des dritten Versuchs, "
    f"{fehler_je_versuch[2]!r}, unverändert weiterreichen; erhalten: Ergebnis {ergebnis!r}, Ausnahme {ausnahme!r}.\n"
    + GLEICHES_OBJEKT
)

# Beim Aufgeben stimmen Zahl der Aufrufe und Protokoll
assert aufrufe == 3 and protokoll == ["Versuch 1: erster", "Versuch 2: zweiter", "Versuch 3: dritter"], (
    f"Scheitern alle drei erlaubten Versuche, ruft mit_wiederholung abfrage {aufrufe}-mal auf, Protokoll {protokoll!r}; "
    "erwartet waren 3 Aufrufe und ['Versuch 1: erster', 'Versuch 2: zweiter', 'Versuch 3: dritter'].\n"
    "Tipp: Auch der letzte Fehlversuch kommt ins Protokoll, bevor die Ausnahme weitergereicht wird."
)

# Mit nur einem erlaubten Versuch gibt es keine Wiederholung
fehler = TimeoutError("einziger")
protokoll = []
ergebnis, ausnahme, aufrufe = ergebnis_von([fehler, "zu spät"], 1, protokoll)
assert ausnahme is fehler and aufrufe == 1 and protokoll == ["Versuch 1: einziger"], (
    f"Mit versuche = 1 und einem TimeoutError ergibt mit_wiederholung Ergebnis {ergebnis!r}, Ausnahme {ausnahme!r} "
    f"bei {aufrufe} Aufruf(en), Protokoll {protokoll!r}; erwartet war genau die Ausnahme {fehler!r} nach einem "
    "Aufruf und das Protokoll ['Versuch 1: einziger'].\n" + GLEICHES_OBJEKT
)

# Andere Fehler kommen sofort beim Aufrufer an, ohne neuen Versuch und ohne Protokoll
for fehler in [ValueError("Syntaxfehler in der Abfrage"), KeyError("kundennummer"), FileNotFoundError("kunden.db"), OSError("Platte voll"), ZeroDivisionError("division by zero")]:
    protokoll = []
    ergebnis, ausnahme, aufrufe = ergebnis_von([fehler, "zweiter Aufruf"], 3, protokoll)
    assert ausnahme is fehler and aufrufe == 1 and protokoll == [], (
        f"Löst der erste Aufruf {fehler!r} aus, ergibt mit_wiederholung Ergebnis {ergebnis!r}, Ausnahme {ausnahme!r} "
        f"bei {aufrufe} Aufruf(en), Protokoll {protokoll!r}; erwartet war genau diese Ausnahme nach einem Aufruf, "
        "Protokoll [].\n"
        "Tipp: Fangen Sie nur TimeoutError und ConnectionError ab, nicht OSError oder Exception: "
        "Eine fehlende Datei fehlt auch beim nächsten Versuch."
    )

# Ein anderer Fehler nach einem vorübergehenden wird ebenfalls sofort weitergereicht
fehler = ValueError("Spalte unbekannt")
protokoll = []
ergebnis, ausnahme, aufrufe = ergebnis_von([TimeoutError("kurz weg"), fehler, "dritter Aufruf"], 5, protokoll)
assert ausnahme is fehler and aufrufe == 2 and protokoll == ["Versuch 1: kurz weg"], (
    f"Bei TimeoutError und dann {fehler!r} ergibt mit_wiederholung Ergebnis {ergebnis!r}, Ausnahme {ausnahme!r} "
    f"bei {aufrufe} Aufruf(en), Protokoll {protokoll!r}; erwartet war {fehler!r} nach 2 Aufrufen, "
    "Protokoll ['Versuch 1: kurz weg']."
)

# Neue Einträge kommen ans Ende des Protokolls
protokoll = ["Start der Abfrage"]
ergebnis, ausnahme, aufrufe = ergebnis_von([TimeoutError("langsam"), 7], 2, protokoll)
assert protokoll == ["Start der Abfrage", "Versuch 1: langsam"], (
    f"Das Protokoll ist nach mit_wiederholung {protokoll!r}, erwartet war ['Start der Abfrage', 'Versuch 1: langsam'].\n"
    "Tipp: Hängen Sie mit append an die übergebene Liste an, statt eine neue anzulegen."
)

# Viele zufällige Abläufe (nicht fest hinschreiben!)
zufall = Zufall(3031)
for runde in range(500):
    versuche = zufall.randint(1, 10)
    plan = []
    for nummer in range(versuche + 1):
        art = zufall.choice(["timeout", "timeout", "verbindung", "verbindung", "anderer", "wert"])
        if art == "timeout":
            plan.append(TimeoutError("Zeitüberschreitung " + str(nummer)))
        elif art == "verbindung":
            plan.append(zufall.choice([ConnectionError, ConnectionRefusedError, ConnectionResetError, BrokenPipeError])("weg " + str(nummer)))
        elif art == "anderer":
            plan.append(zufall.choice([ValueError, KeyError, FileNotFoundError, PermissionError, TypeError])("kaputt " + str(nummer)))
        else:
            plan.append(zufall.randint(-1000, 1000))
    erwartetes_protokoll = []
    erwartetes_ergebnis = None
    erwartete_ausnahme = None
    for nummer in range(versuche):
        schritt = plan[nummer]
        if not isinstance(schritt, BaseException):
            erwartetes_ergebnis = schritt
            break
        if not isinstance(schritt, (TimeoutError, ConnectionError)):
            erwartete_ausnahme = schritt
            break
        erwartetes_protokoll.append(f"Versuch {nummer + 1}: {schritt}")
        if nummer == versuche - 1:
            erwartete_ausnahme = schritt
    protokoll = []
    ergebnis, ausnahme, aufrufe = ergebnis_von(plan, versuche, protokoll)
    assert ergebnis == erwartetes_ergebnis and ausnahme is erwartete_ausnahme and protokoll == erwartetes_protokoll, (
        f"mit_wiederholung(…, {versuche}, []), wenn abfrage nacheinander dies liefert oder auslöst: {plan!r}\n"
        f"ergibt Ergebnis {ergebnis!r}, Ausnahme {ausnahme!r}, Protokoll {protokoll!r};\n"
        f"erwartet waren Ergebnis {erwartetes_ergebnis!r}, Ausnahme {erwartete_ausnahme!r}, Protokoll {erwartetes_protokoll!r}.\n"
        "Eine erwartete Ausnahme muss genau das Objekt aus dieser Liste sein, nicht eine neue mit derselben Meldung."
    )

# Zehn erlaubte Versuche, alle scheitern
fehler_je_versuch = []
for nummer in range(10):
    fehler_je_versuch.append(TimeoutError("Versuch Nummer " + str(nummer + 1)))
protokoll = []
ergebnis, ausnahme, aufrufe = ergebnis_von(fehler_je_versuch, 10, protokoll)
assert ausnahme is fehler_je_versuch[9] and aufrufe == 10 and len(protokoll) == 10 and protokoll[9] == "Versuch 10: Versuch Nummer 10", (
    f"Mit versuche = 10 und zehn TimeoutErrors ergibt mit_wiederholung Ausnahme {ausnahme!r} bei {aufrufe} Aufruf(en) "
    f"und {len(protokoll)} Protokolleinträgen (letzter: {protokoll[-1:]!r}); erwartet war der zehnte TimeoutError "
    "nach 10 Aufrufen und 10 Einträgen, zuletzt 'Versuch 10: Versuch Nummer 10'.\n" + GLEICHES_OBJEKT
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['Ada', 'Ben']\n['Versuch 1: keine Antwort nach 5 s']"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
