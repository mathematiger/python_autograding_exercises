# Automatisch erzeugt aus lehrkraft/muster/3_023_firewallprotokoll.py - nicht von Hand ändern.
# vorlage-hash: a179c6825eaf17b8
# text-hash: 10148ef928cd5598
# thema: kontrollfluss
# inhalt: Generator-Ausdrücke

import ast
import inspect
import textwrap


def bauweise(funktion):
    """Gibt die Menge der Knotentypen im Syntaxbaum der Funktion zurück, leer, wenn der Quelltext fehlt."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return set()
    return {type(knoten) for knoten in ast.walk(baum)}


class Protokollstrom:
    """Ein Iterator über Verbindungen, der mitzählt, wie viele schon abgeholt wurden."""

    def __init__(self, verbindungen):
        """Merkt sich die Verbindungen."""
        self._verbindungen = list(verbindungen)
        self.abgeholt = 0

    def __iter__(self):
        """Ein Iterator gibt bei iter() sich selbst zurück."""
        return self

    def __next__(self):
        """Liefert die nächste Verbindung oder löst StopIteration aus."""
        if self.abgeholt >= len(self._verbindungen):
            raise StopIteration
        self.abgeholt = self.abgeholt + 1
        return self._verbindungen[self.abgeholt - 1]


BEISPIEL = [("10.20.1.5", 443, 5200), ("10.20.1.7", 22, 800), ("10.20.3.9", 443, 12000), ("172.16.0.4", 3389, 600)]

# Die drei Funktionen mit dem Beispiel
ergebnis = (bytes_zu_port(BEISPIEL, 443), gesperrter_port_benutzt(BEISPIEL, {23, 3389}), nur_intern(BEISPIEL, "10.20."))
assert ergebnis == (17200, True, False), (
    f"Für das Beispiel ergeben bytes_zu_port, gesperrter_port_benutzt und nur_intern {ergebnis!r}, "
    "erwartet war (17200, True, False)."
)

# Andere Werte (nicht fest hinschreiben!)
for aufruf, ergebnis, erwartet in [
    ("bytes_zu_port(BEISPIEL, 22)", bytes_zu_port(BEISPIEL, 22), 800),
    ("bytes_zu_port(BEISPIEL, 80)", bytes_zu_port(BEISPIEL, 80), 0),
    ("gesperrter_port_benutzt(BEISPIEL, {23, 25})", gesperrter_port_benutzt(BEISPIEL, {23, 25}), False),
    ("gesperrter_port_benutzt(BEISPIEL, {22})", gesperrter_port_benutzt(BEISPIEL, {22}), True),
    ("nur_intern(BEISPIEL[:3], '10.20.')", nur_intern(BEISPIEL[:3], "10.20."), True),
    ("nur_intern(BEISPIEL[:3], '10.20.1.')", nur_intern(BEISPIEL[:3], "10.20.1."), False),
    ("nur_intern(BEISPIEL, '1')", nur_intern(BEISPIEL, "1"), True),
]:
    assert ergebnis == erwartet, f"{aufruf} ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Leere Protokolle und leere Sperrliste
ergebnis = (bytes_zu_port([], 443), gesperrter_port_benutzt([], {22}), nur_intern([], "10."), gesperrter_port_benutzt(BEISPIEL, set()))
assert ergebnis == (0, False, True, False), (
    f"Mit leerem Protokoll ergeben bytes_zu_port, gesperrter_port_benutzt und nur_intern {ergebnis[:3]!r}, mit leerer "
    f"Sperrliste ergibt gesperrter_port_benutzt {ergebnis[3]!r}; erwartet war (0, False, True) und False.\n"
    "Tipp: In einem leeren Protokoll ist keine Verbindung von außen, also sind alle intern."
)

# Port 0 und Verbindungen mit 0 Bytes zählen mit
protokoll = [("10.0.0.1", 0, 0), ("10.0.0.2", 0, 7), ("10.0.0.3", 1, 5)]
ergebnis = (bytes_zu_port(protokoll, 0), gesperrter_port_benutzt(protokoll, {0}))
assert ergebnis == (7, True), (
    f"bytes_zu_port({protokoll}, 0) und gesperrter_port_benutzt(…, {{0}}) ergeben {ergebnis!r}, erwartet war (7, True)."
)

# Alle drei Funktionen arbeiten mit einem Iterator, der sich nur einmal durchlaufen lässt
ergebnis = (
    bytes_zu_port(Protokollstrom(BEISPIEL), 443),
    gesperrter_port_benutzt(Protokollstrom(BEISPIEL), {3389}),
    nur_intern(Protokollstrom(BEISPIEL), "10.20."),
)
assert ergebnis == (17200, True, False), (
    f"Mit einem Iterator statt einer Liste ergeben die drei Funktionen {ergebnis!r}, erwartet war (17200, True, False).\n"
    "Tipp: Ein Iterator ist nach einem Durchlauf verbraucht; gehen Sie die Verbindungen nur einmal durch."
)

# gesperrter_port_benutzt hört beim ersten Treffer auf
strom = Protokollstrom([("10.0.0.1", 23, 1)] + [("10.0.0.2", 443, 1)] * 1000)
ergebnis = gesperrter_port_benutzt(strom, {23})
assert ergebnis is True and strom.abgeholt == 1, (
    f"gesperrter_port_benutzt holt bei einem Treffer in der ersten von 1001 Verbindungen {strom.abgeholt} Verbindungen "
    f"ab (Ergebnis {ergebnis!r}); erwartet war True nach einer einzigen.\n"
    "Tipp: any(... for ...) mit runden Klammern hört beim ersten wahren Wert auf, any([...]) nicht."
)

# nur_intern hört bei der ersten externen Adresse auf
strom = Protokollstrom([("10.20.0.1", 443, 1), ("8.8.8.8", 53, 1)] + [("10.20.0.2", 443, 1)] * 1000)
ergebnis = nur_intern(strom, "10.20.")
assert ergebnis is False and strom.abgeholt == 2, (
    f"nur_intern holt bei einer externen Adresse an zweiter Stelle von 1002 Verbindungen {strom.abgeholt} Verbindungen "
    f"ab (Ergebnis {ergebnis!r}); erwartet war False nach zwei.\n"
    "Tipp: all(... for ...) mit runden Klammern hört beim ersten falschen Wert auf."
)

# Die Ergebnisse sind echte Wahrheitswerte
ergebnis = (gesperrter_port_benutzt(BEISPIEL, {22}), nur_intern(BEISPIEL, "10."))
assert ergebnis[0] is True and ergebnis[1] is False, (
    f"gesperrter_port_benutzt und nur_intern geben {ergebnis!r} zurück, erwartet war True und False."
)


# Jede Funktion benutzt einen Generator-Ausdruck, keine Schleife und keine Liste
for funktion in [bytes_zu_port, gesperrter_port_benutzt, nur_intern]:
    knotentypen = bauweise(funktion)
    gefunden = sorted(typ.__name__ for typ in knotentypen & {ast.For, ast.While, ast.ListComp})
    assert ast.GeneratorExp in knotentypen and not gefunden, (
        f"{funktion.__name__} soll mit einem Generator-Ausdruck (… for … in …) arbeiten, ohne for- oder "
        f"while-Anweisung und ohne List Comprehension; Generator-Ausdruck gefunden: "
        f"{'ja' if ast.GeneratorExp in knotentypen else 'nein'}, außerdem gefunden: {gefunden or 'nichts'}."
    )


# Vergleichslösung mit einer for-Schleife
def von_hand(verbindungen, port, gesperrt, netz):
    """Berechnet alle drei Antworten in einer einzigen for-Schleife."""
    summe = 0
    benutzt = False
    intern = True
    for quelle, ziel, menge in verbindungen:
        if ziel == port:
            summe = summe + menge
        if ziel in gesperrt:
            benutzt = True
        if quelle[: len(netz)] != netz:
            intern = False
    return summe, benutzt, intern


# 300 zufällige Protokolle
zufall = Zufall(3023)
for _ in range(300):
    verbindungen = [
        (zufall.choice(["10.20.1.5", "10.20.30.4", "10.2.0.1", "192.168.0.10", "8.8.8.8"]), zufall.choice([0, 22, 23, 53, 443, 65535]), zufall.choice([0, 1, 1500, 10**9]))
        for _ in range(zufall.randint(0, 8))
    ]
    port = zufall.choice([0, 22, 443, 8080])
    gesperrt = set(zufall.sample([0, 22, 23, 53, 3389, 65535], zufall.randint(0, 3)))
    netz = zufall.choice(["10.", "10.20.", "10.2", "192.168.0.1", "8"])
    erwartet = von_hand(verbindungen, port, gesperrt, netz)
    ergebnis = (
        bytes_zu_port(Protokollstrom(verbindungen), port),
        gesperrter_port_benutzt(Protokollstrom(verbindungen), gesperrt),
        nur_intern(Protokollstrom(verbindungen), netz),
    )
    assert ergebnis == erwartet, (
        f"Für {verbindungen} mit port={port}, gesperrt={gesperrt}, netz={netz!r} ergeben bytes_zu_port, "
        f"gesperrter_port_benutzt und nur_intern {ergebnis!r}, erwartet war {erwartet!r}."
    )


# An der oberen Grenze: eine Million Verbindungen aus einem Generator, ohne Liste
def grosses_protokoll():
    """Liefert eine Million Verbindungen, ohne sie alle auf einmal im Speicher zu halten."""
    for nummer in range(1000000):
        yield ("10.20.0.1", 443 if nummer % 2 else 80, 1000)


ergebnis = (
    bytes_zu_port(grosses_protokoll(), 443),
    gesperrter_port_benutzt(grosses_protokoll(), {22}),
    nur_intern(grosses_protokoll(), "10.20."),
)
assert ergebnis == (500000000, False, True), (
    f"Mit einer Million Verbindungen ergeben die drei Funktionen {ergebnis!r}, erwartet war (500000000, False, True)."
)

# Die Funktionen brauchen O(n) Schritte
kurz = BEISPIEL * 2500
_, schritte_klein = zaehle_schritte(bytes_zu_port, kurz, 443)
_, schritte_gross = zaehle_schritte(bytes_zu_port, kurz * 4, 443)
assert schritte_gross <= 6 * schritte_klein + 100, (
    f"bytes_zu_port braucht für 10 000 Verbindungen {schritte_klein} und für 40 000 {schritte_gross} Schritte; "
    "bei O(n) wären es etwa viermal so viele."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "17200\nTrue\nFalse"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
