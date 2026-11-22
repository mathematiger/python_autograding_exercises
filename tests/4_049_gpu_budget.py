# Automatisch erzeugt aus lehrkraft/muster/4_049_gpu_budget.py - nicht von Hand ändern.
# vorlage-hash: af9a4b1bdf325e02
# text-hash: 57cb6b699f370bc9
# thema: kontrollfluss
# inhalt: Übung: itertools

def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def einmalig(werte):
    """Ein Generator, der die Werte genau einmal liefert (ohne len und ohne Indizes)."""
    yield from werte


class Abrechnung:
    """Ein endloser Iterator: erst die Werte, dann immer wieder nachlauf; zählt die gelesenen Werte."""

    def __init__(self, werte, nachlauf):
        """Merkt sich die Werte und den Wert, der danach endlos kommt."""
        self.werte = list(werte)
        self.nachlauf = nachlauf
        self.gelesen = 0

    def __iter__(self):
        """Die Abrechnung ist ihr eigener Iterator."""
        return self

    def __next__(self):
        """Liefert den nächsten Wert und zählt mit."""
        wert = self.werte[self.gelesen] if self.gelesen < len(self.werte) else self.nachlauf
        self.gelesen += 1
        if self.gelesen > 10**6:
            raise RuntimeError("mehr als eine Million Werte gelesen – die Funktion hört nicht auf")
        return wert


def vergleich_stunden(werte, budget):
    """Vergleichslösung mit einer Schleife."""
    summe = 0
    for stunden, wert in enumerate(werte):
        summe += wert
        if summe > budget:
            return stunden
    return len(werte)


def vergleich_spruenge(werte, grenze):
    """Vergleichslösung mit Indizes."""
    return [stelle for stelle in range(1, len(werte)) if werte[stelle] - werte[stelle - 1] > grenze]


def vergleich_tage(protokoll):
    """Vergleichslösung: neue Gruppe, sobald sich das Datum ändert."""
    ergebnis = []
    for datum, cent in protokoll:
        if ergebnis and ergebnis[-1][0] == datum:
            ergebnis[-1] = (datum, ergebnis[-1][1] + cent)
        else:
            ergebnis.append((datum, cent))
    return ergebnis


KOSTEN = [120, 80, 300, 90, 450, 60]

# stunden_bis_budget im Beispiel: genau 500 Cent passen noch
ergebnis = wert_von(lambda: stunden_bis_budget(einmalig(KOSTEN), 500))
assert ergebnis == 3, (
    f"stunden_bis_budget({KOSTEN}, 500) ergibt {ergebnis!r}, erwartet war 3 (120 + 80 + 300 = 500, mit der vierten Stunde 590).\n"
    "Tipp: takewhile(lambda summe: summe <= budget, accumulate(kosten)) liefert die Summen, die ins Budget passen."
)

# stunden_bis_budget mit einem anderen Budget (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: [stunden_bis_budget(einmalig(KOSTEN), 499), stunden_bis_budget(einmalig(KOSTEN), 1000)])
assert ergebnis == [2, 4], f"stunden_bis_budget({KOSTEN}, 499) und (…, 1000) ergeben {ergebnis!r}, erwartet war [2, 4]."

# stunden_bis_budget: schon die erste Stunde ist zu teuer
ergebnis = wert_von(lambda: stunden_bis_budget(einmalig([600, 10]), 500))
assert ergebnis == 0, f"stunden_bis_budget([600, 10], 500) ergibt {ergebnis!r}, erwartet war 0."

# stunden_bis_budget: alles passt ins Budget, auch ohne Stunden
ergebnis = wert_von(lambda: [stunden_bis_budget(einmalig([1, 2, 3]), 6), stunden_bis_budget(einmalig([]), 0)])
assert ergebnis == [3, 0], f"stunden_bis_budget([1, 2, 3], 6) und stunden_bis_budget([], 0) ergeben {ergebnis!r}, erwartet war [3, 0]."

