# Automatisch erzeugt aus lehrkraft/muster/3_035_anschaffungen.py - nicht von Hand ändern.
# vorlage-hash: 9fff3da23b433576
# text-hash: 6c5aded69eb0021d
# thema: algorithmen
# inhalt: Backtracking: Teilmengen

def geordnet(auswahlen):
    """Bringt eine Liste von Auswahlen in eine feste Reihenfolge, damit die Reihenfolge egal ist."""
    return sorted(tuple(auswahl) for auswahl in auswahlen)


def teilmengen_von_hand(namen):
    """Vergleichslösung ohne Rekursion: Bit k der Zahl maske entscheidet über namen[k]."""
    ergebnis = []
    for maske in range(2 ** len(namen)):
        ergebnis.append([namen[k] for k in range(len(namen)) if maske >> k & 1])
    return ergebnis


def budget_von_hand(angebote, budget):
    """Vergleichslösung: alle Teilmengen bilden und die zu teuren aussortieren."""
    ergebnis = []
    for maske in range(2 ** len(angebote)):
        teil = [angebote[k] for k in range(len(angebote)) if maske >> k & 1]
        if sum(preis for _, preis in teil) <= budget:
            ergebnis.append([name for name, _ in teil])
    return ergebnis


def ist_liste_von_listen(ergebnis):
    """Prüft, ob ergebnis eine Liste ist, deren Elemente Listen sind."""
    return isinstance(ergebnis, list) and all(isinstance(auswahl, list) for auswahl in ergebnis)


def meldung(aufruf, ergebnis, erwartet):
    """Beschreibt, welche Auswahlen fehlen oder zu viel sind."""
    if not ist_liste_von_listen(ergebnis):
        return f"{aufruf} ergibt {ergebnis!r}, erwartet war eine Liste von Listen."
    bekommen = geordnet(ergebnis)
    soll = geordnet(erwartet)
    fehlend = [list(a) for a in soll if a not in bekommen][:5]
    zu_viel = [list(a) for a in bekommen if a not in soll][:5]
    text = f"{aufruf} ergibt {len(ergebnis)} Auswahlen, erwartet waren {len(erwartet)}."
    if fehlend:
        text += f"\nEs fehlen zum Beispiel: {fehlend}"
    if zu_viel:
        text += f"\nZu viel oder falsch geordnet sind zum Beispiel: {zu_viel}"
    if len(bekommen) != len(set(bekommen)):
        text += "\nManche Auswahlen kommen doppelt vor."
    if ergebnis and len(set(map(id, ergebnis))) < len(ergebnis):
        text += (
            "\nTipp: Mehrere Einträge sind dieselbe Liste. Speichern Sie mit auswahl[:] eine Kopie, "
            "denn auswahl ändert sich danach weiter."
        )
    return text


ANGEBOTE = [("Firewall", 1200), ("Switch", 800), ("Schulung", 600), ("USV", 450)]

# alle_auswahlen mit zwei Namen
ergebnis = alle_auswahlen(["Firewall", "Switch"])
erwartet = [[], ["Firewall"], ["Switch"], ["Firewall", "Switch"]]
assert ist_liste_von_listen(ergebnis) and geordnet(ergebnis) == geordnet(erwartet), (
    meldung('alle_auswahlen(["Firewall", "Switch"])', ergebnis, erwartet)
)

# alle_auswahlen mit drei anderen Namen (nicht fest hinschreiben!)
namen = ["USV", "Router", "Lizenz"]
ergebnis = alle_auswahlen(namen)
erwartet = teilmengen_von_hand(namen)
assert ist_liste_von_listen(ergebnis) and geordnet(ergebnis) == geordnet(erwartet), (
    meldung(f"alle_auswahlen({namen})", ergebnis, erwartet)
)

# alle_auswahlen behält die Reihenfolge innerhalb einer Auswahl
ergebnis = alle_auswahlen(["b", "a"])
assert ist_liste_von_listen(ergebnis) and ["b", "a"] in ergebnis and ["a", "b"] not in ergebnis, (
    f'alle_auswahlen(["b", "a"]) ergibt {ergebnis!r}; erwartet war die Auswahl ["b", "a"] '
    "in der Reihenfolge der Eingabe, nicht sortiert."
)

# alle_auswahlen einer leeren Liste: nur die leere Auswahl
ergebnis = alle_auswahlen([])
assert ergebnis == [[]], (
    f"alle_auswahlen([]) ergibt {ergebnis!r}, erwartet war [[]]: genau eine Auswahl, die leere.\n"
    "Tipp: Ist nichts mehr zu entscheiden, ist die bisherige Auswahl fertig und wird gespeichert."
)

# alle_auswahlen mit einem Namen
ergebnis = alle_auswahlen(["Switch"])
assert ist_liste_von_listen(ergebnis) and geordnet(ergebnis) == [(), ("Switch",)], (
    meldung('alle_auswahlen(["Switch"])', ergebnis, [[], ["Switch"]])
)

# alle_auswahlen verändert die Liste nicht
namen = ["A", "B", "C"]
alle_auswahlen(namen)
assert namen == ["A", "B", "C"], f'Nach alle_auswahlen(["A", "B", "C"]) ist die Liste {namen!r}, erwartet war sie unverändert.'

# im_budget aus dem Beispiel
ergebnis = im_budget(ANGEBOTE, 2000)
erwartet = budget_von_hand(ANGEBOTE, 2000)
assert ist_liste_von_listen(ergebnis) and geordnet(ergebnis) == geordnet(erwartet), (
    meldung("im_budget(angebote, 2000)", ergebnis, erwartet)
)

