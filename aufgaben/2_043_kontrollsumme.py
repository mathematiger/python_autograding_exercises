"""Aufgabe 2_043 – Kontrollsumme                                 Stufe 2 ★★☆☆☆

Ein Betrieb zieht seine Buchungsdaten aus einem alten System in eine neue
Datenbank um. Jede Exportdatei enthält eine Liste von Beträgen in Euro und
am Ende eine Kontrollsumme, die das alte System ausgerechnet hat. Vor dem
Import prüft ein Skript die Datenqualität: Stimmt die Summe der Beträge
nicht mit der Kontrollsumme überein, fehlt eine Buchung oder ist verfälscht,
und die Datei wird abgelehnt. Das erste Skript hat mit == verglichen und
dabei auch korrekte Dateien abgelehnt, denn in Python ist 0.1 + 0.2 == 0.3
falsch.

- `fast_gleich(a, b)` gibt True zurück, wenn sich die Zahlen a und b um
  weniger als TOLERANZ unterscheiden (egal, welche größer ist), sonst
  False.
- `summe_stimmt(betraege, kontrollsumme)` gibt True zurück, wenn die Summe
  der Liste betraege und kontrollsumme fast gleich sind. Benutzen Sie
  dafür fast_gleich.

    0.1 + 0.2 == 0.3                       →  False
    fast_gleich(0.1 + 0.2, 0.3)            →  True
    fast_gleich(19.99, 20.0)               →  False
    summe_stimmt([0.1, 0.2], 0.3)          →  True
    summe_stimmt([12.5, 7.49, 0.01], 20.0) →  True
    summe_stimmt([12.5, 7.49], 20.0)       →  False

Grenzen: 0 ≤ len(betraege) ≤ 10 000. Alle Beträge und die Kontrollsumme
haben höchstens zwei Nachkommastellen (Cent), jeder Betrag liegt zwischen
-100 000 und 100 000 Euro (Gutschriften sind negativ), die Kontrollsumme
zwischen -10**9 und 10**9. Bei fast_gleich sind a und b beliebige
Kommazahlen zwischen -10**9 und 10**9. Die leere Liste hat die Summe 0.

Hintergrund: Der Rechner speichert Kommazahlen (float) im Zweiersystem. So
wie 1/3 im Zehnersystem nicht genau als 0.333… hinzuschreiben ist, lässt
sich 0.1 im Zweiersystem nicht genau darstellen. Gespeichert wird die
nächstgelegene Zahl, und die weicht ein winziges Stück ab:

    0.1 + 0.2              →  0.30000000000000004
    0.1 + 0.2 == 0.3       →  False

Beim Addieren vieler Beträge sammeln sich solche Abweichungen an. Darum
vergleicht man Kommazahlen nie mit ==, sondern prüft, ob ihr Abstand
kleiner als eine kleine Toleranz (oft epsilon genannt) ist:

    abs(a - b) < 0.000001

abs(x) ist der Betrag von x, also der Abstand ohne Vorzeichen: abs(-0.5)
ist 0.5. Wie groß die Toleranz sein darf, hängt von den Daten ab. Hier
sind alle Beträge auf den Cent genau, zwei verschiedene echte Summen
unterscheiden sich also um mindestens 0.01. Ein Unterschied unter einem
halben Cent (TOLERANZ = 0.005) kann nur ein Rundungsfehler sein, einer
ab 0.01 ist eine echte Abweichung.
"""

TOLERANZ = 0.005


def fast_gleich(a, b):
    """Gibt zurück, ob sich a und b um weniger als TOLERANZ unterscheiden."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def summe_stimmt(betraege, kontrollsumme):
    """Gibt zurück, ob die Summe der Beträge zur Kontrollsumme passt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(0.1 + 0.2 == 0.3, fast_gleich(0.1 + 0.2, 0.3), summe_stimmt([12.5, 7.49], 20.0))
