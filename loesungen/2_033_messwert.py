# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_033_messwert.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_033_messwert

"""Aufgabe 2_033 – Messwerte umwandeln                           Stufe 2 ★★☆☆☆

Ein Versandhändler misst für jede Bestellung, wie viele Minuten sie im Lager
braucht, vom Eingang bis zum fertig gepackten Paket (die Durchlaufzeit). Die
Messwerte kommen als Texte aus einem Export der Lagersoftware, und nicht alle
sind brauchbar: Mal fehlt der Wert (leerer Text), mal steht "n/a" oder ein
Tippfehler wie "4S" darin. Ein einziger kaputter Wert darf das Programm nicht
abstürzen lassen.

Vervollständigen Sie die Funktion `als_minuten(text)`. Sie wandelt den Text
mit float(...) in eine Zahl um und gibt sie zurück. Lässt sich der Text nicht
umwandeln, gibt die Funktion -1 zurück, statt abzustürzen. Eine echte
Durchlaufzeit ist nie negativ, deshalb erkennt man an -1 sofort einen
unbrauchbaren Wert. Fangen Sie dafür nur den ValueError ab
(except ValueError:), damit andere Fehler weiterhin gemeldet werden.

    als_minuten("42")      →  42.0
    als_minuten("37.5")    →  37.5
    als_minuten(" 12 ")    →  12.0
    als_minuten("n/a")     →  -1
    als_minuten("")        →  -1
    als_minuten("1,5")     →  -1   (Python schreibt Kommazahlen mit Punkt)

Grenzen: text ist ein Text mit höchstens 20 Zeichen. Brauchbare Texte sind
Zahlen von 0 bis 10 000 wie "42" oder " 37.5 "; Leerzeichen am Anfang und am
Ende stören float nicht. Unbrauchbar ist jeder Text, den float(...) nicht
umwandeln kann. Texte wie "nan", "inf", "1e3" oder "1_000" kommen nicht vor.

Hintergrund: float("n/a") lässt sich nicht ausrechnen. Python löst dann einen
ValueError aus, eine Ausnahme, und ohne weitere Vorkehrung bricht das Programm
damit ab. Mit try und except kann man eine Ausnahme abfangen: Python führt den
Block unter try aus. Geht dort etwas schief, springt es sofort in den Block
unter except, statt abzubrechen, und macht danach ganz normal weiter.

    try:
        stueck = int("drei")
        print("Danke!")
    except ValueError:
        print("Das war keine ganze Zahl.")

Das gibt nur „Das war keine ganze Zahl.“ aus: int("drei") scheitert, also wird
print("Danke!") übersprungen. Hinter except steht die Art der Ausnahme, mit
der man rechnet. Andere Fehler, etwa ein Tippfehler im Variablennamen
(NameError), werden dann nicht verschluckt, sondern weiterhin gemeldet. Statt
vorher mühsam zu prüfen, ob ein Text eine Zahl ist (hat er einen Punkt?
Leerzeichen?), probiert man die Umwandlung einfach aus und behandelt den
Fehlschlag (MIT 6.0001, Lecture 7). Ein return beendet die Funktion auch
mitten im try- oder except-Block.

Tipp: Ein return im try-Block gibt die Zahl zurück, ein return im
except-Block den Wert -1.
"""


def als_minuten(text):
    """Wandelt text in eine Zahl um; gibt -1 zurück, wenn das nicht geht."""
    try:
        return float(text)
    except ValueError:
        return -1


print(als_minuten("42"))
print(als_minuten("n/a"))


# Idee: Die Funktion probiert float(text) in einem try-Block und gibt die Zahl
# sofort mit return zurück. Scheitert die Umwandlung, springt Python in den Block
# unter except ValueError, und die Funktion gibt -1 zurück.
#
# Anderer Weg: das Ergebnis in einer Variablen merken, etwa zahl = float(text)
# im try-Block und zahl = -1 im except-Block, und am Ende einmal return zahl.
#
# Typische Fehler: vorher mit isdigit() prüfen (dann fallen "37.5" und " 12 "
# durch), int statt float (keine Nachkommastellen), except ohne ValueError (das
# verschluckt auch Fehler im eigenen Code) oder "0" als unbrauchbar ansehen.
#
# Weiter geht es mit Aufgabe 2_034: Dort fangen Sie Fehler in einer Schleife ab.
