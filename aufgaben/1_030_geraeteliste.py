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
Wert: Nach farben.remove("rot") ist farben gleich ["grün", "blau"];
remove verändert die Liste selbst und gibt nichts zurück. Steht der Wert
nicht in der Liste, bricht remove das Programm mit einem ValueError ab.
Deshalb fragt man vorher mit in nach, das wie bei Texten (Aufgabe
1_014) True oder False liefert: "rot" in farben ist hier False.
"""

eingabe = input("Verbundene Geräte, durch Kommas getrennt: ")
geraete = eingabe.split(",")
nummer = int(input("Nummer des getauschten Geräts: "))
neu = input("Name des neuen Geräts: ")
defekt = input("Name des defekten Geräts: ")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"Verbundene Geräte: {len(geraete)}")
for geraet in geraete:
    print(f"- {geraet}")
