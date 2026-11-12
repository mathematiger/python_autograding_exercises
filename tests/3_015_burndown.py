# Automatisch erzeugt aus lehrkraft/muster/3_015_burndown.py - nicht von Hand ändern.
# vorlage-hash: 1de0c75c2e5c5b9f
# text-hash: 796fb7a060d81bf1
# thema: fehler
# inhalt: Debugging mit Wertetabelle

# restpunkte aus dem Beispiel
ergebnis = restpunkte(20, [10, 15, 5])
assert ergebnis == [10, 0, 0], (
    f"restpunkte(20, [10, 15, 5]) ergibt {ergebnis!r}, erwartet war [10, 0, 0].\n"
    "Tipp: Fällt der Rest unter 0, ist er 0; max(rest, 0) hilft dabei."
)

# restpunkte für die Wertetabelle des Kollegen und weitere Fälle
for gesamt, erledigt, erwartet in [
    (20, [8, 7, 5], [12, 5, 0]),
    (20, [5, 5], [15, 10]),
    (5, [0, 0, 2], [5, 5, 3]),
    (0, [3, 0], [0, 0]),
    (7, [], []),
]:
    ergebnis = restpunkte(gesamt, erledigt)
    assert ergebnis == erwartet, (
        f"restpunkte({gesamt}, {erledigt}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Für jeden Sprint kommt genau ein Wert in die Liste, der Rest nach diesem Sprint."
    )

# Ist der Rest einmal 0, bleibt er 0
ergebnis = restpunkte(10, [12, 0, 3])
assert ergebnis == [0, 0, 0], (
    f"restpunkte(10, [12, 0, 3]) ergibt {ergebnis!r}, erwartet war [0, 0, 0]. Ein negativer Rest wird zu 0."
)

# fertig_nach: das Beispiel des Kollegen bleibt richtig
ergebnis = fertig_nach(20, [8, 7, 5])
assert ergebnis == 3, f"fertig_nach(20, [8, 7, 5]) ergibt {ergebnis!r}, erwartet war 3."

# Fertig mit Überschuss: der Sprint wird ab 1 gezählt
ergebnis = fertig_nach(20, [10, 15, 5])
assert ergebnis == 2, (
    f"fertig_nach(20, [10, 15, 5]) ergibt {ergebnis!r}, erwartet war 2.\n"
    "Tipp: In der Wertetabelle steht sprint beim Prüfen noch auf der Zahl des vorigen Sprints."
)

# Genau erledigt zählt als fertig
for gesamt, erledigt, erwartet in [(20, [5, 15, 3], 2), (10, [10], 1), (6, [2, 2, 2], 3)]:
    ergebnis = fertig_nach(gesamt, erledigt)
    assert ergebnis == erwartet, (
        f"fertig_nach({gesamt}, {erledigt}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Ist der Rest genau 0, ist nichts mehr offen; prüfen Sie rest <= 0."
    )

# Nie fertig: -1
for gesamt, erledigt in [(20, [5, 5]), (1, [0, 0, 0]), (3, [])]:
    ergebnis = fertig_nach(gesamt, erledigt)
    assert ergebnis == -1, (
        f"fertig_nach({gesamt}, {erledigt}) ergibt {ergebnis!r}, erwartet war -1, denn die Arbeit wird nie fertig.\n"
        "Tipp: Was gibt die Funktion zurück, wenn die Schleife ganz durchgelaufen ist?"
    )

# Nichts zu tun: 0, auch ohne Sprints
for erledigt in [[3], [0, 5], []]:
    ergebnis = fertig_nach(0, erledigt)
    assert ergebnis == 0, (
        f"fertig_nach(0, {erledigt}) ergibt {ergebnis!r}, erwartet war 0: schon vor dem ersten Sprint war nichts offen."
    )

# Ein Sprint ohne geschaffte Punkte am Anfang
ergebnis = fertig_nach(4, [0, 0, 4, 1])
assert ergebnis == 3, f"fertig_nach(4, [0, 0, 4, 1]) ergibt {ergebnis!r}, erwartet war 3."


# Vergleichslösung: mit Summen der ersten k Sprints
def fertig_von_hand(gesamt, erledigt):
    """Probiert k = 0, 1, 2, … und vergleicht gesamt mit der Summe der ersten k Sprints."""
    for k in range(len(erledigt) + 1):
        if sum(erledigt[:k]) >= gesamt:
            return k
    return -1


