"""Aufgabe 4_029 – Ticketbilanz                                 Stufe 4 ★★★★☆

Am Ende jeder Schicht zieht der Service Desk Bilanz über die bearbeiteten
Tickets. Jedes Ticket ist ein Dictionary mit der Nummer, der Priorität
(1 = kritisch, 2 = hoch, 3 = mittel, 4 = niedrig), der Kategorie und den
Minuten, die die Bearbeitung gedauert hat:

    {"nummer": 4711, "prioritaet": 2, "kategorie": "Netzwerk", "minuten": 35}

Schreiben Sie drei Funktionen, die eine Liste solcher Tickets jeweils zu
einem einzigen Wert zusammenfalten, und zwar mit functools.reduce, ohne for-
oder while-Schleife:

- `gesamtminuten(tickets)` liefert die Summe aller Minuten (0 bei einer
  leeren Liste).
- `dringendstes(tickets)` liefert das Ticket mit der kleinsten
  Prioritätszahl; haben mehrere dieselbe, das erste davon in der Liste. Bei
  einer leeren Liste None.
- `minuten_je_kategorie(tickets)` liefert ein Dictionary Kategorie →
  Summe der Minuten, die Kategorien in der Reihenfolge, in der sie zum
  ersten Mal vorkommen. Die Tickets selbst bleiben unverändert.

    tickets = [
        {"nummer": 1, "prioritaet": 3, "kategorie": "Drucker", "minuten": 20},
        {"nummer": 2, "prioritaet": 1, "kategorie": "Netzwerk", "minuten": 45},
        {"nummer": 3, "prioritaet": 1, "kategorie": "Drucker", "minuten": 10},
    ]
    gesamtminuten(tickets)         →  75
    dringendstes(tickets)["nummer"]  →  2
    minuten_je_kategorie(tickets)  →  {"Drucker": 30, "Netzwerk": 45}

Grenzen: 0 ≤ len(tickets) ≤ 10 000. Die Nummern sind verschieden, die
Priorität ist 1, 2, 3 oder 4, die Kategorie ist ein nicht leerer Text (es
gibt höchstens 20 verschiedene), und es gilt 0 ≤ minuten ≤ 10 000.

Hintergrund: Viele Auswertungen haben dieselbe Form: Man beginnt mit einem
Startwert und verrechnet ihn nacheinander mit jedem Element, bis ein
einziges Ergebnis übrig ist. Eine Summe beginnt bei 0 und addiert, ein
Maximum behält jeweils das größere. functools.reduce(funktion, folge,
startwert) macht genau das: Es ruft funktion(zwischenstand, element) für
jedes Element auf und benutzt das Ergebnis als neuen Zwischenstand.

    from functools import reduce

    reduce(lambda summe, zahl: summe + zahl, [3, 5, 7], 0)
    # ((0 + 3) + 5) + 7  →  15

    reduce(lambda groesster, zahl: zahl if zahl > groesster else groesster, [3, 9, 4])
    # ohne Startwert beginnt reduce mit dem ersten Element: 3, dann 9, dann 9  →  9

Ohne Startwert und mit leerer Folge löst reduce einen TypeError aus; mit
Startwert kommt bei leerer Folge der Startwert zurück. Der Zwischenstand
darf jeder Typ sein, auch ein Tupel oder ein Dictionary. Dann sollte die
Funktion den Zwischenstand nicht verändern, sondern einen neuen bauen, etwa
{**stand, schluessel: wert}: So bleibt jede Zwischenstufe für sich richtig,
und kein Dictionary von außen wird aus Versehen überschrieben. Für die
Funktion passt oft ein lambda (Aufgabe 3_025), bei mehr als einer Zeile eine
kleine Hilfsfunktion mit def.
"""

from functools import reduce


def gesamtminuten(tickets):
    """Summe der Bearbeitungsminuten aller Tickets."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def dringendstes(tickets):
    """Das erste Ticket mit der kleinsten Prioritätszahl, None bei leerer Liste."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def minuten_je_kategorie(tickets):
    """Dictionary Kategorie → Summe der Minuten, in der Reihenfolge des ersten Vorkommens."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


tickets = [
    {"nummer": 1, "prioritaet": 3, "kategorie": "Drucker", "minuten": 20},
    {"nummer": 2, "prioritaet": 1, "kategorie": "Netzwerk", "minuten": 45},
    {"nummer": 3, "prioritaet": 1, "kategorie": "Drucker", "minuten": 10},
]
print(gesamtminuten(tickets), dringendstes(tickets)["nummer"], minuten_je_kategorie(tickets))
