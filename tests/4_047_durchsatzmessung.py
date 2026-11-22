# Automatisch erzeugt aus lehrkraft/muster/4_047_durchsatzmessung.py - nicht von Hand ändern.
# vorlage-hash: 16fcf1868765ec72
# text-hash: 21fd41ec6b0991fe
# thema: kontrollfluss
# inhalt: takewhile, dropwhile, compress

def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


class Messung:
    """Liefert Werte einmalig wie ein Generator und zählt, wie viele gelesen wurden; endlos mit nachlauf."""

    def __init__(self, werte, nachlauf=None):
        """Merkt sich die Werte; ist nachlauf nicht None, kommt danach endlos dieser Wert."""
        self.werte = list(werte)
        self.nachlauf = nachlauf
        self.gelesen = 0

    def __iter__(self):
        """Die Messung ist ihr eigener Iterator."""
        return self

    def __next__(self):
        """Liefert den nächsten Wert und zählt mit."""
        if self.gelesen < len(self.werte):
            wert = self.werte[self.gelesen]
        elif self.nachlauf is not None:
            wert = self.nachlauf
        else:
            raise StopIteration
        self.gelesen += 1
        if self.gelesen > 10**6:
            raise RuntimeError("mehr als eine Million Werte gelesen – die Funktion hört nicht auf")
        return wert


def vergleich_anlauf(werte, ziel):
    """Vergleichslösung mit einer Schleife und break."""
    ergebnis = []
    for wert in werte:
        if wert >= ziel:
            break
        ergebnis.append(wert)
    return ergebnis


def vergleich_nach(werte, ziel, sekunden):
    """Vergleichslösung über die Stelle des ersten Werts ab ziel."""
    for stelle, wert in enumerate(werte):
        if wert >= ziel:
            return werte[stelle : stelle + sekunden]
    return []


def vergleich_verlust(werte, verluste):
    """Vergleichslösung mit zip."""
    return [wert for wert, verlust in zip(werte, verluste) if verlust]


WERTE = [40, 120, 450, 910, 960, 700, 950]

# anlaufphase im Beispiel
ergebnis = wert_von(lambda: anlaufphase(list(WERTE), 900))
assert ergebnis == [40, 120, 450], (
    f"anlaufphase({WERTE}, 900) ergibt {ergebnis!r}, erwartet war [40, 120, 450].\n"
    "Tipp: list(takewhile(lambda wert: wert < ziel, durchsatz))."
)

# anlaufphase mit anderen Werten (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: anlaufphase([5, 10, 20, 40, 80, 160], 50))
assert ergebnis == [5, 10, 20, 40], f"anlaufphase([5, 10, 20, 40, 80, 160], 50) ergibt {ergebnis!r}, erwartet war [5, 10, 20, 40]."

# anlaufphase: spätere Einbrüche gehören nicht zur Anlaufphase
ergebnis = wert_von(lambda: anlaufphase([100, 990, 300, 200], 900))
assert ergebnis == [100], (
    f"anlaufphase([100, 990, 300, 200], 900) ergibt {ergebnis!r}, erwartet war [100].\n"
    "Tipp: Die Anlaufphase endet beim ersten Wert ab ziel; eine Comprehension mit if nimmt auch die Einbrüche danach."
)

# anlaufphase: ein Wert genau gleich ziel beendet die Anlaufphase
ergebnis = wert_von(lambda: anlaufphase([300, 600, 900, 100], 900))
assert ergebnis == [300, 600], f"anlaufphase([300, 600, 900, 100], 900) ergibt {ergebnis!r}, erwartet war [300, 600] (900 ist schon mindestens ziel)."

# anlaufphase: sofort am Ziel, nie am Ziel, keine Werte, ziel 0
ergebnis = wert_von(lambda: [anlaufphase([950, 10], 900), anlaufphase([1, 2, 3], 900), anlaufphase([], 900), anlaufphase([0, 5], 0)])
assert ergebnis == [[], [1, 2, 3], [], []], (
    f"anlaufphase für [950, 10], [1, 2, 3], [] (ziel 900) und [0, 5] (ziel 0) ergibt {ergebnis!r}, erwartet war [[], [1, 2, 3], [], []]."
)

