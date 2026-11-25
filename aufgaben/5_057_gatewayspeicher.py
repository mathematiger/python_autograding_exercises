"""Aufgabe 5_057 – Gatewayspeicher                               Stufe 5 ★★★★★

Ein IoT-Gateway in einer Lagerhalle sammelt die Temperaturen von
mehreren hundert Funksensoren und schickt sie gebündelt an die Cloud.
Das Gateway ist ein kleiner Einplatinenrechner mit wenig Arbeitsspeicher;
an einem Tag kommen aber Millionen Messwerte an. Das Programm darf die
Werte darum nie alle auf einmal im Speicher halten, sondern muss sie als
Strom durch eine Kette von Generatoren schicken. Jede Messung ist ein
Paar (sekunde, wert): die Sekunde seit Beginn der Aufzeichnung und die
Temperatur in °C, aufsteigend nach der Zeit. Schreiben Sie drei Funktionen, jede mit
höchstens O(1) zusätzlichem Speicher, außer für das, was sie liefert:

- `bloecke(werte, groesse)` ist ein Generator, der die Werte eines
  beliebigen Iterables in Listen zu je groesse Werten bündelt (der
  letzte Block darf kürzer sein, leere Blöcke gibt es nicht). Er liest
  erst dann weiter, wenn der nächste Block abgeholt wird.
- `kennzahlen(werte)` geht die Werte genau einmal durch und gibt das
  Tupel (anzahl, minimum, maximum, mittelwert) zurück, oder None, wenn
  es keine Werte gibt.
- `minutenmittel(messungen)` ist ein Generator, der für jede Minute
  (sekunde // 60), in der es Messungen gibt, das Paar
  (minute, mittelwert) liefert, sobald die Minute vorbei ist.

    list(bloecke(range(7), 3))          →  [[0, 1, 2], [3, 4, 5], [6]]
    kennzahlen([21.5, 19.0, 23.5])      →  (3, 19.0, 23.5, 21.333333333333332)
    kennzahlen([])                      →  None
    list(minutenmittel([(0, 20.0), (30, 22.0), (61, 21.0), (185, 19.5)]))
                                        →  [(0, 21.0), (1, 21.0), (3, 19.5)]

    werte = (wert for _, wert in messdaten())      # Millionen Messungen
    next(bloecke(werte, 500))                      # liest nur 500

Grenzen: werte und messungen sind beliebige Iterables, auch Generatoren,
die nur einmal durchlaufen werden können, endlich mit bis zu 10**7
Einträgen oder (bei bloecke und minutenmittel) unendlich. Jeder wert
ist eine Zahl von -100 bis 200, jede sekunde eine ganze Zahl ab 0,
aufsteigend sortiert (gleiche Sekunden möglich). 1 ≤ groesse ≤ 10 000.
Die Tests messen mit tracemalloc, wie viel Speicher Ihre Funktionen
belegen: Für 100 000 Werte dürfen es keine 200 KB sein (eine Liste der
Werte allein bräuchte über 3 MB).

Hintergrund: Wie viel Speicher eine Datenmenge braucht, hängt davon ab,
ob sie auf einmal existiert. Eine Liste hält alle Elemente zugleich,
ein Generator immer nur das aktuelle und seinen Zustand:

    import sys
    sys.getsizeof([x * 1.5 for x in range(10**6)])  # 8 448 728 Byte, nur die Liste,
                                                     # dazu je 24 Byte pro float
    sys.getsizeof(x * 1.5 for x in range(10**6))    # etwa 200 Byte, immer

Wie man Generatoren zu Pipelines verkettet, kennen Sie aus Aufgabe
4_036. Eine Pipeline ist aber nur so sparsam wie ihre gierigste Stufe:
Ein einziges list(...), sorted(...), len(list(...)) oder ein Zwischen-
ergebnis, das alle Werte sammelt, holt den ganzen Strom in den
Speicher, und bei einem unendlichen Strom kommt es nie an. Die
Kennzahlen eines Stroms rechnet man darum laufend mit: Man merkt sich
Anzahl, Summe, Minimum und Maximum bisher und aktualisiert sie bei
jedem Wert. Das braucht vier Variablen, egal wie viele Werte kommen. Wer
erst list(werte) schreibt, um danach len, min, max und sum aufzurufen,
braucht dagegen Speicher für alle Werte, und wer min(werte) und danach
max(werte) aufruft, bekommt beim zweiten Mal gar nichts mehr, weil der
Generator schon verbraucht ist (Aufgabe 3_021).

Zum Bündeln hilft itertools.islice (Aufgabe 4_040): Holt man sich
vorher mit it = iter(werte) einen Iterator, liefert list(islice(it, n))
die nächsten n Werte, und zwar bei jedem Aufruf die nächsten; eine
leere Liste heißt, dass der Strom zu Ende ist. (Ab Python 3.12 gibt es
dafür itertools.batched.) Zum Gruppieren nach der Minute passt
itertools.groupby (Aufgabe 4_044): Weil die Messungen nach der Zeit
sortiert sind, liegen alle einer Minute hintereinander, und groupby
liefert jede Gruppe als Iterator, ohne sie zu sammeln. Vorsicht bei
itertools.tee (Aufgabe 4_048): Läuft eine Kopie der anderen weit voraus,
puffert tee alles dazwischen, also im schlimmsten Fall wieder den
ganzen Strom.

Messen kann man den Speicher mit dem Modul tracemalloc der
Standardbibliothek. Es zählt jeden Speicherblock, den Python anlegt,
und merkt sich den höchsten Stand (Spitze):

    import tracemalloc

    tracemalloc.start()
    summe = sum(x * 1.5 for x in range(10**6))
    aktuell, spitze = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(spitze)          # wenige Hundert Byte; mit [x * 1.5 for …] über 30 MB

So prüfen auch die Tests Ihre Lösung, unabhängig davon, wie schnell der
Rechner ist.
"""

import itertools


def bloecke(werte, groesse):
    """Liefert die Werte in Listen zu je groesse Werten; der letzte Block darf kürzer sein."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kennzahlen(werte):
    """Gibt (anzahl, minimum, maximum, mittelwert) der Werte zurück, oder None ohne Werte."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def minutenmittel(messungen):
    """Liefert (minute, mittelwert) für jede Minute mit Messungen, in zeitlicher Reihenfolge."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(list(bloecke(range(7), 3)))
print(kennzahlen([21.5, 19.0, 23.5]), kennzahlen([]))
print(list(minutenmittel([(0, 20.0), (30, 22.0), (61, 21.0), (185, 19.5)])))
