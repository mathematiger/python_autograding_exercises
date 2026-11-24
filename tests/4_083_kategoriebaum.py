# Automatisch erzeugt aus lehrkraft/muster/4_083_kategoriebaum.py - nicht von Hand ändern.
# vorlage-hash: 19c2d3f07524edb7
# text-hash: a37cb4b642451210
# thema: datenstrukturen
# inhalt: Baum als Klasse, Generator

ZEILEN = [
    (1, None, "IT-Zubehör"),
    (2, 1, "Eingabegeräte"),
    (3, 1, "Kabel"),
    (4, 2, "Tastaturen"),
    (5, 2, "Mäuse"),
    (6, 3, "Netzwerkkabel"),
    (7, 6, "Cat 6"),
    (8, 6, "Cat 7"),
]
DURCHLAUF = [
    (0, "IT-Zubehör"), (1, "Eingabegeräte"), (2, "Tastaturen"), (2, "Mäuse"),
    (1, "Kabel"), (2, "Netzwerkkabel"), (3, "Cat 6"), (3, "Cat 7"),
]


def rufe(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def von_hand(zeilen):
    """Baut den Baum ohne baue_baum: sortiert nach id und hängt jedes Kind an seine Eltern."""
    knoten = {kennung: Kategorie(name) for kennung, _, name in zeilen}
    wurzel = None
    for kennung, eltern, _ in sorted(zeilen, key=lambda zeile: zeile[0]):
        if eltern is None:
            wurzel = knoten[kennung]
        else:
            knoten[eltern].kinder.append(knoten[kennung])
    return wurzel


def gestalt(knoten):
    """Vergleichslösung: der Baum als verschachteltes Tupel (name, [Kinder]), ohne die Methoden der SuS."""
    return (knoten.name, [gestalt(kind) for kind in knoten.kinder])


def vergleich_durchlauf(knoten, tiefe=0):
    """Vergleichslösung: Preorder mit einem eigenen Stapel statt Rekursion."""
    ergebnis = []
    stapel = [(tiefe, knoten)]
    while stapel:
        ebene, aktuell = stapel.pop()
        ergebnis.append((ebene, aktuell.name))
        for kind in reversed(aktuell.kinder):
            stapel.append((ebene + 1, kind))
    return ergebnis


def vergleich_blaetter(knoten):
    """Vergleichslösung: die Blätter aus dem Durchlauf mit eigenem Stapel."""
    blaetter = []
    stapel = [knoten]
    while stapel:
        aktuell = stapel.pop()
        if not aktuell.kinder:
            blaetter.append(aktuell.name)
        stapel.extend(reversed(aktuell.kinder))
    return blaetter


def vergleich_pfad(zeilen, name):
    """Vergleichslösung: geht über eltern_id von name zur Wurzel hoch."""
    nach_id = {kennung: (eltern, n) for kennung, eltern, n in zeilen}
    kennung = next((k for k, (_, n) in nach_id.items() if n == name), None)
    if kennung is None:
        return None
    pfad = []
    while kennung is not None:
        eltern, n = nach_id[kennung]
        pfad.append(n)
        kennung = eltern
    return pfad[::-1]


def als_liste(erzeuger):
    """Durchläuft das Ergebnis eines Methodenaufrufs; liefert (Liste, Fehlertext oder None)."""
    try:
        return list(erzeuger()), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def zufallsbaum(zufall, anzahl):
    """Erzeugt Zeilen eines zufälligen Baums mit höchstens 100 Ebenen, gemischt."""
    kennungen = zufall.sample(range(1, 10**6), anzahl)
    zeilen = [(kennungen[0], None, "K0")]
    tiefe = {kennungen[0]: 0}
    for nummer in range(1, anzahl):
        eltern = zufall.choice(kennungen[max(0, nummer - 5):nummer])
        if tiefe[eltern] == 99:
            eltern = kennungen[0]
        tiefe[kennungen[nummer]] = tiefe[eltern] + 1
        zeilen.append((kennungen[nummer], eltern, f"K{nummer}"))
    zufall.shuffle(zeilen)
    return zeilen


TIPP_YIELD_FROM = (
    "\nTipp: Für jedes Kind müssen Sie dessen Werte weiterreichen: yield from kind.durchlauf(tiefe + 1). "
    "Nur kind.durchlauf(...) aufzurufen erzeugt einen Generator, liefert aber nichts."
)

# durchlauf: das erste Paar ist die Kategorie selbst mit Tiefe 0
baum = von_hand(ZEILEN)
ergebnis, fehler = als_liste(baum.durchlauf)
erstes = ergebnis[0] if ergebnis else None
assert erstes == (0, "IT-Zubehör"), (
    f"Das erste Paar von baum.durchlauf() ist {erstes!r}, erwartet war (0, 'IT-Zubehör')." + absturz(fehler)
    + "\nTipp: Beginnen Sie mit yield (tiefe, self.name)."
)

# durchlauf: die Kinder der Wurzel mit Tiefe 1
baum = von_hand(ZEILEN)
ergebnis, fehler = als_liste(baum.durchlauf)
ebene_eins = [paar for paar in ergebnis or [] if paar[0] == 1]
assert ebene_eins == [(1, "Eingabegeräte"), (1, "Kabel")], (
    f"Die Paare mit Tiefe 1 in baum.durchlauf() sind {ebene_eins!r}, erwartet war "
    "[(1, 'Eingabegeräte'), (1, 'Kabel')]. Ganzer Durchlauf: " + f"{ergebnis!r}" + absturz(fehler) + TIPP_YIELD_FROM
)

# durchlauf: das Beispiel vollständig, von oben nach unten
baum = von_hand(ZEILEN)
ergebnis, fehler = als_liste(baum.durchlauf)
assert ergebnis == DURCHLAUF, (
    f"list(baum.durchlauf()) ergibt\n{ergebnis!r},\nerwartet war\n{DURCHLAUF!r}." + absturz(fehler)
    + "\nTipp: Erst die Kategorie, dann jedes Kind mit allem darunter (nicht erst alle Kinder, dann die Enkel)."
)

# durchlauf: ein Teilbaum beginnt bei Tiefe 0, oder bei der übergebenen tiefe
baum = von_hand(ZEILEN)
kabel = baum.kinder[1]
ergebnis, fehler = als_liste(kabel.durchlauf)
mit_tiefe, zweiter_fehler = als_liste(lambda: kabel.durchlauf(5))
erwartet = [(0, "Kabel"), (1, "Netzwerkkabel"), (2, "Cat 6"), (2, "Cat 7")]
assert ergebnis == erwartet and mit_tiefe == [(t + 5, n) for t, n in erwartet], (
    f"Für die Kategorie Kabel ergibt list(kabel.durchlauf()) {ergebnis!r} und list(kabel.durchlauf(5)) "
    f"{mit_tiefe!r}; erwartet waren {erwartet!r} und dieselben Paare mit Tiefe 5, 6, 7."
    + absturz(fehler or zweiter_fehler)
)

# durchlauf: ein einzelnes Blatt
ergebnis, fehler = als_liste(Kategorie("Drucker").durchlauf)
assert ergebnis == [(0, "Drucker")], (
    f"list(Kategorie('Drucker').durchlauf()) ergibt {ergebnis!r}, erwartet war [(0, 'Drucker')]." + absturz(fehler)
)

# durchlauf ist eine Generatormethode
baum = von_hand(ZEILEN)
ergebnis, fehler = rufe(baum.durchlauf)
assert type(ergebnis).__name__ == "generator", (
    f"baum.durchlauf() ergibt ein Objekt vom Typ {type(ergebnis).__name__}, erwartet war ein Generator.\n"
    "Tipp: Schreiben Sie die Werte mit yield, statt eine Liste zu bauen und zurückzugeben." + absturz(fehler)
)

# durchlauf: lässt sich mehrfach durchlaufen und verändert den Baum nicht
baum = von_hand(ZEILEN)
erster, fehler = als_liste(baum.durchlauf)
zweiter, zweiter_fehler = als_liste(baum.durchlauf)
assert erster == zweiter == DURCHLAUF and gestalt(baum) == gestalt(von_hand(ZEILEN)), (
    f"Zwei Durchläufe ergeben {erster!r} und {zweiter!r}; erwartet war beide Male {DURCHLAUF!r}, und der Baum soll "
    "unverändert bleiben." + absturz(fehler or zweiter_fehler)
)

# blaetter: das Beispiel
baum = von_hand(ZEILEN)
ergebnis, fehler = als_liste(baum.blaetter)
assert ergebnis == ["Tastaturen", "Mäuse", "Cat 6", "Cat 7"], (
    f"list(baum.blaetter()) ergibt {ergebnis!r}, erwartet war ['Tastaturen', 'Mäuse', 'Cat 6', 'Cat 7'].\n"
    "Tipp: Ein Blatt ist eine Kategorie mit leerer Liste kinder; reichen Sie die Blätter der Kinder mit yield from "
    "weiter." + absturz(fehler)
)

# blaetter: eine Kategorie ohne Kinder ist selbst ein Blatt
ergebnis, fehler = als_liste(Kategorie("Drucker").blaetter)
assert ergebnis == ["Drucker"], (
    f"list(Kategorie('Drucker').blaetter()) ergibt {ergebnis!r}, erwartet war ['Drucker']." + absturz(fehler)
)

# blaetter ist eine Generatormethode
ergebnis, fehler = rufe(von_hand(ZEILEN).blaetter)
assert type(ergebnis).__name__ == "generator", (
    f"baum.blaetter() ergibt ein Objekt vom Typ {type(ergebnis).__name__}, erwartet war ein Generator." + absturz(fehler)
)

# pfad_zu: das Beispiel
baum = von_hand(ZEILEN)
ergebnis, fehler = rufe(baum.pfad_zu, "Cat 7")
assert ergebnis == ["IT-Zubehör", "Kabel", "Netzwerkkabel", "Cat 7"], (
    f"baum.pfad_zu('Cat 7') ergibt {ergebnis!r}, erwartet war ['IT-Zubehör', 'Kabel', 'Netzwerkkabel', 'Cat 7']."
    + absturz(fehler)
)

# pfad_zu: ein anderes Ziel (nicht fest hinschreiben!)
baum = von_hand(ZEILEN)
ergebnis, fehler = rufe(baum.pfad_zu, "Mäuse")
assert ergebnis == ["IT-Zubehör", "Eingabegeräte", "Mäuse"], (
    f"baum.pfad_zu('Mäuse') ergibt {ergebnis!r}, erwartet war ['IT-Zubehör', 'Eingabegeräte', 'Mäuse']."
    + absturz(fehler)
    + "\nTipp: Fragen Sie jedes Kind nach dem Pfad; liefert eins einen, setzen Sie den eigenen Namen davor."
)

# pfad_zu: die Kategorie selbst
baum = von_hand(ZEILEN)
ergebnis, fehler = rufe(baum.pfad_zu, "IT-Zubehör")
assert ergebnis == ["IT-Zubehör"], f"baum.pfad_zu('IT-Zubehör') ergibt {ergebnis!r}, erwartet war ['IT-Zubehör']." + absturz(
    fehler
)

# pfad_zu: ein Name, den es nicht gibt
baum = von_hand(ZEILEN)
ergebnis, fehler = rufe(baum.pfad_zu, "Drucker")
assert fehler is None and ergebnis is None, (
    f"baum.pfad_zu('Drucker') ergibt {ergebnis!r}, erwartet war None." + absturz(fehler)
    + "\nTipp: Prüfen Sie, ob ein Kind None liefert, bevor Sie seinen Pfad benutzen."
)

# pfad_zu: ein Name über der Kategorie wird nicht gefunden
baum = von_hand(ZEILEN)
ergebnis, fehler = rufe(baum.kinder[1].pfad_zu, "Mäuse")
assert fehler is None and ergebnis is None, (
    f"kabel.pfad_zu('Mäuse') ergibt {ergebnis!r}, erwartet war None: Mäuse liegt nicht unter Kabel." + absturz(fehler)
)

# baue_baum: gibt eine Kategorie zurück, die Wurzel
ergebnis, fehler = rufe(baue_baum, list(ZEILEN))
assert isinstance(ergebnis, Kategorie) and ergebnis.name == "IT-Zubehör", (
    f"baue_baum(zeilen) ergibt {ergebnis!r}, erwartet war die Kategorie 'IT-Zubehör' (ein Objekt der Klasse "
    "Kategorie)." + absturz(fehler)
)

# baue_baum: das Beispiel in der Reihenfolge der Tabelle
ergebnis, fehler = rufe(baue_baum, list(ZEILEN))
erwartet = gestalt(von_hand(ZEILEN))
assert isinstance(ergebnis, Kategorie) and gestalt(ergebnis) == erwartet, (
    f"baue_baum(zeilen) baut den Baum\n{gestalt(ergebnis) if isinstance(ergebnis, Kategorie) else ergebnis!r},\n"
    f"erwartet war (Name, [Kinder]):\n{erwartet!r}" + absturz(fehler)
)

# baue_baum: Zeilen in anderer Reihenfolge, Kinder nach id
zeilen = [ZEILEN[i] for i in [7, 2, 5, 0, 4, 6, 1, 3]]
ergebnis, fehler = rufe(baue_baum, list(zeilen))
assert isinstance(ergebnis, Kategorie) and gestalt(ergebnis) == gestalt(von_hand(ZEILEN)), (
    f"baue_baum mit den Zeilen in der Reihenfolge {[z[0] for z in zeilen]} baut\n"
    f"{gestalt(ergebnis) if isinstance(ergebnis, Kategorie) else ergebnis!r},\n"
    f"erwartet war\n{gestalt(von_hand(ZEILEN))!r}" + absturz(fehler)
    + "\nTipp: Legen Sie erst alle Kategorien in einem Dictionary id → Kategorie an, dann hängen Sie sie in "
    "aufsteigender id an ihre Eltern."
)

# baue_baum: eine Tabelle mit nur einer Zeile
ergebnis, fehler = rufe(baue_baum, [(42, None, "Restposten")])
assert isinstance(ergebnis, Kategorie) and gestalt(ergebnis) == ("Restposten", []), (
    f"baue_baum([(42, None, 'Restposten')]) ergibt {ergebnis!r}, erwartet war eine Kategorie 'Restposten' ohne "
    "Kinder." + absturz(fehler)
)

# baue_baum: die Wurzel muss nicht die kleinste id haben
zeilen = [(30, 50, "Monitore"), (50, None, "Hardware"), (10, 50, "Drucker"), (20, 10, "Toner")]
ergebnis, fehler = rufe(baue_baum, zeilen)
erwartet = ("Hardware", [("Drucker", [("Toner", [])]), ("Monitore", [])])
assert isinstance(ergebnis, Kategorie) and gestalt(ergebnis) == erwartet, (
    f"baue_baum({zeilen!r}) baut {gestalt(ergebnis) if isinstance(ergebnis, Kategorie) else ergebnis!r}, "
    f"erwartet war {erwartet!r}." + absturz(fehler)
)

# 200 zufällige Tabellen: baue_baum, durchlauf, blaetter und pfad_zu
zufall = Zufall(4083)
for _ in range(200):
    zeilen = zufallsbaum(zufall, zufall.randint(1, 15))
    richtig = von_hand(zeilen)
    ergebnis, fehler = rufe(baue_baum, list(zeilen))
    assert isinstance(ergebnis, Kategorie) and gestalt(ergebnis) == gestalt(richtig), (
        f"baue_baum({zeilen!r}) baut {gestalt(ergebnis) if isinstance(ergebnis, Kategorie) else ergebnis!r}, "
        f"erwartet war {gestalt(richtig)!r}." + absturz(fehler)
    )
    ergebnis, fehler = als_liste(richtig.durchlauf)
    assert ergebnis == vergleich_durchlauf(richtig), (
        f"Für den Baum {gestalt(richtig)!r} ergibt durchlauf {ergebnis!r}, erwartet war "
        f"{vergleich_durchlauf(richtig)!r}." + absturz(fehler)
    )
    ergebnis, fehler = als_liste(richtig.blaetter)
    assert ergebnis == vergleich_blaetter(richtig), (
        f"Für den Baum {gestalt(richtig)!r} ergibt blaetter {ergebnis!r}, erwartet war {vergleich_blaetter(richtig)!r}."
        + absturz(fehler)
    )
    ziel = zufall.choice([zeile[2] for zeile in zeilen] + ["gibt es nicht"])
    ergebnis, fehler = rufe(richtig.pfad_zu, ziel)
    assert ergebnis == vergleich_pfad(zeilen, ziel), (
        f"Für den Baum {gestalt(richtig)!r} ergibt pfad_zu({ziel!r}) {ergebnis!r}, erwartet war "
        f"{vergleich_pfad(zeilen, ziel)!r}." + absturz(fehler)
    )

# Laufzeit: durchlauf liefert das erste Paar, ohne den ganzen Baum anzusehen
baum = von_hand(zufallsbaum(zufall, 2000))
_, schritte = zaehle_schritte(lambda: next(baum.durchlauf()))
assert schritte <= 20, (
    f"next(baum.durchlauf()) braucht bei 2000 Kategorien {schritte} Schritte, erlaubt sind 20. Ihr durchlauf sieht "
    "erst den ganzen Baum an, bevor er das erste Paar liefert.\nTipp: Liefern Sie jedes Paar sofort mit yield, statt "
    "erst eine Liste aller Paare zu bauen."
)

# Laufzeit: baue_baum braucht O(n log n) Schritte, nicht O(n²)
klein = zufallsbaum(zufall, 500)
gross = zufallsbaum(zufall, 2000)
_, schritte_klein = zaehle_schritte(baue_baum, klein)
_, schritte_gross = zaehle_schritte(baue_baum, gross)
assert schritte_gross <= 6 * schritte_klein + 100, (
    f"baue_baum braucht für 500 Zeilen {schritte_klein} Schritte und für 2000 Zeilen {schritte_gross}; erlaubt ist "
    "für die vierfache Menge höchstens etwa das Sechsfache (O(n log n)). Bei O(n²) ist es das Sechzehnfache.\n"
    "Tipp: Suchen Sie die Eltern nicht jedes Mal in der Liste der Zeilen, sondern in einem Dictionary id → Kategorie."
)

# Obere Grenze: 10 000 Zeilen, 100 Ebenen tief
zeilen = [(1, None, "Ebene 0")] + [(i + 1, i, f"Ebene {i}") for i in range(1, 100)]
zeilen += [(1000 + i, zufall.randint(1, 99), f"Blatt {i}") for i in range(9900)]
zufall.shuffle(zeilen)
richtig = von_hand(zeilen)
ergebnis, fehler = rufe(baue_baum, list(zeilen))
gebaut = isinstance(ergebnis, Kategorie) and gestalt(ergebnis) == gestalt(richtig)
paare, zweiter_fehler = als_liste(richtig.durchlauf)
assert gebaut and paare == vergleich_durchlauf(richtig), (
    "Bei 10 000 Zeilen und 100 Ebenen "
    + ("baut baue_baum einen anderen Baum" if not gebaut else f"ergibt durchlauf {len(paare or [])} Paare, "
       "nicht die erwarteten 10 000 in der richtigen Reihenfolge")
    + "." + absturz(fehler or zweiter_fehler)
)
