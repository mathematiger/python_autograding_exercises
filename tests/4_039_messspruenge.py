# Automatisch erzeugt aus lehrkraft/muster/4_039_messspruenge.py - nicht von Hand ändern.
# vorlage-hash: f640aef693073262
# text-hash: 3ecabd7642a09cd5
# thema: kontrollfluss
# inhalt: Übung: Iteratoren und Generatoren

import types

BEISPIEL = ["halle1/presse3/temp 61.5", "halle1/presse4/temp 58.0", "halle1/presse3/temp ERR", "halle1/presse3/temp 75.0"]
BEISPIEL_TUPEL = [("halle1/presse3/temp", 61.5), ("halle1/presse4/temp", 58.0), ("halle1/presse3/temp", 75.0)]


class Zaehlquelle:
    """Ein Iterable, das jeden Durchlauf neu beginnt und mitzählt, wie viele Zeilen abgeholt wurden."""

    def __init__(self, zeile_zu_nummer, laenge=None):
        """Merkt sich, wie aus einer Zeilennummer die Zeile wird, und die Länge (None = unendlich)."""
        self.zeile_zu_nummer = zeile_zu_nummer
        self.laenge = laenge
        self.gelesen = 0

    def __iter__(self):
        """Liefert die Zeilen der Reihe nach und zählt jede abgeholte Zeile."""
        nummer = 0
        while self.laenge is None or nummer < self.laenge:
            self.gelesen += 1
            yield self.zeile_zu_nummer(nummer)
            nummer += 1


def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def ruhige_halle(nummer):
    """Unendliches Protokoll: vier Pressen mit Temperaturen 60 bis 64; ab Zeile 1000 springt presse2 auf 90."""
    presse = nummer % 4
    if nummer == 1002:
        return "halle1/presse2/temp 90.0"
    if nummer % 7 == 0:
        return f"halle1/presse{presse}/druck {nummer % 13}"
    return f"halle1/presse{presse}/temp {60 + nummer % 5}"


def vergleich_tupel(zeilen):
    """Vergleichslösung für das Zerlegen, mit Liste statt Generator."""
    ergebnis = []
    for zeile in zeilen:
        teile = zeile.split()
        if len(teile) == 2:
            try:
                ergebnis.append((teile[0], float(teile[1])))
            except ValueError:
                pass
    return ergebnis


def vergleich_passt(topic, muster):
    """Vergleichslösung: übersetzt das Muster in einen regulären Ausdruck."""
    import re

    ausdruck = "/".join("[^/]+" if ebene == "+" else re.escape(ebene) for ebene in muster.split("/"))
    return re.fullmatch(ausdruck, topic) is not None


def vergleich_spruenge(messungen, schwelle):
    """Vergleichslösung: sucht zu jeder Messung rückwärts die letzte desselben Topics."""
    ergebnis = []
    for stelle, (topic, wert) in enumerate(messungen):
        frueher = [w for t, w in messungen[:stelle] if t == topic]
        if frueher and abs(wert - frueher[-1]) > schwelle:
            ergebnis.append((topic, frueher[-1], wert))
    return ergebnis


def zufallszeile(zufall):
    """Eine zufällige Protokollzeile: meist gültig, manchmal kaputt."""
    topic = zufall.choice(["a/x/temp", "a/y/temp", "a/x/druck", "b/x/temp", "a/x/kopf/temp", "a"])
    art = zufall.random()
    if art < 0.1:
        return zufall.choice(["", "   ", f"{topic} ERR", f"{topic} 21,5", f"{topic} 1 2", topic])
    wert = zufall.choice([zufall.randint(-5, 5), zufall.randint(-1000000, 1000000) / 4])
    return f"{topic} {wert}"


# Messprotokoll liefert im Beispiel die gültigen Zeilen als Tupel
ergebnis = wert_von(lambda: list(Messprotokoll(BEISPIEL)))
assert ergebnis == BEISPIEL_TUPEL, f"list(Messprotokoll(...)) ergibt im Beispiel {ergebnis!r}, erwartet war {BEISPIEL_TUPEL!r}."

