"""Aufgabe 3_005 – Sensordaten mit Merge Sort                    Stufe 3 ★★★☆☆

In einer Werkhalle melden viele Funksensoren ihre Messwerte an ein Gateway,
einen kleinen Rechner, der die Nachrichten sammelt und weiterleitet. Jede
Nachricht trägt einen Zeitstempel in Sekunden. Weil die Funkstrecken
unterschiedlich schnell sind, kommen die Nachrichten oft in falscher
Reihenfolge an. Bevor das Gateway sie weiterleitet, sollen die Zeitstempel
aufsteigend sortiert werden. Weil es Tausende Nachrichten pro Minute sind,
reicht ein O(n²)-Verfahren wie Bubble Sort nicht; Sie schreiben Merge Sort.

- `zusammenfuehren(links, rechts)` bekommt zwei schon sortierte Listen und
  gibt eine neue sortierte Liste mit allen Elementen beider Listen zurück.
- `merge_sort(werte)` gibt eine neue, aufsteigend sortierte Liste zurück und
  lässt werte unverändert. Die Funktion ruft sich selbst auf und benutzt
  zusammenfuehren(...).

    zusammenfuehren([3, 8, 9], [1, 8, 12])  →  [1, 3, 8, 8, 9, 12]
    zusammenfuehren([], [4, 5])             →  [4, 5]
    merge_sort([17, 3, 12, 3, 8])           →  [3, 3, 8, 12, 17]
    merge_sort([])                          →  []

Benutzen Sie nicht sorted(...) oder liste.sort().

Grenzen: 0 ≤ len(werte) ≤ 50 000; links und rechts haben zusammen
höchstens 50 000 Elemente und sind aufsteigend sortiert. Die Zeitstempel
sind ganze Zahlen von 0 bis 2 · 10**9, gleiche Zeitstempel dürfen mehrmals
vorkommen. merge_sort soll O(n log n) Schritte brauchen, zusammenfuehren
O(n), wobei n die Zahl aller Elemente ist.

Hintergrund: Merge Sort („Sortieren durch Zusammenführen“) arbeitet nach dem
Prinzip „Teile und herrsche“: Eine Liste mit höchstens einem Element ist
schon sortiert, das ist die Abbruchbedingung der Rekursion. Jede längere
Liste teilt man in der Mitte, sortiert beide Hälften rekursiv mit Merge Sort
und führt die sortierten Hälften zusammen:

    [17, 3, 12, 8]
    teilen:          [17, 3]          [12, 8]
    teilen:       [17]    [3]      [12]    [8]
    zusammenführen:  [3, 17]          [8, 12]
    zusammenführen:       [3, 8, 12, 17]

Das Zusammenführen zweier sortierter Listen geht in einem Durchgang: Zwei
Zeiger i und j stehen am Anfang von links und rechts. Man vergleicht
links[i] mit rechts[j], hängt den kleineren Wert an das Ergebnis und rückt
nur bei dieser Liste weiter. Ist eine Liste aufgebraucht, hängt man den Rest
der anderen an (mit Slicing: links[i:]). Die Liste wird etwa log₂(n)-mal
halbiert, und auf jeder Ebene werden insgesamt n Elemente zusammengeführt.
Merge Sort braucht also O(n · log n) Schritte, auch im schlechtesten Fall.
Für eine Million Elemente sind das etwa 20 Millionen statt einer Billion
Schritte wie bei O(n²). (Nach MIT 6.0001, Lecture 12.)

Tipp: Die Mitte ist mitte = len(werte) // 2; die Hälften sind werte[:mitte]
und werte[mitte:]. Slicing erzeugt neue Listen, werte selbst bleibt so
unverändert.
"""


def zusammenfuehren(links, rechts):
    """Gibt eine neue sortierte Liste aus den beiden sortierten Listen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def merge_sort(werte):
    """Gibt eine neue, aufsteigend sortierte Liste der Werte zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(zusammenfuehren([3, 8, 9], [1, 8, 12]))
print(merge_sort([17, 3, 12, 3, 8]))
