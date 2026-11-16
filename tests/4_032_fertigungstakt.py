# Automatisch erzeugt aus lehrkraft/muster/4_032_fertigungstakt.py - nicht von Hand ändern.
# vorlage-hash: acec4767b5241714
# text-hash: b07aa82e10d6ddb9
# thema: kontrollfluss
# inhalt: Iterator-Protokoll

def restzeit_von_hand(minuten, takt):
    """Vergleichslösung mit range: alle positiven Werte und dann 0."""
    return list(range(minuten, 0, -takt)) + [0]


def zeitplan_von_hand(schritte):
    """Vergleichslösung mit Summen der vorherigen Dauern."""
    ergebnis = []
    for index, (name, dauer) in enumerate(schritte):
        beginn = sum(d for _, d in schritte[:index])
        ergebnis.append((name, beginn, beginn + dauer))
    return ergebnis


def erste_werte(iterator, anzahl):
    """Holt höchstens anzahl Werte mit next; bricht bei StopIteration ab."""
    werte = []
    for _ in range(anzahl):
        try:
            werte.append(next(iterator))
        except StopIteration:
            break
    return werte


def ist_erschoepft(iterator):
    """Prüft, ob next(iterator) StopIteration auslöst."""
    try:
        next(iterator)
    except StopIteration:
        return True
    return False


MONTAGE = [("Zuschnitt", 15), ("Montage", 40), ("Prüfung", 10)]

# Restzeit liefert mit next den ersten Wert
r = Restzeit(10, 3)
try:
    erster = next(r)
except TypeError as fehler:
    erster = f"TypeError: {fehler}"
assert erster == 10, (
    f"next(Restzeit(10, 3)) ergibt {erster!r}, erwartet war 10.\n"
    "Tipp: Schreiben Sie eine Methode __next__, die den aktuellen Wert zurückgibt und den Stand weiterzählt."
)

# Restzeit zählt im Takt herunter
werte = erste_werte(Restzeit(10, 3), 4)
assert werte == [10, 7, 4, 1], f"Die ersten vier Werte von Restzeit(10, 3) sind {werte!r}, erwartet waren [10, 7, 4, 1]."

# Restzeit ist ein Iterator: iter(r) gibt r selbst zurück
r = Restzeit(10, 3)
try:
    selbst = iter(r) is r
except TypeError:
    selbst = False
assert selbst, "iter(Restzeit(10, 3)) soll das Objekt selbst liefern.\nTipp: __iter__ eines Iterators enthält return self."

# Restzeit endet mit genau einer 0
werte = erste_werte(Restzeit(10, 3), 10)
assert werte == [10, 7, 4, 1, 0], (
    f"Restzeit(10, 3) liefert {werte!r}, erwartet war [10, 7, 4, 1, 0].\n"
    "Tipp: Ist der nächste Wert 0 oder kleiner, liefern Sie einmal 0 und danach StopIteration."
)

# Restzeit mit anderen Zahlen (nicht fest hinschreiben!)
werte = erste_werte(Restzeit(9, 3), 10)
assert werte == [9, 6, 3, 0], f"Restzeit(9, 3) liefert {werte!r}, erwartet war [9, 6, 3, 0] (die 0 nur einmal)."

# Restzeit in einer for-Schleife
try:
    werte = list(Restzeit(25, 10))
except TypeError as fehler:
    werte = f"TypeError: {fehler}"
assert werte == [25, 15, 5, 0], f"list(Restzeit(25, 10)) ergibt {werte!r}, erwartet war [25, 15, 5, 0]."

# Nach dem Ende kommt immer wieder StopIteration
r = Restzeit(4, 2)
erste_werte(r, 10)
assert ist_erschoepft(r) and ist_erschoepft(r), (
    "Nachdem Restzeit(4, 2) alle Werte geliefert hat, soll jeder weitere Aufruf von next StopIteration auslösen."
)

