# Automatisch erzeugt aus lehrkraft/muster/4_078_testimages.py - nicht von Hand ändern.
# vorlage-hash: 7414f7c3325d4220
# text-hash: 0b10ef5edef6bdce
# thema: algorithmen
# inhalt: Binäre Suche auf der Antwort

BEISPIEL = [600, 900, 300, 1200, 500]


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def kurz(liste):
    """Kürzt lange Listen für Meldungen."""
    if len(liste) <= 12:
        return repr(liste)
    return f"<Liste mit {len(liste)} Größen, beginnend mit {liste[:5]!r}>"


def passt_von_hand(groessen, fenster, laenge, bandbreite):
    """Vergleichslösung: verteilt die Dauern Nacht für Nacht und zählt die Nächte."""
    naechte = []
    for groesse in groessen:
        dauer = -(-groesse // bandbreite)
        if dauer > laenge:
            return False
        if naechte and sum(naechte[-1]) + dauer <= laenge:
            naechte[-1].append(dauer)
        else:
            naechte.append([dauer])
    return len(naechte) <= fenster


def kleinste_von_hand(groessen, fenster, laenge):
    """Langsame Vergleichslösung: probiert die Bandbreiten von 1 an der Reihe nach."""
    if len(groessen) > fenster * laenge:
        return None
    bandbreite = 1
    while not passt_von_hand(groessen, fenster, laenge, bandbreite):
        bandbreite += 1
    return bandbreite


def pruefe_passt(groessen, fenster, laenge, bandbreite, erwartet, tipp=""):
    """Prüft passt; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(passt, list(groessen), fenster, laenge, bandbreite)
    text = (
        f"passt({kurz(groessen)}, {fenster}, {laenge}, {bandbreite}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    )
    if ergebnis is None:
        text += "\nTipp: Geben Sie True oder False mit return zurück."
    elif tipp:
        text += "\nTipp: " + tipp
    return ergebnis is erwartet or ergebnis == erwartet and isinstance(ergebnis, bool), text


def pruefe_kleinste(groessen, fenster, laenge, erwartet, tipp=""):
    """Prüft kleinste_bandbreite; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(kleinste_bandbreite, list(groessen), fenster, laenge)
    text = (
        f"kleinste_bandbreite({kurz(groessen)}, {fenster}, {laenge}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )
    if erwartet is not None and isinstance(ergebnis, int) and ergebnis == erwartet + 1:
        text += "\nTipp: Mit Ihrem Ergebnis minus 1 passt es auch schon. Prüfen Sie die Grenzen Ihrer Suche."
    elif tipp:
        text += "\nTipp: " + tipp
    if erwartet is None:
        return ergebnis is None, text
    return ergebnis == erwartet and not isinstance(ergebnis, bool), text


# passt: das Beispiel mit 200 MB/s passt in zwei Nächte
stimmt, text = pruefe_passt(BEISPIEL, 2, 10, 200, True)
assert stimmt, text

# passt: das Beispiel mit 199 MB/s braucht drei Nächte
stimmt, text = pruefe_passt(
    BEISPIEL, 2, 10, 199, False, "Bei 199 MB/s dauern die Images 4, 5, 2, 7 und 3 Sekunden (aufgerundet)."
)
assert stimmt, text

# passt: andere Images (nicht fest hinschreiben!)
stimmt, text = pruefe_passt([800, 200, 700, 300, 400, 900], 3, 6, 225, True)
stimmt_zwei, text_zwei = pruefe_passt([800, 200, 700, 300, 400, 900], 3, 6, 224, False)
assert stimmt and stimmt_zwei, text if not stimmt else text_zwei

# passt: mit mehr Nächten reicht eine kleinere Bandbreite
stimmt, text = pruefe_passt(
    BEISPIEL, 3, 10, 150, True, "Zählen Sie die benutzten Nächte und vergleichen Sie mit fenster."
)
assert stimmt, text

# passt: jede Übertragung dauert volle Sekunden (aufrunden)
stimmt, text = pruefe_passt(
    [150, 150],
    1,
    3,
    100,
    False,
    "150 MB bei 100 MB/s dauern 2 Sekunden, nicht 1,5. Runden Sie jede Dauer einzeln auf, "
    "z. B. mit (groesse + bandbreite - 1) // bandbreite.",
)
assert stimmt, text

# passt: ein Image, das das Fenster genau füllt, passt noch hinein
stimmt, text = pruefe_passt(
    [400, 600], 1, 10, 100, True, "4 + 6 = 10 Sekunden füllen das Fenster genau; das passt (<=, nicht <)."
)
assert stimmt, text

# passt: Übertragungen werden nicht auf zwei Nächte verteilt
stimmt, text = pruefe_passt(
    [600, 600, 600],
    2,
    10,
    100,
    False,
    "Zusammen sind es 18 Sekunden, aber in eine Nacht passt nur ein Image mit 6 Sekunden; "
    "das zweite wartet auf die nächste Nacht. Zählen Sie Nächte, nicht nur die Summe der Sekunden.",
)
assert stimmt, text

# passt: ein Image, das länger dauert als ein ganzes Fenster, passt nie
stimmt, text = pruefe_passt(
    [100, 1500, 100],
    100,
    10,
    100,
    False,
    "Das zweite Image dauert 15 Sekunden, ein Fenster hat nur 10. Es passt in keine Nacht, egal wie viele es gibt.",
)
assert stimmt, text

# passt: die erste Nacht wird genutzt, die Zählung beginnt nicht bei 0 Nächten
stimmt, text = pruefe_passt([500], 1, 10, 100, True, "Ein einziges Image von 5 Sekunden passt in eine Nacht.")
assert stimmt, text

# passt: ohne Images passt es
stimmt, text = pruefe_passt([], 1, 10, 1, True)
assert stimmt, text

# passt: die Liste groessen bleibt unverändert
eingabe = list(BEISPIEL)
wert_von(passt, eingabe, 2, 10, 200)
assert eingabe == BEISPIEL, f"passt hat die übergebene Liste verändert, sie ist jetzt {eingabe!r}."

# kleinste_bandbreite: das Beispiel mit zwei Nächten
stimmt, text = pruefe_kleinste(BEISPIEL, 2, 10, 200)
assert stimmt, text

# kleinste_bandbreite: das Beispiel mit drei Nächten
stimmt, text = pruefe_kleinste(BEISPIEL, 3, 10, 150)
assert stimmt, text

# kleinste_bandbreite: andere Images (nicht fest hinschreiben!)
stimmt, text = pruefe_kleinste([800, 200, 700, 300, 400, 900], 3, 6, 225)
assert stimmt, text

# kleinste_bandbreite: unmöglich, wenn mehr Images als Sekunden da sind
stimmt, text = pruefe_kleinste(
    [1, 1, 1],
    1,
    2,
    None,
    "Jede Übertragung dauert mindestens 1 Sekunde, aber es gibt nur 2 Sekunden. Prüfen Sie vor der Suche, "
    "ob die größte sinnvolle Bandbreite passt; sonst geben Sie None zurück.",
)
assert stimmt, text

# kleinste_bandbreite: schon 1 MB/s reicht
stimmt, text = pruefe_kleinste([3, 4], 1, 10, 1, "Die Suche muss bei 1 beginnen, nicht bei 2 oder 0.")
assert stimmt, text

# kleinste_bandbreite: jede Übertragung muss in einer Sekunde fertig sein
stimmt, text = pruefe_kleinste(
    [5, 7, 3], 3, 1, 7, "Jedes Fenster ist 1 Sekunde lang; die obere Grenze der Suche muss max(groessen) einschließen."
)
assert stimmt, text

# kleinste_bandbreite: ohne Images reicht 1
stimmt, text = pruefe_kleinste([], 1, 1, 1, "Ohne Images genügt jede Bandbreite, die kleinste ist 1.")
assert stimmt, text

# Viele zufällige Fälle, verglichen mit dem Durchprobieren von 1 an
zufall = Zufall(4078)
for runde in range(300):
    groessen = [zufall.randint(1, 60) for _ in range(zufall.randint(0, 8))]
    fenster = zufall.randint(1, 4)
    laenge = zufall.randint(1, 12)
    bandbreite = zufall.randint(1, 30)
    stimmt, text = pruefe_passt(groessen, fenster, laenge, bandbreite, passt_von_hand(groessen, fenster, laenge, bandbreite))
    assert stimmt, text
    stimmt, text = pruefe_kleinste(groessen, fenster, laenge, kleinste_von_hand(groessen, fenster, laenge))
    assert stimmt, text

# Laufzeit: kleinste_bandbreite sucht binär, statt alle Bandbreiten durchzuprobieren
proben = []
for faktor in [1, 64]:
    groessen = [faktor * zufall.randint(50, 100) for _ in range(20)]
    erwartet = kleinste_von_hand(groessen, 4, 10)
    ergebnis, schritte = zaehle_schritte(kleinste_bandbreite, list(groessen), 4, 10)
    proben.append((ergebnis == erwartet, ergebnis, erwartet, max(schritte, 1)))
richtig = proben[0][0] and proben[1][0]
schritte_klein = proben[0][3]
schritte_gross = proben[1][3]
assert richtig and schritte_gross <= 4 * schritte_klein, (
    f"Für 20 Images braucht kleinste_bandbreite bei einer Antwort um {proben[0][2]} MB/s {schritte_klein} Schritte, "
    f"bei einer 64-mal so großen Antwort ({proben[1][2]} MB/s) {schritte_gross}, also "
    f"{schritte_gross / schritte_klein:.1f}-mal so viele. Bei binärer Suche wären es höchstens etwa doppelt so viele "
    "(log₂ wächst nur um 6), beim Durchprobieren von 1 an 64-mal so viele.\n"
    "Tipp: Halbieren Sie den Bereich der möglichen Bandbreiten bei jeder Frage an passt."
    if richtig
    else f"Ergebnisse {proben[0][1]!r} und {proben[1][1]!r}, erwartet waren {proben[0][2]} und {proben[1][2]}."
)

# kleinste_bandbreite: ein einziges Image von 10**9 MB in einer Sekunde
stimmt, text = pruefe_kleinste([10**9], 1, 1, 10**9)
assert stimmt, text

# Obere Grenze: 10 000 Images bis 10**9 MB
groessen = [zufall.randint(1, 10**9) for _ in range(10000)]
fenster, laenge = 50, 10**6
ergebnis = wert_von(kleinste_bandbreite, list(groessen), fenster, laenge)
gueltig = (
    isinstance(ergebnis, int)
    and not isinstance(ergebnis, bool)
    and 1 <= ergebnis
    and passt_von_hand(groessen, fenster, laenge, ergebnis)
    and (ergebnis == 1 or not passt_von_hand(groessen, fenster, laenge, ergebnis - 1))
)
assert gueltig, (
    f"Bei 10 000 Images bis 10**9 MB, {fenster} Nächten zu {laenge} Sekunden ergibt kleinste_bandbreite {ergebnis!r}; "
    "das ist nicht die kleinste passende Bandbreite."
)
