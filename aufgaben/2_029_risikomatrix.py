"""Aufgabe 2_029 – Risikomatrix                                  Stufe 2 ★★☆☆☆

Zu Beginn eines IT-Projekts sammelt das Team die Projektrisiken, etwa
„Lieferant liefert Server zu spät“ oder „Schlüsselperson fällt aus“.
Jedes Risiko bekommt zwei Noten von 1 bis 5: die Wahrscheinlichkeit,
dass es eintritt, und den Schaden, wenn es eintritt. In einer
Risikomatrix, einem Raster mit 5 × 5 Feldern, steht jedes Risiko im
Feld (Wahrscheinlichkeit, Schaden). Das Produkt der beiden Noten ist
die Risikozahl des Felds; Felder mit hoher Risikozahl brauchen sofort
Gegenmaßnahmen. Schreiben Sie zwei Funktionen:

- `matrix(risiken)` bekommt eine Liste von Tupeln (name,
  wahrscheinlichkeit, schaden) und gibt ein Dictionary zurück, dessen
  Schlüssel die Tupel (wahrscheinlichkeit, schaden) sind und dessen
  Werte zählen, wie viele Risiken in diesem Feld stehen. Felder ohne
  Risiko kommen nicht vor.
- `kritische_felder(raster, grenze)` bekommt ein solches Dictionary und
  gibt die sortierte Liste der Felder (wahrscheinlichkeit, schaden)
  zurück, deren Risikozahl wahrscheinlichkeit * schaden mindestens
  grenze ist.

    risiken = [("Lieferverzug", 4, 3), ("Ausfall Admin", 2, 5),
               ("Budget überzogen", 4, 3), ("Datenverlust", 1, 5)]
    raster = matrix(risiken)
    raster                       →  {(4, 3): 2, (2, 5): 1, (1, 5): 1}
    raster[(4, 3)]               →  2
    kritische_felder(raster, 10) →  [(2, 5), (4, 3)]

Grenzen: 0 ≤ len(risiken) ≤ 10 000. name ist ein nicht leerer Text,
wahrscheinlichkeit und schaden sind ganze Zahlen von 1 bis 5. Mehrere
Risiken dürfen denselben Namen haben. grenze ist eine ganze Zahl von 1
bis 25. kritische_felder bekommt nur Dictionaries, wie matrix sie
liefert.

Hintergrund: Ein Schlüssel eines Dictionaries muss unveränderlich sein
(genauer: hashbar). Zahlen und Texte sind das, Listen nicht, weil man
eine Liste nach dem Eintragen noch ändern könnte. Ein Tupel aus Zahlen
oder Texten ist unveränderlich und darf deshalb Schlüssel sein. So
beschreibt ein Tupel eine Koordinate, und das Dictionary ist ein
Raster, in dem nur die belegten Felder gespeichert sind:

    belegung = {}
    belegung[(2, 3)] = "Drucker"        # Klammern darf man auch weglassen: belegung[2, 3]
    (2, 3) in belegung                  →  True
    belegung.get((5, 5), "leer")        →  "leer"
    for (zeile, spalte), geraet in belegung.items():
        print(zeile, spalte, geraet)    # 2 3 Drucker

In der Schleife packt (zeile, spalte) den Schlüssel gleich in seine
beiden Zahlen aus. Ein Tupel (name, w, s) packt man ebenso mit
name, w, s = risiko aus. sorted sortiert Tupel wie Wörter im Lexikon:
zuerst nach dem ersten Wert, bei Gleichstand nach dem zweiten, also
(1, 5) vor (2, 1) vor (2, 4).
"""


def matrix(risiken):
    """Zählt, wie viele Risiken in jedem Feld (wahrscheinlichkeit, schaden) stehen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kritische_felder(raster, grenze):
    """Gibt die sortierten Felder zurück, deren Risikozahl mindestens grenze ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


risiken = [("Lieferverzug", 4, 3), ("Ausfall Admin", 2, 5), ("Budget überzogen", 4, 3), ("Datenverlust", 1, 5)]
raster = matrix(risiken)
print(raster)
print(kritische_felder(raster, 10))
