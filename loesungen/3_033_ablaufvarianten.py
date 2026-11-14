# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_033_ablaufvarianten.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_033_ablaufvarianten

"""Aufgabe 3_033 – Ablaufvarianten                              Stufe 3 ★★★☆☆

Eine Prozessanalystin untersucht, wie Anträge in einer Behörde bearbeitet
werden. Ein Antrag durchläuft n Prüfschritte nacheinander. Bei jedem
Arbeitsgang erledigt die Sachbearbeitung entweder einen Schritt oder, wenn
es schnell gehen soll, zwei Schritte auf einmal. Die Analystin will wissen,
wie viele verschiedene Abläufe es dabei gibt, um abzuschätzen, wie viele
Varianten eine Prozesssoftware abbilden müsste. Bei 4 Schritten sind es 5:

    1+1+1+1   1+1+2   1+2+1   2+1+1   2+2

Schreiben Sie die Funktion `ablaeufe(n)`. Überlegen Sie: Der erste
Arbeitsgang erledigt einen oder zwei Schritte; danach bleiben n - 1 oder
n - 2 Schritte übrig. Also ist ablaeufe(n) = ablaeufe(n - 1) +
ablaeufe(n - 2), mit ablaeufe(0) = 1 (nichts mehr zu tun: genau ein Ablauf)
und ablaeufe(1) = 1. Das sind die Fibonacci-Zahlen.

    ablaeufe(4)   →  5
    ablaeufe(10)  →  89
    ablaeufe(0)   →  1

Die Funktion soll rekursiv arbeiten und jedes Teilergebnis im vorgegebenen
Dictionary bekannt speichern, damit es nie zweimal berechnet wird.

Grenzen: 0 ≤ n ≤ 500, eine ganze Zahl. Jedes ablaeufe(k) für k ≤ n soll
höchstens einmal wirklich berechnet werden, die Laufzeit also O(n) sein.

Hintergrund: Rekursion (Aufgabe 3_005) ist hier sehr bequem, aber in der
einfachen Form furchtbar langsam: ablaeufe(30) ruft ablaeufe(29) und
ablaeufe(28) auf, ablaeufe(29) ruft wieder ablaeufe(28) auf, und so weiter.
Dieselben Werte werden immer wieder neu berechnet; die Zahl der Aufrufe
wächst wie die Fibonacci-Zahlen selbst, ungefähr wie 1.6 hoch n. Schon
ablaeufe(40) bräuchte Hunderte Millionen Aufrufe.

Memoisierung heißt: Ergebnisse merken. Vor dem Rechnen schaut die Funktion
in einem Dictionary nach, ob das Ergebnis schon bekannt ist, und gibt es
dann sofort zurück. Sonst rechnet sie es aus und trägt es ein:

    bekannt = {}

    def langsam_berechnet(k):
        if k in bekannt:
            return bekannt[k]
        ergebnis = ...  # wie bisher, mit rekursiven Aufrufen
        bekannt[k] = ergebnis
        return ergebnis

So wird jeder Wert nur einmal berechnet, danach nur noch nachgeschlagen.
"""

bekannt = {}


def ablaeufe(n):
    """Anzahl der Abläufe für n Schritte, wenn jeder Arbeitsgang einen oder zwei Schritte erledigt."""
    if n <= 1:
        return 1
    if n in bekannt:
        return bekannt[n]
    ergebnis = ablaeufe(n - 1) + ablaeufe(n - 2)
    bekannt[n] = ergebnis
    return ergebnis


print(ablaeufe(4))


# Idee: Für n ≤ 1 gibt es genau einen Ablauf. Sonst schaut die Funktion zuerst in bekannt nach; steht n
# dort, kommt das Ergebnis sofort zurück. Sonst rechnet sie ablaeufe(n - 1) + ablaeufe(n - 2), trägt das
# Ergebnis unter bekannt[n] ein und gibt es zurück.
# Anderer Weg: ohne Rekursion mit einer Schleife von unten nach oben, die nur die letzten beiden Werte
# kennt (O(n), O(1) Speicher). Oder mit @functools.lru_cache, das genau dieses Dictionary selbst anlegt
# (kommt in Stufe 4). Die naive Rekursion ohne bekannt braucht etwa 1.6 hoch n Aufrufe.
# Typische Fehler: das Ergebnis berechnen, aber nicht in bekannt eintragen (dann bleibt es langsam), das
# Nachschauen erst nach den rekursiven Aufrufen machen, oder bekannt in der Funktion neu anlegen
# (bekannt = {} bei jedem Aufruf vergisst alles wieder).
# Laufzeit: O(n). Jedes k von 2 bis n wird einmal berechnet, jede Berechnung macht zwei Aufrufe, von
# denen höchstens einer weiterrechnet; alle anderen sind sofort beantwortet.
