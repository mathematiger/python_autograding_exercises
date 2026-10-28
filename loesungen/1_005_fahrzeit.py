# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_005_fahrzeit.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_005_fahrzeit

"""Aufgabe 1_005 – Fahrzeit                                      Stufe 1 ★☆☆☆☆

Die Navigations-App zeigt die Fahrzeit nur in Minuten an, zum Beispiel 135
Minuten. Damit kann man sich wenig vorstellen. Das Programm fragt schon nach
den Minuten. Rechnen Sie sie in ganze Stunden und übrige Minuten um und geben
Sie das Ergebnis aus. Bei Eingabe 135 soll das Programm ausgeben:

    Das sind 2 Stunden und 15 Minuten.

Grenzen: Die Fahrzeit ist eine ganze Zahl zwischen 0 und 10 000 Minuten.

Hintergrund: Der Operator // teilt zwei ganze Zahlen und schneidet den Rest ab:
135 // 60 ergibt 2, denn 60 passt zweimal in 135. Der Operator % (gesprochen
„modulo“) liefert genau diesen Rest: 135 % 60 ergibt 15, denn 135 = 2 * 60 + 15.
Mit / käme dagegen die Kommazahl 2.25 heraus, und die hilft hier nicht.

Tipp: print("Das sind", stunden, "Stunden und", rest, "Minuten.") setzt
zwischen die Teile automatisch ein Leerzeichen.
"""

minuten = int(input("Fahrzeit in Minuten: "))

stunden = minuten // 60
rest = minuten % 60
print("Das sind", stunden, "Stunden und", rest, "Minuten.")


# Idee: minuten // 60 sagt, wie oft 60 ganz in die Minuten passt, das sind die vollen Stunden;
# minuten % 60 ist der Rest, der dabei übrig bleibt.
# Andere Wege: den Rest als minuten - stunden * 60 bestimmen, oder die Stunden mit int(minuten / 60),
# was bei Zahlen ab 0 dasselbe ergibt wie minuten // 60.
# Typische Fehler: / statt // (dann steht 2.25 da) oder die Reihenfolge vertauscht: 60 % minuten statt
# minuten % 60.
