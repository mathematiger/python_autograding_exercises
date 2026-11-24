"""Aufgabe 3_060 – Grenzwertpaare                                Stufe 3 ★★★☆☆

Ein Webshop verschickt Bestellungen ab einem Warenwert von genau
50,00 € versandkostenfrei. Für einen Grenzwerttest dieser Regel (wie in
Aufgabe 3_012) braucht die Testerin Warenkörbe, die genau auf dem Grenzwert
liegen, und will wissen, wie viele Warenkörbe darunter bleiben. Damit
die Testfälle einfach bleiben, besteht jeder Warenkorb aus genau zwei
verschiedenen Artikeln. Die Preise aller Artikel kommen aus dem Katalog,
in Cent und aufsteigend sortiert:

    preise = [499, 1250, 1999, 2490, 3001, 3990, 4800]

Schreiben Sie zwei Funktionen, beide mit der Zwei-Zeiger-Technik:

- `paar_mit_summe(preise, ziel)` gibt ein Paar (i, j) von Positionen
  mit i < j zurück, für das preise[i] + preise[j] == ziel ist, oder
  None, wenn es keins gibt. Gibt es mehrere, ist jedes richtig.
- `anzahl_unter(preise, grenze)` gibt zurück, wie viele Paare (i, j) mit
  i < j es gibt, für die preise[i] + preise[j] < grenze ist, also wie
  viele Warenkörbe aus zwei Artikeln noch Versandkosten kosten.

    paar_mit_summe(preise, 5000)    →  (2, 4)     (19,99 € + 30,01 €)
    paar_mit_summe(preise, 6250)    →  None
    anzahl_unter(preise, 5000)      →  9

Zwei Artikel können gleich viel kosten; dann stehen beide Preise in der
Liste. Ein Artikel darf aber nicht mit sich selbst gepaart werden.

Grenzen: preise hat 0 bis 100 000 Einträge, ganze Zahlen von 1 bis
1 000 000, aufsteigend sortiert, Doppelte möglich. ziel und grenze sind
ganze Zahlen von 1 bis 2 000 000. Beide Funktionen sollen O(n) Schritte
brauchen, also höchstens einige Zugriffe auf preise je Eintrag.

Hintergrund: Die naive Lösung probiert jedes Paar mit zwei
verschachtelten Schleifen: n · (n - 1) / 2 Paare, bei 100 000 Preisen
fast fünf Milliarden, also O(n²) (Aufgabe 3_006). Weil die Liste
sortiert ist, geht es mit zwei Zeigern in einem Durchgang. Der Zeiger
links steht am Anfang, rechts am Ende. Ist die Summe der beiden Preise
zu klein, hilft nur ein größerer Preis links, also links += 1. Ist sie
zu groß, hilft nur ein kleinerer rechts, also rechts -= 1. Stimmt sie,
ist man fertig:

    links, rechts = 0, len(werte) - 1
    while links < rechts:
        summe = werte[links] + werte[rechts]
        if summe == ziel:
            ...
        elif summe < ziel:
            links += 1
        else:
            rechts -= 1

Warum geht dabei kein Paar verloren? Ist werte[links] + werte[rechts] zu
klein, ist werte[links] mit jedem anderen Wert erst recht zu klein,
denn alle anderen Werte zwischen den Zeigern sind höchstens
werte[rechts]. Der linke Wert kann also aussortiert werden. Das ist die
Invariante der Schleife (Aufgabe 2_058): Jedes Paar, das noch in Frage
kommt, liegt zwischen den beiden Zeigern. Bei jedem Durchlauf rückt ein
Zeiger, nach höchstens n Durchläufen treffen sie sich: O(n). Zwei
Zeiger kennen Sie schon aus dem Zusammenführen sortierter Listen in
Aufgabe 2_055 (und im Merge Sort, 3_005); dort
liefen beide in dieselbe Richtung, hier laufen sie aufeinander zu.

Tipp: Bei anzahl_unter zählt ein zu kleines Paar gleich mehrfach: Ist
werte[links] + werte[rechts] < grenze, dann gilt das auch für
werte[links] mit jedem Wert zwischen links und rechts.
"""


def paar_mit_summe(preise, ziel):
    """Gibt Positionen (i, j) mit i < j und preise[i] + preise[j] == ziel zurück, oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def anzahl_unter(preise, grenze):
    """Gibt die Anzahl der Paare i < j mit preise[i] + preise[j] < grenze zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


preise = [499, 1250, 1999, 2490, 3001, 3990, 4800]
print(paar_mit_summe(preise, 5000))
print(anzahl_unter(preise, 5000))
