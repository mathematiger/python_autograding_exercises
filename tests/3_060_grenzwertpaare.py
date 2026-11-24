# Automatisch erzeugt aus lehrkraft/muster/3_060_grenzwertpaare.py - nicht von Hand ändern.
# vorlage-hash: 40b579d7c54b252b
# text-hash: c9866b3ad0afb85c
# thema: algorithmen
# inhalt: Zwei-Zeiger-Technik

import bisect

PREISE = [499, 1250, 1999, 2490, 3001, 3990, 4800]


def wert_von(funktion, preise, zahl):
    """Ruft funktion mit einer Kopie der Preise auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(list(preise), zahl)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def gibt_es_paar(preise, ziel):
    """Vergleichslösung: merkt sich die bisher gesehenen Preise in einer Menge."""
    gesehen = set()
    for preis in preise:
        if ziel - preis in gesehen:
            return True
        gesehen.add(preis)
    return False


def vergleich_anzahl(preise, grenze):
    """Vergleichslösung: zählt für jeden Preis mit bisect, wie viele spätere Preise passen."""
    anzahl = 0
    for i, preis in enumerate(preise):
        bis = bisect.bisect_left(preise, grenze - preis, i + 1)
        anzahl += max(0, bis - i - 1)
    return anzahl


def fehler_im_paar(preise, ziel, ergebnis):
    """Gibt zurück, was an ergebnis nicht stimmt, oder None."""
    if not gibt_es_paar(preise, ziel):
        return None if ergebnis is None else "es gibt kein solches Paar, erwartet war None"
    if ergebnis is None:
        return "es gibt aber ein solches Paar"
    if not isinstance(ergebnis, tuple) or len(ergebnis) != 2 or not all(isinstance(zahl, int) for zahl in ergebnis):
        return "erwartet war ein Tupel (i, j) aus zwei Positionen"
    i, j = ergebnis
    if not 0 <= i < j < len(preise):
        return f"erwartet waren Positionen mit 0 ≤ i < j < {len(preise)}"
    if preise[i] + preise[j] != ziel:
        return f"preise[{i}] + preise[{j}] ist {preise[i] + preise[j]}, nicht {ziel}"
    return None


def pruefe_paar(preise, ziel, hinweis=""):
    """Prüft paar_mit_summe(preise, ziel); liefert (stimmt, Meldung)."""
    ergebnis = wert_von(paar_mit_summe, preise, ziel)
    fehler = fehler_im_paar(preise, ziel, ergebnis)
    gezeigt = preise if len(preise) <= 12 else f"<{len(preise)} Preise>"
    return fehler is None, f"paar_mit_summe({gezeigt}, {ziel}) ergibt {ergebnis!r}; {fehler}.{hinweis}"


def pruefe_anzahl(preise, grenze, hinweis=""):
    """Prüft anzahl_unter(preise, grenze) gegen die Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(anzahl_unter, preise, grenze)
    erwartet = vergleich_anzahl(preise, grenze)
    gezeigt = preise if len(preise) <= 12 else f"<{len(preise)} Preise>"
    text = f"anzahl_unter({gezeigt}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}.{hinweis}"
    return ergebnis == erwartet, text


def zugriffe(funktion, preise, zahl):
    """Ruft funktion mit einer Zaehlliste auf; liefert (Ergebnis, Lesezugriffe)."""
    liste = Zaehlliste(preise)
    try:
        ergebnis = funktion(liste, zahl)
    except Exception as fehler:
        ergebnis = f"{type(fehler).__name__}: {fehler}"
    return ergebnis, liste.lesezugriffe


def zufallspreise(zufall, anzahl, hoechstens):
    """Erzeugt eine sortierte Preisliste, auch mit doppelten Preisen."""
    return sorted(zufall.randint(1, hoechstens) for _ in range(anzahl))


# paar_mit_summe: das Beispiel
stimmt, text = pruefe_paar(PREISE, 5000, "\nTipp: links beginnt bei 0, rechts bei len(preise) - 1.")
assert stimmt, text

# paar_mit_summe: ein anderes Ziel (nicht fest hinschreiben!)
stimmt, text = pruefe_paar(PREISE, 4251)
assert stimmt, text

# paar_mit_summe: der billigste und der teuerste Artikel
stimmt, text = pruefe_paar(PREISE, 5299)
assert stimmt, text

# paar_mit_summe: kein passendes Paar ergibt None
stimmt, text = pruefe_paar(PREISE, 6250, "\nTipp: Treffen sich die Zeiger, gibt es kein Paar; geben Sie dann None zurück.")
assert stimmt, text

# paar_mit_summe: das Ergebnis sind Positionen, nicht Preise
ergebnis = wert_von(paar_mit_summe, PREISE, 5000)
assert ergebnis == (2, 4), (
    f"paar_mit_summe({PREISE}, 5000) ergibt {ergebnis!r}, erwartet war das Tupel (2, 4): die Positionen von "
    "1999 und 3001, nicht die Preise selbst."
)

# paar_mit_summe: zwei Artikel mit gleichem Preis
stimmt, text = pruefe_paar([1000, 2500, 2500, 3000], 5000, "\nTipp: Die Schleife läuft, solange links < rechts ist.")
assert stimmt, text