# 500 zufällige Projekte: restpunkte
zufall = Zufall(3015)
zufaellige = []
for _ in range(500):
    erledigt = [zufall.choice([0, zufall.randint(0, 10), zufall.randint(0, 200)]) for _ in range(zufall.randint(0, 8))]
    gesamt = zufall.choice([0, zufall.randint(0, 40), sum(erledigt), zufall.randint(0, 10**4)])
    zufaellige.append((gesamt, erledigt))
for gesamt, erledigt in zufaellige:
    erwartet = [max(gesamt - sum(erledigt[: k + 1]), 0) for k in range(len(erledigt))]
    ergebnis = restpunkte(gesamt, erledigt)
    assert ergebnis == erwartet, f"restpunkte({gesamt}, {erledigt}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Dieselben 500 zufälligen Projekte: fertig_nach
for gesamt, erledigt in zufaellige:
    erwartet = fertig_von_hand(gesamt, erledigt)
    ergebnis = fertig_nach(gesamt, erledigt)
    assert ergebnis == erwartet, f"fertig_nach({gesamt}, {erledigt}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Hilfsfunktion für die nächsten Tests: Wie viele Werte von erledigt liest eine Funktion?
def lesezugriffe(funktion, anzahl):
    """Ruft funktion(10**4, erledigt) mit anzahl Sprints zu je 1 Punkt auf und gibt die Lesezugriffe zurück.

    None, wenn die Funktion mit der Zählliste nicht arbeiten kann (z. B. weil sie eine Listenmethode benutzt);
    dann wird die Laufzeit nicht geprüft.
    """
    erledigt = Zaehlliste([1] * anzahl)
    try:
        funktion(10**4, erledigt)
    except (AttributeError, TypeError):
        return None
    return erledigt.lesezugriffe


def laufzeit_meldung(funktion, klein, gross):
    """Baut die Meldung für eine Funktion, deren Lesezugriffe schneller als linear wachsen."""
    return (
        f"{funktion.__name__} liest bei 25 Sprints {klein}-mal einen Wert aus erledigt, bei 100 Sprints "
        f"{gross}-mal, also etwa {gross / max(klein, 1):.0f}-mal so oft. Bei O(n) wären es etwa 4-mal so viele, "
        "bei O(n²) 16-mal.\n"
        "Tipp: Bilden Sie die Summe nicht für jeden Sprint neu (etwa mit sum(erledigt[:k])), sondern ziehen Sie in "
        "einer Schleife Sprint für Sprint die geschafften Punkte ab."
    )


# restpunkte liest jeden Sprint nur einmal: O(n), nicht O(n²)
klein = lesezugriffe(restpunkte, 25)
gross = lesezugriffe(restpunkte, 100)
assert klein is None or gross is None or gross <= 6 * klein + 10, laufzeit_meldung(restpunkte, klein, gross)

# fertig_nach liest jeden Sprint nur einmal: O(n), nicht O(n²)
klein = lesezugriffe(fertig_nach, 25)
gross = lesezugriffe(fertig_nach, 100)
assert klein is None or gross is None or gross <= 6 * klein + 10, laufzeit_meldung(fertig_nach, klein, gross)

# An der oberen Grenze: 100 Sprints bei restpunkte
erledigt = [nummer % 41 for nummer in range(100)]
gesamt = 1500
reste = restpunkte(gesamt, erledigt)
assert (len(reste), reste[0], reste[-1]) == (100, 1500, 0), (
    f"Bei 1500 Punkten und 100 Sprints mit 0, 1, …, 40, 0, 1, … Punkten liefert restpunkte {len(reste)} Werte "
    f"(erster {reste[0]}, letzter {reste[-1]}); erwartet waren 100 Werte (erster 1500, letzter 0)."
)

# An der oberen Grenze: 100 Sprints bei fertig_nach
ergebnis = fertig_nach(gesamt, erledigt)
ergebnis_zehn = fertig_nach(gesamt, erledigt[:10])
assert (ergebnis, ergebnis_zehn) == (79, -1), (
    f"Bei 1500 Punkten und 100 Sprints mit 0, 1, …, 40, 0, 1, … Punkten liefert fertig_nach {ergebnis!r}, "
    f"mit nur den ersten 10 Sprints {ergebnis_zehn!r}; erwartet waren 79 und -1."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[10, 0, 0]\n3 2 -1 0"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
