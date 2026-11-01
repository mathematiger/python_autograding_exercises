# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_022_reaktionsfristen.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_022_reaktionsfristen

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
    verletzt = []
    for nummer, frist, reaktion in zip(nummern, fristen, reaktionen):
        if reaktion > frist:
            verletzt.append(nummer)
    return verletzt


def einhaltungsquote(fristen, reaktionen):
    """Gibt den Anteil rechtzeitiger Reaktionen in ganzen Prozent (abgerundet) zurück, None ohne Tickets."""
    if len(fristen) == 0:
        return None
    eingehalten = 0
    for frist, reaktion in zip(fristen, reaktionen):
        if reaktion <= frist:
            eingehalten += 1
    return eingehalten * 100 // len(fristen)


nummern = ["T-101", "T-102", "T-103", "T-104"]
fristen = [60, 240, 60, 30]
reaktionen = [45, 300, 60, 31]
print(verletzte_tickets(nummern, fristen, reaktionen))
print(einhaltungsquote(fristen, reaktionen))


# Idee: for nummer, frist, reaktion in zip(nummern, fristen, reaktionen) liefert die drei Angaben
# desselben Tickets zusammen. verletzte_tickets sammelt die Nummer, wenn reaktion > frist ist.
# einhaltungsquote fängt zuerst die leere Liste ab, zählt dann mit zip(fristen, reaktionen) die
# Tickets mit reaktion <= frist und rechnet eingehalten * 100 // len(fristen).
#
# Anderer Weg: for i in range(len(nummern)) und nummern[i], fristen[i], reaktionen[i] einzeln
# nachschlagen; das tut dasselbe mit mehr Klammern. Die Quote lässt sich auch über die Zahl der
# verletzten Tickets rechnen: (len(fristen) - verletzt) * 100 // len(fristen).
#
# Typische Fehler: >= statt > (dann zählt eine Reaktion genau zur Frist als verletzt), eingehalten //
# len(fristen) * 100 (die Ganzzahldivision ergibt fast immer 0), / statt // (dann kommt 66.66… statt
# 66 heraus) oder die leere Liste nicht abfangen (ZeroDivisionError).
