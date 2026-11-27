# Automatisch erzeugt aus lehrkraft/muster/5_062_messverdichtung.py - nicht von Hand ändern.
# vorlage-hash: 004bc178a0d10f9a
# text-hash: 047dd006a5371207
# thema: funktionen
# inhalt: Strategie und Beobachter mit Funktionen

import math


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def gleich(a, b):
    """Vergleicht zwei Listen von Zahlen oder None mit Toleranz für Kommazahlen."""
    if a is None or b is None or len(a) != len(b):
        return a == b
    for x, y in zip(a, b):
        if (x is None) != (y is None):
            return False
        if x is not None and not math.isclose(x, y, rel_tol=1e-9, abs_tol=1e-6):
            return False
    return True


def perzentil_von(p, werte):
    """Vergleichslösung: zählt ab dem kleinsten Wert, bis mindestens p Prozent erreicht sind."""
    sortiert = sorted(werte)
    for stelle in range(1, len(sortiert) + 1):
        if 100 * stelle >= p * len(sortiert):
            return sortiert[stelle - 1]
    return None


class Mitschrift:
    """Ein Beobachter als Objekt mit __call__, der jeden Aufruf mitschreibt."""

    def __init__(self, name="mitschrift"):
        """Legt eine leere Liste der Aufrufe an."""
        self.name = name
        self.aufrufe = []

    def __call__(self, name, wert):
        """Schreibt den Aufruf (name, wert) mit."""
        self.aufrufe.append((name, wert))


def erfasse_alle(kennzahl, werte):
    """Ruft erfasse für jeden Wert auf; liefert die Liste der Rückgaben."""
    return [kennzahl.erfasse(wert) for wert in werte]


# mittelwert: das Beispiel
ergebnis, fehler = rufe(lambda: mittelwert([120, 180, 150]))
assert ergebnis == 150, f"mittelwert([120, 180, 150]) ergibt {ergebnis!r}, erwartet war 150.0." + absturz(fehler)

# mittelwert: Kommazahlen, negative Werte und ein einzelner Wert
ergebnis, fehler = rufe(lambda: (mittelwert([1.5, 2.0]), mittelwert([-3, 4]), mittelwert([42])))
assert ergebnis is not None and gleich(list(ergebnis), [1.75, 0.5, 42]), (
    f"mittelwert([1.5, 2.0]), mittelwert([-3, 4]) und mittelwert([42]) ergeben {ergebnis!r}, erwartet war "
    "(1.75, 0.5, 42.0)." + absturz(fehler)
)

# perzentil: perzentil(p) gibt eine Funktion zurück
ergebnis, fehler = rufe(lambda: perzentil(50))
assert callable(ergebnis), (
    f"perzentil(50) ergibt {ergebnis!r}, erwartet war eine Funktion, die man mit einer Liste aufruft.\n"
    "Tipp: Definieren Sie in perzentil eine innere Funktion strategie(werte) und geben Sie sie zurück." + absturz(fehler)
)

# perzentil: das Beispiel mit p = 95
ergebnis, fehler = rufe(lambda: perzentil(95)([12, 50, 7, 31]))
assert ergebnis == 50, (
    f"perzentil(95)([12, 50, 7, 31]) ergibt {ergebnis!r}, erwartet war 50: sortiert 7, 12, 31, 50, rang ist die "
    "kleinste ganze Zahl ≥ 95 · 4 / 100 = 3.8, also 4." + absturz(fehler)
)

# perzentil: geht p · len(werte) / 100 genau auf, ist das der Rang
ergebnis, fehler = rufe(lambda: perzentil(50)([12, 50, 7, 31]))
assert ergebnis == 12, (
    f"perzentil(50)([12, 50, 7, 31]) ergibt {ergebnis!r}, erwartet war 12: rang 2 (50 · 4 / 100 = 2.0 genau)."
    + absturz(fehler)
)

