# Automatisch erzeugt aus lehrkraft/muster/1_014_protokoll.py - nicht von Hand ändern.
# vorlage-hash: e2fb8ebf970477b5
# thema: texte_zahlen
# inhalt: `replace`, `count` und `in`

EINGABEN = ["Meier meldet: Drucker defekt. Meier bittet um Rückruf an meier@firma.de", "Meier"]

# Das Beispiel aus der Aufgabe
erwartet = (
    "Der Name kam 2-mal vor.\n"
    "Geschwärzt: *** meldet: Drucker defekt. *** bittet um Rückruf an meier@firma.de\n"
    "Noch ein @ im Text: True"
)
assert AUSGABE == erwartet, f"Beim Beispiel aus der Aufgabe erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}"

# Ein anderer Name, der dreimal vorkommt (nicht fest Meier hinschreiben!)
ausgabe = starte("Kaya: VPN geht nicht. Kaya hat neu gestartet, Kaya wartet.", "Kaya")
erwartet = (
    "Der Name kam 3-mal vor.\n"
    "Geschwärzt: ***: VPN geht nicht. *** hat neu gestartet, *** wartet.\n"
    "Noch ein @ im Text: False"
)
if "Kaya" in ausgabe:
    hinweis = '\nTipp: protokoll.replace(name, "***") ersetzt jedes Vorkommen des Namens, nicht nur das erste.'
else:
    hinweis = ""
assert ausgabe == erwartet, (
    'Bei den Eingaben "Kaya: VPN geht nicht. Kaya hat neu gestartet, Kaya wartet." und "Kaya" erwartet:\n'
    f"{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"
)

# Kommt der Name nicht vor, bleibt der Text, wie er ist
ausgabe = starte("Monitor flackert seit Montag.", "Schulz")
erwartet = "Der Name kam 0-mal vor.\nGeschwärzt: Monitor flackert seit Montag.\nNoch ein @ im Text: False"
assert ausgabe == erwartet, (
    f'Bei den Eingaben "Monitor flackert seit Montag." und "Schulz" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}'
)

# Gezählt wird im ursprünglichen Protokoll, geprüft wird der geschwärzte Text
ausgabe = starte("Bitte Antwort an lena@schule.de, Gruß Lena", "Lena")
erwartet = (
    "Der Name kam 1-mal vor.\n"
    "Geschwärzt: Bitte Antwort an lena@schule.de, Gruß ***\n"
    "Noch ein @ im Text: True"
)
if "0-mal" in ausgabe:
    hinweis = "\nTipp: Im geschwärzten Text steht der Name nicht mehr. Zählen Sie im ursprünglichen Protokoll."
else:
    hinweis = ""
assert ausgabe == erwartet, (
    f'Bei den Eingaben "Bitte Antwort an lena@schule.de, Gruß Lena" und "Lena" erwartet:\n{erwartet}\n'
    f"Ihr Programm gibt aus:\n{ausgabe}{hinweis}"
)

# Ein @, das nur im Namen stand, ist nach dem Schwärzen weg
ausgabe = starte("Konto admin@pc7 gesperrt, admin@pc7 informiert.", "admin@pc7")
erwartet = "Der Name kam 2-mal vor.\nGeschwärzt: Konto *** gesperrt, *** informiert.\nNoch ein @ im Text: False"
if ausgabe.endswith("True"):
    hinweis = "\nTipp: Prüfen Sie mit in, ob im geschwärzten Text noch ein @ steht, nicht im ursprünglichen Protokoll."
else:
    hinweis = ""
assert ausgabe == erwartet, (
    f'Bei den Eingaben "Konto admin@pc7 gesperrt, admin@pc7 informiert." und "admin@pc7" erwartet:\n{erwartet}\n'
    f"Ihr Programm gibt aus:\n{ausgabe}{hinweis}"
)
