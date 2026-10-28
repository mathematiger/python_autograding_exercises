# Automatisch erzeugt aus lehrkraft/muster/1_013_benutzername.py - nicht von Hand ändern.
# vorlage-hash: caa165f26568d9c2
# thema: texte_zahlen
# inhalt: String-Methoden `upper`, `lower`, `strip`

EINGABEN = ["  AMueller ", " pb"]

# Bei den Eingaben "  AMueller " und " pb" stimmen Name und Kürzel
erwartet = "Benutzername: amueller (8 Zeichen)\nStandort: PB"
assert AUSGABE == erwartet, (
    f'Bei den Eingaben "  AMueller " und " pb" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}'
)

# Andere Eingaben ergeben andere Werte (nicht fest amueller und PB hinschreiben!)
ausgabe = starte("TSCHMIDT", "bi")
erwartet = "Benutzername: tschmidt (8 Zeichen)\nStandort: BI"
if "TSCHMIDT" in ausgabe or "Standort: bi" in ausgabe:
    hinweis = "\nTipp: lower() macht alles klein, upper() macht alles groß."
else:
    hinweis = ""
assert ausgabe == erwartet, f'Bei den Eingaben "TSCHMIDT" und "bi" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}'

# Leerzeichen am Ende des Namens werden entfernt
ausgabe = starte("kWeber   ", "DO")
erwartet = "Benutzername: kweber (6 Zeichen)\nStandort: DO"
if "(9 Zeichen)" in ausgabe:
    hinweis = "\nTipp: Der Name hat noch drei Leerzeichen am Ende. strip() entfernt sie."
else:
    hinweis = ""
assert ausgabe == erwartet, f'Bei den Eingaben "kWeber   " und "DO" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}'

# Leerzeichen am Anfang des Namens und rund um das Kürzel werden entfernt
ausgabe = starte("   lBecker", "  ms  ")
erwartet = "Benutzername: lbecker (7 Zeichen)\nStandort: MS"
assert ausgabe == erwartet, (
    f'Bei den Eingaben "   lBecker" und "  ms  " erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}\n'
    "Tipp: Hängen Sie strip() und lower() bzw. upper() hintereinander."
)

# Ein schon sauberer Name bleibt, wie er ist
ausgabe = starte("jnowak", "PB")
erwartet = "Benutzername: jnowak (6 Zeichen)\nStandort: PB"
assert ausgabe == erwartet, f'Bei den Eingaben "jnowak" und "PB" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}'
