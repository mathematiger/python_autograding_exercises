# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_038_binaeradresse.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_038_binaeradresse

"""Aufgabe 2_038 – Binäradresse                                  Stufe 2 ★★☆☆☆

Eine IPv4-Adresse wie 192.168.10.1 besteht aus vier Zahlen von 0 bis 255,
den Oktetten. Der Rechner sieht darin 32 Bits, je acht pro Oktett. Wer
ausrechnen will, welche Adressen in dasselbe Netz gehören, schreibt die
Adresse deshalb oft binär hin, also nur mit den Ziffern 0 und 1:

    11000000.10101000.00001010.00000001

Für eine Schulung zum Thema Subnetze soll ein kleines Werkzeug das
übernehmen. Vervollständigen Sie zwei Funktionen:

- `als_binaer(zahl, stellen)` gibt zahl als Text aus 0 und 1 zurück, vorn
  mit Nullen auf genau `stellen` Zeichen aufgefüllt.
- `adresse_binaer(adresse)` bekommt eine Adresse als Text und gibt die vier
  Oktette binär mit je acht Stellen zurück, durch Punkte getrennt. Benutzen
  Sie dafür als_binaer.

    als_binaer(5, 4)                  →  "0101"
    als_binaer(192, 8)                →  "11000000"
    als_binaer(0, 3)                  →  "000"
    adresse_binaer("192.168.10.1")    →  "11000000.10101000.00001010.00000001"

Rechnen Sie die Binärdarstellung selbst aus, ohne bin(...), format(...)
oder f-Strings mit :b.

Grenzen: Für als_binaer ist 1 ≤ stellen ≤ 32 und 0 ≤ zahl < 2**stellen,
die Zahl passt also immer in die verlangten Stellen. Eine Adresse besteht
aus genau vier ganzen Zahlen von 0 bis 255, ohne führende Nullen und ohne
Leerzeichen, durch Punkte getrennt.

Hintergrund: Im Dezimalsystem ist jede Stelle zehnmal so viel wert wie die
rechts daneben, im Binärsystem nur doppelt so viel: 1101 bedeutet 1·8 +
1·4 + 0·2 + 1·1 = 13. Die letzte Binärziffer einer Zahl ist deshalb
zahl % 2 (0 bei geraden, 1 bei ungeraden Zahlen), und zahl // 2 streicht
sie, genau wie % 10 und // 10 im Dezimalsystem (Aufgabe 2_037). Für 13:

    13 % 2 = 1,   13 // 2 = 6
     6 % 2 = 0,    6 // 2 = 3
     3 % 2 = 1,    3 // 2 = 1
     1 % 2 = 1,    1 // 2 = 0

Die Ziffern kommen von hinten nach vorn heraus: 1, 0, 1, 1, also 1101.
Setzt man jede neue Ziffer vorn an den Text (ziffer + text), steht am Ende
alles in der richtigen Reihenfolge. Wiederholt man den Schritt genau
`stellen`-mal statt nur bis die Zahl 0 ist, kommen die führenden Nullen
von selbst dazu. Die Adresse zerlegen Sie mit split und setzen sie mit
join wieder zusammen (Aufgabe 2_015).
"""


def als_binaer(zahl, stellen):
    """Gibt zahl binär mit genau stellen Ziffern zurück."""
    text = ""
    for _ in range(stellen):
        text = str(zahl % 2) + text
        zahl = zahl // 2
    return text


def adresse_binaer(adresse):
    """Gibt die vier Oktette der Adresse binär mit je acht Stellen zurück, durch Punkte getrennt."""
    teile = []
    for oktett in adresse.split("."):
        teile.append(als_binaer(int(oktett), 8))
    return ".".join(teile)


print(als_binaer(5, 4))
print(adresse_binaer("192.168.10.1"))


# Idee: als_binaer wiederholt genau stellen-mal denselben Schritt: zahl % 2 ist die letzte Binärziffer,
# sie kommt vorn an den Text, und zahl // 2 streicht sie. Weil die Schleife nicht bei zahl == 0 aufhört,
# entstehen die führenden Nullen von selbst. adresse_binaer zerlegt die Adresse mit split("."), wandelt
# jedes Oktett mit als_binaer(int(teil), 8) um und fügt die Teile mit ".".join(...) zusammen.
# Anderer Weg: mit while zahl > 0 nur die nötigen Ziffern bestimmen und danach vorn "0" anhängen, bis der
# Text stellen Zeichen hat. Oder von der höchsten Stelle her: Ist zahl >= 2 ** (stellen - 1), kommt
# eine 1 und dieser Wert wird abgezogen, sonst eine 0, dann mit der nächstkleineren Zweierpotenz weiter.
# Typische Fehler: die Ziffer hinten anhängen (text + ziffer), dann steht alles rückwärts; nur bis
# zahl == 0 rechnen und die führenden Nullen vergessen; im Ergebnis Zahlen statt Text ("0" + 1 geht nicht)
# oder bei der Adresse int(...) vergessen.