# Messprotokoll: der Wert ist ein float, auch bei ganzen Zahlen und Vorzeichen
ergebnis = wert_von(lambda: list(Messprotokoll(["k/temp 12", "k/temp -3.25", "k/temp +7"])))
assert ergebnis == [("k/temp", 12.0), ("k/temp", -3.25), ("k/temp", 7.0)] and all(type(w) is float for _, w in ergebnis), (
    f'list(Messprotokoll(["k/temp 12", "k/temp -3.25", "k/temp +7"])) ergibt {ergebnis!r}, '
    "erwartet war [('k/temp', 12.0), ('k/temp', -3.25), ('k/temp', 7.0)] mit float-Werten."
)

# Messprotokoll überspringt ungültige Zeilen
zeilen = ["", "   ", "k/temp", "k/temp ERR", "k/temp 21,5", "k/temp 1 2", "k/temp 4.5"]
ergebnis = wert_von(lambda: list(Messprotokoll(zeilen)))
assert ergebnis == [("k/temp", 4.5)], (
    f"list(Messprotokoll({zeilen!r})) ergibt {ergebnis!r}, erwartet war [('k/temp', 4.5)].\n"
    "Tipp: Prüfen Sie, ob split() genau zwei Teile liefert, und fangen Sie den ValueError von float(...) ab."
)

# __iter__ ist eine Generatormethode
ergebnis = wert_von(lambda: iter(Messprotokoll(BEISPIEL)))
assert isinstance(ergebnis, types.GeneratorType), (
    f"iter(Messprotokoll(...)) ergibt {ergebnis!r}, erwartet war ein Generator.\nTipp: Schreiben Sie __iter__ mit yield."
)

# Ein Messprotokoll lässt sich mehrmals und verschachtelt durchlaufen
protokoll = Messprotokoll(BEISPIEL)
ergebnis = wert_von(lambda: (list(protokoll), list(protokoll), len([(a, b) for a in protokoll for b in protokoll])))
assert ergebnis == (BEISPIEL_TUPEL, BEISPIEL_TUPEL, 9), (
    f"Zweimal list(protokoll) und die Zahl der Paare aus zwei verschachtelten Durchläufen ergeben {ergebnis!r}, "
    f"erwartet war ({BEISPIEL_TUPEL!r}, dasselbe, 9).\nTipp: __iter__ beginnt jedes Mal neu mit for zeile in self.zeilen."
)

# passend mit + für eine Ebene
messungen = [("halle1/presse3/temp", 1.0), ("halle1/presse3/druck", 2.0), ("halle2/presse3/temp", 3.0), ("halle1/kran/temp", 4.0)]
ergebnis = wert_von(lambda: list(passend(messungen, "halle1/+/temp")))
assert ergebnis == [messungen[0], messungen[3]], (
    f'list(passend(..., "halle1/+/temp")) ergibt {ergebnis!r}, erwartet war {[messungen[0], messungen[3]]!r}.\n'
    'Tipp: Zerlegen Sie Topic und Muster mit split("/") und vergleichen Sie Ebene für Ebene.'
)

# passend: + steht für genau eine Ebene, nicht für mehrere oder keine
messungen = [("halle1/presse3/kopf/temp", 1.0), ("halle1/temp", 2.0), ("halle1/x/temp", 3.0)]
ergebnis = wert_von(lambda: list(passend(messungen, "halle1/+/temp")))
assert ergebnis == [("halle1/x/temp", 3.0)], (
    f'list(passend({messungen!r}, "halle1/+/temp")) ergibt {ergebnis!r}, erwartet war [("halle1/x/temp", 3.0)].\n'
    "Tipp: Topic und Muster müssen gleich viele Ebenen haben."
)

# passend ohne +, mit + am Anfang und am Ende
messungen = [("a/b", 1.0), ("a/c", 2.0), ("x/b", 3.0), ("a", 4.0)]
ergebnis = wert_von(lambda: [list(passend(messungen, "a/b")), list(passend(messungen, "+/b")), list(passend(messungen, "a/+")), list(passend(messungen, "+"))])
erwartet = [[("a/b", 1.0)], [("a/b", 1.0), ("x/b", 3.0)], [("a/b", 1.0), ("a/c", 2.0)], [("a", 4.0)]]
assert ergebnis == erwartet, f'passend mit den Mustern "a/b", "+/b", "a/+" und "+" ergibt {ergebnis!r}, erwartet war {erwartet!r}.'

# passend ist eine Generatorfunktion
assert isinstance(passend([], "a"), types.GeneratorType), "passend(...) soll einen Generator liefern (yield statt return einer Liste)."

