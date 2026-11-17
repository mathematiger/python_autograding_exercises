# Automatisch erzeugt aus lehrkraft/muster/3_035_zusatzmodule.py - nicht von Hand ändern.
# vorlage-hash: 7458e4429718e87c
# text-hash: c1148c98b03fc299
# thema: algorithmen
# inhalt: Backtracking: alle Teilmengen

def geordnet(auswahlen):
    """Bringt eine Liste von Auswahlen in eine feste Reihenfolge, damit die Reihenfolge der Auswahlen egal ist."""
    return sorted(tuple(auswahl) for auswahl in auswahlen)


def vergleich_kombinationen(module):
    """Vergleichslösung ohne Rekursion: Die Bits der Zahlen 0 bis 2**n - 1 sagen, welches Modul dabei ist."""
    auswahlen = []
    for zahl in range(2 ** len(module)):
        auswahlen.append([module[stelle] for stelle in range(len(module)) if zahl >> stelle & 1])
    return auswahlen


def pruefe_kombinationen(module):
    """Ruft kombinationen(module) auf und liefert eine Fehlerbeschreibung oder None."""
    ergebnis = kombinationen(list(module))
    erwartet = geordnet(vergleich_kombinationen(module))
    if not isinstance(ergebnis, list):
        return f"kombinationen({module!r}) liefert {ergebnis!r}, erwartet war eine Liste von Listen."
    bekommen = geordnet(ergebnis)
    if bekommen == erwartet:
        return None
    if len(ergebnis) == len(erwartet):
        text = f"kombinationen({module!r}) liefert zwar {len(ergebnis)} Auswahlen, aber nicht die richtigen."
    else:
        text = f"kombinationen({module!r}) liefert {len(ergebnis)} Auswahlen, erwartet waren {len(erwartet)}."
    if len(set(bekommen)) < len(bekommen):
        text += "\nManche Auswahlen kommen mehrfach vor."
    if len(ergebnis) == len(erwartet) and len(set(bekommen)) == 1:
        text += "\nTipp: Alle Auswahlen sind gleich. Speichern Sie eine Kopie (auswahl[:]), nicht die Liste selbst."
    # Mengen einmal vorher bilden, sonst dauert der Vergleich bei 32 768 Auswahlen zu lange
    erwartet_menge = set(erwartet)
    bekommen_menge = set(bekommen)
    falsch = [list(a) for a in bekommen if a not in erwartet_menge]
    if falsch:
        text += f"\nDiese Auswahlen sind falsch (Namen fehlen, doppelt oder in anderer Reihenfolge als in module): {falsch[:3]}"
    fehlend = [list(a) for a in erwartet if a not in bekommen_menge]
    if fehlend:
        text += f"\nEs fehlen zum Beispiel: {fehlend[:3]}"
    return text


PREISE = {"Mahnwesen": 900, "Lager": 1500, "Shop": 1200}

# kombinationen: das Beispiel mit zwei Modulen
fehler = pruefe_kombinationen(["Mahnwesen", "Lager"])
assert fehler is None, fehler

# kombinationen: drei Module ergeben acht Auswahlen (nicht fest hinschreiben!)
fehler = pruefe_kombinationen(["Mahnwesen", "Lager", "Shop"])
assert fehler is None, fehler

# kombinationen: die leere Auswahl gehört dazu
ergebnis = geordnet(kombinationen(["Lager"]))
if () not in ergebnis:
    hinweis = "\nTipp: „Gar kein Zusatzmodul“ ist auch eine Auswahl, die leere Liste []."
else:
    hinweis = ""
assert ergebnis == [(), ("Lager",)], (
    f'kombinationen(["Lager"]) liefert (geordnet) {[list(a) for a in ergebnis]}, erwartet war [[], ["Lager"]].'
    f"{hinweis}"
)

# kombinationen: ohne Module gibt es genau eine Auswahl, die leere
ergebnis = kombinationen([])
assert isinstance(ergebnis, list) and geordnet(ergebnis) == [()], (
    f"kombinationen([]) liefert {ergebnis!r}, erwartet war [[]] (eine Auswahl: keine Module).\n"
    "Tipp: Sind keine Module mehr zu entscheiden, wird die bisherige Auswahl gespeichert, auch wenn sie leer ist."
)

# kombinationen: die übergebene Liste bleibt unverändert
module = ["Mahnwesen", "Lager", "Shop"]
kombinationen(module)
assert module == ["Mahnwesen", "Lager", "Shop"], (
    f'Nach kombinationen(module) ist module {module!r}, erwartet war unverändert ["Mahnwesen", "Lager", "Shop"].'
)

