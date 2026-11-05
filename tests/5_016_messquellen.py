# Automatisch erzeugt aus lehrkraft/muster/5_016_messquellen.py - nicht von Hand ändern.
# vorlage-hash: 1bf9b8bd14fef936
# text-hash: a9d9b92f7cd96439
# thema: klassen
# inhalt: typing.Protocol

def fehler_bei(aufruf):
    """Führt aufruf() aus und gibt die ausgelöste Ausnahme zurück, sonst None."""
    try:
        aufruf()
    except Exception as fehler:
        return fehler
    return None


def ist_messquelle(objekt):
    """isinstance(objekt, Messquelle), oder der Text der Ausnahme, wenn das nicht geht."""
    try:
        return isinstance(objekt, Messquelle)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


class NurName:
    """Hat einen Namen, kann aber nicht messen."""

    def __init__(self):
        self.name = "nur-name"


class NurMessen:
    """Kann messen, hat aber keinen Namen."""

    def messe(self):
        """Gibt immer 1.0 zurück."""
        return 1.0


class MitProperty:
    """Bietet name als property an."""

    @property
    def name(self):
        """Der Name wird erst beim Lesen zusammengesetzt."""
        return "prop-" + "quelle"

    def messe(self):
        """Gibt immer -3 zurück."""
        return -3


class Antwortzeit:
    """Ein Skript, das name als Klassenattribut hat und Millisekunden als ganze Zahl liefert."""

    name = "web-antwortzeit"

    def messe(self):
        """Gibt die Antwortzeit in Millisekunden zurück."""
        return 180


# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "True False\n({'srv1-cpu': 42.0, 'rack-oben': 24.5}, [1])\n23.0"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"

# Messquelle ist ein Protokoll
assert getattr(Messquelle, "_is_protocol", False) and Protocol in Messquelle.__mro__, (
    "Messquelle soll ein typing.Protocol sein: class Messquelle(Protocol): …"
)

# isinstance funktioniert mit Messquelle
ergebnis = ist_messquelle(Fuehler("a", 1.0))
assert ergebnis is True, (
    f"isinstance(Fuehler('a', 1.0), Messquelle) ergibt {ergebnis!r}, erwartet war True.\n"
    "Tipp: Ohne @runtime_checkable über der Klasse löst isinstance mit einem Protokoll einen TypeError aus."
)

# Objekte mit beiden Bestandteilen sind Messquellen, auch ohne Vererbung
for objekt in [CpuLast("c", [1]), Fuehler("f", 2), MitProperty(), Antwortzeit()]:
    ergebnis = ist_messquelle(objekt)
    assert ergebnis is True, (
        f"isinstance({type(objekt).__name__}(...), Messquelle) ergibt {ergebnis!r}, erwartet war True: Die Klasse hat "
        "name und messe."
    )

# Objekte, denen etwas fehlt, sind keine Messquellen
for objekt, beschreibung, grund in [
    (NurName(), "NurName()", "messe fehlt"),
    (NurMessen(), "NurMessen()", "name fehlt"),
    ("srv1", "'srv1'", "ein Text"),
    (42, "42", "eine Zahl"),
    (None, "None", "None"),
    (Fuehler, "Fuehler", "die Klasse selbst, kein Objekt: Fuehler.name gibt es nicht"),
]:
    ergebnis = ist_messquelle(objekt)
    assert ergebnis is False, (
        f"isinstance({beschreibung}, Messquelle) ergibt {ergebnis!r}, erwartet war False ({grund}).\n"
        "Tipp: Zum Protokoll gehören das Attribut name: str und die Methode messe."
    )

# Die Beispielklassen erben nicht von Messquelle
assert Messquelle not in CpuLast.__mro__ and Messquelle not in Mittelwert.__mro__, (
    "CpuLast und Mittelwert sollen nicht von Messquelle erben; Messquelle beschreibt nur die Struktur."
)

# abfragen aus dem Beispiel
cpu = CpuLast("srv1-cpu", [42.0])
ergebnis = abfragen([cpu, "srv1", Fuehler("rack-oben", 24.5)])
assert ergebnis == ({"srv1-cpu": 42.0, "rack-oben": 24.5}, [1]), (
    f"abfragen([cpu, 'srv1', Fuehler('rack-oben', 24.5)]) ergibt {ergebnis!r}, erwartet war "
    "({'srv1-cpu': 42.0, 'rack-oben': 24.5}, [1])."
)

# abfragen mit vielen verschiedenen Objekten, Reihenfolge der Liste
quellen = [NurName(), Antwortzeit(), 3.5, MitProperty(), NurMessen(), CpuLast("cpu2", [7, 8]), None]
ergebnis = abfragen(quellen)
erwartet = ({"web-antwortzeit": 180, "prop-quelle": -3, "cpu2": 7}, [0, 2, 4, 6])
assert ergebnis == erwartet and list(ergebnis[0]) == ["web-antwortzeit", "prop-quelle", "cpu2"], (
    f"abfragen für NurName, Antwortzeit, 3.5, MitProperty, NurMessen, CpuLast, None ergibt {ergebnis!r}, erwartet war "
    f"{erwartet!r} mit den Namen in der Reihenfolge der Liste.\nTipp: enumerate(quellen) liefert Position und Objekt."
)

