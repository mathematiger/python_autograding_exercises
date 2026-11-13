# Automatisch erzeugt aus lehrkraft/muster/3_033_prueflaeufe.py - nicht von Hand ändern.
# vorlage-hash: 48c25f79c4daf466
# text-hash: a8000ef8ced63a7a
# thema: algorithmen
# inhalt: Memoisierung mit Dictionary

def von_unten(n):
    """Vergleichslösung mit einer Schleife von unten statt Rekursion."""
    vorletzter, letzter = 1, 1
    for _ in range(n - 1):
        vorletzter, letzter = letzter, vorletzter + letzter
    return letzter


# Das Beispiel aus der Aufgabe: 4 Stationen, 5 Abläufe
ergebnis = ablaeufe(4, {})
assert ergebnis == 5, f"ablaeufe(4, {{}}) ergibt {ergebnis!r}, erwartet war 5."

# Andere Werte (nicht fest hinschreiben!)
for n in [2, 3, 7, 12]:
    ergebnis = ablaeufe(n, {})
    assert ergebnis == von_unten(n), f"ablaeufe({n}, {{}}) ergibt {ergebnis!r}, erwartet war {von_unten(n)}."

# Randfälle: 0 und 1 Station haben je einen Ablauf
for n in [0, 1]:
    ergebnis = ablaeufe(n, {})
    assert ergebnis == 1, (
        f"ablaeufe({n}, {{}}) ergibt {ergebnis!r}, erwartet war 1.\nTipp: Die Abbruchbedingung ist n <= 1, nicht nur n == 1."
    )

# Das Ergebnis wird im merker notiert
merker = {}
ergebnis = ablaeufe(10, merker)
assert ergebnis == 89 and merker.get(10) == 89, (
    f"Nach merker = {{}} und ablaeufe(10, merker) ist das Ergebnis {ergebnis!r} und merker {merker!r}; "
    "erwartet waren 89 und merker[10] == 89.\nTipp: Tragen Sie jedes berechnete Ergebnis mit merker[n] = … ein."
)

# Auch die Zwischenergebnisse stehen im merker
merker = {}
ablaeufe(10, merker)
fehlend = [n for n in range(2, 11) if merker.get(n) != von_unten(n)]
assert not fehlend, (
    f"Nach ablaeufe(10, merker) fehlen im merker die richtigen Werte für n = {fehlend}; merker: {merker!r}.\n"
    "Tipp: Geben Sie merker bei jedem rekursiven Aufruf mit, damit auch die Zwischenergebnisse dort landen."
)

# Bekannte Werte werden nachgeschlagen statt neu berechnet
ergebnis = ablaeufe(6, {5: 100, 4: 1})
assert ergebnis == 101, (
    f"ablaeufe(6, {{5: 100, 4: 1}}) ergibt {ergebnis!r}, erwartet war 101 (merker[5] + merker[4]).\n"
    "Tipp: Schauen Sie am Anfang mit if n in merker nach und geben Sie dann merker[n] zurück."
)

# Ist n selbst schon bekannt, wird gar nicht gerechnet
ergebnis = ablaeufe(30, {30: 7})
assert ergebnis == 7, f"ablaeufe(30, {{30: 7}}) ergibt {ergebnis!r}, erwartet war 7 (der notierte Wert)."

# Jeder Wert wird nur einmal berechnet (Schritte zählen statt Zeit messen)
_, schritte_20 = zaehle_schritte(ablaeufe, 20, {})
_, schritte_80 = zaehle_schritte(ablaeufe, 80, {})
assert schritte_20 <= 400 and schritte_80 <= 1600, (
    f"ablaeufe(20, {{}}) braucht {schritte_20} Schritte und ablaeufe(80, {{}}) {schritte_80}; erwartet waren "
    "höchstens 400 und 1600 (O(n), jedes Ergebnis wird einmal berechnet).\n"
    "Tipp: Schauen Sie vor jeder Rechnung im merker nach und tragen Sie jedes Ergebnis dort ein."
)

# Ohne fertigen Cache
assert not hasattr(ablaeufe, "cache_info"), (
    "Merken Sie sich die Ergebnisse selbst im Dictionary merker, ohne functools.lru_cache oder functools.cache."
)

# Viele zufällige n, jedes Mal mit frischem merker
zufall = Zufall(3033)
for n in sorted(zufall.sample(range(401), 60)):
    ergebnis = ablaeufe(n, {})
    assert ergebnis == von_unten(n), f"ablaeufe({n}, {{}}) ergibt {ergebnis!r}, erwartet war {von_unten(n)}."

# Ein gemeinsamer merker über viele Aufrufe in zufälliger Reihenfolge
merker = {}
for n in zufall.sample(range(401), 100):
    ergebnis = ablaeufe(n, merker)
    assert ergebnis == von_unten(n), (
        f"Mit einem merker, der schon frühere Ergebnisse enthält, ergibt ablaeufe({n}, merker) {ergebnis!r}, "
        f"erwartet war {von_unten(n)}."
    )

# Obere Grenze: 400 Stationen
ergebnis = ablaeufe(400, {})
assert ergebnis == von_unten(400), f"ablaeufe(400, {{}}) ergibt {ergebnis!r}, erwartet war {von_unten(400)}."
