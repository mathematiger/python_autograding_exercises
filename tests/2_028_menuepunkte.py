# Automatisch erzeugt aus lehrkraft/muster/2_028_menuepunkte.py - nicht von Hand ändern.
# vorlage-hash: beb7fb22785b518c
# text-hash: fc986869fa49bff4
# thema: datenstrukturen
# inhalt: Mengen: Schnitt, Vereinigung

def beispiel():
    """Baut die beiden Protokolle aus dem Beispiel neu."""
    return [["Datei", "Rechnung", "Datei", "Hilfe"], ["Rechnung", "Export", "Rechnung"]]


def inhalt_stimmt(ergebnis, erwartet):
    """Prüft nur den Inhalt: eine Menge oder Liste mit genau den erwarteten Menüpunkten."""
    return isinstance(ergebnis, (set, list)) and set(ergebnis) == erwartet


def tipp_menge(ergebnis, tipp):
    """Gibt bei einer Liste den Hinweis auf set zurück, sonst den Tipp, der zum Fehlerbild passt."""
    if isinstance(ergebnis, list):
        return "\nTipp: Geben Sie eine Menge (set) zurück, keine Liste."
    return tipp


def tipp_startwert(ergebnis, tipp):
    """Gibt bei leerem Ergebnis von von_allen den Hinweis auf den Startwert zurück, sonst tipp."""
    if ergebnis == set() or ergebnis == []:
        return (
            "\nTipp: Beginnen Sie mit den Punkten der ersten Person, angeklickt(protokolle[0]), nicht mit set(): "
            "Der Schnitt mit der leeren Menge bleibt leer."
        )
    return tipp


# angeklickt aus dem Beispiel (ob Menge oder Liste, zählt hier noch nicht)
protokolle = beispiel()
ergebnis = angeklickt(protokolle[0])
assert inhalt_stimmt(ergebnis, {"Datei", "Rechnung", "Hilfe"}), (
    f"angeklickt({protokolle[0]}) ergibt {ergebnis!r}, erwartet waren die Punkte 'Datei', 'Rechnung' und 'Hilfe', "
    "jeder nur einmal."
)

# angeklickt gibt eine Menge zurück
assert isinstance(ergebnis, set), (
    f"angeklickt({protokolle[0]}) ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war die Menge "
    "{'Datei', 'Rechnung', 'Hilfe'}.\nTipp: Geben Sie eine Menge zurück, keine Liste: set(klicks)."
)

# von_allen aus dem Beispiel (ob Menge oder Liste, zählt hier noch nicht)
ergebnis = von_allen(protokolle)
assert inhalt_stimmt(ergebnis, {"Rechnung"}), (
    f"von_allen({protokolle}) ergibt {ergebnis!r}, erwartet war nur der Punkt 'Rechnung'."
    + tipp_startwert(ergebnis, "\nTipp: Der Schnitt a & b enthält nur, was in beiden Mengen steht.")
)

# von_allen gibt eine Menge zurück
assert isinstance(ergebnis, set), (
    f"von_allen({protokolle}) ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war die Menge {{'Rechnung'}}.\n"
    "Tipp: Geben Sie eine Menge (set) zurück, keine Liste."
)

# von_irgendwem aus dem Beispiel (ob Menge oder Liste, zählt hier noch nicht)
ergebnis = von_irgendwem(protokolle)
assert inhalt_stimmt(ergebnis, {"Datei", "Rechnung", "Hilfe", "Export"}), (
    f"von_irgendwem({protokolle}) ergibt {ergebnis!r}, erwartet waren die Punkte 'Datei', 'Rechnung', 'Hilfe' und "
    "'Export', jeder nur einmal.\nTipp: Die Vereinigung a | b enthält alles, was in mindestens einer der Mengen steht."
)

# von_irgendwem gibt eine Menge zurück
assert isinstance(ergebnis, set), (
    f"von_irgendwem({protokolle}) ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war die Menge "
    "{'Datei', 'Rechnung', 'Hilfe', 'Export'}.\nTipp: Geben Sie eine Menge (set) zurück, keine Liste."
)

# Die Protokolle bleiben unverändert
assert protokolle == beispiel(), (
    f"Nach den Aufrufen ist protokolle {protokolle!r}, erwartet war unverändert {beispiel()!r}.\n"
    "Tipp: set(klicks) legt eine neue Menge an; entfernen Sie nichts aus den Listen selbst."
)

