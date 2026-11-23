# Automatisch erzeugt aus lehrkraft/muster/4_043_trainingsverlauf.py - nicht von Hand ändern.
# vorlage-hash: ba9a97c0c63b4ced
# text-hash: 1e93ea60ddf7295c
# thema: kontrollfluss
# inhalt: accumulate: laufende Werte

def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_abbruch(genauigkeiten, geduld):
    """Vergleichslösung: sucht für jede Epoche das Maximum von vorn (langsam, aber offensichtlich richtig)."""
    for epoche in range(geduld + 1, len(genauigkeiten) + 1):
        if max(genauigkeiten[:epoche]) == max(genauigkeiten[: epoche - geduld]):
            return epoche
    return None


BEISPIEL = [61.0, 70.5, 68.2, 74.1, 73.9, 74.1, 72.0]

# trainingszeit im Beispiel
ergebnis = wert_von(lambda: trainingszeit([30, 28, 31]))
assert ergebnis == [30, 58, 89], (
    f"trainingszeit([30, 28, 31]) ergibt {ergebnis!r}, erwartet war [30, 58, 89].\n"
    "Tipp: list(accumulate(sekunden)) liefert alle Zwischensummen."
)

# trainingszeit mit anderen Werten (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: [trainingszeit([5, 5, 5, 5]), trainingszeit([10000])])
assert ergebnis == [[5, 10, 15, 20], [10000]], (
    f"trainingszeit([5, 5, 5, 5]) und trainingszeit([10000]) ergeben {ergebnis!r}, erwartet war [[5, 10, 15, 20], [10000]]."
)

# trainingszeit ohne Epochen
ergebnis = wert_von(lambda: trainingszeit([]))
assert ergebnis == [], f"trainingszeit([]) ergibt {ergebnis!r}, erwartet war []."

# trainingszeit gibt eine Liste zurück
ergebnis = wert_von(lambda: trainingszeit([1, 2]))
assert isinstance(ergebnis, list), f"trainingszeit([1, 2]) gibt {type(ergebnis).__name__} zurück, erwartet war eine Liste."

# bestwerte im Beispiel
ergebnis = wert_von(lambda: bestwerte(BEISPIEL))
erwartet = [61.0, 70.5, 70.5, 74.1, 74.1, 74.1, 74.1]
assert ergebnis == erwartet, (
    f"bestwerte({BEISPIEL}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: accumulate(genauigkeiten, max) liefert das laufende Maximum."
)

# bestwerte: fallende und steigende Genauigkeiten
ergebnis = wert_von(lambda: [bestwerte([90.0, 80.0, 70.0]), bestwerte([10.0, 20.0, 30.0])])
assert ergebnis == [[90.0, 90.0, 90.0], [10.0, 20.0, 30.0]], (
    f"bestwerte([90.0, 80.0, 70.0]) und bestwerte([10.0, 20.0, 30.0]) ergeben {ergebnis!r}, "
    "erwartet war [[90.0, 90.0, 90.0], [10.0, 20.0, 30.0]]."
)

# bestwerte ohne Epochen und mit 0 und 100 Prozent
ergebnis = wert_von(lambda: [bestwerte([]), bestwerte([0.0, 100.0, 0.0])])
assert ergebnis == [[], [0.0, 100.0, 100.0]], f"bestwerte([]) und bestwerte([0.0, 100.0, 0.0]) ergeben {ergebnis!r}, erwartet war [[], [0.0, 100.0, 100.0]]."

# bestwerte lässt die übergebene Liste unverändert
werte = [3.0, 1.0, 2.0]
wert_von(lambda: bestwerte(werte))
assert werte == [3.0, 1.0, 2.0], f"Nach bestwerte([3.0, 1.0, 2.0]) ist die Liste {werte}, erwartet war sie unverändert."

# accumulate wird benutzt
assert verwendet("accumulate"), "Benutzen Sie itertools.accumulate."

# abbruch_nach im Beispiel mit geduld 2
ergebnis = wert_von(lambda: abbruch_nach(BEISPIEL, 2))
assert ergebnis == 6, (
    f"abbruch_nach(genauigkeiten, 2) ergibt {ergebnis!r}, erwartet war 6 "
    "(Bestwert nach Epoche 6 und nach Epoche 4 ist 74.1).\n"
    "Tipp: Vergleichen Sie in der Liste der Bestwerte die Stellen e - 1 und e - 1 - geduld."
)

# abbruch_nach im Beispiel mit geduld 4: kein Abbruch
ergebnis = wert_von(lambda: abbruch_nach(BEISPIEL, 4))
assert ergebnis is None, f"abbruch_nach(genauigkeiten, 4) ergibt {ergebnis!r}, erwartet war None (Bestwert nach 7 ist 74.1, nach 3 noch 70.5)."

