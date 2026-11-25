"""Aufgabe 5_061 – Wartungstour                                  Stufe 5 ★★★★★

Ein IT-Dienstleister wartet bei seinen Kunden vor Ort Server, Drucker
und Netzwerktechnik. Morgens bekommt eine Technikerin die Liste der
Kundenstandorte, die sie heute anfahren soll. Sie startet an der
Zentrale, fährt jeden Standort genau einmal an und kehrt am Ende zur
Zentrale zurück. Die Disposition kennt die Fahrzeiten zwischen allen
Orten in Minuten und will die Reihenfolge mit der kürzesten
Gesamtfahrzeit. Die Fahrzeiten stehen in einer Matrix fahrzeit:
fahrzeit[i][j] ist die Zeit von Ort i nach Ort j, Ort 0 ist die
Zentrale, die Kundenstandorte sind 1 bis n. Hin und zurück kann die
Zeit verschieden sein (Einbahnstraßen, Stau am Morgen).

Mit bis zu 15 Standorten gibt es 15! ≈ 1,3 · 10**12 Reihenfolgen; alle
durchzuprobieren wie in Aufgabe 4_046 dauert Tage. Schreiben Sie es
darum mit dynamischer Programmierung über Bitmasken (siehe
Hintergrund):

- `tourdauer(fahrzeit, reihenfolge)` gibt die Gesamtzeit der Tour
  zurück, die an der Zentrale beginnt, die Standorte der Liste
  reihenfolge nacheinander anfährt und zur Zentrale zurückkehrt. Ist
  reihenfolge leer, ist die Tour 0 Minuten lang.
- `bestzeiten(fahrzeit)` gibt die Tabelle der Teilprobleme als
  Dictionary zurück: Der Schlüssel (maske, letzter) steht für die
  kürzeste Fahrt, die an der Zentrale beginnt, genau die Standorte der
  Bitmaske maske besucht (Standort k ist das Bit 1 << (k - 1)) und
  beim Standort letzter endet; der Wert ist ihre Dauer. Die Tabelle
  enthält genau die Schlüssel mit maske ≠ 0 und letzter in maske.
- `kuerzeste_tour(fahrzeit)` gibt die kürzeste Gesamtzeit einer Tour
  durch alle Standorte zurück (mit Rückfahrt zur Zentrale).
- `beste_reihenfolge(fahrzeit)` gibt eine Liste der Standorte 1 bis n
  in einer Reihenfolge mit dieser kürzesten Gesamtzeit zurück. Gibt es
  mehrere, ist jede richtig.

    fahrzeit = [[0, 42, 12, 20, 35],      # von der Zentrale
                [40, 0, 40, 30, 12],      # vom Standort 1
                [12, 40, 0, 15, 25],
                [22, 30, 15, 0, 34],
                [35, 14, 25, 34, 0]]
    tourdauer(fahrzeit, [1, 2, 3, 4])            →  166
    bestzeiten(fahrzeit)[(0b0101, 3)]            →  72   (0 → 1 → 3)
    bestzeiten(fahrzeit)[(0b0101, 1)]            →  50   (0 → 3 → 1)
    kuerzeste_tour(fahrzeit)                     →  99
    beste_reihenfolge(fahrzeit)                  →  [3, 1, 4, 2]

Grenzen: fahrzeit ist eine Liste von n + 1 Listen mit je n + 1 ganzen
Zahlen, 0 ≤ n ≤ 15, jede Fahrzeit von 0 bis 1000, fahrzeit[i][i] = 0.
Die Matrix muss nicht symmetrisch sein, und ein Umweg über einen
dritten Ort kann kürzer sein als die direkte Fahrt. reihenfolge
enthält verschiedene Standorte aus 1 bis n (nicht unbedingt alle).
bestzeiten, kuerzeste_tour und beste_reihenfolge sollen O(2**n · n²)
Schritte brauchen.

Hintergrund: Die Aufgaben 3_067 und 3_068 haben Teilergebnisse in
einer Tabelle gesammelt, Aufgabe 4_026 beim Rucksack und Aufgabe 4_027
bei der Editierdistanz ebenso. Das Rezept ist immer dasselbe: ein
Teilproblem finden, dessen Lösung nur von wenigen Angaben abhängt, und
die Tabelle so füllen, dass jedes Teilproblem nur auf schon fertige
zurückgreift. Bei der Tour ist das Teilproblem: Wie schnell kommt man
von der Zentrale aus durch genau die Standorte einer Menge S und steht
am Ende bei k? Wichtig ist nur, welche Standorte schon erledigt sind
und wo man steht, nicht, in welcher Reihenfolge die erledigten
angefahren wurden. Darum gilt:

    beste(S, k) = min über j in S ohne k von  beste(S ohne k, j) + fahrzeit[j][k]
    beste({k}, k) = fahrzeit[0][k]

und die ganze Tour ist das Minimum von beste(alle, k) + fahrzeit[k][0].
Das ist der Algorithmus von Held und Karp (1962). Es gibt 2**n Mengen
und n letzte Standorte, für jeden Eintrag probiert man bis zu n
Vorgänger: O(2**n · n²) Schritte, für n = 15 etwa 7 · 10**6 statt 10**12.

Die Mengen speichert man als Bitmaske, eine ganze Zahl, deren Bits
sagen, wer dazugehört: Standort k ist das Bit 1 << (k - 1), die Menge
{1, 3} ist 0b0101 = 5. Mit den Bitoperatoren rechnet man darauf wie
mit Mengen, nur viel schneller, und ganze Zahlen taugen als Schlüssel
eines Dictionarys oder als Listenindex:

    bit = 1 << (k - 1)        # die Menge {k}
    maske | bit               # k hinzunehmen
    maske & bit               # ungleich 0, wenn k in der Menge ist
    maske ^ bit               # k herausnehmen (wenn k drin ist)
    alle = (1 << n) - 1       # alle n Standorte, z. B. 0b1111 für n = 4
    maske.bit_count()         # wie viele Standorte die Menge hat

    for maske in range(1, 1 << n):          # alle nicht leeren Mengen
        for k in range(1, n + 1):
            if maske & (1 << (k - 1)):
                ...                         # k ist in maske

Eine echte Teilmenge hat immer eine kleinere Zahl als die Menge selbst
(es fehlen Bits). Wer die Masken also aufsteigend durchgeht, findet
beste(S ohne k, j) immer schon in der Tabelle. Statt die Tabelle von
unten zu füllen, geht es auch rekursiv mit @lru_cache (Aufgabe 4_025)
auf einer Funktion beste(maske, k); die Rekursion ist höchstens n tief.
Die Reihenfolge selbst liest man wie in Aufgabe 4_026 rückwärts aus der
Tabelle ab: Man beginnt beim besten letzten Standort und sucht jeweils
den Vorgänger j, für den beste(S ohne k, j) + fahrzeit[j][k] genau
beste(S, k) ergibt.

Bitmasken lohnen sich nur für kleine Mengen: Schon bei n = 30 hat die
Tabelle 30 · 2**30 Einträge. Für große n kennt man kein Verfahren, das
die beste Tour sicher schnell findet; dort nimmt man Näherungen.
"""


def tourdauer(fahrzeit, reihenfolge):
    """Gibt die Dauer der Tour Zentrale → reihenfolge → Zentrale zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bestzeiten(fahrzeit):
    """Gibt das Dictionary (maske, letzter) → kürzeste Dauer von der Zentrale durch maske bis letzter zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kuerzeste_tour(fahrzeit):
    """Gibt die kürzeste Gesamtzeit einer Tour durch alle Standorte mit Rückfahrt zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def beste_reihenfolge(fahrzeit):
    """Gibt eine Reihenfolge der Standorte mit der kürzesten Gesamtzeit zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


fahrzeit = [
    [0, 42, 12, 20, 35],
    [40, 0, 40, 30, 12],
    [12, 40, 0, 15, 25],
    [22, 30, 15, 0, 34],
    [35, 14, 25, 34, 0],
]
print(tourdauer(fahrzeit, [1, 2, 3, 4]), bestzeiten(fahrzeit)[(0b0101, 3)], bestzeiten(fahrzeit)[(0b0101, 1)])
print(kuerzeste_tour(fahrzeit), beste_reihenfolge(fahrzeit))
