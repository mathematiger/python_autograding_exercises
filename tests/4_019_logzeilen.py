# Automatisch erzeugt aus lehrkraft/muster/4_019_logzeilen.py - nicht von Hand ändern.
# vorlage-hash: 61cacfa2cc9cdb9a
# text-hash: 0c184e2b4f4c0a7d
# thema: funktionen
# inhalt: Entpacken mit *rest

import ast
import inspect
import textwrap


def baum_von(funktion):
    """Gibt den Syntaxbaum einer Funktion zurück, None bei Problemen."""
    try:
        return ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return None


def mit_stern(funktion):
    """True, wenn die Funktion in einer Zuweisung einen Sternausdruck (*rest) benutzt."""
    baum = baum_von(funktion)
    if baum is None:
        return False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Assign):
            for ziel in knoten.targets:
                for teil in ast.walk(ziel):
                    if isinstance(teil, ast.Starred):
                        return True
    return False


def mit_verschachteltem_for(funktion):
    """True, wenn im Kopf einer for-Schleife ein Tupel in einem Tupel ausgepackt wird."""
    baum = baum_von(funktion)
    if baum is None:
        return False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.For) and isinstance(knoten.target, ast.Tuple):
            for teil in knoten.target.elts:
                if isinstance(teil, ast.Tuple):
                    return True
    return False


# zerlege aus dem Beispiel
ergebnis = zerlege("2026-11-03 04:12:07 web01 ERROR upstream timed out")
assert ergebnis == ("web01", "ERROR", "upstream timed out"), (
    f'zerlege("2026-11-03 04:12:07 web01 ERROR upstream timed out") ergibt {ergebnis!r}, '
    "erwartet war ('web01', 'ERROR', 'upstream timed out').\n"
    "Tipp: _, _, rechner, stufe, *woerter = zeile.split() und dann die Wörter mit \" \".join(...) verbinden."
)

# Zeile ohne Meldung
try:
    ergebnis = zerlege("2026-11-03 04:13:00 web01 WARN")
except (ValueError, IndexError) as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == ("web01", "WARN", ""), (
    f'zerlege("2026-11-03 04:13:00 web01 WARN") ergibt {ergebnis!r}, erwartet war (\'web01\', \'WARN\', \'\').\n'
    "Tipp: Der Sternausdruck *woerter bekommt dann die leere Liste, und \" \".join([]) ist der leere Text."
)

# Meldungen mit einem und mit vielen Wörtern (nicht fest hinschreiben!)
for zeile, erwartet in [
    ("2026-11-03 04:12:09 db02 INFO backup", ("db02", "INFO", "backup")),
    ("2026-01-01 00:00:00 a DEBUG " + " ".join(["x"] * 100), ("a", "DEBUG", " ".join(["x"] * 100))),
    ("2026-12-31 23:59:59 fw-03 CRITICAL Temperatur 81 Grad", ("fw-03", "CRITICAL", "Temperatur 81 Grad")),
]:
    ergebnis = zerlege(zeile)
    assert ergebnis == erwartet, f"zerlege({zeile[:60]!r}…) ergibt {str(ergebnis)[:120]}, erwartet war {str(erwartet)[:120]}."

# verlauf aus dem Beispiel
ergebnis = verlauf([("04:00", 31), ("04:05", 58), ("04:10", 47)])
assert ergebnis == ("04:00", "04:10", 16), (
    f'verlauf([("04:00", 31), ("04:05", 58), ("04:10", 47)]) ergibt {ergebnis!r}, erwartet war ("04:00", "04:10", 16).\n'
    "Tipp: Die Veränderung ist die letzte minus die erste Last, nicht das Maximum minus das Minimum."
)

# verlauf mit einer und mit zwei Messungen, Last kann sinken
for messreihe, erwartet in [
    ([("09:00", 42)], ("09:00", "09:00", 0)),
    ([("09:00", 100), ("09:05", 0)], ("09:00", "09:05", -100)),
    ([("23:55", 0), ("00:00", 100)], ("23:55", "00:00", 100)),
]:
    try:
        ergebnis = verlauf(messreihe)
    except (ValueError, IndexError) as fehler:
        ergebnis = f"{type(fehler).__name__}: {fehler}"
    assert ergebnis == erwartet, (
        f"verlauf({messreihe}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: erste, *_, letzte = messreihe braucht mindestens zwei Werte; bei nur einer Messung ist sie erste und letzte zugleich."
    )

# ausfallzeit aus dem Beispiel, Reihenfolge des ersten Auftretens
ergebnis = ausfallzeit([("web01", (120, 135)), ("db02", (300, 302)), ("web01", (600, 610))])
assert ergebnis == {"web01": 25, "db02": 2} and list(ergebnis) == ["web01", "db02"], (
    f"ausfallzeit aus dem Beispiel ergibt {ergebnis!r}, erwartet war {{'web01': 25, 'db02': 2}} in dieser Reihenfolge.\n"
    "Tipp: Mit for rechner, (von, bis) in ausfaelle bekommen Sie alle drei Werte direkt."
)