# spruenge im Beispiel
ergebnis = wert_von(lambda: list(spruenge(BEISPIEL_TUPEL, 10)))
assert ergebnis == [("halle1/presse3/temp", 61.5, 75.0)], (
    f"list(spruenge(..., 10)) ergibt im Beispiel {ergebnis!r}, erwartet war [('halle1/presse3/temp', 61.5, 75.0)].\n"
    "Tipp: Merken Sie sich den letzten Wert je Topic in einem Dictionary, nicht den letzten Wert überhaupt."
)

# spruenge nach unten und mehrere Sprünge nacheinander
messungen = [("t", 50.0), ("t", 20.0), ("t", 21.0), ("t", 40.0)]
ergebnis = wert_von(lambda: list(spruenge(messungen, 5)))
assert ergebnis == [("t", 50.0, 20.0), ("t", 21.0, 40.0)], (
    f"list(spruenge({messungen!r}, 5)) ergibt {ergebnis!r}, erwartet war [('t', 50.0, 20.0), ('t', 21.0, 40.0)].\n"
    "Tipp: Vergleichen Sie den Betrag abs(neu - alt), und merken Sie sich nach jedem Wert den neuen."
)

# spruenge: ein Unterschied genau gleich der Schwelle ist kein Sprung
ergebnis = wert_von(lambda: list(spruenge([("t", 10.0), ("t", 15.0), ("t", 10.0)], 5)))
assert ergebnis == [], f"list(spruenge([('t', 10.0), ('t', 15.0), ('t', 10.0)], 5)) ergibt {ergebnis!r}, erwartet war []."

# spruenge mit Schwelle 0: jede Änderung ist ein Sprung, gleiche Werte nicht
ergebnis = wert_von(lambda: list(spruenge([("t", 1.0), ("t", 1.0), ("t", 1.5)], 0)))
assert ergebnis == [("t", 1.0, 1.5)], f"list(spruenge([('t', 1.0), ('t', 1.0), ('t', 1.5)], 0)) ergibt {ergebnis!r}, erwartet war [('t', 1.0, 1.5)]."

# spruenge: der erste Wert eines Topics ist nie ein Sprung
ergebnis = wert_von(lambda: list(spruenge([("a", 0.0), ("b", 900.0), ("c", -900.0)], 1)))
assert ergebnis == [], (
    f"list(spruenge([('a', 0.0), ('b', 900.0), ('c', -900.0)], 1)) ergibt {ergebnis!r}, erwartet war [] (drei verschiedene Topics)."
)

# spruenge ist eine Generatorfunktion
assert isinstance(spruenge([], 1), types.GeneratorType), "spruenge(...) soll einen Generator liefern (yield statt return einer Liste)."

# erster_sprung im Beispiel
protokoll = Messprotokoll(BEISPIEL)
ergebnis = wert_von(lambda: [erster_sprung(protokoll, "halle1/+/temp", 10), erster_sprung(protokoll, "halle1/+/temp", 20)])
assert ergebnis == [("halle1/presse3/temp", 61.5, 75.0), None], (
    f"erster_sprung mit Schwelle 10 und 20 ergibt im Beispiel {ergebnis!r}, erwartet war "
    "[('halle1/presse3/temp', 61.5, 75.0), None].\nTipp: next(kette, None) liefert None, wenn die Kette leer ist."
)

# erster_sprung beachtet das Muster
protokoll = Messprotokoll(["h/a/temp 10", "h/a/druck 1", "h/a/druck 99", "h/a/temp 30"])
ergebnis = wert_von(lambda: [erster_sprung(protokoll, "h/+/temp", 5), erster_sprung(protokoll, "h/a/druck", 5), erster_sprung(protokoll, "x/+", 0)])
assert ergebnis == [("h/a/temp", 10.0, 30.0), ("h/a/druck", 1.0, 99.0), None], (
    f"erster_sprung mit den Mustern h/+/temp, h/a/druck und x/+ ergibt {ergebnis!r}, erwartet war "
    "[('h/a/temp', 10.0, 30.0), ('h/a/druck', 1.0, 99.0), None]."
)

# erster_sprung eines leeren Protokolls
ergebnis = wert_von(lambda: erster_sprung(Messprotokoll([]), "+", 1))
assert ergebnis is None, f"erster_sprung(Messprotokoll([]), '+', 1) ergibt {ergebnis!r}, erwartet war None."

