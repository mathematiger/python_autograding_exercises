# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_074_zufallsbits.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_074_zufallsbits

"""Aufgabe 3_074 – Zufallsbits                                   Stufe 3 ★★★☆☆

Schlüssel, Einmalcodes und Sitzungskennungen sind nur sicher, wenn die
Zufallsbits, aus denen sie entstehen, wirklich ausgewogen sind: Liefert
ein Generator etwas öfter 1 als 0, kann ein Angreifer häufige Schlüssel
zuerst durchprobieren. Das Sicherheitsteam einer Firma prüft darum jeden
neuen Zufallsgenerator mit einem virtuellen Galton-Brett: Eine Kugel
fällt durch reihen Reihen von Nägeln und wird an jedem Nagel nach links
(Bit 0) oder rechts (Bit 1) abgelenkt. Unten landet sie in einem von
reihen + 1 Fächern, und zwar in Fach k, wenn sie k-mal nach rechts ging.
Bei einem guten Generator türmen sich die Kugeln in der Mitte zu einer
Glocke, deren Form man genau ausrechnen kann (siehe Hintergrund).
Schreiben Sie vier Funktionen:

- `galton(kugeln, reihen, zufallsbit)` lässt kugeln Kugeln durch das
  Brett fallen. zufallsbit ist eine Funktion ohne Argumente, die 0 oder
  1 zurückgibt; rufen Sie sie für jede Kugel und jede Reihe genau einmal
  auf, Kugel für Kugel. Sie gibt eine Liste mit reihen + 1 Einträgen
  zurück: an Stelle k, wie viele Kugeln in Fach k landen.
- `erwartete_anzahlen(kugeln, reihen)` gibt die Liste zurück, wie viele
  Kugeln bei einem guten Generator im Mittel in jedem Fach landen.
- `chi_quadrat(beobachtet, erwartet)` misst, wie weit die beobachteten
  Anzahlen von den erwarteten abweichen: die Summe über alle Fächer von
  (beobachtet - erwartet)² / erwartet.
- `verdaechtig(zufallsbit, kugeln, reihen, grenze)` lässt die Kugeln
  fallen und gibt True zurück, wenn chi_quadrat größer als grenze ist.

    galton(2, 3, bits_aus([0, 1, 0,  1, 1, 1]))     →  [0, 1, 0, 1]
    erwartete_anzahlen(16, 4)                       →  [1.0, 4.0, 6.0, 4.0, 1.0]
    chi_quadrat([2, 3, 6, 4, 1], [1, 4, 6, 4, 1])   →  1.25

    random.seed(3074)
    galton(1024, 10, lambda: random.randint(0, 1))
        →  [0, 11, 34, 129, 202, 268, 202, 130, 39, 9, 0]

bits_aus ist im Programm unten vorgegeben: Es macht aus einer Liste eine
Funktion, die bei jedem Aufruf das nächste Bit liefert. Für den
Generator aus random kommt chi_quadrat etwa 8.8 heraus, für einen, der
in 60 von 100 Fällen 1 liefert, fast 500.

Grenzen: 0 ≤ kugeln ≤ 10 000, 1 ≤ reihen ≤ 30. zufallsbit liefert bei
jedem Aufruf 0 oder 1. In chi_quadrat sind beide Listen gleich lang
(1 bis 31 Einträge), alle Werte in erwartet sind größer als 0. grenze
ist eine Zahl von 0 bis 1000.

Hintergrund: Das Galton-Brett (nach dem Naturforscher Francis Galton)
ist eine Simulation wie in Aufgabe 3_073: Jede Kugel ist ein
Zufallsversuch aus reihen Münzwürfen, gezählt wird, wo sie landet. Wie
viele Wege führen in Fach k? Jeder Weg ist eine Folge aus reihen Bits
mit genau k Einsen, und die Anzahl dieser Folgen steht im Pascalschen
Dreieck: Jede Zahl ist die Summe der beiden darüber, am Rand steht 1.

    reihen 0:          1
    reihen 1:        1   1
    reihen 2:      1   2   1
    reihen 3:    1   3   3   1
    reihen 4:  1   4   6   4   1

Eine Zeile entsteht aus der vorigen, indem man eine 1 anhängt und von
hinten nach vorn jeden Eintrag um seinen linken Nachbarn erhöht, oder
mit [1] + [zeile[i] + zeile[i + 1] for i in …] + [1] (Aufgabe 3_017).
Alle 2 hoch reihen Wege sind gleich wahrscheinlich, also landen bei
16 Kugeln und 4 Reihen im Mittel 16 · 6 / 16 = 6 Kugeln in der Mitte.
(math.comb(n, k) rechnet einen Eintrag direkt aus.)

Natürlich trifft eine Simulation die erwarteten Anzahlen nie genau. Ob
die Abweichung noch Zufall ist, sagt die Kennzahl χ² (Chi-Quadrat):
Kleine Abweichungen in Fächern mit vielen Kugeln zählen wenig, große in
dünn besetzten viel. Für 11 Fächer ist bei einem guten Generator χ² nur
in einem von hundert Fällen größer als etwa 23.2; das ist eine übliche
grenze. Die Funktion zufallsbit als Argument zu übergeben (Aufgabe
3_028) hat einen Vorteil: Dasselbe Brett prüft jeden Generator, und für
Tests kann man feste Bits einsetzen. Ein bestandener Test zeigt nur,
dass keine Schieflage auffällt, nicht, dass der Generator sicher ist:
random ist vorhersagbar und für Schlüssel ungeeignet; dafür gibt es das
Modul secrets.
"""