# Restzeit(0, takt) liefert nur 0
werte = erste_werte(Restzeit(0, 5), 10)
assert werte == [0], f"Restzeit(0, 5) liefert {werte!r}, erwartet war [0]."

# Takt größer als die Minuten
werte = erste_werte(Restzeit(3, 10**9), 10)
assert werte == [3, 0], f"Restzeit(3, 10**9) liefert {werte!r}, erwartet war [3, 0]."

# Takt 1 zählt jede Minute
werte = erste_werte(Restzeit(3, 1), 10)
assert werte == [3, 2, 1, 0], f"Restzeit(3, 1) liefert {werte!r}, erwartet war [3, 2, 1, 0]."

# Restzeit rechnet nicht alles im Voraus aus
def drei_werte():
    """Legt einen sehr langen Countdown an und holt nur drei Werte."""
    return erste_werte(Restzeit(10**9, 1), 3)


werte, schritte = zaehle_schritte(drei_werte)
assert werte == [10**9, 10**9 - 1, 10**9 - 2] and schritte <= 100, (
    f"Restzeit(10**9, 1) liefert als erste Werte {werte!r} nach {schritte} Schritten; erwartet waren "
    f"[{10**9}, {10**9 - 1}, {10**9 - 2}] nach höchstens 100 Schritten.\n"
    "Tipp: Merken Sie sich in __init__ nur den nächsten Wert und rechnen Sie in __next__ einen Schritt weiter."
)

# Zeitplan liefert die Schritte mit Beginn und Ende
try:
    werte = erste_werte(Zeitplan(MONTAGE), 10)
except TypeError as fehler:
    werte = f"TypeError: {fehler}"
erwartet = [("Zuschnitt", 0, 15), ("Montage", 15, 55), ("Prüfung", 55, 65)]
assert werte == erwartet, (
    f"Zeitplan({MONTAGE}) liefert {werte!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Merken Sie sich den Index des nächsten Schritts und die Minute, bei der er beginnt."
)

# Zeitplan ist ein Iterator und danach erschöpft
z = Zeitplan(MONTAGE)
try:
    selbst = iter(z) is z
except TypeError:
    selbst = False
erste_werte(z, 10)
assert selbst and ist_erschoepft(z), "iter(Zeitplan(…)) soll das Objekt selbst liefern, und nach dem letzten Schritt kommt StopIteration."

# Zeitplan mit Dauer 0
schritte = [("Freigabe", 0), ("Lackieren", 30), ("Kontrolle", 0)]
werte = erste_werte(Zeitplan(schritte), 10)
erwartet = [("Freigabe", 0, 0), ("Lackieren", 0, 30), ("Kontrolle", 30, 30)]
assert werte == erwartet, f"Zeitplan({schritte}) liefert {werte!r}, erwartet war {erwartet!r}."

# Zeitplan ohne Schritte
assert erste_werte(Zeitplan([]), 10) == [], f"Zeitplan([]) liefert {erste_werte(Zeitplan([]), 10)!r}, erwartet war []."

# Zeitplan verändert die Liste nicht
schritte = list(MONTAGE)
erste_werte(Zeitplan(schritte), 10)
assert schritte == MONTAGE, f"Nach dem Durchlaufen von Zeitplan(schritte) ist schritte {schritte!r}, erwartet war sie unverändert."

# Prozess lässt sich mit for durchlaufen
try:
    werte = list(Prozess(MONTAGE))
except TypeError as fehler:
    werte = f"TypeError: {fehler}"
erwartet = [("Zuschnitt", 0, 15), ("Montage", 15, 55), ("Prüfung", 55, 65)]
assert werte == erwartet, f"list(Prozess({MONTAGE})) ergibt {werte!r}, erwartet war {erwartet!r}."

# Prozess lässt sich mehrmals durchlaufen
prozess = Prozess(MONTAGE)
try:
    erster_lauf = list(prozess)
    zweiter_lauf = list(prozess)
