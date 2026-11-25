# Automatisch erzeugt aus lehrkraft/muster/5_057_gatewayspeicher.py - nicht von Hand ändern.
# vorlage-hash: 7c668715e96b28a7
# text-hash: 5372b830fb75cf61
# thema: kontrollfluss
# inhalt: Generator-Pipelines und Speicher

import math
import tracemalloc


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


class Strom:
    """Ein Iterator, der zählt, wie viele Werte abgeholt wurden, und nach grenze Werten abbricht (statt ewig zu laufen)."""

    def __init__(self, werte, grenze):
        """Merkt sich den Iterator über werte und wie viele Werte höchstens abgeholt werden dürfen."""
        self.iterator = iter(werte)
        self.abgeholt = 0
        self.grenze = grenze

    def __iter__(self):
        """Ein Iterator ist sein eigener Iterator."""
        return self

    def __next__(self):
        """Liefert den nächsten Wert und zählt mit."""
        if self.abgeholt >= self.grenze:
            raise RuntimeError(
                f"Ihre Funktion hat schon {self.grenze} Werte aus einem endlosen Strom gelesen und will noch mehr; "
                "sie versucht vermutlich, den ganzen Strom zu sammeln"
            )
        wert = next(self.iterator)
        self.abgeholt += 1
        return wert


def speicherspitze(aufruf):
    """Führt aufruf() aus und gibt (Ergebnis, Fehlertext, höchsten Speicherbedarf in Byte) zurück."""
    tracemalloc.start()
    try:
        ergebnis, fehler = rufe(aufruf)
        _, spitze = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return ergebnis, fehler, spitze


def temperaturen(anzahl):
    """Ein Generator mit anzahl Temperaturen, die erst beim Abholen entstehen."""
    return (20 + (nummer * 37 % 101) / 10 for nummer in range(anzahl))


def messdaten(anzahl):
    """Ein Generator mit anzahl Messungen (sekunde, wert), etwa alle 2 Sekunden eine."""
    return ((nummer * 2, 20 + (nummer * 37 % 101) / 10) for nummer in range(anzahl))


