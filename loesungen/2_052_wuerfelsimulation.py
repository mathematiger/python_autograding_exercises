# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_052_wuerfelsimulation.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_052_wuerfelsimulation

"""Aufgabe 2_052 – Würfelsimulation                              Stufe 2 ★★☆☆☆

Ein Softwarehaus entwickelt für einen Kunden ein digitales Brettspiel.
Bei der Abnahme fragt der Kunde, ob der eingebaute Würfel fair ist: Mit
zwei Würfeln soll die Augensumme 7 am häufigsten fallen, 2 und 12 am
seltensten. Die Qualitätssicherung will das mit einer Simulation zeigen:
Der Rechner würfelt sehr oft und zählt, wie oft jede Augensumme
herauskommt. Schreiben Sie drei Funktionen:

- `wurf(anzahl)` würfelt mit anzahl Würfeln und gibt die Augensumme
  zurück. Benutzen Sie für jeden Würfel genau einmal random.randint(1, 6)
  (warum, steht im Hintergrund).
- `verteilung(wuerfe, anzahl)` würfelt wuerfe-mal mit wurf(anzahl) und
  gibt ein Dictionary zurück: jede mögliche Augensumme (von anzahl bis
  6 · anzahl) → wie oft sie fiel. Auch Augensummen, die nie fielen,
  stehen darin, mit 0.
- `haeufigste(zaehler)` bekommt so ein Dictionary und gibt die
  Augensumme zurück, die am häufigsten fiel; bei Gleichstand die
  kleinste.

    random.seed(2052)
    wurf(2)                            →  9
    verteilung(5, 1)                   →  {1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 2}
    haeufigste({2: 1, 3: 4, 4: 4})     →  3

Grenzen: 1 ≤ anzahl ≤ 10, 0 ≤ wuerfe ≤ 20 000. haeufigste bekommt ein
Ergebnis von verteilung, die Schlüssel also aufsteigend.

Hintergrund: Aus Aufgabe 1_041 kennen Sie random.randint(a, b) und
random.seed(startzahl): Der Rechner würfelt nicht wirklich, sondern
rechnet aus der Startzahl eine Folge von Zahlen aus, die zufällig
aussehen. Nach demselben random.seed kommt immer dieselbe Folge heraus.
Genau das nutzen Tests: Sie setzen eine Startzahl, rufen Ihre Funktion
auf und vergleichen mit dem, was nach derselben Startzahl herauskommen
muss. Das klappt nur, wenn Ihre Funktion die Zahlen in derselben Weise
zieht, darum genau ein random.randint(1, 6) je Würfel:

    random.seed(5)
    a = random.randint(1, 6) + random.randint(1, 6)
    random.seed(5)
    b = random.randint(1, 6) + random.randint(1, 6)
    a == b       →  True

Eine Simulation macht einen Zufallsversuch sehr oft und zählt die
Ergebnisse. Je mehr Versuche, desto näher kommen die Anteile an die
Wahrscheinlichkeiten heran: Von den 36 gleich wahrscheinlichen Paaren
zweier Würfel ergeben 6 die Summe 7 (1+6, 2+5, …, 6+1), aber nur eins
die 2. Bei 3600 Würfen fällt die 7 also etwa 600-mal. Zum Zählen eignet
sich ein Dictionary (Aufgabe 2_026).
"""

import random


def wurf(anzahl):
    """Würfelt mit anzahl Würfeln und gibt die Augensumme zurück."""
    summe = 0
    for _ in range(anzahl):
        summe = summe + random.randint(1, 6)
    return summe


def verteilung(wuerfe, anzahl):
    """Würfelt wuerfe-mal mit anzahl Würfeln und zählt, wie oft jede Augensumme fiel."""
    zaehler = {}
    for summe in range(anzahl, 6 * anzahl + 1):
        zaehler[summe] = 0
    for _ in range(wuerfe):
        summe = wurf(anzahl)
        zaehler[summe] = zaehler[summe] + 1
    return zaehler


def haeufigste(zaehler):
    """Gibt die Augensumme zurück, die am häufigsten fiel, bei Gleichstand die kleinste."""
    beste = None
    for summe in zaehler:
        if beste is None or zaehler[summe] > zaehler[beste]:
            beste = summe
    return beste


random.seed(2052)
print(wurf(2))
print(verteilung(5, 1))
print(haeufigste({2: 1, 3: 4, 4: 4}))


# Idee: wurf addiert in einer Schleife anzahl-mal random.randint(1, 6). verteilung legt zuerst jede
# mögliche Summe von anzahl bis 6 * anzahl mit 0 an, würfelt dann wuerfe-mal und zählt den passenden
# Eintrag hoch. haeufigste geht die Schlüssel der Reihe nach durch und merkt sich eine Summe nur,
# wenn sie echt häufiger fiel als die bisher beste; so bleibt bei Gleichstand die kleinere stehen.
# Anderer Weg: in haeufigste erst die größte Anzahl mit max(zaehler.values()) bestimmen und dann die
# kleinste Summe mit dieser Anzahl suchen. Statt eines vorher angelegten Dictionarys kann man
# zaehler.get(summe, 0) + 1 benutzen (Aufgabe 2_026), muss dann aber die fehlenden Summen am Ende
# noch mit 0 ergänzen.
# Typische Fehler: random.randint(2, 12) für zwei Würfel (dann ist jede Summe gleich häufig, und die
# Zahlenfolge passt nicht mehr), random.seed in der Funktion aufrufen (dann kommt immer dasselbe
# heraus), die nie gefallenen Summen weglassen, >= statt > in haeufigste (bei Gleichstand gewinnt die
# größere Summe) oder die größte Anzahl statt der Augensumme zurückgeben.
