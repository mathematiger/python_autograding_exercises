"""Aufgabe 1_036 – Reviewdauer                                   Stufe 1 ★☆☆☆☆

Bevor geänderter Code übernommen wird, liest ihn eine Kollegin in
einem Code-Review gegen. Das Team plant die Zeit dafür mit einer
Faustregel: 10 Minuten zum Einarbeiten und für je 20 geänderte Zeilen
3 Minuten. Früher stand diese Formel an drei Stellen im Programm, und
beim Ändern der Regel wurde eine Stelle vergessen. Darum steht sie
jetzt nur noch einmal in der vorgegebenen Funktion reviewminuten.

Das Programm fragt nach den geänderten Zeilen in zwei Dateien. Es soll
ausgeben, wie lange ein Review jeder einzelnen Datei dauert und wie
lange ein gemeinsames Review beider Dateien dauert (dafür zählen die
Zeilen beider Dateien zusammen, und eingearbeitet wird nur einmal).
Ergänzen Sie die drei Variablen dauer_a, dauer_b und dauer_gesamt,
indem Sie jedes Mal die Funktion reviewminuten aufrufen, statt die
Formel neu hinzuschreiben. Bei den Eingaben 120 und 40:

    Datei A: 28 Minuten
    Datei B: 16 Minuten
    Beides in einem Review: 34 Minuten

Grenzen: Beide Zeilenzahlen sind ganze Zahlen von 0 bis 5000.

Hintergrund: Eine Funktion ist ein Stück Code mit einem Namen. Mit def
wird sie einmal festgelegt; die Zeile mit return bestimmt, welcher Wert
herauskommt. Benutzt wird sie, indem man ihren Namen mit dem Wert in
Klammern hinschreibt, genau wie bei len(...) oder round(...):

    dauer = reviewminuten(60)    # dauer ist jetzt 10 + 60 * 3 // 20 = 19

Beim Aufruf bekommt der Parameter zeilen den Wert in den Klammern, und
der Aufruf liefert das Ergebnis von return. Man kann dieselbe Funktion
beliebig oft mit verschiedenen Werten aufrufen. Ändert sich die Regel,
ändert man nur die Funktion, und alle Stellen rechnen richtig.
"""


def reviewminuten(zeilen):
    """Schätzt, wie viele Minuten ein Review mit so vielen geänderten Zeilen dauert."""
    return 10 + zeilen * 3 // 20


datei_a = int(input("Geänderte Zeilen in Datei A: "))
datei_b = int(input("Geänderte Zeilen in Datei B: "))
gesamt = datei_a + datei_b

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"Datei A: {dauer_a} Minuten")
print(f"Datei B: {dauer_b} Minuten")
print(f"Beides in einem Review: {dauer_gesamt} Minuten")
