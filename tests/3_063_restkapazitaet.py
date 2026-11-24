# Automatisch erzeugt aus lehrkraft/muster/3_063_restkapazitaet.py - nicht von Hand ändern.
# vorlage-hash: 766b96c278c303e0
# text-hash: 2cc9b10ee3aa8729
# thema: algorithmen
# inhalt: Paarsumme mit Menge, O(n)

AUFWAENDE = [90, 240, 45, 120, 300, 75, 120, 165]


def wert_von(funktion, aufwaende, frei):
    """Ruft funktion mit einer Kopie der Aufwände auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(list(aufwaende), frei)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def gezeigt(aufwaende):
    """Zeigt kurze Listen ganz, lange nur mit ihrer Länge."""
    return aufwaende if len(aufwaende) <= 12 else f"<{len(aufwaende)} Aufwände>"


def vergleich_paar(aufwaende, frei):
    """Vergleichslösung: probiert für jedes j alle früheren i (langsam, aber offensichtlich richtig)."""
    for j in range(len(aufwaende)):
        for i in range(j):
            if aufwaende[i] + aufwaende[j] == frei:
                return (i, j)
    return None


def vergleich_anzahl(aufwaende, frei):
    """Vergleichslösung: zählt alle Paare mit zwei Schleifen."""
    anzahl = 0
    for j in range(len(aufwaende)):
        for i in range(j):
            if aufwaende[i] + aufwaende[j] == frei:
                anzahl += 1
    return anzahl


def anzahl_ueber_haeufigkeiten(aufwaende, frei):
    """Vergleichslösung für große Listen: multipliziert die Häufigkeiten passender Werte."""
    haeufigkeit = {}
    for wert in aufwaende:
        haeufigkeit[wert] = haeufigkeit.get(wert, 0) + 1
    anzahl = 0
    for wert, wie_oft in haeufigkeit.items():
        partner = frei - wert
        if wert < partner:
            anzahl += wie_oft * haeufigkeit.get(partner, 0)
        elif wert == partner:
            anzahl += wie_oft * (wie_oft - 1) // 2
    return anzahl


def fehler_im_paar(aufwaende, frei, ergebnis):
    """Gibt zurück, was an ergebnis als irgendein passendes Paar nicht stimmt, oder None."""
    if vergleich_paar(aufwaende, frei) is None:
        return None if ergebnis is None else "es gibt kein solches Paar, erwartet war None"
    if ergebnis is None:
        return "es gibt aber ein solches Paar"
    if not isinstance(ergebnis, tuple) or len(ergebnis) != 2 or not all(isinstance(zahl, int) for zahl in ergebnis):
        return "erwartet war ein Tupel (i, j) aus zwei Positionen"
    i, j = ergebnis
    if not 0 <= i < j < len(aufwaende):
        return f"erwartet waren Positionen mit 0 ≤ i < j < {len(aufwaende)}"
    if aufwaende[i] + aufwaende[j] != frei:
        return f"aufwaende[{i}] + aufwaende[{j}] ist {aufwaende[i] + aufwaende[j]}, nicht {frei}"
    return None


def pruefe_irgendein_paar(aufwaende, frei, hinweis=""):
    """Prüft, ob paar_fuer irgendein passendes Paar liefert; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(paar_fuer, aufwaende, frei)
    fehler = fehler_im_paar(aufwaende, frei, ergebnis)
    return fehler is None, f"paar_fuer({gezeigt(aufwaende)}, {frei}) ergibt {ergebnis!r}; {fehler}.{hinweis}"


def pruefe_paar(aufwaende, frei, hinweis=""):
    """Prüft paar_fuer genau gegen das zuerst vollständige Paar; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(paar_fuer, aufwaende, frei)
    erwartet = vergleich_paar(aufwaende, frei)
    text = f"paar_fuer({gezeigt(aufwaende)}, {frei}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"
    return ergebnis == erwartet, text


def pruefe_anzahl(aufwaende, frei, hinweis=""):
    """Prüft anzahl_paare gegen die Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(anzahl_paare, aufwaende, frei)
    erwartet = anzahl_ueber_haeufigkeiten(aufwaende, frei)
    text = f"anzahl_paare({gezeigt(aufwaende)}, {frei}) ergibt {ergebnis!r}, erwartet war {erwartet}.{hinweis}"
    return ergebnis == erwartet, text


