# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_073_kostenrisiko.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_073_kostenrisiko

"""Aufgabe 3_073 – Kostenrisiko                                  Stufe 3 ★★★☆☆

Für die Einführung eines neuen Ticketsystems hat das Controlling drei
Kostenpositionen geschätzt, jede nur als Spanne: Lizenzen 20 000 bis
30 000 Euro, Einrichtung durch einen Dienstleister 5 000 bis 15 000 Euro,
Schulungen 8 000 bis 10 000 Euro. Das Budget beträgt 50 000 Euro. Wie
wahrscheinlich wird es überschritten? Statt das auszurechnen, will das
Controlling das Projekt zehntausendmal am Rechner „durchspielen“: In
jedem Durchlauf bekommt jede Position einen zufälligen Betrag aus ihrer
Spanne, und gezählt wird, wie oft die Summe über dem Budget liegt (eine
Monte-Carlo-Simulation, siehe Hintergrund). Bevor jemand den
Ergebnissen glaubt, soll das Verfahren an einem Wert geprüft werden,
den man genau kennt: der Kreiszahl π. Schreiben Sie drei Funktionen:

- `schaetze_pi(wuerfe, startwert)` setzt mit random.seed(startwert) den
  Zufall zurück und wirft dann wuerfe-mal einen Punkt in das Quadrat
  von (0, 0) bis (1, 1): erst x = random.random(), dann
  y = random.random(). Ein Treffer ist ein Punkt mit x² + y² ≤ 1. Sie
  gibt 4 · Treffer / wuerfe zurück.
- `gesamtkosten(positionen)` spielt das Projekt einmal durch: Für jede
  Position (von, bis) in der Liste positionen zieht sie der Reihe nach
  einen Betrag mit random.uniform(von, bis) und gibt die Summe zurück.
  Sie setzt den Zufall nicht zurück.
- `ueberschreitung(positionen, budget, durchlaeufe, startwert)` setzt
  mit random.seed(startwert) den Zufall zurück, ruft durchlaeufe-mal
  gesamtkosten(positionen) auf und gibt den Anteil der Durchläufe
  zurück, deren Summe größer als budget ist, als Zahl von 0 bis 1.

    schaetze_pi(1000, 3073)                                 →  3.124
    schaetze_pi(100000, 3073)                               →  3.144
    random.seed(7)
    gesamtkosten([(20000, 30000), (5000, 15000), (8000, 10000)])
                                                            →  39048.69…
    ueberschreitung([(20000, 30000), (5000, 15000), (8000, 10000)],
                    50000, 10000, 3073)                     →  0.0798

Das Budget wird also in etwa 8 von 100 Fällen überschritten.

Grenzen: 1 ≤ wuerfe ≤ 200 000 und 1 ≤ durchlaeufe ≤ 20 000; startwert ist
eine ganze Zahl. positionen hat 0 bis 20 Einträge (von, bis) mit
0 ≤ von ≤ bis ≤ 10**7; 0 ≤ budget ≤ 10**9. Damit die Tests dieselben
Zufallszahlen sehen wie Ihr Programm, ziehen Sie genau die Zahlen wie
beschrieben, in dieser Reihenfolge und keine weiteren.

Hintergrund: Eine Monte-Carlo-Simulation (benannt nach dem Spielcasino)
beantwortet eine Frage nach einer Wahrscheinlichkeit oder einer Fläche
durch sehr viele Zufallsversuche, ähnlich wie das Würfeln in Aufgabe
2_052: Der Anteil der „Erfolge“ nähert sich der gesuchten
Wahrscheinlichkeit, je mehr Versuche man macht. Der Fehler schrumpft
allerdings langsam, etwa mit 1 / Wurzel(Versuche): Für eine Stelle
mehr Genauigkeit braucht man hundertmal so viele Versuche.

Für π wirft man Punkte in das Einheitsquadrat (Fläche 1). Der
Viertelkreis mit Radius 1 um (0, 0) hat die Fläche π/4, und ein Punkt
liegt darin, wenn sein Abstand zum Ursprung höchstens 1 ist, also
x² + y² ≤ 1 (Satz des Pythagoras, die Wurzel braucht man dafür nicht).
Der Anteil der Treffer ist also ungefähr π/4, und 4 · Anteil ungefähr π.

random.random() liefert eine Kommazahl von 0 (einschließlich) bis 1
(ausschließlich), random.uniform(a, b) eine von a bis b. Wie in Aufgabe
2_052 sorgt random.seed(startwert) dafür, dass danach immer dieselbe
Folge kommt; so lassen sich Simulationen wiederholen und vergleichen.
Darum setzen schaetze_pi und ueberschreitung den Startwert selbst,
gesamtkosten dagegen nicht: Sonst bekäme jeder Durchlauf dieselben
Beträge. Statt random.seed ginge auch ein eigener Generator
random.Random(startwert) wie in Aufgabe 3_045; er liefert dieselbe
Zahlenfolge und lässt den Zufall anderer Programmteile in Ruhe.
"""

import random


def schaetze_pi(wuerfe, startwert):
    """Schätzt π mit wuerfe zufälligen Punkten im Einheitsquadrat."""
    random.seed(startwert)
    treffer = 0
    for _ in range(wuerfe):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            treffer += 1
    return 4 * treffer / wuerfe


def gesamtkosten(positionen):
    """Zieht für jede Position (von, bis) einen zufälligen Betrag und gibt die Summe zurück."""
    summe = 0
    for von, bis in positionen:
        summe += random.uniform(von, bis)
    return summe


def ueberschreitung(positionen, budget, durchlaeufe, startwert):
    """Gibt den Anteil der Durchläufe zurück, in denen die Gesamtkosten über budget liegen."""
    random.seed(startwert)
    zu_teuer = 0
    for _ in range(durchlaeufe):
        if gesamtkosten(positionen) > budget:
            zu_teuer += 1
    return zu_teuer / durchlaeufe


positionen = [(20000, 30000), (5000, 15000), (8000, 10000)]
print(schaetze_pi(1000, 3073), schaetze_pi(100000, 3073))
print(ueberschreitung(positionen, 50000, 10000, 3073))


# Idee: schaetze_pi setzt random.seed(startwert), zählt in einer Schleife die Punkte mit
# x * x + y * y <= 1 und gibt 4 * treffer / wuerfe zurück. gesamtkosten addiert für jede Position
# random.uniform(von, bis). ueberschreitung setzt einmal den Startwert, zählt die Durchläufe mit
# gesamtkosten(positionen) > budget und teilt durch durchlaeufe.
# Anderer Weg: ein eigener Generator zufall = random.Random(startwert) mit zufall.random() liefert
# dieselben Zahlen; gesamtkosten bräuchte ihn dann als Argument. Kürzer:
# sum(random.uniform(von, bis) for von, bis in positionen). Exakt rechnen ginge auch (die Summe
# gleichverteilter Beträge hat eine bekannte, aber unhandliche Verteilung) – genau das spart die Simulation.
# Typische Fehler: x und y mit einem einzigen random.random() ziehen, random.seed in der Schleife
# (jeder Durchlauf gleich), random.seed in gesamtkosten, die Anzahl statt des Anteils zurückgeben,
# >= statt > beim Budget, den Faktor 4 vergessen.
# Laufzeit: O(wuerfe) bzw. O(durchlaeufe · Positionen); der Fehler der Schätzung schrumpft nur mit
# 1 / Wurzel(wuerfe), für eine Dezimalstelle mehr braucht man hundertmal so viele Würfe.
