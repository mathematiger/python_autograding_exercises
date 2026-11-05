# Automatisch erzeugt aus lehrkraft/muster/4_023_kostendeckel.py - nicht von Hand ändern.
# vorlage-hash: 00883ea2ee92563f
# text-hash: 3e7d08ae09fe1b31
# thema: funktionen
# inhalt: Dekoratoren mit Argumenten

def fehler_bei(aufruf):
    """Führt aufruf() aus und gibt die ausgelöste Ausnahme zurück, sonst None."""
    try:
        aufruf()
    except Exception as fehler:
        return fehler
    return None


# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "kauf: 25499.7 liegt über dem Budget von 25000\n24199.72 25000 kauf"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"

# runde rundet auf die angegebenen Stellen
ergebnisse = [runde(stellen)(lambda: 1234.56789)() for stellen in range(5)]
assert ergebnisse == [1235, 1234.6, 1234.57, 1234.568, 1234.5679], (
    f"runde(0) bis runde(4) machen aus 1234.56789 die Werte {ergebnisse!r}, erwartet war "
    "[1235, 1234.6, 1234.57, 1234.568, 1234.5679].\nTipp: round(ergebnis, stellen)."
)


@runde(1)
def leasing(rate, monate, *, anzahlung=0):
    """Kosten beim Leasing."""
    return anzahlung + rate * monate


# runde reicht Argumente nach Position und nach Namen weiter
ergebnis = (leasing(19.99, 36), leasing(rate=19.99, monate=36, anzahlung=100.04))
assert ergebnis == (719.6, 819.7), (
    f"leasing(19.99, 36) und leasing(rate=19.99, monate=36, anzahlung=100.04) mit @runde(1) ergeben {ergebnis!r}, "
    "erwartet war (719.6, 819.7).\nTipp: Die Hüllfunktion nimmt *args und **kwargs und reicht beide weiter."
)

# Ungültige Stellen werden schon beim Aufruf von runde abgelehnt
for stellen in [-1, 5, 2.0, True, "2", None]:
    fehler = fehler_bei(lambda: runde(stellen))
    assert isinstance(fehler, ValueError), (
        f"runde({stellen!r}) löst {fehler!r} aus, erwartet war ein ValueError.\n"
        "Tipp: Prüfen Sie stellen in runde selbst, vor der Definition des Dekorators; True und 2.0 sind keine "
        "gültigen Stellen."
    )

@budget(1000)
def lizenzen(anzahl, preis):
    """Kosten für Lizenzen."""
    return anzahl * preis


# budget lässt Ergebnisse bis einschließlich grenze durch
ergebnis = (lizenzen(10, 99.5), lizenzen(10, 100), lizenzen(0, 5), lizenzen(3, -2))
assert ergebnis == (995.0, 1000, 0, -6), (
    f"lizenzen(10, 99.5), (10, 100), (0, 5) und (3, -2) mit @budget(1000) ergeben {ergebnis!r}, erwartet war "
    "(995.0, 1000, 0, -6).\nTipp: Genau gleich der Grenze ist erlaubt; geben Sie das Ergebnis unverändert zurück."
)

# Über der Grenze kommt ein ValueError mit Name, Ergebnis und Grenze
fehler = fehler_bei(lambda: lizenzen(11, 100))
meldung = str(fehler)
assert isinstance(fehler, ValueError) and "lizenzen" in meldung and "1100" in meldung and "1000" in meldung, (
    f"lizenzen(11, 100) mit @budget(1000) löst {fehler!r} aus, erwartet war ein ValueError, dessen Meldung den Namen "
    "lizenzen, das Ergebnis 1100 und die Grenze 1000 nennt.\nTipp: funktion.__name__ ist der Name der Funktion."
)

# Ein negatives Budget wird schon beim Aufruf von budget abgelehnt, 0 ist erlaubt
fehler = fehler_bei(lambda: budget(-0.01))
null = fehler_bei(lambda: budget(0)(lambda: 0)())
assert isinstance(fehler, ValueError) and null is None, (
    f"budget(-0.01) löst {fehler!r} aus und budget(0) für eine Funktion mit Ergebnis 0 {null!r}; erwartet war ein "
    "ValueError und kein Fehler.\nTipp: Prüfen Sie grenze in budget selbst, bevor Sie den Dekorator definieren."
)

