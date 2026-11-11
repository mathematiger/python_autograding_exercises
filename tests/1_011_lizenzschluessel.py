# Automatisch erzeugt aus lehrkraft/muster/1_011_lizenzschluessel.py - nicht von Hand ändern.
# vorlage-hash: c3a958ce5759f610
# text-hash: 6d13012d6f0d043c
# thema: texte_zahlen
# inhalt: Länge und Indizes

EINGABEN = ["B7K2-QX9M-41TP"]

# Bei Eingabe B7K2-QX9M-41TP stimmen Länge, erstes und letztes Zeichen
erwartet = "Der Schlüssel hat 14 Zeichen.\nErstes Zeichen: B\nLetztes Zeichen: P"
if "Erstes Zeichen: 7" in AUSGABE:
    hinweis = "\nTipp: Python zählt ab 0. Das erste Zeichen ist schluessel[0]."
else:
    hinweis = ""
assert AUSGABE == erwartet, (
    f"Bei Eingabe B7K2-QX9M-41TP erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}{hinweis}"
)

# Ein anderer Schlüssel ergibt andere Werte (nicht fest 14, B und P hinschreiben!)
ausgabe = starte("A93F-77QD-0X2S5")
erwartet = "Der Schlüssel hat 15 Zeichen.\nErstes Zeichen: A\nLetztes Zeichen: 5"
assert ausgabe == erwartet, (
    f"Bei Eingabe A93F-77QD-0X2S5 erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"
)

# Ein Schlüssel mit Tippfehler ist kürzer; das letzte Zeichen hängt von der Länge ab
erwartet = "Der Schlüssel hat 7 Zeichen.\nErstes Zeichen: C\nLetztes Zeichen: 8"
try:
    ausgabe = starte("C1D4-88")
    hinweis = ""
    if "Letztes Zeichen: 8" not in ausgabe:
        hinweis = "\nTipp: Das letzte Zeichen hängt von der Länge ab. Benutzen Sie den Index anzahl - 1."
except Exception as fehler:
    # Ein fester Index wie schluessel[13] bricht hier mit IndexError ab; dann soll der Tipp erscheinen
    ausgabe = f"(Abbruch: {fehler})"
    hinweis = (
        "\nTipp: Dieser Schlüssel hat nur 7 Zeichen, ein fester Index wie [13] oder der Index anzahl "
        "geht über das Ende hinaus. Das letzte Zeichen hat den Index anzahl - 1."
    )
assert ausgabe == erwartet, (
    f"Bei Eingabe C1D4-88 erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"
)

# Ein Schlüssel aus einem einzigen Zeichen: erstes und letztes Zeichen sind gleich
ausgabe = starte("X")
erwartet = "Der Schlüssel hat 1 Zeichen.\nErstes Zeichen: X\nLetztes Zeichen: X"
assert ausgabe == erwartet, f"Bei Eingabe X erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"

# Das erste Zeichen hat den Index 0, nicht 1
ausgabe = starte("PRO-2026-ABCDE-S")
erwartet = "Der Schlüssel hat 16 Zeichen.\nErstes Zeichen: P\nLetztes Zeichen: S"
if "Erstes Zeichen: R" in ausgabe:
    hinweis = "\nTipp: Python zählt ab 0. Das erste Zeichen ist schluessel[0]."
else:
    hinweis = ""
assert ausgabe == erwartet, (
    f"Bei Eingabe PRO-2026-ABCDE-S erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"
)

# Rand: ein Schlüssel aus 50 Zeichen
ausgabe = starte("KX7Q-1234-ABCD-5678-EFGH-9012-IJKL-3456-MNOP-7890Z")
erwartet = "Der Schlüssel hat 50 Zeichen.\nErstes Zeichen: K\nLetztes Zeichen: Z"
assert ausgabe == erwartet, f"Bei einem Schlüssel aus 50 Zeichen erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"

# 40 zufällige Schlüssel aus 1 bis 50 Zeichen
zufall = Zufall(1011)
erlaubte_zeichen = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
for _ in range(40):
    laenge = zufall.randint(1, 50)
    zeichen = zufall.choices(erlaubte_zeichen, k=laenge)
    schluessel_test = "".join(zeichen)
    erwartet = f"Der Schlüssel hat {laenge} Zeichen.\nErstes Zeichen: {zeichen[0]}\nLetztes Zeichen: {zeichen[-1]}"
    ausgabe = starte(schluessel_test)
    assert ausgabe == erwartet, f"Bei Eingabe {schluessel_test} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"

# Die Länge wird mit len bestimmt
assert verwendet("len"), "Bestimmen Sie die Länge mit len(schluessel)."
