# Automatisch erzeugt aus lehrkraft/muster/2_004_countdown.py - nicht von Hand ändern.
# vorlage-hash: 450dfa44f570c5bb
# thema: kontrollfluss
# inhalt: while-Schleife

EINGABEN = ["3"]

# Countdown ab 3
assert AUSGABE == "3\n2\n1\nStart!", f"Bei Eingabe 3 erwartet:\n3\n2\n1\nStart!\nIhr Programm gibt aus:\n{AUSGABE}"

# Countdown ab 5 (nicht fest 3, 2, 1 hinschreiben!)
ausgabe_fuenf = starte("5")
assert ausgabe_fuenf == "5\n4\n3\n2\n1\nStart!", (
    f"Bei Eingabe 5 erwartet:\n5\n4\n3\n2\n1\nStart!\nIhr Programm gibt aus:\n{ausgabe_fuenf}"
)

# Countdown ab 1: eine Zahl, dann Start!
ausgabe_eins = starte("1")
assert ausgabe_eins == "1\nStart!", f"Bei Eingabe 1 erwartet:\n1\nStart!\nIhr Programm gibt aus:\n{ausgabe_eins}"

# Countdown ab 0: nur Start!
ausgabe_null = starte("0")
if "Start!" in ausgabe_null:
    hinweis = "Tipp: Die Bedingung muss schon beim ersten Mal falsch sein, wenn die Zahl 0 ist."
else:
    hinweis = 'Tipp: print("Start!") gehört unter die Schleife, nicht eingerückt hinein.'
assert ausgabe_null == "Start!", (
    f'Bei Eingabe 0 erwartet nur "Start!" – Ihr Programm gibt aus:\n{ausgabe_null}\n{hinweis}'
)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# Viele zufällige Startzahlen
zufall = Zufall(2004)
for start in sorted(zufall.sample(range(101), 20)):
    # Aufsteigend sortiert, damit eine Fehlermeldung die kleinste fehlerhafte Startzahl zeigt
    # Vergleichsrechnung mit range statt while: alle Zahlen von start abwärts bis 1
    erwartet = "\n".join([str(zahl) for zahl in range(start, 0, -1)] + ["Start!"])
    ausgabe = starte(str(start))
    assert ausgabe == erwartet, f"Bei Eingabe {start} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"

# Countdown ab 1000, der oberen Grenze
ausgabe_tausend = starte("1000")
zeilen = ausgabe_tausend.split("\n")
erwartet = [str(zahl) for zahl in range(1000, 0, -1)] + ["Start!"]
assert zeilen == erwartet, (
    f"Bei Eingabe 1000 erwartet: 1001 Zeilen, 1000 bis 1 und dann „Start!“. "
    f"Ihr Programm gibt {len(zeilen)} Zeilen aus, die ersten: {zeilen[:3]}, die letzten: {zeilen[-3:]}"
)
