# Automatisch erzeugt aus lehrkraft/muster/3_034_speicherbaum.py - nicht von Hand ändern.
# vorlage-hash: 10113c862ba92c07
# text-hash: 062b1047bf05f63d
# thema: algorithmen
# inhalt: Rekursion auf Listen

def alle_eintraege(ordner):
    """Vergleichslösung ohne Rekursion: liefert (Datei-Summe, Tiefe) mit einem Stapel von (Ordner, Ebene)."""
    summe = 0
    tiefste = 0
    stapel = [(ordner, 1)]
    while stapel:
        aktuell, ebene = stapel.pop()
        tiefste = max(tiefste, ebene)
        for eintrag in aktuell:
            if isinstance(eintrag, list):
                stapel.append((eintrag, ebene + 1))
            else:
                summe += eintrag
    return summe, tiefste


def spiegel_von_hand(ordner):
    """Vergleichslösung: kehrt jeden Ordner mit Slicing um."""
    return [spiegel_von_hand(e) if isinstance(e, list) else e for e in ordner[::-1]]


def zaehle_selbstaufrufe(name, argument):
    """Ruft die Funktion name mit argument auf und zählt, wie oft sie dabei insgesamt aufgerufen wird."""
    original = globals()[name]
    aufrufe = []

    def spion(*argumente):
        """Merkt sich den Aufruf und ruft dann die echte Funktion auf."""
        aufrufe.append(1)
        return original(*argumente)

    globals()[name] = spion
    try:
        original(argument)
    finally:
        globals()[name] = original
    return len(aufrufe)


def zufallsordner(zufall, ebenen):
    """Baut einen zufälligen Ordner mit höchstens ebenen Ebenen."""
    inhalt = []
    for _ in range(zufall.randint(0, 4)):
        if ebenen > 1 and zufall.random() < 0.35:
            inhalt.append(zufallsordner(zufall, ebenen - 1))
        else:
            inhalt.append(zufall.randint(0, 1000))
    return inhalt


BEISPIEL = "[120, [30, 5, [700, 2]], [], [[15]]]"


def beispiel():
    """Baut das Laufwerk aus dem Beispiel neu."""
    return [120, [30, 5, [700, 2]], [], [[15]]]


# belegung eines Ordners ohne Unterordner
ergebnis = belegung([30, 5, 7])
assert ergebnis == 42, f"belegung([30, 5, 7]) ergibt {ergebnis!r}, erwartet war 42."

# belegung aus dem Beispiel, mit Unterordnern
ergebnis = belegung(beispiel())
assert ergebnis == 872, (
    f"belegung({BEISPIEL}) ergibt {ergebnis!r}, erwartet war 872.\n"
    "Tipp: Ist ein Eintrag eine Liste, addieren Sie belegung(eintrag), sonst den Eintrag selbst."
    + ("\nTipp: Die Dateien in tieferen Ordnern fehlen; rufen Sie belegung für jeden Unterordner auf." if ergebnis == 120 else "")
)

# belegung mit anderen Werten (nicht fest hinschreiben!)
ergebnis = belegung([[1, [2, [3, [4]]]], 10])
assert ergebnis == 20, f"belegung([[1, [2, [3, [4]]]], 10]) ergibt {ergebnis!r}, erwartet war 20."

# belegung eines leeren Ordners ist 0
ergebnis = belegung([])
assert ergebnis == 0, f"belegung([]) ergibt {ergebnis!r}, erwartet war 0."

# belegung mit nur leeren Ordnern ist 0
ergebnis = belegung([[], [[]], []])
assert ergebnis == 0, f"belegung([[], [[]], []]) ergibt {ergebnis!r}, erwartet war 0."

# belegung ruft sich selbst auf
anzahl = zaehle_selbstaufrufe("belegung", beispiel())
assert anzahl >= 5, (
    f"belegung({BEISPIEL}) hat sich {anzahl}-mal selbst aufgerufen; erwartet war ein Aufruf je Unterordner, also 5.\n"
    "Tipp: Lösen Sie die Aufgabe rekursiv: belegung(eintrag) für jeden Unterordner."
)

# tiefe aus dem Beispiel
ergebnis = tiefe(beispiel())
assert ergebnis == 3, (
    f"tiefe({BEISPIEL}) ergibt {ergebnis!r}, erwartet war 3 (Laufwerk, Ordner, Unterordner).\n"
    "Tipp: Die Tiefe ist 1 plus die größte Tiefe der Unterordner."
)

# tiefe mit anderer Verschachtelung
ergebnis = tiefe([[1, [2, [3, [4]]]], 10])
assert ergebnis == 5, f"tiefe([[1, [2, [3, [4]]]], 10]) ergibt {ergebnis!r}, erwartet war 5."

# tiefe zählt die tiefste Stelle, nicht die Summe
ergebnis = tiefe([[[1]], [[2]], [3]])
assert ergebnis == 3, (
    f"tiefe([[[1]], [[2]], [3]]) ergibt {ergebnis!r}, erwartet war 3.\n"
    "Tipp: Nehmen Sie das Maximum der Tiefen der Unterordner, nicht ihre Summe."
)

# tiefe eines Ordners ohne Unterordner ist 1
ergebnis = tiefe([5, 6])
assert ergebnis == 1, f"tiefe([5, 6]) ergibt {ergebnis!r}, erwartet war 1."

