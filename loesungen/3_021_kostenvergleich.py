# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_021_kostenvergleich.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_021_kostenvergleich

"""Aufgabe 3_021 – Kostenvergleich                              Stufe 3 ★★★☆☆

Eine Schule will neue Laptops anschaffen und vergleicht zwei Angebote
über die ganze Nutzungsdauer: Kauf mit hohen Kosten im ersten Jahr und
danach nur Wartung, oder Leasing mit gleichen Raten in jedem Jahr. Die
Kosten je Jahr in Euro kommen aus einer Tabellenkalkulation, mal als
Liste, mal als Iterator, etwa aus map(int, zeile.split(";")) oder aus
reversed(…). Schreiben Sie drei Funktionen, die mit beidem richtig
rechnen:

- `kostenbericht(jahreskosten)` gibt das Tupel (summe, hoechste,
  jahre) zurück: die Summe aller Jahreskosten, die höchsten Kosten
  eines Jahres und die Anzahl der Jahre.
- `differenzen(angebot_a, angebot_b)` gibt eine Liste (keinen Iterator)
  zurück, die für jedes Jahr b - a enthält. Ist der Wert negativ, ist B
  in diesem Jahr günstiger.
- `vergleich(angebot_a, angebot_b)` gibt das Tupel (gesamt, jahre_b)
  zurück: gesamt ist die Summe der Differenzen b - a über alle Jahre,
  jahre_b die Anzahl der Jahre, in denen B günstiger ist. Benutzen Sie
  dafür differenzen.

    kauf = [1200, 300, 300, 300]
    leasing = [500, 500, 500, 500]
    kostenbericht(kauf)                          →  (2100, 1200, 4)
    kostenbericht(map(int, "500;500;500".split(";")))  →  (1500, 500, 3)
    differenzen(kauf, leasing)                   →  [-700, 200, 200, 200]
    vergleich(kauf, leasing)                     →  (-100, 1)
    vergleich(iter(kauf), reversed(leasing))     →  (-100, 1)

Grenzen: jahreskosten liefert 1 bis 30 ganze Zahlen von 0 bis 10**7.
angebot_a und angebot_b liefern gleich viele, 0 bis 30, solche Zahlen.
Jedes Argument kann eine Liste, ein Tupel, ein range oder ein Iterator
sein und darf daher nur einmal durchlaufen werden; es hat nicht
unbedingt len() oder Indizes.

Hintergrund: In Aufgabe 3_020 haben Sie gesehen, dass ein Iterator nur
vorwärts geht. Viele eingebaute Funktionen liefern keine Liste, sondern
einen Iterator: zip(a, b) liefert die Paare, map(funktion, werte) ruft
die Funktion nacheinander für jeden Wert auf und liefert die
Ergebnisse (map(int, ["3", "4"]) liefert 3 und 4), reversed(liste)
liefert die Elemente von hinten. sum(werte) liefert die Summe aller
Werte, max(werte) den größten (Aufgabe 2_010). Ein solcher Iterator berechnet jedes
Element erst, wenn es gebraucht wird, und ist nach einem Durchlauf
verbraucht:

    zahlen = map(int, ["3", "4"])
    print(sum(zahlen))     # 7
    print(sum(zahlen))     # 0, der Iterator ist leer
    max(zahlen)            # ValueError, der Iterator ist leer

Eine Liste dagegen kann man beliebig oft durchlaufen, weil jedes for
mit iter(liste) einen neuen Iterator holt, der vorn anfängt. Braucht man
die Werte mehr als einmal, sammelt man sie deshalb zuerst mit
werte = list(jahreskosten) in einer Liste und rechnet dann mit ihr. Aus
demselben Grund sollte eine Funktion, deren Ergebnis man mehrmals
benutzen will, eine Liste zurückgeben: return list(zip(a, b)) statt
return zip(a, b).
"""


def kostenbericht(jahreskosten):
    """Gibt (summe, hoechste, jahre) der Jahreskosten zurück."""
    werte = list(jahreskosten)
    return sum(werte), max(werte), len(werte)


def differenzen(angebot_a, angebot_b):
    """Gibt die Liste der Differenzen b - a je Jahr zurück."""
    return [b - a for a, b in zip(angebot_a, angebot_b)]


def vergleich(angebot_a, angebot_b):
    """Gibt (Summe der Differenzen b - a, Anzahl der Jahre mit B günstiger) zurück."""
    unterschiede = differenzen(angebot_a, angebot_b)
    jahre_b = 0
    for unterschied in unterschiede:
        if unterschied < 0:
            jahre_b = jahre_b + 1
    return sum(unterschiede), jahre_b


kauf = [1200, 300, 300, 300]
leasing = [500, 500, 500, 500]
print(kostenbericht(kauf))
print(kostenbericht(map(int, "500;500;500".split(";"))))
print(differenzen(kauf, leasing))
print(vergleich(iter(kauf), reversed(leasing)))


# Idee: kostenbericht braucht die Werte dreimal (Summe, Maximum, Anzahl). Darum sammelt es sie zuerst mit
# list(jahreskosten) in einer Liste, die man beliebig oft durchlaufen kann; danach sind sum, max und len
# einfach. differenzen läuft mit zip durch beide Angebote zugleich und sammelt b - a mit einer List
# Comprehension (Aufgabe 3_017) in einer Liste.
# vergleich braucht die Differenzen zweimal, für die Summe und für das Zählen; weil differenzen eine Liste
# liefert, geht das ohne Weiteres.
#
# Anderer Weg: kostenbericht in einem einzigen Durchlauf mit for und drei Variablen summe, hoechste und
# jahre; das kommt ohne Liste aus und braucht weniger Speicher. differenzen geht auch mit einer
# for-Schleife über zip(angebot_a, angebot_b), die b - a mit append an eine leere Liste anhängt.
#
# Typische Fehler: sum(jahreskosten) und dann max(jahreskosten) auf einem Iterator (ValueError, weil er schon
# leer ist), len(jahreskosten) auf einem Iterator (TypeError), in differenzen return zip(…) oder map(…)
# statt einer Liste (dann liefert der zweite Durchlauf in vergleich nichts mehr) und in vergleich
# <= 0 statt < 0.
#
# Laufzeit: Jede Funktion geht jeden Wert einmal (bzw. eine feste Anzahl von Malen) durch, also O(n) für n
# Jahre; die Liste braucht zusätzlich O(n) Speicher.