# paar_mit_summe: ein Artikel wird nicht mit sich selbst gepaart
stimmt, text = pruefe_paar(
    [1000, 2500, 3000], 5000,
    "\nTipp: 2500 + 2500 wäre derselbe Artikel zweimal; die Schleife endet, bevor links == rechts ist.",
)
assert stimmt, text

# paar_mit_summe: Ziel kleiner als jedes Paar
stimmt, text = pruefe_paar(PREISE, 100)
assert stimmt, text

# paar_mit_summe: Ziel größer als jedes Paar
stimmt, text = pruefe_paar(PREISE, 2000000)
assert stimmt, text

# paar_mit_summe: ein einziger Artikel
stimmt, text = pruefe_paar([2500], 5000)
assert stimmt, text

# paar_mit_summe: leerer Katalog
stimmt, text = pruefe_paar([], 5000)
assert stimmt, text

# anzahl_unter: das Beispiel
stimmt, text = pruefe_anzahl(
    PREISE, 5000,
    "\nTipp: Ist preise[links] + preise[rechts] < grenze, passen alle rechts - links Paare mit preise[links].",
)
assert stimmt, text

# anzahl_unter: eine andere Grenze
stimmt, text = pruefe_anzahl(PREISE, 6000)
assert stimmt, text

# anzahl_unter: genau auf der Grenze zählt nicht
stimmt, text = pruefe_anzahl([1000, 2000, 3000], 4000, "\nTipp: Gezählt wird nur, was echt kleiner ist (<, nicht <=).")
assert stimmt, text

# anzahl_unter: alle Paare liegen darunter
stimmt, text = pruefe_anzahl([100, 200, 300, 400], 2000000)
assert stimmt, text

# anzahl_unter: kein Paar liegt darunter
stimmt, text = pruefe_anzahl([3000, 4000, 5000], 5000)
assert stimmt, text

# anzahl_unter: doppelte Preise
stimmt, text = pruefe_anzahl([1000, 1000, 1000, 4000], 3000)
assert stimmt, text

# anzahl_unter: ein einziger Artikel
stimmt, text = pruefe_anzahl([100], 5000, "\nTipp: Ein Artikel allein ist kein Paar.")
assert stimmt, text

# anzahl_unter: leerer Katalog
stimmt, text = pruefe_anzahl([], 5000)
assert stimmt, text

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar("(2, 4)\n9"), f"Erwartete Ausgabe:\n(2, 4)\n9\nIhr Programm:\n{AUSGABE}"

zufall = Zufall(3060)
faelle = []
for _ in range(400):
    preise = zufallspreise(zufall, zufall.randint(0, 12), zufall.choice([10, 100, 5000]))
    zahl = zufall.randint(1, 2 * max(preise + [1]) + 2)
    faelle.append((preise, zahl))

# paar_mit_summe: viele zufällige Kataloge
for preise, zahl in faelle:
    stimmt, text = pruefe_paar(preise, zahl)
    assert stimmt, text

# anzahl_unter: dieselben zufälligen Kataloge
for preise, zahl in faelle:
    stimmt, text = pruefe_anzahl(preise, zahl)
    assert stimmt, text

# Laufzeit: paar_mit_summe braucht O(n) Zugriffe
preise = list(range(1, 4001))
ergebnis, anzahl = zugriffe(paar_mit_summe, preise, 10000)
if ergebnis is not None:
    text = f"paar_mit_summe für 4000 Preise ohne passendes Paar ergibt {ergebnis!r}, erwartet war None."
else:
    text = (
        f"paar_mit_summe für 4000 Preise ohne passendes Paar braucht {anzahl} Zugriffe auf preise; "
        f"erlaubt sind {4 * len(preise) + 10} (O(n)). Zwei verschachtelte Schleifen brauchen etwa acht Millionen.\n"
        "Tipp: Bei jedem Durchlauf rückt einer der beiden Zeiger um eins."
    )
assert ergebnis is None and anzahl <= 4 * len(preise) + 10, text

# Laufzeit: anzahl_unter braucht O(n) Zugriffe
ergebnis, anzahl = zugriffe(anzahl_unter, preise, 4001)
erwartet = vergleich_anzahl(preise, 4001)
if ergebnis != erwartet:
    text = f"anzahl_unter für 4000 Preise und die Grenze 4001 ergibt {ergebnis!r}, erwartet war {erwartet}."
else:
    text = (
        f"anzahl_unter für 4000 Preise braucht {anzahl} Zugriffe auf preise; "
        f"erlaubt sind {4 * len(preise) + 10} (O(n)).\n"
        "Tipp: Zählen Sie bei einer zu kleinen Summe alle rechts - links Paare auf einmal, statt sie einzeln abzugehen."
    )
assert ergebnis == erwartet and anzahl <= 4 * len(preise) + 10, text

# Obere Grenze: paar_mit_summe bei 100 000 Preisen
preise = zufallspreise(zufall, 100000, 1000000)
stimmt, text = pruefe_paar(preise, preise[100] + preise[99000])
assert stimmt, text

# Obere Grenze: anzahl_unter bei 100 000 Preisen
stimmt, text = pruefe_anzahl(preise, 1000000)
assert stimmt, text