# tiefe eines leeren Ordners ist 1
ergebnis = tiefe([])
assert ergebnis == 1, f"tiefe([]) ergibt {ergebnis!r}, erwartet war 1 (ein leerer Ordner ist eine Ebene)."

# Auch leere Unterordner zählen als Ebene
ergebnis = tiefe([1, [[]]])
assert ergebnis == 3, f"tiefe([1, [[]]]) ergibt {ergebnis!r}, erwartet war 3."

# gespiegelt eines Ordners ohne Unterordner
ergebnis = gespiegelt([1, 2, 3])
assert ergebnis == [3, 2, 1], f"gespiegelt([1, 2, 3]) ergibt {ergebnis!r}, erwartet war [3, 2, 1]."

# gespiegelt aus dem Beispiel: auch die Unterordner sind umgedreht
ergebnis = gespiegelt(beispiel())
erwartet = [[[15]], [], [[2, 700], 5, 30], 120]
assert ergebnis == erwartet, (
    f"gespiegelt({BEISPIEL}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    + ("\nTipp: Auch jeder Unterordner muss umgedreht werden, rufen Sie gespiegelt für ihn auf."
       if ergebnis == beispiel()[::-1] else "")
)

# gespiegelt mit anderer Verschachtelung
ergebnis = gespiegelt([[1, [2, [3, 4]]], 10])
erwartet = [10, [[[4, 3], 2], 1]]
assert ergebnis == erwartet, f"gespiegelt([[1, [2, [3, 4]]], 10]) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# gespiegelt eines leeren Ordners
ergebnis = gespiegelt([])
assert ergebnis == [], f"gespiegelt([]) ergibt {ergebnis!r}, erwartet war []."

# gespiegelt verändert die übergebene Liste nicht
daten = beispiel()
gespiegelt(daten)
assert daten == beispiel(), (
    f"Nach gespiegelt(laufwerk) ist laufwerk {daten!r}, erwartet war unverändert {beispiel()!r}.\n"
    "Tipp: Bauen Sie eine neue Liste auf, statt mit reverse() die alte umzudrehen."
)

# gespiegelt liefert neue Listen, auch für die Unterordner
daten = [[1, 2], [3]]
ergebnis = gespiegelt(daten)
ergebnis[0].append(99)
assert daten == [[1, 2], [3]], (
    "Nach ergebnis = gespiegelt([[1, 2], [3]]) und ergebnis[0].append(99) hat sich das Original zu "
    f"{daten!r} verändert; erwartet war [[1, 2], [3]].\nTipp: Auch jeder Unterordner im Ergebnis soll eine neue Liste sein."
)

# Dateien der Größe 0 und 10**6
daten = [0, [10**6, [0]], 10**6]
ergebnis = (belegung(daten), tiefe(daten), gespiegelt(daten))
erwartet = (2 * 10**6, 3, [10**6, [[0], 10**6], 0])
assert ergebnis == erwartet, f"Für {daten} ergeben belegung, tiefe und gespiegelt {ergebnis!r}, erwartet war {erwartet!r}."

# 300 zufällige Laufwerke für belegung
zufall = Zufall(3034)
for _ in range(300):
    daten = zufallsordner(zufall, 6)
    ergebnis = belegung(daten)
    erwartet = alle_eintraege(daten)[0]
    assert ergebnis == erwartet, f"belegung({daten}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# 300 zufällige Laufwerke für tiefe
for _ in range(300):
    daten = zufallsordner(zufall, 6)
    ergebnis = tiefe(daten)
    erwartet = alle_eintraege(daten)[1]
    assert ergebnis == erwartet, f"tiefe({daten}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# 300 zufällige Laufwerke für gespiegelt
for _ in range(300):
    daten = zufallsordner(zufall, 6)
    vorher = repr(daten)
    ergebnis = gespiegelt(daten)
    erwartet = spiegel_von_hand(daten)
    assert ergebnis == erwartet, f"gespiegelt({daten}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    assert repr(daten) == vorher, f"gespiegelt hat das Laufwerk verändert: vorher {vorher}, nachher {daten!r}."

# Obere Grenze: 100 Ebenen tief
tief = [7]
for _ in range(99):
    tief = [1, tief]
ergebnis = (belegung(tief), tiefe(tief), alle_eintraege(gespiegelt(tief)))
erwartet = (106, 100, (106, 100))
assert ergebnis == erwartet, (
    "Für einen Ordner mit 100 Ebenen ergeben belegung, tiefe und (Summe, Tiefe) von gespiegelt "
    f"{ergebnis!r}, erwartet war {erwartet!r}."
)

# Obere Grenze: 10 000 Einträge, jeder nur einmal angesehen
breit = [[nummer % 1000 for nummer in range(start, start + 99)] for start in range(0, 9900, 99)]
schritte_gesamt = 0
for funktion in (belegung, tiefe, gespiegelt):
    ergebnis, schritte = zaehle_schritte(funktion, breit)
    schritte_gesamt += schritte
assert schritte_gesamt <= 150000, (
    f"belegung, tiefe und gespiegelt haben für 100 Ordner mit je 99 Dateien zusammen {schritte_gesamt} Schritte "
    "gebraucht; erwartet waren höchstens etwa 5 Schritte je Eintrag und Funktion (O(n)).\n"
    "Tipp: Gehen Sie jeden Ordner nur einmal durch."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "872\n3\n[[[15]], [], [[2, 700], 5, 30], 120]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
