# Automatisch erzeugt aus lehrkraft/muster/1_011_lizenzschluessel.py - nicht von Hand ändern.
# vorlage-hash: dd1b49cce31a509b

EINGABEN = ["B7K2-QX9M-41TP"]

# Bei Eingabe B7K2-QX9M-41TP stimmen Länge, erstes und letztes Zeichen
erwartet = "Der Schlüssel hat 14 Zeichen.\nErstes Zeichen: B\nLetztes Zeichen: P"
assert AUSGABE == erwartet, (
    f"Bei Eingabe B7K2-QX9M-41TP erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}"
)

# Ein anderer Schlüssel ergibt andere Werte (nicht fest 14, B und P hinschreiben!)
ausgabe = starte("A93F-77QD-0X2S")
erwartet = "Der Schlüssel hat 14 Zeichen.\nErstes Zeichen: A\nLetztes Zeichen: S"
assert ausgabe == erwartet, (
    f"Bei Eingabe A93F-77QD-0X2S erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"
)

# Ein Schlüssel mit Tippfehler ist kürzer; das letzte Zeichen hängt von der Länge ab
ausgabe = starte("C1D4-88")
erwartet = "Der Schlüssel hat 7 Zeichen.\nErstes Zeichen: C\nLetztes Zeichen: 8"
if "Letztes Zeichen: -" in ausgabe or "Letztes Zeichen: 4" in ausgabe:
    hinweis = "\nTipp: Das letzte Zeichen hängt von der Länge ab. Benutzen Sie den Index anzahl - 1."
else:
    hinweis = ""
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

# Die Länge wird mit len bestimmt
assert verwendet("len"), "Bestimmen Sie die Länge mit len(schluessel)."