import random


def bits_aus(bits):
    """Gibt eine Funktion zurück, die bei jedem Aufruf das nächste Bit aus der Liste bits liefert."""
    naechste = iter(bits)
    return lambda: next(naechste)


def galton(kugeln, reihen, zufallsbit):
    """Lässt kugeln Kugeln durch reihen Reihen fallen; gibt die Anzahl je Fach zurück."""
    faecher = [0] * (reihen + 1)
    for _ in range(kugeln):
        rechts = 0
        for _ in range(reihen):
            rechts += zufallsbit()
        faecher[rechts] += 1
    return faecher


def erwartete_anzahlen(kugeln, reihen):
    """Gibt zurück, wie viele Kugeln bei einem guten Generator im Mittel in jedem Fach landen."""
    zeile = [1]
    for _ in range(reihen):
        zeile = [1] + [zeile[i] + zeile[i + 1] for i in range(len(zeile) - 1)] + [1]
    wege = 2**reihen
    return [kugeln * anzahl / wege for anzahl in zeile]


def chi_quadrat(beobachtet, erwartet):
    """Gibt die Summe von (beobachtet - erwartet)² / erwartet über alle Fächer zurück."""
    summe = 0
    for wert, mittel in zip(beobachtet, erwartet):
        summe += (wert - mittel) ** 2 / mittel
    return summe


def verdaechtig(zufallsbit, kugeln, reihen, grenze):
    """Gibt True zurück, wenn die Kugeln von zufallsbit zu weit von den erwarteten Anzahlen abweichen."""
    beobachtet = galton(kugeln, reihen, zufallsbit)
    return chi_quadrat(beobachtet, erwartete_anzahlen(kugeln, reihen)) > grenze


print(galton(2, 3, bits_aus([0, 1, 0, 1, 1, 1])))
print(erwartete_anzahlen(16, 4), chi_quadrat([2, 3, 6, 4, 1], [1, 4, 6, 4, 1]))
random.seed(3074)
print(galton(1024, 10, lambda: random.randint(0, 1)))
random.seed(3074)
print(verdaechtig(lambda: random.randint(0, 1), 1024, 10, 23.2))
random.seed(3074)
print(verdaechtig(lambda: 1 if random.random() < 0.6 else 0, 1024, 10, 23.2))


# Idee: galton legt reihen + 1 Nullen an und zählt für jede Kugel die Summe aus reihen Aufrufen von
# zufallsbit(); dieses Fach wird um 1 erhöht. erwartete_anzahlen baut Zeile für Zeile das Pascalsche
# Dreieck bis zur Zeile reihen und rechnet jeden Eintrag · kugeln / 2**reihen. chi_quadrat summiert
# (b - e) ** 2 / e über zip(beobachtet, erwartet), verdaechtig setzt die drei zusammen.
# Anderer Weg: math.comb(reihen, k) für jeden Eintrag; für galton ginge auch
# sum(zufallsbit() for _ in range(reihen)) als Generator-Ausdruck (Aufgabe 3_023).
# Typische Fehler: nur reihen statt reihen + 1 Fächer, zufallsbit einmal pro Kugel statt pro Reihe,
# den Wurf mit random selbst ziehen statt zufallsbit zu benutzen, durch beobachtet statt erwartet
# teilen, >= statt > bei der Grenze, 2 * reihen statt 2 ** reihen Wege.
# Laufzeit: galton braucht O(kugeln · reihen) Aufrufe, erwartete_anzahlen O(reihen²) für das Dreieck
# (mit math.comb ähnlich), chi_quadrat O(Fächer).
