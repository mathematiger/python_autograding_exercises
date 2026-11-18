"""Aufgabe 4_034 – Amortisation                                  Stufe 4 ★★★★☆

Ein Betrieb überlegt, seine alten Server gegen sparsamere zu tauschen.
Die Anschaffung kostet einmalig investition Euro. Dafür sinkt die
Stromrechnung: Im ersten Jahr spart der Betrieb ersparnis Euro, und weil
der Strompreis steigt, spart er in jedem weiteren Jahr zuwachs Euro mehr
als im Vorjahr. Die Investition hat sich amortisiert („ist wieder
drin“), sobald die Ersparnisse zusammen mindestens so groß sind wie die
Anschaffungskosten. Lohnend ist sie nur, wenn das vor dem Ende der
Laufzeit passiert, also bevor die neuen Server selbst ausgetauscht
werden.

- `staende(investition, ersparnis, zuwachs)` ist eine Generatorfunktion.
  Sie liefert nacheinander den Stand am Ende von Jahr 1, 2, 3, …:
  Ersparnisse bis dahin minus Investition. Die Folge ist unendlich, der
  Generator endet nie.
- `amortisation(investition, ersparnis, zuwachs, laufzeit)` gibt das
  erste Jahr von 1 bis laufzeit zurück, an dessen Ende der Stand
  mindestens 0 ist, oder None, wenn das innerhalb der Laufzeit nie
  passiert. Benutzen Sie dafür staende und hören Sie im ersten
  passenden Jahr auf.

    stand = staende(10000, 3000, 500)
    next(stand), next(stand), next(stand), next(stand)
        →  (-7000, -3500, 500, 5000)
    amortisation(10000, 3000, 500, 10)  →  3
    amortisation(10000, 3000, 500, 2)   →  None

Grenzen: Alle Argumente sind ganze Zahlen mit 0 ≤ investition ≤ 10**9,
0 ≤ ersparnis ≤ 10**6, 0 ≤ zuwachs ≤ 10**5 und 1 ≤ laufzeit ≤ 10**5.
Ist investition 0, hat sich die Anschaffung schon im ersten Jahr
amortisiert. Sind ersparnis und zuwachs beide 0, amortisiert sie sich
bei investition > 0 nie. amortisation soll nach dem ersten passenden
Jahr keine weiteren Stände mehr berechnen.

Hintergrund: Eine Generatorfunktion (Aufgabe 3_022) enthält yield. Ihr
Aufruf führt noch keine Zeile aus, sondern liefert ein Generator-Objekt.
Erst jedes next(...) lässt den Rumpf bis zum nächsten yield laufen; dort
hält er an, und alle lokalen Variablen bleiben erhalten, bis das
nächste next(...) kommt. Man nennt das lazy („faule“) Auswertung: Es
wird nur berechnet, was jemand abholt. Deshalb darf ein Generator
unendlich sein, solange niemand alles haben will:

    def quadrate():
        zahl = 1
        while True:                # endet nie
            yield zahl * zahl
            zahl += 1

    folge = quadrate()
    next(folge), next(folge), next(folge)    →  (1, 4, 9)
    list(quadrate())                          # hört nie auf!

Wer aus einer unendlichen Folge etwas auswählt, muss selbst für ein Ende
sorgen. zip hört auf, sobald eines seiner Iterables erschöpft ist
(Aufgabe 3_021). Mit einem endlichen range daneben wird daraus eine
endliche Folge, und man bekommt die Nummer gleich mit:

    for nummer, wert in zip(range(1, 4), quadrate()):
        print(nummer, wert)        # 1 1, 2 4, 3 9 – dann ist range zu Ende

next(...) mit zwei Argumenten liefert den nächsten Wert oder, wenn der
Iterator schon erschöpft ist, statt StopIteration den zweiten Wert. Mit
einem Generator-Ausdruck (Aufgabe 3_023) findet man so das erste
passende Element oder einen Ersatzwert:

    next((q for q in [1, 4, 9] if q > 5), None)    →  9
    next((q for q in [1, 4, 9] if q > 50), None)   →  None

Beides zusammen findet in einer unendlichen Folge den ersten Treffer
innerhalb einer Grenze und hört genau dort auf; der Rest der Folge wird
nie berechnet.
"""


def staende(investition, ersparnis, zuwachs):
    """Liefert unendlich den Stand am Ende jedes Jahres: Ersparnisse bis dahin minus Investition."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def amortisation(investition, ersparnis, zuwachs, laufzeit):
    """Gibt das erste Jahr bis laufzeit mit Stand >= 0 zurück, sonst None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


stand = staende(10000, 3000, 500)
print(next(stand), next(stand), next(stand), next(stand))
print(amortisation(10000, 3000, 500, 10), amortisation(10000, 3000, 500, 2))
