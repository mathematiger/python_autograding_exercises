"""Aufgabe 5_060 – Syntaxbaum                                    Stufe 5 ★★★★★

Ein Werkzeug zur Codequalität zerlegt Quelltext in einen Syntaxbaum:
Jeder Knoten ist ein Stück Code (eine Funktion, eine Anweisung, ein
Ausdruck), seine Kinder sind die Stücke, aus denen er besteht. Für jeden
Knoten kennt das Werkzeug außerdem, wie viele Zeichen Code zu ihm
selbst gehören. Daraus berechnet es Kennzahlen: wie tief der Code
verschachtelt ist, in welcher Reihenfolge die Knoten im Quelltext
stehen und wie viele Zeichen jeder Teilbaum umfasst. Die rekursiven
Funktionen dafür sind vorgegeben und funktionieren für normalen Code.
Dann lief das Werkzeug über eine maschinell erzeugte Datei mit einem
Ausdruck wie a + (b + (c + (…))) über 50 000 Ebenen und brach mit
RecursionError ab (siehe Hintergrund).

Der Baum ist ein Dictionary kinder: Knoten → Liste seiner Kinder in der
Reihenfolge im Quelltext; ein Knoten, der dort nicht vorkommt, hat keine
Kinder. Schreiben Sie ohne Rekursion, mit einem eigenen Stapel:

- `tiefe(wurzel, kinder)` gibt die Anzahl der Ebenen zurück, also wie
  `tiefe_rekursiv` (ein Knoten ohne Kinder hat Tiefe 1).
- `reihenfolge(wurzel, kinder)` gibt die Knoten in derselben Reihenfolge
  zurück wie `reihenfolge_rekursiv`: jeden Knoten vor seinen Kindern, die
  Kinder in ihrer Reihenfolge, jedes mit allem darunter.
- `teilbaumgroessen(wurzel, kinder, zeichen)` gibt wie
  `teilbaumgroessen_rekursiv` ein Dictionary Knoten → Summe von zeichen
  über den Knoten und alle Knoten darunter zurück.
- `rekursion_reicht(wurzel, kinder)` gibt True zurück, wenn die
  rekursiven Funktionen für diesen Baum sicher nicht am Rekursionslimit
  scheitern: wenn tiefe(wurzel, kinder) + 50 höchstens
  sys.getrecursionlimit() ist (50 Rahmen Reserve für alles, was beim
  Aufruf schon auf dem Stapel liegt).

    kinder = {"modul": ["def f", "def g"], "def f": ["return"],
              "return": ["a + b"], "def g": ["pass"]}
    zeichen = {"modul": 0, "def f": 8, "return": 7, "a + b": 5, "def g": 8, "pass": 4}
    tiefe("modul", kinder)                    →  4
    reihenfolge("modul", kinder)              →  ["modul", "def f", "return", "a + b",
                                                  "def g", "pass"]
    teilbaumgroessen("modul", kinder, zeichen)["def f"]   →  20
    rekursion_reicht("modul", kinder)         →  True

Verändern Sie sys.setrecursionlimit nicht.

Grenzen: Der Baum hat 1 bis 200 000 Knoten (Texte, verschieden) und
kann bis zu 200 000 Ebenen tief sein; kinder enthält nur Knoten, die von
wurzel aus erreichbar sind, jeder Knoten außer wurzel ist Kind genau
eines Knotens, es gibt keine Kreise. zeichen enthält jeden Knoten des
Baums mit einer ganzen Zahl von 0 bis 10**6. Alle vier Funktionen sollen
O(n) Schritte brauchen.

Hintergrund: Jeder Funktionsaufruf legt einen Rahmen (frame) auf den
Aufrufstapel (call stack): Er enthält die lokalen Variablen und die
Stelle, an der es nach der Rückkehr weitergeht. Kehrt die Funktion
zurück, wird ihr Rahmen wieder entfernt. Bei Rekursion (Aufgaben 2_044
und 3_059) liegt für jede Ebene ein Rahmen auf dem Stapel, bei einem
Baum mit 50 000 Ebenen also 50 000 Rahmen gleichzeitig. Damit ein
Programm mit endloser Rekursion nicht den ganzen Speicher füllt, setzt
Python eine Grenze, das Rekursionslimit, meist 1000:

    import sys
    sys.getrecursionlimit()          # 1000

    def runter(n):
        return 0 if n == 0 else runter(n - 1)

    runter(500)                      # 0
    runter(5000)                     # RecursionError: maximum recursion depth exceeded

Man kann die Grenze mit sys.setrecursionlimit erhöhen, aber das löst
das Problem nicht: Die Rahmen liegen auch auf dem Stapel des
Betriebssystems, der nur ein paar Megabyte groß ist, und ist er voll,
stürzt Python ohne Fehlermeldung ab (Segmentation fault). Python
optimiert auch keine Endrekursion, wie es manche andere Sprachen tun.

Die sichere Lösung ist, den Stapel selbst zu verwalten: eine Liste, auf
die man mit append legt, was noch zu tun ist, und mit pop das Oberste
wieder herunternimmt (Aufgabe 3_056). Die Schleife läuft, bis der
Stapel leer ist. Statt sich für jedes Kind selbst aufzurufen, legt die
Funktion jedes Kind auf den Stapel:

    def zaehle(wurzel, kinder):
        anzahl = 0
        stapel = [wurzel]
        while stapel:
            knoten = stapel.pop()
            anzahl += 1
            stapel.extend(kinder.get(knoten, []))
        return anzahl

Was die Rekursion in lokalen Variablen jeder Ebene mitführt (etwa die
aktuelle Tiefe), legt man mit auf den Stapel, als Tupel
(knoten, ebene). Zwei Dinge werden dabei anders als bei der Rekursion.
Erstens die Reihenfolge: pop nimmt das zuletzt Hingelegte, also kommt
von den Kindern das letzte zuerst dran; wer die Reihenfolge der
Rekursion will, legt sie umgekehrt hin (reversed). Zweitens Ergebnisse,
die erst feststehen, wenn alle Kinder fertig sind, wie die Summe eines
Teilbaums: Die Rekursion rechnet sie beim Zurückkehren aus. Ohne
Rekursion geht man zum Beispiel die Knoten erst in der Reihenfolge von
oben nach unten durch und rechnet die Summen danach rückwärts: Wenn ein
Knoten an die Reihe kommt, sind alle Knoten darunter schon fertig. Die
Tiefe des eigenen Stapels ist nur durch den Arbeitsspeicher begrenzt.
"""

