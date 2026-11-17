"""Aufgabe 4_032 – Gleitender Durchschnitt                       Stufe 4 ★★★★☆

Eine Druckerei misst für jeden Auftrag die Durchlaufzeit in Minuten, von
der Bestellung bis zum Versand. Einzelne Aufträge schwanken stark; um zu
sehen, ob der Prozess insgesamt schneller oder langsamer wird, betrachtet
die Prozessanalyse den gleitenden Durchschnitt: den Mittelwert von je
breite aufeinanderfolgenden Aufträgen, dann ein Auftrag weiter, und so
fort. Bei den Zeiten 4, 8, 6, 10, 2 und breite 2 sind das die
Mittelwerte von (4, 8), (8, 6), (6, 10) und (10, 2).

Die Messreihen können lang sein, und oft braucht man nur die ersten
Werte. Deshalb soll nicht vorab eine Liste aller Mittelwerte entstehen,
sondern ein Iterator, der jeden Mittelwert erst berechnet, wenn er
abgeholt wird. Vervollständigen Sie die Klasse `GleitenderSchnitt`:

- `__init__(self, zeiten, breite)` merkt sich die Liste, die Breite und
  die Stelle, an der das nächste Fenster beginnt (am Anfang 0).
- `__iter__(self)` gibt das Objekt selbst zurück.
- `__next__(self)` gibt den Mittelwert des nächsten Fensters zurück
  (Summe der breite Zeiten geteilt durch breite) und rückt um eine
  Stelle weiter. Gibt es kein vollständiges Fenster mehr, löst es
  StopIteration aus, auch bei jedem weiteren Aufruf.

    schnitt = GleitenderSchnitt([4, 8, 6, 10, 2], 2)
    next(schnitt)   →  6.0
    next(schnitt)   →  7.0
    list(schnitt)   →  [8.0, 6.0]       (nur noch, was übrig ist)
    next(schnitt)   →  StopIteration

Schreiben Sie die Klasse mit __iter__ und __next__ von Hand, ohne yield
und ohne eine fertige Liste aller Mittelwerte im Voraus.

Grenzen: 0 ≤ len(zeiten) ≤ 10 000, jede Zeit ist eine ganze Zahl von 0
bis 100 000. breite ist eine ganze Zahl mit 1 ≤ breite ≤ 100; sie darf
größer als len(zeiten) sein, dann gibt es kein einziges Fenster. Die
Liste zeiten wird nicht verändert.

Hintergrund: In Aufgabe 3_020 haben Sie gesehen, was eine for-Schleife
im Hintergrund tut: Sie ruft einmal iter(...) auf und dann so lange
next(...), bis StopIteration kommt. Diese beiden Funktionen rufen die
Methoden __iter__ und __next__ des Objekts auf. Wer sie selbst schreibt,
macht seine Klasse zum Iterator, und dann funktionieren for, list(),
sum(), zip() und alle anderen Werkzeuge mit ihr. Das ist das
Iterator-Protokoll:

- __next__ liefert den nächsten Wert und merkt sich, wie weit es ist.
  Gibt es nichts mehr, löst es StopIteration aus (raise StopIteration).
  Ein Iterator, der einmal fertig ist, bleibt fertig: Jeder weitere
  Aufruf löst wieder StopIteration aus.
- __iter__ gibt bei einem Iterator sich selbst zurück (return self).
  So kann man einen halb verbrauchten Iterator an for übergeben, und
  die Schleife macht dort weiter, wo er steht.

Ein Beispiel, ein Countdown von start bis 1:

    class Countdown:
        def __init__(self, start):
            self.aktuell = start

        def __iter__(self):
            return self

        def __next__(self):
            if self.aktuell <= 0:
                raise StopIteration
            wert = self.aktuell
            self.aktuell -= 1
            return wert

    for zahl in Countdown(3):
        print(zahl)                   # 3, 2, 1
    zaehler = Countdown(2)
    next(zaehler), next(zaehler)      →  (2, 1)
    next(zaehler)                     →  StopIteration

Der Zustand (hier aktuell, in Ihrer Aufgabe die Stelle des nächsten
Fensters) liegt im Objekt. Deshalb rechnet ein Iterator „faul“ (lazy):
Er berechnet nur, was abgeholt wird. Der Preis: Er lässt sich nur einmal
durchlaufen. Ein zweites list(schnitt) ergibt [], weil der Iterator am
Ende steht. Wie man Klassen baut, die man beliebig oft durchlaufen kann,
zeigt eine spätere Aufgabe; dass Generatorfunktionen mit yield dieselbe Arbeit
kürzer erledigen, wissen Sie aus Aufgabe 3_022, hier geht es aber um das
Protokoll darunter.

Tipp: Ein Fenster passt noch, solange stelle + breite <= len(zeiten) ist.
Die Zeiten des Fensters sind zeiten[stelle:stelle + breite].
"""


class GleitenderSchnitt:
    """Iterator über die gleitenden Mittelwerte von je breite aufeinanderfolgenden Zeiten."""

    def __init__(self, zeiten, breite):
        """Merkt sich Zeiten und Breite; das erste Fenster beginnt an Stelle 0."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        """Ein Iterator gibt sich selbst zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __next__(self):
        """Liefert den Mittelwert des nächsten Fensters oder löst StopIteration aus."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


schnitt = GleitenderSchnitt([4, 8, 6, 10, 2], 2)
print(next(schnitt), next(schnitt), list(schnitt))
