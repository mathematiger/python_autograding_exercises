# Automatisch erzeugt aus lehrkraft/muster/4_048_rackzaehler.py - nicht von Hand ändern.
# vorlage-hash: 51de180be020b02d
# text-hash: 1c797611616c9ff9
# thema: kontrollfluss
# inhalt: pairwise und tee

def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def einmalig(werte):
    """Ein Generator, der die Werte genau einmal liefert (ohne len und ohne Indizes)."""
    yield from werte


def vergleich_verbrauch(werte):
    """Vergleichslösung mit Indizes auf einer Liste."""
    return [werte[stelle] - werte[stelle - 1] for stelle in range(1, len(werte))]


def vergleich_rueck(werte):
    """Vergleichslösung mit Indizes auf einer Liste."""
    return [stelle for stelle in range(1, len(werte)) if werte[stelle] < werte[stelle - 1]]


def vergleich_abstand(werte, abstand):
    """Vergleichslösung mit Indizes auf einer Liste."""
    return [werte[stelle + abstand] - werte[stelle] for stelle in range(len(werte) - abstand)]


# verbraeuche im Beispiel
ergebnis = wert_von(lambda: verbraeuche(einmalig([100, 112, 125, 125, 140])))
assert ergebnis == [12, 13, 0, 15], (
    f"verbraeuche mit den Zählerständen 100, 112, 125, 125, 140 ergibt {ergebnis!r}, erwartet war [12, 13, 0, 15].\n"
    "Tipp: for frueher, spaeter in pairwise(zaehlerstaende) liefert jedes Paar aus Stand und Nachfolger."
)

# verbraeuche mit anderen Werten (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: verbraeuche(einmalig([0, 1000, 2500])))
assert ergebnis == [1000, 1500], f"verbraeuche mit 0, 1000, 2500 ergibt {ergebnis!r}, erwartet war [1000, 1500] (späterer minus früherer Stand)."

# verbraeuche: ein Rücksprung ergibt einen negativen Verbrauch
ergebnis = wert_von(lambda: verbraeuche(einmalig([50, 40, 45])))
assert ergebnis == [-10, 5], f"verbraeuche mit 50, 40, 45 ergibt {ergebnis!r}, erwartet war [-10, 5]."

# verbraeuche mit keinem und mit einem Zählerstand
ergebnis = wert_von(lambda: [verbraeuche(einmalig([])), verbraeuche(einmalig([123]))])
assert ergebnis == [[], []], f"verbraeuche ohne und mit einem Zählerstand ergibt {ergebnis!r}, erwartet war [[], []]."

# verbraeuche benutzt pairwise
assert verwendet("pairwise"), "Benutzen Sie in verbraeuche und rueckspruenge itertools.pairwise."

# rueckspruenge im Beispiel
ergebnis = wert_von(lambda: rueckspruenge(einmalig([500, 520, 3, 9, 8])))
assert ergebnis == [2, 4], (
    f"rueckspruenge mit 500, 520, 3, 9, 8 ergibt {ergebnis!r}, erwartet war [2, 4].\n"
    "Tipp: enumerate(pairwise(zaehlerstaende), start=1) gibt jedem Paar die Stelle seines zweiten Werts."
)

# rueckspruenge: gleich bleibende Stände sind kein Rücksprung
ergebnis = wert_von(lambda: rueckspruenge(einmalig([7, 7, 7, 6, 6])))
assert ergebnis == [3], f"rueckspruenge mit 7, 7, 7, 6, 6 ergibt {ergebnis!r}, erwartet war [3] (nur echt kleinere Stände)."

# rueckspruenge: Rücksprung gleich an der zweiten Stelle
ergebnis = wert_von(lambda: rueckspruenge(einmalig([9, 0, 1, 2])))
assert ergebnis == [1], f"rueckspruenge mit 9, 0, 1, 2 ergibt {ergebnis!r}, erwartet war [1]."

