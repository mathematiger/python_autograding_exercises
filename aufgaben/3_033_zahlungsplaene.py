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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(zahlungsplaene(3))
print(zahlungsplaene(10))
