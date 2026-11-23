# Automatisch erzeugt aus lehrkraft/muster/2_056_plattentausch.py - nicht von Hand ändern.
# vorlage-hash: b46208ec573f8598
# text-hash: eb7a5c9f47d11286
# thema: algorithmen
# inhalt: Suchen, entfernen, zusammenführen

A = [("A7", 1200), ("A2", 30500), ("A9", 41000)]
B = [("B4", 800), ("B1", 35000), ("B3", 52000)]


def wert_von(funktion, *argumente):
    """Ruft funktion mit Kopien der Listen auf; ein Fehler wird als Text zurückgegeben."""
    kopien = [list(argument) if isinstance(argument, list) else argument for argument in argumente]
    try:
        return funktion(*kopien)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_tausch(regal_a, regal_b, defekte, grenze):
    """Vergleichslösung: filtert zuerst und sortiert dann nach (Stunden, Regal, Stelle)."""
    markiert = []
    for regal, platten in [(0, regal_a), (1, regal_b)]:
        for stelle, (nummer, stunden) in enumerate(platten):
            if nummer not in defekte and stunden >= grenze:
                markiert.append((stunden, regal, stelle, nummer))
    return [(nummer, stunden) for stunden, _, _, nummer in sorted(markiert)]


def text_tausch(regal_a, regal_b, defekte, grenze, hinweis=""):
    """Vergleicht tauschliste mit der Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(tauschliste, regal_a, regal_b, defekte, grenze)
    erwartet = vergleich_tausch(regal_a, regal_b, defekte, grenze)
    text = (
        f"tauschliste({regal_a}, {regal_b}, {defekte}, {grenze})\n"
        f"ergibt   {ergebnis!r}\nerwartet {erwartet}{hinweis}"
    )
    return ergebnis == erwartet, text


def regal(zufall, buchstabe, laenge):
    """Erzeugt ein sortiertes Regal mit Seriennummern wie A0, A1, …"""
    stunden = sorted(zufall.randint(0, 100) * 1000 for _ in range(laenge))
    return [(f"{buchstabe}{stelle}", wert) for stelle, wert in enumerate(stunden)]


# ohne_defekte: das Beispiel
ergebnis = wert_von(ohne_defekte, B, ["B1"])
assert ergebnis == [("B4", 800), ("B3", 52000)], (
    f"ohne_defekte(regal_b, ['B1']) ergibt {ergebnis!r}, erwartet war [('B4', 800), ('B3', 52000)].\n"
    "Tipp: Hängen Sie jedes Paar an eine neue Liste an, dessen Seriennummer nicht in defekte steht."
)

# ohne_defekte: mehrere Defekte, auch unbekannte
ergebnis = wert_von(ohne_defekte, A, ["A9", "X1", "A7"])
assert ergebnis == [("A2", 30500)], (
    f"ohne_defekte(regal_a, ['A9', 'X1', 'A7']) ergibt {ergebnis!r}, erwartet war [('A2', 30500)]."
)

# ohne_defekte: keine Defekte ergibt eine Kopie, nicht dieselbe Liste
platten = list(A)
try:
    ergebnis = ohne_defekte(platten, [])
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == A and ergebnis is not platten, (
    f"ohne_defekte(regal_a, []) ergibt {ergebnis!r}; erwartet war eine neue Liste mit denselben Paaren."
)

# ohne_defekte verändert die übergebene Liste nicht
platten = list(B)
try:
    ohne_defekte(platten, ["B1"])
except Exception:
    pass
assert platten == B, (
    f"Nach ohne_defekte(regal_b, ['B1']) ist regal_b {platten}; es sollte unverändert bleiben.\n"
    "Tipp: Bauen Sie eine neue Liste auf, statt mit remove aus der alten zu löschen."
)

# zusammenfuehren: das Beispiel ohne Defekte
ergebnis = wert_von(zusammenfuehren, A, B)
erwartet = [("B4", 800), ("A7", 1200), ("A2", 30500), ("B1", 35000), ("A9", 41000), ("B3", 52000)]
assert ergebnis == erwartet, (
    f"zusammenfuehren(regal_a, regal_b) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: Vergleichen Sie die Stunden regal_a[i][1] und regal_b[j][1] und hängen Sie am Ende den Rest an."
)

# zusammenfuehren: gleiche Stunden, Regal A zuerst
ergebnis = wert_von(zusammenfuehren, [("A1", 500), ("A2", 500)], [("B1", 500)])
assert ergebnis == [("A1", 500), ("A2", 500), ("B1", 500)], (
    f"zusammenfuehren([('A1', 500), ('A2', 500)], [('B1', 500)]) ergibt {ergebnis!r}, "
    "erwartet war [('A1', 500), ('A2', 500), ('B1', 500)].\nTipp: Bei Gleichstand gewinnt regal_a, also <= statt <."
)

# zusammenfuehren: eine Liste leer
ergebnis = wert_von(zusammenfuehren, [], B)
assert ergebnis == B, f"zusammenfuehren([], regal_b) ergibt {ergebnis!r}, erwartet war {B}."

# erste_ab: das Beispiel
ergebnis = wert_von(erste_ab, A, 30000)
assert ergebnis == 1, f"erste_ab(regal_a, 30000) ergibt {ergebnis!r}, erwartet war 1."

# erste_ab: genau auf der Grenze zählt mit
ergebnis = wert_von(erste_ab, A, 41000)
assert ergebnis == 2, (
    f"erste_ab(regal_a, 41000) ergibt {ergebnis!r}, erwartet war 2.\n"
    "Tipp: „mindestens grenze Stunden“ heißt >=, nicht >."
)

# erste_ab: keine Platte über der Grenze ergibt -1
ergebnis = wert_von(erste_ab, A, 41001)
assert ergebnis == -1, (
    f"erste_ab(regal_a, 41001) ergibt {ergebnis!r}, erwartet war -1.\n"
    "Tipp: Das return -1 gehört hinter die Schleife."
)

# erste_ab: leere Liste ergibt -1
ergebnis = wert_von(erste_ab, [], 0)
assert ergebnis == -1, f"erste_ab([], 0) ergibt {ergebnis!r}, erwartet war -1."

# tauschliste: das Beispiel
stimmt, text = text_tausch(A, B, ["B1"], 30000)
assert stimmt, text

# tauschliste: andere Grenze und andere Defekte (nicht fest hinschreiben!)
stimmt, text = text_tausch(A, B, ["A9"], 1000)
assert stimmt, text

# tauschliste: Defekte werden vor dem Suchen entfernt
stimmt, text = text_tausch(
    A, B, ["A2", "B1", "A9"], 30000, "\nTipp: Entfernen Sie die defekten Platten in beiden Regalen."
)
assert stimmt, text

# tauschliste: Grenze 0 nimmt alle nicht defekten Platten
stimmt, text = text_tausch(A, B, [], 0)
assert stimmt, text

# tauschliste: keine Platte über der Grenze ergibt eine leere Liste
stimmt, text = text_tausch(
    A, B, [], 60000, "\nTipp: Liefert erste_ab -1, gibt es nichts zu tauschen; liste[-1:] wäre das letzte Paar."
)
assert stimmt, text

# tauschliste: beide Regale leer
stimmt, text = text_tausch([], [], ["A1"], 0)
assert stimmt, text

# tauschliste verändert die Regale nicht
a = list(A)
b = list(B)
try:
    tauschliste(a, b, ["B1"], 30000)
except Exception:
    pass
assert a == A and b == B, f"Nach tauschliste ist regal_a {a} und regal_b {b}; beide sollten unverändert bleiben."

# Ohne sort() und sorted()
verboten = [name for name in ["sort", "sorted"] if verwendet(name)]
assert verboten == [], f"Ihr Code verwendet {verboten}. Führen Sie die Regale wie in Aufgabe 2_055 zusammen."

# Die Ausgabe des Programms
erwartet = str(vergleich_tausch(A, B, ["B1"], 30000))
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Regale
zufall = Zufall(2056)
for _ in range(300):
    a = regal(zufall, "A", zufall.randint(0, 8))
    b = regal(zufall, "B", zufall.randint(0, 8))
    alle = [nummer for nummer, _ in a + b]
    defekte = zufall.sample(alle, min(len(alle), zufall.randint(0, 3))) + ["X9"]
    stimmt, text = text_tausch(a, b, defekte, zufall.randint(0, 100) * 1000)
    assert stimmt, text

# Laufzeit: jede Liste nur wenige Male durchgehen
a = regal(zufall, "A", 2000)
b = regal(zufall, "B", 2000)
defekte = [a[5][0], b[7][0], "X1", "X2", "X3"]
try:
    _, schritte = zaehle_schritte(tauschliste, a, b, defekte, 50000)
except Exception as fehler:
    schritte = f"(Abbruch: {type(fehler).__name__}: {fehler})"
assert isinstance(schritte, int) and schritte <= 30 * 4000, (
    f"Für zweimal 2000 Platten braucht Ihre Lösung {schritte} Schritte, erlaubt sind 30 · 4000 = 120000.\n"
    "Tipp: Sortieren Sie keine Platte einzeln ein, sondern vergleichen Sie nur die beiden vordersten Paare."
)

# Obere Grenze: zweimal 20 000 Platten
a = regal(zufall, "A", 20000)
b = regal(zufall, "B", 20000)
defekte = [a[0][0], b[-1][0], "X1"]
assert wert_von(tauschliste, a, b, defekte, 50000) == vergleich_tausch(a, b, defekte, 50000), (
    "Bei zweimal 20 000 Platten stimmt das Ergebnis von tauschliste nicht."
)
