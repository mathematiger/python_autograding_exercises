# Automatisch erzeugt aus lehrkraft/muster/3_071_serientickets.py - nicht von Hand ändern.
# vorlage-hash: 5349825563b39b40
# text-hash: 01ce07a5ff043769
# thema: algorithmen
# inhalt: ggT und kgV, euklidischer Algorithmus

def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_ggt(a, b):
    """Vergleichslösung für kleine Zahlen: probiert alle Teiler von der größten Möglichkeit abwärts."""
    if a == 0 or b == 0:
        return a + b
    for teiler in range(min(a, b), 0, -1):
        if a % teiler == 0 and b % teiler == 0:
            return teiler


def vergleich_kgv(a, b):
    """Vergleichslösung für kleine Zahlen: geht die Vielfachen von a durch, bis b eines teilt."""
    vielfaches = a
    while vielfaches % b != 0:
        vielfaches += a
    return vielfaches


def zerlegt(zahl):
    """Vergleichslösung für Listen: Primfaktorzerlegung als Dictionary Primzahl → Exponent."""
    faktoren = {}
    teiler = 2
    while teiler * teiler <= zahl:
        while zahl % teiler == 0:
            faktoren[teiler] = faktoren.get(teiler, 0) + 1
            zahl //= teiler
        teiler += 1
    if zahl > 1:
        faktoren[zahl] = faktoren.get(zahl, 0) + 1
    return faktoren


def kgv_ueber_faktoren(intervalle):
    """Vergleichslösung: kgV als Produkt jeder Primzahl mit ihrem höchsten Exponenten."""
    hoechste = {}
    for intervall in intervalle:
        for primzahl, exponent in zerlegt(intervall).items():
            hoechste[primzahl] = max(hoechste.get(primzahl, 0), exponent)
    ergebnis = 1
    for primzahl, exponent in hoechste.items():
        ergebnis *= primzahl**exponent
    return ergebnis


def ggt_ueber_faktoren(intervalle):
    """Vergleichslösung: ggT als Produkt jeder gemeinsamen Primzahl mit ihrem kleinsten Exponenten."""
    zerlegungen = [zerlegt(intervall) for intervall in intervalle]
    ergebnis = 1
    for primzahl, exponent in zerlegungen[0].items():
        kleinster = min(zerlegung.get(primzahl, 0) for zerlegung in zerlegungen)
        ergebnis *= primzahl**kleinster
    return ergebnis


