# Automatisch erzeugt aus lehrkraft/muster/4_002_abfahrt.py - nicht von Hand ändern.
# vorlage-hash: 6a4311fbaa07c0f7
# text-hash: 46fef9198c236b1b
# thema: klassen
# inhalt: `__repr__` und `__str__`

# str zeigt die Zeile für die Anzeigetafel
abfahrt = Abfahrt("ICE 597", "München", 9, 5)
assert vergleichbar(str(abfahrt)) == vergleichbar("09:05 ICE 597 nach München") and "'" not in str(abfahrt), (
    f'str(Abfahrt("ICE 597", "München", 9, 5)) ergibt {str(abfahrt)!r}, erwartet war "09:05 ICE 597 nach München".\n'
    'Tipp: f"{self.stunde:02d}" schreibt die Stunde zweistellig.'
)

# str mit zweistelligen Zahlen und anderem Zug (nicht fest hinschreiben!)
abfahrt = Abfahrt("RE 4", "Aachen", 17, 42)
assert vergleichbar(str(abfahrt)) == vergleichbar("17:42 RE 4 nach Aachen"), (
    f'str(Abfahrt("RE 4", "Aachen", 17, 42)) ergibt {str(abfahrt)!r}, erwartet war "17:42 RE 4 nach Aachen".'
)

# repr zeigt einen Python-Ausdruck mit Anführungszeichen um die Texte
abfahrt = Abfahrt("ICE 597", "München", 9, 5)
assert repr(abfahrt) == "Abfahrt('ICE 597', 'München', 9, 5)", (
    f'repr(Abfahrt("ICE 597", "München", 9, 5)) ergibt {repr(abfahrt)!r}, '
    "erwartet war \"Abfahrt('ICE 597', 'München', 9, 5)\".\n"
    "Tipp: Texte in repr stehen in Anführungszeichen, Zahlen ohne führende Null."
)

# repr für einen anderen Zug
abfahrt = Abfahrt("S 1", "Dortmund", 0, 30)
assert repr(abfahrt) == "Abfahrt('S 1', 'Dortmund', 0, 30)", (
    f'repr(Abfahrt("S 1", "Dortmund", 0, 30)) ergibt {repr(abfahrt)!r}, erwartet war "Abfahrt(\'S 1\', \'Dortmund\', 0, 30)".'
)

# repr stimmt auch, wenn das Ziel einen Apostroph enthält
abfahrt = Abfahrt("R 9", "L'Aquila", 6, 0)
assert repr(abfahrt) == "Abfahrt('R 9', \"L'Aquila\", 6, 0)", (
    f"repr(Abfahrt('R 9', \"L'Aquila\", 6, 0)) ergibt\n    {repr(abfahrt)}\n"
    "erwartet war\n    Abfahrt('R 9', \"L'Aquila\", 6, 0)\n"
    "Tipp: Schreiben Sie {self.ziel!r} statt '{self.ziel}', dann wählt Python passende Anführungszeichen; "
    "die Zahlen stehen in repr ohne führende Null."
)

# Listen zeigen ihre Elemente mit repr
tafel = [Abfahrt("RE 4", "Aachen", 17, 42), Abfahrt("S 1", "Dortmund", 0, 30)]
assert str(tafel) == "[Abfahrt('RE 4', 'Aachen', 17, 42), Abfahrt('S 1', 'Dortmund', 0, 30)]", (
    f"str() einer Liste mit zwei Abfahrten ergibt {str(tafel)!r}, "
    "erwartet war \"[Abfahrt('RE 4', 'Aachen', 17, 42), Abfahrt('S 1', 'Dortmund', 0, 30)]\".\n"
    "Tipp: Listen benutzen für ihre Elemente __repr__, nicht __str__."
)

# Die Ränder der Uhrzeit: 00:00 und 23:59
erste, letzte = Abfahrt("N 1", "Köln", 0, 0), Abfahrt("N 2", "Bonn", 23, 59)
assert (vergleichbar(str(erste)), vergleichbar(str(letzte))) == (vergleichbar("00:00 N 1 nach Köln"), vergleichbar("23:59 N 2 nach Bonn")), (
    f'Erwartet "00:00 N 1 nach Köln" und "23:59 N 2 nach Bonn", bekommen {str(erste)!r} und {str(letzte)!r}.'
)

# Viele zufällige Abfahrten, auch mit ' und " im Namen
zufall = Zufall(4002)
zeichen = "abcXYZäöü 0123'\"-"
fehlerfall = None
for versuch in range(500):
    zug = "".join(zufall.choice(zeichen) for _ in range(zufall.randint(1, 8)))
    ziel = "".join(zufall.choice(zeichen) for _ in range(zufall.randint(1, 8)))
    stunde, minute = zufall.randint(0, 23), zufall.randint(0, 59)
    abfahrt = Abfahrt(zug, ziel, stunde, minute)
    erwartet_str = str(stunde).zfill(2) + ":" + str(minute).zfill(2) + " " + zug + " nach " + ziel
    erwartet_repr = "Abfahrt(%r, %r, %d, %d)" % (zug, ziel, stunde, minute)
    if vergleichbar(str(abfahrt)) != vergleichbar(erwartet_str):
        fehlerfall = f"str(Abfahrt({zug!r}, {ziel!r}, {stunde}, {minute})) ergibt\n    {str(abfahrt)}\nerwartet war\n    {erwartet_str}"
        break
    if repr(abfahrt) != erwartet_repr:
        fehlerfall = f"repr(Abfahrt({zug!r}, {ziel!r}, {stunde}, {minute})) ergibt\n    {repr(abfahrt)}\nerwartet war\n    {erwartet_repr}"
        break
assert fehlerfall is None, fehlerfall

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("09:05 ICE 597 nach München\n[Abfahrt('ICE 597', 'München', 9, 5)]"), (
    f"Erwartete Ausgabe:\n09:05 ICE 597 nach München\n[Abfahrt('ICE 597', 'München', 9, 5)]\nIhr Programm:\n{AUSGABE}"
)
