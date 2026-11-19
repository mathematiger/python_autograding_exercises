# Automatisch erzeugt aus lehrkraft/muster/2_043_summenabgleich.py - nicht von Hand ändern.
# vorlage-hash: 841b0e8ed9c52919
# text-hash: 11b1647adc46f5da
# thema: texte_zahlen
# inhalt: Kommazahlen vergleichen

def beschreibe(positionen):
    """Kürzt lange Listen für Fehlermeldungen."""
    if len(positionen) <= 8:
        return repr(positionen)
    return f"[{positionen[0]!r}, {positionen[1]!r}, … {len(positionen)} Preise]"


def meldung(positionen, gesamt, ergebnis, erwartet):
    """Baut die Fehlermeldung für einen Aufruf."""
    return (
        f"summe_passt({beschreibe(positionen)}, {gesamt!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    )


# Das Beispiel 0.1 + 0.2 und 0.3 passt
ergebnis = summe_passt([0.1, 0.2], 0.3)
assert ergebnis == True, (
    meldung([0.1, 0.2], 0.3, ergebnis, True)
    + "\nTipp: 0.1 + 0.2 ergibt 0.30000000000000004. Vergleichen Sie nicht mit ==, "
    "sondern prüfen Sie abs(summe - gesamt) < TOLERANZ."
)

# Ein zweites passendes Beispiel
ergebnis = summe_passt([19.99, 5.01], 25.0)
assert ergebnis == True, meldung([19.99, 5.01], 25.0, ergebnis, True)

# Eine falsche Summe passt nicht (nicht immer True zurückgeben!)
ergebnis = summe_passt([10.0, 5.5], 15.6)
assert ergebnis == False, meldung([10.0, 5.5], 15.6, ergebnis, False)

# Gesamtbetrag einen Cent zu klein
ergebnis = summe_passt([0.1, 0.2], 0.29)
assert ergebnis == False, meldung([0.1, 0.2], 0.29, ergebnis, False)

# Gesamtbetrag einen Cent zu groß
ergebnis = summe_passt([0.1, 0.2], 0.31)
assert ergebnis == False, (
    meldung([0.1, 0.2], 0.31, ergebnis, False)
    + "\nTipp: Die Summe ist hier kleiner als der Gesamtbetrag, der Unterschied also negativ. "
    "abs(...) macht daraus den Abstand 0.01."
)

# Ganze Zahlen funktionieren genauso
ergebnis = summe_passt([3, 4, 5], 12)
assert ergebnis == True, meldung([3, 4, 5], 12, ergebnis, True)

# Keine Positionen und Gesamtbetrag 0
ergebnis = summe_passt([], 0)
assert ergebnis == True, meldung([], 0, ergebnis, True)

# Keine Positionen, aber ein Gesamtbetrag
ergebnis = summe_passt([], 0.01)
assert ergebnis == False, meldung([], 0.01, ergebnis, False)

# Eine einzige Position
ergebnis = summe_passt([0.07], 0.07)
assert ergebnis == True, meldung([0.07], 0.07, ergebnis, True)

# Zehnmal 0.1 sind 1.0 (mit == wäre das False)
ergebnis = summe_passt([0.1] * 10, 1.0)
assert ergebnis == True, meldung([0.1] * 10, 1.0, ergebnis, True)

# Viele zufällige Bestellungen: in Cent gerechnet, damit die Vergleichslösung exakt ist
zufall = Zufall(2043)
for runde in range(400):
    cent = [zufall.randint(0, zufall.choice([100, 10000, 10000000])) for _ in range(zufall.randint(0, 12))]
    abweichung = zufall.choice([0, 0, 1, -1, zufall.randint(-500, 500)])
    gesamt_cent = max(0, sum(cent) + abweichung)
    positionen = [wert / 100 for wert in cent]
    gesamt = gesamt_cent / 100
    erwartet = gesamt_cent == sum(cent)
    ergebnis = summe_passt(positionen, gesamt)
    assert ergebnis == erwartet, meldung(positionen, gesamt, ergebnis, erwartet)

# Obere Grenze: 10 000 Positionen mit großen Preisen
cent = [zufall.randint(9000000, 10000000) for _ in range(10000)]
positionen = [wert / 100 for wert in cent]
for abweichung, erwartet in [(0, True), (1, False), (-1, False)]:
    gesamt = (sum(cent) + abweichung) / 100
    ergebnis = summe_passt(positionen, gesamt)
    assert ergebnis == erwartet, meldung(positionen, gesamt, ergebnis, erwartet)
