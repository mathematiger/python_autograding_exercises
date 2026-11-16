# Automatisch erzeugt aus lehrkraft/muster/2_042_kabelweg.py - nicht von Hand ändern.
# vorlage-hash: bd0ba40e15d99994
# text-hash: 7d5f08b574a2341a
# thema: algorithmen
# inhalt: Wurzel per Bisektion

def wurzel_von_hand(x):
    """Vergleichswert mit dem Newton-Verfahren, sehr genau und unabhängig von der Bisektion."""
    if x == 0:
        return 0.0
    schaetzung = max(x, 1.0)
    for _ in range(200):
        schaetzung = (schaetzung + x / schaetzung) / 2
    return schaetzung


def pruefe_wurzel(x):
    """Ruft wurzel(x) auf; gibt None zurück, wenn alles stimmt, sonst eine Meldung."""
    ergebnis = wurzel(x)
    erwartet = wurzel_von_hand(x)
    if not isinstance(ergebnis, (int, float)) or isinstance(ergebnis, bool):
        return f"wurzel({x!r}) ergibt {ergebnis!r}, erwartet war eine Zahl nahe {erwartet:.4f}."
    if abs(ergebnis - erwartet) > 0.001:
        return (
            f"wurzel({x!r}) ergibt {ergebnis!r}, erwartet war eine Zahl nahe {erwartet:.4f} "
            f"(höchstens 0.001 daneben, Ihr Wert liegt {abs(ergebnis - erwartet):.4f} daneben)."
        )
    return None


# wurzel(25) ist etwa 5
fehler = pruefe_wurzel(25)
assert fehler is None, fehler + (
    "\nTipp: Ist mitte * mitte größer als x, wird oben = mitte, sonst unten = mitte."
)

# Eine andere Zahl (nicht fest hinschreiben!): wurzel(2) ist etwa 1.414
fehler = pruefe_wurzel(2)
assert fehler is None, fehler

# Eine dritte Zahl: wurzel(1000) ist etwa 31.623
fehler = pruefe_wurzel(1000)
assert fehler is None, fehler

# kabelweg(30, 40) ist etwa 50
ergebnis = kabelweg(30, 40)
assert isinstance(ergebnis, (int, float)) and abs(ergebnis - 50) <= 0.001, (
    f"kabelweg(30, 40) ergibt {ergebnis!r}, erwartet war etwa 50.0.\n"
    "Tipp: Der Weg ist wurzel(breite * breite + tiefe * tiefe)."
)

# kabelweg mit anderen Maßen
ergebnis = kabelweg(5, 12)
assert isinstance(ergebnis, (int, float)) and abs(ergebnis - 13) <= 0.001, f"kabelweg(5, 12) ergibt {ergebnis!r}, erwartet war etwa 13.0."

# kabelweg benutzt wurzel
assert verwendet("wurzel"), "kabelweg soll die Funktion wurzel aufrufen."

# math.sqrt wird nicht benutzt
assert not verwendet("sqrt") and not verwendet("isqrt"), "Benutzen Sie nicht math.sqrt, sondern die Bisektion."

# Die Bisektion braucht eine Schleife (** 0.5 kommt ohne aus)
assert verwendet("while") or verwendet("for"), (
    "Ihr Code hat keine Schleife. Nähern Sie die Wurzel mit der Bisektion in einer while-Schleife an, "
    "statt sie mit ** 0.5 auszurechnen."
)

# Auch Kommazahlen: wurzel(6.25) ist etwa 2.5
fehler = pruefe_wurzel(6.25)
assert fehler is None, fehler

# Zahlen unter 1: wurzel(0.25) ist etwa 0.5
fehler = pruefe_wurzel(0.25)
assert fehler is None, fehler + (
    "\nTipp: Die Wurzel einer Zahl unter 1 ist größer als die Zahl; beginnen Sie mit oben = max(x, 1)."
)

# Untere Grenze: wurzel(0) ist etwa 0
fehler = pruefe_wurzel(0)
assert fehler is None, fehler

# wurzel(1) ist etwa 1
fehler = pruefe_wurzel(1)
assert fehler is None, fehler

# kabelweg ohne Versatz: kabelweg(0, 0) ist etwa 0
ergebnis = kabelweg(0, 0)
assert isinstance(ergebnis, (int, float)) and abs(ergebnis) <= 0.001, f"kabelweg(0, 0) ergibt {ergebnis!r}, erwartet war etwa 0.0."

# kabelweg in nur eine Richtung: kabelweg(0, 7) ist etwa 7
ergebnis = kabelweg(0, 7)
assert isinstance(ergebnis, (int, float)) and abs(ergebnis - 7) <= 0.001, f"kabelweg(0, 7) ergibt {ergebnis!r}, erwartet war etwa 7.0."

# 300 zufällige Zahlen von 0 bis 10**6
zufall = Zufall(2042)
for _ in range(300):
    exponent = zufall.randint(-3, 6)
    x = round(zufall.uniform(0, 10**exponent), 3)
    fehler = pruefe_wurzel(x)
    assert fehler is None, fehler

# 100 zufällige Kabelwege
for _ in range(100):
    breite = zufall.randint(0, 500)
    tiefe = round(zufall.uniform(0, 500), 1)
    ergebnis = kabelweg(breite, tiefe)
    erwartet = wurzel_von_hand(breite * breite + tiefe * tiefe)
    assert isinstance(ergebnis, (int, float)) and abs(ergebnis - erwartet) <= 0.001, (
        f"kabelweg({breite}, {tiefe}) ergibt {ergebnis!r}, erwartet war etwa {erwartet:.4f}."
    )

# Obere Grenze: wurzel(10**6) ist etwa 1000
fehler = pruefe_wurzel(10**6)
assert fehler is None, fehler

# Obere Grenze: kabelweg(500, 500) ist etwa 707.107
ergebnis = kabelweg(500, 500)
erwartet = wurzel_von_hand(500000)
assert isinstance(ergebnis, (int, float)) and abs(ergebnis - erwartet) <= 0.001, (
    f"kabelweg(500, 500) ergibt {ergebnis!r}, erwartet war etwa {erwartet:.4f}."
)

# Wenige Schritte auch bei 10**6: der Bereich wird halbiert
ergebnis, schritte = zaehle_schritte(wurzel, 10**6)
assert schritte <= 1000, (
    f"wurzel(10**6) hat {schritte} Schritte gebraucht; mit Bisektion genügen etwa 30 Halbierungen, also "
    "höchstens 1000 Schritte.\nTipp: Probieren Sie nicht alle Zahlen in kleinen Schritten durch, sondern halbieren "
    "Sie den Bereich zwischen unten und oben."
)
