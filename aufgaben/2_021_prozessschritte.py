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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def engpass(dauern):
    """Gibt die Nummer (ab 1) des ersten längsten Schritts zurück, None bei leerer Liste."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


dauern = [4, 12, 35, 8, 35]
print(zu_lange(dauern, 10))
print(engpass(dauern))