# anlaufphase liest einen endlosen Generator nur bis zum ersten Wert ab ziel
messung = Messung([10, 20, 30, 950], nachlauf=5)
ergebnis = wert_von(lambda: anlaufphase(messung, 900))
assert ergebnis == [10, 20, 30] and messung.gelesen == 4, (
    f"anlaufphase auf einer endlosen Messung, die mit 10, 20, 30, 950 beginnt, ergibt {ergebnis!r} und liest {messung.gelesen} Werte; "
    "erwartet war [10, 20, 30] nach genau 4 gelesenen Werten."
)

# anlaufphase benutzt takewhile
assert verwendet("takewhile"), "Benutzen Sie in anlaufphase itertools.takewhile."

# nach_dem_anlauf im Beispiel
ergebnis = wert_von(lambda: nach_dem_anlauf(list(WERTE), 900, 3))
assert ergebnis == [910, 960, 700], (
    f"nach_dem_anlauf({WERTE}, 900, 3) ergibt {ergebnis!r}, erwartet war [910, 960, 700].\n"
    "Tipp: dropwhile überspringt die Anlaufphase, islice(..., sekunden) nimmt danach die ersten sekunden Werte."
)

# nach_dem_anlauf mit anderen Werten, Einbrüche bleiben drin
ergebnis = wert_von(lambda: nach_dem_anlauf([1, 2, 60, 3, 70, 4, 80], 50, 4))
assert ergebnis == [60, 3, 70, 4], (
    f"nach_dem_anlauf([1, 2, 60, 3, 70, 4, 80], 50, 4) ergibt {ergebnis!r}, erwartet war [60, 3, 70, 4].\n"
    "Tipp: Nach dem ersten Wert ab ziel prüft dropwhile nichts mehr; Werte unter ziel bleiben drin."
)

# nach_dem_anlauf: weniger Werte als sekunden, und sekunden 0
ergebnis = wert_von(lambda: [nach_dem_anlauf([10, 900, 800], 900, 5), nach_dem_anlauf([10, 900, 800], 900, 0)])
assert ergebnis == [[900, 800], []], f"nach_dem_anlauf([10, 900, 800], 900, 5) und (…, 0) ergeben {ergebnis!r}, erwartet war [[900, 800], []]."

# nach_dem_anlauf: nie am Ziel, sofort am Ziel, keine Werte
ergebnis = wert_von(lambda: [nach_dem_anlauf([1, 2], 900, 3), nach_dem_anlauf([905, 1, 2, 3], 900, 3), nach_dem_anlauf([], 0, 3)])
assert ergebnis == [[], [905, 1, 2], []], (
    f"nach_dem_anlauf für [1, 2], [905, 1, 2, 3] (ziel 900) und [] ergibt {ergebnis!r}, erwartet war [[], [905, 1, 2], []]."
)

# nach_dem_anlauf liest einen endlosen Generator nur so weit wie nötig
messung = Messung([10, 20, 950, 940], nachlauf=930)
ergebnis = wert_von(lambda: nach_dem_anlauf(messung, 900, 5))
assert ergebnis == [950, 940, 930, 930, 930] and messung.gelesen == 7, (
    f"nach_dem_anlauf auf einer endlosen Messung ergibt {ergebnis!r} und liest {messung.gelesen} Werte; "
    "erwartet war [950, 940, 930, 930, 930] nach genau 7 gelesenen Werten.\n"
    "Tipp: list(dropwhile(...)) liest eine endlose Messung ohne Ende; begrenzen Sie vorher mit islice."
)

# nach_dem_anlauf benutzt dropwhile
assert verwendet("dropwhile"), "Benutzen Sie in nach_dem_anlauf itertools.dropwhile."

# mit_verlust im Beispiel
ergebnis = wert_von(lambda: mit_verlust(list(WERTE), [0, 0, 0, 0, 2, 5, 0]))
assert ergebnis == [960, 700], (
    f"mit_verlust({WERTE}, [0, 0, 0, 0, 2, 5, 0]) ergibt {ergebnis!r}, erwartet war [960, 700].\n"
    "Tipp: list(compress(durchsatz, verluste)) nimmt die Werte, bei denen verluste nicht 0 ist."
)

# mit_verlust: jede Zahl über 0 zählt, nicht nur 1
ergebnis = wert_von(lambda: mit_verlust([10, 20, 30, 40], [1, 0, 1000, 7]))
assert ergebnis == [10, 30, 40], f"mit_verlust([10, 20, 30, 40], [1, 0, 1000, 7]) ergibt {ergebnis!r}, erwartet war [10, 30, 40]."

