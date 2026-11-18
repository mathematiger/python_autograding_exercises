# Automatisch erzeugt aus lehrkraft/muster/4_033_bandrotation.py - nicht von Hand ändern.
# vorlage-hash: b0f96d19297a5125
# text-hash: a443abe3d9267073
# thema: kontrollfluss
# inhalt: Iterable gegen Iterator

import inspect


def plan_von_hand(baender, tage):
    """Vergleichslösung: alle Paare (tag, band) als Liste, mit einem eigenen Zähler für das Band."""
    ergebnis = []
    nummer = 0
    for tag in range(1, tage + 1):
        ergebnis.append((tag, baender[nummer]))
        nummer = nummer + 1
        if nummer == len(baender):
            nummer = 0
    return ergebnis


def holen(iterator, anzahl):
    """Ruft anzahl-mal next() auf; liefert (Werte, Ausnahme oder None)."""
    werte = []
    try:
        for _ in range(anzahl):
            werte.append(next(iterator))
    except Exception as ausnahme:
        return werte, ausnahme
    return werte, None


def ist_fertig(iterator):
    """Gibt zurück, ob next(iterator) StopIteration auslöst; sonst eine Beschreibung des Ergebnisses."""
    try:
        wert = next(iterator)
    except StopIteration:
        return True
    except Exception as ausnahme:
        return f"{type(ausnahme).__name__}: {ausnahme}"
    return f"ein weiterer Wert {wert!r}"


BEISPIEL = [(1, "A"), (2, "B"), (3, "C"), (4, "A"), (5, "B")]

# PlanIterator: das erste next() liefert Tag 1 mit dem ersten Band
plan = Sicherungsplan(["A", "B", "C"], 5)
werte, fehler = holen(PlanIterator(plan), 1)
assert fehler is None and werte == [(1, "A")], (
    f"next(PlanIterator(Sicherungsplan(['A', 'B', 'C'], 5))) ergibt {werte[0] if werte else fehler!r}, "
    "erwartet war (1, 'A')."
)

# PlanIterator: die Bänder kommen reihum
werte, fehler = holen(PlanIterator(Sicherungsplan(["A", "B", "C"], 5)), 5)
assert fehler is None and werte == BEISPIEL, (
    f"Fünfmal next() auf PlanIterator(Sicherungsplan(['A', 'B', 'C'], 5)) ergibt {werte}"
    + (f" und dann {type(fehler).__name__}: {fehler}" if fehler else "")
    + f", erwartet war {BEISPIEL}.\nTipp: Das Band für Tag t ist baender[(t - 1) % len(baender)]."
)

# PlanIterator: nach dem letzten Tag kommt StopIteration, und es bleibt dabei
zeiger = PlanIterator(Sicherungsplan(["A", "B"], 2))
holen(zeiger, 2)
ergebnisse = [ist_fertig(zeiger) for _ in range(3)]
assert ergebnisse == [True, True, True], (
    "Nach den beiden Tagen von Sicherungsplan(['A', 'B'], 2) soll jedes weitere next() StopIteration "
    f"auslösen; bekommen: {ergebnisse}.\nTipp: raise StopIteration, sobald tag >= plan.tage ist."
)

# PlanIterator: iter() gibt den Iterator selbst zurück
zeiger = PlanIterator(Sicherungsplan(["A"], 3))
try:
    selbst = iter(zeiger)
except Exception as ausnahme:
    selbst = ausnahme
assert selbst is zeiger, f"iter(zeiger) für einen PlanIterator ergibt {selbst!r}, erwartet war zeiger selbst."

# Sicherungsplan: list(plan) liefert alle Tage
liste = list(Sicherungsplan(["A", "B", "C"], 5))
assert liste == BEISPIEL, f"list(Sicherungsplan(['A', 'B', 'C'], 5)) ergibt {liste}, erwartet war {BEISPIEL}."

# Sicherungsplan: iter(plan) liefert einen PlanIterator, nicht den Plan selbst
plan = Sicherungsplan(["A", "B", "C"], 5)
try:
    zeiger = iter(plan)
except Exception as ausnahme:
    zeiger = ausnahme
assert isinstance(zeiger, PlanIterator), (
    f"iter(plan) ergibt {zeiger!r}, erwartet war ein neuer PlanIterator.\n"
    "Tipp: Sicherungsplan.__iter__ gibt PlanIterator(self) zurück, nicht self."
)

# Sicherungsplan: jedes iter(plan) ist ein neuer Iterator
plan = Sicherungsplan(["A", "B", "C"], 5)
erster = iter(plan)
zweiter = iter(plan)
assert erster is not zweiter, (
    "iter(plan) liefert zweimal dasselbe Objekt; erwartet war bei jedem Aufruf ein neuer PlanIterator.\n"
    "Tipp: Erzeugen Sie in __iter__ jedes Mal einen neuen PlanIterator, statt einen gemerkten zurückzugeben."
)

# Sicherungsplan: zweimal list(plan) ergibt beide Male alle Tage
plan = Sicherungsplan(["A", "B", "C"], 5)
erstes = list(plan)
zweites = list(plan)
assert erstes == BEISPIEL and zweites == BEISPIEL, (
    f"Zweimal list(plan) bei Sicherungsplan(['A', 'B', 'C'], 5) ergibt {erstes} und {zweites}; "
    "erwartet war beide Male die ganze Rotation.\n"
    "Tipp: Der Fortschritt (der Tag) gehört in den PlanIterator, nicht in den Plan."
)

