"""Aufgabe 1_025 – Testlaufzeit                                 Stufe 1 ★☆☆☆☆

Bevor eine neue Version einer Software ausgeliefert wird, laufen
automatische Tests: kleine Programme, die nachprüfen, ob jede Funktion
noch richtig arbeitet. Jeder Test braucht eine gewisse Zeit, gemessen
in Millisekunden (ms, tausendstel Sekunden). Das Team will wissen, wie
lange alle Tests zusammen laufen, damit die Prüfung nicht unbemerkt
immer langsamer wird. Das Programm fragt schon nach der Anzahl der
Tests und in einer for-Schleife nach der Laufzeit jedes einzelnen.
Ergänzen Sie zwei Zeilen, damit es am Ende die Gesamtlaufzeit ausgibt:
eine vor der Schleife und eine in der Schleife. Bei den Eingaben 3,
120, 45 und 300:

    Gesamtlaufzeit: 465 ms

Gibt es keinen Test (Eingabe 0), ist die Gesamtlaufzeit 0 ms.

Grenzen: Die Anzahl der Tests ist eine ganze Zahl von 0 bis 100, jede
Laufzeit eine ganze Zahl von 0 bis 100000.

Hintergrund: Um viele Zahlen zu addieren, braucht man eine Variable,
die das bisherige Ergebnis aufbewahrt, oft summe genannt. Vor der
Schleife setzt man sie auf 0, denn am Anfang ist noch nichts addiert.
In der Schleife rechnet man bei jedem Durchlauf summe = summe + zahl:
Python rechnet zuerst rechts den alten Wert plus die neue Zahl aus und
speichert das Ergebnis dann wieder unter dem Namen summe. Nach der
Schleife steht in summe die Summe aller Zahlen. Stünde summe = 0 in der
Schleife, finge die Summe bei jedem Durchlauf wieder bei 0 an.
"""

anzahl = int(input("Anzahl der Tests: "))
pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
for nummer in range(1, anzahl + 1):
    dauer = int(input(f"Laufzeit von Test {nummer} in ms: "))
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
print(f"Gesamtlaufzeit: {summe} ms")
