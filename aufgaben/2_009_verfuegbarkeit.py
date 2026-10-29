"""Aufgabe 2_009 – Verfügbarkeit                                 Stufe 2 ★★☆☆☆

Ein Rechenzentrum garantiert seinen Kunden im Vertrag eine Verfügbarkeit,
zum Beispiel 99.9 Prozent: In höchstens 0.1 Prozent der Zeit darf ein Dienst
ausfallen. Das Monitoring zählt jeden Monat, wie viele Minuten ein Dienst
nicht erreichbar war. Die Verfügbarkeit in Prozent ist der Anteil der Zeit,
in der er lief:

    Verfügbarkeit = (Gesamtminuten - Ausfallminuten) / Gesamtminuten * 100

Vervollständigen Sie zwei Funktionen:

- `verfuegbarkeit(ausfall, gesamt)` gibt die Verfügbarkeit in Prozent zurück.
- `ziel_erreicht(ausfall, gesamt, ziel)` gibt True zurück, wenn die
  Verfügbarkeit mindestens ziel Prozent beträgt, sonst False. Rechnen Sie
  die Verfügbarkeit hier nicht noch einmal aus, sondern rufen Sie
  verfuegbarkeit(...) auf.

Ein Monat mit 30 Tagen hat 43200 Minuten:

    verfuegbarkeit(30, 43200)          →  99.93055555555556
    verfuegbarkeit(0, 43200)           →  100.0
    ziel_erreicht(30, 43200, 99.9)     →  True
    ziel_erreicht(60, 43200, 99.9)     →  False
    ziel_erreicht(5, 1000, 99.5)       →  True   (genau erreicht zählt)

Grenzen: gesamt und ausfall sind ganze Zahlen mit 1 ≤ gesamt ≤ 10**6 und
0 ≤ ausfall ≤ gesamt. ziel ist eine Zahl mit 0 ≤ ziel ≤ 100.

Hintergrund: Eine Funktion darf andere Funktionen aufrufen, auch selbst
geschriebene. Die aufgerufene heißt dann Hilfsfunktion. Ihr Ergebnis kann man
direkt weiterverwenden:

    def quadrat(x):
        return x * x

    def flaeche_zwei_quadrate(a, b):
        return quadrat(a) + quadrat(b)

So steht jede Formel nur an einer Stelle. Findet man darin einen Fehler oder
ändert sich die Formel, korrigiert man sie einmal, und alle Funktionen, die
sie benutzen, rechnen danach richtig.

Tipp: Ein Vergleich wie a >= b ergibt schon True oder False; den können Sie
direkt mit return zurückgeben.
"""


def verfuegbarkeit(ausfall, gesamt):
    """Gibt den Anteil der Minuten ohne Ausfall in Prozent zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ziel_erreicht(ausfall, gesamt, ziel):
    """Gibt zurück, ob die Verfügbarkeit mindestens ziel Prozent beträgt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(verfuegbarkeit(30, 43200))
print(ziel_erreicht(30, 43200, 99.9))
