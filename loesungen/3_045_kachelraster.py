# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_045_kachelraster.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_045_kachelraster

"""Aufgabe 3_045 – Kachelraster                                  Stufe 3 ★★★☆☆

Ein Kundenportal soll eine neue Startseite bekommen: Statt einer langen
Liste zeigt sie Kacheln (gleich breite Kästen mit je einem Dienst) in
einem Raster, so viele nebeneinander, wie auf den Bildschirm passen.
Bevor das Team die Seite ausrollt, sind drei Dinge zu klären. Schreiben
Sie dafür drei Funktionen und nutzen Sie die passenden Module der
Standardbibliothek:

- `zeilen_im_raster(kacheln, breite, kachelbreite)`: In eine Zeile
  passen breite // kachelbreite Kacheln. Wie viele Zeilen braucht das
  Raster für alle Kacheln? Eine angefangene Zeile zählt mit. Benutzen
  Sie math.ceil.
- `breitenbericht(breiten)` bekommt die Bildschirmbreiten (in Pixeln)
  aller Besuche der letzten Woche und gibt das Tupel (haeufigste,
  median) zurück: die häufigste Breite (bei Gleichstand die, die zuerst
  in der Liste vorkommt) und den Median. Benutzen Sie statistics.mode
  und statistics.median.
- `ab_gruppen(personen, startwert)` teilt Testpersonen für einen A/B-Test
  auf: Gruppe A sieht die neue Startseite, Gruppe B die alte. Die
  Funktion kopiert die Liste, mischt die Kopie mit der shuffle-Methode
  eines random.Random(startwert) und gibt das Tupel (gruppe_a, gruppe_b)
  zurück: Gruppe A ist die vordere Hälfte der gemischten Liste, bei einer
  ungeraden Zahl mit einer Person mehr, Gruppe B der Rest. Die
  übergebene Liste bleibt unverändert.

    zeilen_im_raster(10, 1000, 300)                     →  4
    breitenbericht([1920, 1366, 1920, 390, 1536])       →  (1920, 1536)
    ab_gruppen(["Ada", "Ben", "Cem", "Dana", "Eli"], 3)
        →  (["Ada", "Cem", "Dana"], ["Eli", "Ben"])

Im ersten Beispiel passen 1000 // 300 = 3 Kacheln in eine Zeile, für 10
Kacheln braucht es also 4 Zeilen.

Grenzen: 0 ≤ kacheln ≤ 1 000 000 und 1 ≤ kachelbreite ≤ breite ≤ 10 000,
alles ganze Zahlen. breiten hat 1 bis 100 000 Einträge, ganze Zahlen von
240 bis 7680. personen hat 0 bis 10 000 verschiedene Namen,
startwert ist eine ganze Zahl von 0 bis 10**9.

Hintergrund: Python bringt viele Module mit, fertige Sammlungen von
Funktionen, die man nur noch importieren muss. math kennen Sie aus
Aufgabe 1_006, random aus Aufgabe 1_041. Es gibt zwei übliche Formen:

    import statistics                  # dann statistics.mean(werte)
    from math import ceil, floor       # dann direkt ceil(2.1)  →  3

Die erste zeigt bei jedem Aufruf, woher eine Funktion kommt; die zweite
ist kürzer, kann aber eigene Namen verdecken. Was ein Modul bietet,
zeigen help(statistics) und dir(math) in der Python-Konsole. Drei
Module, die man oft braucht:

- math: ceil rundet auf (ceil(3.2) → 4), floor ab, dazu sqrt, pi, log …
- statistics: mean (Mittelwert), median (der mittlere Wert der
  sortierten Liste; bei gerader Anzahl der Mittelwert der beiden
  mittleren, also oft eine Kommazahl), mode (der häufigste Wert; bei
  Gleichstand der, der zuerst vorkommt), stdev (Standardabweichung).
- random: Statt random.seed (Aufgabe 2_052), das die Zahlenfolge des
  ganzen Programms festlegt, erzeugt random.Random(startwert) einen
  eigenen Zufallsgenerator mit eigener Folge. Er hat dieselben Methoden
  wie das Modul: randint, choice, sample und shuffle, das eine Liste an
  Ort und Stelle mischt und None zurückgibt.

    zufall = random.Random(7)
    karten = [1, 2, 3, 4]
    zufall.shuffle(karten)            # karten ist jetzt gemischt

Mit demselben startwert kommt dieselbe Mischung heraus; so kann man die
Aufteilung später nachvollziehen, und andere Teile des Programms, die
random benutzen, stören nicht.
"""

import math
import random
import statistics


def zeilen_im_raster(kacheln, breite, kachelbreite):
    """Gibt die Zahl der Zeilen zurück, die das Raster für alle Kacheln braucht."""
    je_zeile = breite // kachelbreite
    return math.ceil(kacheln / je_zeile)


def breitenbericht(breiten):
    """Gibt das Tupel (häufigste Breite, Median der Breiten) zurück."""
    return (statistics.mode(breiten), statistics.median(breiten))


def ab_gruppen(personen, startwert):
    """Mischt eine Kopie der Personen und teilt sie in die Gruppen A und B."""
    gemischt = list(personen)
    random.Random(startwert).shuffle(gemischt)
    mitte = math.ceil(len(gemischt) / 2)
    return (gemischt[:mitte], gemischt[mitte:])


print(zeilen_im_raster(10, 1000, 300))
print(breitenbericht([1920, 1366, 1920, 390, 1536]))
print(ab_gruppen(["Ada", "Ben", "Cem", "Dana", "Eli"], 3))


# Idee: Jede Funktion übergibt ihre Arbeit an das passende Modul. zeilen_im_raster rechnet mit //
# die ganzen Kacheln je Zeile aus und rundet kacheln / je_zeile mit math.ceil auf. breitenbericht
# gibt statistics.mode und statistics.median als Tupel zurück. ab_gruppen kopiert die Liste, mischt
# sie mit random.Random(startwert).shuffle und schneidet bei math.ceil(n / 2) in zwei Teile.
# Anderer Weg: ganzzahlig aufrunden mit (kacheln + je_zeile - 1) // je_zeile oder -(-kacheln //
# je_zeile); den Median selbst aus der sortierten Liste holen und die häufigste Breite mit einem
# Dictionary zählen (so prüfen es die Tests). Für die Mitte geht auch (len(gemischt) + 1) // 2.
# Typische Fehler: breite / kachelbreite statt // (halbe Kacheln), round statt ceil (rundet 3.2 ab),
# shuffle auf der übergebenen Liste statt auf einer Kopie, gruppen = zufall.shuffle(...) (shuffle gibt
# None zurück), random.seed(startwert) statt eines eigenen Generators, oder max(set(breiten),
# key=breiten.count) für die häufigste Breite (bei Gleichstand entscheidet die Reihenfolge der
# Menge, nicht die der Liste, und O(n²)).
# Laufzeit: zeilen_im_raster O(1), breitenbericht O(n log n) wegen des Sortierens im Median,
# ab_gruppen O(n).
