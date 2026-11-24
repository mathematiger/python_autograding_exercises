# Automatisch erzeugt aus lehrkraft/muster/5_055_rechnungsmaske.py - nicht von Hand ändern.
# vorlage-hash: c20690ed5c9ef440
# text-hash: 8e178b58a9c095ff
# thema: texte_zahlen
# inhalt: decimal für Geldbeträge

from decimal import ROUND_HALF_UP, Decimal


def wert_von(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, fehler


def ausnahme(fehler):
    """Beschreibt eine gefangene Ausnahme für eine Meldung."""
    return f"{type(fehler).__name__}: {fehler}" if fehler is not None else "keine Ausnahme"


def kaufmaennisch_von_hand(betrag):
    """Vergleichslösung: kaufmännisch runden über die Ziffern, ohne quantize."""
    zeichen, ziffern, exponent = abs(betrag).as_tuple()
    zahl = int("".join(str(ziffer) for ziffer in ziffern) or "0")
    # zahl · 10**exponent ist der Betrag; in halben Cent: zahl · 10**exponent · 200
    if exponent >= -2:
        cent = zahl * 10 ** (exponent + 2)
    else:
        teiler = 10 ** (-exponent - 2)
        cent, rest = divmod(zahl, teiler)
        if 2 * rest >= teiler:
            cent += 1
    ergebnis = Decimal(cent) / 100
    return -ergebnis if betrag < 0 else ergebnis


def ist_decimal_tripel(ergebnis):
    """True, wenn ergebnis ein Tupel aus drei Decimal ist."""
    return isinstance(ergebnis, tuple) and len(ergebnis) == 3 and all(isinstance(teil, Decimal) for teil in ergebnis)


def summe_von_hand(positionen, prozent):
    """Vergleichslösung: rechnet in ganzen Cent mit int."""
    netto_cent = 0
    for menge, einzelpreis in positionen:
        netto_cent += menge * int(einzelpreis * 100)
    steuer_cent, rest = divmod(netto_cent * prozent, 100)
    if 2 * rest >= 100:
        steuer_cent += 1
    return Decimal(netto_cent) / 100, Decimal(steuer_cent) / 100, Decimal(netto_cent + steuer_cent) / 100


def meldung_summe(positionen, prozent, ergebnis, fehler):
    """Baut die Meldung für rechnungssumme."""
    erwartet = summe_von_hand(positionen, prozent)
    gezeigt = positionen if len(positionen) <= 6 else f"<{len(positionen)} Positionen>"
    return (
        f"rechnungssumme({gezeigt}, {prozent}) ergibt {ergebnis!r} ({ausnahme(fehler)}),\n"
        f"erwartet war {erwartet!r}."
    )


# lies_betrag: das Beispiel mit Komma
ergebnis, fehler = wert_von(lies_betrag, "12,5")
assert ergebnis == Decimal("12.5"), (
    f"lies_betrag('12,5') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war Decimal('12.5').\n"
    'Tipp: Ersetzen Sie "," durch "." und geben Sie den Text an Decimal.'
)

# lies_betrag gibt einen Decimal zurück, keinen float
ergebnis, fehler = wert_von(lies_betrag, "12,5")
assert isinstance(ergebnis, Decimal), (
    f"lies_betrag('12,5') ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war ein Decimal."
)

# lies_betrag: der Wert kommt genau aus dem Text, nicht über float
ergebnis, fehler = wert_von(lies_betrag, "0,10")
assert isinstance(ergebnis, Decimal) and sum([ergebnis] * 10) == 1, (
    f"lies_betrag('0,10') ergibt {ergebnis!r} ({ausnahme(fehler)}); zehnmal addiert soll genau 1 herauskommen.\n"
    "Tipp: Decimal(float(text)) übernimmt den Fehler des float; geben Sie den Text direkt an Decimal."
)

# lies_betrag: Punkt und Leerzeichen am Rand (nicht fest hinschreiben!)
ergebnis, fehler = wert_von(lies_betrag, " 1.50 ")
assert ergebnis == Decimal("1.5"), f"lies_betrag(' 1.50 ') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war Decimal('1.50')."

# lies_betrag: ganze Euro und null Euro
for eingabe, erwartet in [("7", Decimal(7)), ("0", Decimal(0)), ("999999,99", Decimal("999999.99"))]:
    ergebnis, fehler = wert_von(lies_betrag, eingabe)
    assert ergebnis == erwartet and isinstance(ergebnis, Decimal), (
        f"lies_betrag({eingabe!r}) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war {erwartet!r}."
    )

# lies_betrag: unlesbare Eingabe ist ein ValueError (InvalidOperation ist keiner)
ergebnis, fehler = wert_von(lies_betrag, "12,50 €")
assert isinstance(fehler, ValueError), (
    f"lies_betrag('12,50 €') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError.\n"
    "Tipp: Decimal löst decimal.InvalidOperation aus; fangen Sie sie ab und lösen Sie einen ValueError aus."
)

# lies_betrag: Tausenderpunkt und Komma zusammen sind nicht lesbar
ergebnis, fehler = wert_von(lies_betrag, "1.234,50")
assert isinstance(fehler, ValueError), f"lies_betrag('1.234,50') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError."

# lies_betrag: leeres Feld
ergebnis, fehler = wert_von(lies_betrag, "   ")
assert isinstance(fehler, ValueError), f"lies_betrag('   ') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError."

# lies_betrag: "nan" ist keine endliche Zahl
ergebnis, fehler = wert_von(lies_betrag, "nan")
assert isinstance(fehler, ValueError), (
    f"lies_betrag('nan') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError.\n"
    "Tipp: Decimal liest 'nan' als NaN; betrag.is_finite() ist dann False."
)

# lies_betrag: "Infinity" ist keine endliche Zahl
ergebnis, fehler = wert_von(lies_betrag, "Infinity")
assert isinstance(fehler, ValueError), f"lies_betrag('Infinity') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError."

# lies_betrag: negativer Betrag
ergebnis, fehler = wert_von(lies_betrag, "-3,00")
assert isinstance(fehler, ValueError), f"lies_betrag('-3,00') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError."

# lies_betrag: ein halber Cent geht nicht auf ganze Cent auf
ergebnis, fehler = wert_von(lies_betrag, "0,005")
assert isinstance(fehler, ValueError), (
    f"lies_betrag('0,005') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError.\n"
    "Tipp: betrag == betrag.quantize(Decimal('0.01')) ist genau dann wahr, wenn er auf ganze Cent aufgeht."
)

# lies_betrag: drei Nachkommastellen
ergebnis, fehler = wert_von(lies_betrag, "12,345")
assert isinstance(fehler, ValueError), f"lies_betrag('12,345') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError."

# lies_betrag: Nullen hinter den Cent sind erlaubt
ergebnis, fehler = wert_von(lies_betrag, "1,500")
assert ergebnis == Decimal("1.5") and fehler is None, (
    f"lies_betrag('1,500') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war Decimal('1.500') bzw. "
    "Decimal('1.5'): 1,500 geht auf ganze Cent auf.\nTipp: Zählen Sie nicht die Nachkommastellen, sondern prüfen Sie "
    "betrag == betrag.quantize(Decimal('0.01'))."
)

# kaufmaennisch: das Beispiel, ein halber Cent wird aufgerundet
ergebnis, fehler = wert_von(kaufmaennisch, Decimal("0.285"))
assert ergebnis == Decimal("0.29"), (
    f"kaufmaennisch(Decimal('0.285')) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war Decimal('0.29').\n"
    "Tipp: quantize(Decimal('0.01'), rounding=ROUND_HALF_UP); ohne rounding und mit round gehen Hälften zur "
    "geraden Ziffer."
)

# kaufmaennisch gibt einen Decimal zurück
ergebnis, fehler = wert_von(kaufmaennisch, Decimal("2.675"))
assert isinstance(ergebnis, Decimal), (
    f"kaufmaennisch(Decimal('2.675')) ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war ein Decimal."
)

# kaufmaennisch: andere Hälften (nicht fest hinschreiben!)
for betrag, erwartet in [("2.675", "2.68"), ("0.125", "0.13"), ("0.135", "0.14"), ("1000000000.005", "1000000000.01")]:
    ergebnis, fehler = wert_von(kaufmaennisch, Decimal(betrag))
    assert ergebnis == Decimal(erwartet), (
        f"kaufmaennisch(Decimal('{betrag}')) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war Decimal('{erwartet}')."
    )

# kaufmaennisch: knapp unter einem halben Cent wird abgerundet
ergebnis, fehler = wert_von(kaufmaennisch, Decimal("0.28499999999999999999"))
assert ergebnis == Decimal("0.28"), (
    f"kaufmaennisch(Decimal('0.28499999999999999999')) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war 0.28.\n"
    "Tipp: Runden Sie in einem Schritt auf Cent, nicht erst auf Zehntelcent."
)

# kaufmaennisch: ganze Cent bleiben
ergebnis, fehler = wert_von(kaufmaennisch, Decimal("4"))
assert ergebnis == 4, (
    f"kaufmaennisch(Decimal('4')) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war Decimal('4.00')."
)

# kaufmaennisch: negative Beträge, Hälften vom Betrag her aufgerundet
ergebnis, fehler = wert_von(kaufmaennisch, Decimal("-0.285"))
assert ergebnis == Decimal("-0.29"), (
    f"kaufmaennisch(Decimal('-0.285')) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war Decimal('-0.29').\n"
    "Tipp: ROUND_HALF_UP rundet Hälften von der Null weg; ROUND_CEILING würde -0.28 ergeben."
)

# kaufmaennisch: null
ergebnis, fehler = wert_von(kaufmaennisch, Decimal("0.004"))
assert ergebnis == 0, f"kaufmaennisch(Decimal('0.004')) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war Decimal('0.00')."

# rechnungssumme: das erste Beispiel
positionen = [(3, Decimal("19.99")), (1, Decimal("1.50"))]
ergebnis, fehler = wert_von(rechnungssumme, positionen, 19)
assert ergebnis == summe_von_hand(positionen, 19), meldung_summe(positionen, 19, ergebnis, fehler)

# rechnungssumme: die Steuer genau ein halber Cent über 0,28
positionen = [(1, Decimal("1.50"))]
ergebnis, fehler = wert_von(rechnungssumme, positionen, 19)
assert ergebnis == summe_von_hand(positionen, 19), (
    meldung_summe(positionen, 19, ergebnis, fehler) + "\nTipp: Runden Sie die Steuer mit kaufmaennisch."
)

# rechnungssumme gibt drei Decimal zurück
ergebnis, fehler = wert_von(rechnungssumme, [(2, Decimal("0.10"))], 7)
assert ist_decimal_tripel(ergebnis), (
    f"rechnungssumme([(2, Decimal('0.10'))], 7) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein Tupel aus "
    "drei Decimal."
)

# rechnungssumme: andere Positionen und 7 % (nicht fest hinschreiben!)
positionen = [(10, Decimal("0.10")), (7, Decimal("12.35")), (1, Decimal("89.00"))]
ergebnis, fehler = wert_von(rechnungssumme, positionen, 7)
assert ergebnis == summe_von_hand(positionen, 7), meldung_summe(positionen, 7, ergebnis, fehler)

# rechnungssumme: netto wird nicht gerundet, die Steuer schon
positionen = [(1, Decimal("0.05"))]
ergebnis, fehler = wert_von(rechnungssumme, positionen, 19)
assert ergebnis == summe_von_hand(positionen, 19), (
    meldung_summe(positionen, 19, ergebnis, fehler) + "\nTipp: 0,05 · 19 % sind 0,0095 €, gerundet 0,01 €."
)

# rechnungssumme: Steuersatz 0
positionen = [(2, Decimal("49.99"))]
ergebnis, fehler = wert_von(rechnungssumme, positionen, 0)
assert ergebnis == summe_von_hand(positionen, 0), meldung_summe(positionen, 0, ergebnis, fehler)

# rechnungssumme: keine Positionen ergibt drei Decimal mit Wert 0
ergebnis, fehler = wert_von(rechnungssumme, [], 19)
assert ist_decimal_tripel(ergebnis) and ergebnis == (0, 0, 0), (
    f"rechnungssumme([], 19) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet waren drei Decimal mit Wert 0.\n"
    "Tipp: sum([]) ist die ganze Zahl 0; beginnen Sie mit Decimal(0) oder sum(..., Decimal(0))."
)

# lies_betrag: 300 zufällige Eingaben in Cent
zufall = Zufall(5055)
for _ in range(300):
    cent = zufall.randint(0, 10**8)
    euro, rest = divmod(cent, 100)
    trenner = zufall.choice([",", "."])
    eingabe = zufall.choice(["", " "]) + f"{euro}{trenner}{rest:02d}" + zufall.choice(["", "  "])
    ergebnis, fehler = wert_von(lies_betrag, eingabe)
    assert ergebnis == Decimal(cent) / 100 and isinstance(ergebnis, Decimal), (
        f"lies_betrag({eingabe!r}) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war {Decimal(cent) / 100!r}."
    )

# kaufmaennisch: 300 zufällige Beträge mit bis zu 20 Nachkommastellen
for _ in range(300):
    stellen = zufall.randint(0, 20)
    betrag = Decimal(zufall.randint(-(10**9) * 10**stellen, 10**9 * 10**stellen)).scaleb(-stellen)
    if zufall.random() < 0.3:
        betrag = Decimal(zufall.randint(-(10**7), 10**7) * 10 + 5).scaleb(-3)
    ergebnis, fehler = wert_von(kaufmaennisch, betrag)
    erwartet = kaufmaennisch_von_hand(betrag)
    assert ergebnis == erwartet, f"kaufmaennisch(Decimal('{betrag}')) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war {erwartet!r}."

# rechnungssumme: 300 zufällige Rechnungen
for _ in range(300):
    positionen = [
        (zufall.randint(1, 1000), Decimal(zufall.randint(0, 10**8)) / 100) for _ in range(zufall.randint(0, 6))
    ]
    prozent = zufall.choice([0, 7, 19, zufall.randint(0, 100)])
    ergebnis, fehler = wert_von(rechnungssumme, positionen, prozent)
    assert ergebnis == summe_von_hand(positionen, prozent), meldung_summe(positionen, prozent, ergebnis, fehler)

# Obere Grenze: 10 000 Positionen mit je 0,10 €
positionen = [(1, Decimal("0.10"))] * 9999 + [(1000, Decimal("1000000"))]
ergebnis, fehler = wert_von(rechnungssumme, positionen, 19)
assert ergebnis == summe_von_hand(positionen, 19), (
    meldung_summe(positionen, 19, ergebnis, fehler) + "\nTipp: Mit float wird die Summe vieler 0,10 € ungenau."
)
