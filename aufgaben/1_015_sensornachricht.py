"""Aufgabe 1_015 – Sensornachricht                               Stufe 1 ★☆☆☆☆

In einem Bürogebäude hängt in jedem Raum ein kleiner Temperatursensor. Jeder
Sensor schickt regelmäßig eine kurze Nachricht an die Gebäudesteuerung,
zum Beispiel "K12:0231". Die ersten drei Zeichen sind der Name des
Sensors, dann kommt ein Doppelpunkt, dann vier Ziffern: die Temperatur in
Zehntelgrad. 0231 bedeutet also 23.1 °C. Die Gebäudesteuerung vergleicht
die Temperatur mit dem Sollwert, also der Temperatur, die im Raum
herrschen soll.

Ältere Sensoren schicken den Namen in Kleinbuchstaben, und bei der
Übertragung landen manchmal Leerzeichen vor oder hinter der Nachricht. Die
Gebäudesteuerung zeigt den Namen trotzdem immer in Großbuchstaben an.

Das Programm fragt schon nach der Nachricht und dem Sollwert. Ergänzen Sie
die Zeilen, die die Leerzeichen am Rand entfernen, den Namen des Sensors
herausschneiden, die Temperatur ausrechnen und das Ergebnis ausgeben. Bei
den Eingaben " k12:0231" und "21" soll das Programm ausgeben:

    Sensor K12 misst 23.1 °C, Abweichung vom Sollwert: 2.1 Grad.

Ist es kälter als der Sollwert, ist die Abweichung negativ, etwa -1.5 Grad.
Beide Zahlen stehen immer mit genau einer Nachkommastelle da.

Grenzen: Ohne die Leerzeichen am Rand hat die Nachricht immer genau acht
Zeichen: drei Buchstaben oder Ziffern als Name, einen Doppelpunkt und vier
Ziffern von 0000 bis 0500 (0.0 °C bis 50.0 °C). Vor und hinter der
Nachricht stehen höchstens drei Leerzeichen. Der Sollwert ist eine Zahl von
15 bis 30 mit höchstens einer Nachkommastelle, zum Beispiel 21 oder 19.5.

Hintergrund: Diese Übung verbindet, was Sie bisher kennen. strip() und
upper() (Aufgabe 1_013) entfernen die Leerzeichen am Rand und machen
Kleinbuchstaben groß. Mit Slicing (Aufgabe 1_012) schneiden Sie Teile aus
einem Text: nachricht[:3] sind die ersten drei Zeichen, nachricht[4:] alles
ab dem fünften. int("0231") (Aufgabe 1_004) macht aus dem Text die Zahl 231,
die führende Null stört dabei nicht. Und in einem f-String (Aufgabe 1_010)
setzt {wert:.1f} eine Zahl mit genau einer Nachkommastelle ein; im f-String
darf auch eine Rechnung stehen, zum Beispiel {a - b:.1f}.

Tipp: Entfernen Sie die Leerzeichen zuerst, sonst verrutschen die Stellen
beim Slicing. Teilen Sie die Zahl aus den vier Ziffern durch 10.
"""

nachricht = input("Nachricht: ")
sollwert = float(input("Sollwert: "))

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
