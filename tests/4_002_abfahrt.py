# Automatisch erzeugt aus lehrkraft/muster/4_002_abfahrt.py - nicht von Hand ändern.
# vorlage-hash: 117755691001da34
# thema: klassen
# inhalt: `__repr__` und `__str__`

# str zeigt die Zeile für die Anzeigetafel
abfahrt = Abfahrt("ICE 597", "München", 9, 5)
assert str(abfahrt) == "09:05 ICE 597 nach München", (
    f'str(Abfahrt("ICE 597", "München", 9, 5)) ergibt {str(abfahrt)!r}, erwartet war "09:05 ICE 597 nach München".\n'
    'Tipp: f"{self.stunde:02d}" schreibt die Stunde zweistellig.'
)

# str mit zweistelligen Zahlen und anderem Zug (nicht fest hinschreiben!)
abfahrt = Abfahrt("RE 4", "Aachen", 17, 42)
assert str(abfahrt) == "17:42 RE 4 nach Aachen", (
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

# repr stimmt auch, wenn das Ziel ein Apostroph enthält
abfahrt = Abfahrt("TGV 9", "Val d'Isère", 6, 0)
assert repr(abfahrt) == "Abfahrt('TGV 9', \"Val d'Isère\", 6, 0)", (
    f"repr(Abfahrt('TGV 9', \"Val d'Isère\", 6, 0)) ergibt {repr(abfahrt)!r}, "
    "erwartet war 'Abfahrt(\\'TGV 9\\', \"Val d\\'Isère\", 6, 0)'.\n"
    "Tipp: Schreiben Sie {self.ziel!r} statt '{self.ziel}', dann wählt Python passende Anführungszeichen."
)

# Listen zeigen ihre Elemente mit repr
tafel = [Abfahrt("RE 4", "Aachen", 17, 42), Abfahrt("S 1", "Dortmund", 0, 30)]
assert str(tafel) == "[Abfahrt('RE 4', 'Aachen', 17, 42), Abfahrt('S 1', 'Dortmund', 0, 30)]", (
    f"str() einer Liste mit zwei Abfahrten ergibt {str(tafel)!r}, "
    "erwartet war \"[Abfahrt('RE 4', 'Aachen', 17, 42), Abfahrt('S 1', 'Dortmund', 0, 30)]\".\n"
    "Tipp: Listen benutzen für ihre Elemente __repr__, nicht __str__."
)

# Die Ausgabe des Programms stimmt
assert AUSGABE == "09:05 ICE 597 nach München\n[Abfahrt('ICE 597', 'München', 9, 5)]", (
    f"Erwartete Ausgabe:\n09:05 ICE 597 nach München\n[Abfahrt('ICE 597', 'München', 9, 5)]\nIhr Programm:\n{AUSGABE}"
)
