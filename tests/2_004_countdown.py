# Automatisch erzeugt aus lehrkraft/muster/2_004_countdown.py - nicht von Hand ändern.
# vorlage-hash: 88d0a2e98633178d
# text-hash: e15d3bd9c3740377
# thema: kontrollfluss
# inhalt: while-Schleife

EINGABEN = ["3"]

# Die Zahlen 3, 2, 1 werden heruntergezählt („Neustart!“ zählt hier noch nicht)
nur_zahlen = vergleichbar(AUSGABE.casefold().replace("neustart", " "))
assert nur_zahlen == vergleichbar("3\n2\n1"), (
    f"Bei Eingabe 3 erwartet: die Zahlen 3, 2 und 1 untereinander – Ihr Programm gibt aus:\n{AUSGABE}\n"
    "Tipp: Geben Sie in der Schleife zahl aus und verringern Sie zahl danach um 1."
)

# Countdown ab 3
if AUSGABE.count("Neustart!") > 1:
    hinweis_drei = '\nTipp: print("Neustart!") gehört unter die Schleife, nicht eingerückt hinein.'
else:
    hinweis_drei = ""
assert vergleichbar(AUSGABE) == vergleichbar("3\n2\n1\nNeustart!"), (
    f"Bei Eingabe 3 erwartet:\n3\n2\n1\nNeustart!\nIhr Programm gibt aus:\n{AUSGABE}{hinweis_drei}"
)

# Countdown ab 5 (nicht fest 3, 2, 1 hinschreiben!)
ausgabe_fuenf = starte("5")
assert vergleichbar(ausgabe_fuenf) == vergleichbar("5\n4\n3\n2\n1\nNeustart!"), (
    f"Bei Eingabe 5 erwartet:\n5\n4\n3\n2\n1\nNeustart!\nIhr Programm gibt aus:\n{ausgabe_fuenf}"
)

# Countdown ab 1: eine Zahl, dann Neustart!
ausgabe_eins = starte("1")
assert vergleichbar(ausgabe_eins) == vergleichbar("1\nNeustart!"), f"Bei Eingabe 1 erwartet:\n1\nNeustart!\nIhr Programm gibt aus:\n{ausgabe_eins}"

# Countdown ab 0: nur Neustart!
ausgabe_null = starte("0")
if "Neustart!" in ausgabe_null:
    hinweis = "Tipp: Die Bedingung muss schon beim ersten Mal falsch sein, wenn die Zahl 0 ist."
else:
    hinweis = 'Tipp: print("Neustart!") gehört unter die Schleife, nicht eingerückt hinein.'
assert vergleichbar(ausgabe_null) == vergleichbar("Neustart!"), (
    f"Bei Eingabe 0 erwartet nur „Neustart!“ – Ihr Programm gibt aus:\n{ausgabe_null}\n{hinweis}"
)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für diese Aufgabe eine while-Schleife."

# Viele zufällige Startzahlen
zufall = Zufall(2004)
for start in sorted(zufall.sample(range(101), 20)):
    # Aufsteigend sortiert, damit eine Fehlermeldung die kleinste fehlerhafte Startzahl zeigt
    # Vergleichsrechnung mit range statt while: alle Zahlen von start abwärts bis 1
    erwartet = "\n".join([str(zahl) for zahl in range(start, 0, -1)] + ["Neustart!"])
    ausgabe = starte(str(start))
    assert vergleichbar(ausgabe) == vergleichbar(erwartet), f"Bei Eingabe {start} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"

# Countdown ab 1000, der oberen Grenze
ausgabe_tausend = starte("1000")
zeilen = ausgabe_tausend.split("\n")
erwartet = [str(zahl) for zahl in range(1000, 0, -1)] + ["Neustart!"]
assert vergleichbar(ausgabe_tausend) == vergleichbar("\n".join(erwartet)), (
    f"Bei Eingabe 1000 erwartet: 1001 Zeilen, 1000 bis 1 und dann „Neustart!“. "
    f"Ihr Programm gibt {len(zeilen)} Zeilen aus, die ersten: {zeilen[:3]}, die letzten: {zeilen[-3:]}"
)
