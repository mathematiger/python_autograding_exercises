"""Aufgabe 2_022 – Reaktionsfristen                             Stufe 2 ★★☆☆☆

Ein IT-Dienstleister hat mit seinen Kunden vereinbart, wie schnell der
Support auf ein Ticket reagieren muss (ein Service Level Agreement, kurz
SLA). Die Frist hängt von der Priorität ab, darum hat jedes Ticket seine
eigene. Das Ticketsystem liefert drei Listen gleicher Länge: die
Ticketnummern, die vereinbarte Frist in Minuten und die tatsächliche
Reaktionszeit in Minuten. Der Eintrag an derselben Stelle gehört jeweils
zum selben Ticket:

    tickets   = ["T-101", "T-102", "T-103", "T-104"]
    fristen   = [60, 240, 30, 240]
    reaktion  = [45, 300, 30, 250]

Ein Ticket verletzt das SLA, wenn die Reaktionszeit größer als die Frist
ist; genau die Frist ist noch eingehalten. Schreiben Sie zwei Funktionen:

- `anzahl_verletzt(fristen, reaktion)` gibt zurück, bei wie vielen
  Tickets das SLA verletzt wurde.
- `ueberzogen(tickets, fristen, reaktion)` gibt für jedes Ticket, das das
  SLA verletzt, ein Tupel (ticket, minuten) zurück, wobei minuten angibt,
  um wie viel die Frist überschritten wurde. Die Tupel stehen in einer
  Liste in der Reihenfolge der Tickets.

    anzahl_verletzt(fristen, reaktion)          →  2
    ueberzogen(tickets, fristen, reaktion)      →  [("T-102", 60), ("T-104", 10)]

Benutzen Sie dafür zip.

Grenzen: Die drei Listen sind gleich lang, 0 bis 100 000 Einträge. Die
Ticketnummern sind nicht leere Texte ohne Wiederholung, Fristen und
Reaktionszeiten ganze Zahlen von 0 bis 100 000.

Hintergrund: zip(a, b) läuft durch zwei Listen zugleich. Bei jedem
Durchlauf liefert es ein Paar aus dem nächsten Element von a und dem
nächsten von b, das man gleich in zwei Variablen auspackt:

    for name, punkte in zip(["Ada", "Bo"], [7, 9]):
        print(name, punkte)          # Ada 7, dann Bo 9

zip nimmt auch drei oder mehr Listen; dann bekommt man bei jedem
Durchlauf ein Tupel mit drei Werten. Sind die Listen verschieden lang,
hört zip mit der kürzesten auf. Das ersetzt die Form for i in
range(len(a)) mit a[i] und b[i] in der Schleife.
"""


def anzahl_verletzt(fristen, reaktion):
    """Gibt zurück, bei wie vielen Tickets die Reaktionszeit über der Frist lag."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ueberzogen(tickets, fristen, reaktion):
    """Gibt (ticket, minuten über der Frist) für alle Tickets mit verletztem SLA zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


tickets = ["T-101", "T-102", "T-103", "T-104"]
fristen = [60, 240, 30, 240]
reaktion = [45, 300, 30, 250]
print(anzahl_verletzt(fristen, reaktion))
print(ueberzogen(tickets, fristen, reaktion))
