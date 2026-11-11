# Automatisch erzeugt aus lehrkraft/muster/2_023_angebote.py - nicht von Hand ändern.
# vorlage-hash: 048dd8ce37c516a4
# text-hash: 0c9052c17d350f6c
# thema: datenstrukturen
# inhalt: sort gegen sorted

# guenstigste aus dem Beispiel
preise = [129900, 104950, 118000, 99900, 104950]
ergebnis = guenstigste(preise, 3)
assert ergebnis == [99900, 104950, 104950], (
    f"guenstigste({[129900, 104950, 118000, 99900, 104950]}, 3) ergibt {ergebnis!r}, erwartet war [99900, 104950, 104950].\n"
    "Tipp: Sortieren Sie aufsteigend und nehmen Sie dann mit [:anzahl] die ersten anzahl Preise."
)

# guenstigste lässt die übergebene Liste unverändert
assert preise == [129900, 104950, 118000, 99900, 104950], (
    f"Nach guenstigste(preise, 3) ist preise {preise!r}; die Liste soll unverändert bleiben.\n"
    "Tipp: preise.sort() sortiert die Liste des Aufrufers; sorted(preise) baut eine neue."
)

# absteigend_sortieren aus dem Beispiel: sortiert die Liste selbst und gibt None zurück
preise = [129900, 104950, 118000, 99900, 104950]
rueckgabe = absteigend_sortieren(preise)
assert preise == [129900, 118000, 104950, 104950, 99900], (
    f"Nach absteigend_sortieren(preise) ist preise {preise!r}, erwartet war [129900, 118000, 104950, 104950, 99900].\n"
    "Tipp: sorted(preise) ändert die Liste nicht, und preise = … in der Funktion ändert nur eine lokale Variable; "
    "benutzen Sie preise.sort(reverse=True)."
)

# absteigend_sortieren gibt nichts zurück
assert rueckgabe is None, (
    f"absteigend_sortieren soll nichts zurückgeben, gibt aber {rueckgabe!r} zurück.\n"
    "Tipp: Die Funktion verändert die Liste selbst; ein return ist nicht nötig."
)

# Andere Preise und andere Anzahlen (nicht fest hinschreiben!)
for werte, anzahl, erwartet in [
    ([5, 3, 8, 1], 2, [1, 3]),
    ([5, 3, 8, 1], 4, [1, 3, 5, 8]),
    ([5, 3, 8, 1], 0, []),
    ([7], 1, [7]),
    ([], 0, []),
    ([2, 2, 2], 2, [2, 2]),
]:
    kopie = list(werte)
    ergebnis = guenstigste(kopie, anzahl)
    if kopie != werte:
        hinweis = "\nTipp: preise.sort() sortiert die Liste des Aufrufers; sorted(preise) baut eine neue."
    else:
        hinweis = ""
    assert ergebnis == erwartet and kopie == werte, (
        f"guenstigste({werte}, {anzahl}) ergibt {ergebnis!r}, erwartet war {erwartet!r}; "
        f"die Liste ist danach {kopie!r} (soll {werte!r} bleiben).{hinweis}"
    )

# absteigend_sortieren bei Randfällen
for werte, erwartet in [([], []), ([4], [4]), ([1, 2, 3], [3, 2, 1]), ([3, 2, 1], [3, 2, 1]), ([1, 10**7, 1], [10**7, 1, 1])]:
    kopie = list(werte)
    absteigend_sortieren(kopie)
    assert kopie == erwartet, (
        f"Nach absteigend_sortieren ist die Liste {werte} zu {kopie!r} geworden, erwartet war {erwartet!r}.\n"
        "Tipp: reverse=True sortiert absteigend."
    )

# sorted und sort werden benutzt
assert verwendet("sorted") and verwendet("sort"), "Benutzen Sie für diese Aufgabe sorted(…) und ….sort(…)."


# Vergleichslösung: immer das kleinste übrige Element herausnehmen
def guenstigste_von_hand(werte, anzahl):
    """Sucht anzahl-mal das Minimum der restlichen Preise."""
    rest = list(werte)
    ergebnis = []
    for _ in range(anzahl):
        kleinster = min(rest)
        rest.remove(kleinster)
        ergebnis.append(kleinster)
    return ergebnis


# 300 zufällige Angebotslisten
zufall = Zufall(2023)
for _ in range(300):
    werte = [zufall.choice([zufall.randint(1, 50), zufall.randint(1, 10**7)]) for _ in range(zufall.randint(0, 10))]
    anzahl = zufall.randint(0, len(werte))
    kopie = list(werte)
    ergebnis = guenstigste(kopie, anzahl)
    erwartet = guenstigste_von_hand(werte, anzahl)
    assert ergebnis == erwartet and kopie == werte, (
        f"guenstigste({werte}, {anzahl}) ergibt {ergebnis!r}, erwartet war {erwartet!r}; die Liste ist danach {kopie!r}."
    )
    absteigend_sortieren(kopie)
    erwartet = list(reversed(guenstigste_von_hand(werte, len(werte))))
    assert kopie == erwartet, f"Nach absteigend_sortieren ist {werte} zu {kopie!r} geworden, erwartet war {erwartet!r}."

# An der oberen Grenze: 100 000 Preise
werte = [(nummer * 7919) % 10**7 + 1 for nummer in range(100000)]
kopie = list(werte)
ergebnis = guenstigste(kopie, 100000)
erwartet = sorted(werte)
absteigend = list(werte)
absteigend_sortieren(absteigend)
assert ergebnis == erwartet and kopie == werte and absteigend == erwartet[::-1], (
    f"Bei 100 000 Preisen liefert guenstigste {len(ergebnis)} Preise, die ersten {ergebnis[:3]}, und "
    f"absteigend_sortieren beginnt mit {absteigend[:3]}; erwartet waren {erwartet[:3]} und {erwartet[::-1][:3]}, "
    f"und die Liste für guenstigste {'bleibt' if kopie == werte else 'ist verändert, soll aber'} unverändert."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "[99900, 104950, 104950]\n[129900, 104950, 118000, 99900, 104950]\n[129900, 118000, 104950, 104950, 99900]"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
