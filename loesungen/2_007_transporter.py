# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_007_transporter.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_007_transporter

"""Aufgabe 2_007 – Transporter beladen                           Stufe 2 ★★☆☆☆

Im Paketzentrum laufen die Pakete auf einem Förderband nacheinander zum
Transporter. Der Transporter darf höchstens eine bestimmte Last in Kilogramm
tragen. Die Packer laden die Pakete in der Reihenfolge ein, in der sie kommen.
Passt ein Paket nicht mehr hinein, ist der Transporter voll und fährt los; die
restlichen Pakete warten auf den nächsten, auch wenn ein späteres, leichteres
Paket noch gepasst hätte. Vervollständigen Sie die Funktion `einladen`, die
zurückgibt, wie viele Pakete in den Transporter kommen.

    einladen([300, 200, 400, 150], 800)  →  2
    einladen([100, 250, 50], 400)        →  3
    einladen([300, 200], 500)            →  2
    einladen([900, 10], 800)             →  0
    einladen([], 800)                    →  0

Im ersten Beispiel sind nach zwei Paketen 500 kg geladen; mit dem dritten
wären es 900 kg, also ist Schluss. Das vierte Paket mit 150 kg wird nicht mehr
angesehen. Genau die Höchstlast (wie im dritten Beispiel) ist erlaubt.

Grenzen: gewichte ist eine Liste mit 0 ≤ len(gewichte) ≤ 10 000 ganzen Zahlen,
jedes Gewicht mit 1 ≤ gewicht ≤ 10 000. hoechstlast ist eine ganze Zahl mit
0 ≤ hoechstlast ≤ 10**8.

Hintergrund: Eine for-Schleife geht normalerweise alle Elemente einer Liste
durch. Mit der Anweisung break verlässt man die Schleife sofort, auch mitten
in der Liste; das Programm macht hinter der Schleife weiter. Man benutzt break,
wenn man unterwegs merkt, dass sich der Rest nicht mehr lohnt:

    for zahl in [4, 8, 15, 16]:
        if zahl > 10:
            break
        print(zahl)

Das gibt nur 4 und 8 aus. Ohne break würde die Schleife alle Zahlen ansehen
und nur die großen nicht ausgeben – das ist etwas anderes.

Tipp: Merken Sie sich in zwei Variablen die bisher geladene Last und die
Anzahl der Pakete. Prüfen Sie vor dem Einladen, ob last + gewicht noch passt.
"""


def einladen(gewichte, hoechstlast):
    """Gibt zurück, wie viele Pakete vom Anfang der Liste in den Transporter passen."""
    last = 0
    anzahl = 0
    for gewicht in gewichte:
        if last + gewicht > hoechstlast:
            break
        last = last + gewicht
        anzahl = anzahl + 1
    return anzahl


print(einladen([300, 200, 400, 150], 800))


# Idee: Die Schleife geht die Pakete der Reihe nach durch und merkt sich die
# bisherige Last und die Anzahl. Vor jedem Paket wird geprüft, ob last + gewicht
# die Höchstlast überschreitet; dann ist der Transporter voll, und break beendet
# die Schleife. Sonst kommt das Paket dazu.
#
# Anderer Weg: eine while-Schleife über den Index, die läuft, solange noch
# Pakete da sind und das nächste passt. Die Bedingung wird dann länger, ein
# break braucht man nicht.
#
# Typische Fehler: >= statt > in der Prüfung (genau die Höchstlast ist erlaubt),
# zu schwere Pakete nur überspringen statt aufzuhören (dann rutschen spätere,
# leichte Pakete nach), oder erst einladen und danach prüfen, sodass ein Paket
# zu viel gezählt wird.
