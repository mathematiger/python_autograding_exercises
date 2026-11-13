# Automatisch erzeugt aus lehrkraft/muster/2_039_inventarnummer.py - nicht von Hand ändern.
# vorlage-hash: ff07384409a5059c
# text-hash: 8e1e28f82e436880
# thema: algorithmen
# inhalt: Ziffern mit // und %

def langsame_quersumme(zahl):
    """Vergleichslösung über den Text der Zahl, anders als der verlangte Weg."""
    return sum(int(ziffer) for ziffer in f"{zahl}")


def langsam_stimmt(nummer):
    """Vergleichslösung: Prüfziffer über den Text der Zahl."""
    text = f"{nummer}"
    return int(text[-1]) == langsame_quersumme(int(text[:-1])) % 10


# Das Beispiel aus der Aufgabe: quersumme(4711) ist 13
assert quersumme(4711) == 13, f"quersumme(4711) ergibt {quersumme(4711)!r}, erwartet war 13 (4 + 7 + 1 + 1)."

# Eine andere Zahl (nicht fest hinschreiben!)
assert quersumme(2025) == 9, f"quersumme(2025) ergibt {quersumme(2025)!r}, erwartet war 9 (2 + 0 + 2 + 5)."

# Eine einstellige Zahl ist ihre eigene Quersumme
assert quersumme(7) == 7, f"quersumme(7) ergibt {quersumme(7)!r}, erwartet war 7."

# Nullen in der Zahl zählen nicht mit, auch nicht am Ende
assert quersumme(1000) == 1 and quersumme(9090) == 18, (
    f"quersumme(1000) ergibt {quersumme(1000)!r} und quersumme(9090) {quersumme(9090)!r}, erwartet waren 1 und 18.\n"
    "Tipp: Wiederholen Sie, solange zahl > 0 ist, nicht nur solange die letzte Ziffer nicht 0 ist."
)

# Die Quersumme von 0 ist 0
assert quersumme(0) == 0, f"quersumme(0) ergibt {quersumme(0)!r}, erwartet war 0."

# Das Beispiel aus der Aufgabe: 47113 stimmt
assert pruefziffer_stimmt(47113) is True, (
    f"pruefziffer_stimmt(47113) ergibt {pruefziffer_stimmt(47113)!r}, erwartet war True "
    "(Quersumme von 4711 ist 13, letzte Ziffer 3)."
)

# Das Beispiel aus der Aufgabe: 47118 stimmt nicht
assert pruefziffer_stimmt(47118) is False, (
    f"pruefziffer_stimmt(47118) ergibt {pruefziffer_stimmt(47118)!r}, erwartet war False (die Prüfziffer wäre 3)."
)

# Nur die letzte Ziffer der Quersumme ist die Prüfziffer: 99 hat Quersumme 18, also passt 998
assert pruefziffer_stimmt(998) is True and pruefziffer_stimmt(9918) is False, (
    f"pruefziffer_stimmt(998) ergibt {pruefziffer_stimmt(998)!r}, pruefziffer_stimmt(9918) {pruefziffer_stimmt(9918)!r}; "
    "erwartet waren True und False.\nTipp: Die Prüfziffer ist quersumme(...) % 10, nicht die ganze Quersumme."
)

# Die Prüfziffer selbst zählt nicht zur Quersumme
assert pruefziffer_stimmt(123) is True and pruefziffer_stimmt(336) is True, (
    f"pruefziffer_stimmt(123) ergibt {pruefziffer_stimmt(123)!r}, pruefziffer_stimmt(336) {pruefziffer_stimmt(336)!r}; "
    "erwartet war beide Male True.\nTipp: Bilden Sie die Quersumme von nummer // 10, also ohne die letzte Ziffer."
)

# Kleinste Nummern: 10 stimmt nicht (Prüfziffer wäre 1), 11 stimmt
assert pruefziffer_stimmt(10) is False and pruefziffer_stimmt(11) is True, (
    f"pruefziffer_stimmt(10) ergibt {pruefziffer_stimmt(10)!r}, pruefziffer_stimmt(11) {pruefziffer_stimmt(11)!r}; "
    "erwartet waren False und True."
)

# Prüfziffer 0: 4006 hat Quersumme 10 bei 4 + 0 + 0 + 6, also passt 40060
assert pruefziffer_stimmt(40060) is True and pruefziffer_stimmt(40061) is False, (
    f"pruefziffer_stimmt(40060) ergibt {pruefziffer_stimmt(40060)!r}, pruefziffer_stimmt(40061) "
    f"{pruefziffer_stimmt(40061)!r}; erwartet waren True und False."
)

# Ohne str(...): nur mit // und % rechnen
assert not verwendet("str"), "Rechnen Sie die Ziffern mit // und % aus, ohne str(...)."

# Viele zufällige Zahlen
zufall = Zufall(2039)
for _ in range(2000):
    zahl = zufall.randint(0, 10 ** zufall.randint(1, 18))
    assert quersumme(zahl) == langsame_quersumme(zahl), (
        f"quersumme({zahl}) ergibt {quersumme(zahl)!r}, erwartet war {langsame_quersumme(zahl)}."
    )

# Viele zufällige Inventarnummern, etwa die Hälfte mit richtiger Prüfziffer
zufall = Zufall(20391)
for _ in range(2000):
    vorne = zufall.randint(1, 10**17 - 1)
    if zufall.random() < 0.5:
        nummer = vorne * 10 + langsame_quersumme(vorne) % 10
    else:
        nummer = vorne * 10 + zufall.randint(0, 9)
    assert pruefziffer_stimmt(nummer) == langsam_stimmt(nummer), (
        f"pruefziffer_stimmt({nummer}) ergibt {pruefziffer_stimmt(nummer)!r}, erwartet war {langsam_stimmt(nummer)}."
    )

# Obere Grenze: 10**18 und die größte Zahl mit 18 Ziffern
assert quersumme(10**18) == 1 and quersumme(10**18 - 1) == 162, (
    f"quersumme(10**18) ergibt {quersumme(10**18)!r}, quersumme(10**18 - 1) {quersumme(10**18 - 1)!r}; "
    "erwartet waren 1 und 162."
)

# Obere Grenze bei der Prüfziffer
assert pruefziffer_stimmt(10**18) is False and pruefziffer_stimmt(10**18 - 7) is True, (
    f"pruefziffer_stimmt(10**18) ergibt {pruefziffer_stimmt(10**18)!r}, pruefziffer_stimmt({10**18 - 7}) "
    f"{pruefziffer_stimmt(10**18 - 7)!r}; erwartet waren False und True."
)
