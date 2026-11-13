"""Aufgabe 3_033 – Prüfabläufe zählen                            Stufe 3 ★★★☆☆

In der Qualitätssicherung einer Fertigung durchläuft jedes Werkstück n
Prüfstationen hintereinander. Ein Prüfer arbeitet die Stationen der Reihe
nach ab: Entweder er prüft eine Station allein, oder er fasst zwei
benachbarte Stationen zu einem Doppeldurchgang zusammen. Für die
Prozessanalyse will das Team wissen, wie viele verschiedene Abläufe es
gibt. Bei 4 Stationen sind es 5:

    1+1+1+1   1+1+2   1+2+1   2+1+1   2+2

Für den ersten Durchgang gibt es zwei Möglichkeiten: Er prüft eine Station
(danach bleiben n - 1) oder zwei (danach bleiben n - 2). Also ist

    abläufe(n) = abläufe(n - 1) + abläufe(n - 2),  abläufe(0) = abläufe(1) = 1

Das ist die Fibonacci-Folge 1, 1, 2, 3, 5, 8, 13, … Die rekursive Funktion
`ablaeufe_langsam` rechnet das genau so aus, ist aber schon bei 35
Stationen quälend langsam. Vervollständigen Sie `ablaeufe(n, merker)`: Sie
rechnet dasselbe rekursiv, schaut aber zuerst im Dictionary merker nach,
ob das Ergebnis für n schon bekannt ist, und trägt jedes neu berechnete
Ergebnis dort ein (merker[n] = …).

    ablaeufe(4, {})              →  5
    ablaeufe(50, {})             →  20365011074
    merker = {}
    ablaeufe(10, merker)         →  89, danach steht merker[10] == 89 darin
    ablaeufe(6, {5: 100, 4: 1})  →  101   (bekannte Werte werden benutzt)

Benutzen Sie nicht functools.lru_cache oder functools.cache.

Grenzen: n ist eine ganze Zahl mit 0 ≤ n ≤ 400. merker ist ein Dictionary,
leer oder mit Ergebnissen, die die Funktion wie gegeben übernimmt. Ihre
Lösung soll O(n) Schritte brauchen: Jedes Ergebnis wird höchstens einmal
berechnet.

Hintergrund: ablaeufe_langsam(5) ruft ablaeufe_langsam(4) und (3) auf,
ablaeufe_langsam(4) ruft wieder (3) und (2) auf, und so weiter. Dieselben
Werte werden immer wieder neu berechnet; die Zahl der Aufrufe wächst
ungefähr wie 1.6 hoch n, für n = 40 sind es über 300 Millionen
(Fibonacci-Beispiel aus MIT 6.0001, Lecture 6). Memoisierung (von
„Memo“, Notiz) heißt: Man notiert jedes Ergebnis in einem Dictionary und
schlägt dort nach, bevor man rechnet.

    def teuer(n, merker):
        if n in merker:
            return merker[n]          # schon bekannt: sofort fertig
        ergebnis = ...                # rekursiv rechnen wie bisher
        merker[n] = ergebnis          # für später notieren
        return ergebnis

Weil alle Aufrufe dasselbe Dictionary bekommen, wird jeder Wert nur einmal
berechnet: Aus exponentiell vielen Aufrufen werden ungefähr 2·n. Das
Dictionary wird als Parameter weitergereicht, damit jede Auswertung ihren
eigenen Merker mitbringt. In Stufe 4 kommt functools.lru_cache, das genau
das fertig erledigt.
"""


def ablaeufe_langsam(n):
    """Anzahl der Prüfabläufe für n Stationen, rekursiv ohne Merker (exponentiell langsam)."""
    if n <= 1:
        return 1
    return ablaeufe_langsam(n - 1) + ablaeufe_langsam(n - 2)


def ablaeufe(n, merker):
    """Anzahl der Prüfabläufe für n Stationen; merker enthält schon berechnete Ergebnisse {n: Anzahl}."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(ablaeufe(4, {}))
print(ablaeufe(10, {}))
