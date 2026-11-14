# Automatisch erzeugt aus lehrkraft/muster/2_039_inventarnummer.py - nicht von Hand ändern.
# vorlage-hash: ab89aacf72f54e8b
# text-hash: b4918e7f3597b08f
# thema: algorithmen
# inhalt: Ziffern mit // und %

def quersumme_vergleich(zahl):
    """Vergleichslösung über den Text der Zahl (in der Aufgabe selbst nicht erlaubt)."""
    return sum(int(ziffer) for ziffer in str(zahl))


def gueltig_vergleich(nummer):
    """Vergleichslösung für die Prüfziffer über den Text der Nummer."""
    text = str(nummer)
    return quersumme_vergleich(int(text[:-1])) % 10 == int(text[-1])


# Das Beispiel aus der Aufgabe: quersumme(4712) ist 14
ergebnis = quersumme(4712)
assert ergebnis == 14, (
    f"quersumme(4712) ergibt {ergebnis!r}, erwartet war 14 (4 + 7 + 1 + 2).\n"
    "Tipp: Addieren Sie zahl % 10 und machen Sie mit zahl // 10 weiter, solange zahl > 0 ist."
)

# Eine andere Zahl (nicht fest hinschreiben!)
ergebnis = quersumme(90817)
assert ergebnis == 25, f"quersumme(90817) ergibt {ergebnis!r}, erwartet war 25 (9 + 0 + 8 + 1 + 7)."

# Nullen in der Mitte und am Ende zählen nicht, die Schleife darf aber nicht vorher aufhören
ergebnis = quersumme(10500)
assert ergebnis == 6, (
    f"quersumme(10500) ergibt {ergebnis!r}, erwartet war 6 (1 + 0 + 5 + 0 + 0).\n"
    "Tipp: Hören Sie erst auf, wenn die ganze Zahl 0 ist, nicht schon bei der ersten Ziffer 0."
)

# Einstellige Zahlen
for zahl in [7, 9]:
    ergebnis = quersumme(zahl)
    assert ergebnis == zahl, f"quersumme({zahl}) ergibt {ergebnis!r}, erwartet war {zahl}."

# Die Zahl 0 hat die Quersumme 0
ergebnis = quersumme(0)
assert ergebnis == 0, f"quersumme(0) ergibt {ergebnis!r}, erwartet war 0."

# Das Beispiel aus der Aufgabe: 47124 ist gültig
ergebnis = nummer_gueltig(47124)
assert ergebnis is True, (
    f"nummer_gueltig(47124) ergibt {ergebnis!r}, erwartet war True (Quersumme von 4712 ist 14, Prüfziffer 4).\n"
    "Tipp: Die Prüfziffer ist nummer % 10, die übrigen Ziffern sind nummer // 10."
)

# Das Beispiel aus der Aufgabe: 47125 ist ungültig
ergebnis = nummer_gueltig(47125)
assert ergebnis is False, f"nummer_gueltig(47125) ergibt {ergebnis!r}, erwartet war False (Prüfziffer müsste 4 sein)."

# Die Prüfziffer ist die letzte Ziffer der Quersumme, nicht die ganze Quersumme
ergebnis = nummer_gueltig(99997)
assert ergebnis is False, (
    f"nummer_gueltig(99997) ergibt {ergebnis!r}, erwartet war False (Quersumme von 9999 ist 36, Prüfziffer 6)."
)
# 99996 ist gültig: Prüfziffer 6 ist die letzte Ziffer der Quersumme 36
ergebnis = nummer_gueltig(99996)
assert ergebnis is True, (
    f"nummer_gueltig(99996) ergibt {ergebnis!r}, erwartet war True (Quersumme von 9999 ist 36, Prüfziffer 6).\n"
    "Tipp: Vergleichen Sie quersumme(...) % 10 mit der letzten Ziffer."
)

# Kleinste Nummern: 10 (Quersumme 1, Prüfziffer 0 falsch) und 11 (richtig)
ergebnisse = (nummer_gueltig(10), nummer_gueltig(11))
assert ergebnisse == (False, True), f"nummer_gueltig(10) und nummer_gueltig(11) ergeben {ergebnisse!r}, erwartet war (False, True)."

# Prüfziffer 0: 550 ist gültig (Quersumme von 55 ist 10)
ergebnis = nummer_gueltig(550)
assert ergebnis is True, f"nummer_gueltig(550) ergibt {ergebnis!r}, erwartet war True (Quersumme 10, Prüfziffer 0)."

# Es wird nur mit Zahlen gerechnet, nicht mit Text
assert not verwendet("str"), "Ihr Code benutzt str(...). Zerlegen Sie die Zahl mit // und %, nicht als Text."

def mit_mitschrift(nummer):
    """Ruft nummer_gueltig(nummer) auf und merkt sich dabei, womit quersumme aufgerufen wird."""
    global quersumme
    echte_quersumme = quersumme
    aufrufe = []

    def mitschreiben(zahl):
        """Merkt sich den Aufruf und rechnet mit der Lösung weiter."""
        aufrufe.append(zahl)
        return echte_quersumme(zahl)

    quersumme = mitschreiben
    try:
        return nummer_gueltig(nummer), aufrufe
    finally:
        quersumme = echte_quersumme


# nummer_gueltig benutzt quersumme
ergebnis, aufrufe = mit_mitschrift(47124)
assert aufrufe[:1] == [4712], (
    f"nummer_gueltig(47124) soll quersumme(4712) aufrufen; aufgerufen wurde quersumme mit {aufrufe}."
)

# 2000 zufällige Zahlen und Nummern
zufall = Zufall(2039)
for runde in range(2000):
    zahl = zufall.randint(0, 10 ** zufall.randint(1, 18))
    ergebnis = quersumme(zahl)
    assert ergebnis == quersumme_vergleich(zahl), f"quersumme({zahl}) ergibt {ergebnis!r}, erwartet war {quersumme_vergleich(zahl)}."
    nummer = zufall.randint(10, 10 ** zufall.randint(2, 18))
    ergebnis = nummer_gueltig(nummer)
    assert ergebnis == gueltig_vergleich(nummer), f"nummer_gueltig({nummer}) ergibt {ergebnis!r}, erwartet war {gueltig_vergleich(nummer)}."

# Obere Grenze: 10**18 und die größte Zahl mit 18 Ziffern
ergebnisse = (quersumme(10**18), quersumme(10**18 - 1), nummer_gueltig(10**18), nummer_gueltig(10**18 - 7))
assert ergebnisse == (1, 162, False, True), (
    "quersumme(10**18), quersumme(10**18 - 1), nummer_gueltig(10**18), nummer_gueltig(10**18 - 7) "
    f"ergeben {ergebnisse!r}, erwartet war (1, 162, False, True)."
)
