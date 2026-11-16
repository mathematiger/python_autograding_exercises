# Automatisch erzeugt aus lehrkraft/muster/5_023_bereitschaft.py - nicht von Hand ändern.
# vorlage-hash: f337ec4fa863d941
# text-hash: 077371c069cf930f
# thema: klassen
# inhalt: __bool__ und __len__

def loest_aus(funktion, *argumente):
    """Ruft funktion auf und gibt True zurück, wenn dabei ein ValueError kam."""
    try:
        funktion(*argumente)
    except ValueError:
        return True
    return False


def plan(*namen, abgemeldet=()):
    """Baut einen Bereitschaftsplan mit diesen Namen; die aus abgemeldet sind nicht erreichbar."""
    bereitschaft = Bereitschaft()
    for name in namen:
        bereitschaft.eintragen(name)
    for name in abgemeldet:
        bereitschaft.abmelden(name)
    return bereitschaft


def wahrheit(objekt):
    """Liefert bool(objekt) oder eine Beschreibung des Fehlers."""
    try:
        return bool(objekt)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def laenge(objekt):
    """Liefert len(objekt) oder eine Beschreibung des Fehlers."""
    try:
        return len(objekt)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


# len einer Warteschlange zählt die offenen Tickets
schlange = Warteschlange()
schlange.hinzufuegen(4711)
schlange.hinzufuegen(4712)
assert laenge(schlange) == 2, (
    f"Nach zwei Aufrufen von hinzufuegen ergibt len(schlange) {laenge(schlange)!r}, erwartet war 2.\n"
    "Tipp: len(schlange) ruft schlange.__len__() auf."
)

# erledigen verringert die Länge
schlange.erledigen(4711)
assert laenge(schlange) == 1, f"Nach erledigen(4711) ergibt len(schlange) {laenge(schlange)!r}, erwartet war 1."

# Eine leere Warteschlange gilt als falsch
assert wahrheit(Warteschlange()) is False, (
    f"bool(Warteschlange()) ergibt {wahrheit(Warteschlange())!r}, erwartet war False.\n"
    "Tipp: Hat die Klasse __len__, ist ein Objekt mit Länge 0 falsch."
)

# Eine Warteschlange mit Tickets gilt als wahr
schlange = Warteschlange()
schlange.hinzufuegen(1)
assert wahrheit(schlange) is True, f"bool(…) einer Warteschlange mit einem Ticket ergibt {wahrheit(schlange)!r}, erwartet war True."

# Nach dem letzten erledigten Ticket ist sie wieder falsch
schlange.erledigen(1)
assert wahrheit(schlange) is False and laenge(schlange) == 0, (
    f"Nach hinzufuegen(1) und erledigen(1) ergeben len und bool {laenge(schlange)!r} und {wahrheit(schlange)!r}, "
    "erwartet waren 0 und False."
)

# Warteschlange verlässt sich auf __len__ und hat kein eigenes __bool__
assert "__bool__" not in vars(Warteschlange), (
    "Warteschlange hat eine Methode __bool__. Ohne sie fragt Python __len__; schreiben Sie nur __len__."
)

# Doppelte und unbekannte Tickets lösen ValueError aus
schlange = Warteschlange()
schlange.hinzufuegen(7)
doppelt = loest_aus(schlange.hinzufuegen, 7)
unbekannt = loest_aus(schlange.erledigen, 8)
assert doppelt and unbekannt and laenge(schlange) == 1, (
    "hinzufuegen(7) für ein schon offenes Ticket und erledigen(8) für ein unbekanntes sollen je einen ValueError "
    f"auslösen und nichts ändern; ValueError: {doppelt} und {unbekannt}, len danach {laenge(schlange)!r}."
)

# Ein erledigtes Ticket kann nicht noch einmal erledigt werden
schlange.erledigen(7)
assert loest_aus(schlange.erledigen, 7), "Ein zweites erledigen(7) soll einen ValueError auslösen."

