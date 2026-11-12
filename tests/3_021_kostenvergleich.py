# Automatisch erzeugt aus lehrkraft/muster/3_021_kostenvergleich.py - nicht von Hand ändern.
# vorlage-hash: 15cd348f44b5c4f1
# text-hash: 26cd75c2a052440d
# thema: kontrollfluss
# inhalt: Verbrauchte Iteratoren

class Einmalig:
    """Durchlaufbar wie ein Strom: Der erste Durchlauf liefert die Werte, jeder weitere nichts; kein len()."""

    def __init__(self, werte):
        """Merkt sich die Werte und zählt die Durchläufe."""
        self._werte = list(werte)
        self.durchlaeufe = 0

    def __iter__(self):
        """Liefert beim ersten Mal einen Iterator über die Werte, danach einen leeren."""
        self.durchlaeufe = self.durchlaeufe + 1
        if self.durchlaeufe == 1:
            return iter(self._werte)
        return iter([])


# kostenbericht mit einer Liste
ergebnis = kostenbericht([1200, 300, 300, 300])
assert ergebnis == (2100, 1200, 4), f"kostenbericht([1200, 300, 300, 300]) ergibt {ergebnis!r}, erwartet war (2100, 1200, 4)."

# kostenbericht mit einem Iterator aus map
try:
    ergebnis = kostenbericht(map(int, "500;500;500".split(";")))
except (ValueError, TypeError) as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == (1500, 500, 3), (
    f'kostenbericht(map(int, "500;500;500".split(";"))) ergibt {ergebnis!r}, erwartet war (1500, 500, 3).\n'
    "Tipp: Nach sum(jahreskosten) ist ein Iterator verbraucht, max findet dann nichts mehr, und len() geht "
    "gar nicht. Sammeln Sie die Werte zuerst mit list(jahreskosten)."
)

# kostenbericht mit reversed, einem Tupel, einem range und einem einzigen Jahr
for werte, beschreibung, erwartet in [
    (reversed([0, 10**7, 7]), "reversed([0, 10**7, 7])", (10**7 + 7, 10**7, 3)),
    ((4, 9, 2), "(4, 9, 2)", (15, 9, 3)),
    (range(1, 31), "range(1, 31)", (465, 30, 30)),
    (iter([0]), "iter([0])", (0, 0, 1)),
]:
    try:
        ergebnis = kostenbericht(werte)
    except (ValueError, TypeError) as fehler:
        ergebnis = f"{type(fehler).__name__}: {fehler}"
    assert ergebnis == erwartet, f"kostenbericht({beschreibung}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# kostenbericht durchläuft seine Werte nur einmal
werte = Einmalig([800, 200, 450])
try:
    ergebnis = kostenbericht(werte)
except (ValueError, TypeError) as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == (1450, 800, 3), (
    f"kostenbericht mit Werten 800, 200, 450, die man nur einmal durchlaufen kann, ergibt {ergebnis!r}, "
    f"erwartet war (1450, 800, 3); durchlaufen wurde {werte.durchlaeufe}-mal.\n"
    "Tipp: Speichern Sie die Werte mit list(...) und rechnen Sie danach nur noch mit dieser Liste."
)

# differenzen aus dem Beispiel, als Liste
ergebnis = differenzen([1200, 300, 300, 300], [500, 500, 500, 500])
assert type(ergebnis) is list and ergebnis == [-700, 200, 200, 200], (
    f"differenzen([1200, 300, 300, 300], [500, 500, 500, 500]) ergibt {ergebnis!r}, erwartet war die Liste "
    "[-700, 200, 200, 200].\nTipp: zip und map liefern Iteratoren; geben Sie eine Liste zurück, etwa mit list(...)."
)

# differenzen mit Iteratoren und ohne Jahre
for a, b, beschreibung, erwartet in [
    (iter([1, 2]), reversed([10, 20]), "iter([1, 2]), reversed([10, 20])", [19, 8]),
    (map(int, ["5"]), (5,), 'map(int, ["5"]), (5,)', [0]),
    ([], [], "[], []", []),
    (Einmalig([3, 4]), Einmalig([1, 9]), "zwei nur einmal durchlaufbaren Werten [3, 4] und [1, 9]", [-2, 5]),
]:
    ergebnis = differenzen(a, b)
    assert ergebnis == erwartet, f"differenzen({beschreibung}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# vergleich aus dem Beispiel, mit Listen und mit Iteratoren
