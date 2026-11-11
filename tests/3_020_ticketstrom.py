# Automatisch erzeugt aus lehrkraft/muster/3_020_ticketstrom.py - nicht von Hand ändern.
# vorlage-hash: dc832d8e8461ff74
# text-hash: ccf497dccaf07597
# thema: kontrollfluss
# inhalt: iter() und next()

import ast
import inspect
import textwrap


class Strom:
    """Ein Iterator, der mitzählt, wie oft next() aufgerufen wurde; kennt weder len() noch Indizes."""

    def __init__(self, werte):
        """Merkt sich die Werte und fängt vorn an."""
        self._werte = list(werte)
        self._position = 0
        self.abgeholt = 0

    def __iter__(self):
        """Ein Iterator gibt bei iter() sich selbst zurück."""
        return self

    def __next__(self):
        """Liefert den nächsten Wert oder löst StopIteration aus."""
        if self._position >= len(self._werte):
            raise StopIteration
        self._position = self._position + 1
        self.abgeholt = self.abgeholt + 1
        return self._werte[self._position - 1]


def bauweise(funktion):
    """Gibt zurück, ob die Funktion for, sum() und next() benutzt."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return True, True, False
    mit_for = False
    mit_sum = False
    mit_next = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, (ast.For, ast.comprehension)):
            mit_for = True
        if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Name):
            mit_sum = mit_sum or knoten.func.id == "sum"
            mit_next = mit_next or knoten.func.id == "next"
    return mit_for, mit_sum, mit_next


# Das Beispiel aus der Aufgabe: Pakete zu zwei Tickets
strom = iter(["T-1", "T-2", "T-3", "T-4", "T-5"])
try:
    pakete = [naechste_tickets(strom, 2) for _ in range(4)]
except StopIteration:
    pakete = "StopIteration (nicht abgefangen)"
erwartet = [["T-1", "T-2"], ["T-3", "T-4"], ["T-5"], []]
assert pakete == erwartet, (
    f"Viermal naechste_tickets(strom, 2) ergibt {pakete!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Holen Sie mit next(strom) ein Ticket nach dem anderen und fangen Sie StopIteration ab, "
    "wenn der Strom leer ist."
)

# Es geht kein Ticket verloren: next() wird genau so oft aufgerufen wie Tickets zurückkommen
strom = Strom(["A", "B", "C", "D", "E", "F", "G"])
erstes = naechste_tickets(strom, 3)
abgeholt = strom.abgeholt
zweites = naechste_tickets(strom, 3)
assert (erstes, abgeholt, zweites) == (["A", "B", "C"], 3, ["D", "E", "F"]), (
    f"Bei einem Strom mit A bis G liefert naechste_tickets(strom, 3) {erstes!r} und ruft dafür {abgeholt}-mal next() auf, "
    f"das zweite Paket ist {zweites!r}; erwartet waren ['A', 'B', 'C'], 3 Aufrufe und ['D', 'E', 'F'].\n"
    "Tipp: Prüfen Sie, ob das Paket schon voll ist, bevor Sie next() aufrufen, nicht danach; "
    "sonst ist das nächste Ticket abgeholt und verloren."
)

# anzahl 0 holt nichts ab
strom = Strom(["A", "B"])
ergebnis = naechste_tickets(strom, 0)
assert ergebnis == [] and strom.abgeholt == 0 and naechste_tickets(strom, 5) == ["A", "B"], (
    f"naechste_tickets(strom, 0) ergibt {ergebnis!r} und ruft {strom.abgeholt}-mal next() auf; erwartet waren [] "
    "ohne einen Aufruf, und danach müssen beide Tickets noch im Strom sein."
)

# Ein leerer Strom und ein Strom mit genau anzahl Tickets
for werte, anzahl in [([], 3), ([], 0), (["X"], 1), (["X", "Y"], 2)]:
    ergebnis = naechste_tickets(Strom(werte), anzahl)
    assert ergebnis == werte, f"naechste_tickets mit einem Strom aus {werte} und anzahl {anzahl} ergibt {ergebnis!r}, erwartet war {werte!r}."

# Auch andere Iteratoren funktionieren
strom = map(str.upper, ["t-7", "t-8", "t-9"])
ergebnis = (naechste_tickets(strom, 1), naechste_tickets(strom, 5))
assert ergebnis == (["T-7"], ["T-8", "T-9"]), (
    f"Mit dem Iterator map(str.upper, ['t-7', 't-8', 't-9']) ergeben naechste_tickets(strom, 1) und "
    f"naechste_tickets(strom, 5) {ergebnis!r}, erwartet war (['T-7'], ['T-8', 'T-9']).\n"
    "Tipp: Ein Iterator hat weder len() noch Indizes; benutzen Sie nur next()."
)

# gesamtdauer aus dem Beispiel und mit anderen Durchlaufbaren
for dauern, beschreibung, erwartet in [
    ([15, 40, 5], "[15, 40, 5]", 60),
    ((7,), "(7,)", 7),
    ([], "[]", 0),
    (range(1, 101), "range(1, 101)", 5050),
    (iter([10**6, 0, 10**6]), "iter([10**6, 0, 10**6])", 2 * 10**6),
    (Strom([3, 4]), "einem Iterator mit 3 und 4", 7),
]:
    ergebnis = gesamtdauer(dauern)
    assert ergebnis == erwartet, (
        f"gesamtdauer({beschreibung}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Holen Sie sich zuerst mit iter(dauern) einen Iterator und rufen Sie next() auf ihm auf; "
        "next() auf einer Liste geht nicht."
    )

# gesamtdauer benutzt next(), aber weder for noch sum()
mit_for, mit_sum, mit_next = bauweise(gesamtdauer)
assert mit_next and not mit_for and not mit_sum, (
    "gesamtdauer soll mit iter() und next() in einer while-Schleife arbeiten, ohne for und ohne sum(); "
    f"gefunden: next() {'ja' if mit_next else 'nein'}, for {'ja' if mit_for else 'nein'}, sum() {'ja' if mit_sum else 'nein'}."
)

# naechste_tickets benutzt next()
mit_for, mit_sum, mit_next = bauweise(naechste_tickets)
assert mit_next, "naechste_tickets soll die Tickets mit next(strom) abholen."


def kopiert_beim_anhaengen(funktion):
    """Gibt zurück, ob die Funktion mit liste + [...] oder insert anhängt (beides kostet O(Länge) je Ticket)."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.BinOp) and isinstance(knoten.op, ast.Add):
            if isinstance(knoten.left, ast.List) or isinstance(knoten.right, ast.List):
                return True
        if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute) and knoten.func.attr == "insert":
            return True
    return False


