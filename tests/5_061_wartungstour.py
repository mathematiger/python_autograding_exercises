# Automatisch erzeugt aus lehrkraft/muster/5_061_wartungstour.py - nicht von Hand ändern.
# vorlage-hash: 42acc41ec729c1b8
# text-hash: b66c1f86dbeccbdf
# thema: algorithmen
# inhalt: Bitmasken-DP, beste Reihenfolge

import ast
import inspect
from itertools import permutations

FAHRZEIT = [
    [0, 42, 12, 20, 35],
    [40, 0, 40, 30, 12],
    [12, 40, 0, 15, 25],
    [22, 30, 15, 0, 34],
    [35, 14, 25, 34, 0],
]


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def dauer_von(fahrzeit, reihenfolge):
    """Vergleichslösung für tourdauer: Summe über die Indizes."""
    orte = [0] + list(reihenfolge) + [0]
    return sum(fahrzeit[orte[i]][orte[i + 1]] for i in range(len(orte) - 1))


def alle_touren(fahrzeit):
    """Vergleichslösung: probiert alle Reihenfolgen durch; liefert (kürzeste Dauer, Menge der besten Reihenfolgen)."""
    n = len(fahrzeit) - 1
    dauern = {reihenfolge: dauer_von(fahrzeit, reihenfolge) for reihenfolge in permutations(range(1, n + 1))}
    kuerzeste = min(dauern.values())
    return kuerzeste, {reihenfolge for reihenfolge, dauer in dauern.items() if dauer == kuerzeste}


def tabelle_von(fahrzeit):
    """Vergleichslösung für bestzeiten: zu jeder Teilmenge und jedem letzten Standort alle Reihenfolgen."""
    n = len(fahrzeit) - 1
    tabelle = {}
    for reihenfolge_laenge in range(1, n + 1):
        for teil in permutations(range(1, n + 1), reihenfolge_laenge):
            maske = sum(2 ** (k - 1) for k in teil)
            dauer = dauer_von(fahrzeit, teil) - fahrzeit[teil[-1]][0]
            schluessel = (maske, teil[-1])
            tabelle[schluessel] = min(dauer, tabelle.get(schluessel, dauer))
    return tabelle


def ist_reihenfolge(ergebnis, n):
    """Prüft, ob ergebnis eine Liste ist, die jeden Standort 1 bis n genau einmal enthält."""
    return isinstance(ergebnis, list) and sorted(ergebnis) == list(range(1, n + 1))


def zufallsmatrix(zufall, n, hoechstens=1000):
    """Eine zufällige, nicht symmetrische Fahrzeitmatrix für n Standorte."""
    return [[0 if i == j else zufall.randint(0, hoechstens) for j in range(n + 1)] for i in range(n + 1)]


def versteckte_tour(zufall, n):
    """Eine Matrix, in der genau eine Tour aus lauter Fahrten von 1 Minute besteht; liefert (matrix, tour)."""
    matrix = [[0 if i == j else zufall.randint(100, 1000) for j in range(n + 1)] for i in range(n + 1)]
    tour = list(range(1, n + 1))
    zufall.shuffle(tour)
    orte = [0, *tour, 0]
    for von, nach in zip(orte, orte[1:]):
        matrix[von][nach] = 1
    return matrix, tour


def benutzt_bitoperatoren():
    """Prüft im Quelltext aller Funktionen des Programms, ob & und << (oder >>) vorkommen."""
    datei = bestzeiten.__code__.co_filename
    gefunden = set()
    for wert in list(globals().values()):
        if not inspect.isfunction(wert) or wert.__code__.co_filename != datei:
            continue
        try:
            baum = ast.parse(inspect.getsource(wert).strip())
        except (OSError, TypeError, SyntaxError):
            continue
        for knoten in ast.walk(baum):
            if isinstance(knoten, (ast.BinOp, ast.AugAssign)):
                gefunden.add(type(knoten.op).__name__)
    return "BitAnd" in gefunden and ("LShift" in gefunden or "RShift" in gefunden)


# tourdauer: das Beispiel
ergebnis, fehler = rufe(lambda: tourdauer(FAHRZEIT, [1, 2, 3, 4]))
assert ergebnis == 166, (
    f"tourdauer(fahrzeit, [1, 2, 3, 4]) ergibt {ergebnis!r}, erwartet war 166 (42 + 40 + 15 + 34 + 35)."
    + ("\nTipp: Die Rückfahrt zur Zentrale (35 Minuten) gehört dazu." if ergebnis == 131 else "")
    + ("\nTipp: Die Fahrt von der Zentrale zum ersten Standort (42 Minuten) gehört dazu." if ergebnis == 124 else "")
    + absturz(fehler)
)

