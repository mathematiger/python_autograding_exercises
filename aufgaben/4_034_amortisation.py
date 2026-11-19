"""Aufgabe 4_034 – Amortisation                                  Stufe 4 ★★★★☆

Ein Unternehmen überlegt, die alte Klimaanlage seines Serverraums durch
eine sparsamere zu ersetzen. Die neue Anlage kostet einmalig die
Investition und spart im ersten Jahr die Stromkosten ersparnis. Weil der
Strompreis steigt, wächst die Ersparnis jedes Jahr um steigerung. Die
Investition hat sich amortisiert (ist wieder hereingeholt), sobald die
Summe der Ersparnisse mindestens so groß ist wie die Investition.

Wie viele Jahre das dauert, weiß vorher niemand; darum soll keine Liste
mit fester Länge entstehen, sondern eine unendliche Folge, die Jahr für
Jahr erst dann berechnet wird, wenn jemand danach fragt.

- `salden(investition, ersparnis, steigerung)` ist ein Generator, der
  unendlich viele Paare (jahr, saldo) liefert: Jahr 1, 2, 3 … und den
  Saldo am Ende des Jahres, also Summe der Ersparnisse bis dahin minus
  Investition.
- `amortisationsjahr(investition, ersparnis, steigerung, laufzeit)` gibt
  das erste Jahr zurück, an dessen Ende der Saldo ≥ 0 ist, aber nur unter
  den ersten laufzeit Jahren (so lange hält die Anlage). Amortisiert sie
  sich in dieser Zeit nicht, kommt None zurück. Benutzen Sie dafür
  salden und next(..., None) mit Standardwert.

    folge = salden(10000, 3000, 500)
    next(folge)  →  (1, -7000)
    next(folge)  →  (2, -3500)        (im 2. Jahr 3500 gespart)
    next(folge)  →  (3, 500)          (im 3. Jahr 4000 gespart)
    amortisationsjahr(10000, 3000, 500, 15)  →  3
    amortisationsjahr(10000, 3000, 500, 2)   →  None
    amortisationsjahr(10000, 1000, 0, 15)    →  10    (Saldo genau 0)

Grenzen: Alle Werte sind ganze Zahlen mit 0 ≤ investition ≤ 10**9,
0 ≤ ersparnis ≤ 10**6, 0 ≤ steigerung ≤ 10**4 und
0 ≤ laufzeit ≤ 100 000. Ersparnis und Steigerung dürfen 0 sein; dann
amortisiert sich eine Investition über 0 nie. amortisationsjahr soll
nur so viele Jahre berechnen, wie es braucht: Amortisiert sich die
Anlage im Jahr 2, darf eine Laufzeit von 100 000 Jahren nichts kosten.

Hintergrund: In Aufgabe 3_022 haben Sie Generatoren kennengelernt: Eine
Funktion mit yield gibt beim Aufruf nicht sofort ein Ergebnis zurück,
sondern einen Generator, der bei jedem next() bis zum nächsten yield
weiterläuft und dort anhält. Diese Bedarfsauswertung (lazy evaluation)
hat eine überraschende Folge: Ein Generator darf unendlich sein. Eine
Liste aller Quadratzahlen passt in keinen Speicher, ein Generator
dagegen braucht nur den aktuellen Zustand:

    def quadratzahlen():
        zahl = 1
        while True:                 # endet nie, und das ist gewollt
            yield zahl * zahl
            zahl += 1

    folge = quadratzahlen()
    next(folge), next(folge), next(folge)   →  (1, 4, 9)

Gefährlich wird es nur, wenn man den ganzen Generator abholen will:
list(quadratzahlen()) oder for ohne break laufen endlos. Man nimmt sich
darum nur, was man braucht. Zwei Werkzeuge helfen dabei:

- zip hört auf, sobald eines seiner Iterables leer ist, und holt auch
  nur so viel ab. zip(range(5), quadratzahlen()) liefert fünf Paare und
  fragt den unendlichen Generator nur fünfmal.
- next(iterator, standard) liefert den nächsten Wert oder standard,
  wenn der Iterator leer ist, statt StopIteration auszulösen. Mit einem
  Generator-Ausdruck (Aufgabe 3_023) findet man so den ersten passenden
  Wert, ohne weiter zu rechnen:

    erste_grosse = next((q for q in quadratzahlen() if q > 50), None)   →  64
    next((q for _, q in zip(range(5), quadratzahlen()) if q > 50), None)   →  None
"""


def salden(investition, ersparnis, steigerung):
    """Liefert unendlich viele Paare (jahr, saldo am Jahresende)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def amortisationsjahr(investition, ersparnis, steigerung, laufzeit):
    """Gibt das erste Jahr mit Saldo ≥ 0 innerhalb der Laufzeit zurück, sonst None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(amortisationsjahr(10000, 3000, 500, 15))
