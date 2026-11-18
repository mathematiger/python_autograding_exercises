"""Aufgabe 2_044 – Testreihenfolgen                              Stufe 2 ★★☆☆☆

Ein Entwicklungsteam hat einen hartnäckigen Fehler: Die automatischen
Tests laufen einzeln alle durch, zusammen aber manchmal nicht. Vermutlich
hinterlässt ein Test Daten, über die ein späterer stolpert, und es kommt
auf die Reihenfolge an. Bevor das Team alle Reihenfolgen durchprobieren
lässt, will es wissen, wie viele das sind. Bei n Tests kann jeder der n
Tests als erster laufen, danach bleiben n - 1 Tests in beliebiger
Reihenfolge übrig. Die Anzahl ist also n · (n - 1) · … · 2 · 1, die
Fakultät von n, geschrieben n!. Für 0 Tests gibt es genau eine
Reihenfolge, die leere, also ist 0! = 1.

Vervollständigen Sie die Funktion `reihenfolgen(n)`, die n! zurückgibt.
Lösen Sie die Aufgabe rekursiv: Die Funktion ruft sich selbst auf, ohne
Schleife und ohne math.factorial.

    reihenfolgen(3)   →  6       (ABC, ACB, BAC, BCA, CAB, CBA)
    reihenfolgen(5)   →  120
    reihenfolgen(1)   →  1
    reihenfolgen(0)   →  1

Grenzen: n ist eine ganze Zahl mit 0 ≤ n ≤ 500. Python rechnet mit
beliebig großen ganzen Zahlen; 500! hat 1135 Ziffern.

Hintergrund: Eine Funktion darf sich selbst aufrufen; das nennt man
Rekursion (MIT 6.0001, Lecture 6). Das klappt, wenn man ein Problem auf
ein kleineres Problem derselben Art zurückführen kann. Hier gilt
n! = n · (n - 1)!: Wer (n - 1)! kennt, muss nur noch mit n malnehmen.
Damit das nicht endlos weitergeht, braucht jede Rekursion eine
Abbruchbedingung, einen kleinsten Fall, den man ohne weiteren Aufruf
beantwortet. Am Beispiel der Summe 1 + 2 + … + n:

    def summe_bis(n):
        if n == 0:                      # Abbruchbedingung
            return 0
        return n + summe_bis(n - 1)     # kleineres Problem derselben Art

summe_bis(3) ruft summe_bis(2) auf, das summe_bis(1), das summe_bis(0).
Erst summe_bis(0) liefert sofort 0; dann rechnen die wartenden Aufrufe
rückwärts fertig: 1 + 0, 2 + 1, 3 + 3, Ergebnis 6. Fehlt die
Abbruchbedingung, ruft sich die Funktion immer weiter auf, bis Python
mit einem RecursionError abbricht.
"""


def reihenfolgen(n):
    """Gibt n! zurück, die Anzahl der Reihenfolgen von n Tests, rekursiv berechnet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(reihenfolgen(3), reihenfolgen(5))
