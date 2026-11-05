# Automatisch erzeugt aus lehrkraft/muster/3_022_lauflaengen.py - nicht von Hand ändern.
# vorlage-hash: 1847375913dffad5
# text-hash: e530343d83bff3c5
# thema: kontrollfluss
# inhalt: Generatoren mit yield

def ist_generator(objekt):
    """Gibt zurück, ob objekt ein Generator ist (Ergebnis einer Funktion mit yield)."""
    return type(objekt).__name__ == "generator"


# laeufe aus dem Beispiel
ergebnis = list(laeufe("AAAABBC"))
assert ergebnis == [("A", 4), ("B", 2), ("C", 1)], (
    f'list(laeufe("AAAABBC")) ergibt {ergebnis!r}, erwartet war [("A", 4), ("B", 2), ("C", 1)].\n'
    "Tipp: Vergessen Sie den letzten Lauf nicht; er muss nach der Schleife noch geliefert werden."
)

# laeufe ist ein Generator
assert ist_generator(laeufe("AB")), (
    f'laeufe("AB") liefert ein Objekt vom Typ {type(laeufe("AB")).__name__}, erwartet war ein Generator.\n'
    "Tipp: Liefern Sie die Tupel mit yield, statt eine Liste zurückzugeben."
)

# entpacke ist ein Generator
assert ist_generator(entpacke([("A", 1)])), (
    f'entpacke([("A", 1)]) liefert ein Objekt vom Typ {type(entpacke([("A", 1)])).__name__}, erwartet war ein Generator.\n'
    "Tipp: Liefern Sie jedes Zeichen einzeln mit yield."
)

# kodiere aus dem Beispiel und Randfälle
for text, erwartet in [
    ("xxyxx", [("x", 2), ("y", 1), ("x", 2)]),
    ("", []),
    ("Q", [("Q", 1)]),
    ("aAaa", [("a", 1), ("A", 1), ("a", 2)]),
    ("  \n\n", [(" ", 2), ("\n", 2)]),
    ("zzzz", [("z", 4)]),
]:
    try:
        ergebnis = kodiere(text)
    except IndexError as fehler:
        ergebnis = f"IndexError: {fehler}"
    assert ergebnis == erwartet, (
        f"kodiere({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Ein neuer Lauf beginnt, sobald ein Zeichen anders ist als das vorige; gleiche Zeichen weiter "
        "hinten bilden einen eigenen Lauf. Bei leerem Text gibt es kein text[0]; liefern Sie dann gar nichts."
    )

# kodiere gibt eine Liste zurück
assert type(kodiere("ab")) is list, f'kodiere("ab") liefert {type(kodiere("ab")).__name__}, erwartet war eine Liste.'

# entpacke aus dem Beispiel und Randfälle
for paare, erwartet in [([("A", 3), ("b", 1)], "AAAb"), ([], ""), ([("x", 1), ("x", 2)], "xxx"), ((("-", 5),), "-----")]:
    ergebnis = "".join(entpacke(paare))
    assert ergebnis == erwartet, f'"".join(entpacke({paare!r})) ergibt {ergebnis!r}, erwartet war {erwartet!r}.'

# entpacke arbeitet auch mit einem Iterator und holt die Paare erst, wenn sie gebraucht werden
class Paarstrom:
    """Ein Iterator über Paare, der mitzählt, wie viele Paare schon abgeholt wurden."""

    def __init__(self, paare):
        """Merkt sich die Paare."""
        self._paare = list(paare)
        self.abgeholt = 0

    def __iter__(self):
        """Ein Iterator gibt bei iter() sich selbst zurück."""
        return self

    def __next__(self):
        """Liefert das nächste Paar oder löst StopIteration aus."""
        if self.abgeholt >= len(self._paare):
            raise StopIteration
        self.abgeholt = self.abgeholt + 1
        return self._paare[self.abgeholt - 1]


strom = Paarstrom([("a", 10**6), ("b", 10**6), ("c", 1)])
zeichen = entpacke(strom)
anfang = [next(zeichen, None) for _ in range(5)]
assert anfang == ["a"] * 5 and strom.abgeholt == 1, (
    "Die ersten fünf Werte von entpacke für die Paare ('a', 10**6), ('b', 10**6), ('c', 1) beginnen mit "
    f"{[repr(teil)[:12] for teil in anfang]}, und es wurden "
    f"{strom.abgeholt} von 3 Paaren abgeholt; erwartet war fünfmal 'a' nach einem einzigen Paar.\n"
    "Tipp: Liefern Sie jedes Zeichen sofort einzeln mit yield, statt erst alles zusammenzusetzen."
)


