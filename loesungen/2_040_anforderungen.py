# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_040_anforderungen.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_040_anforderungen

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
    text = ""
    while zahl > 0:
        text = str(zahl % 2) + text
        zahl = zahl // 2
    while len(text) < stellen:
        text = "0" + text
    return text


print(binaer(11))
print(binaer(11, 6))


# Idee: Solange zahl > 0 ist, die letzte Binärziffer zahl % 2 vorn an den Text setzen und zahl = zahl // 2
# rechnen. Danach vorn Nullen anfügen, solange der Text kürzer als stellen ist. Weil stellen mindestens 1
# ist, wird aus dem leeren Text für zahl = 0 dabei automatisch "0".
# Anderer Weg: Die Ziffern in einer Liste sammeln und am Ende umgedreht mit "".join(...) zusammensetzen.
# Oder von links: die größte Zweierpotenz suchen, die nicht größer als zahl ist, und für jede Potenz
# abwärts prüfen, ob sie hineinpasst (1) oder nicht (0). Fertig ginge es mit bin(zahl)[2:].zfill(stellen).
# Typische Fehler: die Ziffern hinten anhängen (Ergebnis rückwärts), zahl = 0 vergessen (leerer Text),
# zahl / 2 statt zahl // 2 oder beim Auffüllen abschneiden, wenn der Text länger als stellen ist.