# Sicherungsplan: ein neuer Iterator beginnt vorn, auch wenn ein anderer schon läuft
plan = Sicherungsplan(["A", "B", "C"], 5)
zeiger = iter(plan)
holen(zeiger, 2)
werte_neu, _ = holen(iter(plan), 1)
werte_alt, _ = holen(zeiger, 1)
assert werte_neu == [(1, "A")] and werte_alt == [(3, "C")], (
    f"Nach zweimal next(zeiger) erwartet: next(iter(plan)) == (1, 'A') und next(zeiger) == (3, 'C'); "
    f"bekommen {werte_neu} und {werte_alt}.\nTipp: Zwei Iteratoren desselben Plans haben je einen eigenen Tag."
)

# Sicherungsplan: verschachtelte Schleifen über denselben Plan
plan = Sicherungsplan(["A", "B", "C"], 5)
gleiches_band = []
for tag, band in plan:
    for anderer_tag, anderes_band in plan:
        if band == anderes_band and tag < anderer_tag:
            gleiches_band.append((tag, anderer_tag))
assert gleiches_band == [(1, 4), (2, 5)], (
    f"Zwei verschachtelte for-Schleifen über denselben Plan finden die Tagespaare {gleiches_band}, erwartet waren "
    "[(1, 4), (2, 5)] (Band A an Tag 1 und 4, Band B an Tag 2 und 5)."
)

# Ein einziges Band wird jeden Tag benutzt
liste = list(Sicherungsplan(["Notband"], 3))
assert liste == [(1, "Notband"), (2, "Notband"), (3, "Notband")], (
    f"list(Sicherungsplan(['Notband'], 3)) ergibt {liste}, erwartet war [(1, 'Notband'), (2, 'Notband'), (3, 'Notband')]."
)

# Ein Plan über 0 Tage ist leer
plan = Sicherungsplan(["A", "B"], 0)
ende = ist_fertig(iter(plan))
assert ende is True, f"next(iter(Sicherungsplan(['A', 'B'], 0))) soll StopIteration auslösen, bekommen: {ende}."

# Weniger Tage als Bänder
liste = list(Sicherungsplan(["A", "B", "C", "D"], 2))
assert liste == [(1, "A"), (2, "B")], f"list(Sicherungsplan(['A', 'B', 'C', 'D'], 2)) ergibt {liste}, erwartet war [(1, 'A'), (2, 'B')]."

# Die Liste der Bänder bleibt unverändert
baender = ["A", "B", "C"]
list(Sicherungsplan(baender, 7))
assert baender == ["A", "B", "C"], f"Nach dem Durchlaufen ist baender {baender}, erwartet war unverändert ['A', 'B', 'C']."

# Faul: ein Plan über 10**12 Tage liefert die ersten Tage sofort
plan = Sicherungsplan(["A", "B", "C"], 10**12)
werte, fehler = holen(iter(plan), 4)
assert fehler is None and werte == [(1, "A"), (2, "B"), (3, "C"), (4, "A")], (
    f"Bei Sicherungsplan(['A', 'B', 'C'], 10**12) ergeben die ersten vier next() {werte}"
    + (f" und dann {type(fehler).__name__}: {fehler}" if fehler else "")
    + ".\nTipp: Berechnen Sie das Band erst in __next__ und legen Sie keine Liste aller Tage an."
)

# Kein yield in __iter__ oder __next__
generatoren = []
for klasse, name in [(Sicherungsplan, "__iter__"), (PlanIterator, "__iter__"), (PlanIterator, "__next__")]:
    if inspect.isgeneratorfunction(getattr(klasse, name, None)):
        generatoren.append(f"{klasse.__name__}.{name}")
assert generatoren == [], (
    f"{', '.join(generatoren)} benutzt yield. Schreiben Sie das Protokoll hier von Hand: "
    "Sicherungsplan.__iter__ gibt einen neuen PlanIterator zurück, PlanIterator.__next__ liefert ein Paar."
)

# Viele zufällige Pläne, jeder zweimal durchlaufen
zufall = Zufall(4033)
for runde in range(300):
    baender = [f"Band {nummer}" for nummer in range(1, zufall.randint(1, 6) + 1)]
    tage = zufall.randint(0, 15)
    plan = Sicherungsplan(baender, tage)
    erwartet = plan_von_hand(baender, tage)
    erstes = list(plan)
    zweites = list(plan)
    assert erstes == erwartet and zweites == erwartet, (
        f"Sicherungsplan({baender}, {tage}): list(plan) ergibt {erstes}, ein zweites list(plan) {zweites}; "
        f"erwartet war beide Male {erwartet}."
    )

# Obere Grenze: 100 Bänder, 10 000 Tage
baender = [f"B{nummer:03d}" for nummer in range(100)]
erwartet = plan_von_hand(baender, 10_000)
bekommen = list(Sicherungsplan(baender, 10_000))
assert bekommen == erwartet, (
    f"Bei 100 Bändern und 10 000 Tagen erwartet {len(erwartet)} Paare, die letzten {erwartet[-2:]}; "
    f"bekommen {len(bekommen)}, die letzten {bekommen[-2:]}."
)

# Die Ausgabe des Programms stimmt
erwartete_zeile = str(BEISPIEL)
assert vergleichbar(AUSGABE) == vergleichbar(f"{erwartete_zeile}\n{erwartete_zeile}"), (
    f"Erwartete Ausgabe: zweimal {erwartete_zeile} – Ihr Programm:\n{AUSGABE}"
)
