# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_010_testbericht.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_010_testbericht

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

print(f"Testlauf: {bestanden} von {gesamt} Tests bestanden ({quote:.2f} %)")


# Idee: Ein einziger f-String mit drei geschweiften Klammern: {bestanden}, {gesamt} und {quote:.2f}.
# Alles andere in der Zeile ist fester Text, auch die Klammern und das Prozentzeichen.
# Anderer Weg: "Testlauf: " + str(bestanden) + " von " + ... wie in Aufgabe 1_008, und die Quote mit
# format(quote, ".2f") in einen Text mit zwei Nachkommastellen verwandeln; das ist aber viel länger.
# Typische Fehler: das f vor dem Anführungszeichen vergessen (dann steht wörtlich {bestanden} da),
# {quote} ohne :.2f (90.38461538461539) oder round(quote, 2), das bei 100.0 nur 100.0 statt 100.00 zeigt.
