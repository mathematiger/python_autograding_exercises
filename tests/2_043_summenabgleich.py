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
    """Baut die Fehlermeldung für einen Aufruf, bei None mit Tipp zum fehlenden return."""
    text = f"summe_passt({beschreibe(positionen)}, {gesamt!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    if ergebnis is None:
        text += "\nTipp: Ihre Funktion gibt None zurück; fehlt ein return für den Fall False?"
    return text


def tipp_abs(ergebnis):
    """Gibt den Tipp zu abs(...) zurück, wenn ein zu großer Gesamtbetrag fälschlich passt, sonst einen leeren Text."""
    if ergebnis is not True:
        return ""
    return (
        "\nTipp: Die Summe ist hier kleiner als der Gesamtbetrag, der Unterschied also negativ. "
        "abs(...) macht daraus den Abstand."
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
assert ergebnis == False, meldung([10.0, 5.5], 15.6, ergebnis, False) + tipp_abs(ergebnis)

# Gesamtbetrag einen Cent zu klein
ergebnis = summe_passt([0.1, 0.2], 0.29)
assert ergebnis == False, meldung([0.1, 0.2], 0.29, ergebnis, False)

# Gesamtbetrag einen Cent zu groß
ergebnis = summe_passt([0.1, 0.2], 0.31)
assert ergebnis == False, meldung([0.1, 0.2], 0.31, ergebnis, False) + tipp_abs(ergebnis)

# Ganze Zahlen funktionieren genauso
ergebnis = summe_passt([3, 4, 5], 12)
assert ergebnis == True, meldung([3, 4, 5], 12, ergebnis, True)

# Keine Positionen und Gesamtbetrag 0
ergebnis = summe_passt([], 0)
assert ergebnis == True, meldung([], 0, ergebnis, True)

# Keine Positionen, aber ein Gesamtbetrag
ergebnis = summe_passt([], 0.01)
assert ergebnis == False, meldung([], 0.01, ergebnis, False) + tipp_abs(ergebnis)

# Eine einzige Position
ergebnis = summe_passt([0.07], 0.07)
assert ergebnis == True, meldung([0.07], 0.07, ergebnis, True)

# Zehnmal 0.1 sind 1.0 (mit == wäre das False)
ergebnis = summe_passt([0.1] * 10, 1.0)
assert ergebnis == True, meldung([0.1] * 10, 1.0, ergebnis, True)

# Viele zufällige Bestellungen: in Cent gerechnet, damit die Vergleichslösung exakt ist
zufall = Zufall(2043)
for runde in range(400):
    anzahl = zufall.randint(0, 12)
    # Höchstpreis so, dass auch Summe plus Abweichung höchstens 100 000 Euro (10 000 000 Cent) ist
    hoechstpreis = zufall.choice([100, 10000, 9999500 // max(anzahl, 1)])
    cent = [zufall.randint(0, hoechstpreis) for _ in range(anzahl)]
    abweichung = zufall.choice([0, 0, 1, -1, zufall.randint(-500, 500)])
    gesamt_cent = max(0, sum(cent) + abweichung)
    positionen = [wert / 100 for wert in cent]
    gesamt = gesamt_cent / 100
    erwartet = gesamt_cent == sum(cent)
    ergebnis = summe_passt(positionen, gesamt)
    assert ergebnis == erwartet, meldung(positionen, gesamt, ergebnis, erwartet)

# Obere Grenze: 10 000 Positionen zu je höchstens 10 Euro (zusammen höchstens 100 000 Euro)
cent = [zufall.randint(0, 1000) for _ in range(10000)]
positionen = [wert / 100 for wert in cent]
for abweichung, erwartet in [(0, True), (1, False), (-1, False)]:
    gesamt = (sum(cent) + abweichung) / 100
    ergebnis = summe_passt(positionen, gesamt)
    assert ergebnis == erwartet, meldung(positionen, gesamt, ergebnis, erwartet)
