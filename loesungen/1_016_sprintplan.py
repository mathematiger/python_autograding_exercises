# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_016_sprintplan.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_016_sprintplan

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

ueberplant = geplant > kapazitaet
genau_passend = geplant == kapazitaet
luft_uebrig = geplant < kapazitaet

print("Überplant:", ueberplant)
print("Genau passend:", genau_passend)
print("Luft übrig:", luft_uebrig)


# Idee: Jede der drei Variablen bekommt das Ergebnis eines Vergleichs zwischen geplant und kapazitaet:
# > für überplant, == für genau passend, < für Luft übrig. Der Vergleich liefert direkt True oder False,
# print schreibt den Wert hinter den Text.
# Anderer Weg: über die Differenz, etwa ueberplant = geplant - kapazitaet > 0; oder luft_uebrig =
# kapazitaet > geplant mit vertauschten Seiten. Beides ergibt dasselbe.
# Typische Fehler: = statt == (genau_passend = geplant = kapazitaet ist eine doppelte Zuweisung, dann
# steht eine Zahl statt True oder False da und geplant ist überschrieben),
# >= statt > (dann ist ein genau passender Plan auch überplant) oder die Seiten vertauscht, sodass
# überplant und Luft übrig gerade andersherum herauskommen.
