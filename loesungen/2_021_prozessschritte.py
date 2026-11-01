# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_021_prozessschritte.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_021_prozessschritte

"""Aufgabe 2_021 – Prozessschritte                               Stufe 2 ★★☆☆☆

Ein Versandhändler will wissen, warum manche Bestellungen so lange
brauchen. Die Bearbeitung einer Bestellung besteht aus Prozessschritten,
die nacheinander ablaufen: Bestellung prüfen, Zahlung prüfen, Ware
kommissionieren (aus dem Lager zusammensuchen), verpacken, übergeben.
Die Software misst, wie viele Minuten jeder Schritt gedauert hat, und
speichert die Dauern als Liste in der Reihenfolge der Schritte. In den
Berichten werden die Schritte ab 1 nummeriert, nicht ab 0.

Schreiben Sie zwei Funktionen:

- `zu_lange(dauern, soll)` gibt die Nummern (ab 1) aller Schritte, die
  länger als soll Minuten gedauert haben, als Liste zurück, in der
  Reihenfolge der Schritte.
- `engpass(dauern)` gibt die Nummer (ab 1) des Schritts mit der größten
  Dauer zurück, also den Engpass des Prozesses. Dauern mehrere Schritte
  gleich lang, zählt der erste davon. Bei einer leeren Liste gibt die
  Funktion None zurück.

    dauern = [4, 12, 35, 8, 35]
    zu_lange(dauern, 10)   →  [2, 3, 5]
    zu_lange(dauern, 35)   →  []
    engpass(dauern)        →  3
    engpass([])            →  None

Grenzen: 0 ≤ len(dauern) ≤ 100 000, jede Dauer ist eine ganze Zahl von 1
bis 10**6, ebenso soll.

Hintergrund: Oft braucht man in einer Schleife nicht nur den Wert,
sondern auch seine Position. Statt mit range(len(liste)) über die
Indizes zu laufen und liste[i] nachzuschlagen, liefert enumerate(liste)
bei jedem Durchlauf ein Paar (index, wert), das man in der for-Zeile
gleich in zwei Variablen auspackt:

    for index, wert in enumerate(["a", "b", "c"]):
        print(index, wert)          →  0 a, 1 b, 2 c

Mit enumerate(liste, start=1) beginnt die Zählung bei 1 statt bei 0;
die Werte bleiben dieselben. So muss man nirgends + 1 rechnen.

Tipp: Für engpass merken Sie sich die bisher größte Dauer und ihre
Nummer und ersetzen beide nur, wenn eine Dauer echt größer ist.
"""


def zu_lange(dauern, soll):
    """Gibt die Nummern (ab 1) der Schritte zurück, die länger als soll gedauert haben."""
    nummern = []
    for nummer, dauer in enumerate(dauern, start=1):
        if dauer > soll:
            nummern.append(nummer)
    return nummern


def engpass(dauern):
    """Gibt die Nummer (ab 1) des ersten längsten Schritts zurück, None bei leerer Liste."""
    beste_nummer = None
    beste_dauer = 0
    for nummer, dauer in enumerate(dauern, start=1):
        if dauer > beste_dauer:
            beste_nummer = nummer
            beste_dauer = dauer
    return beste_nummer


dauern = [4, 12, 35, 8, 35]
print(zu_lange(dauern, 10))
print(engpass(dauern))


# Idee: for nummer, dauer in enumerate(dauern, start=1) liefert bei jedem Durchlauf die Nummer ab 1
# und die Dauer zugleich. zu_lange sammelt die Nummern mit dauer > soll in einer Liste. engpass merkt
# sich die bisher größte Dauer und ihre Nummer und ersetzt beide nur bei dauer > beste_dauer; so bleibt
# bei gleich langen Schritten der erste stehen. Weil jede Dauer mindestens 1 ist, kann beste_dauer bei
# 0 beginnen, und bei leerer Liste bleibt beste_nummer None.
#
# Anderer Weg: for index in range(len(dauern)) mit dauern[index] und index + 1; das tut dasselbe,
# ist aber umständlicher. Für engpass geht auch dauern.index(max(dauern)) + 1, wenn man die leere
# Liste vorher abfängt.
#
# Typische Fehler: enumerate ohne start=1 (alle Nummern um eins zu klein), >= statt > (bei zu_lange
# zählt genau soll mit, bei engpass gewinnt der letzte statt der erste gleich lange Schritt) oder
# die Dauer statt der Nummer zurückgeben.
