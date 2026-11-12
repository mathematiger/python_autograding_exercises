# Automatisch erzeugt aus lehrkraft/muster/5_014_sensorstapel.py - nicht von Hand ändern.
# vorlage-hash: 7135c5ac74a08df5
# text-hash: 0ae50f13aaa2596c
# thema: klassen
# inhalt: `__class_getitem__`

def fehler_bei(aufruf):
    """Führt aufruf() aus und gibt die ausgelöste Ausnahme zurück, sonst None."""
    try:
        aufruf()
    except Exception as fehler:
        return fehler
    return None


# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Stapel[float]([21.5, 22.0])\nabgelehnt\n22.0 1"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"

# Stapel[float] ist eine Unterklasse von Stapel mit elementtyp float
variante = Stapel[float]
assert isinstance(variante, type) and issubclass(variante, Stapel) and variante.elementtyp is float, (
    f"Stapel[float] ergibt {variante!r}; erwartet war eine Unterklasse von Stapel mit elementtyp float.\n"
    "Tipp: type(name, (cls,), {'elementtyp': typ, …}) erzeugt die Unterklasse."
)

# Stapel[float] heißt "Stapel[float]"
assert isinstance(variante, type) and issubclass(variante, Stapel) and variante.__name__ == "Stapel[float]" and variante.elementtyp is float, (
    f"Stapel[float] ergibt {variante!r}; erwartet war eine Unterklasse von Stapel mit __name__ 'Stapel[float]' "
    "und elementtyp float.\nTipp: type(name, (cls,), {'elementtyp': typ, …}) erzeugt die Unterklasse."
)

# Dieselbe Klasse für denselben Typ, eine andere für einen anderen
assert Stapel[float] is Stapel[float] and Stapel[int] is not Stapel[float], (
    "Stapel[float] is Stapel[float] soll True sein und Stapel[int] eine andere Klasse.\n"
    "Tipp: Merken Sie sich die erzeugten Klassen in einem Dictionary mit dem Schlüssel (cls, typ)."
)

# len zählt die abgelegten Werte
zaehler = Stapel[int]()
for wert in [5, 8, 13]:
    zaehler.lege_ab(wert)
assert len(zaehler) == 3, f"Nach lege_ab(5), lege_ab(8), lege_ab(13) ergibt len {len(zaehler)!r}, erwartet war 3."

# nimm gibt zuerst den zuletzt abgelegten Wert zurück
ergebnis = (zaehler.nimm(), zaehler.nimm())
assert ergebnis == (13, 8), (
    f"Nach lege_ab(5), lege_ab(8), lege_ab(13) ergeben zweimal nimm() {ergebnis!r}, erwartet war (13, 8).\n"
    "Tipp: Oben liegt der zuletzt abgelegte Wert; list.pop() ohne Argument nimmt das letzte Element."
)

# repr zeigt den Klassennamen und die Werte von unten nach oben
zaehler = Stapel[int]()
for wert in [5, 8, 13]:
    zaehler.lege_ab(wert)
ergebnis = repr(zaehler)
assert ergebnis == "Stapel[int]([5, 8, 13])", (
    f"Nach lege_ab(5), lege_ab(8), lege_ab(13) ergibt repr {ergebnis!r}, erwartet war 'Stapel[int]([5, 8, 13])'.\n"
    "Tipp: f'{type(self).__name__}({self._werte!r})' – type(self).__name__ ist der Name der Unterklasse."
)

# Der Stapel arbeitet zuletzt abgelegt, zuerst genommen
zaehler = Stapel[int]()
for wert in [5, 8, 13]:
    zaehler.lege_ab(wert)
ergebnis = (len(zaehler), zaehler.nimm(), zaehler.nimm(), len(zaehler), repr(zaehler))
assert ergebnis == (3, 13, 8, 1, "Stapel[int]([5])"), (
    f"Nach lege_ab(5), lege_ab(8), lege_ab(13) ergeben len, nimm(), nimm(), len und repr {ergebnis!r}; "
    "erwartet war (3, 13, 8, 1, 'Stapel[int]([5])')."
)