# Die Ausgabe des Programms
erwartet = f"{BEISPIEL_TUPEL}\n('halle1/presse3/temp', 61.5, 75.0)\nNone"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Die Kette liest bei einem unendlichen Protokoll nur so weit wie nötig
quelle = Zaehlquelle(ruhige_halle)
ergebnis = wert_von(lambda: erster_sprung(Messprotokoll(quelle), "halle1/+/temp", 10))
assert ergebnis == ("halle1/presse2/temp", 63.0, 90.0) and quelle.gelesen == 1003, (
    f"erster_sprung bei einem unendlichen Protokoll ergibt {ergebnis!r} nach {quelle.gelesen} gelesenen Zeilen; "
    "erwartet war ('halle1/presse2/temp', 63.0, 90.0) nach genau 1003 Zeilen.\n"
    "Tipp: Sammeln Sie in keiner Stufe eine Liste; jede Stufe gibt mit yield sofort weiter."
)

# Jede Stufe holt nur einen Wert, wenn sie einen liefern soll
quelle = Zaehlquelle(lambda nummer: f"a/b {nummer}")
kette = wert_von(lambda: spruenge(passend(Messprotokoll(quelle), "a/+"), 0.5))
ergebnis = wert_von(lambda: [next(kette), next(kette)])
assert ergebnis == [("a/b", 0.0, 1.0), ("a/b", 1.0, 2.0)] and quelle.gelesen == 3, (
    f"Zwei next(...) auf spruenge(passend(Messprotokoll(quelle), 'a/+'), 0.5) ergeben {ergebnis!r} nach "
    f"{quelle.gelesen} gelesenen Zeilen; erwartet war [('a/b', 0.0, 1.0), ('a/b', 1.0, 2.0)] nach 3 Zeilen."
)

# Viele zufällige Protokolle, jede Stufe einzeln und alles zusammen
zufall = Zufall(4039)
for runde in range(200):
    zeilen = [zufallszeile(zufall) for _ in range(zufall.randint(0, 12))]
    erwartet_tupel = vergleich_tupel(zeilen)
    ergebnis = wert_von(lambda: list(Messprotokoll(zeilen)))
    assert ergebnis == erwartet_tupel, f"list(Messprotokoll({zeilen!r}))\n  ergibt   {ergebnis!r}\n  erwartet {erwartet_tupel!r}"
    muster = zufall.choice(["a/+/temp", "+/x/temp", "a/x/+", "+/+/+", "a", "+", "a/x/kopf/temp", "+/+/+/+"])
    erwartet_passend = [(t, w) for t, w in erwartet_tupel if vergleich_passt(t, muster)]
    ergebnis = wert_von(lambda: list(passend(erwartet_tupel, muster)))
    assert ergebnis == erwartet_passend, f"list(passend({erwartet_tupel!r}, {muster!r}))\n  ergibt   {ergebnis!r}\n  erwartet {erwartet_passend!r}"
    schwelle = zufall.choice([0, 1, 3, zufall.randint(0, 1000000)])
    erwartet_spruenge = vergleich_spruenge(erwartet_tupel, schwelle)
    ergebnis = wert_von(lambda: list(spruenge(erwartet_tupel, schwelle)))
    assert ergebnis == erwartet_spruenge, f"list(spruenge({erwartet_tupel!r}, {schwelle}))\n  ergibt   {ergebnis!r}\n  erwartet {erwartet_spruenge!r}"
    erwartet_erster = (vergleich_spruenge(erwartet_passend, schwelle) or [None])[0]
    ergebnis = wert_von(lambda: erster_sprung(Messprotokoll(zeilen), muster, schwelle))
    assert ergebnis == erwartet_erster, f"erster_sprung(Messprotokoll({zeilen!r}), {muster!r}, {schwelle}) ergibt {ergebnis!r}, erwartet war {erwartet_erster!r}."

# Obere Grenze: 100 000 Zeilen ohne Sprung
quelle = Zaehlquelle(lambda nummer: f"h/p{nummer % 50}/temp {nummer % 3}", laenge=100000)
ergebnis = wert_von(lambda: erster_sprung(Messprotokoll(quelle), "h/+/temp", 2))
assert ergebnis is None and quelle.gelesen == 100000, (
    f"Bei 100 000 Zeilen ohne Sprung ergibt erster_sprung {ergebnis!r} nach {quelle.gelesen} Zeilen, erwartet war None nach 100 000."
)
