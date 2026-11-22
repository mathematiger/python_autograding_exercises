# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_047_rolllaeden.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_047_rolllaeden

"""Aufgabe 1_047 – Rollläden                                     Stufe 1 ★☆☆☆☆

In einem Bürogebäude steuert eine Zentrale alle elektrischen Rollläden.
Jeder Rollladen hat eine Kennung wie R2 und meldet sich bei der
Zentrale mit seinem Raum und seiner Öffnung in Prozent (0 heißt ganz
zu, 100 ganz offen). Die Zentrale speichert das in einem Dictionary:
Kennung → Tupel aus Raum und Öffnung. Das Programm fragt nach einer
neuen Meldung: Kennung, Raum und Öffnung. Ergänzen Sie den Code:

- Ist die Kennung schon bekannt, gibt das Programm aus, welchen Raum und
  welche Öffnung der Rollladen vorher hatte, in der Form
  R2 bekannt: vorher Küche 0 %. Sonst gibt es R4 neu aus.
- Danach steht die Meldung im Dictionary: Ein bekannter Rollladen
  bekommt die neuen Werte, ein neuer kommt hinzu.
- Zum Schluss gibt das Programm alle Rollläden aus, jeden in einer
  eigenen Zeile mit Kennung, Raum und Öffnung.

Bei Eingabe R2, Küche und 30:

    R2 bekannt: vorher Küche 0 %
    Alle Rollläden:
    R1 Wohnzimmer 100 %
    R2 Küche 30 %
    R3 Bad 50 %

Grenzen: Kennung und Raum sind nicht leere Texte ohne Leerzeichen, die
Öffnung ist eine ganze Zahl von 0 bis 100.

Hintergrund: Diese Übung verbindet Tupel (Aufgabe 1_044) mit
Dictionaries (Aufgaben 1_045 und 1_046). Der Wert zu einem Schlüssel
darf selbst ein Tupel sein; dann packt man ihn nach dem Nachschlagen
aus. Ob es einen Schlüssel gibt, prüft man vorher mit in:

    lager = {"Maus": ("Regal 3", 12)}
    if "Maus" in lager:
        ort, anzahl = lager["Maus"]       # ort ist "Regal 3", anzahl 12
    lager["Maus"] = ("Regal 3", 11)      # neues Tupel eintragen

Ein Tupel lässt sich nicht ändern. Soll sich ein Teil ändern, trägt man
ein ganz neues Tupel ein.
"""

rolllaeden = {"R1": ("Wohnzimmer", 100), "R2": ("Küche", 0), "R3": ("Bad", 50)}

kennung = input("Kennung: ")
raum = input("Raum: ")
oeffnung = int(input("Öffnung in Prozent: "))

if kennung in rolllaeden:
    alter_raum, alte_oeffnung = rolllaeden[kennung]
    print(f"{kennung} bekannt: vorher {alter_raum} {alte_oeffnung} %")
else:
    print(f"{kennung} neu")
rolllaeden[kennung] = (raum, oeffnung)

print("Alle Rollläden:")
for name, eintrag in rolllaeden.items():
    ort, prozent = eintrag
    print(f"{name} {ort} {prozent} %")


# Idee: Mit if kennung in rolllaeden: prüft man, ob der Rollladen bekannt ist. Nur dann schlägt man
# das alte Tupel nach und packt es in alter_raum und alte_oeffnung aus, bevor
# rolllaeden[kennung] = (raum, oeffnung) es durch ein neues Tupel ersetzt oder einen neuen Eintrag
# anlegt. In der Schleife über .items() packt man jedes Tupel wieder in Raum und Öffnung aus.
# Anderer Weg: rolllaeden[kennung][0] und rolllaeden[kennung][1] lesen die Teile über ihren Index;
# in der Schleife geht auch print(name, eintrag[0], eintrag[1], "%").
# Typische Fehler: den neuen Wert vor dem Nachschlagen eintragen (dann steht hinter „vorher“ schon
# der neue Wert), rolllaeden[kennung] ohne vorherige Prüfung mit in (KeyError bei einem neuen
# Rollladen), print(name, eintrag) (gibt das Tupel mit Klammern aus) oder versuchen, nur einen Teil
# des Tupels zu ändern (TypeError, Tupel sind unveränderlich).
