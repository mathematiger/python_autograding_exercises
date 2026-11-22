# Automatisch erzeugt aus lehrkraft/muster/3_034_rackbaum.py - nicht von Hand ändern.
# vorlage-hash: 42810329a4b44f4e
# text-hash: 1f3e44975c3263de
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


def kopie(anlage):
    """Gibt eine tiefe Kopie der verschachtelten Liste zurück."""
    return vergleich_gespiegelt(vergleich_gespiegelt(anlage))


def erster_fehler(funktion, vergleich, anlagen):
    """Gibt (anlage, erwartet, bekommen) für die erste Anlage zurück, bei der funktion anders als vergleich rechnet, sonst None."""
    for anlage in anlagen:
        erwartet = vergleich(anlage)
        bekommen = funktion(kopie(anlage))
        if bekommen != erwartet:
            return anlage, erwartet, bekommen
    return None


def meldung_zufall(name, fehlerfall):
    """Formuliert die Meldung zum Fehlerfall aus erster_fehler für die Funktion name."""
    anlage, erwartet, bekommen = fehlerfall
    return f"Für die Anlage {anlage!r} war bei {name}\n  {erwartet!r} erwartet, Ihr Ergebnis:\n  {bekommen!r}."


def erste_veraenderte(funktion, anlagen):
    """Gibt die erste Anlage zurück, die funktion beim Aufruf verändert, sonst None."""
    for anlage in anlagen:
        uebergeben = kopie(anlage)
        funktion(uebergeben)
        if uebergeben != anlage:
            return anlage
    return None


def wert_von(funktion, anlage):
    """Ruft funktion(anlage) auf; ein Fehler wie RecursionError wird als Text zurückgegeben."""
    try:
        return funktion(anlage)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


TIPP_BREIT = (
    "Tipp: Gehen Sie die Elemente einer Ebene mit for durch und rufen Sie die Funktion nur für innere Listen auf "
    "(nicht für anlage[1:])."
)


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

# Tief verschachtelt: gesamt bei 50 Ebenen
tief = [7]
for ebene in range(49):
    tief = [tief, ebene]
ergebnis = gesamt(tief)
assert ergebnis == 7 + sum(range(49)), (
    f"Für eine Anlage aus 50 ineinandersteckenden Listen [[[…[7], 0]…], 48] war bei gesamt {7 + sum(range(49))} "
    f"erwartet, Ihr Ergebnis: {ergebnis!r}."
)

# Tief verschachtelt: tiefe bei 50 Ebenen
ergebnis = tiefe(tief)
assert ergebnis == 50, (
    f"Für eine Anlage aus 50 ineinandersteckenden Listen [[[…[7], 0]…], 48] war bei tiefe 50 erwartet, "
    f"Ihr Ergebnis: {ergebnis!r}."
)

# Tief verschachtelt: gespiegelt bei 50 Ebenen
erwartet = vergleich_gespiegelt(tief)
ergebnis = gespiegelt(tief)
assert ergebnis == erwartet, (
    "Für eine Anlage aus 50 ineinandersteckenden Listen [[[…[7], 0]…], 48] stimmt gespiegelt nicht.\n"
    f"Erwartet war {erwartet!r},\nIhr Ergebnis: {ergebnis!r}."
)

# Viele zufällige Anlagen: gesamt im Vergleich mit einer Lösung ohne Rekursion
zufall = Zufall(3034)
zufallsanlagen = [zufallsanlage(zufall, runde % 6) for runde in range(400)]
fehlerfall = erster_fehler(gesamt, vergleich_gesamt, zufallsanlagen)
assert fehlerfall is None, meldung_zufall("gesamt", fehlerfall)

# Viele zufällige Anlagen: tiefe im Vergleich mit einer Lösung ohne Rekursion
fehlerfall = erster_fehler(tiefe, vergleich_tiefe, zufallsanlagen)
assert fehlerfall is None, meldung_zufall("tiefe", fehlerfall)

# Viele zufällige Anlagen: gespiegelt im Vergleich mit einer anderen Lösung
fehlerfall = erster_fehler(gespiegelt, vergleich_gespiegelt, zufallsanlagen)
assert fehlerfall is None, meldung_zufall("gespiegelt", fehlerfall)

# Viele zufällige Anlagen: gespiegelt verändert keine davon
veraendert = erste_veraenderte(gespiegelt, zufallsanlagen)
assert veraendert is None, (
    f"gespiegelt(anlage) hat die übergebene Anlage {veraendert!r} verändert, erwartet war, dass sie unverändert bleibt.\n"
    "Tipp: Bauen Sie eine neue Liste auf, statt anlage oder ihre inneren Listen umzudrehen."
)

# Obere Grenze: gesamt bei 100 Racks mit je 98 Servern, mit den Listen 9 901 Einträge
grosse_anlage = [[(rack * 98 + platz) * 101 for platz in range(98)] for rack in range(100)]
ergebnis = gesamt(grosse_anlage)
assert ergebnis == vergleich_gesamt(grosse_anlage), (
    f"Bei 100 Racks mit je 98 Servern war bei gesamt {vergleich_gesamt(grosse_anlage)} erwartet, Ihr Ergebnis: {ergebnis!r}."
)

# Obere Grenze: tiefe bei 100 Racks mit je 98 Servern
ergebnis = tiefe(grosse_anlage)
assert ergebnis == 2, f"Bei 100 Racks mit je 98 Servern war bei tiefe 2 erwartet, Ihr Ergebnis: {ergebnis!r}."

# Obere Grenze: gespiegelt bei 100 Racks mit je 98 Servern
erwartet = vergleich_gespiegelt(grosse_anlage)
ergebnis = gespiegelt(grosse_anlage)
assert ergebnis == erwartet, (
    "Bei 100 Racks mit je 98 Servern stimmt gespiegelt nicht mit der Vergleichslösung überein."
)

# Obere Grenze: gesamt bei einem einzigen Rack mit 9 999 Servern, mit der Liste 10 000 Einträge
breite_anlage = [(platz * 37) % 1000 for platz in range(9999)]
ergebnis = wert_von(gesamt, breite_anlage)
assert ergebnis == sum(breite_anlage), (
    f"Bei einem Rack mit 9 999 Servern war bei gesamt {sum(breite_anlage)} erwartet, Ihr Ergebnis: {ergebnis!r}.\n"
    f"{TIPP_BREIT}"
)

# Obere Grenze: tiefe bei einem einzigen Rack mit 9 999 Servern
ergebnis = wert_von(tiefe, breite_anlage)
assert ergebnis == 1, f"Bei einem Rack mit 9 999 Servern war bei tiefe 1 erwartet, Ihr Ergebnis: {ergebnis!r}.\n{TIPP_BREIT}"

# Obere Grenze: gespiegelt bei einem einzigen Rack mit 9 999 Servern
erwartet = breite_anlage[::-1]
ergebnis = wert_von(gespiegelt, breite_anlage)
assert ergebnis == erwartet, (
    "Bei einem Rack mit 9 999 Servern stimmt gespiegelt nicht mit der umgedrehten Liste überein, "
    f"Ihr Ergebnis beginnt mit: {repr(ergebnis)[:100]}\n{TIPP_BREIT}"
)
