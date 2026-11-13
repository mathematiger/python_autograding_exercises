# Automatisch erzeugt aus lehrkraft/muster/5_021_messreihe.py - nicht von Hand ändern.
# vorlage-hash: d29f69ca311bd1b3
# text-hash: 9a4d7ed9dd03e52e
# thema: datenstrukturen
# inhalt: Eigene Sequenz mit Slices

def beschreibe(reihe):
    """Werte, start und takt einer Messreihe als Tupel, für Vergleiche und Meldungen."""
    return (list(reihe._werte) if hasattr(reihe, "_werte") else list(reihe), reihe.start, reihe.takt)


def versuche(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, fehler


def erwartetes_slice(werte, start, takt, stueck):
    """Vergleichslösung: Werte, start und takt eines Slices, über eine Liste der Indizes."""
    alle = list(range(len(werte)))
    ausgewaehlt = alle[stueck]
    schritt = 1 if stueck.step is None else stueck.step
    if ausgewaehlt:
        erster = ausgewaehlt[0]
    else:
        erster = range(len(werte))[stueck].start
    return ([werte[stelle] for stelle in ausgewaehlt], start + erster * takt, takt * schritt)


BEISPIEL = [4.5, 4.8, 5.1, 6.0, 5.4]

# __init__ speichert start und takt, len zählt die Werte
reihe = Messreihe(BEISPIEL, start=600, takt=60)
assert (len(reihe), reihe.start, reihe.takt) == (5, 600, 60), (
    f"Für Messreihe({BEISPIEL}, start=600, takt=60) erwartet len 5, start 600, takt 60; "
    f"bekommen: {versuche(len, reihe)[0]!r}, {getattr(reihe, 'start', None)!r}, {getattr(reihe, 'takt', None)!r}."
)

# Ohne Angaben ist start 0 und takt 1
reihe = Messreihe([1, 2])
assert (reihe.start, reihe.takt) == (0, 1), f"Messreihe([1, 2]) hat start {reihe.start!r} und takt {reihe.takt!r}, erwartet 0 und 1."

# Ganzzahlige Indizes, auch negativ
reihe = Messreihe(BEISPIEL, start=600, takt=60)
ergebnis = (reihe[0], reihe[1], reihe[4], reihe[-1], reihe[-5])
assert ergebnis == (4.5, 4.8, 5.4, 5.4, 4.5), (
    f"reihe[0], reihe[1], reihe[4], reihe[-1], reihe[-5] ergeben {ergebnis!r}, erwartet war (4.5, 4.8, 5.4, 5.4, 4.5)."
)

# Die Werte werden kopiert: spätere Änderungen an der Liste wirken nicht
quelle = [1, 2, 3]
reihe = Messreihe(quelle)
quelle.append(4)
quelle[0] = 99
assert (len(reihe), reihe[0]) == (3, 1), (
    f"Nach Messreihe(quelle) und Änderungen an quelle hat die Messreihe len {len(reihe)} und reihe[0] {reihe[0]!r}; "
    "erwartet waren 3 und 1.\nTipp: Speichern Sie list(werte), eine Kopie."
)

# Auch ein anderes Iterable (Generator, range) als Werte
reihe = Messreihe(wert * 2 for wert in range(4))
assert (len(reihe), reihe[3]) == (4, 6), f"Messreihe(Generator 0, 2, 4, 6) hat len {len(reihe)} und reihe[3] {reihe[3]!r}, erwartet 4 und 6."

# Index außerhalb: IndexError
reihe = Messreihe(BEISPIEL)
for index in [5, 7, -6]:
    _, fehler = versuche(reihe.__getitem__, index)
    assert isinstance(fehler, IndexError), f"reihe[{index}] bei 5 Werten muss einen IndexError auslösen, bekommen: {fehler!r}."

# Falscher Indextyp: TypeError
for index in ["1", 1.0, None]:
    _, fehler = versuche(reihe.__getitem__, index)
    assert isinstance(fehler, TypeError), f"reihe[{index!r}] muss einen TypeError auslösen, bekommen: {fehler!r}."

# Ein Slice liefert eine Messreihe mit den richtigen Werten
reihe = Messreihe(BEISPIEL, start=600, takt=60)
teil, fehler = versuche(reihe.__getitem__, slice(1, 4))
assert isinstance(teil, Messreihe) and list(teil) == [4.8, 5.1, 6.0], (
    f"reihe[1:4] ergibt {teil!r}" + (f" (Ausnahme {fehler!r})" if fehler else "")
    + ", erwartet war eine Messreihe mit den Werten [4.8, 5.1, 6.0].\n"
    "Tipp: Prüfen Sie mit isinstance(index, slice) und bauen Sie Messreihe(self._werte[index], ...)."
)

# Der Slice beginnt zur Zeit des ersten ausgewählten Werts
teil = reihe[1:4]
assert (teil.start, teil.takt) == (660, 60), (
    f"reihe[1:4] hat start {teil.start!r} und takt {teil.takt!r}, erwartet waren 660 (600 + 1 · 60) und 60."
)

# Schrittweite: der Takt wird größer
teil = reihe[::2]
assert beschreibe(teil) == ([4.5, 5.1, 5.4], 600, 120), (
    f"reihe[::2] ergibt {beschreibe(teil)!r} (Werte, start, takt), erwartet war ([4.5, 5.1, 5.4], 600, 120).\n"
    "Tipp: range(len(self))[index] liefert start und step des Slices fertig normalisiert."
)

# Negative Schrittweite: rückwärts, ab dem letzten Wert
teil = reihe[::-1]
assert beschreibe(teil) == ([5.4, 6.0, 5.1, 4.8, 4.5], 840, -60), (
    f"reihe[::-1] ergibt {beschreibe(teil)!r}, erwartet war ([5.4, 6.0, 5.1, 4.8, 4.5], 840, -60)."
)

# Negative und zu große Grenzen
for stueck in [slice(-3, None), slice(2, 100), slice(-100, 2), slice(4, 0, -2)]:
    teil = reihe[stueck]
    erwartet = erwartetes_slice(BEISPIEL, 600, 60, stueck)
    assert beschreibe(teil) == erwartet, f"reihe[{stueck}] ergibt {beschreibe(teil)!r}, erwartet war {erwartet!r}."

# Ein leerer Slice ist eine leere Messreihe
teil = reihe[3:1]
assert isinstance(teil, Messreihe) and len(teil) == 0 and teil.takt == 60, (
    f"reihe[3:1] ergibt {teil!r}, erwartet war eine leere Messreihe mit takt 60."
)

# Ein Slice eines Slices
teil = reihe[1:][::2]
assert beschreibe(teil) == ([4.8, 6.0], 660, 120), f"reihe[1:][::2] ergibt {beschreibe(teil)!r}, erwartet war ([4.8, 6.0], 660, 120)."

# in prüft die Werte
reihe = Messreihe(BEISPIEL, start=600, takt=60)
ergebnis = (6.0 in reihe, 7.0 in reihe, 4.5 in reihe)
assert ergebnis == (True, False, True), f"6.0 in reihe, 7.0 in reihe, 4.5 in reihe ergeben {ergebnis!r}, erwartet war (True, False, True)."

# in auch für Slices: nur die ausgewählten Werte zählen
teil = reihe[1:3]
ergebnis = (4.5 in teil, 5.1 in teil)
assert ergebnis == (False, True), (
    f"Für teil = reihe[1:3] ergeben 4.5 in teil und 5.1 in teil {ergebnis!r}, erwartet war (False, True)."
)

# Geerbte Methoden: Iteration, index, count, reversed, isinstance
reihe = Messreihe([3, 1, 3, 2], start=0, takt=10)
ergebnis = (list(reihe), reihe.index(2), reihe.count(3), list(reversed(reihe)), isinstance(reihe, Sequence))
assert ergebnis == ([3, 1, 3, 2], 3, 2, [2, 3, 1, 3], True), (
    f"list, index(2), count(3), reversed und isinstance(…, Sequence) ergeben {ergebnis!r}, "
    "erwartet war ([3, 1, 3, 2], 3, 2, [2, 3, 1, 3], True)."
)

# Die vorgegebene Methode zeitpunkt passt zu den Slices
reihe = Messreihe(BEISPIEL, start=600, takt=60)
teil = reihe[4:0:-2]
ergebnis = [teil.zeitpunkt(stelle) for stelle in range(len(teil))]
assert ergebnis == [840, 720], f"Für reihe[4:0:-2] liefert zeitpunkt die Zeiten {ergebnis!r}, erwartet war [840, 720]."

# Leere Messreihe
leer = Messreihe([])
ergebnis = (len(leer), list(leer), 1 in leer, len(leer[:]))
assert ergebnis == (0, [], False, 0), f"Messreihe([]) ergibt len, list, 1 in, len(leer[:]) = {ergebnis!r}, erwartet war (0, [], False, 0)."

# in braucht nicht die ganze Liste: Vergleiche zählen statt Zeit messen
class Gezaehlt(int):
    """Ganze Zahl, die mitzählt, wie oft sie mit == verglichen wird."""

    vergleiche = 0

    def __eq__(self, anderer):
        Gezaehlt.vergleiche += 1
        return int(self) == int(anderer)

    __hash__ = int.__hash__

gross = Messreihe([Gezaehlt(wert) for wert in range(100000)])
Gezaehlt.vergleiche = 0
gefunden = Gezaehlt(100001) in gross
assert gefunden is False and Gezaehlt.vergleiche <= 5, (
    f"100001 in Messreihe(0 bis 99 999) ergibt {gefunden!r} nach {Gezaehlt.vergleiche} Vergleichen mit ==; "
    "erwartet waren False und höchstens 5 Vergleiche (O(1)).\n"
    "Tipp: Legen Sie im __init__ eine Menge (set) der Werte an und fragen Sie in __contains__ sie statt der Liste."
)

# Viele zufällige Slices gegen die Vergleichslösung
zufall = Zufall(5021)
for _ in range(1500):
    werte = [zufall.randint(-5, 5) for _ in range(zufall.randint(0, 9))]
    start = zufall.randint(0, 86400)
    takt = zufall.randint(1, 3600)
    reihe = Messreihe(werte, start=start, takt=takt)
    stueck = slice(
        zufall.choice([None, zufall.randint(-12, 12)]),
        zufall.choice([None, zufall.randint(-12, 12)]),
        zufall.choice([None, 1, 2, 3, -1, -2, -3]),
    )
    teil = reihe[stueck]
    erwartet = erwartetes_slice(werte, start, takt, stueck)
    bekommen = beschreibe(teil)
    if not erwartet[0]:
        # Bei leeren Slices ist start beliebig
        erwartet = (erwartet[0], None, erwartet[2])
        bekommen = (bekommen[0], None, bekommen[2])
    gesucht = zufall.randint(-6, 6)
    assert bekommen == erwartet and (gesucht in teil) == (gesucht in erwartet[0]), (
        f"Messreihe({werte}, start={start}, takt={takt})[{stueck}] ergibt {beschreibe(teil)!r}, erwartet war {erwartet!r}"
        f" (Werte, start, takt); {gesucht} in teil ergibt {gesucht in teil}."
    )

# Obere Grenze: 100 000 Werte, Slice und Index
gross = Messreihe([wert * 0.5 for wert in range(100000)], start=86400, takt=3600)
teil = gross[-10::3]
assert (len(gross), gross[-1], beschreibe(teil)) == (
    100000, 49999.5, ([49995.0, 49996.5, 49998.0, 49999.5], 86400 + 99990 * 3600, 10800)
), f"Bei 100 000 Werten ergeben len, reihe[-1] und reihe[-10::3]: {len(gross)}, {gross[-1]!r}, {beschreibe(teil)!r}."