# abbruch_nach mit geduld 1: die erste Epoche ohne Verbesserung
ergebnis = wert_von(lambda: abbruch_nach(BEISPIEL, 1))
assert ergebnis == 3, f"abbruch_nach(genauigkeiten, 1) ergibt {ergebnis!r}, erwartet war 3 (Epoche 3 ist schlechter als Epoche 2)."

# Eine gleich gute Genauigkeit ist keine Verbesserung
ergebnis = wert_von(lambda: abbruch_nach([50.0, 60.0, 60.0, 60.0], 2))
assert ergebnis == 4, (
    f"abbruch_nach([50.0, 60.0, 60.0, 60.0], 2) ergibt {ergebnis!r}, erwartet war 4 "
    "(nach Epoche 4 und Epoche 2 ist der Bestwert 60.0)."
)

# Vor Epoche geduld + 1 wird nicht abgebrochen
ergebnis = wert_von(lambda: [abbruch_nach([80.0, 70.0], 2), abbruch_nach([80.0, 70.0, 60.0], 2)])
assert ergebnis == [None, 3], (
    f"abbruch_nach([80.0, 70.0], 2) und abbruch_nach([80.0, 70.0, 60.0], 2) ergeben {ergebnis!r}, erwartet war [None, 3].\n"
    "Tipp: Für Epoche e braucht man den Bestwert nach Epoche e - geduld, also mindestens geduld + 1 Epochen."
)

# Steigt die Genauigkeit immer, läuft das Training bis zum Ende
ergebnis = wert_von(lambda: [abbruch_nach([1.0, 2.0, 3.0, 4.0], 1), abbruch_nach([], 3), abbruch_nach([55.5], 1)])
assert ergebnis == [None, None, None], (
    f"abbruch_nach([1.0, 2.0, 3.0, 4.0], 1), abbruch_nach([], 3) und abbruch_nach([55.5], 1) ergeben {ergebnis!r}, "
    "erwartet war [None, None, None]."
)

# Eine späte Verbesserung zählt: der Vergleich beginnt geduld Epochen vorher
ergebnis = wert_von(lambda: abbruch_nach([10.0, 20.0, 15.0, 25.0, 24.0, 23.0, 22.0], 3))
assert ergebnis == 7, f"abbruch_nach([10.0, 20.0, 15.0, 25.0, 24.0, 23.0, 22.0], 3) ergibt {ergebnis!r}, erwartet war 7."

# Die Ausgabe des Programms
erwartet = "[30, 58, 89]\n[61.0, 70.5, 70.5, 74.1, 74.1, 74.1, 74.1]\n6\nNone"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Trainingsverläufe
zufall = Zufall(4043)
for _ in range(400):
    anzahl = zufall.randint(0, 12)
    sekunden = [zufall.randint(1, 10000) for _ in range(anzahl)]
    werte = [float(zufall.randint(0, 20) * 5) for _ in range(anzahl)]
    geduld = zufall.randint(1, 5)
    ergebnis = wert_von(lambda: [trainingszeit(sekunden), bestwerte(werte)])
    erwartet = [[sum(sekunden[: stelle + 1]) for stelle in range(anzahl)], [max(werte[: stelle + 1]) for stelle in range(anzahl)]]
    assert ergebnis == erwartet, f"Für sekunden = {sekunden} und genauigkeiten = {werte} ergeben trainingszeit und bestwerte {ergebnis!r}, erwartet war {erwartet!r}."
    ergebnis = wert_von(lambda: abbruch_nach(werte, geduld))
    erwartet = vergleich_abbruch(werte, geduld)
    assert ergebnis == erwartet, f"abbruch_nach({werte}, {geduld}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Laufzeit: abbruch_nach liest jede Genauigkeit nur wenige Male
werte = Zaehlliste([float(stelle) / 1000 for stelle in range(4000)])
ergebnis = wert_von(lambda: abbruch_nach(werte, 10))
assert ergebnis is None and werte.lesezugriffe <= 5 * 4000, (
    f"abbruch_nach liest bei 4000 steigenden Genauigkeiten {werte.lesezugriffe}-mal aus der Liste "
    f"(Ergebnis {ergebnis!r}); bei O(n) wären es höchstens einige Tausend.\n"
    "Tipp: Berechnen Sie die Bestwerte einmal mit accumulate, statt für jede Epoche max(...) von vorn zu suchen."
)

# Obere Grenze: 100 000 Epochen
sekunden = [zufall.randint(1, 10000) for _ in range(100000)]
werte = [stelle / 1000 for stelle in range(99000)] + [50.0] * 1000
ergebnis = wert_von(lambda: [trainingszeit(sekunden)[-1], bestwerte(werte)[-1], abbruch_nach(werte, 1000), abbruch_nach(werte, 999)])
erwartet = [sum(sekunden), 98.999, 100000, 99999]
assert ergebnis == erwartet, (
    f"Bei 100 000 Epochen ergeben die letzte Trainingszeit, der letzte Bestwert und abbruch_nach mit geduld 1000 und 999 "
    f"{ergebnis!r}, erwartet war {erwartet!r}."
)
