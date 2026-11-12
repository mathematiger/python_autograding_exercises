# Automatisch erzeugt aus lehrkraft/muster/3_023_mitschnitt.py - nicht von Hand ändern.
# vorlage-hash: adf03b92ef3f0ef3
# text-hash: 1f3fafbc4393aabf
# thema: kontrollfluss
# inhalt: Generator-Ausdrücke

import ast
import inspect
import textwrap


def bauweise(funktion):
    """Gibt zurück, ob die Funktion einen Generator-Ausdruck und ob sie eine Schleife oder Zwischenliste enthält."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return False, False
    mit_generator = False
    mit_liste = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.GeneratorExp):
            mit_generator = True
        if isinstance(knoten, (ast.For, ast.While, ast.ListComp, ast.SetComp, ast.DictComp)):
            mit_liste = True
        if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Name) and knoten.func.id in ("list", "tuple", "set", "sorted"):
            mit_liste = True
    return mit_generator, mit_liste


class Paketstrom:
    """Ein Iterator über Pakete, der mitzählt, wie viele Pakete schon abgeholt wurden; kein len()."""

    def __init__(self, pakete):
        """Merkt sich die Pakete."""
        self._pakete = list(pakete)
        self.abgeholt = 0

    def __iter__(self):
        """Ein Iterator gibt bei iter() sich selbst zurück."""
        return self

    def __next__(self):
        """Liefert das nächste Paket oder löst StopIteration aus."""
        if self.abgeholt >= len(self._pakete):
            raise StopIteration
        self.abgeholt = self.abgeholt + 1
        return self._pakete[self.abgeholt - 1]


mitschnitt = [(443, 1500), (53, 80), (443, 900), (22, 120)]

# datenmenge aus dem Beispiel
ergebnis = datenmenge(mitschnitt, 443)
assert ergebnis == 2400, (
    f"datenmenge(mitschnitt, 443) ergibt {ergebnis!r}, erwartet war 2400.\n"
    "Tipp: Summieren Sie nur die Längen der Pakete, deren Zielport gleich port ist."
)

# Andere Ports (nicht fest hinschreiben!)
for port, erwartet in [(53, 80), (22, 120), (80, 0), (0, 0)]:
    ergebnis = datenmenge(mitschnitt, port)
    assert ergebnis == erwartet, f"datenmenge(mitschnitt, {port}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# zu_gross aus dem Beispiel: genau die MTU ist noch nicht zu groß
ergebnis = (zu_gross(mitschnitt, 1500), zu_gross(mitschnitt, 1400), zu_gross(mitschnitt, 1499))
assert ergebnis == (False, True, True), (
    f"zu_gross(mitschnitt, …) mit mtu 1500, 1400 und 1499 ergibt {ergebnis!r}, erwartet war (False, True, True).\n"
    "Tipp: „länger als mtu“ heißt laenge > mtu; ein Paket mit genau 1500 Byte passt bei mtu 1500 noch."
)

# nur_freigegeben aus dem Beispiel
ergebnis = (nur_freigegeben(mitschnitt, {53, 443}), nur_freigegeben(mitschnitt, {22, 53, 443}))
assert ergebnis == (False, True), (
    f"nur_freigegeben(mitschnitt, {{53, 443}}) und nur_freigegeben(mitschnitt, {{22, 53, 443}}) ergeben {ergebnis!r}, "
    "erwartet war (False, True).\nTipp: Das Paket an Port 22 ist im ersten Fall nicht freigegeben."
)

# Weitere Freigaben und Ränder der Ports
for pakete, freigaben, erwartet in [
    ([(0, 10), (65535, 10)], {0, 65535}, True),
    ([(0, 10), (65535, 10)], {0}, False),
    ([(80, 10)], set(), False),
    ([(80, 10), (80, 20)], {80, 443}, True),
    ([(81, 10)], {80, 8080}, False),
]:
    ergebnis = nur_freigegeben(pakete, freigaben)
    assert ergebnis == erwartet, f"nur_freigegeben({pakete}, {freigaben}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ränder der Längen und der MTU
for pakete, mtu, erwartet in [([(1, 65535)], 65535, False), ([(1, 69)], 68, True), ([(1, 68)], 68, False), ([(5, 1)], 68, False)]:
    ergebnis = zu_gross(pakete, mtu)
    assert ergebnis == erwartet, f"zu_gross({pakete}, {mtu}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ein leerer Mitschnitt
ergebnis = (datenmenge([], 443), zu_gross([], 1500), nur_freigegeben([], set()))
assert ergebnis == (0, False, True), (
    f"Mit einem leeren Mitschnitt ergeben datenmenge, zu_gross und nur_freigegeben {ergebnis!r}, "
    "erwartet war (0, False, True).\nTipp: Ohne Pakete ist kein Paket zu groß, und alle (keine) Pakete sind freigegeben."
)

# Die Ergebnisse sind Zahlen und Wahrheitswerte
arten = [type(datenmenge(mitschnitt, 443)), type(zu_gross(mitschnitt, 1500)), type(nur_freigegeben(mitschnitt, {443}))]
assert arten == [int, bool, bool], (
    f"Die drei Funktionen geben {[art.__name__ for art in arten]} zurück, erwartet waren int, bool und bool."
)

# Auch ein Iterator als Mitschnitt funktioniert
ergebnis = (
    datenmenge(iter(mitschnitt), 443),
    zu_gross(map(tuple, mitschnitt), 1000),
    nur_freigegeben(reversed(mitschnitt), {22, 53, 443}),
)
assert ergebnis == (2400, True, True), (
    f"Mit Iteratoren über den Mitschnitt ergeben datenmenge(…, 443), zu_gross(…, 1000) und "
    f"nur_freigegeben(…, {{22, 53, 443}}) {ergebnis!r}, erwartet war (2400, True, True).\n"
    "Tipp: Ein Iterator hat weder len() noch Indizes und kann nur einmal durchlaufen werden."
)

# zu_gross hört beim ersten zu großen Paket auf
strom = Paketstrom([(443, 100), (443, 9000)] + [(443, 100)] * 1000)
ergebnis = zu_gross(strom, 1500)
assert ergebnis is True and strom.abgeholt == 2, (
    f"zu_gross mit einem Strom, dessen zweites Paket 9000 Byte lang ist, ergibt {ergebnis!r} und holt "
    f"{strom.abgeholt} von 1002 Paketen ab; erwartet waren True nach 2 Paketen.\n"
    "Tipp: any(… for …) mit runden Klammern hört beim ersten wahren Wert auf; any([…]) mit eckigen Klammern "
    "baut zuerst die ganze Liste und holt dafür alle Pakete ab."
)

# nur_freigegeben hört beim ersten nicht freigegebenen Paket auf
strom = Paketstrom([(443, 100), (53, 80), (23, 60)] + [(443, 100)] * 1000)
ergebnis = nur_freigegeben(strom, {53, 443})
assert ergebnis is False and strom.abgeholt == 3, (
    f"nur_freigegeben mit einem Strom, dessen drittes Paket an Port 23 geht, ergibt {ergebnis!r} und holt "
    f"{strom.abgeholt} von 1003 Paketen ab; erwartet waren False nach 3 Paketen.\n"
    "Tipp: all(… for …) mit runden Klammern hört beim ersten falschen Wert auf; eine Zwischenliste holt alle Pakete ab."
)

# datenmenge holt jedes Paket genau einmal ab
strom = Paketstrom(mitschnitt)
ergebnis = datenmenge(strom, 53)
assert ergebnis == 80 and strom.abgeholt == 4, (
    f"datenmenge mit einem Strom aus den vier Beispielpaketen ergibt für Port 53 {ergebnis!r} und holt "
    f"{strom.abgeholt} Pakete ab; erwartet waren 80 und 4 Pakete."
)

# Jede Funktion benutzt einen Generator-Ausdruck, keine Schleife und keine Zwischenliste
for funktion in [datenmenge, zu_gross, nur_freigegeben]:
    mit_generator, mit_liste = bauweise(funktion)
    assert mit_generator and not mit_liste, (
        f"{funktion.__name__} soll mit einem Generator-Ausdruck (… for … in …) in sum, any oder all arbeiten, ohne "
        "for-/while-Anweisung und ohne Liste, Menge oder Comprehension in eckigen oder geschweiften Klammern; "
        f"gefunden: Generator-Ausdruck {'ja' if mit_generator else 'nein'}, Schleife oder Zwischenliste "
        f"{'ja' if mit_liste else 'nein'}."
    )


# Vergleichslösung mit gewöhnlichen Schleifen über die Indizes
def von_hand(pakete, port, mtu, freigaben):
    """Berechnet alle drei Ergebnisse mit einer Schleife über die Indizes."""
    summe = 0
    gross = False
    erlaubt = True
    for index in range(len(pakete)):
        ziel = pakete[index][0]
        laenge = pakete[index][1]
        if ziel == port:
            summe = summe + laenge
        if laenge > mtu:
            gross = True
        if ziel not in freigaben:
            erlaubt = False
    return summe, gross, erlaubt


# 300 zufällige Mitschnitte, als Liste und als Iterator
zufall = Zufall(3023)
PORTS = [22, 53, 80, 443, 8080]
for _ in range(300):
    pakete = [(zufall.choice(PORTS), zufall.choice([1, 60, 1499, 1500, 1501, 9000])) for _ in range(zufall.randint(0, 8))]
    port = zufall.choice(PORTS)
    mtu = zufall.choice([68, 1500, 9000])
    freigaben = set(zufall.sample(PORTS, zufall.randint(0, 5)))
    erwartet = von_hand(pakete, port, mtu, freigaben)
    ergebnis = (datenmenge(Paketstrom(pakete), port), zu_gross(iter(pakete), mtu), nur_freigegeben(Paketstrom(pakete), freigaben))
    assert ergebnis == erwartet, (
        f"Mit pakete = {pakete} ergeben datenmenge(…, {port}), zu_gross(…, {mtu}) und "
        f"nur_freigegeben(…, {freigaben}) {ergebnis!r}, erwartet war {erwartet!r}."
    )

# An der oberen Grenze: 100 000 Pakete als Iterator
pakete = [((nummer * 7) % 65536, (nummer * 37) % 65535 + 1) for nummer in range(100000)]
freigaben = set(range(65536)) - {pakete[-1][0]}
erwartet = von_hand(pakete, 443, 65535, freigaben)
ergebnis = (datenmenge(iter(pakete), 443), zu_gross(iter(pakete), 65535), nur_freigegeben(iter(pakete), freigaben))
assert ergebnis == erwartet, f"Bei 100 000 Paketen ergeben die drei Funktionen {ergebnis!r}, erwartet war {erwartet!r}."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "2400\nFalse True\nFalse True"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
