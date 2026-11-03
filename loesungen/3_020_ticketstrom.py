# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_020_ticketstrom.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_020_ticketstrom

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
    paket = []
    while len(paket) < anzahl:
        try:
            paket.append(next(strom))
        except StopIteration:
            break
    return paket


def gesamtdauer(dauern):
    """Gibt die Summe aller Bearbeitungszeiten zurück, mit iter() und next() statt for."""
    zeiger = iter(dauern)
    summe = 0
    while True:
        try:
            dauer = next(zeiger)
        except StopIteration:
            return summe
        summe = summe + dauer


strom = iter(["T-1", "T-2", "T-3", "T-4", "T-5"])
print(naechste_tickets(strom, 2))
print(naechste_tickets(strom, 2))
print(naechste_tickets(strom, 2))
print(naechste_tickets(strom, 2))
print(gesamtdauer([15, 40, 5]))


# Idee: naechste_tickets ruft next(strom) auf, solange das Paket noch nicht voll ist, und hängt jedes
# Ticket an. Die Prüfung steht vor dem Aufruf, damit nie ein Ticket zu viel abgeholt wird. Löst next()
# StopIteration aus, ist der Strom leer, und break beendet die Schleife. gesamtdauer holt sich mit
# iter(dauern) einen Iterator (eine Liste kann next() nicht) und macht dann von Hand, was for tut: next()
# in einer Endlosschleife, bis StopIteration kommt; dann ist die Summe fertig.
#
# Anderer Weg: In naechste_tickets eine for-Schleife über strom mit break, sobald das Paket voll ist;
# das geht, wenn break gleich nach dem append steht. Prüft man erst am Anfang des nächsten Durchlaufs, hat
# for das nächste Ticket schon geholt, und es ist verloren. Kürzer: list(itertools.islice(strom, anzahl))
# (Stufe 4).
#
# Typische Fehler: next(dauern) auf einer Liste (TypeError: 'list' object is not an iterator), len(strom)
# oder strom[0] auf einem Iterator, die Bedingung erst nach next() prüfen (ein Ticket geht verloren),
# StopIteration nicht abfangen (bei leerem Strom bricht das Programm ab) oder bei anzahl 0 trotzdem einmal
# next() aufrufen.
#
# Laufzeit: Jeder Aufruf von next() und jedes append kostet O(1); naechste_tickets braucht O(anzahl)
# Schritte, gesamtdauer O(n) für n Werte.
