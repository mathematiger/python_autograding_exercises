# Automatisch erzeugt aus lehrkraft/muster/4_033_bandrotation.py - nicht von Hand ändern.
# vorlage-hash: c38d04d6459bd0ea
# text-hash: f80860ff34a12597
# thema: kontrollfluss
# inhalt: Iterable gegen Iterator

def erwarteter_plan(baender, tage):
    """Vergleichslösung: alle Paare (tag, band) als Liste."""
    paare = []
    index = 0
    for tag in range(1, tage + 1):
        paare.append((tag, baender[index]))
        index = index + 1
        if index == len(baender):
            index = 0
    return paare


def kurz(liste):
    """Kürzt lange Listen für Fehlermeldungen."""
    if not isinstance(liste, list) or len(liste) <= 6:
        return repr(liste)
    return f"[{liste[0]!r}, {liste[1]!r}, … {liste[-1]!r}] ({len(liste)} Einträge)"


def naechstes(iterator, wie_oft):
    """Ruft wie_oft next(iterator) auf; danach steht "StopIteration" statt weiterer Werte."""
    werte = []
    for _ in range(wie_oft):
        try:
            werte.append(next(iterator))
        except StopIteration:
            werte.append("StopIteration")
    return werte


DREI = ["Band A", "Band B", "Band C"]

# Ein PlanIterator liefert die ersten Tage
iterator = PlanIterator(Rotationsplan(DREI, 4))
werte = naechstes(iterator, 2)
assert werte == [(1, "Band A"), (2, "Band B")], (
    f"Zweimal next(PlanIterator(Rotationsplan({DREI}, 4))) ergibt {werte!r}, erwartet war "
    "[(1, 'Band A'), (2, 'Band B')].\nTipp: Der Iterator beginnt bei Tag 1 und rückt bei jedem next um einen Tag weiter."
)

# Nach dem letzten Band ist wieder das erste dran
iterator = PlanIterator(Rotationsplan(DREI, 5))
werte = naechstes(iterator, 5)
assert werte == erwarteter_plan(DREI, 5), (
    f"Fünfmal next für Rotationsplan({DREI}, 5) ergibt {werte!r}, erwartet war {erwarteter_plan(DREI, 5)!r}.\n"
    "Tipp: Das Band für Tag t ist baender[(t - 1) % len(baender)]."
)

# Nach dem letzten Tag kommt StopIteration, auch beim nächsten Mal
iterator = PlanIterator(Rotationsplan(DREI, 2))
werte = naechstes(iterator, 4)
assert werte == [(1, "Band A"), (2, "Band B"), "StopIteration", "StopIteration"], (
    f"Viermal next für Rotationsplan({DREI}, 2) ergibt {werte!r}, erwartet waren zwei Paare und dann "
    "zweimal StopIteration."
)

# Das Beispiel: list(plan) liefert alle vier Tage
plan = Rotationsplan(DREI, 4)
ergebnis = list(plan)
assert ergebnis == erwarteter_plan(DREI, 4), f"list(Rotationsplan({DREI}, 4)) ergibt {ergebnis!r}, erwartet war {erwarteter_plan(DREI, 4)!r}."

# Ein PlanIterator gibt bei iter() sich selbst zurück
iterator = PlanIterator(Rotationsplan(DREI, 4))
assert iter(iterator) is iterator, "iter(iterator) muss für einen PlanIterator das Objekt selbst zurückgeben (return self)."

# iter(plan) liefert einen PlanIterator
plan = Rotationsplan(DREI, 4)
iterator = iter(plan)
assert isinstance(iterator, PlanIterator), (
    f"iter(plan) ergibt {iterator!r}, erwartet war ein neues PlanIterator-Objekt.\n"
    "Tipp: Rotationsplan.__iter__ gibt PlanIterator(self) zurück."
)

# Jeder Aufruf von iter(plan) liefert einen neuen Iterator
plan = Rotationsplan(DREI, 4)
erster = iter(plan)
zweiter = iter(plan)
assert erster is not zweiter and erster is not plan, (
    "iter(plan) muss bei jedem Aufruf ein neues Iterator-Objekt liefern, nicht das Plan-Objekt selbst "
    "und nicht zweimal dasselbe."
)

