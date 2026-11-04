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

Grenzen: jahreskosten liefert 1 bis 100 000 ganze Zahlen von 0 bis
10**9. angebot_a und angebot_b liefern gleich viele, 0 bis 100 000,
solche Zahlen. Jedes Argument kann eine Liste, ein Tupel, ein range
oder ein Iterator sein und darf daher nur einmal durchlaufen werden; es
hat nicht unbedingt len() oder Indizes.

Hintergrund: In Aufgabe 3_020 haben Sie gesehen, dass ein Iterator nur
vorwärts geht. Viele eingebaute Funktionen liefern keine Liste, sondern
einen Iterator: zip(a, b) liefert die Paare, map(funktion, werte) ruft
die Funktion nacheinander für jeden Wert auf und liefert die
Ergebnisse (map(int, ["3", "4"]) liefert 3 und 4), reversed(liste)
liefert die Elemente von hinten. Ein solcher Iterator berechnet jedes
Element erst, wenn es gebraucht wird, und ist nach einem Durchlauf
verbraucht:

    zahlen = map(int, ["3", "4"])
    print(sum(zahlen))     # 7
    print(sum(zahlen))     # 0, der Iterator ist leer
    max(zahlen)            # ValueError: max() arg is an empty sequence

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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def differenzen(angebot_a, angebot_b):
    """Gibt die Liste der Differenzen b - a je Jahr zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def vergleich(angebot_a, angebot_b):
    """Gibt (Summe der Differenzen b - a, Anzahl der Jahre mit B günstiger) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kauf = [1200, 300, 300, 300]
leasing = [500, 500, 500, 500]
print(kostenbericht(kauf))
print(kostenbericht(map(int, "500;500;500".split(";"))))
print(differenzen(kauf, leasing))
print(vergleich(iter(kauf), reversed(leasing)))