except TypeError as fehler:
    erster_lauf = zweiter_lauf = f"TypeError: {fehler}"
assert erster_lauf == zweiter_lauf == erwartet, (
    f"Zweimal list(prozess) ergibt {erster_lauf!r} und {zweiter_lauf!r}, erwartet war beide Male {erwartet!r}.\n"
    "Tipp: Prozess.__iter__ gibt bei jedem Aufruf einen neuen Zeitplan zurück, nicht self."
)

# iter(prozess) liefert jedes Mal einen neuen Zeitplan
prozess = Prozess(MONTAGE)
erster = iter(prozess)
zweiter = iter(prozess)
assert isinstance(erster, Zeitplan) and erster is not zweiter and erster is not prozess, (
    f"iter(prozess) ergibt {erster!r} und beim zweiten Mal {zweiter!r}; erwartet waren zwei verschiedene Zeitplan-Objekte."
)

# Prozess ist selbst kein Iterator
assert not hasattr(Prozess(MONTAGE), "__next__"), (
    "Prozess hat eine Methode __next__, soll aber nur iterierbar sein; das Weiterzählen übernimmt Zeitplan."
)

# Zwei verschachtelte Schleifen über denselben Prozess sind unabhängig
prozess = Prozess([("A", 1), ("B", 2)])
paare = [(aussen[0], innen[0]) for aussen in prozess for innen in prozess]
assert paare == [("A", "A"), ("A", "B"), ("B", "A"), ("B", "B")], (
    f"Zwei verschachtelte Schleifen über Prozess([('A', 1), ('B', 2)]) ergeben die Paare {paare!r}, "
    "erwartet waren alle vier Paare."
)

# Die Klassen benutzen kein yield, sondern das Iterator-Protokoll
assert hasattr(Restzeit, "__next__") and hasattr(Zeitplan, "__next__"), (
    "Restzeit und Zeitplan sollen eine Methode __next__ haben, statt mit yield einen Generator zu bauen."
)

# 300 zufällige Countdowns
zufall = Zufall(4032)
for _ in range(300):
    minuten = zufall.randint(0, 60)
    takt = zufall.randint(1, 15)
    werte = erste_werte(Restzeit(minuten, takt), 100)
    erwartet = restzeit_von_hand(minuten, takt)
    assert werte == erwartet, f"Restzeit({minuten}, {takt}) liefert {werte!r}, erwartet war {erwartet!r}."

# 300 zufällige Prozesse
for _ in range(300):
    schritte = [(f"S{nummer}", zufall.randint(0, 50)) for nummer in range(zufall.randint(0, 8))]
    werte = list(Prozess(schritte))
    erwartet = zeitplan_von_hand(schritte)
    assert werte == erwartet, f"list(Prozess({schritte})) ergibt {werte!r}, erwartet war {erwartet!r}."

# Obere Grenze: 100 000 Schritte
schritte = [(f"S{nummer}", 10**4) for nummer in range(100000)]
werte = list(Prozess(schritte))
assert len(werte) == 100000 and werte[-1] == ("S99999", 999990000, 10**9), (
    f"Bei 100 000 Schritten zu je 10**4 Minuten ergibt list(Prozess(…)) {len(werte)} Einträge, der letzte "
    f"{werte[-1] if werte else None!r}; erwartet waren 100000 Einträge, der letzte ('S99999', 999990000, {10**9})."
)

# Obere Grenze: großer Countdown mit großem Takt
werte = list(Restzeit(10**9, 10**8 + 1))
assert werte == restzeit_von_hand(10**9, 10**8 + 1), f"list(Restzeit(10**9, 10**8 + 1)) ergibt {werte!r}."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[10, 7, 4, 1, 0]\nZuschnitt: Minute 0 bis 15\nMontage: Minute 15 bis 55\nPrüfung: Minute 55 bis 65"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
