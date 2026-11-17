# Automatisch erzeugt aus lehrkraft/muster/3_034_rackbaum.py - nicht von Hand ändern.
# vorlage-hash: 42810329a4b44f4e
# text-hash: 1a215d7f3cb63278
# thema: algorithmen
# inhalt: Rekursion auf Listen

def vergleich_gesamt(anlage):
    """Vergleichslösung ohne Rekursion: ein eigener Stapel noch offener Listen."""
    summe = 0
    offen = [anlage]
    while offen:
        for element in offen.pop():
            if isinstance(element, list):
                offen.append(element)
            else:
                summe += element
    return summe


def vergleich_tiefe(anlage):
    """Vergleichslösung ohne Rekursion: Ebene für Ebene nach unten gehen."""
    ebene = [anlage]
    stufen = 0
    while ebene:
        stufen += 1
        naechste = []
        for liste in ebene:
            naechste.extend(element for element in liste if isinstance(element, list))
        ebene = naechste
    return stufen


def vergleich_gespiegelt(anlage):
    """Vergleichslösung als Comprehension über reversed."""
    return [vergleich_gespiegelt(x) if isinstance(x, list) else x for x in reversed(anlage)]


def zufallsanlage(zufall, rest):
    """Erzeugt eine zufällige verschachtelte Liste mit höchstens rest weiteren Ebenen."""
    anlage = []
    for _ in range(zufall.randint(0, 4)):
        if rest > 0 and zufall.random() < 0.35:
            anlage.append(zufallsanlage(zufall, rest - 1))
        else:
            anlage.append(zufall.randint(0, 10**6))
    return anlage


def ruft_sich_selbst_auf(name, anlage):
    """Ersetzt die Funktion name kurz durch eine zählende Hülle; True, wenn sie mehr als einmal lief."""
    original = globals()[name]
    aufrufe = []

    def zaehlend(liste):
        """Zählt den Aufruf und reicht ihn an die echte Funktion weiter."""
        aufrufe.append(1)
        return original(liste)

    globals()[name] = zaehlend
    try:
        zaehlend(anlage)
    finally:
        globals()[name] = original
    return len(aufrufe) > 1


BEISPIEL = [[512, 256, [128, 128]], 1024]

# gesamt: das Beispiel aus der Aufgabe
ergebnis = gesamt([[512, 256, [128, 128]], 1024])
assert ergebnis == 2048, (
    f"gesamt([[512, 256, [128, 128]], 1024]) ergibt {ergebnis!r}, erwartet war 2048.\n"
    "Tipp: Ist ein Element eine Liste, rufen Sie gesamt(element) auf und addieren das Ergebnis."
)

# gesamt: eine Liste ohne innere Listen
ergebnis = gesamt([100, 200, 300])
assert ergebnis == 600, f"gesamt([100, 200, 300]) ergibt {ergebnis!r}, erwartet war 600."

# gesamt: eine andere verschachtelte Anlage (nicht fest hinschreiben!)
ergebnis = gesamt([[1, [2, [3]]], [4], 5])
assert ergebnis == 15, f"gesamt([[1, [2, [3]]], [4], 5]) ergibt {ergebnis!r}, erwartet war 15."

# gesamt: die leere Liste
ergebnis = gesamt([])
assert ergebnis == 0, f"gesamt([]) ergibt {ergebnis!r}, erwartet war 0 (ein leeres Rack hat keinen Speicher)."

# gesamt: leere innere Listen und Server mit 0 GB
ergebnis = gesamt([[], [[], 0], [[]]])
assert ergebnis == 0, f"gesamt([[], [[], 0], [[]]]) ergibt {ergebnis!r}, erwartet war 0."

# gesamt ruft sich selbst auf
assert ruft_sich_selbst_auf("gesamt", [[1], [2]]), (
    "gesamt([[1], [2]]) hat sich nicht selbst aufgerufen. Lösen Sie die Aufgabe rekursiv: "
    "Für eine innere Liste rufen Sie gesamt(element) auf."
)

# tiefe: das Beispiel aus der Aufgabe
ergebnis = tiefe([[512, 256, [128, 128]], 1024])
assert ergebnis == 3, (
    f"tiefe([[512, 256, [128, 128]], 1024]) ergibt {ergebnis!r}, erwartet war 3 "
    "(Anlage → Rack → Gehäuse)."
)

# tiefe: eine Liste ohne innere Listen hat Tiefe 1
ergebnis = tiefe([100, 200])
assert ergebnis == 1, f"tiefe([100, 200]) ergibt {ergebnis!r}, erwartet war 1."

# tiefe: die leere Liste hat Tiefe 1
ergebnis = tiefe([])
assert ergebnis == 1, (
    f"tiefe([]) ergibt {ergebnis!r}, erwartet war 1.\nTipp: Auch eine leere Liste ist eine Ebene; zählen Sie 1 dazu."
)

# tiefe: leere innere Listen zählen mit
ergebnis = tiefe([5, [[]]])
assert ergebnis == 3, f"tiefe([5, [[]]]) ergibt {ergebnis!r}, erwartet war 3."