# im_budget mit einem anderen Budget
ergebnis = im_budget(ANGEBOTE, 1100)
erwartet = budget_von_hand(ANGEBOTE, 1100)
assert ist_liste_von_listen(ergebnis) and geordnet(ergebnis) == geordnet(erwartet), (
    meldung("im_budget(angebote, 1100)", ergebnis, erwartet)
)

# Genau das Budget auszugeben ist erlaubt
ergebnis = im_budget([("Switch", 800), ("USV", 450)], 1250)
assert ist_liste_von_listen(ergebnis) and ["Switch", "USV"] in ergebnis, (
    meldung('im_budget([("Switch", 800), ("USV", 450)], 1250)', ergebnis, [[], ["Switch"], ["USV"], ["Switch", "USV"]])
    + "\nTipp: Eine Auswahl, die das Budget genau ausschöpft, passt noch (preis <= rest)."
)

# Alles passt ins Budget
ergebnis = im_budget(ANGEBOTE, 10**7)
erwartet = teilmengen_von_hand(["Firewall", "Switch", "Schulung", "USV"])
assert ist_liste_von_listen(ergebnis) and geordnet(ergebnis) == geordnet(erwartet), (
    meldung("im_budget(angebote, 10**7)", ergebnis, erwartet)
)

# Budget 0: nur die leere Auswahl
ergebnis = im_budget(ANGEBOTE, 0)
assert ergebnis == [[]], f"im_budget(angebote, 0) ergibt {ergebnis!r}, erwartet war [[]]."

# Keine Angebote: nur die leere Auswahl
ergebnis = im_budget([], 500)
assert ergebnis == [[]], f"im_budget([], 500) ergibt {ergebnis!r}, erwartet war [[]]."

# im_budget verändert die Angebote nicht
angebote_kopie = list(ANGEBOTE)
im_budget(angebote_kopie, 2000)
assert angebote_kopie == ANGEBOTE, f"Nach im_budget(angebote, 2000) ist angebote {angebote_kopie!r}, erwartet war sie unverändert."

# 200 zufällige Namenslisten für alle_auswahlen
zufall = Zufall(3035)
for _ in range(200):
    namen = zufall.sample(["A", "B", "C", "D", "E", "F", "G"], zufall.randint(0, 6))
    ergebnis = alle_auswahlen(namen)
    erwartet = teilmengen_von_hand(namen)
    assert ist_liste_von_listen(ergebnis) and geordnet(ergebnis) == geordnet(erwartet), (
        meldung(f"alle_auswahlen({namen})", ergebnis, erwartet)
    )

# 200 zufällige Angebote für im_budget
for _ in range(200):
    namen = zufall.sample(["A", "B", "C", "D", "E", "F", "G", "H"], zufall.randint(0, 7))
    angebote = [(name, zufall.randint(1, 1000)) for name in namen]
    budget = zufall.randint(0, 3000)
    ergebnis = im_budget(angebote, budget)
    erwartet = budget_von_hand(angebote, budget)
    assert ist_liste_von_listen(ergebnis) and geordnet(ergebnis) == geordnet(erwartet), (
        meldung(f"im_budget({angebote}, {budget})", ergebnis, erwartet)
    )

# Obere Grenze: alle_auswahlen mit 15 Namen
namen = [f"Posten{nummer}" for nummer in range(15)]
ergebnis = alle_auswahlen(namen)
assert ist_liste_von_listen(ergebnis) and len(ergebnis) == 2**15 and len(set(map(tuple, ergebnis))) == 2**15, (
    f"alle_auswahlen mit 15 Namen ergibt {len(ergebnis)} verschiedene Auswahlen, erwartet waren 2**15 = 32768."
)

# Zu teure Angebote werden gar nicht erst ausprobiert
teuer = [(f"Server{nummer}", 5000) for nummer in range(14)]
ergebnis, schritte = zaehle_schritte(im_budget, teuer, 4999)
assert ergebnis == [[]] and schritte <= 2000, (
    f"im_budget mit 14 Angeboten zu je 5000 Euro und Budget 4999 ergibt {ergebnis!r} nach {schritte} Schritten; "
    "erwartet war [[]] nach höchstens 2000 Schritten.\nTipp: Passt ein Angebot nicht mehr ins restliche Budget, "
    "nehmen Sie es gar nicht erst in die Auswahl auf, statt erst alle 16384 Auswahlen zu bilden."
)

# Obere Grenze: 20 Angebote, höchstens drei passen zusammen ins Budget
angebote = [(f"Lizenz{nummer}", 1000 + nummer) for nummer in range(20)]
ergebnis = im_budget(angebote, 3100)
erwartet_anzahl = 1 + 20 + 190 + sum(
    1 for a in range(20) for b in range(a + 1, 20) for c in range(b + 1, 20) if 3000 + a + b + c <= 3100
)
assert ist_liste_von_listen(ergebnis) and len(ergebnis) == erwartet_anzahl, (
    f"im_budget mit 20 Angeboten von 1000 bis 1019 Euro und Budget 3100 ergibt {len(ergebnis)} Auswahlen, "
    f"erwartet waren {erwartet_anzahl}."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("16\n12"), f"Erwartete Ausgabe:\n16\n12\nIhr Programm:\n{AUSGABE}"
