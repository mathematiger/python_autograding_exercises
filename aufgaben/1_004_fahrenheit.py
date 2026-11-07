"""Aufgabe 1_004 – Fahrenheit                                    Stufe 1 ★☆☆☆☆

Die Klimaanlage im Serverraum stammt von einem US-Hersteller, ihre Steuerung
erwartet Sollwerte in Grad Fahrenheit. Im Datenblatt der Server steht die
zulässige Ansaugtemperatur aber in Grad Celsius. Das Programm fragt schon nach
der Temperatur in Celsius. Rechnen Sie sie um und geben Sie das Ergebnis aus.
Bei Eingabe 25 soll das Programm ausgeben:

    Das sind 77.0 Grad Fahrenheit.

Die Formel: Fahrenheit = Celsius * 9 / 5 + 32

Grenzen: Die Temperatur ist eine Zahl von -50 bis 50 mit höchstens einer
Nachkommastelle, zum Beispiel 25, -3.5 oder 36.5.

Hintergrund: input() liefert immer einen Text, auch wenn man eine Zahl eintippt.
Mit "25" kann Python nicht rechnen. Deshalb wandelt float("25") den Text in
die Kommazahl 25.0 um (int("25") würde die ganze Zahl 25 liefern). Erst dann
kann man mit *, / und + rechnen; / teilt und liefert immer eine Kommazahl.

Tipp: print("Das sind", fahrenheit, "Grad Fahrenheit.") setzt zwischen die
Teile automatisch ein Leerzeichen.
"""

eingabe = input("Temperatur in Celsius: ")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
