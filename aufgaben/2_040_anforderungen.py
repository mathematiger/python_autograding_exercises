"""Aufgabe 2_040 – Anforderungen als Bits                        Stufe 2 ★★☆☆☆

Für eine Ausschreibung neuer Notebooks prüft die Einkaufsabteilung jedes
Angebot gegen eine Liste von Anforderungen (Akkulaufzeit, Gewicht, Garantie
…). Das Bewertungswerkzeug speichert das Ergebnis platzsparend als eine
einzige ganze Zahl: In ihrer Binärdarstellung steht jede Stelle für eine
Anforderung, 1 heißt erfüllt, 0 nicht erfüllt. Die Stelle ganz rechts ist
Anforderung 1, die links daneben Anforderung 2 und so weiter. Für den
Bericht soll die Zahl als Folge von Nullen und Einsen erscheinen.

Vervollständigen Sie die Funktion `binaer(zahl, stellen=1)`. Sie liefert die
Binärdarstellung von zahl als Text. Ist der Text kürzer als stellen, wird er
vorn mit Nullen aufgefüllt, damit die Anforderungen mehrerer Angebote
untereinander stehen. Ist er länger, wird nichts abgeschnitten.

    binaer(11)        →  "1011"      (8 + 2 + 1)
    binaer(11, 6)     →  "001011"
    binaer(0)         →  "0"
    binaer(0, 4)      →  "0000"
    binaer(300, 4)    →  "100101100"

Rechnen Sie mit // und % selbst, ohne die fertigen Funktionen bin(...) und
format(...).

Grenzen: zahl ist eine ganze Zahl mit 0 ≤ zahl < 2**60, stellen eine ganze
Zahl mit 1 ≤ stellen ≤ 64.

Hintergrund: Im Zehnersystem ist jede Stelle zehnmal so viel wert wie die
rechts daneben, im Binärsystem (Zweiersystem) nur doppelt so viel: 1011 ist
1·8 + 0·4 + 1·2 + 1·1 = 11. Die Ziffern bekommt man wie bei der Quersumme
(Aufgabe 2_039), nur mit 2 statt 10: zahl % 2 ist die letzte Binärziffer,
zahl // 2 die Zahl ohne sie.

    11 % 2 → 1,   11 // 2 → 5
     5 % 2 → 1,    5 // 2 → 2
     2 % 2 → 0,    2 // 2 → 1
     1 % 2 → 1,    1 // 2 → 0   fertig: von unten gelesen 1011

Die Ziffern kommen also von hinten nach vorn. Darum setzt man jede neue
Ziffer vorn an den bisherigen Text: text = str(ziffer) + text.

Tipp: Mit einer zweiten while-Schleife, die eine "0" vorn anfügt, solange
len(text) < stellen ist, erledigt sich auch zahl = 0 von selbst.
"""


def binaer(zahl, stellen=1):
    """Binärdarstellung von zahl als Text, vorn mit Nullen auf mindestens stellen Zeichen aufgefüllt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(binaer(11))
print(binaer(11, 6))
