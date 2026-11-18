"""Aufgabe 1_038 – Zeitpuffer                                    Stufe 1 ★☆☆☆☆

In einem Softwareprojekt wird die Arbeit in Arbeitspakete zerlegt, und
für jedes Paket schätzt das Team, wie viele Tage es dauert. Erfahrungs-
gemäß dauert fast alles länger als geschätzt. Die Projektleitung plant
deshalb für jedes Arbeitspaket 25 Prozent Puffer ein: Aus einer
Schätzung von 10 Tagen werden 10 * 1.25 = 12.5 geplante Tage.

Das Programm fragt nach den Schätzungen für zwei Arbeitspakete, rechnet
für jedes die geplante Dauer aus und addiert beide. Schreiben Sie dafür
die Funktion mit_puffer mit einem Parameter tage, die die geplante
Dauer tage * 1.25 mit return zurückgibt (nicht ausgibt). Den Rest des
Programms gibt es schon. Bei den Eingaben 10 und 6:

    Arbeitspaket A: 12.5 Tage
    Arbeitspaket B: 7.5 Tage
    Zusammen: 20.0 Tage

Grenzen: Beide Schätzungen sind ganze Zahlen von 0 bis 1000.

Hintergrund: Eine Funktion kann ein Ergebnis an die Stelle
zurückliefern, an der sie aufgerufen wurde. Dafür steht im Rumpf
return und dahinter der Wert:

    def doppelt(zahl):
        return zahl * 2

    ergebnis = doppelt(21)          # ergebnis ist jetzt 42
    summe = doppelt(1) + doppelt(5) # 2 + 10, also 12

return beendet die Funktion sofort. print(...) in der Funktion würde
den Wert nur auf den Bildschirm schreiben; der Aufruf liefert dann
None („nichts“), und mit None kann man nicht weiterrechnen. Deshalb
gibt eine Funktion, deren Ergebnis weiterverwendet wird, es mit return
zurück. Die eigene Funktion mit def kennen Sie aus Aufgabe 1_037.
"""

paket_a = int(input("Schätzung Arbeitspaket A in Tagen: "))
paket_b = int(input("Schätzung Arbeitspaket B in Tagen: "))

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

plan_a = mit_puffer(paket_a)
plan_b = mit_puffer(paket_b)
print(f"Arbeitspaket A: {plan_a} Tage")
print(f"Arbeitspaket B: {plan_b} Tage")
print(f"Zusammen: {plan_a + plan_b} Tage")