# stunden_bis_budget: kostenlose Stunden zählen mit, auch bei budget 0
ergebnis = wert_von(lambda: [stunden_bis_budget(einmalig([0, 0, 5, 0]), 0), stunden_bis_budget(einmalig([0, 3, 0, 0, 9]), 3)])
assert ergebnis == [2, 4], (
    f"stunden_bis_budget([0, 0, 5, 0], 0) und stunden_bis_budget([0, 3, 0, 0, 9], 3) ergeben {ergebnis!r}, erwartet war [2, 4].\n"
    "Tipp: Entscheidend ist die laufende Summe, nicht die einzelne Stunde."
)

# stunden_bis_budget liest eine endlose Abrechnung nur bis zur ersten Stunde über dem Budget
abrechnung = Abrechnung([100, 200, 300], nachlauf=50)
ergebnis = wert_von(lambda: stunden_bis_budget(abrechnung, 800))
assert ergebnis == 7 and abrechnung.gelesen == 8, (
    f"stunden_bis_budget auf einer endlosen Abrechnung (100, 200, 300, dann immer 50) mit budget 800 ergibt {ergebnis!r} "
    f"nach {abrechnung.gelesen} gelesenen Werten, erwartet war 7 nach genau 8 gelesenen Werten.\n"
    "Tipp: list(accumulate(kosten)) hört bei einem endlosen Iterator nie auf; schalten Sie takewhile direkt dahinter."
)

# stunden_bis_budget benutzt accumulate und takewhile
assert verwendet("accumulate") and verwendet("takewhile"), "Benutzen Sie in stunden_bis_budget accumulate und takewhile."

# kostenspruenge im Beispiel
ergebnis = wert_von(lambda: kostenspruenge(einmalig(KOSTEN), 150))
assert ergebnis == [2, 4], (
    f"kostenspruenge({KOSTEN}, 150) ergibt {ergebnis!r}, erwartet war [2, 4].\n"
    "Tipp: enumerate(pairwise(kosten), start=1) liefert die Stelle der späteren Stunde mit."
)

# kostenspruenge mit einer anderen Grenze
ergebnis = wert_von(lambda: kostenspruenge(einmalig(KOSTEN), 300))
assert ergebnis == [4], f"kostenspruenge({KOSTEN}, 300) ergibt {ergebnis!r}, erwartet war [4]."

# kostenspruenge: genau grenze teurer ist kein Sprung, billiger auch nicht
ergebnis = wert_von(lambda: kostenspruenge(einmalig([100, 250, 100, 251, 0]), 150))
assert ergebnis == [3], (
    f"kostenspruenge([100, 250, 100, 251, 0], 150) ergibt {ergebnis!r}, erwartet war [3].\n"
    "Tipp: Ein Sprung ist nur, was um mehr als grenze teurer ist; ein Preisrückgang zählt nicht (kein abs)."
)

# kostenspruenge mit grenze 0, ohne und mit einer Stunde
ergebnis = wert_von(lambda: [kostenspruenge(einmalig([5, 5, 6]), 0), kostenspruenge(einmalig([]), 0), kostenspruenge(einmalig([7]), 0)])
assert ergebnis == [[2], [], []], f"kostenspruenge mit grenze 0 für [5, 5, 6], [] und [7] ergibt {ergebnis!r}, erwartet war [[2], [], []]."

# kostenspruenge benutzt pairwise
assert verwendet("pairwise"), "Benutzen Sie in kostenspruenge itertools.pairwise."

# kosten_je_tag im Beispiel
protokoll = [("2026-11-02", 120), ("2026-11-02", 80), ("2026-11-03", 300)]
ergebnis = wert_von(lambda: kosten_je_tag(einmalig(protokoll)))
assert ergebnis == [("2026-11-02", 200), ("2026-11-03", 300)], (
    f"kosten_je_tag({protokoll}) ergibt {ergebnis!r}, erwartet war [('2026-11-02', 200), ('2026-11-03', 300)].\n"
    "Tipp: groupby(protokoll, key=lambda eintrag: eintrag[0]) liefert je Tag das Datum und die Einträge dieses Tages."
)