# von_allen bei drei Personen (nicht fest hinschreiben!)
protokolle = [
    ["Start", "Kunden", "Suche", "Kunden"],
    ["Suche", "Start", "Hilfe"],
    ["Kunden", "Start", "Suche", "Start", "Drucken"],
]
ergebnis = von_allen(protokolle)
assert ergebnis == {"Start", "Suche"}, (
    f"Für protokolle = {protokolle} ergibt von_allen {ergebnis!r}, erwartet war {{'Start', 'Suche'}}."
    + tipp_menge(
        ergebnis,
        tipp_startwert(ergebnis, "\nTipp: Gehen Sie mit einer Schleife durch alle Protokolle, nicht nur durch die ersten beiden."),
    )
)

# von_irgendwem bei drei Personen
ergebnis = von_irgendwem(protokolle)
erwartet = {"Start", "Kunden", "Suche", "Hilfe", "Drucken"}
assert ergebnis == erwartet, (
    f"Für protokolle = {protokolle} ergibt von_irgendwem {ergebnis!r}, erwartet war {erwartet!r}."
    + tipp_menge(ergebnis, "\nTipp: Gehen Sie mit einer Schleife durch alle Protokolle, nicht nur durch die ersten beiden.")
)

# Nur die letzte Person hat einen Punkt nicht gefunden
protokolle = [["Export", "Hilfe"], ["Hilfe", "Export"], ["Hilfe"]]
ergebnis = von_allen(protokolle)
assert ergebnis == {"Hilfe"}, (
    f"von_allen({protokolle}) ergibt {ergebnis!r}, erwartet war {{'Hilfe'}}."
    + tipp_menge(ergebnis, tipp_startwert(ergebnis, "\nTipp: Auch das letzte Protokoll muss in den Schnitt eingehen."))
)

# von_allen bei einer einzigen Person
protokolle = [["Hilfe", "Hilfe", "Datei"]]
ergebnis = von_allen(protokolle)
assert ergebnis == {"Hilfe", "Datei"}, (
    f"Bei nur einer Person {protokolle} ergibt von_allen {ergebnis!r}, erwartet war {{'Hilfe', 'Datei'}}."
    + tipp_menge(ergebnis, tipp_startwert(ergebnis, ""))
)

# von_irgendwem bei einer einzigen Person
ergebnis = von_irgendwem(protokolle)
assert ergebnis == {"Hilfe", "Datei"}, (
    f"Bei nur einer Person {protokolle} ergibt von_irgendwem {ergebnis!r}, erwartet war {{'Hilfe', 'Datei'}}."
    + tipp_menge(ergebnis, "")
)

# angeklickt, wenn eine Person nichts angeklickt hat
ergebnis = angeklickt([])
assert ergebnis == set(), (
    f"angeklickt([]) ergibt {ergebnis!r}, erwartet war set()."
    + tipp_menge(ergebnis, "\nTipp: Die leere Menge ist set(); {} wäre ein leeres Dictionary.")
)

# von_irgendwem, wenn eine Person nichts angeklickt hat
protokolle = [["Datei", "Hilfe"], []]
ergebnis = von_irgendwem(protokolle)
assert ergebnis == {"Datei", "Hilfe"}, (
    f"Für protokolle = {protokolle} ergibt von_irgendwem {ergebnis!r}, erwartet war {{'Datei', 'Hilfe'}}."
    + tipp_menge(ergebnis, "")
)

# von_allen, wenn eine Person nichts angeklickt hat
ergebnis = von_allen(protokolle)
assert ergebnis == set(), (
    f"Für protokolle = {protokolle} ergibt von_allen {ergebnis!r}, erwartet war set()."
    + tipp_menge(
        ergebnis,
        "\nTipp: Die leere Menge ist set(); {} wäre ein leeres Dictionary. "
        "Hat eine Person nichts angeklickt, hat niemand alles gefunden.",
    )
)

# Niemand hat etwas angeklickt
protokolle = [[], []]
ergebnis = (von_allen(protokolle), von_irgendwem(protokolle))
assert ergebnis == (set(), set()), (
    f"Für protokolle = {protokolle} ergeben von_allen und von_irgendwem {ergebnis!r}, erwartet war (set(), set())."
    + tipp_menge(ergebnis[0], tipp_menge(ergebnis[1], ""))
)


