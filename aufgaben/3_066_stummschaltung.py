"""Aufgabe 3_066 – Stummschaltung                                Stufe 3 ★★★☆☆

Während einer geplanten Wartung soll das Überwachungssystem eines
Rechenzentrums keine Alarme schicken, sonst klingelt mitten in der Nacht
das Telefon der Bereitschaft. Die Oberfläche bietet dafür nur feste
Schaltflächen: „60 Min.“, „30 Min.“, „10 Min.“, „5 Min.“ und „1 Min.“.
Jeder Klick verlängert die Stummschaltung um diese Zeit, jede Schaltfläche
darf beliebig oft geklickt werden. Ein Skript soll die Klicks für genau
d Minuten erzeugen, und zwar mit möglichst wenigen Klicks. Das ist
dasselbe Problem wie beim Wechselgeld: einen Betrag aus möglichst wenigen
Münzen zusammensetzen.

Die Zeitstufen stehen in einer Liste stufen. Schreiben Sie zwei
Funktionen:

- `gierig(minuten, stufen)` stückelt minuten gierig: so oft wie möglich
  die größte Stufe, mit dem Rest so oft wie möglich die nächstkleinere
  und so weiter. Sie gibt eine Liste von Tupeln (stufe, anzahl) zurück,
  von der größten Stufe zur kleinsten, nur mit Stufen, die mindestens
  einmal geklickt werden. Die Liste stufen soll unverändert bleiben.

- `gegenbeispiel(stufen, bis)` sucht das kleinste d mit 1 ≤ d ≤ bis, bei
  dem gierig mehr Klicks braucht als nötig, und gibt es zurück. Gibt es
  keins, gibt sie None zurück. Die wenigsten möglichen Klicks liefert die
  vorgegebene Funktion `wenigste_klicks(bis, stufen)`: Sie gibt eine
  Liste beste zurück, in der beste[d] die kleinste Zahl von Klicks für
  genau d Minuten ist (für alle d von 0 bis bis).

    gierig(75, [60, 30, 10, 5, 1])     →  [(60, 1), (10, 1), (5, 1)]
    gierig(137, [60, 30, 10, 5, 1])    →  [(60, 2), (10, 1), (5, 1), (1, 2)]
    gierig(30, [25, 15, 1])            →  [(25, 1), (1, 5)]
    gegenbeispiel([60, 30, 10, 5, 1], 1000)  →  None
    gegenbeispiel([25, 15, 1], 100)          →  30

Bei den Stufen 25, 15 und 1 Minute stückelt gierig 30 Minuten in sechs
Klicks (25 + 1 + 1 + 1 + 1 + 1), dabei reichen zwei (15 + 15).

Grenzen: 0 ≤ minuten ≤ 10**9 und 1 ≤ bis ≤ 10 000, beides ganze Zahlen.
stufen enthält 1 bis 10 verschiedene ganze Zahlen mit
1 ≤ stufe ≤ 1000 in beliebiger Reihenfolge, und 1 ist immer dabei
(darum lässt sich jede Minutenzahl zusammensetzen). gierig soll nur
O(k log k) Schritte brauchen, wobei k die Zahl der Stufen ist, egal wie
groß minuten ist: Ziehen Sie eine Stufe also nicht einzeln immer wieder
ab, sondern rechnen Sie mit // und %.

Hintergrund: In Aufgabe 3_065 hat ein Greedy-Verfahren („gierig“) die
meisten Termine gefunden: Es nimmt bei jedem Schritt das, was im Moment
am besten aussieht, und nimmt das nie zurück. Hier heißt „am besten“:
die größte Stufe, die noch passt. Wie oft sie passt und was übrig
bleibt, liefern die Ganzzahldivision und der Rest (Aufgabe 1_005):
137 // 60 ist 2, 137 % 60 ist 17, und mit den 17 Minuten geht es bei der
nächstkleineren Stufe weiter.

Bei den Euromünzen und bei Stufen wie 60, 30, 10, 5, 1 liefert gierig
immer die wenigsten Stücke. Das liegt an den Werten, nicht am Verfahren:
Bei den Stufen 4, 3 und 1 nimmt gierig für 6 Minuten 4 + 1 + 1, also
drei Klicks, obwohl 3 + 3 mit zwei auskommt. Der große erste Schritt
verbaut einen besseren Weg, und gierig korrigiert sich nie. Ein Greedy-
Verfahren ist also nur dann richtig, wenn man es begründen kann (wie in
Aufgabe 3_065); sonst testet man es gegen eine sichere, langsamere
Lösung. Genau das tut gegenbeispiel. Wie wenigste_klicks die beste
Anzahl findet, ist Thema der nächsten Aufgabe; hier benutzen Sie die
Funktion nur.

Tipp: sorted(stufen, reverse=True) liefert die Stufen von groß nach
klein, ohne die Liste stufen zu verändern. Die Zahl der Klicks einer
gierigen Stückelung ist die Summe der Anzahlen.
"""


def wenigste_klicks(bis, stufen):
    """Gibt eine Liste beste zurück: beste[d] ist die kleinste Zahl von Klicks für genau d Minuten."""
    beste = [0] * (bis + 1)
    for d in range(1, bis + 1):
        kandidaten = []
        for stufe in stufen:
            if stufe <= d:
                kandidaten.append(beste[d - stufe] + 1)
        beste[d] = min(kandidaten)
    return beste


def gierig(minuten, stufen):
    """Stückelt minuten gierig; gibt Tupel (stufe, anzahl) von der größten zur kleinsten Stufe zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gegenbeispiel(stufen, bis):
    """Gibt das kleinste d bis bis zurück, bei dem gierig mehr Klicks braucht als nötig, sonst None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(gierig(75, [60, 30, 10, 5, 1]))
print(gegenbeispiel([25, 15, 1], 100))
