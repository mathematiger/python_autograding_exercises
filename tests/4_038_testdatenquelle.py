# Automatisch erzeugt aus lehrkraft/muster/4_038_testdatenquelle.py - nicht von Hand ändern.
# vorlage-hash: 573df7ac74381c8e
# text-hash: 4e4a7ca78b031c8f
# thema: kontrollfluss
# inhalt: iter() mit Endmarke

import io


class Quelle:
    """Eine Testdatenquelle wie die alte Bibliothek: liefert die Werte und danach None, zählt die Aufrufe."""

    def __init__(self, werte):
        """Merkt sich die Werte, die vor dem None kommen."""
        self.werte = list(werte)
        self.aufrufe = 0

    def __call__(self):
        """Liefert den nächsten Wert, nach dem letzten None; danach aufgerufen ist ein Fehler."""
        self.aufrufe += 1
        if self.aufrufe <= len(self.werte):
            return self.werte[self.aufrufe - 1]
        if self.aufrufe == len(self.werte) + 1:
            return None
        raise RuntimeError("Die Quelle wurde nach dem None noch einmal aufgerufen.")


class Zaehlstrom(io.StringIO):
    """Ein Datenstrom, der mitzählt, wie oft read aufgerufen wurde und mit welcher Anzahl."""

    def __init__(self, text):
        """Legt den Strom mit dem Text an."""
        super().__init__(text)
        self.leseaufrufe = []

    def read(self, anzahl=-1):
        """Liest wie StringIO.read und merkt sich die Anzahl."""
        self.leseaufrufe.append(anzahl)
        return super().read(anzahl)


