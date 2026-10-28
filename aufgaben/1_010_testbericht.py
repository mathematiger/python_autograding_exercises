"""Aufgabe 1_010 – Testbericht                                  Stufe 1 ★☆☆☆☆

In einem Softwareprojekt laufen nach jeder Änderung automatische Tests. Am
Ende soll eine Zeile zeigen, wie viele Tests bestanden haben und wie viel
Prozent das sind. Das Programm fragt schon nach der Zahl der bestandenen
Tests und nach der Zahl aller Tests und rechnet die Quote in Prozent aus.
Geben Sie den Bericht mit einem f-String aus, die Quote mit genau zwei
Nachkommastellen. Bei Eingabe 47 und 52 soll das Programm ausgeben:

    Testlauf: 47 von 52 Tests bestanden (90.38 %)

Grenzen: Die Zahl aller Tests ist eine ganze Zahl zwischen 1 und 10 000, die
Zahl der bestandenen eine ganze Zahl zwischen 0 und der Zahl aller Tests.

Hintergrund: Ein f-String ist ein Text mit einem f vor dem Anführungszeichen.
Was darin in geschweiften Klammern steht, rechnet Python aus und setzt den
Wert an diese Stelle, ganz ohne str(...) und +: f"{anzahl} Tests" ergibt bei
anzahl = 5 den Text "5 Tests". Hinter einem Doppelpunkt in der Klammer kann
man angeben, wie der Wert aussehen soll: f"{wert:.2f}" zeigt eine Kommazahl
mit genau zwei Nachkommastellen und rundet dabei. Bei wert = 2 / 3 ergibt das
"0.67", bei wert = 100.0 ergibt es "100.00".

Tipp: Ohne :.2f steht in der Zeile 90.38461538461539 statt 90.38.
"""

bestanden = int(input("Bestandene Tests: "))
gesamt = int(input("Alle Tests: "))
quote = bestanden / gesamt * 100

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
