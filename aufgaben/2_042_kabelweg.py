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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kabelweg(breite, tiefe):
    """Gibt die Länge des schrägen Kabelwegs in Metern zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(round(wurzel(25), 2))
print(round(kabelweg(30, 40), 2))