class Zeichen(str):
    """Ein Zeichen, das sich merkt, wenn es mit * vervielfacht wird."""

    def __mul__(self, anzahl):
        """Merkt sich die Anzahl und vervielfacht wie ein gewöhnlicher Text."""
        vervielfacht.append(anzahl)
        return str.__mul__(self, anzahl)

    __rmul__ = __mul__


# entpacke setzt auch einen einzelnen Lauf nicht im Voraus zusammen
vervielfacht = []
ergebnis = "".join(entpacke([(Zeichen("a"), 3), (Zeichen("b"), 2)]))
assert ergebnis == "aaabb" and vervielfacht == [], (
    f'"".join(entpacke([("a", 3), ("b", 2)])) ergibt {ergebnis!r}, und dabei wurde {len(vervielfacht)}-mal '
    "zeichen * anzahl gebildet; erwartet war 'aaabb' ohne Vervielfachen.\n"
    "Tipp: Liefern Sie das Zeichen in einer Schleife anzahl-mal mit yield, statt erst zeichen * anzahl zu "
    "bilden; bei anzahl = 10**9 wäre das ein Text mit einer Milliarde Zeichen."
)

# kodiere benutzt laeufe
_echte_laeufe = laeufe
aufrufe = []


def laeufe(text):
    """Zählt die Aufrufe und liefert dieselben Läufe wie die echte Funktion."""
    aufrufe.append(text)
    return _echte_laeufe(text)


ergebnis = kodiere("aab")
laeufe = _echte_laeufe
assert ergebnis == [("a", 2), ("b", 1)] and aufrufe == ["aab"], (
    f'kodiere("aab") ergibt {ergebnis!r} und ruft laeufe {len(aufrufe)}-mal auf; erwartet war [("a", 2), ("b", 1)] '
    "mit einem Aufruf von laeufe.\nTipp: list(laeufe(text)) sammelt alle Werte des Generators in einer Liste."
)


# Vergleichslösung: über die Indizes laufen und das Laufende suchen
def kodiere_von_hand(text):
    """Sucht für jeden Lauf mit einer while-Schleife das Ende."""
    ergebnis = []
    anfang = 0
    while anfang < len(text):
        ende = anfang
        while ende < len(text) and text[ende] == text[anfang]:
            ende = ende + 1
        ergebnis.append((text[anfang], ende - anfang))
        anfang = ende
    return ergebnis


# 300 zufällige Texte, hin und zurück
zufall = Zufall(3022)
for _ in range(300):
    text = "".join(zufall.choice("aaAbb #") for _ in range(zufall.randint(0, 15)))
    erwartet = kodiere_von_hand(text)
    ergebnis = kodiere(text)
    assert ergebnis == erwartet, f"kodiere({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    zurueck = "".join(entpacke(erwartet))
    assert zurueck == text, f'"".join(entpacke({erwartet!r})) ergibt {zurueck!r}, erwartet war {text!r}.'

# An der oberen Grenze: 100 000 Zeichen
text = "".join("xy"[(nummer // 3) % 2] * (nummer % 4 + 1) for nummer in range(40000))[:100000]
ergebnis = kodiere(text)
erwartet = kodiere_von_hand(text)
assert ergebnis == erwartet, f"kodiere mit 100 000 Zeichen liefert {len(ergebnis)} Läufe, erwartet waren {len(erwartet)}."

# entpacke an der oberen Grenze: 100 000 Zeichen
assert "".join(entpacke(erwartet)) == text, "entpacke liefert für die Läufe eines Textes mit 100 000 Zeichen nicht den Text zurück."

# laeufe braucht O(n) Schritte
_, schritte_klein = zaehle_schritte(kodiere, text[:25000])
_, schritte_gross = zaehle_schritte(kodiere, text)
assert schritte_gross <= 6 * schritte_klein + 100, (
    f"kodiere braucht für 25 000 Zeichen {schritte_klein} und für 100 000 Zeichen {schritte_gross} Schritte; "
    "bei O(n) wären es etwa viermal so viele.\nTipp: Gehen Sie den Text nur einmal von vorn nach hinten durch."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[('A', 4), ('B', 2), ('C', 1)]\n[('x', 2), ('y', 1), ('x', 2)]\nAAAb"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
