# Automatisch erzeugt aus lehrkraft/muster/3_036_menuereihenfolge.py - nicht von Hand ändern.
# vorlage-hash: b32cbe0c3fd4a873
# text-hash: 7a07447cbda75f5d
# thema: algorithmen
# inhalt: Permutationen rekursiv

import sys


def rekursive_aufrufe(funktion, *argumente):
    """Gibt die Namen der Funktionen zurück, die sich während des Aufrufs direkt selbst aufrufen."""
    namen = []

    def beobachte(rahmen, ereignis, _wert):
        """Merkt sich einen Aufruf, dessen Aufrufer dieselbe Funktion ist."""
        if ereignis == "call" and rahmen.f_back is not None and rahmen.f_back.f_code is rahmen.f_code:
            namen.append(rahmen.f_code.co_name)

    # Einen schon gesetzten Profiler danach wiederherstellen, auch wenn der Aufruf abbricht
    vorher = sys.getprofile()
    sys.setprofile(beobachte)
    try:
        funktion(*argumente)
    finally:
        sys.setprofile(vorher)
    return namen


def als_listen(ergebnis):
    """Wandelt jede Reihenfolge in eine Liste um; bei unpassendem Ergebnis bleibt es, wie es ist."""
    try:
        return [list(reihenfolge) for reihenfolge in ergebnis]
    except TypeError:
        return ergebnis


def vergleich(eintraege):
    """Langsame Vergleichslösung ohne Rekursion: Reihenfolgen Stelle für Stelle verlängern."""
    teile = [[]]
    for _ in eintraege:
        laenger = []
        for teil in teile:
            for eintrag in eintraege:
                if eintrag not in teil:
                    laenger.append(teil + [eintrag])
        teile = laenger
    return teile


def kurz(liste):
    """Kürzt lange Ergebnislisten für Fehlermeldungen."""
    if not isinstance(liste, list) or len(liste) <= 6:
        return repr(liste)
    return f"[{liste[0]!r}, {liste[1]!r}, … insgesamt {len(liste)} Einträge]"


beispiel = ["Start", "Suche", "Profil"]
erwartet_beispiel = vergleich(beispiel)

# Im Beispiel kommen alle sechs Reihenfolgen vor (Ordnung zählt hier noch nicht)
ergebnis = als_listen(alle_reihenfolgen(["Start", "Suche", "Profil"]))
assert isinstance(ergebnis, list) and sorted(ergebnis) == sorted(erwartet_beispiel), (
    f"alle_reihenfolgen({beispiel}) ergibt {ergebnis!r};\nerwartet waren diese sechs Reihenfolgen "
    f"(in beliebiger Ordnung): {erwartet_beispiel}"
)

# Im Beispiel stehen die Reihenfolgen in der verlangten Ordnung
ergebnis = als_listen(alle_reihenfolgen(["Start", "Suche", "Profil"]))
assert ergebnis == erwartet_beispiel, (
    f"alle_reihenfolgen({beispiel}) ergibt\n{ergebnis}\nerwartet war\n{erwartet_beispiel}\n"
    "Tipp: Gehen Sie die möglichen ersten Einträge von vorn nach hinten durch und hängen Sie für jeden "
    "die Reihenfolgen des Rests in deren Ordnung an."
)

# Zwei Einträge ergeben zwei Reihenfolgen (nicht fest hinschreiben!)
ergebnis = als_listen(alle_reihenfolgen(["Hilfe", "Konto"]))
assert ergebnis == [["Hilfe", "Konto"], ["Konto", "Hilfe"]], (
    f'alle_reihenfolgen(["Hilfe", "Konto"]) ergibt {ergebnis!r}, erwartet war [["Hilfe", "Konto"], ["Konto", "Hilfe"]].'
)

# Ein Eintrag ergibt eine Reihenfolge
ergebnis = als_listen(alle_reihenfolgen(["Start"]))
assert ergebnis == [["Start"]], f'alle_reihenfolgen(["Start"]) ergibt {ergebnis!r}, erwartet war [["Start"]].'

# Keine Einträge: genau eine, die leere Reihenfolge
ergebnis = als_listen(alle_reihenfolgen([]))
assert ergebnis == [[]], (
    f"alle_reihenfolgen([]) ergibt {ergebnis!r}, erwartet war [[]].\n"
    "Tipp: Die leere Liste hat genau eine Reihenfolge, die leere Liste. Geben Sie [[]] zurück, nicht []."
)

# Vier Einträge: 24 Reihenfolgen in der verlangten Ordnung
vier = ["Start", "Suche", "Profil", "Hilfe"]
ergebnis = als_listen(alle_reihenfolgen(vier))
assert ergebnis == vergleich(vier), (
    f"alle_reihenfolgen({vier}) ergibt {kurz(ergebnis)}, erwartet waren die 24 Reihenfolgen "
    f"{kurz(vergleich(vier))}"
)

# Die übergebene Liste bleibt unverändert
eintraege = ["Start", "Suche", "Profil", "Hilfe"]
alle_reihenfolgen(eintraege)
assert eintraege == ["Start", "Suche", "Profil", "Hilfe"], (
    f"Nach alle_reihenfolgen(eintraege) hat sich eintraege verändert: {eintraege!r}.\n"
    "Tipp: Bauen Sie den Rest mit Slicing als neue Liste, statt Einträge zu entfernen."
)

# Ohne itertools.permutations
assert not verwendet("permutations"), "Erzeugen Sie die Reihenfolgen selbst rekursiv, nicht mit itertools.permutations."

# alle_reihenfolgen ist rekursiv gelöst
assert rekursive_aufrufe(alle_reihenfolgen, ["Start", "Suche", "Profil"]) != [], (
    'alle_reihenfolgen(["Start", "Suche", "Profil"]) ruft keine Funktion rekursiv auf, erwartet war eine '
    "rekursive Lösung.\nTipp: Rufen Sie alle_reihenfolgen für den Rest (alle Einträge außer dem ersten "
    "gewählten) selbst auf."
)

# Viele zufällige Menüs mit bis zu 6 Einträgen
zufall = Zufall(3036)
woerter = ["Start", "Suche", "Profil", "Hilfe", "Konto", "Warenkorb", "Nachrichten", "Einstellungen"]
for runde in range(60):
    eintraege = zufall.sample(woerter, runde % 7)
    ergebnis = als_listen(alle_reihenfolgen(eintraege))
    erwartet = vergleich(eintraege)
    assert ergebnis == erwartet, f"alle_reihenfolgen({eintraege}) ergibt {kurz(ergebnis)}, erwartet war {kurz(erwartet)}."

# Obere Grenze: 7 Einträge, 5040 Reihenfolgen
sieben = woerter[:7]
ergebnis = als_listen(alle_reihenfolgen(sieben))
erwartet = vergleich(sieben)
assert ergebnis == erwartet, (
    f"alle_reihenfolgen({sieben}) ergibt {kurz(ergebnis)}, erwartet waren 5040 Reihenfolgen {kurz(erwartet)}."
)