# tourdauer: eine andere Reihenfolge
ergebnis, fehler = rufe(lambda: tourdauer(FAHRZEIT, [3, 1, 4, 2]))
assert ergebnis == 99, f"tourdauer(fahrzeit, [3, 1, 4, 2]) ergibt {ergebnis!r}, erwartet war 99 (20 + 30 + 12 + 25 + 12)." + absturz(fehler)

# tourdauer: die Richtung zählt (fahrzeit[i][j] ist die Fahrt von i nach j)
ergebnis, fehler = rufe(lambda: tourdauer(FAHRZEIT, [2, 4, 1, 3]))
assert ergebnis == 103, (
    f"tourdauer(fahrzeit, [2, 4, 1, 3]) ergibt {ergebnis!r}, erwartet war 103 (12 + 25 + 14 + 30 + 22); "
    "das ist [3, 1, 4, 2] rückwärts, aber die Fahrzeiten hin und zurück sind verschieden."
    + ("\nTipp: fahrzeit[von][nach], nicht fahrzeit[nach][von]." if ergebnis == 99 else "")
    + absturz(fehler)
)

# tourdauer: nur ein Teil der Standorte
ergebnis, fehler = rufe(lambda: tourdauer(FAHRZEIT, [4]))
assert ergebnis == 70, f"tourdauer(fahrzeit, [4]) ergibt {ergebnis!r}, erwartet war 70 (35 hin, 35 zurück)." + absturz(fehler)

# tourdauer: keine Standorte
ergebnis, fehler = rufe(lambda: (tourdauer(FAHRZEIT, []), tourdauer([[0]], [])))
assert ergebnis == (0, 0), f"tourdauer(fahrzeit, []) und tourdauer([[0]], []) ergeben {ergebnis!r}, erwartet war (0, 0)." + absturz(fehler)

# bestzeiten: zwei Einträge aus dem Beispiel
ergebnis, fehler = rufe(lambda: bestzeiten(FAHRZEIT))
teil = None if not isinstance(ergebnis, dict) else (ergebnis.get((0b0101, 3)), ergebnis.get((0b0101, 1)))
assert teil == (72, 50), (
    f"bestzeiten(fahrzeit) hat unter (0b0101, 3) und (0b0101, 1) die Werte {teil!r}, erwartet war (72, 50): "
    "0b0101 ist die Menge {1, 3}; 0 → 1 → 3 dauert 42 + 30 = 72, 0 → 3 → 1 dauert 20 + 30 = 50."
    + ("\nTipp: Standort k ist das Bit 1 << (k - 1), Standort 1 also das niedrigste Bit." if ergebnis and (0b1010, 3) in ergebnis and (0b0101, 3) not in ergebnis else "")
    + absturz(fehler)
)

# bestzeiten: ein einzelner Standort ist die direkte Fahrt von der Zentrale
ergebnis, fehler = rufe(lambda: bestzeiten(FAHRZEIT))
einzeln = None if not isinstance(ergebnis, dict) else [ergebnis.get((1 << (k - 1), k)) for k in range(1, 5)]
assert einzeln == [42, 12, 20, 35], (
    f"bestzeiten(fahrzeit) hat für die Masken mit einem Standort ((1, 1), (2, 2), (4, 3), (8, 4)) die Werte "
    f"{einzeln!r}, erwartet war [42, 12, 20, 35]: die Fahrt von der Zentrale direkt dorthin." + absturz(fehler)
)

# bestzeiten: genau die Schlüssel mit maske ≠ 0 und letzter in maske
ergebnis, fehler = rufe(lambda: bestzeiten(FAHRZEIT))
erwartet = set(tabelle_von(FAHRZEIT))
schluessel = set(ergebnis) if isinstance(ergebnis, dict) else None
assert schluessel == erwartet, (
    (f"bestzeiten(fahrzeit) hat {len(schluessel)} Schlüssel" if schluessel is not None else f"bestzeiten(fahrzeit) ergibt {ergebnis!r}")
    + f", erwartet war ein Dictionary mit den {len(erwartet)} Schlüsseln (maske, letzter) mit maske von 1 bis 15 und "
    "letzter in maske."
    + (f"\nZu viel: {sorted(schluessel - erwartet)[:5]}" if schluessel and schluessel - erwartet else "")
    + (f"\nEs fehlen: {sorted(erwartet - schluessel)[:5]}" if schluessel is not None and erwartet - schluessel else "")
    + absturz(fehler)
)

