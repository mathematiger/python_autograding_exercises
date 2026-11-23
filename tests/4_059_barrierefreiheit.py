# Automatisch erzeugt aus lehrkraft/muster/4_059_barrierefreiheit.py - nicht von Hand ändern.
# vorlage-hash: c6a07ac6ca95620a
# text-hash: db5f85377e0fbb0a
# thema: datenstrukturen
# inhalt: collections.Counter

from collections import Counter

BEISPIEL = [
    ("/start", "alt-text"),
    ("/antrag", "label"),
    ("/antrag", "kontrast"),
    ("/termine", "label"),
    ("/start", "kontrast"),
    ("/antrag", "label"),
]


def wert_von(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_je_regel(befunde):
    """Vergleichslösung mit einem gewöhnlichen Dictionary."""
    anzahlen = {}
    for _seite, regel in befunde:
        anzahlen[regel] = anzahlen.get(regel, 0) + 1
    return anzahlen


def vergleich_dringendste(befunde, n):
    """Vergleichslösung: sortiert nach Anzahl absteigend, dann nach erstem Auftreten."""
    anzahlen = vergleich_je_regel(befunde)
    zuerst = {}
    for stelle, (_seite, regel) in enumerate(befunde):
        zuerst.setdefault(regel, stelle)
    reihenfolge = sorted(anzahlen, key=lambda regel: (-anzahlen[regel], zuerst[regel]))
    return [(regel, anzahlen[regel]) for regel in reihenfolge[:n]]


def vergleich_differenz(a, b):
    """Vergleichslösung: für jede Regel a minus b, nur positive Ergebnisse."""
    ergebnis = {}
    for regel in a:
        if a[regel] - b.get(regel, 0) > 0:
            ergebnis[regel] = a[regel] - b.get(regel, 0)
    return ergebnis


def vergleich_gesamt(zaehlungen):
    """Vergleichslösung: addiert Eintrag für Eintrag."""
    summe = {}
    for zaehlung in zaehlungen:
        for regel, anzahl in zaehlung.items():
            summe[regel] = summe.get(regel, 0) + anzahl
    return summe


def als_dict(wert):
    """Ein Counter oder Dictionary als gewöhnliches Dictionary, alles andere unverändert."""
    if isinstance(wert, dict):
        return dict(wert)
    return wert


def meldung(aufruf, ergebnis, erwartet, tipp=""):
    """Fehlermeldung mit Aufruf, Ergebnis und erwartetem Wert."""
    return f"{aufruf} ergibt {ergebnis!r},\nerwartet war {erwartet!r}.{tipp}"


# je_regel im Beispiel: die Anzahlen stimmen
ergebnis = wert_von(je_regel, BEISPIEL)
assert als_dict(ergebnis) == vergleich_je_regel(BEISPIEL), meldung(
    "je_regel(befunde)", ergebnis, Counter(vergleich_je_regel(BEISPIEL)),
    "\nTipp: Counter(regel for seite, regel in befunde) zählt die Regeln.",
)

# je_regel gibt einen Counter zurück
assert isinstance(ergebnis, Counter), (
    f"je_regel(befunde) ergibt ein {type(ergebnis).__name__}, erwartet war ein Counter.\n"
    "Tipp: from collections import Counter steht schon oben; geben Sie Counter(...) zurück."
)

# je_regel mit anderen Befunden (nicht fest hinschreiben!)
befunde = [("/a", "sprache"), ("/b", "sprache"), ("/b", "fokus"), ("/c", "sprache")]
ergebnis = wert_von(je_regel, befunde)
assert als_dict(ergebnis) == vergleich_je_regel(befunde), meldung(f"je_regel({befunde})", ergebnis, vergleich_je_regel(befunde))

# je_regel zählt Regeln, nicht Seiten
befunde = [("/antrag", "label"), ("/antrag", "label"), ("/antrag", "kontrast")]
ergebnis = wert_von(je_regel, befunde)
assert als_dict(ergebnis) == {"label": 2, "kontrast": 1}, meldung(
    f"je_regel({befunde})", ergebnis, Counter({"label": 2, "kontrast": 1}),
    "\nTipp: Zählen Sie nur den zweiten Teil jedes Paares.",
)

# je_regel: keine Befunde
ergebnis = wert_von(je_regel, [])
assert als_dict(ergebnis) == {}, meldung("je_regel([])", ergebnis, Counter())

# dringendste im Beispiel
ergebnis = wert_von(dringendste, BEISPIEL, 2)
assert ergebnis == [("label", 3), ("kontrast", 2)], meldung(
    "dringendste(befunde, 2)", ergebnis, [("label", 3), ("kontrast", 2)], "\nTipp: most_common(n) liefert genau diese Liste."
)

# dringendste mit anderem n (nicht fest hinschreiben!)
ergebnis = wert_von(dringendste, BEISPIEL, 1)
assert ergebnis == [("label", 3)], meldung("dringendste(befunde, 1)", ergebnis, [("label", 3)])

# dringendste: bei gleicher Anzahl die Regel, die früher auftaucht
befunde = [("/a", "fokus"), ("/b", "sprache"), ("/c", "alt-text"), ("/d", "sprache"), ("/e", "fokus"), ("/f", "alt-text")]
ergebnis = wert_von(dringendste, befunde, 3)
assert ergebnis == vergleich_dringendste(befunde, 3), meldung(
    f"dringendste({befunde}, 3)", ergebnis, vergleich_dringendste(befunde, 3),
    "\nTipp: Sortieren Sie nicht nach dem Namen; most_common behält bei Gleichstand die Reihenfolge des ersten Auftretens.",
)

# dringendste: n größer als die Zahl der Regeln liefert alle
ergebnis = wert_von(dringendste, BEISPIEL, 10)
assert ergebnis == vergleich_dringendste(BEISPIEL, 10), meldung("dringendste(befunde, 10)", ergebnis, vergleich_dringendste(BEISPIEL, 10))

# dringendste: n = 0 liefert eine leere Liste
ergebnis = wert_von(dringendste, BEISPIEL, 0)
assert ergebnis == [], meldung("dringendste(befunde, 0)", ergebnis, [], "\nTipp: most_common(0) ist [], aber most_common() ohne Argument alles.")

# dringendste: keine Befunde
ergebnis = wert_von(dringendste, [], 3)
assert ergebnis == [], meldung("dringendste([], 3)", ergebnis, [])

# veraenderung im Beispiel: besser und schlechter
vorher = Counter({"label": 3, "kontrast": 2})
nachher = Counter({"label": 1, "kontrast": 2, "alt-text": 4})
ergebnis = wert_von(veraenderung, vorher, nachher)
erwartet = ({"label": 2}, {"alt-text": 4})
assert isinstance(ergebnis, tuple) and len(ergebnis) == 2 and tuple(als_dict(teil) for teil in ergebnis) == erwartet, meldung(
    "veraenderung(vorher, nachher)", ergebnis, (Counter({"label": 2}), Counter({"alt-text": 4})),
    "\nTipp: vorher - nachher behält nur, was positiv bleibt; nachher - vorher ebenso.",
)

# veraenderung mit anderen Zahlen (nicht fest hinschreiben!)
vorher = Counter({"fokus": 7, "sprache": 1, "alt-text": 5})
nachher = Counter({"fokus": 2, "sprache": 3, "alt-text": 5, "label": 1})
erwartet = (vergleich_differenz(vorher, nachher), vergleich_differenz(nachher, vorher))
ergebnis = wert_von(veraenderung, vorher, nachher)
assert isinstance(ergebnis, tuple) and tuple(als_dict(teil) for teil in ergebnis) == erwartet, meldung(
    "veraenderung(vorher, nachher)", ergebnis, erwartet,
    "\nTipp: Regeln ohne Veränderung (alt-text) dürfen nicht mit 0 darin stehen.",
)

# veraenderung: eine Regel ist ganz behoben
vorher = Counter({"label": 4, "kontrast": 1})
nachher = Counter({"kontrast": 1})
ergebnis = wert_von(veraenderung, vorher, nachher)
assert isinstance(ergebnis, tuple) and tuple(als_dict(teil) for teil in ergebnis) == ({"label": 4}, {}), meldung(
    "veraenderung(vorher, nachher)", ergebnis, (Counter({"label": 4}), Counter())
)

# veraenderung lässt beide Counter unverändert
vorher = Counter({"label": 3, "kontrast": 2})
nachher = Counter({"label": 1, "alt-text": 4})
wert_von(veraenderung, vorher, nachher)
assert dict(vorher) == {"label": 3, "kontrast": 2} and dict(nachher) == {"label": 1, "alt-text": 4}, (
    f"Nach veraenderung sind vorher {vorher!r} und nachher {nachher!r}, sie sollten unverändert sein.\n"
    "Tipp: subtract ändert den Counter selbst; der Operator - gibt einen neuen zurück."
)

# gesamt im Beispiel
ergebnis = wert_von(gesamt, [Counter({"label": 2}), Counter({"label": 1, "kontrast": 5})])
assert als_dict(ergebnis) == {"label": 3, "kontrast": 5}, meldung(
    "gesamt([Counter({'label': 2}), Counter({'label': 1, 'kontrast': 5})])", ergebnis, Counter({"kontrast": 5, "label": 3}),
    "\nTipp: sum(zaehlungen, Counter()) addiert alle Counter.",
)

# gesamt mit drei Countern (nicht fest hinschreiben!)
zaehlungen = [Counter({"fokus": 1}), Counter({"sprache": 2, "fokus": 3}), Counter({"sprache": 1})]
erwartet = vergleich_gesamt(zaehlungen)
ergebnis = wert_von(gesamt, zaehlungen)
assert als_dict(ergebnis) == erwartet, meldung("gesamt(zaehlungen)", ergebnis, erwartet)

# gesamt: leere Liste ergibt einen leeren Counter
ergebnis = wert_von(gesamt, [])
assert isinstance(ergebnis, Counter) and als_dict(ergebnis) == {}, meldung(
    "gesamt([])", ergebnis, Counter(), "\nTipp: Ohne Startwert beginnt sum bei 0; geben Sie Counter() als Startwert mit."
)

# gesamt lässt die übergebenen Counter unverändert
zaehlungen = [Counter({"label": 2}), Counter({"label": 1})]
wert_von(gesamt, zaehlungen)
assert [dict(zaehlung) for zaehlung in zaehlungen] == [{"label": 2}, {"label": 1}], (
    f"Nach gesamt ist die Liste {zaehlungen!r}, die Counter sollten unverändert sein.\n"
    "Tipp: update ändert den ersten Counter; beginnen Sie mit einem neuen."
)

# Viele zufällige Prüfläufe
zufall = Zufall(4059)
regeln = ["alt-text", "label", "kontrast", "fokus", "sprache", "ueberschrift"]
seiten = ["/start", "/antrag", "/termine", "/hilfe"]
for _ in range(200):
    befunde = [(zufall.choice(seiten), zufall.choice(regeln)) for _ in range(zufall.randint(0, 15))]
    n = zufall.randint(0, 7)
    ergebnis = wert_von(je_regel, befunde)
    assert als_dict(ergebnis) == vergleich_je_regel(befunde), meldung(f"je_regel({befunde})", ergebnis, vergleich_je_regel(befunde))
    ergebnis = wert_von(dringendste, befunde, n)
    assert ergebnis == vergleich_dringendste(befunde, n), meldung(f"dringendste({befunde}, {n})", ergebnis, vergleich_dringendste(befunde, n))
    vorher = Counter({regel: zufall.randint(1, 5) for regel in zufall.sample(regeln, zufall.randint(0, 6))})
    nachher = Counter({regel: zufall.randint(1, 5) for regel in zufall.sample(regeln, zufall.randint(0, 6))})
    ergebnis = wert_von(veraenderung, Counter(vorher), Counter(nachher))
    erwartet = (vergleich_differenz(vorher, nachher), vergleich_differenz(nachher, vorher))
    assert isinstance(ergebnis, tuple) and tuple(als_dict(teil) for teil in ergebnis) == erwartet, meldung(
        f"veraenderung({vorher!r}, {nachher!r})", ergebnis, erwartet
    )
    zaehlungen = [Counter({regel: zufall.randint(1, 9) for regel in zufall.sample(regeln, 2)}) for _ in range(zufall.randint(0, 5))]
    ergebnis = wert_von(gesamt, [Counter(zaehlung) for zaehlung in zaehlungen])
    assert als_dict(ergebnis) == vergleich_gesamt(zaehlungen), meldung(f"gesamt({zaehlungen!r})", ergebnis, vergleich_gesamt(zaehlungen))

# Obere Grenze: 100 000 Befunde
befunde = [(f"/seite{nummer % 500}", f"regel{zufall.randint(0, 300)}") for nummer in range(100000)]
ergebnis = wert_von(dringendste, befunde, 100)
assert ergebnis == vergleich_dringendste(befunde, 100), "Bei 100 000 Befunden stimmt dringendste(befunde, 100) nicht."
# Obere Grenze: 1000 Counter zusammenzählen
zaehlungen = [Counter({f"regel{zufall.randint(0, 50)}": zufall.randint(1, 100000) for _ in range(5)}) for _ in range(1000)]
ergebnis = wert_von(gesamt, zaehlungen)
assert als_dict(ergebnis) == vergleich_gesamt(zaehlungen), "Bei 1000 Countern stimmt gesamt(zaehlungen) nicht."