# kombinationen: itertools wird nicht benutzt
assert not verwendet("combinations") and not verwendet("product"), (
    "Ihr Code benutzt itertools.combinations oder itertools.product. Bauen Sie die Auswahlen selbst rekursiv auf."
)

# kombinationen: fünf Module
fehler = pruefe_kombinationen(["A", "B", "C", "D", "E"])
assert fehler is None, fehler

# bezahlbare: das Beispiel aus der Aufgabe
ergebnis = bezahlbare(["Mahnwesen", "Lager", "Shop"], dict(PREISE), 2200)
erwartet = [[], ["Shop"], ["Lager"], ["Mahnwesen"], ["Mahnwesen", "Shop"]]
assert geordnet(ergebnis) == geordnet(erwartet), (
    f'bezahlbare(["Mahnwesen", "Lager", "Shop"], preise, 2200) liefert {ergebnis!r}, '
    f"erwartet waren (in beliebiger Reihenfolge) {erwartet}."
)

# bezahlbare: ein anderes Budget
ergebnis = bezahlbare(["Mahnwesen", "Lager", "Shop"], dict(PREISE), 1000)
assert geordnet(ergebnis) == [(), ("Mahnwesen",)], (
    f'bezahlbare(["Mahnwesen", "Lager", "Shop"], preise, 1000) liefert {ergebnis!r}, erwartet war [[], ["Mahnwesen"]].'
)

# bezahlbare: genau das Budget zu treffen ist erlaubt
ergebnis = bezahlbare(["Mahnwesen", "Lager", "Shop"], dict(PREISE), 2100)
assert ("Mahnwesen", "Shop") in geordnet(ergebnis), (
    f'bezahlbare(["Mahnwesen", "Lager", "Shop"], preise, 2100) liefert {ergebnis!r}; '
    '["Mahnwesen", "Shop"] kostet genau 2100 Euro und gehört dazu.\nTipp: Erlaubt ist kosten <= budget.'
)

# bezahlbare: Budget 0 lässt nur die leere Auswahl zu
ergebnis = bezahlbare(["Mahnwesen", "Lager"], dict(PREISE), 0)
assert geordnet(ergebnis) == [()], f'bezahlbare(["Mahnwesen", "Lager"], preise, 0) liefert {ergebnis!r}, erwartet war [[]].'

# bezahlbare: ein großes Budget lässt alle Auswahlen zu
ergebnis = bezahlbare(["Mahnwesen", "Lager", "Shop"], dict(PREISE), 10**7)
assert len(ergebnis) == 8, (
    f'bezahlbare(["Mahnwesen", "Lager", "Shop"], preise, 10**7) liefert {len(ergebnis)} Auswahlen, erwartet waren alle 8.'
)

# bezahlbare: ohne Module
ergebnis = bezahlbare([], {}, 500)
assert geordnet(ergebnis) == [()], f"bezahlbare([], {{}}, 500) liefert {ergebnis!r}, erwartet war [[]]."

# Viele zufällige Modullisten und Budgets
zufall = Zufall(3035)
fehlerfall = None
for runde in range(200):
    anzahl = runde % 9
    module = [f"M{nummer}" for nummer in zufall.sample(range(100), anzahl)]
    preise = {modul: zufall.randint(1, 10**6) for modul in module}
    budget = zufall.randint(0, 3 * 10**6)
    fehler = pruefe_kombinationen(module)
    erwartet = geordnet(a for a in vergleich_kombinationen(module) if sum(preise[m] for m in a) <= budget)
    bekommen = geordnet(bezahlbare(list(module), dict(preise), budget))
    if fehler is not None:
        fehlerfall = fehler
        break
    if bekommen != erwartet:
        fehlerfall = (
            f"bezahlbare({module!r}, {preise!r}, {budget}) liefert (geordnet) {[list(a) for a in bekommen]},\n"
            f"erwartet war (geordnet) {[list(a) for a in erwartet]}."
        )
        break
assert fehlerfall is None, fehlerfall

# Obere Grenze: 15 Module, 32 768 Auswahlen
module = [f"Modul{nummer}" for nummer in range(15)]
fehler = pruefe_kombinationen(module)
assert fehler is None, fehler

# Obere Grenze: bezahlbare mit 15 Modulen
preise = {modul: 1000 * (nummer + 1) for nummer, modul in enumerate(module)}
erwartet = geordnet(a for a in vergleich_kombinationen(module) if sum(preise[m] for m in a) <= 20000)
bekommen = geordnet(bezahlbare(list(module), dict(preise), 20000))
assert bekommen == erwartet, (
    f"Bei 15 Modulen mit Preisen 1000, 2000, …, 15000 und Budget 20000 liefert bezahlbare {len(bekommen)} Auswahlen, "
    f"erwartet waren {len(erwartet)}."
)