def gleich(a, b):
    """Vergleicht Tupel und Listen mit Kommazahlen bis auf Rundungsfehler."""
    if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)):
        return type(a) is type(b) and len(a) == len(b) and all(gleich(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
    return a == b


def vergleich_minuten(messungen):
    """Vergleichslösung: sammelt alle Messungen je Minute in einem Dictionary."""
    je_minute = {}
    for sekunde, wert in messungen:
        je_minute.setdefault(sekunde // 60, []).append(wert)
    return [(minute, sum(werte) / len(werte)) for minute, werte in je_minute.items()]


GRENZE = 200_000

# bloecke: das Beispiel
ergebnis, fehler = rufe(lambda: list(bloecke(range(7), 3)))
assert ergebnis == [[0, 1, 2], [3, 4, 5], [6]], (
    f"list(bloecke(range(7), 3)) ergibt {ergebnis!r}, erwartet war [[0, 1, 2], [3, 4, 5], [6]].\n"
    "Tipp: it = iter(werte), dann immer wieder block = list(itertools.islice(it, groesse)), bis block leer ist."
    + absturz(fehler)
)

# bloecke: geht genau auf, kein leerer Block am Ende
ergebnis, fehler = rufe(lambda: list(bloecke(range(6), 2)))
assert ergebnis == [[0, 1], [2, 3], [4, 5]], (
    f"list(bloecke(range(6), 2)) ergibt {ergebnis!r}, erwartet war [[0, 1], [2, 3], [4, 5]] ohne leeren Block."
    + absturz(fehler)
)

# bloecke: funktioniert mit einem Generator, der nur einmal läuft
ergebnis, fehler = rufe(lambda: list(bloecke((wert * 10 for wert in range(5)), 2)))
assert ergebnis == [[0, 10], [20, 30], [40]], (
    f"bloecke mit einem Generator ergibt {ergebnis!r}, erwartet war [[0, 10], [20, 30], [40]].\n"
    "Tipp: Holen Sie sich einmal am Anfang it = iter(werte); ein neues iter() oder Indizes gehen bei Generatoren nicht."
    + absturz(fehler)
)

# bloecke: Blockgröße 1 und leere Eingabe
ergebnis, fehler = rufe(lambda: (list(bloecke("abc", 1)), list(bloecke([], 4)), list(bloecke([7], 10))))
assert ergebnis == ([["a"], ["b"], ["c"]], [], [[7]]), (
    f"bloecke('abc', 1), bloecke([], 4) und bloecke([7], 10) ergeben {ergebnis!r}, erwartet war "
    "([['a'], ['b'], ['c']], [], [[7]])." + absturz(fehler)
)

# bloecke: liest erst weiter, wenn der nächste Block abgeholt wird
strom = Strom(itertools.count(), 10_000)
ergebnis, fehler = rufe(lambda: next(bloecke(strom, 500)))
assert ergebnis == list(range(500)) and strom.abgeholt == 500, (
    f"next(bloecke(unendlicher_strom, 500)) ergibt {str(ergebnis)[:60]} und holt {strom.abgeholt} Werte ab; erwartet "
    "waren die ersten 500 Werte, und nur diese 500 abgeholt.\nTipp: Bauen Sie bloecke als Generator mit yield und "
    "sammeln Sie nie den ganzen Strom." + absturz(fehler)
)

# bloecke: wenig Speicher bei 100000 Werten
ergebnis, fehler, spitze = speicherspitze(lambda: sum(len(block) for block in bloecke(temperaturen(100_000), 100)))
assert ergebnis == 100_000 and spitze < GRENZE, (
    f"bloecke(… 100000 Werte …, 100) liefert zusammen {ergebnis!r} Werte und belegt in der Spitze {spitze} Byte; "
    f"erwartet waren 100000 Werte mit weniger als {GRENZE} Byte. Sammeln Sie nicht alle Werte, sondern nur den "
    "aktuellen Block." + absturz(fehler)
)

# kennzahlen: das Beispiel
ergebnis, fehler = rufe(lambda: kennzahlen([21.5, 19.0, 23.5]))
assert gleich(ergebnis, (3, 19.0, 23.5, 64 / 3)), (
    f"kennzahlen([21.5, 19.0, 23.5]) ergibt {ergebnis!r}, erwartet war (3, 19.0, 23.5, 21.333333333333332)."
    + absturz(fehler)
)

# kennzahlen: andere Werte (nicht fest hinschreiben!)
ergebnis, fehler = rufe(lambda: kennzahlen([5, -3.5, 12, 0]))
assert gleich(ergebnis, (4, -3.5, 12, 3.375)), f"kennzahlen([5, -3.5, 12, 0]) ergibt {ergebnis!r}, erwartet war (4, -3.5, 12, 3.375)." + absturz(fehler)

# kennzahlen: geht den Strom nur einmal durch (ein Generator ist danach verbraucht)
ergebnis, fehler = rufe(lambda: kennzahlen(wert for wert in [4.0, 8.0, 6.0]))
assert gleich(ergebnis, (3, 4.0, 8.0, 6.0)), (
    f"kennzahlen eines Generators mit 4.0, 8.0, 6.0 ergibt {ergebnis!r}, erwartet war (3, 4.0, 8.0, 6.0).\n"
    "Tipp: len, min, max und sum nacheinander gehen bei einem Generator nicht, er ist nach dem ersten Durchlauf "
    "leer. Rechnen Sie alles in einer Schleife mit." + absturz(fehler)
)

# kennzahlen: ein einziger Wert
ergebnis, fehler = rufe(lambda: kennzahlen(iter([-100])))
assert gleich(ergebnis, (1, -100, -100, -100)), f"kennzahlen eines Stroms mit nur -100 ergibt {ergebnis!r}, erwartet war (1, -100, -100, -100.0)." + absturz(fehler)

# kennzahlen: alle Werte negativ (Minimum und Maximum nicht mit 0 beginnen)
ergebnis, fehler = rufe(lambda: kennzahlen(iter([-5, -2, -9])))
assert gleich(ergebnis, (3, -9, -2, -16 / 3)), (
    f"kennzahlen von -5, -2, -9 ergibt {ergebnis!r}, erwartet war (3, -9, -2, {-16 / 3!r}).\n"
    "Tipp: Beginnen Sie Minimum und Maximum nicht mit 0, sondern mit dem ersten Wert (oder None)." + absturz(fehler)
)

# kennzahlen: leere Eingabe ergibt None
ergebnis, fehler = rufe(lambda: (kennzahlen([]), kennzahlen(iter([]))))
assert fehler is None and ergebnis == (None, None), (
    f"kennzahlen([]) und kennzahlen(iter([])) ergeben {ergebnis!r}, erwartet war (None, None)." + absturz(fehler)
)

# kennzahlen: wenig Speicher bei 100000 Werten
ergebnis, fehler, spitze = speicherspitze(lambda: kennzahlen(temperaturen(100_000)))
erwartet = (100_000, 20.0, 30.0, sum(temperaturen(100_000)) / 100_000)
assert gleich(ergebnis, erwartet) and spitze < GRENZE, (
    f"kennzahlen von 100000 Werten ergibt {ergebnis!r} und belegt in der Spitze {spitze} Byte; erwartet war "
    f"{erwartet!r} mit weniger als {GRENZE} Byte.\nTipp: Kein list(werte); merken Sie sich nur Anzahl, Summe, Minimum "
    "und Maximum bisher." + absturz(fehler)
)

# minutenmittel: das Beispiel
messungen = [(0, 20.0), (30, 22.0), (61, 21.0), (185, 19.5)]
ergebnis, fehler = rufe(lambda: list(minutenmittel(messungen)))
assert gleich(ergebnis, [(0, 21.0), (1, 21.0), (3, 19.5)]), (
    f"list(minutenmittel({messungen})) ergibt {ergebnis!r}, erwartet war [(0, 21.0), (1, 21.0), (3, 19.5)].\n"
    "Tipp: itertools.groupby mit key=lambda m: m[0] // 60 liefert die Messungen jeder Minute; Minute 2 hat keine "
    "Messung und fehlt." + absturz(fehler)
)

# minutenmittel: andere Messungen (nicht fest hinschreiben!)
messungen = [(120, 10.0), (150, 11.0), (179, 15.0), (180, 30.0), (180, 31.0), (600, -4.0)]
ergebnis, fehler = rufe(lambda: list(minutenmittel(iter(messungen))))
assert gleich(ergebnis, vergleich_minuten(messungen)), (
    f"list(minutenmittel({messungen})) ergibt {ergebnis!r}, erwartet war {vergleich_minuten(messungen)!r}."
    + absturz(fehler)
)

# minutenmittel: Sekunde 59 gehört noch zu Minute 0, Sekunde 60 zu Minute 1
messungen = [(59, 1.0), (60, 3.0)]
ergebnis, fehler = rufe(lambda: list(minutenmittel(messungen)))
assert gleich(ergebnis, [(0, 1.0), (1, 3.0)]), f"list(minutenmittel({messungen})) ergibt {ergebnis!r}, erwartet war [(0, 1.0), (1, 3.0)]." + absturz(fehler)

# minutenmittel: keine Messungen
ergebnis, fehler = rufe(lambda: list(minutenmittel(iter([]))))
assert ergebnis == [], f"list(minutenmittel(iter([]))) ergibt {ergebnis!r}, erwartet war []." + absturz(fehler)

# minutenmittel ist ein Generator und liefert eine Minute, sobald sie vorbei ist
strom = Strom(messdaten(10**9), 10_000)
ergebnis, fehler = rufe(lambda: next(minutenmittel(strom)))
assert gleich(ergebnis, (0, vergleich_minuten(messdaten(30))[0][1])) and strom.abgeholt <= 31, (
    f"next(minutenmittel(…)) bei einem endlosen Strom ergibt {ergebnis!r} und holt {strom.abgeholt} Messungen ab; "
    "erwartet war die Minute 0 nach höchstens 31 Messungen (30 aus Minute 0 und die erste aus Minute 1)."
    + absturz(fehler)
)

zufall = Zufall(5057)

# Viele zufällige Ströme im Vergleich
for _ in range(100):
    sekunde = zufall.randint(0, 300)
    messungen = []
    for _ in range(zufall.randint(0, 40)):
        sekunde += zufall.choice([0, 1, 5, 30, 61, 200])
        messungen.append((sekunde, zufall.randint(-1000, 2000) / 10))
    werte = [wert for _, wert in messungen]
    groesse = zufall.randint(1, 7)
    ergebnis, fehler = rufe(
        lambda: (
            list(bloecke(iter(werte), groesse)), kennzahlen(iter(werte)), list(minutenmittel(iter(messungen))),
        )
    )
    erwartet = (
        [werte[stelle:stelle + groesse] for stelle in range(0, len(werte), groesse)],
        (len(werte), min(werte), max(werte), sum(werte) / len(werte)) if werte else None,
        vergleich_minuten(messungen),
    )
    assert gleich(ergebnis, erwartet), (
        f"Für die Messungen {messungen} ergeben bloecke(…, {groesse}), kennzahlen und minutenmittel\n{ergebnis!r},"
        f"\nerwartet war\n{erwartet!r}." + absturz(fehler)
    )

# Obere Grenze: die ganze Pipeline mit 100000 Messungen und wenig Speicher
def pipeline():
    """Bildet Minutenmittel, bündelt sie und zählt Blöcke und Minuten."""
    anzahl_bloecke = 0
    minuten = 0
    for block in bloecke(minutenmittel(messdaten(100_000)), 50):
        anzahl_bloecke += 1
        minuten += len(block)
    return anzahl_bloecke, minuten


ergebnis, fehler, spitze = speicherspitze(pipeline)
assert ergebnis == (67, 3334) and spitze < GRENZE, (
    f"Die Pipeline über 100000 Messungen ergibt {ergebnis!r} (Blöcke, Minuten) und belegt in der Spitze {spitze} "
    f"Byte; erwartet war (67, 3334) mit weniger als {GRENZE} Byte.\nTipp: minutenmittel darf die Messungen nicht "
    "sammeln, auch nicht je Minute in einem Dictionary aller Minuten." + absturz(fehler)
)