# Vergleichslösung: mit Listen statt Mengen
def von_allen_von_hand(protokolle):
    """Sammelt die Punkte des ersten Protokolls, die in jedem Protokoll vorkommen, ohne Mengenoperatoren."""
    gemeinsam = []
    for punkt in set(protokolle[0]):
        ueberall = True
        for klicks in protokolle:
            if punkt not in klicks:
                ueberall = False
        if ueberall and punkt not in gemeinsam:
            gemeinsam.append(punkt)
    return sorted(gemeinsam)


def von_irgendwem_von_hand(protokolle):
    """Sammelt alle Punkte aller Protokolle in einer Liste ohne Doppelte."""
    alle = []
    for klicks in protokolle:
        for punkt in klicks:
            if punkt not in alle:
                alle.append(punkt)
    return sorted(alle)


# 300 zufällige Usability-Tests für von_allen
zufall = Zufall(2028)
menue = ["Datei", "Bearbeiten", "Ansicht", "Rechnung", "Kunden", "Export", "Hilfe", "Suche"]
for _ in range(300):
    protokolle = []
    for _ in range(zufall.randint(1, 5)):
        protokolle.append(zufall.choices(menue[: zufall.randint(1, 8)], k=zufall.randint(0, 8)))
    vorher = [list(klicks) for klicks in protokolle]
    erwartet = von_allen_von_hand(protokolle)
    ergebnis = von_allen(protokolle)
    assert isinstance(ergebnis, set) and sorted(ergebnis) == erwartet, (
        f"Für protokolle = {vorher} ergibt von_allen {ergebnis!r}, erwartet war die Menge der Punkte {erwartet}."
        + tipp_menge(ergebnis, "")
    )
    assert protokolle == vorher, f"Nach von_allen ist protokolle {protokolle!r}, erwartet war unverändert {vorher!r}."

# 300 zufällige Usability-Tests für von_irgendwem
zufall = Zufall(2028)
for _ in range(300):
    protokolle = []
    for _ in range(zufall.randint(1, 5)):
        protokolle.append(zufall.choices(menue[: zufall.randint(1, 8)], k=zufall.randint(0, 8)))
    vorher = [list(klicks) for klicks in protokolle]
    erwartet = von_irgendwem_von_hand(protokolle)
    ergebnis = von_irgendwem(protokolle)
    assert isinstance(ergebnis, set) and sorted(ergebnis) == erwartet, (
        f"Für protokolle = {vorher} ergibt von_irgendwem {ergebnis!r}, erwartet war die Menge der Punkte {erwartet}."
        + tipp_menge(ergebnis, "")
    )
    assert protokolle == vorher, f"Nach von_irgendwem ist protokolle {protokolle!r}, erwartet war unverändert {vorher!r}."

# An der oberen Grenze: von_allen bei 100 Personen mit je 1000 Klicks aus 200 Menüpunkten
menue = [f"Punkt {nummer}" for nummer in range(200)]
protokolle = []
for person in range(100):
    # Punkt 0 klickt jede Person, Punkt 199 keine, sonst jede Person 120 aufeinanderfolgende Punkte
    klicks = ["Punkt 0"] + [menue[(person + schritt % 120) % 199] for schritt in range(999)]
    protokolle.append(klicks)
erwartet_allen = set(von_allen_von_hand(protokolle))
erwartet_irgendwem = set(von_irgendwem_von_hand(protokolle))
ergebnis = von_allen(protokolle)
if isinstance(ergebnis, set):
    hinweis = ""
else:
    hinweis = "\nTipp: Geben Sie eine Menge (set) zurück, keine Liste."
assert ergebnis == erwartet_allen, (
    f"Bei 100 Personen mit je 1000 Klicks ergibt von_allen {len(ergebnis)} Menüpunkte, "
    f"erwartet waren {len(erwartet_allen)}.{hinweis}"
)

# An der oberen Grenze: von_irgendwem bei 100 Personen mit je 1000 Klicks
ergebnis = von_irgendwem(protokolle)
if isinstance(ergebnis, set):
    hinweis = ""
else:
    hinweis = "\nTipp: Geben Sie eine Menge (set) zurück, keine Liste."
assert ergebnis == erwartet_irgendwem, (
    f"Bei 100 Personen mit je 1000 Klicks ergibt von_irgendwem {len(ergebnis)} Menüpunkte, "
    f"erwartet waren {len(erwartet_irgendwem)}.{hinweis}"
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['Datei', 'Hilfe', 'Rechnung']\n['Rechnung']\n['Datei', 'Export', 'Hilfe', 'Rechnung']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
