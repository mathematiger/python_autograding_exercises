"""Aufgabe 3_034 – Verschachtelte Racks                          Stufe 3 ★★★☆☆

Die Inventarliste eines Rechenzentrums ist verschachtelt aufgebaut: Das
Rechenzentrum besteht aus Räumen, ein Raum aus Racks (Schränken), ein Rack
aus Servern oder aus Gehäusen, in denen wiederum mehrere Einschubserver
(Blades) stecken. Jeder Server steht als ganze Zahl für seinen Speicher in
GB da, jede Gruppe als Liste. Wie tief die Listen geschachtelt sind, ist
nicht festgelegt. Ein Beispiel mit einem Rack aus zwei Servern und einem
Gehäuse mit zwei Blades, daneben ein einzelner Server:

    anlage = [[512, 256, [128, 128]], 1024]

Vervollständigen Sie drei Funktionen, die sich jeweils selbst aufrufen:

- `gesamt(anlage)` liefert den Speicher aller Server zusammen.
- `tiefe(anlage)` liefert, wie viele Listen höchstens ineinanderstecken.
  Eine Liste ohne innere Liste (auch die leere) hat die Tiefe 1.
- `gespiegelt(anlage)` liefert die Ansicht von der Rückseite: eine neue
  Liste, in der die Reihenfolge auf allen Ebenen umgedreht ist. anlage
  selbst bleibt unverändert.

    gesamt(anlage)      →  2048
    tiefe(anlage)       →  3
    gespiegelt(anlage)  →  [1024, [[128, 128], 256, 512]]
    gesamt([])          →  0
    tiefe([])           →  1

Grenzen: anlage ist eine Liste, deren Elemente ganze Zahlen von 0 bis
10**6 oder wieder solche Listen sind; auch leere Listen kommen vor. Es
gibt höchstens 10 000 Zahlen und Listen insgesamt, und die Tiefe ist
höchstens 50. Benutzen Sie Rekursion, keinen eigenen Stapel.

Hintergrund: Eine Funktion darf sich selbst aufrufen (Rekursion, Aufgabe
3_005). Damit das endet, braucht sie eine Abbruchbedingung, bei der sie das
Ergebnis direkt kennt, und jeder Selbstaufruf bekommt ein kleineres
Teilproblem. Verschachtelte Listen passen genau dazu: Jede innere Liste ist
wieder eine Anlage, nur eine kleinere. Man geht die Elemente einer Ebene
durch; eine Zahl behandelt man direkt (Abbruchbedingung), eine Liste
übergibt man der Funktion selbst. Ob ein Element eine Liste ist, sagt
isinstance(element, list). Beispiel: wie viele Server gibt es?

    def anzahl(anlage):
        ergebnis = 0
        for element in anlage:
            if isinstance(element, list):
                ergebnis = ergebnis + anzahl(element)   # kleineres Teilproblem
            else:
                ergebnis = ergebnis + 1                 # ein Server
        return ergebnis

Bei der leeren Liste läuft die Schleife gar nicht, und es kommt 0 heraus.
Jeder Aufruf merkt sich seine eigenen lokalen Variablen; das Ergebnis der
inneren Liste wird einfach zum Zwischenstand der äußeren addiert.

Tipp: Für tiefe ist die Tiefe einer Liste 1 plus die größte Tiefe ihrer
inneren Listen (0, wenn sie keine hat).
"""


def gesamt(anlage):
    """Gibt die Summe aller Zahlen in der verschachtelten Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def tiefe(anlage):
    """Gibt zurück, wie viele Listen höchstens ineinanderstecken (mindestens 1)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gespiegelt(anlage):
    """Gibt eine neue Liste zurück, in der die Reihenfolge auf allen Ebenen umgedreht ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


anlage = [[512, 256, [128, 128]], 1024]
print(gesamt(anlage), tiefe(anlage), gespiegelt(anlage))
