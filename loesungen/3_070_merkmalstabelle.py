# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_070_merkmalstabelle.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_070_merkmalstabelle

"""Aufgabe 3_070 – Merkmalstabelle                               Stufe 3 ★★★☆☆

Ein Datenteam trainiert ein Modell, das eingehende Support-Tickets
automatisch einer Kategorie zuordnet. Das Modell rechnet nicht mit
Wörtern, sondern mit Zahlen: Jedes Wort wird über seinen Hashwert auf
eine von m Spalten einer Tabelle verteilt (Spalte = hash(wort) % m), und
gezählt wird, wie oft in einem Ticket ein Wort jeder Spalte vorkommt.
Diesen Kniff nennt man Hashing-Trick. Ist m eine Primzahl, verteilen sich
die Wörter erfahrungsgemäß gleichmäßiger auf die Spalten, als wenn m
viele Teiler hat. Das Team probiert viele Tabellengrößen aus und
braucht dafür drei Funktionen:

- `sieb(n)` gibt eine Liste ist_prim mit n + 1 Wahrheitswerten zurück:
  ist_prim[k] ist True, wenn k eine Primzahl ist, sonst False.
- `primzahlen_bis(n)` gibt alle Primzahlen von 2 bis n aufsteigend
  sortiert zurück, als Liste von Kandidaten für m.
- `naechste_primzahlen(wuensche)` bekommt eine Liste gewünschter
  Tabellengrößen und gibt für jede die kleinste Primzahl zurück, die
  mindestens so groß ist, in derselben Reihenfolge.

Eine Primzahl ist eine ganze Zahl größer als 1, die nur durch 1 und sich
selbst teilbar ist. Beide Funktionen sollen das Sieb des Eratosthenes
verwenden (siehe Hintergrund, die beiden anderen über sieb), nicht
jede Zahl einzeln durch Teilen prüfen.

    sieb(10)   →  [False, False, True, True, False, True, False, True, False, False, False]
    primzahlen_bis(30)                       →  [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    primzahlen_bis(1)                        →  []
    naechste_primzahlen([1000, 24, 97, 2])   →  [1009, 29, 97, 2]

Grenzen: Für sieb gilt 0 ≤ n ≤ 1 100 000, für primzahlen_bis
0 ≤ n ≤ 10**6. wuensche hat 0 bis 10 000 Einträge, ganze Zahlen
mit 2 ≤ wunsch ≤ 10**6, Doppelte möglich. sieb und primzahlen_bis
sollen O(n log log n) Schritte brauchen, also kaum mehr als O(n).
naechste_primzahlen soll nur einmal sieben und danach je Wunsch nur
wenige Schritte brauchen.

Hintergrund: Ob eine einzelne Zahl k eine Primzahl ist, prüft man, indem
man sie durch 2, 3, 4, … teilt; es genügt, bis zur Wurzel von k zu gehen,
weil zu jedem größeren Teiler ein kleinerer gehört. Für alle Zahlen bis n
kostet das aber etwa n · √n Schritte. Das Sieb des Eratosthenes (nach
dem griechischen Gelehrten, um 250 v. Chr.) teilt gar nicht, sondern
streicht. Man legt eine Liste von Wahrheitswerten an, ist_prim[k] für
k = 0 bis n, zuerst alle True außer 0 und 1. Dann geht man aufwärts:
Ist ist_prim[p] noch True, ist p eine Primzahl, und man streicht alle
ihre Vielfachen, indem man sie auf False setzt:

    p = 2:  streicht 4, 6, 8, 10, …
    p = 3:  streicht 9, 12, 15, …    (6 ist schon gestrichen)
    p = 4:  schon gestrichen, nichts zu tun
    p = 5:  streicht 25, 30, 35, …

Zwei Abkürzungen machen das Sieb schnell: Man beginnt bei p · p, weil
die kleineren Vielfachen 2p, 3p, … schon von einer kleineren Primzahl
gestrichen wurden, und man hört auf, sobald p · p > n ist. Die
Vielfachen durchläuft range(p * p, n + 1, p) mit der Schrittweite p
(Aufgabe 1_024). Was am Ende noch True ist, sind genau die Primzahlen.
Gestrichen wird für jede Primzahl p etwa n / p-mal; zusammen sind das
n · (1/2 + 1/3 + 1/5 + …) ≈ n · log log n Schritte, und log log n ist
selbst für n = 10**6 kleiner als 3. Das Sieb tauscht wie die Menge in
Aufgabe 3_063 Speicher gegen Zeit: eine Liste mit n + 1 Einträgen.

Tipp: Die Wurzel als ganze Zahl liefert math.isqrt(n) (Aufgabe 3_045
zum Modul math). Für naechste_primzahlen sieben Sie einmal bis etwas
über den größten Wunsch: Bis 10**6 liegt die nächste Primzahl nie mehr
als 114 Zahlen weiter.
"""