# Zwei Warteschlangen sind unabhängig
erste = Warteschlange()
zweite = Warteschlange()
erste.hinzufuegen(5)
assert (laenge(erste), laenge(zweite)) == (1, 0), (
    f"Nach erste.hinzufuegen(5) ergeben len(erste) und len(zweite) {(laenge(erste), laenge(zweite))}, erwartet war (1, 0).\n"
    "Tipp: Legen Sie den Speicher für die Tickets in __init__ auf self an, nicht als Klassenattribut."
)

# len eines Bereitschaftsplans zählt alle eingetragenen Personen
p = plan("Ada", "Bo", "Cem")
assert laenge(p) == 3, f'len eines Plans mit "Ada", "Bo" und "Cem" ergibt {laenge(p)!r}, erwartet war 3.'

# Ein Plan mit erreichbaren Personen gilt als wahr
assert wahrheit(p) is True, f"bool eines Plans mit drei erreichbaren Personen ergibt {wahrheit(p)!r}, erwartet war True."

# Abgemeldete Personen zählen für len weiter mit
p = plan("Ada", "Bo", abgemeldet=["Ada"])
assert laenge(p) == 2, f'len eines Plans mit "Ada" (abgemeldet) und "Bo" ergibt {laenge(p)!r}, erwartet war 2.'

# Sind alle abgemeldet, gilt der Plan als falsch, obwohl len nicht 0 ist
p = plan("Ada", "Bo", abgemeldet=["Ada", "Bo"])
assert laenge(p) == 2 and wahrheit(p) is False, (
    f"Ein Plan mit zwei abgemeldeten Personen ergibt len {laenge(p)!r} und bool {wahrheit(p)!r}, erwartet waren 2 und False.\n"
    "Tipp: Schreiben Sie __bool__; es hat Vorrang vor __len__ und muss True oder False liefern."
)

# zurueckmelden macht den Plan wieder wahr
p.zurueckmelden("Bo")
assert wahrheit(p) is True, f"Nach zurueckmelden('Bo') ergibt bool(plan) {wahrheit(p)!r}, erwartet war True."

# Mehrfaches Ab- und Zurückmelden zählt nicht doppelt
p = plan("Ada", "Bo")
p.abmelden("Ada")
p.abmelden("Ada")
p.zurueckmelden("Bo")
p.abmelden("Bo")
assert wahrheit(p) is False and laenge(p) == 2, (
    "Nach eintragen Ada und Bo, abmelden Ada (zweimal), zurueckmelden Bo (war schon erreichbar), abmelden Bo "
    f"ergeben bool und len {wahrheit(p)!r} und {laenge(p)!r}, erwartet waren False und 2.\n"
    "Tipp: Ändern Sie einen Zähler nur, wenn sich die Erreichbarkeit wirklich ändert."
)

# Abmelden, zurückmelden und wieder abmelden
p = plan("Ada")
p.abmelden("Ada")
p.zurueckmelden("Ada")
zwischendurch = wahrheit(p)
p.abmelden("Ada")
assert zwischendurch is True and wahrheit(p) is False, (
    "Nach eintragen, abmelden, zurueckmelden und abmelden von Ada ergibt bool(plan) zwischendurch "
    f"{zwischendurch!r} und am Ende {wahrheit(p)!r}, erwartet waren True und False.\n"
    "Tipp: Jede Änderung der Erreichbarkeit verändert die Zahl der Erreichbaren um genau 1."
)

# Ein leerer Plan gilt als falsch und hat die Länge 0
assert (laenge(Bereitschaft()), wahrheit(Bereitschaft())) == (0, False), (
    f"Ein leerer Plan ergibt len und bool {(laenge(Bereitschaft()), wahrheit(Bereitschaft()))}, erwartet war (0, False)."
)

# Doppelt eintragen und unbekannte Namen lösen ValueError aus
p = plan("Ada")
fehler = (loest_aus(p.eintragen, "Ada"), loest_aus(p.abmelden, "Zoe"), loest_aus(p.zurueckmelden, "Zoe"))
assert fehler == (True, True, True) and laenge(p) == 1, (
    "eintragen('Ada') zum zweiten Mal, abmelden('Zoe') und zurueckmelden('Zoe') für eine nicht eingetragene Person "
    f"sollen je einen ValueError auslösen; ValueError kam: {fehler}, len danach {laenge(p)!r}."
)

