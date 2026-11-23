"""Aufgabe 2_055 – Modellrangliste                               Stufe 2 ★★☆☆☆

Ein Team für maschinelles Lernen sucht die beste Einstellung für ein
Modell, das Spam-Mails erkennen soll. Dafür trainiert es viele Varianten
des Modells mit verschiedenen Einstellungen und misst bei jeder die
Fehlerrate: wie viel Prozent der Testmails sie falsch einordnet. Die
Arbeit läuft auf zwei Rechnern. Jeder liefert eine Rangliste aus Paaren
(name, fehlerrate), aufsteigend nach Fehlerrate sortiert, die beste
Variante vorn:

    rechner_a = [("a3", 2.1), ("a1", 4.5), ("a2", 4.5), ("a4", 7.0)]
    rechner_b = [("b2", 1.8), ("b1", 4.5), ("b3", 9.9)]

Schreiben Sie die Funktion `zusammenfuehren(rechner_a, rechner_b)`, die
eine neue Liste mit allen Paaren beider Ranglisten zurückgibt, wieder
aufsteigend nach Fehlerrate. Bei gleicher Fehlerrate kommen die Paare
von Rechner A vor denen von Rechner B, und innerhalb einer Liste bleibt
ihre Reihenfolge erhalten:

    zusammenfuehren(rechner_a, rechner_b)
    →  [("b2", 1.8), ("a3", 2.1), ("a1", 4.5), ("a2", 4.5), ("b1", 4.5), ("a4", 7.0), ("b3", 9.9)]

Die beiden Listen bleiben unverändert. Benutzen Sie weder sort() noch
sorted(), und gehen Sie jede Liste nur einmal von vorn nach hinten
durch.

Grenzen: Jede Liste hat 0 bis 50 000 Paare und ist aufsteigend nach
Fehlerrate sortiert. Die Namen sind verschiedene, nicht leere Texte,
die Fehlerraten Kommazahlen von 0 bis 100, gleiche kommen vor. Ihre
Lösung soll höchstens etwa 20 · (Länge von rechner_a + Länge von
rechner_b) Schritte brauchen.

Hintergrund: Weil beide Listen sortiert sind, steht das kleinste Paar,
das noch fehlt, immer vorn in einer der beiden. Man braucht also nur
zwei Stellen i und j, eine für jede Liste, und vergleicht in einer
while-Schleife (Aufgabe 1_033) die beiden Paare an diesen Stellen: Das
kleinere kommt mit append in das Ergebnis, und nur seine Stelle rückt
um eins weiter. Ist eine Liste zu Ende, hängt man den Rest der anderen
an, er ist schon sortiert:

    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:      # hier ganze Zahlen; bei Paaren vergleichen Sie a[i][1]
            ergebnis.append(a[i])
            i += 1
        else:
            ergebnis.append(b[j])
            j += 1

Jedes Paar wird so genau einmal angefasst. Wer stattdessen jedes Paar
von b an der richtigen Stelle des Ergebnisses einsortiert, sucht diese
Stelle immer wieder von vorn; bei 50 000 Paaren sind das Milliarden
Vergleiche. Auf dieses Zusammenführen baut später Merge Sort auf
(Aufgabe 3_005). Paare auspacken kennen Sie aus Aufgabe 1_044.
"""


def zusammenfuehren(rechner_a, rechner_b):
    """Gibt eine neue, nach Fehlerrate sortierte Liste mit allen Paaren beider Ranglisten zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


rechner_a = [("a3", 2.1), ("a1", 4.5), ("a2", 4.5), ("a4", 7.0)]
rechner_b = [("b2", 1.8), ("b1", 4.5), ("b3", 9.9)]
print(zusammenfuehren(rechner_a, rechner_b))
