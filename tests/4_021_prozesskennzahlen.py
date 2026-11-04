# Automatisch erzeugt aus lehrkraft/muster/4_021_prozesskennzahlen.py - nicht von Hand ändern.
# vorlage-hash: 728b50185d2d18d4
# text-hash: 65c82667a93a45a2
# thema: funktionen
# inhalt: Closures und nonlocal

def gleich(a, b):
    """Vergleicht Zahlen und Tupel aus Zahlen mit einer kleinen Toleranz für Kommazahlen."""
    if isinstance(a, tuple) and isinstance(b, tuple):
        return len(a) == len(b) and all(gleich(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= 1e-9 * max(1, abs(b))
    return False


# normierer aus dem Beispiel
auf_eins = normierer(10, 50)
ergebnis = (auf_eins(30), auf_eins(10), auf_eins(50), auf_eins(60), auf_eins(0))
assert gleich(ergebnis, (0.5, 0.0, 1.0, 1.25, -0.25)), (
    f"normierer(10, 50) rechnet 30, 10, 50, 60 und 0 um in {ergebnis!r}, erwartet war (0.5, 0.0, 1.0, 1.25, -0.25).\n"
    "Tipp: (x - kleinster) / (groesster - kleinster); Werte außerhalb des Bereichs werden nicht abgeschnitten."
)

# Zwei Normierer stören sich nicht
a = normierer(0, 10)
b = normierer(-100, 100)
ergebnis = (a(5), b(5), a(10))
assert gleich(ergebnis, (0.5, 0.525, 1.0)), (
    f"Mit a = normierer(0, 10) und b = normierer(-100, 100) ergeben a(5), b(5) und a(10) {ergebnis!r}, "
    "erwartet war (0.5, 0.525, 1.0).\nTipp: Jede zurückgegebene Funktion muss ihre eigenen Grenzen benutzen, "
    "nicht globale Variablen."
)

# Mit Kommazahlen und an den Grenzen
ergebnis = (normierer(-10**6, 10**6)(0), normierer(0.5, 1.5)(1.25), normierer(-3, -1)(-2))
assert gleich(ergebnis, (0.5, 0.75, 0.5)), (
    f"normierer(-10**6, 10**6)(0), normierer(0.5, 1.5)(1.25) und normierer(-3, -1)(-2) ergeben {ergebnis!r}, "
    "erwartet war (0.5, 0.75, 0.5)."
)

# Ungültige Grenzen lösen sofort einen ValueError mit beiden Werten aus
for kleinster, groesster in [(5, 5), (7, 3), (0.5, -0.5)]:
    try:
        normierer(kleinster, groesster)
        meldung = None
    except ValueError as fehler:
        meldung = str(fehler)
    assert meldung is not None and str(kleinster) in meldung and str(groesster) in meldung, (
        f"normierer({kleinster}, {groesster}) soll sofort einen ValueError auslösen, dessen Meldung {kleinster} und "
        f"{groesster} enthält; bekommen: {'kein ValueError' if meldung is None else repr(meldung)}.\n"
        "Tipp: Prüfen Sie in normierer selbst, nicht erst in der zurückgegebenen Funktion; dort kommt die "
        "Division durch 0 erst später."
    )

# auswertung aus dem Beispiel, mit zwei unabhängigen Auswertungen
verpacken = auswertung()
schritte = [verpacken(12), verpacken(20)]
retouren = auswertung()
schritte.append(retouren(45))
schritte.append(verpacken(4))
erwartet = [(1, 12.0, 12), (2, 16.0, 20), (1, 45.0, 45), (3, 12.0, 20)]
assert all(gleich(x, y) for x, y in zip(schritte, erwartet)) and len(schritte) == 4, (
    f"verpacken(12), verpacken(20), retouren(45), verpacken(4) ergeben {schritte!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Legen Sie anzahl, summe und laengste in auswertung an, nicht global, und kündigen Sie sie in "
    "erfasse mit nonlocal an."
)

# Der Wert 0 und mehrfach derselbe Wert
null = auswertung()
ergebnis = (null(0), null(0), null(0))
assert gleich(ergebnis, ((1, 0.0, 0), (2, 0.0, 0), (3, 0.0, 0))), (
    f"Dreimal erfasse(0) ergibt {ergebnis!r}, erwartet war ((1, 0.0, 0), (2, 0.0, 0), (3, 0.0, 0)).\n"
    "Tipp: Auch der Messwert 0 zählt mit; prüfen Sie Ihre Bedingungen, ob sie 0 als „kein Wert“ behandeln."
)

# Der Zustand steckt in der Closure, nicht in globalen Variablen
def neue_globale_namen():
    """Benutzt eine Auswertung und gibt die dabei neu angelegten globalen Namen und die Funktion zurück."""
    vorher = set(globals())
    erfasse = auswertung()
    erfasse(3)
    erfasse(9)
    return set(globals()) - vorher, erfasse


neu, messung = neue_globale_namen()
assert neu == set() and messung.__closure__ is not None, (
    f"auswertung() und erfasse legen neue globale Variablen an: {sorted(neu)!r}, oder erfasse hat keine Closure.\n"
    "Tipp: Alles, was erfasse sich merken soll, gehört als lokale Variable in auswertung."
)

# Viele unabhängige Auswertungen mit zufälligen Werten
zufall = Zufall(4021)
auswertungen = [auswertung() for _ in range(10)]
werte = [[] for _ in range(10)]
for _ in range(500):
    nummer = zufall.randrange(10)
    minuten = zufall.choice([0, 1, 7, 60, zufall.randint(0, 10**6)])
    werte[nummer].append(minuten)
    ergebnis = auswertungen[nummer](minuten)
    erwartet = (len(werte[nummer]), sum(werte[nummer]) / len(werte[nummer]), max(werte[nummer]))
    assert gleich(ergebnis, erwartet), (
        f"Auswertung {nummer} nach den Werten {werte[nummer][-6:]} (die letzten): erfasse liefert {ergebnis!r}, "
        f"erwartet war {erwartet!r}."
    )

# Zufällige Normierer gegen eine Nachrechnung
for _ in range(300):
    kleinster = zufall.randint(-10**6, 10**6 - 1)
    groesster = zufall.randint(kleinster + 1, 10**6)
    x = zufall.randint(-10**6, 10**6)
    ergebnis = normierer(kleinster, groesster)(x)
    erwartet = (x - kleinster) / (groesster - kleinster)
    assert gleich(ergebnis, erwartet), f"normierer({kleinster}, {groesster})({x}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: 100 000 Werte, jeder Aufruf O(1)
erfasse = auswertung()
for minuten in range(99999):
    erfasse(minuten % 1000)
_, schritte_spaet = zaehle_schritte(erfasse, 10**6)
_, schritte_frueh = zaehle_schritte(auswertung(), 10**6)
ergebnis = erfasse(0)
erwartet = (100001, (sum(m % 1000 for m in range(99999)) + 10**6) / 100001, 10**6)
assert gleich(ergebnis, erwartet) and schritte_spaet <= schritte_frueh + 5, (
    f"Nach 100 000 Werten liefert erfasse {ergebnis!r} (erwartet {erwartet!r}); der 100 000. Aufruf braucht "
    f"{schritte_spaet} Schritte, der erste {schritte_frueh}.\nTipp: Merken Sie sich Anzahl, Summe und Maximum, "
    "statt alle Werte in einer Liste zu sammeln und jedes Mal neu auszurechnen."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "0.5 0.0 1.25\n(2, 16.0, 20)"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