import math


def sieb(n):
    """Gibt die Liste ist_prim mit n + 1 Wahrheitswerten zurück (Sieb des Eratosthenes)."""
    ist_prim = [True] * (n + 1)
    ist_prim[0] = False
    if n >= 1:
        ist_prim[1] = False
    for p in range(2, math.isqrt(n) + 1):
        if ist_prim[p]:
            for vielfaches in range(p * p, n + 1, p):
                ist_prim[vielfaches] = False
    return ist_prim


def primzahlen_bis(n):
    """Gibt alle Primzahlen von 2 bis n aufsteigend zurück."""
    ist_prim = sieb(n)
    primzahlen = []
    for zahl in range(2, n + 1):
        if ist_prim[zahl]:
            primzahlen.append(zahl)
    return primzahlen


def naechste_primzahlen(wuensche):
    """Gibt zu jedem Wunsch die kleinste Primzahl zurück, die mindestens so groß ist."""
    if not wuensche:
        return []
    ist_prim = sieb(max(wuensche) + 114)
    ergebnis = []
    for wunsch in wuensche:
        kandidat = wunsch
        while not ist_prim[kandidat]:
            kandidat += 1
        ergebnis.append(kandidat)
    return ergebnis


print(sieb(10))
print(primzahlen_bis(30))
print(naechste_primzahlen([1000, 24, 97, 2]))


# Idee: sieb(n) legt ist_prim = [True] * (n + 1) an, setzt 0 und 1 (falls vorhanden) auf False und
# streicht für jedes p von 2 bis isqrt(n), das noch True ist, die Vielfachen p · p, p · p + p, … bis n.
# primzahlen_bis sammelt alle k mit ist_prim[k]. naechste_primzahlen siebt einmal bis
# max(wuensche) + 114 und geht von jedem Wunsch aufwärts, bis ist_prim True ist; das sind nur
# wenige Schritte, weil Primzahlen dicht liegen.
# Anderer Weg: Das Streichen geht ohne innere Schleife mit einer Ausschnitt-Zuweisung,
# ist_prim[p * p :: p] = [False] * len(range(p * p, n + 1, p)), die in C läuft. Für viele Wünsche
# kann man auch von hinten eine Liste naechste[k] füllen (naechste[k] = k, wenn k prim ist, sonst
# naechste[k + 1]); dann ist jede Antwort ein einziger Zugriff. Der naive Weg prüft jede Zahl durch
# Teilen bis zur Wurzel: O(n · √n) für primzahlen_bis.
# Typische Fehler: ist_prim nur n statt n + 1 Einträge lang (n fehlt), 1 als Primzahl stehen lassen,
# beim Streichen p selbst streichen (Start bei p statt bei 2p oder p · p), range(p * p, n, p) ohne n,
# nur bis max(wuensche) sieben (dann fehlt die nächste Primzahl darüber), für jeden Wunsch neu sieben,
# max([]) bei leeren Wünschen.
# Laufzeit: Das Sieb braucht O(n log log n): Für jede Primzahl p wird etwa n / p-mal gestrichen, und
# die Summe der Kehrwerte der Primzahlen bis n wächst nur wie log log n. naechste_primzahlen braucht
# dazu O(k · g) für k Wünsche, wobei g die Lücke bis zur nächsten Primzahl ist (bis 10**6 höchstens 114).
