"""Aufgabe 2_022 – Reaktionsfristen                              Stufe 2 ★★☆☆☆

Ein Systemhaus betreut die Rechner mehrerer Kunden. Im Vertrag, dem
Service Level Agreement (SLA), steht für jedes Ticket eine
Reaktionsfrist: Innerhalb so vieler Minuten muss sich jemand vom Support
melden. Am Monatsende will die Teamleitung sehen, bei welchen Tickets das
nicht geklappt hat. Das Ticketsystem exportiert dafür drei gleich lange
Listen: die Ticketnummern, die Fristen in Minuten und die tatsächlichen
Reaktionszeiten in Minuten. An derselben Stelle stehen jeweils die Daten
desselben Tickets.

Schreiben Sie zwei Funktionen:

- `verletzte_tickets(nummern, fristen, reaktionen)` gibt die Nummern der
  Tickets zurück, deren Reaktionszeit größer als die Frist war, in der
  Reihenfolge der Listen. Genau zur Frist zu reagieren ist noch
  rechtzeitig.
- `einhaltungsquote(fristen, reaktionen)` gibt zurück, bei wie viel
  Prozent der Tickets die Frist eingehalten wurde, als ganze Zahl
  abgerundet (also mit //). Gibt es keine Tickets, gibt sie None zurück.

    nummern    = ["T-101", "T-102", "T-103", "T-104"]
    fristen    = [60, 240, 60, 30]
    reaktionen = [45, 300, 60, 31]
    verletzte_tickets(nummern, fristen, reaktionen)   →  ["T-102", "T-104"]
    einhaltungsquote(fristen, reaktionen)             →  50
    einhaltungsquote([60, 60, 60], [1, 2, 99])        →  66

Grenzen: Die drei Listen sind gleich lang, 0 bis 100 000 Einträge. Die
Nummern sind verschiedene Texte, die Fristen ganze Zahlen von 1 bis
10 000, die Reaktionszeiten ganze Zahlen von 0 bis 100 000.

Hintergrund: zip(a, b) läuft über zwei Listen zugleich und liefert bei
jedem Durchlauf ein Tupel mit je einem Element aus jeder Liste, das man
in der for-Zeile auspackt:

    for name, alter in zip(["Ada", "Alan"], [36, 41]):
        print(name, alter)          →  Ada 36, Alan 41

Das geht mit beliebig vielen Listen: zip(a, b, c) liefert Dreiertupel.
Sind die Listen verschieden lang, hört zip bei der kürzesten auf. Ohne
zip müsste man mit range(len(a)) über die Indizes laufen und a[i], b[i]
und c[i] einzeln nachschlagen.
"""


def verletzte_tickets(nummern, fristen, reaktionen):
    """Gibt die Nummern der Tickets zurück, deren Reaktionszeit über der Frist lag."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def einhaltungsquote(fristen, reaktionen):
    """Gibt den Anteil rechtzeitiger Reaktionen in ganzen Prozent (abgerundet) zurück, None ohne Tickets."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


nummern = ["T-101", "T-102", "T-103", "T-104"]
fristen = [60, 240, 60, 30]
reaktionen = [45, 300, 60, 31]
print(verletzte_tickets(nummern, fristen, reaktionen))
print(einhaltungsquote(fristen, reaktionen))
