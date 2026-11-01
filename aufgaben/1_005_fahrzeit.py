"""Aufgabe 1_005 – Fahrzeit                                      Stufe 1 ★☆☆☆☆

Ein IT-Dienstleister schickt Techniker zu Kunden vor Ort. Das Ticketsystem
zählt die Fahrzeiten eines Technikers im Monat in Minuten zusammen, zum
Beispiel 135 Minuten. Für die Abrechnung soll die Summe in Stunden und Minuten
dastehen. Das Programm fragt schon nach den Minuten. Rechnen Sie sie in ganze
Stunden und übrige Minuten um und geben Sie das Ergebnis aus. Bei Eingabe 135
soll das Programm ausgeben:

    Das sind 2 Stunden und 15 Minuten.

Die Wörter „Stunden“ und „Minuten“ bleiben immer gleich, auch bei 1.

Grenzen: Die Fahrzeit eines Monats ist eine ganze Zahl von 0 bis 10 000 Minuten.

Hintergrund: Der Operator // teilt zwei ganze Zahlen und schneidet den Rest ab:
135 // 60 ergibt 2, denn 60 passt zweimal in 135. Der Operator % (gesprochen
„modulo“) liefert genau diesen Rest: 135 % 60 ergibt 15, denn 135 = 2 * 60 + 15.
Mit / käme dagegen die Kommazahl 2.25 heraus, und die hilft hier nicht.

Tipp: print("Das sind", stunden, "Stunden und", rest, "Minuten.") setzt
zwischen die Teile automatisch ein Leerzeichen.
"""

minuten = int(input("Fahrzeit in Minuten: "))

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
