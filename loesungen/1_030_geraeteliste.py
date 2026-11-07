# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_030_geraeteliste.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_030_geraeteliste

"""Aufgabe 1_030 – Geräteliste                                   Stufe 1 ★☆☆☆☆

Eine Smart-Home-Zentrale führt eine Liste aller Geräte, die mit ihr
verbunden sind, etwa Thermostate und Rauchmelder. Bei der Wartung tauscht
der Techniker ein Gerät gegen ein neues Modell aus, und ein defektes
Gerät nimmt er ganz ab. Das Programm fragt nach der Geräteliste (durch
Kommas getrennt), nach der Nummer des getauschten Geräts (gezählt ab 1),
nach dem Namen des neuen Geräts und nach dem Namen des defekten Geräts.
Ergänzen Sie den Code so, dass zuerst das Gerät mit der eingegebenen
Nummer durch das neue ersetzt wird, an derselben Stelle. Danach soll
das defekte Gerät aus der Liste entfernt werden, aber nur, wenn es in
der Liste steht: Hat sich der Techniker vertippt, bleibt die Liste, wie
sie ist. Bei den Eingaben
Thermostat,Rauchmelder,Fensterkontakt,Bewegungsmelder und 2 und
Rauchmelder Pro und Fensterkontakt:

    Verbundene Geräte: 3
    - Thermostat
    - Rauchmelder Pro
    - Bewegungsmelder

Grenzen: Die Liste hat 1 bis 20 Geräte mit verschiedenen, nicht leeren
Namen ohne Komma. Die Nummer ist eine ganze Zahl von 1 bis zur Anzahl
der Geräte. Das neue Gerät hat einen Namen, der noch nicht in der Liste
steht. Das defekte Gerät ist nicht das Gerät mit der eingegebenen
Nummer und nicht das neue Gerät.

Hintergrund: Eine Liste kann man nach dem Anlegen verändern. Eine
Zuweisung an einen Index ersetzt ein Element: Nach farben = ["rot",
"gelb", "blau"] und farben[1] = "grün" ist farben gleich ["rot",
"grün", "blau"]. Die Methode remove entfernt ein Element über seinen
Wert: farben.remove("rot") ergibt ["grün", "blau"]. Steht der Wert
nicht in der Liste, bricht remove das Programm mit einem ValueError ab.
Deshalb fragt man vorher mit in nach, das wie bei Texten (Aufgabe
1_014) True oder False liefert: "rot" in farben ist hier False.
"""

eingabe = input("Verbundene Geräte, durch Kommas getrennt: ")
geraete = eingabe.split(",")
nummer = int(input("Nummer des getauschten Geräts: "))
neu = input("Name des neuen Geräts: ")
defekt = input("Name des defekten Geräts: ")

geraete[nummer - 1] = neu
if defekt in geraete:
    geraete.remove(defekt)

print(f"Verbundene Geräte: {len(geraete)}")
for geraet in geraete:
    print(f"- {geraet}")


# Idee: Die Nummer zählt ab 1, die Liste ab 0, also ersetzt geraete[nummer - 1] = neu das richtige Gerät
# an seiner Stelle. Danach prüft if defekt in geraete:, ob das defekte Gerät überhaupt in der Liste steht,
# und nur dann entfernt geraete.remove(defekt) es.
# Anderer Weg: Man könnte die Liste mit einer Schleife und append neu aufbauen und dabei das defekte Gerät
# auslassen. Das geht, ist aber viel länger als remove.
# Typische Fehler: geraete[nummer] = neu (dann wird das Gerät dahinter ersetzt, beim letzten bricht das
# Programm mit IndexError ab), remove ohne vorherige Prüfung mit in (ValueError bei einem Tippfehler) oder
# zuerst entfernen und dann ersetzen (dann rutschen die Geräte nach und die Nummer zeigt auf das falsche).
