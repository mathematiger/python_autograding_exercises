# Automatisch erzeugt aus lehrkraft/muster/5_030_netzscanner.py - nicht von Hand ändern.
# vorlage-hash: b8fe964c9383410d
# text-hash: 7e9361820c66f1ed
# thema: kontrollfluss
# inhalt: Iterable, Iterator, Generator typisieren

import itertools
import types
import typing


def form(typ):
    """Bringt eine Annotation in vergleichbare Form; typing.X und collections.abc.X sowie Optional und | zählen gleich."""
    if typ is None:
        return type(None)
    if isinstance(typ, list):
        return tuple(form(teil) for teil in typ)
    herkunft = typing.get_origin(typ)
    if herkunft is None:
        return typ
    teile = typing.get_args(typ)
    if herkunft is typing.Union or herkunft is types.UnionType:
        return ("Union", frozenset(form(teil) for teil in teile))
    return (herkunft, tuple(form(teil) for teil in teile))


def annotationen(funktion):
    """Gibt die Annotationen der Funktion in vergleichbarer Form zurück, bei einem Fehler dessen Text."""
    try:
        hinweise = typing.get_type_hints(funktion)
    except Exception as fehler:
        return f"nicht lesbar ({fehler})"
    return {name: form(typ) for name, typ in hinweise.items()}


def lesbar(funktion):
    """Die Annotationen so, wie Python sie kennt, für Meldungen."""
    try:
        return {name: str(typ).replace("collections.abc.", "") for name, typ in typing.get_type_hints(funktion).items()}
    except Exception as fehler:
        return f"nicht lesbar ({fehler})"