# bestzeiten: die ganze Tabelle für das Beispiel
ergebnis, fehler = rufe(lambda: bestzeiten(FAHRZEIT))
erwartet = tabelle_von(FAHRZEIT)
falsch = sorted(s for s in erwartet if ergebnis.get(s) != erwartet[s]) if isinstance(ergebnis, dict) else []
assert isinstance(ergebnis, dict) and not falsch, (
    (f"bestzeiten(fahrzeit) ist unter {falsch[0]} falsch: erwartet {erwartet[falsch[0]]}, bekommen "
     f"{ergebnis.get(falsch[0])!r}." if falsch else f"bestzeiten(fahrzeit) ergibt {ergebnis!r}, erwartet war ein Dictionary.")
    + "\nTipp: beste[(maske, k)] ist das Minimum über alle j in maske ohne k von beste[(maske ^ bit_k, j)] + fahrzeit[j][k]."
    + absturz(fehler)
)

# bestzeiten: keine Standorte
ergebnis, fehler = rufe(lambda: bestzeiten([[0]]))
assert ergebnis == {}, f"bestzeiten([[0]]) ergibt {ergebnis!r}, erwartet war {{}}: ohne Standorte gibt es kein Teilproblem." + absturz(fehler)

# kuerzeste_tour: das Beispiel
ergebnis, fehler = rufe(lambda: kuerzeste_tour(FAHRZEIT))
assert ergebnis == 99, (
    f"kuerzeste_tour(fahrzeit) ergibt {ergebnis!r}, erwartet war 99 (Reihenfolge 3, 1, 4, 2)."
    + ("\nTipp: Zum Wert aus bestzeiten kommt noch die Rückfahrt fahrzeit[letzter][0]." if ergebnis == 87 else "")
    + absturz(fehler)
)

# kuerzeste_tour: eine zweite Matrix, in der der Umweg kürzer ist als die direkte Fahrt
umweg = [
    [0, 5, 100, 100],
    [100, 0, 5, 100],
    [100, 100, 0, 5],
    [5, 100, 100, 0],
]
ergebnis, fehler = rufe(lambda: kuerzeste_tour(umweg))
assert ergebnis == 20, f"kuerzeste_tour({umweg}) ergibt {ergebnis!r}, erwartet war 20 (0 → 1 → 2 → 3 → 0, je 5 Minuten)." + absturz(fehler)

# kuerzeste_tour: ein einzelner Standort
ergebnis, fehler = rufe(lambda: kuerzeste_tour([[0, 7], [9, 0]]))
assert ergebnis == 16, (
    f"kuerzeste_tour([[0, 7], [9, 0]]) ergibt {ergebnis!r}, erwartet war 16: 7 hin und 9 zurück." + absturz(fehler)
)

# kuerzeste_tour: gar kein Standort
ergebnis, fehler = rufe(lambda: kuerzeste_tour([[0]]))
assert ergebnis == 0, (
    f"kuerzeste_tour([[0]]) ergibt {ergebnis!r}, erwartet war 0: Ohne Standorte bleibt die Technikerin in der "
    "Zentrale." + absturz(fehler)
)

# kuerzeste_tour: Fahrzeiten 0 (Kunden im selben Gebäude) zählen wie jede andere Dauer
null = [[0, 0, 5], [5, 0, 0], [0, 5, 0]]
ergebnis, fehler = rufe(lambda: kuerzeste_tour(null))
assert ergebnis == 0, (
    f"kuerzeste_tour({null}) ergibt {ergebnis!r}, erwartet war 0 (0 → 1 → 2 → 0, jede Fahrt 0 Minuten)."
    + ("\nTipp: Eine Dauer von 0 ist ein gültiger Wert; prüfen Sie mit is None statt mit if not." if ergebnis == 15 else "")
    + absturz(fehler)
)

# beste_reihenfolge: das Beispiel
ergebnis, fehler = rufe(lambda: beste_reihenfolge(FAHRZEIT))
assert ergebnis == [3, 1, 4, 2], (
    f"beste_reihenfolge(fahrzeit) ergibt {ergebnis!r}, erwartet war [3, 1, 4, 2] (99 Minuten)."
    + (f"\nIhre Reihenfolge dauert {dauer_von(FAHRZEIT, ergebnis)} Minuten." if ist_reihenfolge(ergebnis, 4) else "")
    + ("\nTipp: Beim Rückwärtsablesen kommt der letzte Standort zuerst; drehen Sie die Liste am Ende um." if ergebnis == [2, 4, 1, 3] else "")
    + absturz(fehler)
)

# beste_reihenfolge: ein einzelner Standort
ergebnis, fehler = rufe(lambda: beste_reihenfolge([[0, 7], [9, 0]]))
assert ergebnis == [1], f"beste_reihenfolge([[0, 7], [9, 0]]) ergibt {ergebnis!r}, erwartet war [1]." + absturz(fehler)

# beste_reihenfolge: gar kein Standort
ergebnis, fehler = rufe(lambda: beste_reihenfolge([[0]]))
assert ergebnis == [], f"beste_reihenfolge([[0]]) ergibt {ergebnis!r}, erwartet war []." + absturz(fehler)