# rueckspruenge: ohne Rücksprung, ohne und mit einem Wert
ergebnis = wert_von(lambda: [rueckspruenge(einmalig([1, 2, 3])), rueckspruenge(einmalig([])), rueckspruenge(einmalig([5]))])
assert ergebnis == [[], [], []], f"rueckspruenge ohne Rücksprung, ohne und mit einem Wert ergibt {ergebnis!r}, erwartet war [[], [], []]."

# vergleich im Beispiel
ergebnis = wert_von(lambda: vergleich(einmalig([10, 12, 11, 15, 13]), 2))
assert ergebnis == [1, 3, 2], (
    f"vergleich mit 10, 12, 11, 15, 13 und abstand 2 ergibt {ergebnis!r}, erwartet war [1, 3, 2].\n"
    "Tipp: frueher, spaeter = tee(tageswerte); schieben Sie spaeter mit islice(spaeter, abstand, None) vor."
)

# vergleich mit abstand 1 ist der Unterschied zum Vortag
ergebnis = wert_von(lambda: vergleich(einmalig([4, 9, 2]), 1))
assert ergebnis == [5, -7], f"vergleich mit 4, 9, 2 und abstand 1 ergibt {ergebnis!r}, erwartet war [5, -7]."

# vergleich mit abstand 7 über zwei Wochen
woche1 = [30, 32, 31, 29, 35, 10, 9]
woche2 = [33, 30, 31, 40, 35, 12, 8]
ergebnis = wert_von(lambda: vergleich(einmalig(woche1 + woche2), 7))
erwartet = [neu - alt for alt, neu in zip(woche1, woche2)]
assert ergebnis == erwartet, f"vergleich über zwei Wochen mit abstand 7 ergibt {ergebnis!r}, erwartet war {erwartet}."

# vergleich: abstand so groß wie die Zahl der Werte oder größer
ergebnis = wert_von(lambda: [vergleich(einmalig([1, 2, 3]), 3), vergleich(einmalig([1, 2]), 1000), vergleich(einmalig([]), 1)])
assert ergebnis == [[], [], []], (
    f"vergleich mit 3 Werten und abstand 3, mit 2 Werten und abstand 1000 und ohne Werte ergibt {ergebnis!r}, erwartet war [[], [], []]."
)

# vergleich benutzt tee
assert verwendet("tee"), "Benutzen Sie in vergleich itertools.tee, wie verlangt."

# Die Ausgabe des Programms
erwartet = "[12, 13, 0, 15]\n[2, 4]\n[1, 3, 2]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Zählerstände und Tageswerte
zufall = Zufall(4048)
for _ in range(300):
    werte = []
    stand = zufall.randint(0, 10**6)
    for _ in range(zufall.randint(0, 15)):
        stand = zufall.randint(0, 50) if zufall.random() < 0.15 else stand + zufall.randint(0, 40)
        werte.append(stand)
    ergebnis = wert_von(lambda: verbraeuche(einmalig(werte)))
    assert ergebnis == vergleich_verbrauch(werte), f"verbraeuche({werte}) ergibt {ergebnis!r}, erwartet war {vergleich_verbrauch(werte)}."
    ergebnis = wert_von(lambda: rueckspruenge(einmalig(werte)))
    assert ergebnis == vergleich_rueck(werte), f"rueckspruenge({werte}) ergibt {ergebnis!r}, erwartet war {vergleich_rueck(werte)}."
    abstand = zufall.randint(1, 8)
    ergebnis = wert_von(lambda: vergleich(einmalig(werte), abstand))
    erwartet = vergleich_abstand(werte, abstand)
    assert ergebnis == erwartet, f"vergleich({werte}, {abstand}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 200 000 Werte, abstand 1000
werte = [zufall.randint(0, 10**9) for _ in range(200000)]
ergebnis = wert_von(lambda: [verbraeuche(einmalig(werte)), rueckspruenge(einmalig(werte)), vergleich(einmalig(werte), 1000)])
erwartet = [vergleich_verbrauch(werte), vergleich_rueck(werte), vergleich_abstand(werte, 1000)]
assert ergebnis == erwartet, "Bei 200 000 Werten stimmen die Ergebnisse nicht mit der Vergleichslösung überein."
