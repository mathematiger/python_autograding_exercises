# Automatisch erzeugt aus lehrkraft/muster/3_005_merge_sort.py - nicht von Hand ändern.
# vorlage-hash: a2d7c487167026c0
# thema: algorithmen
# inhalt: Merge Sort rekursiv

# Das Beispiel aus der Aufgabe: zwei sortierte Listen zusammenführen
ergebnis = zusammenfuehren([3, 8, 9], [1, 8, 12])
assert ergebnis == [1, 3, 8, 8, 9, 12], (
    f"zusammenfuehren([3, 8, 9], [1, 8, 12]) ergibt {ergebnis!r}, erwartet war [1, 3, 8, 8, 9, 12].\n"
    "Tipp: Vergleichen Sie links[i] mit rechts[j] und hängen Sie den kleineren Wert an das Ergebnis."
)

# Weitere Paare (nicht fest hinschreiben!)
for links, rechts, erwartet in [
    ([1, 2, 3], [4, 5, 6], [1, 2, 3, 4, 5, 6]),
    ([4, 5, 6], [1, 2, 3], [1, 2, 3, 4, 5, 6]),
    ([1, 5, 9], [2, 3, 4, 10, 11], [1, 2, 3, 4, 5, 9, 10, 11]),
    ([7], [7], [7, 7]),
]:
    ergebnis = zusammenfuehren(links, rechts)
    assert ergebnis == erwartet, (
        f"zusammenfuehren({links}, {rechts}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Ist eine Liste aufgebraucht, hängen Sie den Rest der anderen an, z. B. mit rechts[j:]."
    )

# Eine leere Liste beim Zusammenführen
for links, rechts in [([], [4, 5]), ([4, 5], []), ([], [])]:
    ergebnis = zusammenfuehren(links, rechts)
    erwartet = links + rechts
    assert ergebnis == erwartet, f"zusammenfuehren({links}, {rechts}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Das Beispiel aus der Aufgabe wird sortiert
ergebnis = merge_sort([17, 3, 12, 3, 8])
assert ergebnis == [3, 3, 8, 12, 17], (
    f"merge_sort([17, 3, 12, 3, 8]) ergibt {ergebnis!r}, erwartet war [3, 3, 8, 12, 17].\n"
    "Tipp: Teilen Sie die Liste in der Mitte, sortieren Sie beide Hälften mit merge_sort "
    "und geben Sie zusammenfuehren(links, rechts) zurück."
)

# Weitere Listen (nicht fest hinschreiben!)
for werte, erwartet in [
    ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([2, 1], [1, 2]),
    ([1640995300, 1640995210, 1640995255], [1640995210, 1640995255, 1640995300]),
    ([9, 9, 1, 9], [1, 9, 9, 9]),
]:
    ergebnis = merge_sort(list(werte))
    assert ergebnis == erwartet, f"merge_sort({werte}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Leere Liste und Liste mit einem Element
for werte in [[], [42]]:
    ergebnis = merge_sort(list(werte))
    assert ergebnis == werte, (
        f"merge_sort({werte}) ergibt {ergebnis!r}, erwartet war {werte}.\n"
        "Tipp: Eine Liste mit höchstens einem Element ist schon sortiert; das ist die Abbruchbedingung."
    )

# Eine längere Liste wird richtig sortiert
ergebnis = merge_sort([(37 * zahl) % 1009 for zahl in range(1009)])
assert ergebnis == list(range(1009)), "Eine gemischte Liste der Zahlen 0 bis 1008 ist nach merge_sort nicht sortiert."

# merge_sort lässt die übergebene Liste unverändert
werte = [17, 3, 12, 8]
ergebnis = merge_sort(werte)
assert werte == [17, 3, 12, 8] and ergebnis == [3, 8, 12, 17], (
    f"Nach ergebnis = merge_sort(werte) mit werte = [17, 3, 12, 8] ist werte {werte} und ergebnis {ergebnis!r}; "
    "erwartet war werte unverändert und ergebnis [3, 8, 12, 17].\n"
    "Tipp: Arbeiten Sie mit den Hälften werte[:mitte] und werte[mitte:]; das sind neue Listen."
)

# sorted(...) wird nicht benutzt
assert not verwendet("sorted"), "Benutzen Sie nicht sorted(...), sondern führen Sie die Listen selbst zusammen."


# Diese Funktion ersetzt merge_sort bzw. zusammenfuehren zeitweise und zählt die Aufrufe
def zaehle_aufrufe(name, werte):
    """Ruft merge_sort(werte) auf und zählt dabei die Aufrufe der Funktion name."""
    original = globals()[name]
    aufrufe = []

    def spion(*argumente):
        """Merkt sich den Aufruf und ruft dann die echte Funktion auf."""
        aufrufe.append(argumente)
        return original(*argumente)

    globals()[name] = spion
    try:
        globals()["merge_sort"](werte)
    finally:
        globals()[name] = original
    return len(aufrufe)


# merge_sort ruft sich selbst auf
anzahl = zaehle_aufrufe("merge_sort", [4, 3, 2, 1])
assert anzahl >= 3, (
    f"merge_sort([4, 3, 2, 1]) hat sich {anzahl - 1}-mal selbst aufgerufen; Merge Sort sortiert beide Hälften "
    "rekursiv mit merge_sort."
)

# merge_sort benutzt zusammenfuehren
anzahl = zaehle_aufrufe("zusammenfuehren", [4, 3, 2, 1])
assert anzahl >= 3, (
    f"merge_sort([4, 3, 2, 1]) hat zusammenfuehren {anzahl}-mal aufgerufen, erwartet war dreimal "
    "(zweimal für die Hälften, einmal für die ganze Liste).\n"
    "Tipp: Geben Sie am Ende zusammenfuehren(links, rechts) mit den beiden sortierten Hälften zurück."
)

# Die Ausgabe des Programms stimmt
assert AUSGABE == "[1, 3, 8, 8, 9, 12]\n[3, 3, 8, 12, 17]", (
    f"Erwartete Ausgabe:\n[1, 3, 8, 8, 9, 12]\n[3, 3, 8, 12, 17]\nIhr Programm:\n{AUSGABE}"
)