def zugriffe(funktion, aufwaende, frei):
    """Ruft funktion mit einer Zaehlliste auf; liefert (Ergebnis, Lesezugriffe)."""
    liste = Zaehlliste(aufwaende)
    try:
        ergebnis = funktion(liste, frei)
    except Exception as fehler:
        ergebnis = f"{type(fehler).__name__}: {fehler}"
    return ergebnis, liste.lesezugriffe


# paar_fuer: das Beispiel liefert ein passendes Paar
stimmt, text = pruefe_irgendein_paar(
    AUFWAENDE, 165, "\nTipp: Zu einem Aufwand x passt genau der Aufwand frei - x."
)
assert stimmt, text

# paar_fuer: im Beispiel das Paar, das als erstes vollständig ist
ergebnis = wert_von(paar_fuer, AUFWAENDE, 165)
assert ergebnis == (2, 3), (
    f"paar_fuer({AUFWAENDE}, 165) ergibt {ergebnis!r}, erwartet war (2, 3): An Position 3 (120) ist der "
    "Partner 45 schon gesehen, früher wird kein Paar vollständig.\n"
    "Tipp: Gehen Sie die Liste einmal von vorn durch und fragen Sie bei jedem Eintrag, ob sein Partner "
    "schon vorkam."
)

# paar_fuer: ein anderer freier Zeitraum (nicht fest hinschreiben!)
stimmt, text = pruefe_paar(AUFWAENDE, 210)
assert stimmt, text

# paar_fuer: zwei Einträge mit gleichem Aufwand
stimmt, text = pruefe_paar(AUFWAENDE, 240)
assert stimmt, text

# paar_fuer: kein passendes Paar ergibt None
stimmt, text = pruefe_paar(AUFWAENDE, 500, "\nTipp: Geben Sie nach der Schleife None zurück.")
assert stimmt, text

# paar_fuer: das Ergebnis sind Positionen, nicht Aufwände
ergebnis = wert_von(paar_fuer, [30, 70, 50], 120)
assert ergebnis == (1, 2), (
    f"paar_fuer([30, 70, 50], 120) ergibt {ergebnis!r}, erwartet war das Tupel (1, 2): die Positionen von 70 "
    "und 50, nicht die Aufwände selbst, und die kleinere Position zuerst."
)

# paar_fuer: ein Eintrag wird nicht mit sich selbst gepaart
stimmt, text = pruefe_paar(
    [120, 50], 240,
    "\nTipp: Fragen Sie erst nach dem Partner und merken Sie sich den Eintrag danach; sonst findet 120 sich selbst.",
)
assert stimmt, text

# paar_fuer: bei gleichen Aufwänden zählt der früheste Partner
stimmt, text = pruefe_paar(
    [100, 100, 140], 240,
    "\nTipp: Merken Sie sich zu jedem Aufwand die Position, an der er zum ersten Mal vorkam, und "
    "überschreiben Sie sie nicht.",
)
assert stimmt, text

# paar_fuer: der späte Eintrag entscheidet, nicht der frühe Partner
stimmt, text = pruefe_paar(
    [10, 60, 140, 190], 200,
    "\nTipp: Gesucht ist das Paar mit dem kleinsten j, nicht das mit dem kleinsten i.",
)
assert stimmt, text

# paar_fuer: die größten Aufwände
stimmt, text = pruefe_paar([100000, 5, 100000], 200000)
assert stimmt, text

# paar_fuer: frei ist kleiner als jedes Paar
stimmt, text = pruefe_paar([2, 3, 4], 1)
assert stimmt, text

# paar_fuer: ein einziger Eintrag
stimmt, text = pruefe_paar([120], 240)
assert stimmt, text

# paar_fuer: leere Liste
stimmt, text = pruefe_paar([], 240)
assert stimmt, text

# anzahl_paare: das Beispiel
stimmt, text = pruefe_anzahl(AUFWAENDE, 165, "\nTipp: (2, 3), (0, 5) und (2, 6) passen.")
assert stimmt, text

# anzahl_paare: ein anderer freier Zeitraum
stimmt, text = pruefe_anzahl(AUFWAENDE, 210)
assert stimmt, text

# anzahl_paare: kein passendes Paar
stimmt, text = pruefe_anzahl(AUFWAENDE, 500)
assert stimmt, text

# anzahl_paare: doppelte Aufwände auf beiden Seiten
stimmt, text = pruefe_anzahl(
    [50, 190, 50, 190], 240,
    "\nTipp: Jede 190 passt zu jeder 50 davor; zählen Sie mit einem Dictionary, wie oft jeder Aufwand schon vorkam.",
)
assert stimmt, text