# naechste_tickets hängt mit append an, ohne das Paket jedes Mal zu kopieren
assert not kopiert_beim_anhaengen(naechste_tickets), (
    "naechste_tickets baut das Paket mit liste + [ticket] oder insert auf. Beides kopiert bzw. verschiebt bei jedem "
    "Ticket das ganze Paket, zusammen O(anzahl²) statt O(anzahl).\n"
    "Tipp: paket.append(ticket) hängt in O(1) an."
)


# Vergleichslösung mit einer Liste und Slicing
def pakete_von_hand(werte, groessen):
    """Schneidet die Pakete der Reihe nach aus der Liste aus."""
    ergebnis = []
    anfang = 0
    for groesse in groessen:
        ergebnis.append(werte[anfang : anfang + groesse])
        anfang = min(len(werte), anfang + groesse)
    return ergebnis


# 300 zufällige Ströme und Paketgrößen
zufall = Zufall(3020)
for _ in range(300):
    werte = [f"T-{nummer}" for nummer in range(zufall.randint(0, 15))]
    groessen = [zufall.randint(0, 5) for _ in range(zufall.randint(1, 6))]
    strom = Strom(werte)
    ergebnis = [naechste_tickets(strom, groesse) for groesse in groessen]
    erwartet = pakete_von_hand(werte, groessen)
    assert ergebnis == erwartet, (
        f"Ein Strom mit {len(werte)} Tickets in Paketen der Größen {groessen} ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )
    dauern = [zufall.randint(0, 10**6) for _ in range(zufall.randint(0, 10))]
    ergebnis = gesamtdauer(Strom(dauern))
    assert ergebnis == sum(dauern), f"gesamtdauer mit einem Iterator über {dauern} ergibt {ergebnis!r}, erwartet war {sum(dauern)}."

# An der oberen Grenze: 100 000 Tickets in einem Paket, Schritte zählen
werte = [f"T-{nummer}" for nummer in range(100000)]
strom = Strom(werte)
paket, schritte_gross = zaehle_schritte(naechste_tickets, strom, 100000)
_, schritte_klein = zaehle_schritte(naechste_tickets, Strom(werte[:25000]), 25000)
assert paket == werte and naechste_tickets(strom, 1) == [], (
    f"naechste_tickets mit 100 000 Tickets und anzahl 100 000 liefert {len(paket)} Tickets, "
    f"die ersten {paket[:2]}; erwartet waren alle 100 000 und danach ein leerer Strom."
)

# naechste_tickets braucht O(anzahl) Schritte
assert schritte_gross <= 6 * schritte_klein + 100, (
    f"naechste_tickets braucht für 25 000 Tickets {schritte_klein} und für 100 000 Tickets {schritte_gross} Schritte; "
    "bei O(anzahl) wären es etwa viermal so viele.\nTipp: Holen Sie jedes Ticket genau einmal mit next() und hängen "
    "Sie es mit append an; gehen Sie das Paket nicht in einer zweiten Schleife durch."
)

# gesamtdauer an der oberen Grenze
dauern = [(nummer * 7919) % (10**6 + 1) for nummer in range(100000)]
ergebnis = gesamtdauer(iter(dauern))
assert ergebnis == sum(dauern), f"gesamtdauer mit 100 000 Werten ergibt {ergebnis!r}, erwartet war {sum(dauern)}."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['T-1', 'T-2']\n['T-3', 'T-4']\n['T-5']\n[]\n60"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