# perzentil: der Rang wird aufgerundet, nicht gerundet
ergebnis, fehler = rufe(lambda: perzentil(60)([12, 50, 7, 31]))
assert ergebnis == 31, (
    f"perzentil(60)([12, 50, 7, 31]) ergibt {ergebnis!r}, erwartet war 31: 60 · 4 / 100 = 2.4, aufgerundet rang 3."
    + absturz(fehler)
)

# perzentil: der Rang wird aufgerundet, auch knapp über einer ganzen Zahl
ergebnis, fehler = rufe(lambda: perzentil(26)([12, 50, 7, 31]))
assert ergebnis == 12, (
    f"perzentil(26)([12, 50, 7, 31]) ergibt {ergebnis!r}, erwartet war 12: 26 · 4 / 100 = 1.04, aufgerundet rang 2."
    + absturz(fehler)
)

# perzentil: p = 100 ist das Maximum, p = 1 bei wenigen Werten das Minimum
ergebnis, fehler = rufe(lambda: (perzentil(100)([3, 9, 1]), perzentil(1)([3, 9, 1]), perzentil(1)([8])))
assert ergebnis == (9, 1, 8), (
    f"perzentil(100)([3, 9, 1]), perzentil(1)([3, 9, 1]) und perzentil(1)([8]) ergeben {ergebnis!r}, erwartet war "
    "(9, 1, 8)." + absturz(fehler)
)

# perzentil: kein Rundungsfehler bei p · n / 100
ergebnis, fehler = rufe(lambda: perzentil(7)(list(range(100))))
assert ergebnis == 6, (
    f"perzentil(7)([0, 1, …, 99]) ergibt {ergebnis!r}, erwartet war 6 (rang genau 7)."
    + ("\nTipp: Der Rang ist genau 7, also kommt der siebte Wert (6). Achtung: 7 / 100 * 100 ist 7.000000000000001 und "
       "würde zu 8 aufgerundet; rechnen Sie (p * n + 99) // 100." if ergebnis == 7 else "")
    + absturz(fehler)
)

# perzentil: die Liste bleibt unverändert
werte = [12, 50, 7, 31]
ergebnis, fehler = rufe(lambda: perzentil(95)(werte))
assert werte == [12, 50, 7, 31], (
    f"perzentil(95)(werte) hat werte zu {werte!r} verändert.\nTipp: sorted(werte) gibt eine neue Liste zurück, "
    "werte.sort() sortiert die Liste selbst." + absturz(fehler)
)

# alarm_ab: meldet nur Werte über der Schwelle
meldungen = []
ergebnis, fehler = rufe(lambda: alarm_ab(200, meldungen))
if callable(ergebnis):
    for wert in [150, 280, 200, 201.5]:
        ergebnis("api", wert)
assert meldungen == [("api", 280), ("api", 201.5)], (
    f"Ein Beobachter alarm_ab(200, meldungen), aufgerufen mit den Werten 150, 280, 200 und 201.5, hinterlässt "
    f"meldungen = {meldungen!r}, erwartet war [('api', 280), ('api', 201.5)] (200 ist nicht größer als 200)."
    + ("" if callable(ergebnis) else f"\nalarm_ab gibt {ergebnis!r} zurück statt einer Funktion.") + absturz(fehler)
)

# alarm_ab: zwei Alarme sind unabhängig voneinander
hoch, niedrig = [], []
ergebnis, fehler = rufe(lambda: (alarm_ab(90, hoch), alarm_ab(-5, niedrig)))
if ergebnis and all(callable(teil) for teil in ergebnis):
    ergebnis[0]("cpu", 50)
    ergebnis[1]("frost", -2)
    ergebnis[0]("cpu", 95)
assert (hoch, niedrig) == ([("cpu", 95)], [("frost", -2)]), (
    f"Zwei Beobachter alarm_ab(90, hoch) und alarm_ab(-5, niedrig) hinterlassen hoch = {hoch!r} und niedrig = "
    f"{niedrig!r}, erwartet war [('cpu', 95)] und [('frost', -2)]." + absturz(fehler)
)

