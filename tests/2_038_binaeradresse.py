# Automatisch erzeugt aus lehrkraft/muster/2_038_binaeradresse.py - nicht von Hand ändern.
# vorlage-hash: 85b580579afb4a1c
# text-hash: 7fb6b5f7ebd26fb9
# thema: algorithmen
# inhalt: Binärdarstellung von Hand

def binaer_mit_format(zahl, stellen):
    """Vergleichslösung mit format, das hier nur die Tests benutzen."""
    return format(zahl, "b").zfill(stellen)


def adresse_mit_format(adresse):
    """Vergleichslösung mit format für die ganze Adresse."""
    return ".".join(format(int(teil), "08b") for teil in adresse.split("."))


# Die Beispiele aus der Aufgabe
for zahl, stellen, erwartet in [(5, 4, "0101"), (192, 8, "11000000"), (0, 3, "000")]:
    ergebnis = als_binaer(zahl, stellen)
    assert ergebnis == erwartet, f"als_binaer({zahl}, {stellen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Andere Zahlen (nicht fest hinschreiben!)
for zahl, stellen, erwartet in [(13, 4, "1101"), (13, 8, "00001101"), (255, 8, "11111111"), (6, 3, "110")]:
    ergebnis = als_binaer(zahl, stellen)
    tipp = ""
    if ergebnis == erwartet[::-1]:
        tipp = "\nTipp: Die Ziffern kommen von hinten heraus. Setzen Sie jede neue Ziffer vorn an: ziffer + text."
    assert ergebnis == erwartet, f"als_binaer({zahl}, {stellen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{tipp}"

# Führende Nullen bis zur verlangten Länge
for zahl, stellen, erwartet in [(1, 8, "00000001"), (0, 1, "0"), (1, 1, "1"), (2, 5, "00010")]:
    ergebnis = als_binaer(zahl, stellen)
    assert ergebnis == erwartet, (
        f"als_binaer({zahl}, {stellen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Das Ergebnis hat immer genau stellen Zeichen; vorn fehlende Stellen sind Nullen."
    )

# als_binaer liefert einen Text
assert type(als_binaer(5, 4)) is str, (
    f"als_binaer(5, 4) ergibt {als_binaer(5, 4)!r} vom Typ {type(als_binaer(5, 4)).__name__}, erwartet war der Text '0101'."
)

# Die Adresse aus der Aufgabe
ergebnis = adresse_binaer("192.168.10.1")
assert ergebnis == "11000000.10101000.00001010.00000001", (
    f'adresse_binaer("192.168.10.1") ergibt {ergebnis!r}, erwartet war "11000000.10101000.00001010.00000001".'
)

# Andere Adressen, auch mit 0 und 255
for adresse in ["10.0.0.255", "0.0.0.0", "255.255.255.0", "172.16.254.3"]:
    ergebnis = adresse_binaer(adresse)
    erwartet = adresse_mit_format(adresse)
    assert ergebnis == erwartet, (
        f"adresse_binaer({adresse!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Jedes Oktett hat genau acht Stellen: als_binaer(int(teil), 8)."
    )

# Gerechnet wird von Hand, ohne bin(...) und format(...)
assert not verwendet("bin") and not verwendet("format"), (
    "Ihr Code benutzt bin(...) oder format(...). Rechnen Sie die Binärziffern selbst mit % 2 und // 2 aus."
)

# 500 zufällige Zahlen mit zufälliger Stellenzahl
zufall = Zufall(2038)
for _ in range(500):
    stellen = zufall.randint(1, 32)
    zahl = zufall.randint(0, 2**stellen - 1)
    ergebnis = als_binaer(zahl, stellen)
    erwartet = binaer_mit_format(zahl, stellen)
    assert ergebnis == erwartet, f"als_binaer({zahl}, {stellen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# 200 zufällige Adressen
for _ in range(200):
    adresse = ".".join(str(zufall.randint(0, 255)) for _ in range(4))
    ergebnis = adresse_binaer(adresse)
    erwartet = adresse_mit_format(adresse)
    assert ergebnis == erwartet, f"adresse_binaer({adresse!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Obere Grenze: 32 Stellen
for zahl in [2**32 - 1, 2**31, 0]:
    ergebnis = als_binaer(zahl, 32)
    erwartet = binaer_mit_format(zahl, 32)
    assert ergebnis == erwartet, f"als_binaer({zahl}, 32) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Die Ausgabe des Programms stimmt
assert AUSGABE == "0101\n11000000.10101000.00001010.00000001", (
    f"Erwartete Ausgabe:\n0101\n11000000.10101000.00001010.00000001\nIhr Programm gibt aus:\n{AUSGABE}"
)
