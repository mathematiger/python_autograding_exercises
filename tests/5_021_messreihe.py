# Automatisch erzeugt aus lehrkraft/muster/5_021_messreihe.py - nicht von Hand ändern.
# vorlage-hash: 69e49e80b3843c04
# text-hash: 550b550bfff5b94f
# thema: datenstrukturen
# inhalt: Eigene Sequenz mit Slices

def versuche(funktion):
    """Ruft funktion() auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(), None
    except Exception as fehler:
        return None, fehler


def beschreibe(reihe):
    """Beschreibt eine Messreihe als (start, takt, Werte) oder gibt das Objekt zurück."""
    if isinstance(reihe, Messreihe):
        return reihe.start, reihe.takt, list(reihe._werte)
    return reihe


WERTE = [4.1, 4.3, 4.0, 3.8, 4.2]

# len liefert die Anzahl der Werte
reihe = Messreihe(3600, 60, WERTE)
ergebnis, fehler = versuche(lambda: len(reihe))
assert ergebnis == 5, f"len(reihe) ergibt {ergebnis!r} {fehler or ''}, erwartet war 5."

# Ganze Zahlen als Index
ergebnis, fehler = versuche(lambda: [reihe[0], reihe[2], reihe[4]])
assert ergebnis == [4.1, 4.0, 4.2], f"reihe[0], reihe[2], reihe[4] ergeben {ergebnis!r} {fehler or ''}, erwartet war [4.1, 4.0, 4.2]."

# Negative Indizes zählen von hinten
ergebnis, fehler = versuche(lambda: [reihe[-1], reihe[-5]])
assert ergebnis == [4.2, 4.1], (
    f"reihe[-1] und reihe[-5] ergeben {ergebnis!r} {fehler or ''}, erwartet war [4.2, 4.1].\n"
    "Tipp: Für einen negativen Index ist die Stelle index + len(self)."
)

# Außerhalb: IndexError, auch bei negativen Indizes
for index in [5, -6, 10**6, -(10**6)]:
    ergebnis, fehler = versuche(lambda: reihe[index])
    assert isinstance(fehler, IndexError), (
        f"reihe[{index}] bei 5 Werten soll einen IndexError auslösen, ergibt aber {ergebnis!r} {fehler!r}.\n"
        "Tipp: Python würde self._werte[-6] zwar ablehnen, self._werte[-1] aber nicht; prüfen Sie die Grenzen selbst."
    )

# Andere Typen als Index: TypeError
for index in ["1", 1.0, None, True]:
    ergebnis, fehler = versuche(lambda: reihe[index])
    assert isinstance(fehler, TypeError), (
        f"reihe[{index!r}] soll einen TypeError auslösen, ergibt aber {ergebnis!r} {fehler!r}.\n"
        "Tipp: bool ist eine Unterklasse von int; schließen Sie es mit isinstance(index, bool) eigens aus."
    )

# Das Beispiel: Slice mit Schrittweite liefert eine Messreihe mit neuem Start und Takt
ergebnis, fehler = versuche(lambda: beschreibe(reihe[1:5:2]))
assert ergebnis == (3660, 120, [4.3, 3.8]), (
    f"reihe[1:5:2] ergibt {ergebnis!r} {fehler or ''}, erwartet war eine Messreihe mit start 3660, takt 120 "
    "und den Werten [4.3, 3.8].\nTipp: range(*index.indices(len(self))) liefert die ausgewählten Stellen."
)

# Ein Slice ohne Schrittweite behält den Takt
ergebnis, fehler = versuche(lambda: beschreibe(reihe[2:]))
assert ergebnis == (3720, 60, [4.0, 3.8, 4.2]), (
    f"reihe[2:] ergibt {ergebnis!r} {fehler or ''}, erwartet war (3720, 60, [4.0, 3.8, 4.2]) als Messreihe."
)

# Slices mit negativen und zu großen Grenzen wie bei Listen
for ausschnitt, erwartet in [
    (slice(-2, None), (3780, 60, [3.8, 4.2])),
    (slice(-100, 2), (3600, 60, [4.1, 4.3])),
    (slice(3, 100), (3780, 60, [3.8, 4.2])),
]:
    ergebnis, fehler = versuche(lambda: beschreibe(reihe[ausschnitt]))
    assert ergebnis == erwartet, f"reihe[{ausschnitt.start}:{ausschnitt.stop}] ergibt {ergebnis!r} {fehler or ''}, erwartet war {erwartet}."

# Negative Schrittweite: rückwärts, der Takt wird negativ
ergebnis, fehler = versuche(lambda: beschreibe(reihe[::-2]))
assert ergebnis == (3840, -120, [4.2, 4.0, 4.1]), (
    f"reihe[::-2] ergibt {ergebnis!r} {fehler or ''}, erwartet war (3840, -120, [4.2, 4.0, 4.1]).\n"
    "Tipp: Der neue Start ist der Zeitpunkt des ersten ausgewählten Werts, der neue Takt takt · step."
)

# Leerer Ausschnitt ist eine leere Messreihe
ergebnis, fehler = versuche(lambda: reihe[3:1])
assert isinstance(ergebnis, Messreihe) and len(ergebnis._werte) == 0, (
    f"reihe[3:1] ergibt {beschreibe(ergebnis)!r} {fehler or ''}, erwartet war eine leere Messreihe."
)

# Ausschnitte von Ausschnitten passen zu den Zeitpunkten
lang = Messreihe(0, 10, list(range(100)))
ergebnis, fehler = versuche(lambda: lang[10:90:3][5:20:2])
bekommen = beschreibe(ergebnis)
erwartet = (250, 60, list(range(100))[10:90:3][5:20:2])
assert bekommen == erwartet, f"Messreihe(0, 10, range(100))[10:90:3][5:20:2] ergibt {bekommen!r} {fehler or ''}, erwartet war {erwartet}."

# Die Mixin-Methoden von Sequence funktionieren
ergebnis, fehler = versuche(lambda: (list(reihe), 3.8 in reihe, 9.9 in reihe, reihe.index(4.0), list(reversed(reihe)), reihe.count(4.1)))
assert ergebnis == (WERTE, True, False, 2, WERTE[::-1], 1), (
    f"list, in, index, reversed und count ergeben {ergebnis!r} {fehler or ''}, erwartet war "
    f"({WERTE}, True, False, 2, {WERTE[::-1]}, 1).\n"
    "Tipp: Diese Methoden erbt Messreihe von Sequence; sie brauchen einen IndexError am Ende."
)

# Messreihe ist eine Sequence
assert isinstance(reihe, Sequence), "Messreihe soll von collections.abc.Sequence erben."

# Leere Messreihe
leer = Messreihe(0, 1, [])
ergebnis, fehler = versuche(lambda: (len(leer), list(leer), 1 in leer, beschreibe(leer[:])))
assert ergebnis == (0, [], False, (0, 1, [])), (
    f"Für Messreihe(0, 1, []) ergeben len, list, 1 in, [:] {ergebnis!r} {fehler or ''}, erwartet war (0, [], False, (0, 1, []))."
)
# Leere Messreihe: schon Index 0 liegt außerhalb
ergebnis, fehler = versuche(lambda: leer[0])
assert isinstance(fehler, IndexError), f"Messreihe(0, 1, [])[0] soll einen IndexError auslösen, ergibt {ergebnis!r} {fehler!r}."

# Spätere Änderungen an der übergebenen Liste ändern die Messreihe nicht
quelle = [1.0, 2.0]
reihe_q = Messreihe(0, 5, quelle)
quelle.append(3.0)
quelle[0] = 99.0
ergebnis, fehler = versuche(lambda: (len(reihe_q), reihe_q[0]))
assert ergebnis == (2, 1.0), f"Nach Änderungen an der übergebenen Liste ergeben len und [0] {ergebnis!r} {fehler or ''}, erwartet war (2, 1.0)."

# Ein Ausschnitt teilt seine Werte nicht mit dem Original
original = Messreihe(0, 1, [1, 2, 3, 4])
kopie = original[1:3]
if isinstance(kopie, Messreihe):
    kopie._werte.append(99)
ergebnis, fehler = versuche(lambda: list(original))
assert ergebnis == [1, 2, 3, 4], f"Nach einer Änderung an original[1:3] ist original {ergebnis!r} {fehler or ''}, erwartet war [1, 2, 3, 4]."

# Viele zufällige Indizes und Slices, verglichen mit einer Liste
zufall = Zufall(5021)
for _ in range(500):
    laenge = zufall.randint(0, 12)
    werte = [zufall.randint(-20, 20) for _ in range(laenge)]
    start = zufall.randint(0, 10**6)
    takt = zufall.randint(1, 3600)
    r = Messreihe(start, takt, werte)
    if zufall.random() < 0.4:
        index = zufall.randint(-15, 15)
        ergebnis, fehler = versuche(lambda: r[index])
        if -laenge <= index < laenge:
            assert fehler is None and ergebnis == werte[index], (
                f"Messreihe({start}, {takt}, {werte})[{index}] ergibt {ergebnis!r} {fehler or ''}, erwartet war {werte[index]}."
            )
        else:
            assert isinstance(fehler, IndexError), (
                f"Messreihe({start}, {takt}, {werte})[{index}] soll einen IndexError auslösen, ergibt {ergebnis!r} {fehler!r}."
            )
    else:
        grenzen = [None] + list(range(-15, 16))
        ausschnitt = slice(zufall.choice(grenzen), zufall.choice(grenzen), zufall.choice([None, 1, 2, 3, -1, -2, -3]))
        stellen = list(range(laenge))[ausschnitt]
        schritt = 1 if ausschnitt.step is None else ausschnitt.step
        erster = stellen[0] if stellen else range(*ausschnitt.indices(laenge)).start
        erwartet = (start + erster * takt, takt * schritt, werte[ausschnitt])
        ergebnis, fehler = versuche(lambda: beschreibe(r[ausschnitt]))
        erwartet_ohne_start = erwartet[1:]
        passt = ergebnis == erwartet if stellen else isinstance(ergebnis, tuple) and ergebnis[1:] == erwartet_ohne_start
        assert passt, (
            f"Messreihe({start}, {takt}, {werte})[{ausschnitt.start}:{ausschnitt.stop}:{ausschnitt.step}] ergibt "
            f"{ergebnis!r} {fehler or ''}, erwartet war {erwartet}."
        )

# Obere Grenze: 100 000 Werte, Zugriff in O(1)
gross = Messreihe(0, 1, list(range(100_000)))
ergebnis, schritte = zaehle_schritte(lambda: gross[99_999] + gross[-100_000] + gross[50_000])
assert ergebnis == 99_999 + 0 + 50_000 and schritte <= 60, (
    f"Drei Zugriffe auf eine Messreihe mit 100 000 Werten ergeben {ergebnis!r} und brauchen {schritte} Schritte; "
    "erwartet waren 149999 und höchstens 60 Schritte, also O(1) je Zugriff.\n"
    "Tipp: Gehen Sie bei einem einzelnen Index nicht durch die Liste, sondern greifen Sie direkt auf self._werte zu."
)

# Obere Grenze: Slice über 100 000 Werte
ergebnis, fehler = versuche(lambda: beschreibe(gross[::1000]))
assert ergebnis == (0, 1000, list(range(0, 100_000, 1000))), (
    f"Messreihe(0, 1, range(100000))[::1000] ergibt eine falsche Messreihe {fehler or ''}: "
    f"start und takt {ergebnis[:2] if isinstance(ergebnis, tuple) else ergebnis!r}, erwartet (0, 1000)."
)

# Die Ausgabe des Programms stimmt
ERWARTET = "5 4.2 Messreihe(start=3660, takt=120, werte=[4.3, 3.8])"
assert vergleichbar(AUSGABE) == vergleichbar(ERWARTET), f'Erwartete Ausgabe: "{ERWARTET}" – Ihr Programm: "{AUSGABE}"'