# mit_verlust: endet mit der kürzeren Folge
ergebnis = wert_von(lambda: [mit_verlust([10, 20, 30], [1, 1, 1, 1, 1]), mit_verlust([10, 20, 30, 40], [0, 3])])
assert ergebnis == [[10, 20, 30], [20]], (
    f"mit_verlust([10, 20, 30], [1, 1, 1, 1, 1]) und mit_verlust([10, 20, 30, 40], [0, 3]) ergeben {ergebnis!r}, erwartet war [[10, 20, 30], [20]]."
)

# mit_verlust: ohne Verluste und ohne Werte
ergebnis = wert_von(lambda: [mit_verlust([10, 20], [0, 0]), mit_verlust([], []), mit_verlust([5], [])])
assert ergebnis == [[], [], []], f"mit_verlust ohne Verluste oder ohne Werte ergibt {ergebnis!r}, erwartet war [[], [], []]."

# mit_verlust mit einer endlosen Messung und einer endlichen Liste von Verlusten
messung = Messung([500, 600], nachlauf=700)
ergebnis = wert_von(lambda: mit_verlust(messung, [0, 1, 0, 1]))
assert ergebnis == [600, 700], (
    f"mit_verlust auf einer endlosen Messung mit verluste = [0, 1, 0, 1] ergibt {ergebnis!r}, erwartet war [600, 700].\n"
    "Tipp: compress hört auf, sobald eine der beiden Folgen zu Ende ist; len(durchsatz) gibt es bei einem Generator nicht."
)

# mit_verlust benutzt compress
assert verwendet("compress"), "Benutzen Sie in mit_verlust itertools.compress."

# Die Ausgabe des Programms
erwartet = "[40, 120, 450]\n[910, 960, 700]\n[960, 700]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Messreihen, mal als Liste, mal als einmaliger Iterator
zufall = Zufall(4047)
for runde in range(300):
    werte = [zufall.choice([zufall.randint(0, 100), zufall.randint(800, 1000)]) for _ in range(zufall.randint(0, 12))]
    ziel = zufall.choice([0, 50, 500, 900, 1001])
    sekunden = zufall.randint(0, 8)
    verluste = [zufall.choice([0, 0, 1, 3]) for _ in range(zufall.randint(0, 12))]
    quelle = (lambda: list(werte)) if runde % 2 == 0 else (lambda: iter(werte))
    ergebnis = wert_von(lambda: anlaufphase(quelle(), ziel))
    assert ergebnis == vergleich_anlauf(werte, ziel), f"anlaufphase({werte}, {ziel}) ergibt {ergebnis!r}, erwartet war {vergleich_anlauf(werte, ziel)}."
    ergebnis = wert_von(lambda: nach_dem_anlauf(quelle(), ziel, sekunden))
    erwartet = vergleich_nach(werte, ziel, sekunden)
    assert ergebnis == erwartet, f"nach_dem_anlauf({werte}, {ziel}, {sekunden}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    ergebnis = wert_von(lambda: mit_verlust(quelle(), verluste))
    erwartet = vergleich_verlust(werte, verluste)
    assert ergebnis == erwartet, f"mit_verlust({werte}, {verluste}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 100 000 Werte
werte = [zufall.randint(0, 899) for _ in range(99999)] + [10000]
verluste = [zufall.randint(0, 2) for _ in range(100000)]
ergebnis = wert_von(lambda: [len(anlaufphase(iter(werte), 900)), nach_dem_anlauf(iter(werte), 900, 100000), mit_verlust(iter(werte), verluste)])
assert ergebnis == [99999, [10000], vergleich_verlust(werte, verluste)], "Bei 100 000 Messwerten stimmen die Ergebnisse nicht."
# Obere Grenze: 100 000 Werte nach dem Anlauf aus einer endlosen Messung
messung = Messung([0] * 99999 + [900], nachlauf=950)
ergebnis = wert_von(lambda: len(nach_dem_anlauf(messung, 900, 100000)))
assert ergebnis == 100000 and messung.gelesen == 199999, (
    f"nach_dem_anlauf(…, 900, 100000) auf einer endlosen Messung ergibt {ergebnis!r} Werte nach {messung.gelesen} gelesenen, "
    "erwartet waren 100 000 Werte nach 199 999 gelesenen."
)