# anzahl_paare: viele gleiche Aufwände, die zusammen passen
stimmt, text = pruefe_anzahl(
    [120, 120, 120, 120], 240,
    "\nTipp: Vier gleiche Einträge ergeben 4 · 3 / 2 = 6 Paare; ein Eintrag zählt nicht mit sich selbst.",
)
assert stimmt, text

# anzahl_paare: ein einziger Eintrag
stimmt, text = pruefe_anzahl([120], 240, "\nTipp: Ein Eintrag allein ist kein Paar.")
assert stimmt, text

# anzahl_paare: leere Liste
stimmt, text = pruefe_anzahl([], 240)
assert stimmt, text

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar("(2, 3)\n3"), f"Erwartete Ausgabe:\n(2, 3)\n3\nIhr Programm:\n{AUSGABE}"

zufall = Zufall(3063)
faelle = []
for _ in range(400):
    hoechstens = zufall.choice([5, 30, 100000])
    aufwaende = [zufall.randint(1, hoechstens) for _ in range(zufall.randint(0, 12))]
    if aufwaende and zufall.random() < 0.7:
        frei = zufall.choice(aufwaende) + zufall.choice(aufwaende)
    else:
        frei = zufall.randint(1, 2 * hoechstens)
    faelle.append((aufwaende, frei))

# paar_fuer: viele zufällige Listen
for aufwaende, frei in faelle:
    stimmt, text = pruefe_paar(aufwaende, frei)
    assert stimmt, text

# anzahl_paare: dieselben zufälligen Listen
for aufwaende, frei in faelle:
    ergebnis = wert_von(anzahl_paare, aufwaende, frei)
    erwartet = vergleich_anzahl(aufwaende, frei)
    assert ergebnis == erwartet, f"anzahl_paare({aufwaende}, {frei}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Laufzeit: paar_fuer braucht O(n) Zugriffe
aufwaende = list(range(1, 1501))
zufall.shuffle(aufwaende)
ergebnis, anzahl = zugriffe(paar_fuer, aufwaende, 5000)
if ergebnis is not None:
    text = f"paar_fuer für 1500 Aufwände ohne passendes Paar ergibt {ergebnis!r}, erwartet war None."
else:
    text = (
        f"paar_fuer für 1500 Aufwände ohne passendes Paar braucht {anzahl} Zugriffe auf aufwaende; "
        f"erlaubt sind {3 * len(aufwaende) + 10} (O(n)). Zwei verschachtelte Schleifen brauchen über zwei "
        "Millionen, frei - wert in aufwaende sieht jedes Mal die ganze Liste an.\n"
        "Tipp: Merken Sie sich die gesehenen Aufwände in einem Dictionary und fragen Sie dort nach dem Partner."
    )
assert ergebnis is None and anzahl <= 3 * len(aufwaende) + 10, text

# Laufzeit: anzahl_paare braucht O(n) Zugriffe
ergebnis, anzahl = zugriffe(anzahl_paare, aufwaende, 1501)
if ergebnis != 750:
    text = f"anzahl_paare für die Aufwände 1 bis 1500 und frei = 1501 ergibt {ergebnis!r}, erwartet war 750."
else:
    text = (
        f"anzahl_paare für 1500 Aufwände braucht {anzahl} Zugriffe auf aufwaende; "
        f"erlaubt sind {3 * len(aufwaende) + 10} (O(n)).\n"
        "Tipp: Gehen Sie die Liste nur einmal durch und zählen Sie in einem Dictionary, wie oft jeder Aufwand "
        "schon vorkam."
    )
assert ergebnis == 750 and anzahl <= 3 * len(aufwaende) + 10, text

# Alle Aufwände sind durch 3 teilbar außer zweien mit Rest 1; nur diese beiden zusammen haben Rest 2.
# Obere Grenze: paar_fuer bei 100 000 Einträgen mit genau einem passenden Paar
aufwaende = [3 * zufall.randint(1, 33333) for _ in range(100000)]
aufwaende[31000] = 40000
aufwaende[87000] = 55003
ergebnis = wert_von(paar_fuer, aufwaende, 95003)
assert ergebnis == (31000, 87000), (
    f"paar_fuer für 100 000 Aufwände mit genau einem passenden Paar an den Positionen 31000 und 87000 ergibt "
    f"{ergebnis!r}, erwartet war (31000, 87000)."
)

# Obere Grenze: anzahl_paare bei 100 000 Einträgen
aufwaende = [zufall.randint(1, 100000) for _ in range(100000)]
stimmt, text = pruefe_anzahl(aufwaende, 100001)
assert stimmt, text