# tiefe: die tiefste innere Liste zählt, nicht die erste
ergebnis = tiefe([[1], [2, [3, [4]]], [5]])
assert ergebnis == 4, (
    f"tiefe([[1], [2, [3, [4]]], [5]]) ergibt {ergebnis!r}, erwartet war 4.\n"
    "Tipp: Nehmen Sie das Maximum über alle inneren Listen, nicht die erste oder die letzte."
)

# tiefe ruft sich selbst auf
assert ruft_sich_selbst_auf("tiefe", [[1], [2]]), (
    "tiefe([[1], [2]]) hat sich nicht selbst aufgerufen. Lösen Sie die Aufgabe rekursiv."
)

# gespiegelt: eine Liste ohne innere Listen
ergebnis = gespiegelt([1, 2, 3])
assert ergebnis == [3, 2, 1], f"gespiegelt([1, 2, 3]) ergibt {ergebnis!r}, erwartet war [3, 2, 1]."

# gespiegelt: das Beispiel aus der Aufgabe, auch innen umgedreht
ergebnis = gespiegelt([[512, 256, [128, 128]], 1024])
assert ergebnis == [1024, [[128, 128], 256, 512]], (
    f"gespiegelt([[512, 256, [128, 128]], 1024]) ergibt {ergebnis!r}, erwartet war [1024, [[128, 128], 256, 512]].\n"
    "Tipp: Auch jede innere Liste muss gespiegelt werden; rufen Sie dafür gespiegelt(element) auf."
)

# gespiegelt: mehrere Ebenen (nicht fest hinschreiben!)
ergebnis = gespiegelt([1, [2, [3, 4]], 5])
assert ergebnis == [5, [[4, 3], 2], 1], f"gespiegelt([1, [2, [3, 4]], 5]) ergibt {ergebnis!r}, erwartet war [5, [[4, 3], 2], 1]."

# gespiegelt: leere Listen
ergebnis = (gespiegelt([]), gespiegelt([[], [7, []]]))
assert ergebnis == ([], [[[], 7], []]), (
    f"gespiegelt([]) und gespiegelt([[], [7, []]]) ergeben {ergebnis!r}, erwartet war ([], [[[], 7], []])."
)

# gespiegelt verändert die übergebene Anlage nicht
anlage = [[512, 256, [128, 128]], 1024]
gespiegelt(anlage)
assert anlage == BEISPIEL, (
    f"Nach gespiegelt(anlage) ist anlage {anlage!r}, erwartet war unverändert {BEISPIEL!r}.\n"
    "Tipp: liste.reverse() dreht die Liste selbst um; bauen Sie stattdessen eine neue Liste auf, "
    "z. B. mit for element in reversed(anlage)."
)

# gespiegelt ruft sich selbst auf
assert ruft_sich_selbst_auf("gespiegelt", [[1], [2]]), (
    "gespiegelt([[1], [2]]) hat sich nicht selbst aufgerufen. Lösen Sie die Aufgabe rekursiv."
)

# Tief verschachtelt: 50 Ebenen
tief = [7]
for ebene in range(49):
    tief = [tief, ebene]
bekommen = (gesamt(tief), tiefe(tief), gespiegelt(gespiegelt(tief)) == tief)
erwartet = (7 + sum(range(49)), 50, True)
assert bekommen == erwartet, (
    "Für eine Anlage mit 50 ineinandersteckenden Listen [[[…[7], 0]…], 48] erwartet "
    f"(gesamt, tiefe, zweimal gespiegelt gleich Original) = {erwartet}, bekommen {bekommen}."
)

# Viele zufällige Anlagen im Vergleich mit einer Lösung ohne Rekursion
zufall = Zufall(3034)
fehlerfall = None
for runde in range(400):
    anlage = zufallsanlage(zufall, runde % 6)
    kopie = vergleich_gespiegelt(vergleich_gespiegelt(anlage))
    erwartet = (vergleich_gesamt(anlage), vergleich_tiefe(anlage), vergleich_gespiegelt(anlage))
    bekommen = (gesamt(anlage), tiefe(anlage), gespiegelt(anlage))
    if bekommen != erwartet or anlage != kopie:
        fehlerfall = (kopie, erwartet, bekommen)
        break
assert fehlerfall is None, (
    f"Für die Anlage {fehlerfall[0]!r} erwartet (gesamt, tiefe, gespiegelt) =\n  {fehlerfall[1]!r}\n"
    f"bekommen\n  {fehlerfall[2]!r}"
)

# Obere Grenze: 100 Racks mit je 99 Servern, 10 000 Einträge
grosse_anlage = [[(rack * 99 + platz) * 101 for platz in range(99)] for rack in range(100)]
erwartet = (vergleich_gesamt(grosse_anlage), 2, vergleich_gespiegelt(grosse_anlage))
bekommen = (gesamt(grosse_anlage), tiefe(grosse_anlage), gespiegelt(grosse_anlage))
assert bekommen == erwartet, (
    "Bei 100 Racks mit je 99 Servern stimmt das Ergebnis nicht: "
    f"gesamt erwartet {erwartet[0]}, bekommen {bekommen[0]!r}; tiefe erwartet 2, bekommen {bekommen[1]!r}; "
    f"gespiegelt {'stimmt' if bekommen[2] == erwartet[2] else 'stimmt nicht'}."
)
