"""Aufgabe 3_033 – Prozessvarianten                              Stufe 3 ★★★☆☆

Ein Versicherer analysiert seinen Freigabeprozess für Schadensmeldungen. Der
Prozess besteht aus n Prüfschritten, die in fester Reihenfolge erledigt werden.
Eine Sachbearbeiterin erledigt in einem Arbeitsgang einen, zwei oder drei
aufeinanderfolgende Schritte, dann geht die Akte weiter. Für eine Simulation
will die Prozessanalyse wissen, wie viele verschiedene Abläufe es gibt, also
wie viele Möglichkeiten, die n Schritte in Arbeitsgänge zu zerlegen. Bei drei
Schritten sind es vier: 1+1+1, 1+2, 2+1 und 3.

Schreiben Sie die Funktion `varianten(n, merker=None)`. Sie soll rekursiv
arbeiten: Der erste Arbeitsgang umfasst 1, 2 oder 3 Schritte, danach bleiben
n - 1, n - 2 oder n - 3 Schritte übrig, und für jeden Rest zählt man die
Varianten mit demselben Verfahren. Für 0 Schritte gibt es genau eine Variante
(nichts tun), für eine negative Zahl keine. Damit das auch für große n schnell
geht, merkt sich die Funktion jedes Ergebnis im Dictionary merker (Schlüssel n,
Wert die Anzahl) und berechnet nichts doppelt. Wird merker nicht übergeben,
legt die Funktion ein neues, leeres Dictionary an.

    varianten(3)   →  4
    varianten(4)   →  7
    varianten(10)  →  274
    merker = {}
    varianten(5, merker)
    merker[5]      →  13

Grenzen: 0 ≤ n ≤ 300. Ihre Lösung soll O(n) Schritte brauchen, also jedes
Teilergebnis nur einmal berechnen. Nach varianten(n, merker) steht für jede
Zahl k von 1 bis n, deren Ergebnis berechnet wurde, varianten(k) unter dem
Schlüssel k in merker, mindestens aber für k = n.

Hintergrund: Die Rekursion (Aufgabe 3_005) varianten(n) = varianten(n - 1) +
varianten(n - 2) + varianten(n - 3) ist richtig, aber ohne Gedächtnis sehr
langsam: varianten(n - 1) berechnet varianten(n - 2) noch einmal, beide
berechnen varianten(n - 3) und so weiter. Die Anzahl der Aufrufe wächst
exponentiell, schon bei n = 35 sind es über eine Milliarde. Bei
Memoisierung (von englisch memo, Notiz) legt man jedes Ergebnis in einem
Dictionary ab und schaut zuerst dort nach, bevor man rechnet:

    def fib(n, merker):
        if n <= 1:
            return n
        if n in merker:
            return merker[n]
        ergebnis = fib(n - 1, merker) + fib(n - 2, merker)
        merker[n] = ergebnis
        return ergebnis

Jedes n wird jetzt nur einmal wirklich berechnet, alle weiteren Aufrufe sind
ein Nachschlagen in O(1). Das Dictionary muss bei allen rekursiven Aufrufen
dasselbe sein, deshalb wird es als Argument weitergereicht. Als Standardwert
nimmt man None und legt das Dictionary erst in der Funktion an
(if merker is None: merker = {}); warum merker={} als Standardwert eine Falle
sein kann, kommt in Stufe 4.
"""


def varianten(n, merker=None):
    """Gibt die Anzahl der Möglichkeiten zurück, n Schritte in Arbeitsgänge zu 1, 2 oder 3 Schritten zu zerlegen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(varianten(3))
print(varianten(10))
