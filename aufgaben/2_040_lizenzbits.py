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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(binaer(13))
