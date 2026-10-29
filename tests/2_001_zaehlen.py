# Automatisch erzeugt aus lehrkraft/muster/2_001_zaehlen.py - nicht von Hand ändern.
# vorlage-hash: ed45b13e0519d95e
# text-hash: 9f5851ee965e910e
# thema: kontrollfluss
# inhalt: for-Schleife

# Ausgabe sind die Zahlen 1 bis 5
if AUSGABE.startswith("0"):
    hinweis = "\nTipp: range(5) liefert 0 bis 4, range(1, 6) liefert 1 bis 5."
else:
    hinweis = ""
assert AUSGABE == "1\n2\n3\n4\n5", f"Erwartet:\n1\n2\n3\n4\n5\nIhr Programm gibt aus:\n{AUSGABE}{hinweis}"

# Eine for-Schleife wird benutzt
assert verwendet("for"), "Benutzen Sie eine for-Schleife, statt fünfmal print zu schreiben."