# erfasse: das Beispiel mit Mittelwert und Fenster 3
kennzahl = Kennzahl("api.antwortzeit", mittelwert, 3)
ergebnis, fehler = rufe(lambda: erfasse_alle(kennzahl, [120, 180, 150, 240, 310, 290]))
assert gleich(ergebnis, [None, None, 150, None, None, 280]), (
    f"erfasse mit 120, 180, 150, 240, 310, 290 bei Fenster 3 ergibt {ergebnis!r}, erwartet war "
    "[None, None, 150.0, None, None, 280.0]."
    + ("\nTipp: Beginnen Sie nach dem Verdichten ein leeres Fenster." if ergebnis and len(ergebnis) == 6 and ergebnis[5] is None else "")
    + absturz(fehler)
)

# erfasse: Fenster 1 verdichtet jeden Wert einzeln, andere Strategie
kennzahl = Kennzahl("temperatur", max, 1)
ergebnis, fehler = rufe(lambda: erfasse_alle(kennzahl, [21.5, -3, 0]))
assert ergebnis == [21.5, -3, 0], (
    f"erfasse mit 21.5, -3, 0 bei Fenster 1 und Strategie max ergibt {ergebnis!r}, erwartet war [21.5, -3, 0]."
    + absturz(fehler)
)

# erfasse: die Strategie ist austauschbar und gilt ab dem nächsten vollen Fenster
kennzahl = Kennzahl("cpu", max, 2)


def tauschen():
    """Erfasst zwei Fenster mit max, tauscht mitten im dritten die Strategie und erfasst weiter."""
    rueckgaben = erfasse_alle(kennzahl, [10, 40, 30, 20, 5])
    kennzahl.strategie = min
    return rueckgaben + erfasse_alle(kennzahl, [70, 60, 50])


ergebnis, fehler = rufe(tauschen)
assert ergebnis == [None, 40, None, 30, None, 5, None, 50], (
    f"Fenster 2 mit max für 10, 40, 30, 20, 5, dann strategie = min und weiter mit 70, 60, 50: erfasse ergibt "
    f"{ergebnis!r}, erwartet war [None, 40, None, 30, None, 5, None, 50] (das Fenster 5, 70 wird mit min verdichtet)."
    + ("\nTipp: Rufen Sie self.strategie erst beim Verdichten auf, nicht schon in __init__." if ergebnis and ergebnis[5] == 70 else "")
    + absturz(fehler)
)

# erfasse: eine Strategie aus perzentil
kennzahl = Kennzahl("api", perzentil(95), 4)
ergebnis, fehler = rufe(lambda: erfasse_alle(kennzahl, [12, 50, 7, 31]))
assert ergebnis == [None, None, None, 50], f"erfasse mit perzentil(95) und Fenster 4 für 12, 50, 7, 31 ergibt {ergebnis!r}, erwartet war [None, None, None, 50]." + absturz(fehler)

# Beobachter: ein aufrufbares Objekt wird mit (name, wert) benachrichtigt
kennzahl = Kennzahl("ram", max, 2)
mitschrift = Mitschrift()
ergebnis, fehler = rufe(lambda: (kennzahl.anmelden(mitschrift), erfasse_alle(kennzahl, [3, 8, 6, 1, 9])))
assert mitschrift.aufrufe == [("ram", 8), ("ram", 6)], (
    f"Ein angemeldeter Beobachter bei Fenster 2 mit max und den Werten 3, 8, 6, 1, 9 wurde mit "
    f"{mitschrift.aufrufe!r} aufgerufen, erwartet war [('ram', 8), ('ram', 6)]." + absturz(fehler)
)

# Beobachter: anmelden gibt den Beobachter zurück (geht auch als Dekorator)
kennzahl = Kennzahl("ram", max, 1)
ergebnis, fehler = rufe(lambda: kennzahl.anmelden(mitschrift))
assert ergebnis is mitschrift, (
    f"kennzahl.anmelden(beobachter) gibt {ergebnis!r} zurück, erwartet war der Beobachter selbst.\n"
    "Tipp: return beobachter am Ende von anmelden." + absturz(fehler)
)