def ergebnis_von(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def statistik_schritte(werte):
    """Spielt latenzstatistik() mit den Werten durch; gibt die gelieferten Zahlen und den Rückgabewert zurück."""
    statistik = latenzstatistik()
    geliefert = [next(statistik)]
    for wert in werte:
        geliefert.append(statistik.send(wert))
    try:
        statistik.send(None)
    except StopIteration as ende:
        return geliefert, ende.value
    return geliefert, "kein Ende nach send(None)"


def mittel_mit_zaehlung(werte):
    """Ruft mittlere_latenz(werte) auf und zählt dabei die Aufrufe von latenzstatistik."""
    original = globals()["latenzstatistik"]
    aufrufe = []

    def mitzaehlen():
        """Zählt den Aufruf und gibt die echte latenzstatistik zurück."""
        aufrufe.append(True)
        return original()

    globals()["latenzstatistik"] = mitzaehlen
    try:
        ergebnis = ergebnis_von(mittlere_latenz, werte)
    finally:
        globals()["latenzstatistik"] = original
    return ergebnis, len(aufrufe)


def nah(a, b):
    """True, wenn zwei Zahlen bis auf Rundungsfehler gleich sind."""
    return isinstance(a, (int, float)) and abs(a - b) <= 1e-9 * max(1.0, abs(b))


ITERATOR_STR = form(Iterator[str])
GENERATOR_STR = form(Generator[str, None, None])

# hostadressen im Beispiel
ergebnis = ergebnis_von(lambda: list(hostadressen("192.168.1", 1, 3)))
assert ergebnis == ["192.168.1.1", "192.168.1.2", "192.168.1.3"], (
    f'list(hostadressen("192.168.1", 1, 3)) ergibt {ergebnis!r}, erwartet war ["192.168.1.1", "192.168.1.2", "192.168.1.3"].'
)

# hostadressen mit anderen Werten (nicht fest hinschreiben!), letzter gehört dazu
ergebnis = ergebnis_von(lambda: list(hostadressen("10.20", 254, 255)))
assert ergebnis == ["10.20.254", "10.20.255"], f'list(hostadressen("10.20", 254, 255)) ergibt {ergebnis!r}, erwartet war ["10.20.254", "10.20.255"].'

# hostadressen mit erster gleich letzter
ergebnis = ergebnis_von(lambda: list(hostadressen("a", 0, 0)))
assert ergebnis == ["a.0"], f'list(hostadressen("a", 0, 0)) ergibt {ergebnis!r}, erwartet war ["a.0"].'

# hostadressen mit letzter kleiner als erster
ergebnis = ergebnis_von(lambda: list(hostadressen("a", 5, 4)))
assert ergebnis == [], f'list(hostadressen("a", 5, 4)) ergibt {ergebnis!r}, erwartet war [].'

# hostadressen ist lazy: die erste Adresse kommt, ohne die übrigen zu bauen
try:
    ergebnis, schritte = zaehle_schritte(lambda: next(iter(hostadressen("10.0.0", 0, 100000))))
except Exception as fehler:
    ergebnis, schritte = f"{type(fehler).__name__}: {fehler}", None
assert ergebnis == "10.0.0.0" and isinstance(schritte, int) and schritte < 1000, (
    f'next(iter(hostadressen("10.0.0", 0, 100000))) ergibt {ergebnis!r} nach {schritte} Schritten, '
    'erwartet war "10.0.0.0" nach wenigen Schritten.\n'
    "Tipp: Liefern Sie jede Adresse mit yield, statt eine Liste zu bauen."
)

# hostadressen ist annotiert
ergebnis = annotationen(hostadressen)
erwartet = {"praefix": str, "erster": int, "letzter": int}
assert isinstance(ergebnis, dict) and ergebnis.get("return") in (ITERATOR_STR, GENERATOR_STR) and {k: v for k, v in ergebnis.items() if k != "return"} == erwartet, (
    f"Die Annotationen von hostadressen sind {lesbar(hostadressen)}; erwartet war praefix: str, erster: int, "
    "letzter: int und die Rückgabe Iterator[str]."
)

# erreichbare im Beispiel
ergebnis = ergebnis_von(lambda: list(erreichbare(hostadressen("10.0.0", 1, 6), lambda a: a.endswith(("2", "5")))))
assert ergebnis == ["10.0.0.2", "10.0.0.5"], f"erreichbare(...) ergibt im Beispiel {ergebnis!r}, erwartet war ['10.0.0.2', '10.0.0.5']."

# erreichbare mit einer Liste und einer anderen Prüfung
ergebnis = ergebnis_von(lambda: list(erreichbare(["drucker", "nas", "router"], lambda a: "r" in a)))
assert ergebnis == ["drucker", "router"], f'erreichbare(["drucker", "nas", "router"], …) ergibt {ergebnis!r}, erwartet war ["drucker", "router"].'

# erreichbare, wenn niemand antwortet
ergebnis = ergebnis_von(lambda: list(erreichbare(["a", "b"], lambda a: False)))
assert ergebnis == [], f"erreichbare, wenn niemand antwortet, ergibt {ergebnis!r}, erwartet war []."

# erreichbare fragt erst, wenn die nächste Adresse gebraucht wird, auch bei unendlich vielen
gefragt = []


def antwortet_jede_dritte(adresse):
    """Merkt sich jede Anfrage; antwortet bei jeder dritten Adresse."""
    gefragt.append(adresse)
    return len(gefragt) % 3 == 0


unendlich = (f"10.1.{nummer}" for nummer in itertools.count())
iterator = ergebnis_von(erreichbare, unendlich, antwortet_jede_dritte)
vorher = len(gefragt)
erste = ergebnis_von(lambda: [next(iterator), next(iterator)])
assert vorher == 0 and erste == ["10.1.2", "10.1.5"] and len(gefragt) == 6, (
    f"Bei unendlich vielen Adressen fragt erreichbare vor dem ersten next() {vorher}-mal, liefert dann {erste!r} "
    f"nach {len(gefragt)} Anfragen; erwartet war 0-mal, dann ['10.1.2', '10.1.5'] nach 6 Anfragen."
)

# erreichbare ist annotiert, adressen so großzügig wie möglich
ergebnis = annotationen(erreichbare)
erwartet = {"adressen": form(Iterable[str]), "antwortet": form(Callable[[str], bool])}
assert isinstance(ergebnis, dict) and ergebnis.get("return") in (ITERATOR_STR, GENERATOR_STR) and {k: v for k, v in ergebnis.items() if k != "return"} == erwartet, (
    f"Die Annotationen von erreichbare sind {lesbar(erreichbare)}; erwartet war adressen: Iterable[str], "
    "antwortet: Callable[[str], bool] und die Rückgabe Iterator[str].\n"
    "Tipp: list[str] oder Iterator[str] für adressen wären zu eng; die Funktion läuft nur einmal mit for darüber."
)

# latenzstatistik im Beispiel
ergebnis = ergebnis_von(statistik_schritte, [12.5, 7.5])
assert isinstance(ergebnis, tuple) and ergebnis[0] == [0, 1, 2] and nah(ergebnis[1], 10.0), (
    f"latenzstatistik mit 12.5, 7.5 und dann None liefert {ergebnis!r}, erwartet war [0, 1, 2] und der Rückgabewert 10.0.\n"
    "Tipp: Den Mittelwert gibt return zurück, er steckt in StopIteration.value."
)

# latenzstatistik mit anderen Werten
ergebnis = ergebnis_von(statistik_schritte, [1.0, 2.0, 6.0, 3.0])
assert isinstance(ergebnis, tuple) and ergebnis[0] == [0, 1, 2, 3, 4] and nah(ergebnis[1], 3.0), (
    f"latenzstatistik mit 1.0, 2.0, 6.0, 3.0 liefert {ergebnis!r}, erwartet war [0, 1, 2, 3, 4] und 3.0."
)

# latenzstatistik ohne Werte gibt 0.0 zurück
ergebnis = ergebnis_von(statistik_schritte, [])
assert ergebnis == ([0], 0.0), f"latenzstatistik, gleich mit None beendet, liefert {ergebnis!r}, erwartet war ([0], 0.0)."

# latenzstatistik: ein Messwert 0 beendet nicht
ergebnis = ergebnis_von(statistik_schritte, [0, 0.0, 9])
assert isinstance(ergebnis, tuple) and ergebnis[0] == [0, 1, 2, 3] and nah(ergebnis[1], 3.0), (
    f"latenzstatistik mit 0, 0.0, 9 liefert {ergebnis!r}, erwartet war [0, 1, 2, 3] und 3.0.\n"
    "Tipp: Prüfen Sie mit is not None, nicht mit if wert."
)

# latenzstatistik ist annotiert
ergebnis = annotationen(latenzstatistik)
erwartet = {"return": form(Generator[int, typing.Optional[float], float])}
assert ergebnis == erwartet, (
    f"Die Annotationen von latenzstatistik sind {lesbar(latenzstatistik)}; erwartet war die Rückgabe "
    "Generator[int, float | None, float]: liefert int, nimmt float oder None an, gibt float zurück."
)

# mittlere_latenz im Beispiel
ergebnis = ergebnis_von(mittlere_latenz, [12.5, 7.5, 4.0])
assert nah(ergebnis, 8.0), f"mittlere_latenz([12.5, 7.5, 4.0]) ergibt {ergebnis!r}, erwartet war 8.0."

# mittlere_latenz ohne Messwerte
ergebnis = ergebnis_von(mittlere_latenz, [])
assert ergebnis == 0.0, f"mittlere_latenz([]) ergibt {ergebnis!r}, erwartet war 0.0."

# mittlere_latenz mit einem Generator
ergebnis = ergebnis_von(mittlere_latenz, (float(x) for x in range(5)))
assert nah(ergebnis, 2.0), f"mittlere_latenz(Generator über 0..4) ergibt {ergebnis!r}, erwartet war 2.0."

# mittlere_latenz benutzt latenzstatistik
ergebnis, aufrufe = mittel_mit_zaehlung([3.0, 5.0])
assert aufrufe == 1 and nah(ergebnis, 4.0), (
    f"mittlere_latenz([3.0, 5.0]) ergibt {ergebnis!r} und ruft latenzstatistik {aufrufe}-mal auf; erwartet war 4.0 "
    "mit genau einem Aufruf."
)

# mittlere_latenz ist annotiert
ergebnis = annotationen(mittlere_latenz)
assert ergebnis == {"messwerte": form(Iterable[float]), "return": float}, (
    f"Die Annotationen von mittlere_latenz sind {lesbar(mittlere_latenz)}; erwartet war messwerte: Iterable[float] und die Rückgabe float."
)

# Die Ausgabe des Programms
erwartet = "['192.168.1.1', '192.168.1.2', '192.168.1.3']\n['10.0.0.2', '10.0.0.5']\n8.0"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Netze und Messreihen
zufall = Zufall(5030)
for _ in range(200):
    erster = zufall.randint(0, 300)
    letzter = erster + zufall.randint(-2, 12)
    erwartet = [f"172.16.{nummer}" for nummer in range(erster, letzter + 1)]
    ergebnis = ergebnis_von(lambda: list(hostadressen("172.16", erster, letzter)))
    assert ergebnis == erwartet, f'list(hostadressen("172.16", {erster}, {letzter})) ergibt {ergebnis!r}, erwartet war {erwartet!r}.'
    offen = set(zufall.sample(erwartet, zufall.randint(0, len(erwartet))))
    ergebnis = ergebnis_von(lambda: list(erreichbare(iter(erwartet), offen.__contains__)))
    assert ergebnis == [a for a in erwartet if a in offen], f"erreichbare mit den offenen Adressen {sorted(offen)} ergibt {ergebnis!r}."
    werte = [zufall.choice([0, 10**4, zufall.randint(0, 10**4), zufall.randint(0, 1000) / 10]) for _ in range(zufall.randint(0, 10))]
    erwartet_mittel = sum(werte) / len(werte) if werte else 0.0
    ergebnis = ergebnis_von(mittlere_latenz, werte)
    assert nah(ergebnis, erwartet_mittel), f"mittlere_latenz({werte!r}) ergibt {ergebnis!r}, erwartet war {erwartet_mittel!r}."

# Obere Grenze: 100 000 Messwerte
werte = [zufall.randint(0, 10**4) for _ in range(100000)]
ergebnis = ergebnis_von(mittlere_latenz, werte)
assert nah(ergebnis, sum(werte) / len(werte)), f"Bei 100 000 Messwerten ergibt mittlere_latenz {ergebnis!r}, erwartet war {sum(werte) / len(werte)!r}."
