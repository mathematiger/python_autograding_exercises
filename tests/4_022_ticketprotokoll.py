# Automatisch erzeugt aus lehrkraft/muster/4_022_ticketprotokoll.py - nicht von Hand ändern.
# vorlage-hash: 827d4a0fca0f287a
# text-hash: d00835590c0fc0b5
# thema: funktionen
# inhalt: Dekoratoren und functools.wraps

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[\"eskaliere('T-17', stufe=2) -> 'T-17 auf Stufe 2'\", \"schliesse('T-99') -> Fehler: ValueError\"]\neskaliere"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"


@protokolliere
def weise_zu(ticket, person, *, prioritaet="normal"):
    """Weist ein Ticket einer Person zu."""
    return (ticket, person, prioritaet)


# Ergebnis wird durchgereicht, Argumente nach Position und nach Namen
PROTOKOLL.clear()
ergebnis = weise_zu("T-3", person="Kim", prioritaet="hoch")
assert ergebnis == ("T-3", "Kim", "hoch") and PROTOKOLL == ["weise_zu('T-3', person='Kim', prioritaet='hoch') -> ('T-3', 'Kim', 'hoch')"], (
    f"weise_zu('T-3', person='Kim', prioritaet='hoch') ergibt {ergebnis!r} und protokolliert {PROTOKOLL!r}; erwartet war "
    "('T-3', 'Kim', 'hoch') und die Zeile \"weise_zu('T-3', person='Kim', prioritaet='hoch') -> ('T-3', 'Kim', 'hoch')\".\n"
    "Tipp: Erst die Argumente nach Position mit repr, dann die nach Namen als name=repr(wert)."
)

# Benannte Argumente in der Reihenfolge des Aufrufs
PROTOKOLL.clear()
weise_zu("T-4", prioritaet="niedrig", person="Ali")
assert PROTOKOLL == ["weise_zu('T-4', prioritaet='niedrig', person='Ali') -> ('T-4', 'Ali', 'niedrig')"], (
    f"weise_zu('T-4', prioritaet='niedrig', person='Ali') protokolliert {PROTOKOLL!r}; die benannten Argumente "
    "sollen in der Reihenfolge des Aufrufs erscheinen.\nTipp: for name, wert in kwargs.items()."
)

# Eine Funktion ohne Argumente und ohne Ergebnis
@protokolliere
def ping():
    """Prüft, ob das Ticketsystem erreichbar ist."""


# Ohne Argumente und mit Ergebnis None
PROTOKOLL.clear()
ergebnis = ping()
assert ergebnis is None and PROTOKOLL == ["ping() -> None"], (
    f"ping() ohne Argumente ergibt {ergebnis!r} und protokolliert {PROTOKOLL!r}; erwartet war None und ['ping() -> None']."
)

# Eine Ausnahme wird protokolliert und unverändert weitergegeben
fehler_original = KeyError("T-404")


@protokolliere
def oeffne(ticket):
    """Öffnet ein Ticket, das es nicht gibt."""
    raise fehler_original


PROTOKOLL.clear()
try:
    oeffne("T-404")
    gefangen = None
except Exception as fehler:
    gefangen = fehler
assert gefangen is fehler_original and PROTOKOLL == ["oeffne('T-404') -> Fehler: KeyError"], (
    f"oeffne('T-404') löst {gefangen!r} aus und protokolliert {PROTOKOLL!r}; erwartet war derselbe KeyError, der in "
    "oeffne ausgelöst wurde, und die Zeile \"oeffne('T-404') -> Fehler: KeyError\".\n"
    "Tipp: Fangen Sie die Ausnahme mit except Exception, schreiben Sie ins Protokoll und geben Sie sie mit raise "
    "ohne Argument weiter."
)

# Nach einer Ausnahme geht es normal weiter, die Zeilen stehen in der Reihenfolge der Aufrufe
PROTOKOLL.clear()
for ticket in ["T-1", "T-99", "T-2"]:
    try:
        schliesse(ticket)
    except ValueError:
        pass
erwartet = ["schliesse('T-1') -> None", "schliesse('T-99') -> Fehler: ValueError", "schliesse('T-2') -> None"]
assert PROTOKOLL == erwartet, f"schliesse für T-1, T-99 und T-2 protokolliert {PROTOKOLL!r}, erwartet war {erwartet!r}."

# functools.wraps übernimmt Name, Docstring und __wrapped__
angaben = (eskaliere.__name__, eskaliere.__doc__, getattr(weise_zu, "__wrapped__", None) is not None)
assert angaben == ("eskaliere", "Hebt ein Ticket auf eine höhere Eskalationsstufe.", True), (
    f"Die dekorierte Funktion eskaliere heißt {angaben[0]!r} mit Docstring {angaben[1]!r}, __wrapped__ vorhanden: "
    f"{angaben[2]} (geprüft an weise_zu); erwartet waren der Name und Docstring der ursprünglichen Funktion und __wrapped__.\n"
    "Tipp: Schreiben Sie @functools.wraps(funktion) über die Hüllfunktion."
)

# __wrapped__ ist das Original: sein Aufruf landet nicht im Protokoll
PROTOKOLL.clear()
original = getattr(eskaliere, "__wrapped__", None)
ergebnis = original("T-5", 3) if original is not None else "kein __wrapped__ (functools.wraps fehlt)"
assert ergebnis == "T-5 auf Stufe 3" and PROTOKOLL == [], (
    f"eskaliere.__wrapped__('T-5', 3) ergibt {ergebnis!r} und protokolliert {PROTOKOLL!r}; erwartet war "
    "'T-5 auf Stufe 3' ohne Protokollzeile."
)

# Der Dekorator ruft die Funktion genau einmal auf
zaehler = []


@protokolliere
def zaehle(wert):
    """Merkt sich jeden Aufruf."""
    zaehler.append(wert)
    return len(zaehler)


PROTOKOLL.clear()
ergebnis = (zaehle(1), zaehle(2))
assert ergebnis == (1, 2) and zaehler == [1, 2], (
    f"Zwei Aufrufe der dekorierten Funktion rufen das Original {len(zaehler)}-mal auf (Ergebnisse {ergebnis!r}); "
    "erwartet war genau ein Aufruf des Originals je Aufruf der dekorierten Funktion.\nTipp: Rufen Sie funktion(*args, **kwargs) nur einmal auf und "
    "merken Sie sich das Ergebnis."
)

# Viele zufällige Aufrufe gegen eine Nachrechnung
zufall = Zufall(4022)


@protokolliere
def bewerte(*werte, **angaben):
    """Gibt die Summe der Werte zurück, bei negativer Summe einen Fehler."""
    summe = sum(werte) + sum(angaben.values())
    if summe < 0:
        raise ArithmeticError("negativ")
    return summe


for _ in range(300):
    werte = [zufall.randint(-5, 9) for _ in range(zufall.randint(0, 4))]
    namen = zufall.sample(["a", "b", "prio", "x1", "z"], zufall.randint(0, 3))
    angaben = {name: zufall.randint(-5, 9) for name in namen}
    summe = sum(werte) + sum(angaben.values())
    teile = [repr(wert) for wert in werte] + [f"{name}={wert!r}" for name, wert in angaben.items()]
    ende = f"{summe!r}" if summe >= 0 else "Fehler: ArithmeticError"
    erwartet = f"bewerte({', '.join(teile)}) -> {ende}"
    PROTOKOLL.clear()
    try:
        ergebnis = bewerte(*werte, **angaben)
    except ArithmeticError:
        ergebnis = None
    assert PROTOKOLL == [erwartet] and ergebnis == (summe if summe >= 0 else None), (
        f"bewerte(*{werte}, **{angaben}) ergibt {ergebnis!r} und protokolliert {PROTOKOLL!r}; erwartet war {erwartet!r}."
    )

# An der oberen Grenze: 100 000 Aufrufe
PROTOKOLL.clear()
for nummer in range(100000):
    eskaliere(f"T-{nummer}")
assert len(PROTOKOLL) == 100000 and PROTOKOLL[-1] == "eskaliere('T-99999') -> 'T-99999 auf Stufe 1'", (
    f"Nach 100 000 Aufrufen hat PROTOKOLL {len(PROTOKOLL)} Zeilen, die letzte {PROTOKOLL[-1:]!r}; erwartet waren "
    "100 000 Zeilen, die letzte \"eskaliere('T-99999') -> 'T-99999 auf Stufe 1'\"."
)
