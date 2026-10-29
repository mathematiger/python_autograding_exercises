# Automatisch erzeugt aus lehrkraft/muster/1_013_benutzername.py - nicht von Hand ändern.
# vorlage-hash: 2995a863f7c33049
# thema: texte_zahlen
# inhalt: String-Methoden `upper`, `lower`, `strip`

EINGABEN = ["  AMueller ", " pb  "]

# Bei den Eingaben "  AMueller " und " pb  " stimmen Name und Kürzel
erwartet = "Benutzername: amueller (8 Zeichen)\nStandort: PB"
assert AUSGABE == erwartet, (
    f'Bei den Eingaben "  AMueller " und " pb  " erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}'
)

# Auch hinter dem Kürzel sind die Leerzeichen entfernt (in der Ausgabe sieht man sie nicht)
assert standort == "PB", (
    f'Bei der Eingabe " pb  " enthält standort {standort!r}, erwartet war \'PB\'.\n'
    "Tipp: strip() entfernt die Leerzeichen auf beiden Seiten."
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

# Ränder: ein Buchstabe ohne Leerzeichen und 20 Buchstaben mit fünf Leerzeichen auf beiden Seiten
raender = [
    ("Q", "pb", "Benutzername: q (1 Zeichen)\nStandort: PB"),
    ("     ABCDEFGHIJKLMNOPQRST     ", "     hb     ", "Benutzername: abcdefghijklmnopqrst (20 Zeichen)\nStandort: HB"),
]
for name_test, standort_test, erwartet in raender:
    ausgabe = starte(name_test, standort_test)
    assert ausgabe == erwartet, (
        f'Bei den Eingaben "{name_test}" und "{standort_test}" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}'
    )

# 40 zufällige Eingaben mit gemischter Groß- und Kleinschreibung und Leerzeichen am Rand
zufall = Zufall(1013)
kleinbuchstaben = "abcdefghijklmnopqrstuvwxyz"
for _ in range(40):
    # Erst den bereinigten Wert auslosen, dann einzelne Buchstaben umschalten und Leerzeichen anfügen
    name_sauber = "".join(zufall.choices(kleinbuchstaben, k=zufall.randint(1, 20)))
    name_test = ""
    for buchstabe in name_sauber:
        name_test += zufall.choice([buchstabe, buchstabe.upper()])
    name_test = " " * zufall.randint(0, 5) + name_test + " " * zufall.randint(0, 5)
    standort_sauber = "".join(zufall.choices(kleinbuchstaben.upper(), k=2))
    standort_test = ""
    for buchstabe in standort_sauber:
        standort_test += zufall.choice([buchstabe, buchstabe.lower()])
    standort_test = " " * zufall.randint(0, 5) + standort_test + " " * zufall.randint(0, 5)
    erwartet = f"Benutzername: {name_sauber} ({len(name_sauber)} Zeichen)\nStandort: {standort_sauber}"
    ausgabe = starte(name_test, standort_test)
    assert ausgabe == erwartet, (
        f'Bei den Eingaben "{name_test}" und "{standort_test}" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}'
    )