# kosten_je_tag mit drei Tagen (nicht fest hinschreiben!)
protokoll = [("2026-11-04", 5), ("2026-11-05", 1), ("2026-11-05", 2), ("2026-11-05", 3), ("2026-11-06", 0)]
ergebnis = wert_von(lambda: kosten_je_tag(einmalig(protokoll)))
assert ergebnis == [("2026-11-04", 5), ("2026-11-05", 6), ("2026-11-06", 0)], (
    f"kosten_je_tag({protokoll}) ergibt {ergebnis!r}, erwartet war [('2026-11-04', 5), ('2026-11-05', 6), ('2026-11-06', 0)]."
)

# kosten_je_tag: die Reihenfolge des Protokolls bleibt, auch wenn sie nicht sortiert ist
protokoll = [("2026-12-01", 7), ("2026-11-30", 3), ("2026-11-30", 4)]
ergebnis = wert_von(lambda: kosten_je_tag(einmalig(protokoll)))
assert ergebnis == [("2026-12-01", 7), ("2026-11-30", 7)], (
    f"kosten_je_tag({protokoll}) ergibt {ergebnis!r}, erwartet war [('2026-12-01', 7), ('2026-11-30', 7)] (Reihenfolge des Protokolls)."
)

# kosten_je_tag ohne Einträge
ergebnis = wert_von(lambda: kosten_je_tag(einmalig([])))
assert ergebnis == [], f"kosten_je_tag([]) ergibt {ergebnis!r}, erwartet war []."

# kosten_je_tag benutzt groupby
assert verwendet("groupby"), "Benutzen Sie in kosten_je_tag itertools.groupby."

# Die Ausgabe des Programms
erwartet = "3\n[2, 4]\n[('2026-11-02', 200), ('2026-11-03', 300)]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Abrechnungen
zufall = Zufall(4049)
for _ in range(300):
    werte = [zufall.choice([0, zufall.randint(0, 200), zufall.randint(0, 100000)]) for _ in range(zufall.randint(0, 12))]
    budget = zufall.choice([0, zufall.randint(0, 1000), zufall.randint(0, 10**6)])
    ergebnis = wert_von(lambda: stunden_bis_budget(einmalig(werte), budget))
    erwartet = vergleich_stunden(werte, budget)
    assert ergebnis == erwartet, f"stunden_bis_budget({werte}, {budget}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    grenze = zufall.choice([0, 50, 1000, 100000])
    ergebnis = wert_von(lambda: kostenspruenge(einmalig(werte), grenze))
    erwartet = vergleich_spruenge(werte, grenze)
    assert ergebnis == erwartet, f"kostenspruenge({werte}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    protokoll = [(f"2026-11-{zufall.randint(1, 3):02d}", wert) for wert in werte]
    ergebnis = wert_von(lambda: kosten_je_tag(einmalig(protokoll)))
    erwartet = vergleich_tage(protokoll)
    assert ergebnis == erwartet, f"kosten_je_tag({protokoll}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 200 000 Stunden, größtes Budget
werte = [zufall.randint(0, 100000) for _ in range(200000)]
protokoll = [(f"2026-{1 + stelle // 20000:02d}-{1 + stelle // 1000 % 20:02d}", wert) for stelle, wert in enumerate(werte)]
ergebnis = wert_von(lambda: [stunden_bis_budget(einmalig(werte), 10**12), stunden_bis_budget(einmalig(werte), 5 * 10**9)])
assert ergebnis == [200000, vergleich_stunden(werte, 5 * 10**9)], f"stunden_bis_budget mit 200 000 Stunden ergibt {ergebnis!r}."
# Obere Grenze: kostenspruenge und kosten_je_tag mit 200 000 Einträgen
ergebnis = wert_von(lambda: [kostenspruenge(einmalig(werte), 90000), kosten_je_tag(einmalig(protokoll))])
assert ergebnis == [vergleich_spruenge(werte, 90000), vergleich_tage(protokoll)], (
    "Bei 200 000 Stunden stimmen kostenspruenge oder kosten_je_tag nicht mit der Vergleichslösung überein."
)