# zustaendige_stufe aus dem Beispiel
stufen = [plan("Ada", abgemeldet=["Ada"]), plan("Cem")]
ergebnis = zustaendige_stufe(stufen)
assert ergebnis == 2, (
    f"zustaendige_stufe([<Ada abgemeldet>, <Cem>]) ergibt {ergebnis!r}, erwartet war 2.\n"
    "Tipp: Fragen Sie mit if stufe:, das ruft __bool__ auf; die Nummer zählt ab 1."
)

# zustaendige_stufe nimmt die erste passende Stufe
stufen = [plan("Ada"), plan("Bo"), plan("Cem")]
ergebnis = zustaendige_stufe(stufen)
assert ergebnis == 1, f"zustaendige_stufe mit drei erreichbaren Stufen ergibt {ergebnis!r}, erwartet war 1."

# Eine leere Stufe wird übersprungen
stufen = [Bereitschaft(), plan("X", "Y", abgemeldet=["X"]), plan("Z")]
ergebnis = zustaendige_stufe(stufen)
assert ergebnis == 2, f"zustaendige_stufe([<leer>, <X abgemeldet, Y erreichbar>, <Z>]) ergibt {ergebnis!r}, erwartet war 2."

# Keine Stufe erreichbar: None
stufen = [Bereitschaft(), plan("X", abgemeldet=["X"])]
ergebnis = zustaendige_stufe(stufen)
assert ergebnis is None, f"zustaendige_stufe ohne erreichbare Stufe ergibt {ergebnis!r}, erwartet war None."

# Keine Stufen: None
ergebnis = zustaendige_stufe([])
assert ergebnis is None, f"zustaendige_stufe([]) ergibt {ergebnis!r}, erwartet war None."

# lagebericht mit offenen Tickets
schlange = Warteschlange()
for nummer in (10, 20, 30):
    schlange.hinzufuegen(nummer)
ergebnis = lagebericht(schlange)
assert isinstance(ergebnis, str) and vergleichbar(ergebnis) == vergleichbar("3 offene Tickets"), (
    f'lagebericht(<3 Tickets>) ergibt {ergebnis!r}, erwartet war "3 offene Tickets".'
)

# lagebericht einer leeren Warteschlange
ergebnis = lagebericht(Warteschlange())
assert isinstance(ergebnis, str) and vergleichbar(ergebnis) == vergleichbar("keine offenen Tickets"), (
    f'lagebericht(Warteschlange()) ergibt {ergebnis!r}, erwartet war "keine offenen Tickets".\n'
    "Tipp: Eine leere Warteschlange ist nicht None; prüfen Sie zuerst mit is None, dann mit if not schlange."
)

# lagebericht ohne Warteschlange
ergebnis = lagebericht(None)
assert isinstance(ergebnis, str) and vergleichbar(ergebnis) == vergleichbar("keine Warteschlange"), (
    f'lagebericht(None) ergibt {ergebnis!r}, erwartet war "keine Warteschlange".\n'
    "Tipp: if schlange: ist auch für eine leere Warteschlange falsch; für None prüfen Sie mit schlange is None."
)

# Ränder: kleinste und größte Ticketnummer
schlange = Warteschlange()
schlange.hinzufuegen(1)
schlange.hinzufuegen(10**9)
schlange.erledigen(1)
assert laenge(schlange) == 1 and wahrheit(schlange) is True, (
    f"Nach hinzufuegen(1), hinzufuegen(10**9), erledigen(1) ergeben len und bool {laenge(schlange)!r} und "
    f"{wahrheit(schlange)!r}, erwartet waren 1 und True."
)