for a, b, beschreibung in [
    ([1200, 300, 300, 300], [500, 500, 500, 500], "kauf, leasing"),
    (iter([1200, 300, 300, 300]), reversed([500, 500, 500, 500]), "iter(kauf), reversed(leasing)"),
]:
    ergebnis = vergleich(a, b)
    assert ergebnis == (-100, 1), (
        f"vergleich({beschreibung}) ergibt {ergebnis!r}, erwartet war (-100, 1).\n"
        "Tipp: Die Differenzen werden zweimal gebraucht (Summe und Anzahl); als Liste geht das, als Iterator nicht."
    )

# vergleich: gleiche Kosten sind nicht günstiger, ohne Jahre gibt es nichts
for a, b, erwartet in [([5, 5], [5, 4], (-1, 1)), ([0], [0], (0, 0)), ([], [], (0, 0)), ([1, 2, 3], [4, 5, 6], (9, 0))]:
    ergebnis = vergleich(a, b)
    assert ergebnis == erwartet, (
        f"vergleich({a}, {b}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: B ist nur günstiger, wenn b - a kleiner als 0 ist."
    )

# vergleich benutzt differenzen
_echte_differenzen = differenzen
aufrufe = []


def differenzen(angebot_a, angebot_b):
    """Zählt die Aufrufe und rechnet wie die echte Funktion."""
    aufrufe.append(1)
    return _echte_differenzen(angebot_a, angebot_b)


ergebnis = vergleich([2, 2], [1, 3])
differenzen = _echte_differenzen
assert ergebnis == (0, 1) and len(aufrufe) == 1, (
    f"vergleich([2, 2], [1, 3]) ergibt {ergebnis!r} und ruft differenzen {len(aufrufe)}-mal auf; erwartet war (0, 1) "
    "mit genau einem Aufruf von differenzen.\nTipp: Rufen Sie differenzen einmal auf und merken Sie sich die Liste; "
    "ein zweiter Aufruf fände bei Iteratoren keine Werte mehr."
)

# 300 zufällige Angebote, als Liste und als Iterator
zufall = Zufall(3021)
for _ in range(300):
    jahre = zufall.randint(0, 8)
    a = [zufall.choice([0, 300, 500, 1200, 10**7]) for _ in range(jahre)]
    b = [zufall.choice([0, 300, 500, 1200, 10**7]) for _ in range(jahre)]
    erwartet_diff = [b[i] - a[i] for i in range(jahre)]
    erwartet_vergleich = (sum(b) - sum(a), len([i for i in range(jahre) if b[i] < a[i]]))
    ergebnis = (differenzen(iter(a), Einmalig(b)), vergleich(Einmalig(a), iter(b)))
    assert ergebnis == (erwartet_diff, erwartet_vergleich), (
        f"Mit a = {a} und b = {b} (als Iteratoren) ergeben differenzen und vergleich {ergebnis!r}, "
        f"erwartet war {(erwartet_diff, erwartet_vergleich)!r}."
    )
    if jahre > 0:
        erwartet = (sum(a), max(a), len(a))
        ergebnis = kostenbericht(map(int, [str(wert) for wert in a]))
        assert ergebnis == erwartet, f"kostenbericht mit einem map-Iterator über {a} ergibt {ergebnis!r}, erwartet war {erwartet}."

# An der oberen Grenze: 30 Jahre als Iteratoren
a = [(nummer * 7919 * 104729) % (10**7 + 1) for nummer in range(30)]
b = [(nummer * 104729 * 7919 * 13) % (10**7 + 1) for nummer in range(30)]
ergebnis = kostenbericht(iter(a))
assert ergebnis == (sum(a), max(a), 30), f"kostenbericht mit 30 Werten ergibt {ergebnis!r}, erwartet war {(sum(a), max(a), 30)}."

# vergleich an der oberen Grenze: 30 Jahre als map- und reversed-Iterator
ergebnis = vergleich(map(int, a), reversed(b))
erwartet = (sum(b) - sum(a), len([i for i in range(30) if b[29 - i] < a[i]]))
assert ergebnis == erwartet, f"vergleich mit 30 Jahren ergibt {ergebnis!r}, erwartet war {erwartet}."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "(2100, 1200, 4)\n(1500, 500, 3)\n[-700, 200, 200, 200]\n(-100, 1)"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