def ergebnis_von(funktion):
    """Ruft die Funktion ohne Argumente auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


# testfaelle im Beispiel
quelle = Quelle([3, 0, ""])
ergebnis = ergebnis_von(lambda: list(testfaelle(quelle)))
assert ergebnis == [3, 0, ""], f'list(testfaelle(...)) mit den Werten 3, 0, "" und dann None ergibt {ergebnis!r}, erwartet war [3, 0, ""].'

# testfaelle mit anderen Werten (nicht fest hinschreiben!)
ergebnis = ergebnis_von(lambda: list(testfaelle(Quelle(["login", {"nutzer": "ada"}, [1, 2]]))))
assert ergebnis == ["login", {"nutzer": "ada"}, [1, 2]], (
    f"list(testfaelle(...)) mit drei Testfällen ergibt {ergebnis!r}, erwartet war ['login', {{'nutzer': 'ada'}}, [1, 2]]."
)

# testfaelle hört nicht bei 0, "" oder False auf, nur bei None
ergebnis = ergebnis_von(lambda: list(testfaelle(Quelle([False, 0, 0.0, "", [], 5]))))
assert ergebnis == [False, 0, 0.0, "", [], 5], (
    f"list(testfaelle(...)) mit den Werten False, 0, 0.0, \"\", [], 5 ergibt {ergebnis!r}, erwartet waren alle sechs.\n"
    "Tipp: Nehmen Sie None als Endmarke; iter vergleicht mit ==, und False == None ist False."
)

# testfaelle bei einer Quelle, die sofort None liefert
ergebnis = ergebnis_von(lambda: list(testfaelle(Quelle([]))))
assert ergebnis == [], f"list(testfaelle(...)) bei einer Quelle, die sofort None liefert, ergibt {ergebnis!r}, erwartet war []."

# testfaelle gibt einen Iterator zurück
quelle = Quelle([1, 2])
ergebnis = testfaelle(quelle)
assert iter(ergebnis) is ergebnis and hasattr(ergebnis, "__next__"), (
    f"testfaelle(...) ergibt ein Objekt vom Typ {type(ergebnis).__name__}, erwartet war ein Iterator.\n"
    "Tipp: iter(naechster, None) ist schon der fertige Iterator."
)

# testfaelle ruft naechster erst beim Abholen auf, einmal je Wert
quelle = Quelle([10, 20, 30])
iterator = testfaelle(quelle)
vorher = quelle.aufrufe
erster = next(iterator)
nachher = quelle.aufrufe
assert (vorher, erster, nachher) == (0, 10, 1), (
    f"Nach testfaelle(quelle) wurde quelle {vorher}-mal aufgerufen, nach dem ersten next() {nachher}-mal "
    f"(Wert {erster!r}); erwartet war 0-mal, dann 1-mal mit dem Wert 10.\n"
    "Tipp: Sammeln Sie die Werte nicht in einer Liste; iter(naechster, None) ruft erst bei next() auf."
)

# testfaelle ruft naechster nach dem None nicht mehr auf
quelle = Quelle([1, 2])
iterator = testfaelle(quelle)
ergebnis = ergebnis_von(lambda: (list(iterator), list(iterator)))
assert ergebnis == ([1, 2], []) and quelle.aufrufe == 3, (
    f"Zweimal list(...) über denselben Iterator ergibt {ergebnis!r} nach {quelle.aufrufe} Aufrufen der Quelle; "
    "erwartet war ([1, 2], []) nach 3 Aufrufen."
)

# bloecke im Beispiel
ergebnis = ergebnis_von(lambda: list(bloecke(io.StringIO("ABCDEFGH"), 3)))
assert ergebnis == ["ABC", "DEF", "GH"], (
    f'list(bloecke(io.StringIO("ABCDEFGH"), 3)) ergibt {ergebnis!r}, erwartet war ["ABC", "DEF", "GH"].'
)

# bloecke, wenn die Länge genau aufgeht
ergebnis = ergebnis_von(lambda: list(bloecke(io.StringIO("ABCDEF"), 2)))
assert ergebnis == ["AB", "CD", "EF"], (
    f'list(bloecke(io.StringIO("ABCDEF"), 2)) ergibt {ergebnis!r}, erwartet war ["AB", "CD", "EF"] ohne leeren Text am Ende.'
)

# bloecke mit groesse 1 und mit einer groesse über der Textlänge
ergebnis = [ergebnis_von(lambda: list(bloecke(io.StringIO("xyz"), 1))), ergebnis_von(lambda: list(bloecke(io.StringIO("xyz"), 100)))]
assert ergebnis == [["x", "y", "z"], ["xyz"]], (
    f"bloecke mit groesse 1 und groesse 100 bei \"xyz\" ergibt {ergebnis!r}, erwartet war [['x', 'y', 'z'], ['xyz']]."
)

# bloecke bei einem leeren Datenstrom
ergebnis = ergebnis_von(lambda: list(bloecke(io.StringIO(""), 4)))
assert ergebnis == [], f'list(bloecke(io.StringIO(""), 4)) ergibt {ergebnis!r}, erwartet war [].'

# bloecke liest erst beim Abholen, je Stück einmal mit groesse
strom = Zaehlstrom("0123456789")
iterator = bloecke(strom, 4)
vorher = list(strom.leseaufrufe)
erstes = next(iterator)
assert vorher == [] and erstes == "0123" and strom.leseaufrufe == [4], (
    f"Nach bloecke(strom, 4) wurde read mit {vorher} aufgerufen, nach dem ersten next() mit {strom.leseaufrufe} "
    f"(Stück {erstes!r}); erwartet war erst gar nicht, dann einmal read(4) mit dem Stück '0123'."
)

# Beide Funktionen benutzen iter und keine while-Schleife
assert verwendet("iter") and not verwendet("while"), (
    "Benutzen Sie iter(funktion, endmarke) statt einer while-Schleife."
)

# Die Ausgabe des Programms
erwartet = "[3, 0, '']\n['ABC', 'DEF', 'GH']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Quellen und Datenströme
zufall = Zufall(4038)
for _ in range(300):
    werte = [zufall.choice([0, 1, -1, "", "a", False, True, 0.0, (), "None"]) for _ in range(zufall.randint(0, 8))]
    ergebnis = ergebnis_von(lambda: list(testfaelle(Quelle(werte))))
    assert ergebnis == werte, f"list(testfaelle(...)) mit den Werten {werte!r} und dann None ergibt {ergebnis!r}."
    text = "".join(zufall.choice("ab\n ") for _ in range(zufall.randint(0, 20)))
    groesse = zufall.randint(1, 7)
    erwartet = [text[anfang : anfang + groesse] for anfang in range(0, len(text), groesse)]
    ergebnis = ergebnis_von(lambda: list(bloecke(io.StringIO(text), groesse)))
    assert ergebnis == erwartet, f"list(bloecke(io.StringIO({text!r}), {groesse})) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Obere Grenze: 100 000 Testfälle
quelle = Quelle(range(100000))
ergebnis = ergebnis_von(lambda: sum(testfaelle(quelle)))
assert ergebnis == sum(range(100000)) and quelle.aufrufe == 100001, (
    f"Bei 100 000 Testfällen ergibt sum(testfaelle(...)) {ergebnis!r} nach {quelle.aufrufe} Aufrufen, "
    f"erwartet war {sum(range(100000))} nach 100 001 Aufrufen."
)

# Obere Grenze: 10**6 Zeichen
text = "".join(zufall.choice("0123456789") for _ in range(1000)) * 1000
for groesse in [1000, 10**6, 999]:
    ergebnis = ergebnis_von(lambda: list(bloecke(io.StringIO(text), groesse)))
    anzahl = (len(text) + groesse - 1) // groesse
    assert isinstance(ergebnis, list) and len(ergebnis) == anzahl and "".join(ergebnis) == text, (
        f"Bei 10**6 Zeichen und groesse {groesse} ergibt bloecke {len(ergebnis)} Stücke, erwartet waren {anzahl}, "
        "die zusammen den ganzen Text ergeben."
    )