# Ränder von ausfallzeit: keine Ausfälle, Ausfall von 0 Minuten, der ganze Tag
ergebnis = (ausfallzeit([]), ausfallzeit([("a", (5, 5))]), ausfallzeit([("a", (0, 1440)), ("b", (0, 0))]))
assert ergebnis == ({}, {"a": 0}, {"a": 1440, "b": 0}), (
    f"ausfallzeit([]), ausfallzeit([('a', (5, 5))]) und ausfallzeit([('a', (0, 1440)), ('b', (0, 0))]) ergeben {ergebnis!r}; "
    "erwartet waren {}, {'a': 0} und {'a': 1440, 'b': 0}.\nTipp: Auch ein Rechner mit 0 Minuten steht im Ergebnis."
)

# Die übergebenen Listen bleiben unverändert
messreihe = [("04:00", 31), ("04:05", 58)]
ausfaelle = [("web01", (1, 2))]
verlauf(messreihe)
ausfallzeit(ausfaelle)
assert messreihe == [("04:00", 31), ("04:05", 58)] and ausfaelle == [("web01", (1, 2))], (
    f"Nach den Aufrufen sind messreihe {messreihe!r} und ausfaelle {ausfaelle!r}; beide sollen unverändert bleiben."
)

# Entpacken wird benutzt
ergebnis = (mit_stern(zerlege), mit_stern(verlauf), mit_verschachteltem_for(ausfallzeit))
assert ergebnis == (True, True, True), (
    "zerlege und verlauf sollen in einer Zuweisung einen Sternausdruck benutzen (… *rest = …), ausfallzeit "
    "verschachteltes Entpacken im Schleifenkopf (for rechner, (von, bis) in …); gefunden: "
    f"zerlege {'ja' if ergebnis[0] else 'nein'}, verlauf {'ja' if ergebnis[1] else 'nein'}, "
    f"ausfallzeit {'ja' if ergebnis[2] else 'nein'}."
)


# Vergleichslösungen mit Indizes
def zerlege_von_hand(zeile):
    """Zerlegt die Zeile über die Positionen der Leerzeichen."""
    teile = zeile.split(" ")
    return teile[2], teile[3], " ".join(teile[4:])


def ausfallzeit_von_hand(ausfaelle):
    """Summiert die Minuten über Indizes."""
    summen = {}
    for eintrag in ausfaelle:
        if eintrag[0] not in summen:
            summen[eintrag[0]] = 0
        summen[eintrag[0]] += eintrag[1][1] - eintrag[1][0]
    return summen


# 300 zufällige Zeilen, Messreihen und Ausfalllisten
zufall = Zufall(4019)
WOERTER = ["disk", "voll", "timeout", "neu", "gestartet", "404", "ok"]
for _ in range(300):
    woerter = [zufall.choice(WOERTER) for _ in range(zufall.randint(0, 5))]
    zeile = " ".join(["2026-11-03", "04:00:00", zufall.choice(["web01", "db2", "x"]), zufall.choice(["INFO", "ERROR"])] + woerter)
    ergebnis = zerlege(zeile)
    assert ergebnis == zerlege_von_hand(zeile), f"zerlege({zeile!r}) ergibt {ergebnis!r}, erwartet war {zerlege_von_hand(zeile)!r}."
    messreihe = [(f"{nummer:02d}:00", zufall.randint(0, 100)) for nummer in range(zufall.randint(1, 6))]
    erwartet = (messreihe[0][0], messreihe[-1][0], messreihe[-1][1] - messreihe[0][1])
    ergebnis = verlauf(messreihe)
    assert ergebnis == erwartet, f"verlauf({messreihe}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    ausfaelle = []
    for _ in range(zufall.randint(0, 6)):
        von = zufall.randint(0, 1440)
        ausfaelle.append((zufall.choice(["web01", "db2", "x"]), (von, zufall.randint(von, 1440))))
    ergebnis = ausfallzeit(ausfaelle)
    erwartet = ausfallzeit_von_hand(ausfaelle)
    assert ergebnis == erwartet and list(ergebnis) == list(erwartet), (
        f"ausfallzeit({ausfaelle}) ergibt {ergebnis!r}, erwartet war {erwartet!r} (in dieser Reihenfolge)."
    )

# An der oberen Grenze: 100 000 Messungen und 100 000 Ausfälle
messreihe = [(f"m{nummer}", nummer % 101) for nummer in range(100000)]
ausfaelle = [(f"srv{nummer % 500}", (nummer % 1000, nummer % 1000 + nummer % 441)) for nummer in range(100000)]
ergebnis = verlauf(messreihe)
summen = ausfallzeit(ausfaelle)
erwartet = ausfallzeit_von_hand(ausfaelle)
assert ergebnis == ("m0", "m99999", 99999 % 101) and summen == erwartet, (
    f"Bei 100 000 Messungen ergibt verlauf {ergebnis!r}, erwartet war ('m0', 'm99999', {99999 % 101}); "
    f"ausfallzeit liefert {len(summen)} Rechner, srv0 mit {summen.get('srv0')!r} Minuten "
    f"(erwartet {len(erwartet)} Rechner, srv0 mit {erwartet['srv0']} Minuten)."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "('web01', 'ERROR', 'upstream timed out')\n('web01', 'WARN', '')\n('04:00', '04:10', 16)\n{'web01': 25, 'db02': 2}"
)
# Ein defaultdict oder Counter druckt sich mit seinem Typnamen davor; das ist ebenso richtig.
zeilen = AUSGABE.split("\n")
assert zeilen[:3] == erwartete_ausgabe.split("\n")[:3] and len(zeilen) == 4 and "{'web01': 25, 'db02': 2}" in zeilen[3], (
    f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
)
