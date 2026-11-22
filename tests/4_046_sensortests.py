# Automatisch erzeugt aus lehrkraft/muster/4_046_sensortests.py - nicht von Hand ändern.
# vorlage-hash: 4e641ae5b0ffdc78
# text-hash: b18f8aad09bbede7
# thema: kontrollfluss
# inhalt: product, permutations, combinations

def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def abstand_test(von, nach):
    """Weg entlang der Gänge zwischen zwei Punkten."""
    return abs(von[0] - nach[0]) + abs(von[1] - nach[1])


def laenge_von(lager, gateways, reihenfolge):
    """Länge des Rundgangs in der angegebenen Reihenfolge."""
    punkte = [lager] + [gateways[name] for name in reihenfolge] + [lager]
    return sum(abstand_test(a, b) for a, b in zip(punkte, punkte[1:]))


def vergleich_route(lager, gateways):
    """Vergleichslösung: probiert rekursiv alle Reihenfolgen durch und nimmt die kleinste nach (Länge, Namen)."""
    beste = []

    def weiter(bisher, rest):
        """Hängt jeden übrigen Namen an und geht tiefer; ist nichts übrig, wird verglichen."""
        if not rest:
            kandidat = (laenge_von(lager, gateways, bisher), tuple(bisher))
            if not beste or kandidat < beste[0]:
                beste[:] = [kandidat]
            return
        for name in rest:
            weiter(bisher + [name], [anderer for anderer in rest if anderer != name])

    weiter([], list(gateways))
    return beste[0]


def vergleich_paare(messwerte, toleranz):
    """Vergleichslösung mit zwei verschachtelten Schleifen."""
    namen = sorted(messwerte)
    paare = []
    for i in range(len(namen)):
        for j in range(i + 1, len(namen)):
            if abs(messwerte[namen[i]] - messwerte[namen[j]]) > toleranz:
                paare.append((namen[i], namen[j]))
    return paare


GATEWAYS = {"nord": (0, 10), "ost": (8, 0), "mitte": (4, 4)}

# testmatrix im Beispiel
ergebnis = wert_von(lambda: testmatrix(["v1", "v2"], ["LoRa"], [60, 300]))
erwartet = [("v1", "LoRa", 60), ("v1", "LoRa", 300), ("v2", "LoRa", 60), ("v2", "LoRa", 300)]
assert ergebnis == erwartet, (
    f'testmatrix(["v1", "v2"], ["LoRa"], [60, 300]) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: list(product(firmwares, funkmodule, intervalle))."
)

# testmatrix mit anderen Werten (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: testmatrix(["v3"], ["LoRa", "Zigbee"], [10, 20, 30]))
erwartet = [("v3", modul, takt) for modul in ["LoRa", "Zigbee"] for takt in [10, 20, 30]]
assert ergebnis == erwartet, f'testmatrix(["v3"], ["LoRa", "Zigbee"], [10, 20, 30]) ergibt {ergebnis!r}, erwartet war {erwartet!r}.'

# testmatrix: ist eine Liste leer, gibt es keinen Testfall
ergebnis = wert_von(lambda: [testmatrix([], ["LoRa"], [60]), testmatrix(["v1"], [], [60]), testmatrix(["v1"], ["LoRa"], [])])
assert ergebnis == [[], [], []], f"testmatrix mit je einer leeren Liste ergibt {ergebnis!r}, erwartet war [[], [], []]."

# testmatrix benutzt product
assert verwendet("product"), "Benutzen Sie in testmatrix itertools.product."

# vergleichspaare im Beispiel
ergebnis = wert_von(lambda: vergleichspaare({"s2": 21.9, "s1": 21.5, "s3": 24.0}, 1.0))
assert ergebnis == [("s1", "s3"), ("s2", "s3")], (
    f'vergleichspaare({{"s2": 21.9, "s1": 21.5, "s3": 24.0}}, 1.0) ergibt {ergebnis!r}, erwartet war [("s1", "s3"), ("s2", "s3")].\n'
    "Tipp: combinations(sorted(messwerte), 2) liefert jedes Paar einmal, mit dem alphabetisch kleineren Namen vorn."
)

