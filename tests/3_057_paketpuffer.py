# Automatisch erzeugt aus lehrkraft/muster/3_057_paketpuffer.py - nicht von Hand ändern.
# vorlage-hash: cc243b2bb7d6118c
# text-hash: 995118162d9ecc67
# thema: datenstrukturen
# inhalt: Warteschlange mit deque

import copy

BEISPIEL = [["a", "b", "c"], [], ["d", "e"], ["f"]]


def wert_von(funktion, ankuenfte, platz):
    """Ruft funktion mit einer Kopie von ankuenfte auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(copy.deepcopy(ankuenfte), platz)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich(ankuenfte, platz):
    """Langsame Vergleichslösung: eine Liste mit pop(0), Ankunftstakt im Paar."""
    puffer = []
    gesendet = []
    verworfen = []
    warten = {}
    takt = 0
    while takt < len(ankuenfte) or len(puffer) > 0:
        neue = ankuenfte[takt] if takt < len(ankuenfte) else []
        for name in neue:
            if len(puffer) == platz:
                verworfen.append(name)
            else:
                puffer.append((takt, name))
        if len(puffer) > 0:
            ankunft, name = puffer.pop(0)
            gesendet.append((takt, name))
            warten[name] = takt - ankunft
        takt += 1
    return (gesendet, verworfen), warten


def gezeigt(ankuenfte):
    """Kürzt lange Eingaben für die Meldung."""
    if sum(len(takt) for takt in ankuenfte) <= 20:
        return repr(ankuenfte)
    return f"<{len(ankuenfte)} Takte, {sum(len(takt) for takt in ankuenfte)} Pakete>"


def meldung(funktion, ankuenfte, platz, erwartet, hinweis=""):
    """Prüft funktion(ankuenfte, platz) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, ankuenfte, platz)
    text = (
        f"{funktion.__name__}({gezeigt(ankuenfte)}, {platz})\n"
        f"ergibt   {ergebnis!r}\nerwartet {erwartet!r}{hinweis}"
    )
    return ergebnis == erwartet, text


def pruefe_beide(ankuenfte, platz, hinweis=""):
    """Prüft weiterleiten und wartezeiten gegen die Vergleichslösung; liefert (stimmt, Meldung)."""
    erwartet_weiter, erwartet_warten = vergleich(ankuenfte, platz)
    stimmt, text = meldung(weiterleiten, ankuenfte, platz, erwartet_weiter, hinweis)
    if not stimmt:
        return stimmt, text
    return meldung(wartezeiten, ankuenfte, platz, erwartet_warten, hinweis)


def zufallsankuenfte(zufall, takte, hoechstens):
    """Erzeugt Takte mit 0 bis hoechstens Paketen, alle Namen verschieden."""
    ankuenfte = []
    nummer = 0
    for _ in range(takte):
        takt = []
        for _ in range(zufall.randint(0, hoechstens)):
            takt.append(f"p{nummer}")
            nummer += 1
        ankuenfte.append(takt)
    return ankuenfte


# weiterleiten: das Beispiel
stimmt, text = meldung(
    weiterleiten, BEISPIEL, 2, ([(0, "a"), (1, "b"), (2, "d"), (3, "e"), (4, "f")], ["c"]),
    "\nTipp: Erst stellen sich die neuen Pakete an, dann wird das vorderste gesendet.",
)
assert stimmt, text

# weiterleiten: genug Platz, nichts wird verworfen
stimmt, text = meldung(weiterleiten, [["x", "y"], ["z"]], 5, ([(0, "x"), (1, "y"), (2, "z")], []))
assert stimmt, text

# weiterleiten: das vorderste Paket zuerst (nicht das zuletzt angekommene)
stimmt, text = meldung(
    weiterleiten, [["x", "y", "z"]], 3, ([(0, "x"), (1, "y"), (2, "z")], []),
    "\nTipp: Eine Warteschlange gibt mit popleft() das Paket zurück, das am längsten wartet; pop() wäre ein Stapel.",
)
assert stimmt, text

