# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_015_sensornachricht.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_015_sensornachricht

"""Aufgabe 1_015 – Sensornachricht                               Stufe 1 ★☆☆☆☆

In einem Bürogebäude hängt in jedem Raum ein kleiner Temperatursensor. Jeder
Sensor schickt regelmäßig eine kurze Nachricht an die Gebäudesteuerung,
zum Beispiel "K12:0231". Die ersten drei Zeichen sind der Name des
Sensors, dann kommt ein Doppelpunkt, dann vier Ziffern: die Temperatur in
Zehntelgrad. 0231 bedeutet also 23.1 °C. Die Gebäudesteuerung vergleicht
die Temperatur mit dem Sollwert, also der Temperatur, die im Raum
herrschen soll.

Das Programm fragt schon nach der Nachricht und dem Sollwert. Ergänzen Sie
die drei Zeilen, die den Namen des Sensors herausschneiden, die Temperatur
ausrechnen und das Ergebnis ausgeben. Bei den Eingaben "K12:0231" und "21"
soll das Programm ausgeben:

    Sensor K12 misst 23.1 °C, Abweichung vom Sollwert: 2.1 Grad.

Ist es kälter als der Sollwert, ist die Abweichung negativ, etwa -1.5 Grad.
Beide Zahlen stehen immer mit genau einer Nachkommastelle da.

Grenzen: Die Nachricht hat immer genau acht Zeichen: drei Zeichen Name, einen
Doppelpunkt und vier Ziffern von 0000 bis 1500 (0.0 °C bis 150.0 °C). Der
Sollwert ist eine Zahl zwischen 0 und 100 mit höchstens einer
Nachkommastelle, zum Beispiel 21 oder 19.5.

Hintergrund: Diese Übung verbindet, was Sie bisher kennen. Mit Slicing
(Aufgabe 1_012) schneiden Sie Teile aus einem Text: nachricht[:3] sind die
ersten drei Zeichen, nachricht[4:] alles ab dem fünften. int("0231")
(Aufgabe 1_004) macht aus dem Text die Zahl 231, die führende Null stört
dabei nicht. Und in einem f-String (Aufgabe 1_010) setzt {wert:.1f} eine
Zahl mit genau einer Nachkommastelle ein; im f-String darf auch eine
Rechnung stehen, zum Beispiel {a - b:.1f}.

Tipp: Teilen Sie die Zahl aus den vier Ziffern durch 10.
"""

nachricht = input("Nachricht: ")
sollwert = float(input("Sollwert: "))

sensor = nachricht[:3]
temperatur = int(nachricht[4:]) / 10
print(f"Sensor {sensor} misst {temperatur:.1f} °C, Abweichung vom Sollwert: {temperatur - sollwert:.1f} Grad.")


# Idee: nachricht[:3] schneidet den Namen heraus, nachricht[4:] die vier Ziffern. int(...) macht daraus
# eine ganze Zahl, geteilt durch 10 ergibt sie die Temperatur in Grad. Im f-String stehen beide Zahlen mit
# :.1f, die Abweichung wird gleich dort ausgerechnet.
# Anderer Weg: float(nachricht[4:8]) / 10 rechnet dasselbe; man kann die Abweichung auch vorher in einer
# eigenen Variablen speichern.
# Typische Fehler: nachricht[:4] (mit Doppelpunkt), das Teilen durch 10 vergessen (231 statt 23.1),
# Sollwert minus Temperatur statt umgekehrt (falsches Vorzeichen) oder die Zahlen ohne :.1f ausgeben
# (dann steht 2.1000000000000014 da).
