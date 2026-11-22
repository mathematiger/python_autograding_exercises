"""Aufgabe 4_046 – Sensortests                                   Stufe 4 ★★★★☆

Eine Firma baut Funk-Sensorknoten für Lagerhallen: kleine Geräte, die
Temperatur und Luftfeuchte messen und über ein Gateway, eine
Empfangsstation an der Hallendecke, ins Firmennetz schicken. Vor dem
Ausrollen sind drei Dinge zu planen. Schreiben Sie mit dem Modul
itertools drei Funktionen:

- `testmatrix(firmwares, funkmodule, intervalle)` gibt die Liste aller
  Testfälle zurück: jedes Tupel (firmware, funkmodul, intervall) genau
  einmal, in der Reihenfolge von itertools.product (zuerst ändert sich
  das Intervall, zuletzt die Firmware).
- `vergleichspaare(messwerte, toleranz)` bekommt ein Dictionary vom
  Sensornamen zum Messwert. Alle Sensoren hängen im selben Raum und
  sollten fast dasselbe messen. Die Funktion gibt die Liste aller Paare
  (a, b) zurück, deren Werte sich um mehr als toleranz unterscheiden,
  mit a vor b im Alphabet; die Paare in der Reihenfolge von
  itertools.combinations über die alphabetisch sortierten Namen.
- `kuerzeste_route(lager, gateways)` plant den Rundgang eines
  Technikers, der jedes Gateway einmal wartet. Er startet am Lager,
  besucht alle Gateways und kehrt zum Lager zurück. lager ist ein Punkt
  (x, y), gateways ordnet jedem Namen einen Punkt zu. Weil er den Gängen
  der Halle folgt, ist der Weg zwischen zwei Punkten |x1 - x2| + |y1 -
  y2| Meter. Die Funktion gibt das Tupel (laenge, reihenfolge) des
  kürzesten Rundgangs zurück, reihenfolge als Tupel der Namen. Haben
  mehrere Reihenfolgen dieselbe Länge, gilt die alphabetisch kleinste.
  Ohne Gateways ist das Ergebnis (0, ()).

    testmatrix(["v1", "v2"], ["LoRa"], [60, 300])
        →  [("v1", "LoRa", 60), ("v1", "LoRa", 300),
            ("v2", "LoRa", 60), ("v2", "LoRa", 300)]
    vergleichspaare({"s2": 21.9, "s1": 21.5, "s3": 24.0}, 1.0)
        →  [("s1", "s3"), ("s2", "s3")]
    kuerzeste_route((0, 0), {"nord": (0, 10), "ost": (8, 0), "mitte": (4, 4)})
        →  (36, ("nord", "mitte", "ost"))

Im Beispiel ist ("ost", "mitte", "nord") genauso kurz, steht aber
alphabetisch hinter ("nord", "mitte", "ost").

Grenzen: firmwares, funkmodule und intervalle haben je 0 bis 20
verschiedene Einträge. messwerte hat 0 bis 300 Einträge, Werte von -40
bis 85, 0 ≤ toleranz ≤ 100. gateways hat 0 bis 8 Einträge, alle
Koordinaten sind ganze Zahlen von 0 bis 1000; zwei Gateways können am
selben Punkt hängen.

Hintergrund: In den Aufgaben 3_035 und 3_036 haben Sie alle Auswahlen
und alle Reihenfolgen selbst rekursiv aufgebaut. Das Modul itertools
hat diese Werkzeuge fertig; alle drei liefern lazy Tupel:

    from itertools import combinations, permutations, product

    list(product("ab", [1, 2]))     →  [("a", 1), ("a", 2), ("b", 1), ("b", 2)]
    list(permutations("abc"))       →  [("a", "b", "c"), ("a", "c", "b"),
                                        ("b", "a", "c"), …]   (6 Stück)
    list(permutations("abc", 2))    →  [("a", "b"), ("a", "c"), ("b", "a"), …]
    list(combinations("abcd", 2))   →  [("a", "b"), ("a", "c"), ("a", "d"),
                                        ("b", "c"), ("b", "d"), ("c", "d")]

product bildet alle Kombinationen je eines Elements aus jedem Iterable,
wie verschachtelte for-Schleifen (die letzte ändert sich am
schnellsten); product(werte, repeat=3) ist product(werte, werte,
werte). permutations liefert alle Reihenfolgen, bei denen es also auf
die Ordnung ankommt; combinations alle Auswahlen von r Elementen ohne
Wiederholung, bei denen die Ordnung egal ist. Beide halten sich an die
Reihenfolge der Eingabe: Ist sie sortiert, kommen auch die Tupel
alphabetisch sortiert heraus.

Die Anzahlen wachsen schnell: n Elemente haben n! Reihenfolgen (8! =
40 320) und n · (n - 1) / 2 Paare. Alle Reihenfolgen durchzuprobieren
geht darum nur für wenige Elemente; für die kürzeste Rundreise durch
viele Punkte kennt man kein schnelles Verfahren.
"""

from itertools import combinations, permutations, product


def testmatrix(firmwares, funkmodule, intervalle):
    """Gibt alle Testfälle (firmware, funkmodul, intervall) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def vergleichspaare(messwerte, toleranz):
    """Gibt alle Sensorpaare zurück, deren Werte sich um mehr als toleranz unterscheiden."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kuerzeste_route(lager, gateways):
    """Gibt (laenge, reihenfolge) des kürzesten Rundgangs vom Lager über alle Gateways zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(testmatrix(["v1", "v2"], ["LoRa"], [60, 300]))
print(vergleichspaare({"s2": 21.9, "s1": 21.5, "s3": 24.0}, 1.0))
print(kuerzeste_route((0, 0), {"nord": (0, 10), "ost": (8, 0), "mitte": (4, 4)}))
