"""Aufgabe 2_044 – Testreihenfolgen                              Stufe 2 ★★☆☆☆

Eine Testsuite sollte in jeder Reihenfolge dasselbe Ergebnis liefern.
Manchmal hängt ein Test aber heimlich von einem anderen ab, etwa weil
der erste eine Datei anlegt, die der zweite braucht. Das Qualitätsteam
überlegt, ob es alle Reihenfolgen durchprobieren kann. Bei n Tests gibt
es dafür n Möglichkeiten für den ersten Test, dann n - 1 für den zweiten
und so weiter, zusammen n! = n · (n - 1) · … · 2 · 1 Reihenfolgen
(gesprochen „n Fakultät“). Für 0 Tests gibt es genau eine Reihenfolge,
die leere: 0! = 1.

Vervollständigen Sie die Funktion `reihenfolgen(n)`, die n! zurückgibt.
Schreiben Sie sie rekursiv, also ohne for, ohne while und ohne
math.factorial (siehe Hintergrund).

    reihenfolgen(3)   →  6
    reihenfolgen(4)   →  24
    reihenfolgen(1)   →  1
    reihenfolgen(0)   →  1

Grenzen: n ist eine ganze Zahl mit 0 ≤ n ≤ 300.

Hintergrund: Eine Funktion darf sich selbst aufrufen; das nennt man
Rekursion. Sie lohnt sich, wenn sich eine Aufgabe auf eine kleinere
Aufgabe derselben Art zurückführen lässt. Hier gilt n! = n · (n - 1)!:
Wer weiß, wie viele Reihenfolgen 3 Tests haben, muss für 4 Tests nur
noch mit 4 malnehmen. Jede rekursive Funktion braucht zwei Teile:

- die Abbruchbedingung: ein kleinster Fall, dessen Antwort man direkt
  kennt, hier n == 0 mit dem Ergebnis 1;
- den rekursiven Aufruf mit einem kleineren Wert, hier n - 1.

Ein Beispiel, das die Zahlen von 1 bis n addiert:

    def summe_bis(n):
        if n == 0:
            return 0                      # Abbruchbedingung
        return n + summe_bis(n - 1)       # kleineres Teilproblem

    summe_bis(3)  →  3 + summe_bis(2)  →  3 + 2 + summe_bis(1)  →  … →  6

Jeder Aufruf wartet, bis der innere fertig ist; Python merkt sich die
wartenden Aufrufe im Aufrufstapel. Fehlt die Abbruchbedingung, ruft sich
die Funktion immer weiter auf, bis Python nach etwa 1000 Ebenen mit
einem RecursionError abbricht.
"""


def reihenfolgen(n):
    """Gibt die Anzahl der Reihenfolgen von n Tests zurück, also n!."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(reihenfolgen(4))
