# Automatisch erzeugt aus lehrkraft/muster/3_024_stromeffizienz.py - nicht von Hand ändern.
# vorlage-hash: 12a221129595b3da
# text-hash: db18343231883e60
# thema: kontrollfluss
# inhalt: Comprehensions und Generatoren

import ast
import inspect
import textwrap


def bauweise(funktion):
    """Gibt die Arten von Comprehensions in der Funktion zurück und ob sie eine for-/while-Anweisung enthält."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return set(), True
    arten = set()
    mit_schleife = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
            arten.add(type(knoten).__name__)
        if isinstance(knoten, (ast.For, ast.While)):
            mit_schleife = True
    return arten, mit_schleife


def ist_generator(objekt):
    """Gibt zurück, ob objekt ein Generator ist (Ergebnis einer Funktion mit yield)."""
    return type(objekt).__name__ == "generator"


class Zeilenstrom:
    """Ein Iterator über Textzeilen, der mitzählt, wie viele Zeilen schon abgeholt wurden; kein len()."""

    def __init__(self, zeilen):
        """Merkt sich die Zeilen."""
        self._zeilen = list(zeilen)
        self.abgeholt = 0

    def __iter__(self):
        """Ein Iterator gibt bei iter() sich selbst zurück."""
        return self

    def __next__(self):
        """Liefert die nächste Zeile oder löst StopIteration aus."""
        if self.abgeholt >= len(self._zeilen):
            raise StopIteration
        self.abgeholt = self.abgeholt + 1
        return self._zeilen[self.abgeholt - 1]


def gleich(ergebnis, erwartet):
    """Vergleicht zwei Dictionaries mit PUE-Werten; Kommazahlen dürfen in der letzten Stelle abweichen."""
    if not isinstance(ergebnis, dict) or list(ergebnis.keys()) != list(erwartet.keys()):
        return False
    for stunde, wert in erwartet.items():
        if not isinstance(ergebnis[stunde], (int, float)) or abs(ergebnis[stunde] - wert) > 0.000001:
            return False
    return True


def beispiel():
    """Baut die Zeilen aus der Aufgabe neu."""
    return ["stunde;gesamt;it", "0;390;300", "1;-;290", "2;480;300", "3;300;200"]


# messungen aus dem Beispiel
ergebnis = list(messungen(beispiel()))
assert ergebnis == [(0, 390, 300), (2, 480, 300), (3, 300, 200)], (
    f"list(messungen(zeilen)) ergibt {ergebnis!r}, erwartet war [(0, 390, 300), (2, 480, 300), (3, 300, 200)].\n"
    'Tipp: Überspringen Sie die Kopfzeile, zerlegen Sie jede Zeile mit split(";") und wandeln Sie die Teile mit int() um.'
)

# messungen ist ein Generator
assert ist_generator(messungen(beispiel())), (
    f"messungen(zeilen) liefert ein Objekt vom Typ {type(messungen(beispiel())).__name__}, erwartet war ein Generator.\n"
    "Tipp: Liefern Sie jedes Tupel mit yield, statt eine Liste zurückzugeben."
)

# Gestörte Zähler in einer der beiden Spalten oder in beiden
zeilen = ["Stunde;Gesamt;IT", "5;-;100", "6;200;-", "7;-;-", "8;150;100"]
ergebnis = list(messungen(zeilen))
assert ergebnis == [(8, 150, 100)], (
    f"list(messungen({zeilen})) ergibt {ergebnis!r}, erwartet war [(8, 150, 100)].\n"
    'Tipp: Eine Zeile fällt weg, sobald gesamt oder it "-" ist.'
)

# Nur die Kopfzeile, und eine einzige Messung mit den Rändern
for zeilen, erwartet in [
    (["stunde;gesamt;it"], []),
    (["stunde;gesamt;it", "0;1;1"], [(0, 1, 1)]),
    (["stunde;gesamt;it", "1000000;1000000;1"], [(1000000, 1000000, 1)]),
]:
    ergebnis = list(messungen(zeilen))
    assert ergebnis == erwartet, f"list(messungen({zeilen})) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# messungen arbeitet mit einem Iterator und holt die Zeilen erst, wenn sie gebraucht werden
strom = Zeilenstrom(beispiel() + [f"{stunde};400;300" for stunde in range(4, 1000)])
werte = messungen(strom)
erstes = next(werte, None)
assert erstes == (0, 390, 300) and strom.abgeholt == 2, (
    f"Das erste Tupel von messungen für einen Zeilenstrom ist {erstes!r}, und dafür wurden {strom.abgeholt} von "
    "1000 Zeilen abgeholt; erwartet waren (0, 390, 300) nach 2 Zeilen (Kopfzeile und erste Messung).\n"
    "Tipp: Holen Sie die Kopfzeile mit next() ab und liefern Sie danach jedes Tupel sofort mit yield."
)

# pue_je_stunde aus dem Beispiel
ergebnis = pue_je_stunde(beispiel())
assert gleich(ergebnis, {0: 1.3, 2: 1.6, 3: 1.5}), (
    f"pue_je_stunde(zeilen) ergibt {ergebnis!r}, erwartet war {{0: 1.3, 2: 1.6, 3: 1.5}}.\n"
    "Tipp: Die PUE einer Stunde ist gesamt / it, gerundet mit round(…, 2); Stunden mit gestörtem Zähler fehlen."
)

# pue_je_stunde rundet und funktioniert mit einem Iterator
for zeilen, erwartet in [
    (iter(["stunde;gesamt;it", "4;1000;300", "9;7;7"]), {4: 3.33, 9: 1.0}),
    (iter(["stunde;gesamt;it", "0;5;3", "1;-;5", "2;1000000;1"]), {0: 1.67, 2: 1000000.0}),
    (iter(["stunde;gesamt;it"]), {}),
]:
    ergebnis = pue_je_stunde(zeilen)
    assert gleich(ergebnis, erwartet), f"pue_je_stunde mit einem Iterator ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# gesamt_pue aus dem Beispiel: Summe durch Summe, nicht der Mittelwert der Stundenwerte
ergebnis = gesamt_pue(beispiel())
assert ergebnis == 1.46, (
    f"gesamt_pue(zeilen) ergibt {ergebnis!r}, erwartet war 1.46 (1170 / 800).\n"
    "Tipp: Teilen Sie die Summe aller gesamt-Werte durch die Summe aller it-Werte; der Mittelwert "
    "der Stundenwerte 1.3, 1.6 und 1.5 wäre 1.47."
)

# gesamt_pue mit einem Iterator, der nur einmal durchlaufen werden kann
for zeilen, beschreibung, erwartet in [
    (iter(beispiel()), "iter(zeilen)", 1.46),
    (Zeilenstrom(["stunde;gesamt;it", "0;300;100", "1;-;100", "2;100;100"]), "einem Strom mit 300/100 und 100/100", 2.0),
    (iter(["stunde;gesamt;it", "7;1000000;1"]), "einer Messung 1000000/1", 1000000.0),
    (iter(["stunde;gesamt;it", "0;-;-", "3;5;4"]), "einer gültigen Messung 5/4", 1.25),
]:
    try:
        ergebnis = gesamt_pue(zeilen)
    except (ZeroDivisionError, ValueError, TypeError, RuntimeError) as fehler:
        ergebnis = f"{type(fehler).__name__}: {fehler}"
    assert ergebnis == erwartet, (
        f"gesamt_pue mit {beschreibung} ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Ein Iterator ist nach einem Durchlauf verbraucht. Sammeln Sie die Messungen einmal mit list(…), "
        "bevor Sie zwei Summen bilden."
    )

# kritische_stunden aus dem Beispiel und mit anderen Grenzen
pue = {0: 1.3, 2: 1.6, 3: 1.5}
for grenze, erwartet in [(1.45, [2, 3]), (1.0, [0, 2, 3]), (1.5, [2]), (1.6, []), (1.3, [2, 3]), (10.0, [])]:
    ergebnis = kritische_stunden(pue, grenze)
    assert ergebnis == erwartet, (
        f"kritische_stunden({pue}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: „größer als grenze“ heißt wert > grenze; genau die Grenze zählt nicht."
    )

# kritische_stunden ohne Stunden und in der Reihenfolge des Dictionarys
for pue, grenze, erwartet in [({}, 1.2, []), ({5: 2.0, 9: 1.0, 11: 3.5}, 1.0, [5, 11])]:
    ergebnis = kritische_stunden(pue, grenze)
    assert ergebnis == erwartet, f"kritische_stunden({pue}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# pue_je_stunde und gesamt_pue benutzen messungen genau einmal
_echte_messungen = messungen
aufrufe = []


def messungen(zeilen):
    """Zählt die Aufrufe und liefert dieselben Tupel wie die echte Funktion."""
    aufrufe.append(1)
    return _echte_messungen(zeilen)


ergebnis = (pue_je_stunde(["stunde;gesamt;it", "1;20;10"]), gesamt_pue(["stunde;gesamt;it", "1;30;10"]))
messungen = _echte_messungen
assert ergebnis == ({1: 2.0}, 3.0) and len(aufrufe) == 2, (
    f"pue_je_stunde und gesamt_pue ergeben {ergebnis!r} und rufen messungen zusammen {len(aufrufe)}-mal auf; "
    "erwartet waren ({1: 2.0}, 3.0) mit je einem Aufruf von messungen.\n"
    "Tipp: Zerlegen Sie die Zeilen nicht noch einmal selbst, sondern benutzen Sie messungen(zeilen) einmal."
)

# Die verlangten Sprachmittel
for funktion, art, name, beispiel_code in [
    (pue_je_stunde, "DictComp", "Dict Comprehension", "{stunde: … for …}"),
    (gesamt_pue, "GeneratorExp", "Generator-Ausdruck", "sum(… for …)"),
    (kritische_stunden, "ListComp", "List Comprehension", "[stunde for …]"),
]:
    arten, mit_schleife = bauweise(funktion)
    assert art in arten and not mit_schleife, (
        f"{funktion.__name__} soll mit {name} {beispiel_code} arbeiten, ohne for- oder while-Anweisung; "
        f"gefunden: {name} {'ja' if art in arten else 'nein'}, Schleife {'ja' if mit_schleife else 'nein'}."
    )


# Vergleichslösung: alles in einer Schleife über die Indizes, mit Zählern statt Comprehensions
def von_hand(zeilen, grenze):
    """Berechnet Messungen, Stundenwerte, Gesamtwert und kritische Stunden mit einer Schleife."""
    tupel = []
    stundenwerte = {}
    kritisch = []
    summe_gesamt = 0
    summe_it = 0
    for index in range(1, len(zeilen)):
        teile = zeilen[index].split(";")
        if "-" in teile:
            continue
        stunde, gesamt, it = int(teile[0]), int(teile[1]), int(teile[2])
        tupel.append((stunde, gesamt, it))
        stundenwerte[stunde] = round(gesamt / it, 2)
        if stundenwerte[stunde] > grenze:
            kritisch.append(stunde)
        summe_gesamt = summe_gesamt + gesamt
        summe_it = summe_it + it
    gesamtwert = round(summe_gesamt / summe_it, 2) if summe_it > 0 else None
    return tupel, stundenwerte, gesamtwert, kritisch


# 300 zufällige Exporte, als Liste und als Iterator
zufall = Zufall(3024)
for _ in range(300):
    stunden = sorted(zufall.sample(range(0, 10**6 + 1), zufall.randint(0, 8)))
    zeilen = ["stunde;gesamt;it"]
    for stunde in stunden:
        it = zufall.randint(1, 500)
        gesamt = zufall.randint(it, 2 * it)
        zeilen.append(f"{stunde};{zufall.choice([str(gesamt), str(gesamt), '-'])};{zufall.choice([str(it), str(it), '-'])}")
    grenze = zufall.choice([1.0, 1.25, 1.5, 2.0])
    tupel, stundenwerte, gesamtwert, kritisch = von_hand(zeilen, grenze)
    ergebnis = list(messungen(Zeilenstrom(zeilen)))
    assert ergebnis == tupel, f"list(messungen({zeilen})) ergibt {ergebnis!r}, erwartet war {tupel!r}."
    ergebnis = pue_je_stunde(Zeilenstrom(zeilen))
    assert gleich(ergebnis, stundenwerte), f"pue_je_stunde({zeilen}) ergibt {ergebnis!r}, erwartet war {stundenwerte!r}."
    ergebnis = kritische_stunden(stundenwerte, grenze)
    assert ergebnis == kritisch, f"kritische_stunden({stundenwerte}, {grenze}) ergibt {ergebnis!r}, erwartet war {kritisch!r}."
    if gesamtwert is not None:
        ergebnis = gesamt_pue(Zeilenstrom(zeilen))
        assert ergebnis == gesamtwert, f"gesamt_pue({zeilen}) ergibt {ergebnis!r}, erwartet war {gesamtwert!r}."

# An der oberen Grenze: 100 000 Stunden, jede siebte mit gestörtem Zähler
zeilen = ["stunde;gesamt;it"]
for nummer in range(100000):
    it = nummer % 997 + 1
    gesamt = "-" if nummer % 7 == 0 else str(it + (nummer * 37) % (it + 1))
    zeilen.append(f"{nummer * 10};{gesamt};{it}")
tupel, stundenwerte, gesamtwert, kritisch = von_hand(zeilen, 1.5)
ergebnis = (len(list(messungen(iter(zeilen)))), pue_je_stunde(iter(zeilen)), gesamt_pue(iter(zeilen)))
assert ergebnis[0] == len(tupel) and gleich(ergebnis[1], stundenwerte) and ergebnis[2] == gesamtwert, (
    f"Bei 100 000 Stunden liefern messungen {ergebnis[0]} Tupel (erwartet {len(tupel)}), pue_je_stunde "
    f"{len(ergebnis[1])} Einträge (erwartet {len(stundenwerte)}) und gesamt_pue {ergebnis[2]!r} (erwartet {gesamtwert!r})."
)

# kritische_stunden an der oberen Grenze
ergebnis = kritische_stunden(stundenwerte, 1.5)
assert ergebnis == kritisch, (
    f"kritische_stunden mit {len(stundenwerte)} Stunden liefert {len(ergebnis)} Stunden, erwartet waren {len(kritisch)}, "
    f"die ersten {kritisch[:3]}, Ihre {ergebnis[:3]}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[(0, 390, 300), (2, 480, 300), (3, 300, 200)]\n{0: 1.3, 2: 1.6, 3: 1.5}\n1.46\n[2, 3]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
