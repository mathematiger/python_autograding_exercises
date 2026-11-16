# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_042_kabelweg.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_042_kabelweg

"""Aufgabe 2_042 – Kabelweg                                      Stufe 2 ★★☆☆☆

In einer Lagerhalle sollen WLAN-Access-Points an der Decke hängen. Das
Netzwerkkabel kommt vom Verteilerschrank in einer Ecke und läuft quer
durch die Halle in einem Kabelkanal schräg zum Access Point. Wie lang
der Weg ist, sagt der Satz des Pythagoras: Liegt der Access Point
breite Meter nach rechts und tiefe Meter nach hinten, ist der Weg
die Wurzel aus breite² + tiefe² lang. Der kleine Rechner im Schrank
hat aber keine Wurzelfunktion. Schreiben Sie zwei Funktionen:

- `wurzel(x)` gibt eine Näherung der Quadratwurzel von x zurück, die
  höchstens 0.001 vom echten Wert abweicht. Benutzen Sie dafür die
  Bisektion (siehe Hintergrund), nicht math.sqrt und nicht ** 0.5.
- `kabelweg(breite, tiefe)` gibt die Länge des Kabelwegs in Metern
  zurück und benutzt dafür wurzel.

    wurzel(25)          →  etwa 5.0     (zum Beispiel 4.99997)
    wurzel(2)           →  etwa 1.414
    wurzel(0)           →  etwa 0.0
    kabelweg(30, 40)    →  etwa 50.0

Grenzen: 0 ≤ x ≤ 10**6 und 0 ≤ breite, tiefe ≤ 500, alle ganze Zahlen
oder Kommazahlen. Das Ergebnis darf höchstens 0.001 vom echten Wert
abweichen. Ihre Lösung soll auch für x = 10**6 mit höchstens etwa 100
Halbierungen auskommen.

Hintergrund: Die Bisektion (auch Intervallhalbierung) ist ein
Näherungsverfahren: Man kennt einen Bereich, in dem die Lösung sicher
liegt, und halbiert ihn so lange, bis er klein genug ist. Die Wurzel
von x liegt immer zwischen unten = 0 und oben = max(x, 1); die 1 ist
nötig, weil die Wurzel einer Zahl unter 1 größer ist als die Zahl
selbst (die Wurzel von 0.25 ist 0.5). Man probiert die Mitte
mitte = (unten + oben) / 2. Ist mitte * mitte größer als x, ist mitte
zu groß, und die Lösung liegt in der unteren Hälfte: oben = mitte.
Sonst liegt sie in der oberen Hälfte: unten = mitte. Jeder Durchlauf
halbiert den Bereich; das wiederholt eine while-Schleife (Aufgabe
2_004), bis oben - unten kleiner als die erlaubte Abweichung ist.

    while oben - unten > 0.001:
        mitte = (unten + oben) / 2
        ...

Bei x = 10**6 ist der Bereich am Anfang 1 000 000 breit; nach 30
Halbierungen ist er schon kleiner als 0.001. Wer dagegen in kleinen
Schritten von 0 aus hochzählt (Guess-and-check, Aufgabe 2_005), bräuchte
für 0.001 Genauigkeit eine Million Schritte.
"""


def wurzel(x):
    """Gibt eine Näherung der Quadratwurzel von x zurück, auf 0.001 genau."""
    unten = 0
    oben = max(x, 1)
    while oben - unten > 0.001:
        mitte = (unten + oben) / 2
        if mitte * mitte > x:
            oben = mitte
        else:
            unten = mitte
    return (unten + oben) / 2


def kabelweg(breite, tiefe):
    """Gibt die Länge des schrägen Kabelwegs in Metern zurück."""
    return wurzel(breite * breite + tiefe * tiefe)


print(round(wurzel(25), 2))
print(round(kabelweg(30, 40), 2))


# Idee: Die Wurzel liegt zwischen unten = 0 und oben = max(x, 1). In jedem Durchlauf wird die Mitte
# probiert: Ist mitte * mitte > x, ist die Mitte zu groß und wird die neue obere Grenze, sonst die neue untere.
# Sobald oben - unten höchstens 0.001 ist, liegt die echte Wurzel zwischen beiden Grenzen, und die Mitte
# davon weicht höchstens 0.0005 ab. kabelweg ruft wurzel(breite * breite + tiefe * tiefe) auf.
#
# Anderer Weg: Guess-and-check mit schaetzung = 0 und schaetzung += 0.0001, solange schaetzung * schaetzung < x;
# das braucht bei x = 10**6 zehn Millionen Durchläufe. Viel schneller als die Bisektion ist das
# Newton-Verfahren: schaetzung = (schaetzung + x / schaetzung) / 2 nähert sich nach wenigen Schritten an.
#
# Typische Fehler: oben = x statt max(x, 1) (bei x < 1 liegt die Wurzel außerhalb des Bereichs), die Zweige
# vertauschen (der Bereich wandert von der Wurzel weg), unten = mitte + 1 wie bei der binären Suche in Listen
# (bei Kommazahlen springt man über die Lösung) oder die Schleife bis oben - unten > 0 laufen lassen
# (Kommazahlen werden nicht immer gleich, dann läuft sie sehr lange oder endlos).
#
# Laufzeit: Jeder Durchlauf halbiert den Bereich; bei der Breite b und der Genauigkeit e sind es etwa
# log2(b / e) Durchläufe, für x = 10**6 also rund 30.