# Falscher Typ: TypeError, der Stapel bleibt unverändert
temperaturen = Stapel[float]()
temperaturen.lege_ab(19.5)
for wert in ["defekt", 21, None, [1.0]]:
    fehler = fehler_bei(lambda: temperaturen.lege_ab(wert))
    assert isinstance(fehler, TypeError) and len(temperaturen) == 1, (
        f"Stapel[float]().lege_ab({wert!r}) soll einen TypeError auslösen und nichts ablegen; bekommen: {fehler!r}, "
        f"Länge danach {len(temperaturen)}.\n"
        "Tipp: Prüfen Sie mit isinstance(wert, self.elementtyp), bevor Sie ablegen."
    )

# Falscher Typ: die Meldung nennt Wert und Typ
temperaturen = Stapel[float]()
temperaturen.lege_ab(19.5)
for wert in ["defekt", 21, None, [1.0]]:
    fehler = fehler_bei(lambda: temperaturen.lege_ab(wert))
    meldung = str(fehler) if fehler else ""
    assert isinstance(fehler, TypeError) and vergleichbar(repr(wert)) in vergleichbar(meldung) and vergleichbar("float") in vergleichbar(meldung) and len(temperaturen) == 1, (
        f"Stapel[float]().lege_ab({wert!r}) soll einen TypeError mit {wert!r} und float in der Meldung auslösen und "
        f"nichts ablegen; bekommen: {fehler!r}, Länge danach {len(temperaturen)}.\n"
        "Tipp: Prüfen Sie mit isinstance(wert, self.elementtyp), bevor Sie ablegen."
    )

# isinstance gilt wie immer, auch für Unterklassen
ganz = Stapel[int]()
ganz.lege_ab(True)
eigen = type("Messwert", (float,), {})
messwerte = Stapel[float]()
messwerte.lege_ab(eigen(3.5))
assert len(ganz) == 1 and len(messwerte) == 1, "Stapel[int] soll True annehmen und Stapel[float] ein Objekt einer Unterklasse von float."

# Ein Stapel ohne Typ nimmt alles an
alles = Stapel()
for wert in [1, "a", None, 2.5, (1, 2)]:
    alles.lege_ab(wert)
assert len(alles) == 5 and Stapel.elementtyp is object and repr(alles) == "Stapel([1, 'a', None, 2.5, (1, 2)])", (
    f"Stapel() soll alles annehmen; nach fünf Werten ergibt repr {repr(alles)!r}, erwartet war "
    "\"Stapel([1, 'a', None, 2.5, (1, 2)])\"."
)

# nimm auf einem leeren Stapel: IndexError
for stapel in [Stapel(), Stapel[str]()]:
    fehler = fehler_bei(stapel.nimm)
    assert isinstance(fehler, IndexError), f"nimm() auf einem leeren {type(stapel).__name__} soll einen IndexError auslösen; bekommen: {fehler!r}."

# Keine Klasse in eckigen Klammern: TypeError
for beschreibung, aufruf in [
    ("Stapel[int, str]", lambda: Stapel[int, str]),
    ("Stapel[3]", lambda: Stapel[3]),
    ("Stapel['int']", lambda: Stapel["int"]),
]:
    fehler = fehler_bei(aufruf)
    assert isinstance(fehler, TypeError), (
        f"{beschreibung} soll einen TypeError auslösen; bekommen: {fehler!r}.\n"
        "Tipp: isinstance(typ, type) ist nur für Klassen True."
    )

# Ein schon parametrisierter Stapel lässt sich nicht noch einmal parametrisieren
fehler = fehler_bei(lambda: Stapel[int][str])
assert isinstance(fehler, TypeError), (
    f"Stapel[int][str] soll einen TypeError auslösen; bekommen: {fehler!r}.\n"
    "Tipp: Merken Sie sich in der erzeugten Klasse, dass sie schon parametrisiert ist."
)

# Eigene Klassen als Typ und Unterklassen von Stapel
class Meldung:
    """Eine Statusmeldung eines Sensors."""


class Puffer(Stapel):
    """Ein Stapel mit eigenem Namen."""


