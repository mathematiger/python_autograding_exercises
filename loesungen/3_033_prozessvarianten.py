# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_033_prozessvarianten.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_033_prozessvarianten

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
    if merker is None:
        merker = {}
    if n < 0:
        return 0
    if n == 0:
        return 1
    if n in merker:
        return merker[n]
    ergebnis = varianten(n - 1, merker) + varianten(n - 2, merker) + varianten(n - 3, merker)
    merker[n] = ergebnis
    return ergebnis


print(varianten(3))
print(varianten(10))


# Idee: Die Rekursion folgt dem ersten Arbeitsgang: 1, 2 oder 3 Schritte, danach der Rest. Abbruch bei
# n == 0 (eine Variante) und n < 0 (keine). Vor dem Rechnen wird im merker nachgeschlagen, nach dem Rechnen
# wird das Ergebnis dort abgelegt; derselbe merker wird an alle rekursiven Aufrufe weitergereicht.
#
# Anderer Weg: Die Tabelle von unten füllen, ganz ohne Rekursion: [1, 1, 2] und dann immer die Summe der
# letzten drei anhängen. Das ist ebenfalls O(n) und stößt nicht an die Rekursionsgrenze von Python. Der
# naive rekursive Weg ohne merker braucht etwa 1,84 hoch n Aufrufe, also exponentiell viele.
#
# Typische Fehler: merker nicht an die rekursiven Aufrufe weitergeben (dann hat jeder Aufruf ein neues,
# leeres Dictionary und nichts wird gespart), das Ergebnis nicht speichern, varianten(0) = 0 statt 1 oder
# merker = {} ohne if merker is None (dann wird ein übergebenes Dictionary ignoriert).
#
# Laufzeit: O(n). Jedes k von 1 bis n wird einmal berechnet, mit drei Aufrufen, die danach nur noch
# nachschlagen (O(1) im Dictionary).