# vergleichspaare: genau toleranz Unterschied ist noch in Ordnung
ergebnis = wert_von(lambda: vergleichspaare({"a": 20, "b": 21, "c": 22}, 1))
assert ergebnis == [("a", "c")], f'vergleichspaare({{"a": 20, "b": 21, "c": 22}}, 1) ergibt {ergebnis!r}, erwartet war [("a", "c")] (mehr als toleranz).'

# vergleichspaare: der größere Wert kann auch beim zweiten Namen stehen
ergebnis = wert_von(lambda: vergleichspaare({"z": -10, "y": 30, "x": 5}, 10))
assert ergebnis == [("x", "y"), ("x", "z"), ("y", "z")], (
    f'vergleichspaare({{"z": -10, "y": 30, "x": 5}}, 10) ergibt {ergebnis!r}, erwartet war [("x", "y"), ("x", "z"), ("y", "z")].\n'
    "Tipp: abs(...) misst den Unterschied in beide Richtungen."
)

# vergleichspaare mit null oder einem Sensor und mit toleranz 0
ergebnis = wert_von(lambda: [vergleichspaare({}, 1), vergleichspaare({"s": 20}, 0), vergleichspaare({"a": 1, "b": 1, "c": 2}, 0)])
assert ergebnis == [[], [], [("a", "c"), ("b", "c")]], (
    f"vergleichspaare ohne Sensor, mit einem Sensor und mit toleranz 0 ergibt {ergebnis!r}, "
    'erwartet war [[], [], [("a", "c"), ("b", "c")]].'
)

# vergleichspaare benutzt combinations
assert verwendet("combinations"), "Benutzen Sie in vergleichspaare itertools.combinations."

# kuerzeste_route im Beispiel
ergebnis = wert_von(lambda: kuerzeste_route((0, 0), GATEWAYS))
assert ergebnis == (36, ("nord", "mitte", "ost")), (
    f"kuerzeste_route((0, 0), gateways) ergibt {ergebnis!r}, erwartet war (36, ('nord', 'mitte', 'ost')).\n"
    "Tipp: Probieren Sie mit permutations alle Reihenfolgen durch und vergessen Sie den Rückweg zum Lager nicht."
)

# kuerzeste_route: der Rückweg zum Lager zählt mit
ergebnis = wert_von(lambda: kuerzeste_route((0, 0), {"a": (5, 0)}))
assert ergebnis == (10, ("a",)), f'kuerzeste_route((0, 0), {{"a": (5, 0)}}) ergibt {ergebnis!r}, erwartet war (10, ("a",)) – hin und zurück.'

# kuerzeste_route mit anderen Punkten (nicht fest hinschreiben!)
gateways = {"c": (10, 0), "a": (0, 10), "b": (10, 10)}
ergebnis = wert_von(lambda: kuerzeste_route((0, 0), gateways))
assert ergebnis == (40, ("a", "b", "c")), f"kuerzeste_route((0, 0), {gateways}) ergibt {ergebnis!r}, erwartet war (40, ('a', 'b', 'c'))."

# kuerzeste_route bei Gleichstand: die alphabetisch kleinste Reihenfolge
gateways = {"west": (0, 5), "ost": (10, 5)}
ergebnis = wert_von(lambda: kuerzeste_route((5, 0), gateways))
assert ergebnis == (30, ("ost", "west")), (
    f"kuerzeste_route((5, 0), {gateways}) ergibt {ergebnis!r}, erwartet war (30, ('ost', 'west')) – beide Richtungen sind gleich lang.\n"
    "Tipp: Durchlaufen Sie permutations(sorted(gateways)) und ersetzen Sie das bisher Beste nur bei echt kürzerer Länge."
)