meldungen = Puffer[Meldung]()
meldungen.lege_ab(Meldung())
assert type(meldungen).__name__ == "Puffer[Meldung]" and isinstance(meldungen, Puffer) and Puffer[Meldung] is not Stapel[Meldung], (
    f"Puffer[Meldung]() hat den Typ {type(meldungen).__name__!r}; erwartet war 'Puffer[Meldung]', eine Unterklasse von "
    "Puffer, verschieden von Stapel[Meldung].\nTipp: Benutzen Sie cls und cls.__name__, nicht Stapel."
)

# Zwei Stapel teilen sich ihre Werte nicht
a = Stapel[int]()
b = Stapel[int]()
a.lege_ab(1)
assert (len(a), len(b)) == (1, 0), f"Nach a.lege_ab(1) haben a und b die Längen {(len(a), len(b))}, erwartet war (1, 0)."

# Viele zufällige Abläufe gegen eine Liste
zufall = Zufall(5014)
typen = [int, float, str, object]
for _ in range(200):
    typ = zufall.choice(typen)
    stapel = Stapel[typ]()
    vergleich = []
    for _ in range(20):
        if zufall.random() < 0.6:
            wert = zufall.choice([1, 2.5, "x", None, True])
            gueltig = isinstance(wert, typ)
            fehler = fehler_bei(lambda: stapel.lege_ab(wert))
            if gueltig:
                vergleich.append(wert)
            assert (fehler is None) == gueltig, (
                f"Stapel[{typ.__name__}].lege_ab({wert!r}): erwartet {'kein' if gueltig else 'ein'} TypeError, bekommen {fehler!r}."
            )
        else:
            fehler = fehler_bei(stapel.nimm) if not vergleich else None
            if vergleich:
                erwartet = vergleich.pop()
                ergebnis = stapel.nimm()
                assert ergebnis is erwartet, f"nimm() ergibt {ergebnis!r}, erwartet war {erwartet!r}."
            else:
                assert isinstance(fehler, IndexError), f"nimm() auf einem leeren Stapel soll einen IndexError auslösen; bekommen: {fehler!r}."
        assert len(stapel) == len(vergleich), f"len ergibt {len(stapel)}, erwartet war {len(vergleich)}."

# An der oberen Grenze: 100 000 Werte, lege_ab und nimm in O(1)
gross = Stapel[int]()
for wert in range(100000):
    gross.lege_ab(wert)
_, schritte_voll = zaehle_schritte(gross.nimm)
klein = Stapel[int]()
klein.lege_ab(1)
_, schritte_klein = zaehle_schritte(klein.nimm)
assert len(gross) == 99999 and gross.nimm() == 99998 and schritte_voll <= schritte_klein + 5, (
    f"Bei 100 000 Werten hat nimm() {schritte_voll} Schritte gebraucht, bei einem Wert {schritte_klein}; "
    "erwartet war gleich viel.\nTipp: list.pop() am Ende kostet O(1), pop(0) oder insert(0, …) O(n)."
)


def arbeitet_am_anfang(*methoden):
    """Gibt True zurück, wenn eine der Methoden pop(0) oder insert(0, …) aufruft (das läuft in C und zählt nicht)."""
    import ast
    import inspect
    import textwrap

    for methode in methoden:
        baum = ast.parse(textwrap.dedent(inspect.getsource(methode)))
        for knoten in ast.walk(baum):
            if not (isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute)):
                continue
            erstes = knoten.args[0] if knoten.args else None
            if knoten.func.attr in ("pop", "insert") and isinstance(erstes, ast.Constant) and erstes.value == 0:
                return True
    return False


# lege_ab und nimm arbeiten am Ende der Liste, nicht am Anfang
assert not arbeitet_am_anfang(Stapel.lege_ab, Stapel.nimm), (
    "lege_ab oder nimm benutzen pop(0) oder insert(0, …); das verschiebt bei jedem Aufruf alle Werte (O(n)).\n"
    "Tipp: Legen Sie oben am Ende der Liste ab: append und pop() ohne Argument."
)
