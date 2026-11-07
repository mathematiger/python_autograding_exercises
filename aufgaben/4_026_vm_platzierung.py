"""Aufgabe 4_026 – VM-Platzierung                                Stufe 4 ★★★★☆

Ein Rechenzentrum betreibt virtuelle Maschinen (VMs) für seine Kunden.
Ein Host-Server fällt aus, und auf dem Ersatz-Host ist nur noch Platz
für eine begrenzte Menge Arbeitsspeicher (RAM). Jede VM braucht eine
feste Menge RAM in GB und hat einen Nutzen: wie viel ihr Weiterlaufen
wert ist, etwa nach den vereinbarten Servicestufen der Kunden. Welche
VMs sollen auf den Ersatz-Host, damit der Gesamtnutzen am größten ist
und ihr RAM zusammen nicht über die freie Menge geht? Eine VM läuft
ganz oder gar nicht, teilen kann man sie nicht. Jede VM ist ein Tupel
(name, ram, nutzen). Schreiben Sie zwei Funktionen:

- `bester_nutzen(vms, ram)` gibt den größten erreichbaren Gesamtnutzen
  zurück. Lösen Sie es rekursiv mit einer inneren Funktion, die Sie mit
  @lru_cache(maxsize=None) dekorieren.
- `auswahl(vms, ram)` gibt die Namen einer besten Auswahl zurück, in
  der Reihenfolge von vms. Lösen Sie es mit einer Tabelle, die Sie Zeile
  für Zeile von unten aufbauen, und lesen Sie die Auswahl rückwärts aus
  der Tabelle ab. Gibt es mehrere beste Auswahlen, ist jede richtig.

    vms = [("web", 4, 40), ("db", 6, 70), ("mail", 3, 25), ("build", 5, 50)]
    bester_nutzen(vms, 11)   →  120
    auswahl(vms, 11)         →  ["db", "build"]   (11 GB, Nutzen 70 + 50)
    bester_nutzen(vms, 2)    →  0                 (keine VM passt)

Grenzen: 0 ≤ len(vms) ≤ 100, die Namen sind verschiedene, nicht leere
Texte. ram einer VM ist eine ganze Zahl von 1 bis 1000, nutzen eine
ganze Zahl von 0 bis 10**6. Der freie RAM des Hosts ist eine ganze Zahl
von 0 bis 1000. Beide Funktionen sollen O(n · ram) Schritte brauchen
(n VMs, ram GB frei), nicht 2**n.

Hintergrund: Dieses Problem heißt Rucksackproblem: Gegenstände mit
Gewicht und Wert, ein Rucksack mit Höchstgewicht. Gierig nach dem
besten Verhältnis Nutzen pro GB zu wählen klappt nicht immer: Im
Beispiel hat db das beste Verhältnis (fast 11,7 pro GB), danach kommen
web und build mit je 10 pro GB. Gierig nimmt man db und web und kommt
auf 110; mit db und build wären es 120. Probiert man dagegen alle Teilmengen aus, sind
das 2**n Stück, bei 100 VMs mehr, als je ein Rechner schafft.

Die Rettung ist dynamische Programmierung: Man zerlegt das Problem in
Teilprobleme, die sich oft wiederholen, und löst jedes nur einmal. Bei
jeder VM gibt es zwei Möglichkeiten, nehmen oder nicht nehmen, und
danach bleibt dasselbe Problem mit den restlichen VMs und dem
restlichen RAM. Ein Teilproblem ist also durch zwei Zahlen bestimmt:
ab welcher VM noch entschieden wird und wie viel RAM noch frei ist. Es
gibt höchstens (n + 1) · (ram + 1) solche Paare, viel weniger als 2**n.

Rekursiv geschrieben merkt sich lru_cache (Aufgabe 4_025) jedes Paar.
Weil eine Liste nicht hashbar ist, bekommt die gecachte Funktion nicht
die Liste, sondern nur die zwei Zahlen; die Liste sieht sie als
Variable der äußeren Funktion (Closure, Aufgabe 4_021). Als Beispiel
eine verwandte Frage: Auf wie viele Arten kann man aus den Zahlen einer
Liste welche auswählen, sodass ihre Summe genau ziel ist?

    def arten(zahlen, ziel):
        @lru_cache(maxsize=None)
        def ab(index, rest):
            if index == len(zahlen):
                return 1 if rest == 0 else 0
            ohne = ab(index + 1, rest)
            if zahlen[index] > rest:
                return ohne
            return ohne + ab(index + 1, rest - zahlen[index])
        return ab(0, ziel)

    arten([2, 3, 5], 5)   →  2   ({2, 3} und {5})

Weil die innere Funktion bei jedem Aufruf von arten neu entsteht, hat
sie auch einen neuen, leeren Cache; Ergebnisse für andere Listen
können sich nicht vermischen.

Als Tabelle rechnet man dasselbe von unten nach oben: Zeile i enthält
für jede Restmenge r das Ergebnis mit den ersten i Zahlen. Zeile i + 1
entsteht nur aus Zeile i, Rekursion und Cache braucht man nicht:

    tabelle = [[1] + [0] * ziel]           # Zeile 0: ohne Zahlen nur Summe 0
    for zahl in zahlen:
        alt = tabelle[-1]
        neu = list(alt)                    # die Zahl nicht nehmen
        for r in range(zahl, ziel + 1):
            neu[r] = alt[r] + alt[r - zahl]   # oder die Zahl nehmen
        tabelle.append(neu)
    tabelle[-1][ziel]                      →  2

Die Tabelle hat einen Vorteil: Man kann rückwärts ablesen, wie das
Ergebnis entstanden ist. Unterscheidet sich der Wert in Zeile i von dem
in Zeile i - 1 in derselben Spalte, wurde der i-te Gegenstand genommen,
und man macht in Zeile i - 1 bei der um sein Gewicht kleineren Spalte
weiter.
"""

from functools import lru_cache


def bester_nutzen(vms, ram):
    """Gibt den größten Gesamtnutzen einer Auswahl von vms zurück, deren RAM zusammen höchstens ram ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auswahl(vms, ram):
    """Gibt die Namen einer besten Auswahl von vms in ihrer Reihenfolge zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


vms = [("web", 4, 40), ("db", 6, 70), ("mail", 3, 25), ("build", 5, 50)]
print(bester_nutzen(vms, 11))
print(auswahl(vms, 11))
print(bester_nutzen(vms, 2))