# kuerzeste_route ohne Gateways und mit zwei Gateways am selben Punkt
ergebnis = wert_von(lambda: [kuerzeste_route((3, 3), {}), kuerzeste_route((0, 0), {"b": (2, 2), "a": (2, 2)})])
assert ergebnis == [(0, ()), (8, ("a", "b"))], (
    f"kuerzeste_route ohne Gateways und mit zwei Gateways am selben Punkt ergibt {ergebnis!r}, erwartet war [(0, ()), (8, ('a', 'b'))]."
)

# kuerzeste_route benutzt permutations
assert verwendet("permutations"), "Benutzen Sie in kuerzeste_route itertools.permutations."

# Die Ausgabe des Programms
erwartet = (
    "[('v1', 'LoRa', 60), ('v1', 'LoRa', 300), ('v2', 'LoRa', 60), ('v2', 'LoRa', 300)]\n"
    "[('s1', 's3'), ('s2', 's3')]\n(36, ('nord', 'mitte', 'ost'))"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Messwerte und Hallen
zufall = Zufall(4046)
for _ in range(150):
    namen = zufall.sample(["s1", "s2", "s3", "s4", "s5", "s6", "s7"], zufall.randint(0, 7))
    messwerte = {name: zufall.randint(-400, 850) / 10 for name in namen}
    toleranz = zufall.choice([0, 0.5, 1, 5, 100])
    ergebnis = wert_von(lambda: vergleichspaare(messwerte, toleranz))
    erwartet = vergleich_paare(messwerte, toleranz)
    assert ergebnis == erwartet, f"vergleichspaare({messwerte}, {toleranz}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    lager = (zufall.randint(0, 20), zufall.randint(0, 20))
    gateways = {name: (zufall.randint(0, 20), zufall.randint(0, 20)) for name in zufall.sample("abcdef", zufall.randint(0, 5))}
    ergebnis = wert_von(lambda: kuerzeste_route(lager, gateways))
    erwartet = vergleich_route(lager, gateways)
    assert ergebnis == erwartet, f"kuerzeste_route({lager}, {gateways}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    listen = [zufall.sample(range(100), zufall.randint(0, 3)) for _ in range(3)]
    ergebnis = wert_von(lambda: testmatrix(*listen))
    erwartet = [(a, b, c) for a in listen[0] for b in listen[1] for c in listen[2]]
    assert ergebnis == erwartet, f"testmatrix(*{listen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Obere Grenze: 20 · 20 · 20 Testfälle und 300 Sensoren
listen = [[f"f{nummer}" for nummer in range(20)], [f"m{nummer}" for nummer in range(20)], list(range(20))]
messwerte = {f"s{nummer:03d}": zufall.randint(-400, 850) / 10 for nummer in range(300)}
ergebnis = wert_von(lambda: [len(testmatrix(*listen)), vergleichspaare(messwerte, 50)])
assert ergebnis == [8000, vergleich_paare(messwerte, 50)], (
    "Bei 20 · 20 · 20 Testfällen oder 300 Sensoren stimmen die Ergebnisse von testmatrix oder vergleichspaare nicht."
)

# Obere Grenze: 8 Gateways
lager = (500, 0)
gateways = {name: (zufall.randint(0, 1000), zufall.randint(0, 1000)) for name in "abcdefgh"}
ergebnis = wert_von(lambda: kuerzeste_route(lager, gateways))
erwartet_laenge = min(laenge_von(lager, gateways, reihenfolge) for reihenfolge in permutations("abcdefgh"))
gueltig = isinstance(ergebnis, tuple) and len(ergebnis) == 2 and sorted(ergebnis[1]) == list("abcdefgh")
assert gueltig and ergebnis[0] == erwartet_laenge == laenge_von(lager, gateways, ergebnis[1]), (
    f"Bei 8 Gateways ergibt kuerzeste_route {ergebnis!r}, erwartet war ein Rundgang der Länge {erwartet_laenge}."
)
