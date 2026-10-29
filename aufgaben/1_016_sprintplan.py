"""Aufgabe 1_016 – Sprintplan                                    Stufe 1 ★☆☆☆☆

Ein Entwicklungsteam arbeitet in Sprints, also in Abschnitten von zwei
Wochen. Jede Aufgabe im Sprint ist in Story Points geschätzt, einer Zahl
für den Aufwand. Aus den letzten Sprints weiß das Team, wie viele Story
Points es in einem Sprint schafft; das ist seine Kapazität. Vor dem Start
prüft das Planungsprogramm, ob der Plan zur Kapazität passt.

Das Programm fragt schon nach den geplanten Story Points und der
Kapazität. Ergänzen Sie die drei Zeilen, die die Variablen ueberplant,
genau_passend und luft_uebrig füllen:

- ueberplant ist True, wenn mehr Punkte geplant sind, als das Team schafft.
- genau_passend ist True, wenn genau so viele Punkte geplant sind.
- luft_uebrig ist True, wenn weniger Punkte geplant sind.

Bei den Eingaben 34 und 30 soll das Programm ausgeben:

    Überplant: True
    Genau passend: False
    Luft übrig: False

Grenzen: Beide Eingaben sind ganze Zahlen von 0 bis 200.

Hintergrund: Ein Vergleich wie a > b liefert keinen Text und keine Zahl,
sondern einen Wahrheitswert: True (wahr) oder False (falsch). Diesen Wert
kann man wie jeden anderen in einer Variablen speichern und ausgeben. Die
Vergleiche sind == (gleich), != (ungleich), < (kleiner), > (größer),
<= (kleiner oder gleich) und >= (größer oder gleich). Achtung: Ein
einzelnes = speichert einen Wert in einer Variablen, erst == vergleicht.
"""

geplant = int(input("Geplante Story Points: "))
kapazitaet = int(input("Kapazität des Teams: "))

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print("Überplant:", ueberplant)
print("Genau passend:", genau_passend)
print("Luft übrig:", luft_uebrig)
