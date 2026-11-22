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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def verteilung(wuerfe, anzahl):
    """Würfelt wuerfe-mal mit anzahl Würfeln und zählt, wie oft jede Augensumme fiel."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def haeufigste(zaehler):
    """Gibt die Augensumme zurück, die am häufigsten fiel, bei Gleichstand die kleinste."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


random.seed(2052)
print(wurf(2))
print(verteilung(5, 1))
print(haeufigste({2: 1, 3: 4, 4: 4}))