# 200 zufällige Abläufe mit Warteschlangen und Plänen
zufall = Zufall(5023)
for _ in range(200):
    schlange = Warteschlange()
    p = Bereitschaft()
    offen = set()
    personen = {}
    ablauf = []
    for _ in range(15):
        aktion = zufall.choice(["hinzufuegen", "erledigen", "eintragen", "abmelden", "zurueckmelden"])
        if aktion in ("hinzufuegen", "erledigen"):
            wert = zufall.randint(1, 6)
            erwartet_fehler = (wert in offen) == (aktion == "hinzufuegen")
            ausgeloest = loest_aus(getattr(schlange, aktion), wert)
            if not erwartet_fehler:
                offen.symmetric_difference_update({wert})
        else:
            wert = zufall.choice("ABCD")
            if aktion == "eintragen":
                erwartet_fehler = wert in personen
            else:
                erwartet_fehler = wert not in personen
            ausgeloest = loest_aus(getattr(p, aktion), wert)
            if not erwartet_fehler:
                personen[wert] = aktion != "abmelden"
        ablauf.append(f"{aktion}({wert!r})")
        ist = (ausgeloest, laenge(schlange), wahrheit(schlange), laenge(p), wahrheit(p))
        soll = (erwartet_fehler, len(offen), bool(offen), len(personen), any(personen.values()))
        assert ist == soll, (
            f"Nach {', '.join(ablauf)}: ValueError, len und bool der Warteschlange, len und bool des Plans "
            f"ergeben {ist}, erwartet war {soll}."
        )

# 200 zufällige Eskalationen
for _ in range(200):
    stufen = []
    erreichbar = []
    for _ in range(zufall.randint(0, 6)):
        namen = [f"N{k}" for k in range(zufall.randint(0, 3))]
        weg = [name for name in namen if zufall.random() < 0.6]
        stufen.append(plan(*namen, abgemeldet=weg))
        erreichbar.append(len(namen) > len(weg))
    erwartet = erreichbar.index(True) + 1 if True in erreichbar else None
    ergebnis = zustaendige_stufe(stufen)
    assert ergebnis == erwartet, (
        f"Bei Stufen, in denen jemand erreichbar ist: {erreichbar}, ergibt zustaendige_stufe {ergebnis!r}, "
        f"erwartet war {erwartet!r}."
    )


# Viele Tickets und Personen: len und bool in O(1)
def viele_aufrufe():
    """Füllt Warteschlange und Plan mit je 20 000 Einträgen und fragt danach 1000-mal len und bool ab."""
    schlange = Warteschlange()
    p = Bereitschaft()
    for nummer in range(1, 20001):
        schlange.hinzufuegen(nummer)
        p.eintragen(f"P{nummer}")
    for nummer in range(1, 20001):
        p.abmelden(f"P{nummer}")
    ergebnisse = []
    for _ in range(1000):
        ergebnisse.append((len(schlange), bool(schlange), len(p), bool(p)))
    return ergebnisse


ergebnisse, schritte = zaehle_schritte(viele_aufrufe)
assert ergebnisse[-1] == (20000, True, 20000, False) and schritte <= 600000, (
    f"20 000 Tickets und 20 000 abgemeldete Personen, dann 1000-mal len und bool: Ergebnis {ergebnisse[-1]} "
    f"nach {schritte} Schritten; erwartet war (20000, True, 20000, False) nach höchstens 600 000 Schritten.\n"
    "Tipp: Zählen Sie in __bool__ nicht jedes Mal alle Personen durch, sondern führen Sie die Zahl der "
    "Erreichbaren in einem Attribut mit."
)

# Obere Grenze: 100 000 Tickets
schlange = Warteschlange()
for nummer in range(10**9 - 99999, 10**9 + 1):
    schlange.hinzufuegen(nummer)
for nummer in range(10**9 - 99999, 10**9):
    schlange.erledigen(nummer)
assert (laenge(schlange), wahrheit(schlange)) == (1, True), (
    f"Nach 100 000 Tickets und 99 999 erledigten ergeben len und bool {laenge(schlange)!r} und "
    f"{wahrheit(schlange)!r}, erwartet waren 1 und True."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "2 offene Tickets\n1 False 2"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
