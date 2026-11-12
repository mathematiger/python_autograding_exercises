# Automatisch erzeugt aus lehrkraft/muster/2_037_kundennummer.py - nicht von Hand ändern.
# vorlage-hash: b00f7181ddea1b71
# text-hash: 1c69ef556eb1a9b2
# thema: algorithmen
# inhalt: Ziffern mit // und %

def quersumme_mit_text(zahl):
    """Vergleichslösung über den Text der Zahl."""
    return sum(int(zeichen) for zeichen in str(zahl))


def gueltig_mit_text(nummer):
    """Vergleichslösung über den Text der Nummer."""
    text = str(nummer)
    return quersumme_mit_text(int(text[:-1])) % 10 == int(text[-1])


# Das Beispiel aus der Aufgabe
assert quersumme(48153) == 21, f"quersumme(48153) ergibt {quersumme(48153)!r}, erwartet war 21 (4 + 8 + 1 + 5 + 3)."

# Andere Zahlen (nicht fest hinschreiben!)
for zahl, erwartet in [(999, 27), (1004, 5), (123456789, 45)]:
    ergebnis = quersumme(zahl)
    assert ergebnis == erwartet, f"quersumme({zahl}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Einstellige Zahlen und 0
for zahl in [7, 1, 0]:
    ergebnis = quersumme(zahl)
    assert ergebnis == zahl, f"quersumme({zahl}) ergibt {ergebnis!r}, erwartet war {zahl}."

# Nullen in der Zahl, auch am Ende
for zahl, erwartet in [(10, 1), (100500, 6), (10**18, 1)]:
    ergebnis = quersumme(zahl)
    assert ergebnis == erwartet, (
        f"quersumme({zahl}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Die Schleife soll laufen, solange zahl > 0 ist, nicht solange die letzte Ziffer nicht 0 ist."
    )

# quersumme liefert eine ganze Zahl
assert type(quersumme(48153)) is int, (
    f"quersumme(48153) ergibt {quersumme(48153)!r} vom Typ {type(quersumme(48153)).__name__}, erwartet war die ganze Zahl 21.\n"
    "Tipp: Mit // statt / bleibt die Zahl ganz."
)

# Die Beispiele zu ist_gueltig
for nummer, erwartet in [(48158, True), (48153, False)]:
    ergebnis = ist_gueltig(nummer)
    assert ergebnis is erwartet, f"ist_gueltig({nummer}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Zweistellige Nummern: die Prüfziffer ist die erste Ziffer
for nummer, erwartet in [(10, False), (11, True), (99, True), (98, False)]:
    ergebnis = ist_gueltig(nummer)
    assert ergebnis is erwartet, f"ist_gueltig({nummer}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ist die Quersumme zweistellig, zählt nur ihre letzte Stelle
for nummer, erwartet in [(99999993, True), (999999963, False), (1900, True)]:
    ergebnis = ist_gueltig(nummer)
    assert ergebnis is erwartet, (
        f"ist_gueltig({nummer}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Die Prüfziffer ist die Quersumme der übrigen Ziffern % 10."
    )

# Die letzte Ziffer zählt nicht zur Quersumme
assert ist_gueltig(110) is False and ist_gueltig(112) is True, (
    f"ist_gueltig(110) ergibt {ist_gueltig(110)!r} und ist_gueltig(112) ergibt {ist_gueltig(112)!r}, "
    "erwartet waren False und True.\n"
    "Tipp: Bilden Sie die Quersumme von nummer // 10, also ohne die letzte Ziffer."
)

# Gerechnet wird ohne str(...)
assert not verwendet("str"), "Ihr Code benutzt str(...). Zerlegen Sie die Zahl mit // und % in ihre Ziffern."

# 500 zufällige Zahlen gegen eine Vergleichslösung über den Text
zufall = Zufall(2037)
for _ in range(500):
    zahl = zufall.randint(0, 10 ** zufall.randint(1, 18))
    ergebnis = quersumme(zahl)
    assert ergebnis == quersumme_mit_text(zahl), (
        f"quersumme({zahl}) ergibt {ergebnis!r}, erwartet war {quersumme_mit_text(zahl)}."
    )

# 500 zufällige Kundennummern, etwa jede zweite gültig
for _ in range(500):
    vorne = zufall.randint(1, 10**11 - 1)
    if zufall.random() < 0.5:
        nummer = vorne * 10 + quersumme_mit_text(vorne) % 10
    else:
        nummer = vorne * 10 + zufall.randint(0, 9)
    ergebnis = ist_gueltig(nummer)
    assert ergebnis is gueltig_mit_text(nummer), (
        f"ist_gueltig({nummer}) ergibt {ergebnis!r}, erwartet war {gueltig_mit_text(nummer)}."
    )

# Obere Grenze: die größte Nummer und große gültige Nummern
for nummer in [10**12, 999999999992, 999999999999]:
    ergebnis = ist_gueltig(nummer)
    assert ergebnis is gueltig_mit_text(nummer), (
        f"ist_gueltig({nummer}) ergibt {ergebnis!r}, erwartet war {gueltig_mit_text(nummer)}."
    )

# Die Ausgabe des Programms stimmt
assert AUSGABE == "21\nTrue", f"Erwartete Ausgabe:\n21\nTrue\nIhr Programm gibt aus:\n{AUSGABE}"