# Beobachter: alle, in der Reihenfolge der Anmeldung
kennzahl = Kennzahl("api.antwortzeit", mittelwert, 3)
dashboard, export, alarme, reihenfolge = Dashboard(), [], [], []


def alle_anmelden():
    """Meldet die vier Beobachter aus dem Beispiel an und erfasst die sechs Werte."""
    kennzahl.anmelden(dashboard.zeige)
    kennzahl.anmelden(partial(exportiere, export))
    kennzahl.anmelden(alarm_ab(200, alarme))
    kennzahl.anmelden(lambda name, wert: reihenfolge.append("lambda"))
    kennzahl.anmelden(lambda name, wert: reihenfolge.append("zweite lambda"))
    return erfasse_alle(kennzahl, [120, 180, 150, 240, 310, 290])


ergebnis, fehler = rufe(alle_anmelden)
# 150 statt 150.0 im Export ist auch richtig (ganze Zahlen dürfen int bleiben)
assert (dashboard.anzeige, [vergleichbar(zeile) for zeile in export], alarme, reihenfolge) == (
    {"api.antwortzeit": 280.0},
    [vergleichbar("api.antwortzeit;150.0"), vergleichbar("api.antwortzeit;280.0")],
    [("api.antwortzeit", 280.0)],
    ["lambda", "zweite lambda", "lambda", "zweite lambda"],
), (
    "Mit den Beobachtern aus dem Beispiel und zwei Lambdas danach ergeben sich\n"
    f"  dashboard.anzeige = {dashboard.anzeige!r}\n  export = {export!r}\n  alarme = {alarme!r}\n"
    f"  Aufrufe der Lambdas: {reihenfolge!r}\nerwartet war {{'api.antwortzeit': 280.0}}, "
    "['api.antwortzeit;150.0', 'api.antwortzeit;280.0'], [('api.antwortzeit', 280.0)] und "
    "['lambda', 'zweite lambda', 'lambda', 'zweite lambda']." + absturz(fehler)
)

# Beobachter: doppelt anmelden benachrichtigt trotzdem nur einmal
kennzahl = Kennzahl("ram", max, 1)
mitschrift = Mitschrift()
ergebnis, fehler = rufe(lambda: (kennzahl.anmelden(mitschrift), kennzahl.anmelden(mitschrift), kennzahl.erfasse(7)))
assert mitschrift.aufrufe == [("ram", 7)], (
    f"Ein zweimal angemeldeter Beobachter wird bei einem verdichteten Wert mit {mitschrift.aufrufe!r} aufgerufen, "
    "erwartet war genau einmal [('ram', 7)]." + absturz(fehler)
)

# Beobachter: abmelden beendet die Benachrichtigung
kennzahl = Kennzahl("ram", max, 1)
erste, zweite = Mitschrift(), Mitschrift()


def an_und_ab():
    """Meldet zwei Beobachter an, erfasst einen Wert, meldet den ersten ab und erfasst noch einen."""
    kennzahl.anmelden(erste)
    kennzahl.anmelden(zweite)
    kennzahl.erfasse(1)
    kennzahl.abmelden(erste)
    kennzahl.erfasse(2)


ergebnis, fehler = rufe(an_und_ab)
assert (erste.aufrufe, zweite.aufrufe) == ([("ram", 1)], [("ram", 1), ("ram", 2)]), (
    f"Nach anmelden(erste), anmelden(zweite), erfasse(1), abmelden(erste), erfasse(2) wurde der erste mit "
    f"{erste.aufrufe!r}, der zweite mit {zweite.aufrufe!r} aufgerufen; erwartet war [('ram', 1)] und "
    "[('ram', 1), ('ram', 2)]." + absturz(fehler)
)

# Beobachter: eine gebundene Methode lässt sich wieder abmelden (== statt is)
kennzahl = Kennzahl("cpu", max, 1)
dashboard = Dashboard()


def methode_an_und_ab():
    """Meldet dashboard.zeige an, erfasst, meldet dashboard.zeige ab und erfasst noch einmal."""
    kennzahl.anmelden(dashboard.zeige)
    kennzahl.erfasse(30)
    kennzahl.abmelden(dashboard.zeige)
    kennzahl.erfasse(99)


