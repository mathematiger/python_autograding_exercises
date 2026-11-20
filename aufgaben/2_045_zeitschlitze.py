"""Aufgabe 2_045 – Zeitschlitze                                  Stufe 2 ★★☆☆☆

Funksensoren in einer Fabrikhalle teilen sich einen Funkkanal. Damit sich
ihre Nachrichten nicht überlagern, ist jeder Sendezyklus in n gleich
lange Zeitschlitze eingeteilt. Eine kurze Nachricht (ein Messwert)
belegt einen Zeitschlitz, eine lange Nachricht (ein Statusbericht) zwei
aufeinanderfolgende. Der Planer möchte wissen, wie viele verschiedene
Belegungen eines Zyklus es gibt, bei denen alle Schlitze belegt sind.
Bei n = 3 gibt es drei: kurz-kurz-kurz, kurz-lang und lang-kurz.

Überlegen Sie für den ersten Schlitz: Beginnt der Zyklus mit einer
kurzen Nachricht, bleiben n - 1 Schlitze übrig, beginnt er mit einer
langen, bleiben n - 2. Also ist die Zahl der Belegungen von n die Summe
der Belegungen von n - 1 und von n - 2. Für 0 Schlitze gibt es genau
eine Belegung (die leere), für einen Schlitz auch genau eine.

Schreiben Sie die Anzahl zweimal:

- `belegungen_rekursiv(n)` rekursiv nach dieser Überlegung, ohne for und
  ohne while.
- `belegungen_schleife(n)` mit einer Schleife, ohne sich selbst
  aufzurufen. Sie muss auch große n schnell schaffen (siehe Hintergrund).

    belegungen_rekursiv(3)   →  3
    belegungen_rekursiv(4)   →  5
    belegungen_schleife(10)  →  89

Grenzen: Für belegungen_rekursiv ist n eine ganze Zahl mit 0 ≤ n ≤ 20,
für belegungen_schleife eine mit 0 ≤ n ≤ 5000. belegungen_schleife soll
für n nur etwa n Schleifendurchläufe brauchen.

Hintergrund: Die Zahlen 1, 1, 2, 3, 5, 8, 13, … heißen Fibonacci-Zahlen:
Jede ist die Summe der beiden davor. Rekursiv sieht das genauso aus wie
die Regel, nur braucht es zwei Abbruchbedingungen, weil der Aufruf zwei
kleinere Fälle braucht (wie Rekursion grundsätzlich funktioniert, steht
in Aufgabe 2_044):

    def fib(n):
        if n <= 1:
            return 1
        return fib(n - 1) + fib(n - 2)

Das ist kurz, aber langsam: fib(5) ruft fib(4) und fib(3) auf, fib(4)
ruft noch einmal fib(3) auf, und so weiter. Dieselben Werte werden immer
wieder neu berechnet; die Zahl der Aufrufe wächst mit jedem n um etwa
den Faktor 1,6. Für n = 20 sind es über 20 000 Aufrufe, für n = 50
wären es über 40 Milliarden.

Eine Schleife rechnet von unten nach oben und merkt sich nur die beiden
letzten Werte. Dafür braucht sie für n nur n Durchläufe:

    vorletzte, letzte = 1, 1
    for _ in range(n - 1):
        vorletzte, letzte = letzte, vorletzte + letzte

Die Zeile mit dem Komma weist zwei Variablen gleichzeitig zu; rechts
werden erst beide Werte ausgerechnet, dann links beide gesetzt.
"""


def belegungen_rekursiv(n):
    """Gibt die Zahl der Belegungen von n Zeitschlitzen zurück, rekursiv berechnet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def belegungen_schleife(n):
    """Gibt die Zahl der Belegungen von n Zeitschlitzen zurück, mit einer Schleife berechnet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(belegungen_rekursiv(4))
print(belegungen_schleife(10))