# beste_reihenfolge: bei mehreren besten Reihenfolgen ist jede richtig
gleich = [[0, 10, 10, 10], [10, 0, 10, 10], [10, 10, 0, 10], [10, 10, 10, 0]]
ergebnis, fehler = rufe(lambda: beste_reihenfolge(gleich))
assert ist_reihenfolge(ergebnis, 3), (
    f"beste_reihenfolge({gleich}) ergibt {ergebnis!r}, erwartet war eine Liste mit jedem der Standorte 1, 2, 3 genau "
    "einmal (hier sind alle Reihenfolgen gleich gut)." + absturz(fehler)
)

# Die Tabelle rechnet mit Bitmasken (&, <<)
assert benutzt_bitoperatoren(), (
    "In Ihrem Programm kommen die Bitoperatoren & und << nicht beide vor. Speichern Sie die Menge der besuchten "
    "Standorte als Bitmaske: 1 << (k - 1) ist Standort k, maske & bit prüft, ob er dabei ist (siehe Hintergrund)."
)

zufall = Zufall(5061)

# Viele zufällige Matrizen: die Tabelle im Vergleich mit allen Reihenfolgen
for _ in range(60):
    matrix = zufallsmatrix(zufall, zufall.randint(1, 5), zufall.choice([3, 50, 1000]))
    ergebnis, fehler = rufe(lambda: bestzeiten(matrix))
    erwartet = tabelle_von(matrix)
    assert ergebnis == erwartet, (
        f"bestzeiten({matrix}) ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}." + absturz(fehler)
    )

# Viele zufällige Matrizen: kürzeste Tour und beste Reihenfolge im Vergleich mit allen Reihenfolgen
for _ in range(150):
    n = zufall.randint(0, 6)
    matrix = zufallsmatrix(zufall, n, zufall.choice([3, 50, 1000]))
    kuerzeste, beste = alle_touren(matrix)
    ergebnis, fehler = rufe(lambda: (kuerzeste_tour(matrix), beste_reihenfolge(matrix)))
    zeit, reihenfolge = ergebnis if ergebnis else (None, None)
    gueltig = ist_reihenfolge(reihenfolge, n) and tuple(reihenfolge) in beste
    assert zeit == kuerzeste and gueltig, (
        f"Für fahrzeit = {matrix} ergeben kuerzeste_tour {zeit!r} und beste_reihenfolge {reihenfolge!r}"
        + (f" ({dauer_von(matrix, reihenfolge)} Minuten)" if ist_reihenfolge(reihenfolge, n) else "")
        + f"; erwartet war {kuerzeste} und eine Reihenfolge mit dieser Dauer, z. B. {list(min(beste))}." + absturz(fehler)
    )

# Laufzeit: O(2**n · n²) statt n! Reihenfolgen
klein = zufallsmatrix(zufall, 5)
gross = zufallsmatrix(zufall, 8)
_, schritte_klein = zaehle_schritte(kuerzeste_tour, klein)
ergebnis, schritte_gross = zaehle_schritte(kuerzeste_tour, gross)
assert ergebnis == alle_touren(gross)[0] and schritte_gross <= 40 * schritte_klein, (
    f"kuerzeste_tour braucht für 5 Standorte {schritte_klein} Schritte, für 8 Standorte {schritte_gross}, also das "
    f"{schritte_gross / max(schritte_klein, 1):.0f}-Fache; bei O(2**n · n²) wäre es etwa das 20-Fache, wer alle "
    "Reihenfolgen durchprobiert, braucht das 300- bis 500-Fache (8! = 40 320 gegen 5! = 120).\n"
    "Tipp: Füllen Sie die Tabelle bestzeiten und nehmen Sie daraus das Minimum (siehe Hintergrund)."
)

# Obere Grenze: kuerzeste_tour mit 15 Standorten
matrix, tour = versteckte_tour(zufall, 15)
ergebnis, fehler = rufe(lambda: kuerzeste_tour(matrix))
assert ergebnis == 16, (
    f"kuerzeste_tour mit 15 Standorten ergibt {ergebnis!r}; erwartet war 16: Die Tour {tour} besteht aus 16 Fahrten "
    "von je 1 Minute, alle anderen Fahrten dauern mindestens 100 Minuten." + absturz(fehler)
)

# Obere Grenze: beste_reihenfolge mit 15 Standorten
matrix, tour = versteckte_tour(zufall, 15)
ergebnis, fehler = rufe(lambda: beste_reihenfolge(matrix))
assert ergebnis == tour, (
    f"beste_reihenfolge mit 15 Standorten ergibt {ergebnis!r}; erwartet war {tour}, die einzige Tour aus lauter "
    "Fahrten von 1 Minute." + absturz(fehler)
)
