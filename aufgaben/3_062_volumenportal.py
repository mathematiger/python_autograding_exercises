"""Aufgabe 3_062 – Volumenportal                                 Stufe 3 ★★★☆☆

Ein Internetanbieter misst für jeden Geschäftskunden, wie viele Megabyte
(MB) pro Minute über seinen Anschluss übertragen werden. Im
Kundenportal kann man sich für einen beliebigen Zeitraum das
übertragene Datenvolumen anzeigen lassen, etwa für die Zeit eines
Datensicherungslaufs oder einer Videokonferenz. Das Portal bekommt
Tausende solcher Anfragen am Tag, und eine Messreihe hat 1440 Werte pro
Tag; jede Anfrage einzeln aufzusummieren, ist zu langsam.

Die Messwerte stehen in einer Liste, Eintrag m für Minute m. Ein
Zeitraum (von, bis) umfasst wie bei range die Minuten von bis
ausschließlich bis, also werte[von:bis]. Schreiben Sie drei Funktionen:

- `praefixsummen(werte)` gibt die Liste p mit len(werte) + 1 Einträgen
  zurück, in der p[i] die Summe der ersten i Werte ist; p[0] ist 0.
- `volumen(praefix, von, bis)` gibt mit der Präfixsummenliste das
  Volumen des Zeitraums (von, bis) zurück, ohne Schleife.
- `beantworte(werte, anfragen)` gibt für eine Liste von Zeiträumen die
  Liste ihrer Volumen zurück, in derselben Reihenfolge. Benutzen Sie
  dafür die beiden anderen Funktionen.

    werte = [120, 80, 0, 300, 45, 60, 210, 15]
    praefixsummen(werte)   →  [0, 120, 200, 200, 500, 545, 605, 815, 830]
    p = praefixsummen(werte)
    volumen(p, 2, 5)       →  345        (0 + 300 + 45)
    beantworte(werte, [(0, 8), (3, 4), (2, 2)])   →  [830, 300, 0]

Grenzen: werte hat 0 bis 100 000 Einträge, ganze Zahlen von 0 bis
100 000. anfragen hat 0 bis 100 000 Paare (von, bis) mit 0 ≤ von ≤
bis ≤ len(werte); bei von == bis ist der Zeitraum leer. volumen soll
O(1) Schritte brauchen, also gleich viele, egal wie lang der Zeitraum
ist, und beantworte O(n + q) für n Werte und q Anfragen.

Hintergrund: Naiv rechnet man jede Anfrage mit sum(werte[von:bis]) neu
aus. Das sind bis zu n Schritte je Anfrage, zusammen O(n · q), bei
100 000 Werten und 100 000 Anfragen also bis zu zehn Milliarden. Die
Idee der Präfixsummen ist, einmal vorab für jede Stelle die Summe
aller Werte davor auszurechnen, in einem Durchgang mit einer laufenden
Summe wie in Aufgabe 1_025:

    werte  =     [ 3, 1, 4,  1,  5]
    p      =  [0, 3, 4, 8,  9, 14]

Dann ist die Summe eines Bereichs der Unterschied zweier Präfixsummen:
p[bis] ist die Summe von allem vor bis, p[von] die Summe von allem vor
von; zieht man das eine vom anderen ab, bleibt genau werte[von:bis]
übrig. Im Beispiel ist die Summe von werte[1:4] = 1 + 4 + 1 gleich
p[4] - p[1] = 9 - 3 = 6. Das kostet zwei Zugriffe, egal wie lang der
Bereich ist: O(1). Die Vorarbeit von O(n) lohnt sich, sobald viele
Anfragen an dieselben Werte kommen. Dass p einen Eintrag mehr hat als
werte und mit 0 beginnt, erspart den Sonderfall von == 0. Wie beim
gleitenden Fenster in Aufgabe 3_061 rechnet man also nichts doppelt;
dort lag aber die Breite fest, hier darf jeder Zeitraum anders sein.
"""


def praefixsummen(werte):
    """Gibt die Liste der Präfixsummen zurück: p[i] ist die Summe der ersten i Werte."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def volumen(praefix, von, bis):
    """Gibt die Summe der Werte von von bis ausschließlich bis zurück, ohne Schleife."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def beantworte(werte, anfragen):
    """Gibt für jeden Zeitraum (von, bis) in anfragen das Volumen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


werte = [120, 80, 0, 300, 45, 60, 210, 15]
p = praefixsummen(werte)
print(p)
print(volumen(p, 2, 5))
print(beantworte(werte, [(0, 8), (3, 4), (2, 2)]))
