# Automatisch erzeugt aus lehrkraft/muster/5_056_bandbreitenanteile.py - nicht von Hand ändern.
# vorlage-hash: e6b01622a6a8f9c9
# text-hash: 70e285fda06650a2
# thema: texte_zahlen
# inhalt: fractions.Fraction

import math
from fractions import Fraction


def wert_von(funktion, *argumente):
    """Ruft funktion mit Kopien der Dictionaries auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    kopien = [dict(argument) if isinstance(argument, dict) else argument for argument in argumente]
    try:
        return funktion(*kopien), None
    except Exception as fehler:
        return None, fehler


def ausnahme(fehler):
    """Beschreibt eine gefangene Ausnahme für eine Meldung."""
    return f" ({type(fehler).__name__}: {fehler})" if fehler is not None else ""


def kurz(wert):
    """Kürzt lange Werte für Meldungen."""
    text = repr(wert)
    return text if len(text) <= 300 else text[:280] + " …"


def zuteilung_von_hand(gewichte, bandbreite):
    """Vergleichslösung: ganze Zahlen mit divmod; alle Reste haben denselben Nenner, die Summe der Gewichte."""
    summe = sum(gewichte.values())
    ergebnis = {}
    reste = []
    for position, (klasse, gewicht) in enumerate(gewichte.items()):
        ganz, rest = divmod(gewicht * bandbreite, summe)
        ergebnis[klasse] = ganz
        reste.append((-rest, position, klasse))
    reste.sort()
    for _, _, klasse in reste[: bandbreite - sum(ergebnis.values())]:
        ergebnis[klasse] += 1
    return ergebnis


def fehler_in_gewichten(anteile, ergebnis):
    """Prüft die Eigenschaften kleinster Gewichte; gibt None oder eine Beschreibung des Fehlers zurück."""
    if not isinstance(ergebnis, dict) or list(ergebnis) != list(anteile):
        return "erwartet war ein Dictionary mit denselben Klassen in derselben Reihenfolge"
    if not all(type(wert) is int for wert in ergebnis.values()):
        return "erwartet waren int-Werte"
    erste = next(klasse for klasse in anteile if anteile[klasse] > 0)
    for klasse in anteile:
        # gleiches Verhältnis: ergebnis[k] / ergebnis[erste] == anteile[k] / anteile[erste], über Kreuz multipliziert
        if ergebnis[klasse] * anteile[erste] != anteile[klasse] * ergebnis[erste]:
            return f"das Verhältnis von {klasse} zu {erste} stimmt nicht"
    if math.gcd(*ergebnis.values()) != 1:
        return f"alle Gewichte sind noch durch {math.gcd(*ergebnis.values())} teilbar, es geht kleiner"
    return None


def ist_bruch(wert):
    """True, wenn wert eine Fraction ist (kein float)."""
    return isinstance(wert, Fraction)


ANTEILE = {"sprache": Fraction(1, 2), "video": Fraction(1, 3), "standard": Fraction(1, 6)}

# anteile: das Beispiel
ergebnis, fehler = wert_von(anteile, GEWICHTE)
erwartet = {"sprache": Fraction(5, 12), "video": Fraction(1, 4), "geschaeft": Fraction(1, 6), "standard": Fraction(1, 6)}
assert ergebnis == erwartet, (
    f"anteile({GEWICHTE}) ergibt {kurz(ergebnis)}{ausnahme(fehler)},\nerwartet war {erwartet}.\n"
    "Tipp: Fraction(gewicht, summe) teilt exakt und kürzt von selbst."
)

# anteile: die Werte sind Brüche, keine float
ergebnis, fehler = wert_von(anteile, GEWICHTE)
assert ergebnis is not None and all(ist_bruch(wert) for wert in ergebnis.values()), (
    f"anteile({GEWICHTE}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}; erwartet waren Fraction-Werte.\n"
    "Tipp: gewicht / summe ist ein float; Fraction(gewicht, summe) bleibt exakt."
)

# anteile: andere Gewichte (nicht fest hinschreiben!)
gewichte = {"a": 7, "b": 21, "c": 14}
ergebnis, fehler = wert_von(anteile, gewichte)
erwartet = {"a": Fraction(1, 6), "b": Fraction(1, 2), "c": Fraction(1, 3)}
assert ergebnis == erwartet, f"anteile({gewichte}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet}."

# anteile: die Klassen in derselben Reihenfolge wie in gewichte
gewichte = {"zeta": 1, "alpha": 2, "mitte": 3}
ergebnis, fehler = wert_von(anteile, gewichte)
assert ergebnis is not None and list(ergebnis) == list(gewichte), (
    f"anteile({gewichte}) hat die Klassen in der Reihenfolge {list(ergebnis) if ergebnis else ergebnis}, "
    f"erwartet war {list(gewichte)}."
)

# anteile: die Anteile ergeben zusammen genau 1
gewichte = {f"klasse{i}": i for i in range(1, 8)}
ergebnis, fehler = wert_von(anteile, gewichte)
assert ergebnis is not None and sum(ergebnis.values()) == 1, (
    f"Die Anteile zu {gewichte} ergeben zusammen {sum(ergebnis.values()) if ergebnis else ergebnis!r}{ausnahme(fehler)}, "
    "erwartet war genau 1."
)

# anteile: Gewicht 0 ergibt den Anteil 0
gewichte = {"sprache": 3, "backup": 0}
ergebnis, fehler = wert_von(anteile, gewichte)
erwartet = {"sprache": Fraction(1), "backup": Fraction(0)}
assert ergebnis == erwartet, f"anteile({gewichte}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet}."

# anteile: eine einzige Klasse
ergebnis, fehler = wert_von(anteile, {"alles": 1000000})
assert ergebnis == {"alles": 1}, f"anteile({{'alles': 1000000}}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {{'alles': Fraction(1, 1)}}."

# gewichte_aus: das Beispiel
ergebnis, fehler = wert_von(gewichte_aus, ANTEILE)
erwartet = {"sprache": 3, "video": 2, "standard": 1}
assert ergebnis == erwartet, (
    f"gewichte_aus({ANTEILE}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet}.\n"
    "Tipp: Multiplizieren Sie alle Anteile mit dem kgV der Nenner (math.lcm)."
)

# gewichte_aus: die Gewichte sind ganze Zahlen (int)
ergebnis, fehler = wert_von(gewichte_aus, ANTEILE)
assert ergebnis is not None and all(type(wert) is int for wert in ergebnis.values()), (
    f"gewichte_aus({ANTEILE}) ergibt {kurz(ergebnis)}; erwartet waren int-Werte, keine Fraction oder float.\n"
    "Tipp: int(bruch) macht aus einem Bruch mit Nenner 1 eine ganze Zahl."
)

# gewichte_aus: Anteile, deren Summe nicht 1 ist, und kürzen (nicht fest hinschreiben!)
eingabe = {"sprache": Fraction(1, 4), "video": Fraction(1, 4), "daten": Fraction(1, 2), "rest": Fraction(1, 2)}
ergebnis, fehler = wert_von(gewichte_aus, eingabe)
erwartet = {"sprache": 1, "video": 1, "daten": 2, "rest": 2}
assert ergebnis == erwartet, (
    f"gewichte_aus({eingabe}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet}.\n"
    "Tipp: Nach dem Multiplizieren mit dem kgV teilen Sie durch den ggT aller Werte (math.gcd)."
)

# gewichte_aus: gleiche Nenner, die sich noch kürzen lassen
eingabe = {"a": Fraction(2, 9), "b": Fraction(4, 9), "c": Fraction(2, 3)}
ergebnis, fehler = wert_von(gewichte_aus, eingabe)
erwartet = {"a": 1, "b": 2, "c": 3}
assert ergebnis == erwartet, f"gewichte_aus({eingabe}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet}."

# gewichte_aus: der Anteil 0 bleibt 0
eingabe = {"sprache": Fraction(3, 10), "backup": Fraction(0), "video": Fraction(1, 5)}
ergebnis, fehler = wert_von(gewichte_aus, eingabe)
erwartet = {"sprache": 3, "backup": 0, "video": 2}
assert ergebnis == erwartet, f"gewichte_aus({eingabe}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet}."

# gewichte_aus: eine einzige Klasse
ergebnis, fehler = wert_von(gewichte_aus, {"alles": Fraction(3, 7)})
assert ergebnis == {"alles": 1}, f"gewichte_aus({{'alles': Fraction(3, 7)}}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {{'alles': 1}}."

# gewichte_aus: große, teilerfremde Nenner
eingabe = {"a": Fraction(1, 999983), "b": Fraction(1, 999979), "c": Fraction(1)}
ergebnis, fehler = wert_von(gewichte_aus, eingabe)
erwartet = {"a": 999979, "b": 999983, "c": 999983 * 999979}
assert ergebnis == erwartet, (
    f"gewichte_aus({eingabe}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet}.\n"
    "Tipp: Rechnen Sie exakt mit den Brüchen; mit float gehen bei so großen Nennern Stellen verloren."
)

# zuteilung: das Beispiel
ergebnis, fehler = wert_von(zuteilung, GEWICHTE, 1000)
erwartet = {"sprache": 417, "video": 250, "geschaeft": 167, "standard": 166}
assert ergebnis == erwartet, (
    f"zuteilung({GEWICHTE}, 1000) ergibt {kurz(ergebnis)}{ausnahme(fehler)},\nerwartet war {erwartet}.\n"
    "Tipp: Erst alle genauen Anteile abrunden, dann die fehlenden kbit/s nach absteigendem Rest verteilen; bei "
    "gleichem Rest gewinnt die frühere Klasse."
)

# zuteilung: die Summe ist genau die Bandbreite
gewichte = {"a": 1, "b": 1, "c": 1}
ergebnis, fehler = wert_von(zuteilung, gewichte, 100)
assert ergebnis is not None and sum(ergebnis.values()) == 100, (
    f"zuteilung({gewichte}, 100) ergibt {kurz(ergebnis)}{ausnahme(fehler)}; zusammen sind das "
    f"{sum(ergebnis.values()) if ergebnis else ergebnis!r} kbit/s, erwartet waren genau 100.\n"
    "Tipp: Mit round statt Abrunden und Verteilen kommen 99 oder 101 heraus."
)

# zuteilung: die Werte sind ganze Zahlen
ergebnis, fehler = wert_von(zuteilung, GEWICHTE, 1000)
assert ergebnis is not None and all(type(wert) is int for wert in ergebnis.values()), (
    f"zuteilung({GEWICHTE}, 1000) ergibt {kurz(ergebnis)}; erwartet waren int-Werte.\n"
    "Tipp: math.floor(bruch) ist ein int."
)

# zuteilung: bei gleichem Rest gewinnt die frühere Klasse (nicht fest hinschreiben!)
gewichte = {"a": 1, "b": 1, "c": 1}
ergebnis, fehler = wert_von(zuteilung, gewichte, 101)
erwartet = {"a": 34, "b": 34, "c": 33}
assert ergebnis == erwartet, (
    f"zuteilung({gewichte}, 101) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet}.\n"
    "Tipp: sorted ist stabil; sortieren Sie nur nach dem Rest, absteigend (reverse=True oder minus Rest)."
)

# zuteilung: gleiche Reste, die float verschieden ausrechnet
gewichte = {"sprache": 10, "steuerung": 1, "video": 4, "standard": 3}
ergebnis, fehler = wert_von(zuteilung, gewichte, 1000)
erwartet = zuteilung_von_hand(gewichte, 1000)
assert ergebnis == erwartet, (
    f"zuteilung({gewichte}, 1000) ergibt {kurz(ergebnis)}{ausnahme(fehler)},\nerwartet war {erwartet}.\n"
    "sprache und steuerung haben genau denselben Rest 5/9, darum bekommt sprache die zusätzliche kbit/s.\n"
    "Tipp: Mit float sind die beiden Reste minimal verschieden; rechnen Sie mit Fraction."
)

# zuteilung: der größte Rest gewinnt, auch wenn die Klasse weiter hinten steht
gewichte = {"a": 1, "b": 2}
ergebnis, fehler = wert_von(zuteilung, gewichte, 10)
erwartet = {"a": 3, "b": 7}
assert ergebnis == erwartet, (
    f"zuteilung({gewichte}, 10) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet} "
    "(genau 3 1/3 und 6 2/3; der Rest 2/3 von b ist größer)."
)

# zuteilung: Gewicht 0 bekommt nichts
gewichte = {"sprache": 1, "backup": 0, "video": 1}
ergebnis, fehler = wert_von(zuteilung, gewichte, 7)
erwartet = {"sprache": 4, "backup": 0, "video": 3}
assert ergebnis == erwartet, f"zuteilung({gewichte}, 7) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet}."

# zuteilung: Bandbreite 0
ergebnis, fehler = wert_von(zuteilung, GEWICHTE, 0)
erwartet = {"sprache": 0, "video": 0, "geschaeft": 0, "standard": 0}
assert ergebnis == erwartet, f"zuteilung({GEWICHTE}, 0) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {erwartet}."

# zuteilung: Bandbreite, die genau aufgeht
gewichte = {"a": 3, "b": 1}
ergebnis, fehler = wert_von(zuteilung, gewichte, 400)
assert ergebnis == {"a": 300, "b": 100}, f"zuteilung({gewichte}, 400) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {{'a': 300, 'b': 100}}."

# zuteilung: eine einzige Klasse
ergebnis, fehler = wert_von(zuteilung, {"alles": 5}, 999)
assert ergebnis == {"alles": 999}, f"zuteilung({{'alles': 5}}, 999) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {{'alles': 999}}."

zufall = Zufall(5056)

# anteile und gewichte_aus: 300 zufällige Gewichte hin und zurück
for _ in range(300):
    gewichte = {f"k{i}": zufall.choice([0, zufall.randint(1, 12), zufall.randint(1, 10**6)]) for i in range(zufall.randint(1, 8))}
    gewichte["k0"] = zufall.randint(1, 50)
    ergebnis, fehler = wert_von(anteile, gewichte)
    summe = sum(gewichte.values())
    erwartet = {klasse: Fraction(gewicht, summe) for klasse, gewicht in gewichte.items()}
    assert ergebnis == erwartet, f"anteile({gewichte}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {kurz(erwartet)}."
    ergebnis, fehler = wert_von(gewichte_aus, erwartet)
    teiler = math.gcd(*gewichte.values())
    gekuerzt = {klasse: gewicht // teiler for klasse, gewicht in gewichte.items()}
    assert ergebnis == gekuerzt, (
        f"gewichte_aus({kurz(erwartet)}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}, erwartet war {kurz(gekuerzt)}."
    )

# gewichte_aus: 300 zufällige Brüche mit verschiedenen Nennern
for _ in range(300):
    eingabe = {}
    for i in range(zufall.randint(1, 6)):
        nenner = zufall.randint(1, 60)
        eingabe[f"k{i}"] = Fraction(zufall.randint(0, nenner), nenner)
    eingabe["k0"] = Fraction(zufall.randint(1, 9), 10)
    ergebnis, fehler = wert_von(gewichte_aus, eingabe)
    problem = fehler_in_gewichten(eingabe, ergebnis)
    assert problem is None, f"gewichte_aus({eingabe}) ergibt {kurz(ergebnis)}{ausnahme(fehler)}; {problem}."

# zuteilung: 500 zufällige Gewichte und Bandbreiten
for _ in range(500):
    gewichte = {f"k{i}": zufall.randint(0, zufall.choice([3, 12, 10**6])) for i in range(zufall.randint(1, 8))}
    gewichte["k0"] = zufall.randint(1, 12)
    bandbreite = zufall.choice([zufall.randint(0, 100), zufall.randint(0, 10**4), zufall.randint(0, 10**9)])
    ergebnis, fehler = wert_von(zuteilung, gewichte, bandbreite)
    erwartet = zuteilung_von_hand(gewichte, bandbreite)
    assert ergebnis == erwartet, (
        f"zuteilung({gewichte}, {bandbreite}) ergibt {kurz(ergebnis)}{ausnahme(fehler)},\nerwartet war {erwartet}."
    )

# Obere Grenze: 50 Klassen mit großen Gewichten und 10**9 kbit/s
gewichte = {f"klasse{i:02d}": zufall.randint(0, 10**6) for i in range(50)}
gewichte["klasse00"] = 10**6
ergebnis, fehler = wert_von(zuteilung, gewichte, 10**9)
erwartet = zuteilung_von_hand(gewichte, 10**9)
assert ergebnis == erwartet, f"zuteilung für 50 Klassen und 10**9 kbit/s ergibt {kurz(ergebnis)}{ausnahme(fehler)},\nerwartet war {kurz(erwartet)}."

# Obere Grenze: gewichte_aus mit 50 Anteilen und Nennern bis 10**6
eingabe = {f"klasse{i:02d}": Fraction(zufall.randint(0, 10**6), 10**6) for i in range(50)}
eingabe["klasse00"] = Fraction(1, 999983)
ergebnis, fehler = wert_von(gewichte_aus, eingabe)
problem = fehler_in_gewichten(eingabe, ergebnis)
assert problem is None, f"gewichte_aus für 50 Anteile mit Nennern bis 10**6 ergibt {kurz(ergebnis)}{ausnahme(fehler)}; {problem}."
