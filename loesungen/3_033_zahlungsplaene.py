# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_033_zahlungsplaene.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_033_zahlungsplaene

"""Aufgabe 3_033 – Zahlungspläne                                 Stufe 3 ★★★☆☆

Ein Systemhaus vermietet Server an kleine Firmen. Die Miete läuft über eine
feste Zahl von Monaten, und die Kundin darf selbst einteilen, wie sie zahlt:
Jede Zahlung deckt entweder einen Monat oder zwei Monate auf einmal ab. Bei
drei Monaten gibt es drei Zahlungspläne:

    1 + 1 + 1
    1 + 2
    2 + 1

Für die Vertragssoftware soll eine Funktion ausrechnen, wie viele
verschiedene Zahlungspläne es für eine Laufzeit gibt. Überlegen Sie: Die
erste Zahlung deckt einen Monat ab (dann bleiben monate - 1 Monate übrig)
oder zwei (dann bleiben monate - 2). Die Zahl der Pläne ist also die Summe
der Pläne für diese beiden kürzeren Laufzeiten. Für 0 Monate gibt es genau
einen Plan (nichts zahlen), für 1 Monat ebenfalls einen.

Vervollständigen Sie die rekursive Funktion
`zahlungsplaene(monate, merker=None)`. Damit sie auch bei langen Laufzeiten
sofort fertig ist, merkt sie sich jedes Zwischenergebnis im Dictionary
merker und rechnet keine Laufzeit zweimal aus.

    zahlungsplaene(3)   →  3
    zahlungsplaene(4)   →  5
    zahlungsplaene(0)   →  1
    zahlungsplaene(60)  →  2504730781961

Grenzen: monate ist eine ganze Zahl mit 0 ≤ monate ≤ 90. Für eine Laufzeit
von n Monaten darf Ihre Funktion sich selbst nur O(n)-mal aufrufen.

Hintergrund: Die Rechnung oben ist dieselbe wie bei den Fibonacci-Zahlen
(nach MIT 6.0001, Lecture 6): f(n) = f(n - 1) + f(n - 2). Schreibt man das
direkt als Rekursion hin (Aufgabe 3_005), wird es schnell sehr langsam,
weil dieselben Werte immer wieder ausgerechnet werden. f(5) braucht f(4)
und f(3), f(4) braucht noch einmal f(3), und so weiter; die Zahl der
Aufrufe wächst ungefähr wie 1,6 hoch n. Für 60 Monate wären es mehrere
Billionen.

Die Abhilfe heißt Memoisierung: Man speichert jedes fertige Ergebnis in
einem Dictionary, mit dem Argument als Schlüssel. Bevor die Funktion
rechnet, schaut sie nach, ob das Ergebnis schon da ist:

    def f(n, merker=None):
        if merker is None:
            merker = {}
        if n in merker:
            return merker[n]
        ...                       # rechnen, dabei f(..., merker) aufrufen
        merker[n] = ergebnis
        return ergebnis

Wichtig ist, dass alle rekursiven Aufrufe dasselbe Dictionary bekommen;
darum wird merker weitergereicht. So wird jeder Wert von 0 bis n nur
einmal berechnet, und die Funktion braucht O(n) Aufrufe. Der Standardwert
None statt {} hat einen Grund: Ein {} im Funktionskopf würde nur einmal
angelegt und von allen späteren Aufrufen geteilt.
"""


def zahlungsplaene(monate, merker=None):
    """Gibt die Zahl der Zahlungspläne für monate Monate zurück (Zahlungen über einen oder zwei Monate)."""
    if merker is None:
        merker = {}
    if monate <= 1:
        return 1
    if monate in merker:
        return merker[monate]
    ergebnis = zahlungsplaene(monate - 1, merker) + zahlungsplaene(monate - 2, merker)
    merker[monate] = ergebnis
    return ergebnis


print(zahlungsplaene(3))
print(zahlungsplaene(10))


# Idee: Fehlt der Merker, legt die Funktion ein leeres Dictionary an. Für 0 und 1 Monat ist das Ergebnis
# 1. Sonst schaut sie in merker nach; steht monate dort schon, gibt sie den Wert zurück. Nur wenn nicht,
# rechnet sie zahlungsplaene(monate - 1, merker) + zahlungsplaene(monate - 2, merker), speichert das in
# merker[monate] und gibt es zurück.
# Anderer Weg: ohne Merker direkt rekursiv rechnen. Das ist richtig, aber die Zahl der Aufrufe wächst wie
# 1,6 hoch n, also exponentiell; schon für 40 Monate sind es über 300 Millionen. Ganz ohne Rekursion geht
# es mit einer Schleife, die von unten zählt und sich nur die letzten beiden Werte merkt; das ist die
# Vergleichslösung in den Tests. Fertig zum Zwischenspeichern gibt es functools.cache (Aufgabe 4_025).
# Typische Fehler: merker beim rekursiven Aufruf nicht weiterreichen (dann legt jeder Aufruf ein neues,
# leeres Dictionary an, und nichts ist gewonnen), das Ergebnis nicht in merker eintragen, merker={} im
# Funktionskopf, oder als Abbruch nur monate == 0 prüfen (bei 1 folgt dann zahlungsplaene(-1)).
# Laufzeit: O(n). Jeder Wert von 2 bis n wird einmal berechnet; jede Berechnung ruft zwei Werte auf, von
# denen der zweite schon im Merker steht. Ohne Merker wären es O(1,6 hoch n) Aufrufe.