ergebnis, fehler = rufe(methode_an_und_ab)
assert fehler is None and dashboard.anzeige == {"cpu": 30}, (
    f"anmelden(dashboard.zeige), erfasse(30), abmelden(dashboard.zeige), erfasse(99) ergibt dashboard.anzeige = "
    f"{dashboard.anzeige!r}, erwartet war {{'cpu': 30}}.\nTipp: dashboard.zeige ist bei jedem Zugriff ein neues "
    "Methodenobjekt; vergleichen Sie mit == (in, remove), nicht mit is." + absturz(fehler)
)

# Beobachter: abmelden eines nicht angemeldeten Beobachters löst ValueError aus
kennzahl = Kennzahl("cpu", max, 1)
try:
    kennzahl.abmelden(Mitschrift())
    ausnahme = None
except Exception as fehler:
    ausnahme = fehler
assert isinstance(ausnahme, ValueError), (
    "kennzahl.abmelden(...) für einen nicht angemeldeten Beobachter löst "
    + (f"{ausnahme!r}" if ausnahme else "keine Ausnahme") + " aus, erwartet war ein ValueError."
)

# Beobachter: wer sich während der Benachrichtigung abmeldet, überspringt niemanden
kennzahl = Kennzahl("cpu", max, 1)
einmalig_aufrufe, danach = [], Mitschrift()


def einmalig(name, wert):
    """Ein Beobachter, der sich beim ersten Aufruf selbst abmeldet."""
    einmalig_aufrufe.append(wert)
    kennzahl.abmelden(einmalig)


ergebnis, fehler = rufe(lambda: (kennzahl.anmelden(einmalig), kennzahl.anmelden(danach), erfasse_alle(kennzahl, [5, 6])))
assert (einmalig_aufrufe, danach.aufrufe) == ([5], [("cpu", 5), ("cpu", 6)]), (
    f"Ein Beobachter, der sich beim ersten Aufruf selbst abmeldet, wurde mit {einmalig_aufrufe!r} aufgerufen, der "
    f"danach angemeldete mit {danach.aufrufe!r}; erwartet war [5] und [('cpu', 5), ('cpu', 6)].\n"
    "Tipp: Wer über self.beobachter selbst läuft, während remove die Liste ändert, überspringt den nächsten; laufen "
    "Sie über eine Kopie." + absturz(fehler)
)

zufall = Zufall(5062)

# Viele zufällige Messreihen mit zufälligen Strategien und Fenstern
for _ in range(200):
    fenster = zufall.randint(1, 6)
    p = zufall.randint(1, 100)
    art = zufall.choice(["mittelwert", "max", "min", "perzentil"])
    werte = [zufall.choice([zufall.randint(-10**9, 10**9), zufall.randint(-5, 5), zufall.uniform(-100, 100)]) for _ in range(zufall.randint(0, 20))]
    strategie = {"mittelwert": mittelwert, "max": max, "min": min}.get(art) or perzentil(p)
    vergleich = {"mittelwert": lambda w: sum(w) / len(w), "max": max, "min": min}.get(art) or (lambda w: perzentil_von(p, w))
    erwartet = [None] * len(werte)
    for ende in range(fenster, len(werte) + 1, fenster):
        erwartet[ende - 1] = vergleich(werte[ende - fenster:ende])
    kennzahl = Kennzahl("k", strategie, fenster)
    mitschrift = Mitschrift()
    ergebnis, fehler = rufe(lambda: (kennzahl.anmelden(mitschrift), erfasse_alle(kennzahl, werte))[1])
    gemeldet = [wert for _, wert in mitschrift.aufrufe]
    beschreibung = art if art != "perzentil" else f"perzentil({p})"
    assert gleich(ergebnis, erwartet) and gleich(gemeldet, [w for w in erwartet if w is not None]), (
        f"Mit Strategie {beschreibung}, Fenster {fenster} und den Werten {werte} ergibt erfasse\n{ergebnis!r}\n"
        f"und der Beobachter bekommt {gemeldet!r};\nerwartet war\n{erwartet!r}." + absturz(fehler)
    )

