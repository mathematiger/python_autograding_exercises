"""Aufgabe 1_046 – Tabellenspalte                                Stufe 1 ★☆☆☆☆

In einer Datenbank hat jede Tabelle feste Spalten, und jede Spalte hat
einen Datentyp: INTEGER für ganze Zahlen, TEXT für Texte, DATE für ein
Datum. Ein kleines Verwaltungsprogramm hält den Aufbau der Tabelle
kunden in einem Dictionary: Spaltenname → Datentyp. Das Programm fragt
nach dem Namen einer neuen Spalte und nach ihrem Datentyp. Ergänzen Sie
den Code so, dass die neue Spalte ins Dictionary spalten eingetragen
wird und danach alle Spalten ausgegeben werden, jede in einer eigenen
Zeile: zuerst der Name, dann ein Leerzeichen, dann der Datentyp. Gibt es
die Spalte schon, ersetzt der neue Datentyp den alten. Bei Eingabe email
und TEXT:

    Tabelle kunden:
    id INTEGER
    name TEXT
    ort TEXT
    email TEXT

Grenzen: Spaltenname und Datentyp sind nicht leere Texte ohne
Leerzeichen.

Hintergrund: Wie man den Wert zu einem Schlüssel liest, wissen Sie aus
Aufgabe 1_045. Mit derselben Schreibweise links vom = trägt man einen
Wert ein: Gibt es den Schlüssel noch nicht, kommt ein neuer Eintrag
hinten dazu; gibt es ihn schon, wird sein Wert ersetzt. Ein Schlüssel
kommt also nie doppelt vor. Mit for und .items() geht man alle Einträge
in der Reihenfolge durch, in der sie eingetragen wurden, und bekommt
jedes Mal Schlüssel und Wert zugleich (ausgepackt wie ein Tupel in Aufgabe
1_044):

    preise = {"Maus": 15}
    preise["Tastatur"] = 30      # neuer Eintrag
    preise["Maus"] = 12          # ersetzt den Wert
    for artikel, preis in preise.items():
        print(artikel, preis)    # Maus 12, dann Tastatur 30
"""

spalten = {"id": "INTEGER", "name": "TEXT", "ort": "TEXT"}

spalte = input("Neue Spalte: ")
typ = input("Datentyp: ")

print("Tabelle kunden:")
pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