# abfragen mit leerer Liste und misst jede Quelle genau einmal
cpu = CpuLast("einmal", [1, 2, 3])
ergebnis = (abfragen([]), abfragen([cpu]), abfragen([cpu]))
assert ergebnis == (({}, []), ({"einmal": 1}, []), ({"einmal": 2}, [])), (
    f"abfragen([]) und zweimal abfragen([cpu]) mit den Werten 1, 2, 3 ergeben {ergebnis!r}, erwartet war "
    "(({}, []), ({'einmal': 1}, []), ({'einmal': 2}, [])).\nTipp: Rufen Sie messe() pro Quelle genau einmal auf."
)

# Ein Mittelwert ist selbst eine Messquelle
rack = Mittelwert("rack", [Fuehler("o", 24.5), Fuehler("u", 21.5)])
ergebnis = (ist_messquelle(rack), getattr(rack, "name", None), rack.messe())
assert ergebnis == (True, "rack", 23.0), (
    f"Für Mittelwert('rack', [Fuehler('o', 24.5), Fuehler('u', 21.5)]) ergeben isinstance(…, Messquelle), name und "
    f"messe() {ergebnis!r}, erwartet war (True, 'rack', 23.0)."
)

# Ein Mittelwert misst bei jedem Aufruf neu
cpu = CpuLast("c", [10, 30])
mittel = Mittelwert("m", [cpu, Fuehler("f", 20)])
ergebnis = (mittel.messe(), mittel.messe())
assert ergebnis == (15.0, 25.0), (
    f"Ein Mittelwert aus CpuLast mit [10, 30] und einem Fühler mit 20 liefert bei zwei Messungen {ergebnis!r}, erwartet "
    "war (15.0, 25.0).\nTipp: Rufen Sie in messe() bei jedem Aufruf messe() aller Quellen auf, statt den Wert im "
    "Konstruktor zu berechnen."
)

# Mittelwerte lassen sich verschachteln und in abfragen benutzen
innen = Mittelwert("innen", [Fuehler("a", 10), Fuehler("b", 20)])
aussen = Mittelwert("aussen", [innen, Fuehler("c", 30), Antwortzeit()])
ergebnis = abfragen([aussen, innen])
assert ergebnis == ({"aussen": 75.0, "innen": 15.0}, []), (
    f"abfragen([aussen, innen]) mit verschachtelten Mittelwerten ergibt {ergebnis!r}, erwartet war "
    "({'aussen': 75.0, 'innen': 15.0}, [])."
)

# Ungültige Quellen lehnt schon der Konstruktor ab
for quellen, grund in [([], "leere Liste"), ([Fuehler("a", 1), "b"], "ein Text"), ([NurMessen()], "ohne name"), ([NurName()], "ohne messe")]:
    fehler = fehler_bei(lambda: Mittelwert("x", quellen))
    assert isinstance(fehler, TypeError), (
        f"Mittelwert('x', …) mit {grund} löst {fehler!r} aus, erwartet war ein TypeError schon beim Anlegen.\n"
        "Tipp: Prüfen Sie im Konstruktor mit isinstance(quelle, Messquelle) jede Quelle."
    )

# Der Mittelwert merkt sich eine Kopie der Liste
liste = [Fuehler("a", 4)]
mittel = Mittelwert("m", liste)
liste.append(Fuehler("b", 100))
assert mittel.messe() == 4.0, (
    f"Nachdem an die übergebene Liste noch ein Fühler angehängt wurde, misst der Mittelwert {mittel.messe()!r}, "
    "erwartet war weiterhin 4.0.\nTipp: Speichern Sie list(quellen), nicht die Liste des Aufrufers."
)

# 300 zufällige Listen aus Objekten aller Art
zufall = Zufall(5016)
for _ in range(300):
    quellen = []
    erwartete_werte = {}
    erwartet_abgelehnt = []
    for position in range(zufall.randint(0, 8)):
        art = zufall.randint(0, 5)
        wert = zufall.choice([0, -1.5, 10**6, -(10**6), zufall.randint(-100, 100)])
        if art == 0:
            quellen.append(Fuehler(f"f{position}", wert))
            erwartete_werte[f"f{position}"] = wert
        elif art == 1:
            quellen.append(CpuLast(f"c{position}", [wert, 0]))
            erwartete_werte[f"c{position}"] = wert
        elif art == 2:
            quellen.append(Mittelwert(f"m{position}", [Fuehler("x", wert), Fuehler("y", wert)]))
            erwartete_werte[f"m{position}"] = wert
        else:
            quellen.append(zufall.choice([NurName(), NurMessen(), "text", wert, None, (1, 2)]))
            erwartet_abgelehnt.append(position)
    ergebnis = abfragen(quellen)
    assert ergebnis == (erwartete_werte, erwartet_abgelehnt), (
        f"abfragen für {[type(objekt).__name__ for objekt in quellen]} ergibt {ergebnis!r}, erwartet war "
        f"{(erwartete_werte, erwartet_abgelehnt)!r}."
    )

# An der oberen Grenze: 10 000 Objekte und ein Mittelwert aus 1000 Quellen
quellen = [Fuehler(f"f{nummer}", nummer) if nummer % 4 else "kaputt" for nummer in range(10000)]
werte, abgelehnt = abfragen(quellen)
mittel = Mittelwert("alle", [Fuehler(f"g{nummer}", nummer) for nummer in range(1000)])
assert len(werte) == 7500 and abgelehnt[:3] == [0, 4, 8] and len(abgelehnt) == 2500 and mittel.messe() == 499.5, (
    f"Mit 10 000 Objekten liefert abfragen {len(werte)} Werte und {len(abgelehnt)} abgelehnte Positionen, der Mittelwert "
    f"aus 0 bis 999 ist {mittel.messe()!r}; erwartet waren 7500, 2500 und 499.5."
)
