# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_072_blockverteilung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_072_blockverteilung

"""Aufgabe 3_072 – Blockverteilung                               Stufe 3 ★★★☆☆

Ein Speichercluster im Rechenzentrum zerlegt jede Datei in nummerierte
Blöcke und verteilt sie auf mehrere Speicherknoten. Damit jeder Server
ohne Nachfragen weiß, wo ein Block liegt, wird der Platz aus der
Blocknummer berechnet: Block k liegt auf dem Knoten

    (16807 hoch k  modulo  2147483647)  modulo  anzahl_knoten

Das sieht zufällig aus und verteilt die Blöcke gleichmäßig, ist aber
jedes Mal dasselbe. (2147483647 ist die Primzahl 2**31 - 1; die Formel
stammt von einem bekannten Zufallszahlengenerator.) Die Blocknummern
sind sehr groß, bis 10**18. Schreiben Sie drei Funktionen:

- `potenz_mod(basis, exponent, modul)` gibt basis hoch exponent modulo
  modul zurück, mit schnellem Potenzieren (siehe Hintergrund).
- `knoten_fuer(block, anzahl_knoten)` gibt den Knoten (0 bis
  anzahl_knoten - 1) für Block block nach der Formel oben zurück.
- `verteilung(bloecke, anzahl_knoten)` gibt eine Liste mit
  anzahl_knoten Einträgen zurück: an Stelle i, wie viele der Blöcke in
  der Liste bloecke auf Knoten i liegen.

    potenz_mod(3, 13, 7)                  →  3
    potenz_mod(2, 10, 1000)               →  24
    knoten_fuer(1, 10)                    →  7
    knoten_fuer(10**18, 10)               →  9
    verteilung([1, 2, 3, 4, 5], 3)        →  [0, 3, 2]

Verwenden Sie weder ** noch pow, sondern schreiben Sie das Verfahren
selbst.

Grenzen: 0 ≤ basis ≤ 10**18, 0 ≤ exponent ≤ 10**18, 1 ≤ modul ≤ 10**18;
basis hoch 0 ist 1 (auch für basis 0), modulo modul. 0 ≤ block ≤ 10**18,
1 ≤ anzahl_knoten ≤ 1000. bloecke hat 0 bis 2000 Einträge.
potenz_mod soll O(log exponent) Schritte brauchen, also auch für
exponent 10**18 nur wenige hundert.

Hintergrund: Modulare Arithmetik rechnet nur mit Resten (Aufgabe 1_005
zu %). Dabei darf man zwischendurch beliebig oft den Rest nehmen, das
Ergebnis bleibt gleich:

    (a * b) % m  ==  ((a % m) * (b % m)) % m

So bleiben alle Zwischenergebnisse kleiner als m. Trotzdem wäre es zu
langsam, für 16807 hoch 10**18 die Basis 10**18-mal zu multiplizieren.
Schnelles Potenzieren (auch „Quadrieren und Multiplizieren“) halbiert den
Exponenten in jedem Schritt:

    a hoch 13 = a hoch 8  ·  a hoch 4  ·  a hoch 1      (13 = 8 + 4 + 1)

Die Potenzen a, a², a⁴, a⁸, … entstehen, indem man immer wieder
quadriert. Welche davon man braucht, verraten die Binärziffern des
Exponenten (13 ist binär 1101): Ist der Exponent ungerade, kommt die
aktuelle Potenz ins Ergebnis, danach wird sie quadriert und der
Exponent mit // 2 halbiert, bis er 0 ist:

    exponent   ungerade?   ergebnis      potenz
       13         ja       1 · a         a  → a²
        6         nein     a             a² → a⁴
        3         ja       a · a⁴        a⁴ → a⁸
        1         ja       a⁵ · a⁸       a⁸ → a¹⁶
        0                  a¹³

Nach jeder Multiplikation nimmt man den Rest modulo m. Der Exponent
halbiert sich jedes Mal, darum genügen für 10**18 etwa 60 Durchläufe
(2**60 ist ungefähr 10**18), wie bei der binären Suche (Aufgabe 3_002).
Man kann es auch rekursiv schreiben (Aufgabe 2_044): a hoch n ist
(a hoch (n // 2))², für ungerades n noch mal a. Python kann das übrigens
schon: pow(basis, exponent, modul) rechnet genau so. Für die Aufgabe
schreiben Sie es selbst, damit Sie sehen, wie es geht.
"""

BASIS = 16807
MODUL = 2147483647


def potenz_mod(basis, exponent, modul):
    """Gibt basis hoch exponent modulo modul zurück (schnelles Potenzieren)."""
    ergebnis = 1 % modul
    potenz = basis % modul
    while exponent > 0:
        if exponent % 2 == 1:
            ergebnis = ergebnis * potenz % modul
        potenz = potenz * potenz % modul
        exponent //= 2
    return ergebnis


def knoten_fuer(block, anzahl_knoten):
    """Gibt den Speicherknoten zurück, auf dem Block block liegt."""
    return potenz_mod(BASIS, block, MODUL) % anzahl_knoten


def verteilung(bloecke, anzahl_knoten):
    """Gibt zu jedem Knoten zurück, wie viele der Blöcke auf ihm liegen."""
    anzahlen = [0] * anzahl_knoten
    for block in bloecke:
        anzahlen[knoten_fuer(block, anzahl_knoten)] += 1
    return anzahlen


print(potenz_mod(3, 13, 7), potenz_mod(2, 10, 1000))
print(knoten_fuer(1, 10), knoten_fuer(2, 1000))
print(verteilung([1, 2, 3, 4, 5], 3))


# Idee: ergebnis beginnt bei 1 % modul, potenz bei basis % modul. Solange exponent > 0: ist er
# ungerade, multipliziert man potenz ins Ergebnis; dann wird potenz quadriert und exponent mit // 2
# halbiert. Nach jeder Multiplikation nimmt man % modul, damit die Zahlen klein bleiben.
# knoten_fuer ist potenz_mod(16807, block, 2147483647) % anzahl_knoten, verteilung zählt in einer
# Liste aus anzahl_knoten Nullen.
# Anderer Weg: rekursiv: halb = potenz_mod(basis, exponent // 2, modul); ergebnis = halb * halb % modul,
# bei ungeradem exponent noch * basis % modul; Rekursionsanfang exponent == 0. Der naive Weg
# multipliziert exponent-mal (O(n)), für 10**18 unmöglich; (basis ** exponent) % modul baut erst die
# riesige Zahl und nimmt den Rest zu spät.
# Typische Fehler: 1 statt 1 % modul zurückgeben (falsch bei modul 1), die Basis nicht vorher modulo
# nehmen, potenz nur bei ungeradem Exponenten quadrieren, / statt // beim Halbieren (dann wird der
# Exponent ein float).
# Laufzeit: O(log exponent), weil sich der Exponent in jedem Durchlauf halbiert: für 10**18 etwa
# 60 Durchläufe. verteilung braucht O(n log k) für n Blöcke mit Nummern bis k.