# weiterleiten: bei vollem Puffer wird das neue Paket verworfen, nicht das älteste
stimmt, text = meldung(
    weiterleiten, [["a", "b", "c", "d"]], 2, ([(0, "a"), (1, "b")], ["c", "d"]),
    "\nTipp: Prüfen Sie vor dem Anhängen len(puffer) < platz; deque(maxlen=…) würde das älteste hinauswerfen.",
)
assert stimmt, text

# weiterleiten: nach dem letzten Takt wird weiter gesendet
stimmt, text = meldung(
    weiterleiten, [["a", "b", "c"]], 3, ([(0, "a"), (1, "b"), (2, "c")], []),
    "\nTipp: Die Schleife läuft, solange Takte übrig sind oder der Puffer nicht leer ist.",
)
assert stimmt, text

# weiterleiten: das Senden in Takt t macht Platz erst für Takt t + 1
stimmt, text = meldung(
    weiterleiten, [["a"], ["b", "c"]], 1, ([(0, "a"), (1, "b")], ["c"]),
    "\nTipp: In Takt 1 ist a schon gesendet; b passt in den Puffer, c nicht mehr.",
)
assert stimmt, text

# weiterleiten: leere Takte am Anfang
stimmt, text = meldung(weiterleiten, [[], [], ["a"]], 1, ([(2, "a")], []))
assert stimmt, text

# weiterleiten: keine Takte
stimmt, text = meldung(weiterleiten, [], 4, ([], []))
assert stimmt, text

# weiterleiten: nur leere Takte
stimmt, text = meldung(weiterleiten, [[], []], 4, ([], []))
assert stimmt, text

# wartezeiten: das Beispiel
stimmt, text = meldung(
    wartezeiten, BEISPIEL, 2, {"a": 0, "b": 1, "d": 0, "e": 1, "f": 1},
    "\nTipp: Merken Sie sich für jedes Paket den Takt, in dem es ankam.",
)
assert stimmt, text

# wartezeiten: verworfene Pakete fehlen
stimmt, text = meldung(
    wartezeiten, [["a", "b", "c"], ["d"]], 2, {"a": 0, "b": 1, "d": 1},
    "\nTipp: Nur gesendete Pakete bekommen eine Wartezeit.",
)
assert stimmt, text

# wartezeiten: keine Takte
stimmt, text = meldung(wartezeiten, [], 1, {})
assert stimmt, text

# weiterleiten verändert ankuenfte nicht
ankuenfte = copy.deepcopy(BEISPIEL)
try:
    weiterleiten(ankuenfte, 2)
except Exception:
    pass
assert ankuenfte == BEISPIEL, f"Nach weiterleiten ist ankuenfte {ankuenfte}; es sollte unverändert bleiben."

# Der Puffer ist eine deque
assert verwendet("deque") and verwendet("popleft"), (
    "Ihr Code verwendet keine deque mit popleft(). Eine Liste mit pop(0) braucht für jedes Paket so viele "
    "Schritte, wie Pakete warten."
)

# Die Ausgabe des Programms
erwartet = "\n".join(str(teil) for teil in vergleich(BEISPIEL, 2))
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Ankünfte
zufall = Zufall(3057)
for _ in range(500):
    ankuenfte = zufallsankuenfte(zufall, zufall.randint(0, 8), zufall.randint(0, 4))
    stimmt, text = pruefe_beide(ankuenfte, zufall.randint(1, 5))
    assert stimmt, text

# Obere Grenze: 10 000 Takte mit zusammen etwa 100 000 Paketen, kleiner Puffer
ankuenfte = zufallsankuenfte(zufall, 10000, 19)
stimmt, text = pruefe_beide(ankuenfte, 50)
assert stimmt, text

# Obere Grenze: 100 000 Pakete auf einmal in einen großen Puffer
ankuenfte = [[f"p{nummer}" for nummer in range(100000)]]
ergebnis = wert_von(weiterleiten, ankuenfte, 100000)
assert ergebnis == ([(nummer, f"p{nummer}") for nummer in range(100000)], []), (
    "Bei 100 000 Paketen in einem Takt und platz 100000 stimmt weiterleiten nicht."
)
