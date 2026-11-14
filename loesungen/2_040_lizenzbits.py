# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_040_lizenzbits.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_040_lizenzbits

"""Aufgabe 2_040 – Lizenzbits                                   Stufe 2 ★★☆☆☆

Eine Firma hat für ihre Buchhaltungssoftware Lizenzen gekauft, bei denen
nicht jedes Modul freigeschaltet ist. Welche Module eine Lizenz enthält,
steht als eine einzige ganze Zahl im Lizenzschlüssel: Jedes Modul hat ein
Bit, und eine 1 an seiner Stelle der Binärdarstellung heißt
„freigeschaltet“. Die Stelle ganz rechts gehört zum Basismodul, die zweite
von rechts zum Export, die dritte zur Mahnung, die vierte zur Lohnabrechnung
und so weiter. Die Zahl 13 ist binär 1101: Basismodul, Mahnung und
Lohnabrechnung sind freigeschaltet, der Export nicht.

Damit die Lizenzverwaltung vor dem Kauf weiterer Module die Lizenzen
übersichtlich anzeigen kann, schreiben Sie die Funktion `binaer(zahl)`,
die die Binärdarstellung von zahl als Text aus den Zeichen 0 und 1 liefert,
ohne führende Nullen (nur die Zahl 0 selbst ist "0").

    binaer(13)  →  "1101"
    binaer(6)   →  "110"
    binaer(1)   →  "1"
    binaer(0)   →  "0"

Rechnen Sie die Ziffern selbst aus: ohne bin(), format() und f"{zahl:b}".

Grenzen: 0 ≤ zahl ≤ 2**64 - 1, eine ganze Zahl.

Hintergrund: Im Zehnersystem liefert zahl % 10 die letzte Ziffer und
zahl // 10 den Rest (Aufgabe 2_039). Im Zweiersystem geht es genauso, nur mit
2: zahl % 2 ist das letzte Bit (0 oder 1), zahl // 2 die Zahl ohne dieses
Bit. So entstehen die Bits von rechts nach links:

    13 % 2 = 1    13 // 2 = 6
     6 % 2 = 0     6 // 2 = 3
     3 % 2 = 1     3 // 2 = 1
     1 % 2 = 1     1 // 2 = 0   → fertig, von unten gelesen: 1101

Weil das letzte Bit zuerst herauskommt, setzt man jedes neue Bit vorn an
den bisherigen Text: text = str(bit) + text.
"""


def binaer(zahl):
    """Liefert die Binärdarstellung von zahl als Text, etwa "1101" für 13."""
    if zahl == 0:
        return "0"
    text = ""
    while zahl > 0:
        text = str(zahl % 2) + text
        zahl = zahl // 2
    return text


print(binaer(13))


# Idee: Solange zahl größer als 0 ist, ist zahl % 2 das nächste Bit von rechts; es wird vorn an den
# bisherigen Text gesetzt, und mit zahl // 2 geht es weiter. Die Zahl 0 wird vorher abgefangen, weil die
# Schleife bei ihr nie läuft und sonst der leere Text herauskäme.
# Anderer Weg: Die Bits erst in einer Liste sammeln (bits.append(str(zahl % 2))), die Liste am Ende mit
# bits.reverse() umdrehen und mit "".join(bits) zusammensetzen. Oder rekursiv:
# binaer(zahl) = binaer(zahl // 2) + str(zahl % 2) für zahl ≥ 2, sonst str(zahl).
# Typische Fehler: das Bit hinten anhängen (Darstellung rückwärts, 11 wird "1101" statt "1011"),
# die 0 vergessen (leerer Text), zahl / 2 statt zahl // 2 (Kommazahlen, die Schleife endet erst sehr spät).
