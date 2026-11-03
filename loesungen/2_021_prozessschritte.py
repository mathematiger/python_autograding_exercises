# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_021_prozessschritte.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_021_prozessschritte

"""Aufgabe 2_021 – Prozessschritte                               Stufe 2 ★★☆☆☆

Ein Systemhaus richtet für neue Mitarbeitende Laptops ein. Jede
Einrichtung läuft in festen Schritten ab: Gerät auspacken, Betriebssystem
installieren, Software verteilen, Konto anlegen und so weiter. Das Team
hat gemessen, wie viele Minuten jeder Schritt gedauert hat, und die
Dauern in der Reihenfolge der Schritte in einer Liste gespeichert. Der
erste Schritt hat die Nummer 1:

    dauern = [5, 42, 18, 42, 7]     # Schritt 1 bis 5

Geplant (der Sollwert) sind höchstens soll Minuten pro Schritt. Schreiben
Sie zwei Funktionen:

- `zu_lange(dauern, soll)` gibt die Nummern aller Schritte zurück, die
  länger als soll gedauert haben, als Liste in der Reihenfolge der
  Schritte.
- `engpass(dauern)` gibt die Nummer des Schritts zurück, der am längsten
  gedauert hat. Dauern mehrere Schritte gleich lange, zählt der erste.

    zu_lange([5, 42, 18, 42, 7], 15)   →  [2, 3, 4]
    zu_lange([5, 42, 18, 42, 7], 42)   →  []
    engpass([5, 42, 18, 42, 7])        →  2

Benutzen Sie in beiden Funktionen enumerate und nicht max() oder
liste.index(...).

Grenzen: dauern hat 1 bis 100 000 Einträge, alle ganze Zahlen von 0 bis
10 000. soll ist eine ganze Zahl von 0 bis 10 000.

Hintergrund: Eine for-Schleife über eine Liste liefert nur die Werte.
Braucht man zusätzlich die Position, liefert enumerate(liste) bei jedem
Durchlauf ein Paar aus Zähler und Wert, das man gleich in zwei
Variablen auspackt:

    for index, wert in enumerate(["a", "b", "c"]):
        print(index, wert)          # 0 a, dann 1 b, dann 2 c

Normalerweise beginnt der Zähler bei 0, wie die Indizes einer Liste. Mit
enumerate(liste, start=1) beginnt er bei 1; das ist praktisch, wenn
Menschen die Einträge ab 1 zählen. Das ersetzt die umständlichere Form
for index in range(len(liste)) mit liste[index] in der Schleife.
"""


def zu_lange(dauern, soll):
    """Gibt die Nummern (ab 1) der Schritte zurück, die länger als soll gedauert haben."""
    nummern = []
    for nummer, dauer in enumerate(dauern, start=1):
        if dauer > soll:
            nummern.append(nummer)
    return nummern


def engpass(dauern):
    """Gibt die Nummer (ab 1) des ersten Schritts mit der längsten Dauer zurück."""
    beste_nummer = 1
    laengste = dauern[0]
    for nummer, dauer in enumerate(dauern, start=1):
        if dauer > laengste:
            beste_nummer = nummer
            laengste = dauer
    return beste_nummer


dauern = [5, 42, 18, 42, 7]
print(zu_lange(dauern, 15))
print(engpass(dauern))


# Idee: for nummer, dauer in enumerate(dauern, start=1) liefert Nummer und Dauer zugleich. Für
# zu_lange kommt jede Nummer mit dauer > soll in die Ergebnisliste. Für engpass merkt man sich die
# Nummer und die Dauer des bisher längsten Schritts und ersetzt beide nur, wenn ein Schritt echt
# länger dauert; so bleibt bei Gleichstand der erste stehen.
#
# Anderer Weg: enumerate ohne start und am Ende index + 1 zurückgeben. Für engpass kann man sich auch
# nur die Nummer merken und mit dauern[beste_nummer - 1] vergleichen. Mit fertigen Mitteln
# ginge es als dauern.index(max(dauern)) + 1, das war hier aber nicht verlangt.
#
# Typische Fehler: den Index ab 0 statt der Nummer ab 1 zurückgeben, >= statt > (dann zählt
# genau soll als zu lang oder bei engpass der letzte von mehreren gleich langen Schritten), oder die
# Dauer statt der Nummer zurückgeben.