# Der Plan lässt sich zweimal hintereinander durchlaufen
plan = Rotationsplan(DREI, 4)
zweimal = [list(plan), list(plan)]
assert zweimal == [erwarteter_plan(DREI, 4)] * 2, (
    f"Zweimal list(plan) ergibt {zweimal!r}; erwartet war zweimal {erwarteter_plan(DREI, 4)!r}.\n"
    "Tipp: Die Position gehört in den Iterator, nicht in den Plan; dann beginnt jeder Durchlauf vorn."
)

# Ein angefangener Iterator stört einen neuen nicht
plan = Rotationsplan(DREI, 4)
angefangen = iter(plan)
next(angefangen)
next(angefangen)
neu = next(iter(plan))
weiter = next(angefangen)
assert (neu, weiter) == ((1, "Band A"), (3, "Band C")), (
    "Nach zweimal next(angefangen) soll next(iter(plan)) wieder (1, 'Band A') liefern und next(angefangen) "
    f"danach (3, 'Band C'); bekommen: {neu!r} und {weiter!r}."
)

# Verschachtelte Durchläufe: Plan mit sich selbst um einen Tag versetzt vergleichen
plan = Rotationsplan(DREI, 4)
versetzt = iter(plan)
next(versetzt)
paare = list(zip(plan, versetzt))
erwartet = list(zip(erwarteter_plan(DREI, 4), erwarteter_plan(DREI, 4)[1:]))
assert paare == erwartet, f"list(zip(plan, versetzt)) mit einem um einen Tag versetzten Iterator ergibt {paare!r}, erwartet war {erwartet!r}."

# Null Tage: ein leerer Plan
plan = Rotationsplan(DREI, 0)
ergebnis = list(plan)
assert ergebnis == [], f"list(Rotationsplan({DREI}, 0)) ergibt {ergebnis!r}, erwartet war []."

# Ein einziges Band wird jeden Tag benutzt
plan = Rotationsplan(["Band X"], 3)
ergebnis = list(plan)
assert ergebnis == [(1, "Band X"), (2, "Band X"), (3, "Band X")], (
    f'list(Rotationsplan(["Band X"], 3)) ergibt {ergebnis!r}, erwartet war dreimal "Band X" an den Tagen 1 bis 3.'
)

# Jedes Paar wird erst berechnet, wenn es abgeholt wird
plan = Rotationsplan(DREI, 100000)
ergebnis, schritte = zaehle_schritte(lambda: next(iter(plan)))
assert ergebnis == (1, "Band A") and schritte <= 40, (
    f"next(iter(Rotationsplan({DREI}, 100000))) ergibt {ergebnis!r} nach {schritte} ausgeführten Zeilen; "
    "erwartet war (1, 'Band A') nach höchstens 40 Zeilen.\n"
    "Tipp: Berechnen Sie in __next__ nur das eine Paar, statt vorab eine Liste aller Tage anzulegen."
)

# Auch das Anlegen des Plans rechnet keine Tage vorab aus
_, schritte = zaehle_schritte(lambda: Rotationsplan(DREI, 100000))
assert schritte <= 20, (
    f"Rotationsplan({DREI}, 100000) braucht beim Anlegen {schritte} ausgeführte Zeilen, erwartet waren höchstens 20.\n"
    "Tipp: __init__ merkt sich nur die Bänder und die Zahl der Tage; die Paare entstehen erst in __next__."
)

# Viele zufällige Pläne, jeweils zweimal durchlaufen
zufall = Zufall(4033)
for runde in range(200):
    baender = [f"Band {nummer}" for nummer in range(1, zufall.randint(1, 8) + 1)]
    tage = zufall.choice([zufall.randint(0, 3), zufall.randint(0, 40)])
    plan = Rotationsplan(baender, tage)
    erwartet = erwarteter_plan(baender, tage)
    zweimal = [list(plan), list(plan)]
    assert zweimal == [erwartet, erwartet], (
        f"Zweimal list(Rotationsplan({baender}, {tage})) ergibt {kurz(zweimal[0])} und {kurz(zweimal[1])}, "
        f"erwartet war jeweils {kurz(erwartet)}."
    )

# Obere Grenze: 100 Bänder und 100 000 Tage
baender = [f"Band {nummer}" for nummer in range(1, 101)]
plan = Rotationsplan(baender, 100000)
ergebnis = list(plan)
erwartet = erwarteter_plan(baender, 100000)
assert ergebnis == erwartet, f"list(Rotationsplan(100 Bänder, 100000)) ergibt {kurz(ergebnis)}, erwartet war {kurz(erwartet)}."
