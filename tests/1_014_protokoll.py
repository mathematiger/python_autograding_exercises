# Automatisch erzeugt aus lehrkraft/muster/1_014_protokoll.py - nicht von Hand ändern.
# vorlage-hash: f930977ed9ad253a
# text-hash: 667ba74d458d5117
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

# Stand schon vorher *** im Protokoll, zählt das nicht als Name
ausgabe = starte("Ticket *** offen, Kaya fragt nach", "Kaya")
erwartet = "Der Name kam 1-mal vor.\nGeschwärzt: Ticket *** offen, *** fragt nach\nNoch ein @ im Text: False"
if "2-mal" in ausgabe:
    hinweis = "\nTipp: Zählen Sie den Namen im ursprünglichen Protokoll, nicht die *** im geschwärzten Text."
else:
    hinweis = ""
assert ausgabe == erwartet, (
    f'Bei den Eingaben "Ticket *** offen, Kaya fragt nach" und "Kaya" erwartet:\n{erwartet}\n'
    f"Ihr Programm gibt aus:\n{ausgabe}{hinweis}"
)

# Ränder: das Protokoll ist nur der Name, und ein Protokoll aus 300 Zeichen mit 60-mal dem Namen
raender = [
    ("Meier", "Meier", "Der Name kam 1-mal vor.\nGeschwärzt: ***\nNoch ein @ im Text: False"),
    ("Kaya," * 60, "Kaya", "Der Name kam 60-mal vor.\nGeschwärzt: " + "***," * 60 + "\nNoch ein @ im Text: False"),
]
for protokoll_test, name_test, erwartet in raender:
    ausgabe = starte(protokoll_test, name_test)
    assert ausgabe == erwartet, (
        f'Bei den Eingaben "{protokoll_test}" und "{name_test}" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}'
    )

# 40 zufällige Protokolle aus Wörtern, zwischen denen der Name ein paarmal steht
zufall = Zufall(1014)
namen = ["Meier", "Kaya", "Nowak", "Lena", "Schulz", "admin@pc7"]
woerter = ["drucker", "defekt", "bitte", "um", "rückruf", "an", "meier@firma.de", "vpn", "geht", "nicht",
           "seit", "montag", "monitor", "flackert", "lena@schule.de", "neu", "gestartet"]
for _ in range(40):
    name_test = zufall.choice(namen)
    # Protokoll und geschwärzten Text Stück für Stück gleichzeitig aufbauen und dabei mitzählen. Die Wörter
    # sind klein geschrieben, enthalten also keinen der Namen; zwei von ihnen enthalten ein @.
    teile = []
    teile_geschwaerzt = []
    anzahl_erwartet = 0
    for _ in range(zufall.randint(1, 15)):
        if zufall.random() < 0.25:
            teile.append(name_test)
            teile_geschwaerzt.append("***")
            anzahl_erwartet += 1
        else:
            wort = zufall.choice(woerter)
            teile.append(wort)
            teile_geschwaerzt.append(wort)
    protokoll_test = " ".join(teile)
    geschwaerzt_erwartet = " ".join(teile_geschwaerzt)
    adresse_erwartet = "meier@firma.de" in teile or "lena@schule.de" in teile
    erwartet = (
        f"Der Name kam {anzahl_erwartet}-mal vor.\n"
        f"Geschwärzt: {geschwaerzt_erwartet}\n"
        f"Noch ein @ im Text: {adresse_erwartet}"
    )
    ausgabe = starte(protokoll_test, name_test)
    assert ausgabe == erwartet, (
        f'Bei den Eingaben "{protokoll_test}" und "{name_test}" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}'
    )
