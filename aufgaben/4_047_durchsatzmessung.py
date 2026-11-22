"""Aufgabe 4_047 – Durchsatzmessung                              Stufe 4 ★★★★☆

Eine Außenstelle bekommt eine neue Glasfaserleitung mit 1000 Mbit/s.
Bei der Abnahme kopiert die Administratorin eine große Datei über die
Leitung, und ein Messwerkzeug liefert jede Sekunde den Durchsatz, also
wie viele Mbit in dieser Sekunde übertragen wurden. Am Anfang ist der
Durchsatz klein: TCP, das Protokoll unter der Kopie, schickt erst
wenige Pakete und steigert sich, solange keine verloren gehen (der
sogenannte Slow Start). Danach sollte er fast die volle Bandbreite
erreichen, mit gelegentlichen Einbrüchen. Schreiben Sie mit dem Modul
itertools drei Funktionen, die je eine Liste zurückgeben:

- `anlaufphase(durchsatz, ziel)`: die Messwerte vom Anfang an, solange
  sie kleiner als ziel sind. Mit dem ersten Wert ab ziel endet die
  Anlaufphase; spätere Einbrüche gehören nicht mehr dazu.
- `nach_dem_anlauf(durchsatz, ziel, sekunden)`: die ersten sekunden
  Messwerte ab dem ersten Wert, der mindestens ziel ist, einschließlich
  dieses Werts und auch mit späteren Einbrüchen. Gibt es weniger, dann
  alle bis zum Ende.
- `mit_verlust(durchsatz, verluste)`: verluste enthält für jede Sekunde,
  wie viele Pakete verloren gingen. Die Funktion gibt die Messwerte der
  Sekunden zurück, in denen mindestens ein Paket verloren ging. Ist eine
  der beiden Folgen kürzer, endet das Ergebnis mit ihr.

durchsatz ist ein beliebiges Iterable, auch ein Generator, der ohne Ende
weiterliefert, solange die Messung läuft. Lesen Sie darum nur so viele
Werte, wie Sie brauchen.

    werte = [40, 120, 450, 910, 960, 700, 950]
    anlaufphase(werte, 900)                    →  [40, 120, 450]
    nach_dem_anlauf(werte, 900, 3)             →  [910, 960, 700]
    mit_verlust(werte, [0, 0, 0, 0, 2, 5, 0])  →  [960, 700]

Grenzen: durchsatz liefert ganze Zahlen von 0 bis 10 000; ist er
endlos, kommt irgendwann ein Wert ab ziel. 0 ≤ ziel ≤ 10 000,
0 ≤ sekunden ≤ 100 000. verluste ist eine Liste mit 0 bis 100 000
ganzen Zahlen von 0 bis 1000. Endliche Folgen haben höchstens
100 000 Werte.

Hintergrund: Mit islice (Aufgabe 4_040) nimmt man von einem Iterable
eine feste Anzahl. Oft hängt das Ende aber vom Inhalt ab. Dafür hat
itertools zwei Gegenstücke, die beide eine Bedingung als Funktion
bekommen:

    from itertools import compress, dropwhile, takewhile

    werte = [1, 4, 6, 3, 8]
    list(takewhile(lambda x: x < 5, werte))    →  [1, 4]
    list(dropwhile(lambda x: x < 5, werte))    →  [6, 3, 8]

takewhile liefert Elemente, solange die Bedingung gilt, und hört beim
ersten Element auf, für das sie nicht gilt; dieses Element liefert es
nicht mehr. dropwhile überspringt Elemente, solange die Bedingung gilt,
und liefert danach alles, ohne die Bedingung noch einmal zu prüfen.
Das ist der Unterschied zu einer Comprehension mit if (Aufgabe 3_017):
Die 3 im Beispiel ist kleiner als 5, steht aber hinter der 6 und
gehört darum nicht zum Anfang. Beide arbeiten lazy und lesen nur so
weit wie nötig; takewhile liest also genau ein Element über das letzte
gelieferte hinaus.

compress(daten, auswahl) liefert die Elemente von daten, bei denen das
Element von auswahl an derselben Stelle wahr ist, also nicht 0, nicht
False, nicht leer. Es hört auf, sobald eine der beiden Folgen zu Ende
ist:

    list(compress("abcde", [1, 0, 3, 0]))      →  ["a", "c"]

Alle drei geben Iteratoren zurück; list(...) macht daraus eine Liste,
islice(..., n) begrenzt sie auf n Elemente.
"""

from itertools import compress, dropwhile, islice, takewhile


def anlaufphase(durchsatz, ziel):
    """Gibt die Messwerte vom Anfang zurück, solange sie kleiner als ziel sind."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def nach_dem_anlauf(durchsatz, ziel, sekunden):
    """Gibt die ersten sekunden Messwerte ab dem ersten Wert von mindestens ziel zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def mit_verlust(durchsatz, verluste):
    """Gibt die Messwerte der Sekunden zurück, in denen Pakete verloren gingen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


werte = [40, 120, 450, 910, 960, 700, 950]
print(anlaufphase(werte, 900))
print(nach_dem_anlauf(werte, 900, 3))
print(mit_verlust(werte, [0, 0, 0, 0, 2, 5, 0]))