def pruefe(funktion, argumente, erwartet, hinweis=""):
    """Prüft funktion(*argumente) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, *argumente)
    gezeigt = ", ".join(repr(argument) for argument in argumente)
    if isinstance(ergebnis, float):
        hinweis += "\nTipp: Rechnen Sie mit // statt /, dann bleibt das Ergebnis eine ganze Zahl und wird nicht gerundet."
    return ergebnis == erwartet, f"{funktion.__name__}({gezeigt}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"


# ggt: das Beispiel aus der Aufgabe
stimmt, text = pruefe(ggt, (12, 18), 6, "\nTipp: Ersetzen Sie (a, b) durch (b, a % b), bis b 0 ist.")
assert stimmt, text

# ggt: andere Zahlen (nicht fest hinschreiben!)
stimmt, text = pruefe(ggt, (84, 120), 12)
assert stimmt, text

# ggt: die erste Zahl ist größer
stimmt, text = pruefe(ggt, (120, 84), 12)
assert stimmt, text

# ggt: teilerfremde Zahlen ergeben 1
stimmt, text = pruefe(ggt, (35, 64), 1)
assert stimmt, text

# ggt: eine Zahl teilt die andere
stimmt, text = pruefe(ggt, (7, 91), 7)
assert stimmt, text

# ggt: zwei gleiche Zahlen
stimmt, text = pruefe(ggt, (45, 45), 45)
assert stimmt, text

# ggt: b = 0 ergibt a
stimmt, text = pruefe(ggt, (30, 0), 30, "\nTipp: ggT(a, 0) = a ist der Rekursionsanfang bzw. das Ende der Schleife.")
assert stimmt, text

# ggt: a = 0 ergibt b
stimmt, text = pruefe(ggt, (0, 30), 30)
assert stimmt, text

# kgv: das Beispiel aus der Aufgabe
stimmt, text = pruefe(kgv, (12, 18), 36, "\nTipp: kgV(a, b) = a · b // ggT(a, b)")
assert stimmt, text

# kgv: andere Zahlen (nicht fest hinschreiben!)
stimmt, text = pruefe(kgv, (8, 20), 40)
assert stimmt, text

# kgv: teilerfremde Zahlen ergeben das Produkt
stimmt, text = pruefe(kgv, (9, 14), 126)
assert stimmt, text

# kgv: eine Zahl teilt die andere
stimmt, text = pruefe(kgv, (6, 24), 24)
assert stimmt, text

# kgv: mit 1
stimmt, text = pruefe(kgv, (1, 17), 17)
assert stimmt, text

# kgv: das Ergebnis ist eine ganze Zahl, auch bei großen Zahlen
stimmt, text = pruefe(kgv, (2**58 + 1, 3 * (2**58 + 1)), 3 * (2**58 + 1))
assert stimmt, text

# gemeinsam_faellig: das Beispiel aus der Aufgabe
stimmt, text = pruefe(
    gemeinsam_faellig, ([12, 18, 30],), 180,
    "\nTipp: Nehmen Sie die Intervalle nacheinander dazu: kgV(kgV(12, 18), 30).",
)
assert stimmt, text

# gemeinsam_faellig: andere Intervalle (nicht fest hinschreiben!)
stimmt, text = pruefe(gemeinsam_faellig, ([4, 6, 10, 15],), 60)
assert stimmt, text

# gemeinsam_faellig: ein einziges Serienticket
stimmt, text = pruefe(gemeinsam_faellig, ([14],), 14, "\nTipp: Beginnen Sie mit 1, denn kgV(1, x) = x.")
assert stimmt, text

# gemeinsam_faellig: Doppelte ändern nichts
stimmt, text = pruefe(gemeinsam_faellig, ([7, 7, 7],), 7)
assert stimmt, text

# gemeinsam_faellig: tägliche Tickets
stimmt, text = pruefe(gemeinsam_faellig, ([1, 1],), 1)
assert stimmt, text

# pruefrhythmus: das Beispiel aus der Aufgabe
stimmt, text = pruefe(
    pruefrhythmus, ([12, 18, 30],), 6,
    "\nTipp: Nehmen Sie die Intervalle nacheinander dazu: ggT(ggT(12, 18), 30).",
)
assert stimmt, text

# pruefrhythmus: andere Intervalle (nicht fest hinschreiben!)
stimmt, text = pruefe(pruefrhythmus, ([28, 42, 70],), 14)
assert stimmt, text

# pruefrhythmus: ein einziges Serienticket
stimmt, text = pruefe(pruefrhythmus, ([14],), 14, "\nTipp: Beginnen Sie mit 0 oder dem ersten Intervall, denn ggT(0, x) = x.")
assert stimmt, text

# pruefrhythmus: teilerfremde Intervalle ergeben 1
stimmt, text = pruefe(pruefrhythmus, ([6, 10, 15],), 1)
assert stimmt, text

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar("6 36\n180 6"), f"Erwartete Ausgabe:\n6 36\n180 6\nIhr Programm:\n{AUSGABE}"

# Den Algorithmus selbst schreiben, nicht math.gcd oder math.lcm
assert not verwendet("gcd") and not verwendet("lcm"), (
    "Ihr Programm ruft gcd oder lcm auf. Schreiben Sie den euklidischen Algorithmus selbst, siehe Hintergrund."
)

zufall = Zufall(3071)

# ggt und kgv: viele zufällige Paare
for _ in range(300):
    a = zufall.randint(1, zufall.choice([20, 1000]))
    b = zufall.randint(1, zufall.choice([20, 1000]))
    stimmt, text = pruefe(ggt, (a, b), vergleich_ggt(a, b))
    assert stimmt, text
    stimmt, text = pruefe(kgv, (a, b), vergleich_kgv(a, b))
    assert stimmt, text

# gemeinsam_faellig und pruefrhythmus: viele zufällige Listen
for _ in range(200):
    faktor = zufall.choice([1, 2, 6, 7])
    intervalle = [faktor * zufall.randint(1, 60) for _ in range(zufall.randint(1, 6))]
    stimmt, text = pruefe(gemeinsam_faellig, (intervalle,), kgv_ueber_faktoren(intervalle))
    assert stimmt, text
    stimmt, text = pruefe(pruefrhythmus, (intervalle,), ggt_ueber_faktoren(intervalle))
    assert stimmt, text

# Laufzeit: ggt braucht O(log n) Schritte
ergebnis, schritte = zaehle_schritte(ggt, 1_000_000, 999_999)
assert ergebnis == 1 and schritte <= 200, (
    f"ggt(1000000, 999999) ergibt {ergebnis!r} mit {schritte} Schritten; erwartet war 1 mit höchstens 200 "
    "Schritten (O(log n)). Alle Teiler durchzuprobieren braucht fast eine Million Schritte, wiederholtes "
    "Abziehen ebenso.\nTipp: Rechnen Sie mit dem Rest a % b statt mit a - b."
)

# Obere Grenze: ggt mit 18-stelligen Zahlen (aufeinanderfolgende Fibonacci-Zahlen sind der ungünstigste Fall)
fibonacci = [1, 1]
while fibonacci[-1] < 10**18:
    fibonacci.append(fibonacci[-1] + fibonacci[-2])
a, b = fibonacci[-2], fibonacci[-3]
ergebnis, schritte = zaehle_schritte(ggt, a, b)
assert ergebnis == 1 and schritte <= 400, (
    f"ggt({a}, {b}) ergibt {ergebnis!r} mit {schritte} Schritten; erwartet war 1 mit höchstens 400 Schritten."
)

# Obere Grenze: ggt mit gemeinsamem großem Teiler
stimmt, text = pruefe(ggt, (999_999_999_989 * 999_983, 999_999_999_989 * 999_979), 999_999_999_989)
assert stimmt, text

# Obere Grenze: gemeinsam_faellig mit 1000 Intervallen bis 10**6
intervalle = [zufall.randint(1, 10**6) for _ in range(1000)]
erwartet = kgv_ueber_faktoren(intervalle)
ergebnis = wert_von(gemeinsam_faellig, intervalle)
assert ergebnis == erwartet, (
    f"gemeinsam_faellig mit 1000 Intervallen bis 10**6 ergibt {str(ergebnis)[:40]}…, erwartet war eine Zahl "
    f"mit {len(str(erwartet))} Stellen, beginnend mit {str(erwartet)[:40]}."
)

# Obere Grenze: pruefrhythmus mit 1000 Intervallen bis 10**6
rhythmus = zufall.randint(1, 1000)
intervalle = [rhythmus * zufall.randint(1, 10**6 // rhythmus) for _ in range(1000)]
stimmt, text = pruefe(pruefrhythmus, (intervalle,), ggt_ueber_faktoren(intervalle))
assert stimmt, text.replace(repr(intervalle), "<1000 Intervalle>")
