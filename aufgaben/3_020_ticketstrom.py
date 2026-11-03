"""Aufgabe 3_020 – Ticketstrom                                    Stufe 3 ★★★☆☆

Im Support eines Softwarehauses kommen neue Tickets nicht als fertige
Liste an, sondern als Strom: Das Ticketsystem liefert sie eins nach dem
anderen, und was einmal abgeholt ist, kommt kein zweites Mal. Die
Teamleitung verteilt die Tickets in Paketen an die Mitarbeitenden; jedes
Paket soll genau dort weitermachen, wo das vorige aufgehört hat.
Außerdem will sie wissen, wie viele Minuten die erledigten Tickets
zusammen gedauert haben. Schreiben Sie zwei Funktionen:

- `naechste_tickets(strom, anzahl)` bekommt einen Iterator strom und
  holt mit next() höchstens anzahl Tickets aus ihm, in ihrer
  Reihenfolge, und gibt sie als Liste zurück. Ist der Strom vorher
  erschöpft, enthält die Liste entsprechend weniger Tickets. Es darf kein
  Ticket mehr abgeholt werden als zurückgegeben wird, sonst wäre es
  verloren.
- `gesamtdauer(dauern)` bekommt etwas Durchlaufbares (eine Liste, ein
  Tupel, ein range oder einen Iterator) mit den Bearbeitungszeiten in
  Minuten und gibt ihre Summe zurück. Benutzen Sie dafür iter() und
  next() in einer while-Schleife, ohne for und ohne sum().

    strom = iter(["T-1", "T-2", "T-3", "T-4", "T-5"])
    naechste_tickets(strom, 2)        →  ["T-1", "T-2"]
    naechste_tickets(strom, 2)        →  ["T-3", "T-4"]
    naechste_tickets(strom, 2)        →  ["T-5"]
    naechste_tickets(strom, 2)        →  []
    gesamtdauer([15, 40, 5])          →  60

Grenzen: Der Strom liefert 0 bis 100 000 Tickets, nicht leere Texte.
anzahl ist eine ganze Zahl von 0 bis 100 000. dauern liefert 0 bis
100 000 ganze Zahlen von 0 bis 10**6. Ihre Lösung soll O(anzahl) bzw.
O(n) Schritte brauchen.

Hintergrund: Was tut for eigentlich? for x in werte fragt zuerst mit
iter(werte) nach einem Iterator, einem Objekt, das sich merkt, wie weit
man schon ist. Dann ruft for immer wieder next() auf diesem Iterator auf
und bekommt jedes Mal das nächste Element. Gibt es keins mehr, löst
next() die Ausnahme StopIteration aus, und for hört auf. Dasselbe von
Hand:

    zeiger = iter(["a", "b"])
    print(next(zeiger))      # a
    print(next(zeiger))      # b
    next(zeiger)             # StopIteration

Eine Liste selbst merkt sich keine Position; jeder Aufruf iter(liste)
liefert einen neuen Iterator, der vorn anfängt. Ein Iterator dagegen
geht nur vorwärts: Was next() einmal geliefert hat, ist weg, und
iter(iterator) gibt denselben Iterator zurück. Deshalb macht ein
zweites Paket mit demselben Iterator dort weiter, wo das erste aufhört.
StopIteration fängt man wie jede andere Ausnahme mit try/except
(Aufgabe 3_007) ab.
"""


def naechste_tickets(strom, anzahl):
    """Holt höchstens anzahl Tickets aus dem Iterator strom und gibt sie als Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gesamtdauer(dauern):
    """Gibt die Summe aller Bearbeitungszeiten zurück, mit iter() und next() statt for."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


strom = iter(["T-1", "T-2", "T-3", "T-4", "T-5"])
print(naechste_tickets(strom, 2))
print(naechste_tickets(strom, 2))
print(naechste_tickets(strom, 2))
print(naechste_tickets(strom, 2))
print(gesamtdauer([15, 40, 5]))