# Viele zufällige An- und Abmeldungen im Vergleich mit einer Liste
for _ in range(100):
    kennzahl = Kennzahl("k", max, 1)
    beobachter = [Mitschrift(f"b{nummer}") for nummer in range(4)]
    angemeldet = []
    schritte = []
    for runde in range(15):
        wer = zufall.choice(beobachter)
        aktion = zufall.choice(["anmelden", "abmelden", "erfasse"])
        schritte.append(f"{aktion}({wer.name})" if aktion != "erfasse" else f"erfasse({runde})")
        if aktion == "anmelden":
            ergebnis, fehler = rufe(lambda: kennzahl.anmelden(wer))
            if wer not in angemeldet:
                angemeldet.append(wer)
            ok = fehler is None
        elif aktion == "abmelden":
            try:
                kennzahl.abmelden(wer)
                fehler = None
            except ValueError as ausnahme:
                fehler = ausnahme
            ok = (fehler is None) == (wer in angemeldet)
            if wer in angemeldet:
                angemeldet.remove(wer)
        else:
            vorher = [len(b.aufrufe) for b in beobachter]
            ergebnis, fehler = rufe(lambda: kennzahl.erfasse(runde))
            nachher = [len(b.aufrufe) for b in beobachter]
            ok = fehler is None and [n - v for v, n in zip(vorher, nachher)] == [int(b in angemeldet) for b in beobachter]
        assert ok, (
            f"Nach {', '.join(schritte)} stimmt etwas nicht: angemeldet sein sollten {[b.name for b in angemeldet]}"
            + (f"; der letzte Schritt löst {fehler!r} aus" if fehler else "")
            + (" (abmelden eines nicht angemeldeten Beobachters muss ValueError auslösen)" if aktion == "abmelden" else "")
            + "."
        )

# Obere Grenze: 200000 Werte mit Fenster 10000 und perzentil(95)
werte = [(nummer * 7919) % 100_003 for nummer in range(200_000)]
kennzahl = Kennzahl("api", perzentil(95), 10_000)
mitschrift = Mitschrift()
ergebnis, fehler = rufe(lambda: (kennzahl.anmelden(mitschrift), erfasse_alle(kennzahl, werte))[1])
erwartet = [perzentil_von(95, werte[start:start + 10_000]) for start in range(0, 200_000, 10_000)]
assert ergebnis is not None and [w for w in ergebnis if w is not None] == erwartet and len(mitschrift.aufrufe) == 20, (
    f"Mit 200000 Werten, Fenster 10000 und perzentil(95) ergeben sich {None if ergebnis is None else sum(w is not None for w in ergebnis)} "
    f"verdichtete Werte und {len(mitschrift.aufrufe)} Benachrichtigungen, erwartet waren je 20, "
    f"beginnend mit {erwartet[:3]}." + absturz(fehler)
)

# Obere Grenze: 200000 Werte mit Fenster 1 und 10 Beobachtern
kennzahl = Kennzahl("cpu", max, 1)
beobachter = [Mitschrift() for _ in range(10)]
ergebnis, fehler = rufe(lambda: ([kennzahl.anmelden(b) for b in beobachter], erfasse_alle(kennzahl, range(200_000)))[1])
assert ergebnis == list(range(200_000)) and all(len(b.aufrufe) == 200_000 for b in beobachter), (
    f"Mit 200000 Werten, Fenster 1 und 10 Beobachtern bekommen die Beobachter {[len(b.aufrufe) for b in beobachter]} "
    "Benachrichtigungen, erwartet waren je 200000." + absturz(fehler)
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE.splitlines()[0]) == vergleichbar("[None, None, 150.0, None, None, 280.0]"), (
    f"Die erste Zeile der Ausgabe ist {AUSGABE.splitlines()[0]!r}, erwartet war '[None, None, 150.0, None, None, 280.0]'."
)