# Das Attribut budget nennt die Grenze
assert getattr(lizenzen, "budget", None) == 1000 and getattr(kauf, "budget", None) == 25000, (
    f"lizenzen.budget ist {getattr(lizenzen, 'budget', None)!r} und kauf.budget {getattr(kauf, 'budget', None)!r}, "
    "erwartet war 1000 und 25000.\nTipp: Setzen Sie im Dekorator huelle.budget = grenze, bevor Sie huelle zurückgeben."
)

# Jeder Aufruf von budget hat seine eigene Grenze
klein = budget(10)
gross = budget(10**9)


@klein
def kurs():
    """Kosten für einen Kurs."""
    return 50


@gross
def server():
    """Kosten für einen Server."""
    return 50


ergebnis = (type(fehler_bei(kurs)).__name__, server())
assert ergebnis == ("ValueError", 50), (
    f"Mit budget(10) und budget(10**9) für zwei Funktionen mit Ergebnis 50 ergibt sich {ergebnis!r}, erwartet war "
    "('ValueError', 50): Jeder Dekorator merkt sich seine eigene Grenze."
)

# Ein Dekorator aus budget(…) lässt sich für mehrere Funktionen benutzen
deckel = budget(100)
a = deckel(lambda x: x)
b = deckel(lambda x: 2 * x)
ergebnis = (a(80), type(fehler_bei(lambda: b(80))).__name__)
assert ergebnis == (80, "ValueError"), (
    f"deckel = budget(100) auf zwei Funktionen angewendet ergibt {ergebnis!r}, erwartet war (80, 'ValueError')."
)

# functools.wraps übernimmt Name und Docstring
angaben = (kauf.__name__, kauf.__doc__, leasing.__name__, lizenzen.__doc__)
erwartet = ("kauf", "Gesamtkosten beim Kauf: Anschaffung plus Betrieb über die Jahre.", "leasing", "Kosten für Lizenzen.")
assert angaben == erwartet, (
    f"Name und Docstring der dekorierten Funktionen sind {angaben!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Schreiben Sie @functools.wraps(funktion) über jede Hüllfunktion."
)

@budget(100)
@runde(0)
def gerundet_geprueft():
    """100.4 wird erst auf 100 gerundet und dann geprüft."""
    return 100.4


@runde(0)
@budget(100)
def geprueft_gerundet():
    """100.4 wird erst geprüft und dann gerundet."""
    return 100.4


# Die Reihenfolge der Dekoratoren zählt: budget prüft die gerundete Zahl
ergebnis = (gerundet_geprueft(), type(fehler_bei(geprueft_gerundet)).__name__)
assert ergebnis == (100, "ValueError"), (
    f"@budget(100) über @runde(0) ergibt für 100.4 {ergebnis[0]!r}, umgekehrt löst es {ergebnis[1]} aus; erwartet war "
    "100 und ValueError."
)

# Die Funktion wird genau einmal aufgerufen
aufrufe = []


@budget(10)
@runde(2)
def zaehle():
    """Merkt sich jeden Aufruf."""
    aufrufe.append(1)
    return 1.234


ergebnis = zaehle()
assert ergebnis == 1.23 and len(aufrufe) == 1, (
    f"zaehle() ergibt {ergebnis!r} und ruft das Original {len(aufrufe)}-mal auf, erwartet war 1.23 nach genau einem Aufruf."
)

# 300 zufällige Grenzen, Stellen und Ergebnisse
zufall = Zufall(4023)
for _ in range(300):
    stellen = zufall.randint(0, 4)
    grenze = zufall.choice([0, 1, 99.5, 1000, 10**9, zufall.randint(0, 10**6)])
    wert = zufall.choice([0, grenze, -grenze, zufall.uniform(-10**6, 10**6), zufall.randint(-10**9, 10**9)])
    gerundet = round(wert, stellen)
    funktion = budget(grenze)(runde(stellen)(lambda wert=wert: wert))
    try:
        ergebnis = funktion()
    except ValueError:
        ergebnis = "ValueError"
    erwartet = gerundet if gerundet <= grenze else "ValueError"
    assert ergebnis == erwartet, (
        f"budget({grenze!r})(runde({stellen})(funktion)) ergibt für das Ergebnis {wert!r} den Wert {ergebnis!r}, "
        f"erwartet war {erwartet!r}."
    )

# An der oberen Grenze: 100 000 Aufrufe
summe = 0
for nummer in range(100000):
    summe = summe + lizenzen(nummer % 11, 90.5)
assert summe == 45249547.5, f"100 000 Aufrufe von lizenzen ergeben zusammen {summe!r}, erwartet war 45249547.5."