import sys


def tiefe_rekursiv(wurzel, kinder):
    """Gibt die Anzahl der Ebenen unter wurzel zurück (rekursiv)."""
    hoechste = 0
    for kind in kinder.get(wurzel, []):
        hoechste = max(hoechste, tiefe_rekursiv(kind, kinder))
    return hoechste + 1


def reihenfolge_rekursiv(wurzel, kinder):
    """Gibt die Knoten von oben nach unten zurück, jeden vor seinen Kindern (rekursiv)."""
    knoten = [wurzel]
    for kind in kinder.get(wurzel, []):
        knoten.extend(reihenfolge_rekursiv(kind, kinder))
    return knoten


def teilbaumgroessen_rekursiv(wurzel, kinder, zeichen, ergebnis=None):
    """Gibt zu jedem Knoten die Summe von zeichen über seinen Teilbaum zurück (rekursiv)."""
    if ergebnis is None:
        ergebnis = {}
    summe = zeichen[wurzel]
    for kind in kinder.get(wurzel, []):
        teilbaumgroessen_rekursiv(kind, kinder, zeichen, ergebnis)
        summe += ergebnis[kind]
    ergebnis[wurzel] = summe
    return ergebnis


def tiefe(wurzel, kinder):
    """Gibt die Anzahl der Ebenen unter wurzel zurück, mit eigenem Stapel."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def reihenfolge(wurzel, kinder):
    """Gibt die Knoten von oben nach unten zurück, jeden vor seinen Kindern, mit eigenem Stapel."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def teilbaumgroessen(wurzel, kinder, zeichen):
    """Gibt zu jedem Knoten die Summe von zeichen über seinen Teilbaum zurück, ohne Rekursion."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def rekursion_reicht(wurzel, kinder):
    """Gibt True zurück, wenn die Tiefe des Baums plus 50 das Rekursionslimit nicht übersteigt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kinder = {"modul": ["def f", "def g"], "def f": ["return"], "return": ["a + b"], "def g": ["pass"]}
zeichen = {"modul": 0, "def f": 8, "return": 7, "a + b": 5, "def g": 8, "pass": 4}
print(tiefe("modul", kinder), reihenfolge("modul", kinder))
print(teilbaumgroessen("modul", kinder, zeichen), rekursion_reicht("modul", kinder))
