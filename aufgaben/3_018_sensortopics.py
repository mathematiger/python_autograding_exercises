"""Aufgabe 3_018 – Sensortopics                                  Stufe 3 ★★★☆☆

In einer Fabrikhalle melden Dutzende Sensoren ihre Messwerte über MQTT,
ein schlankes Protokoll für vernetzte Geräte. Jeder Sensor schickt
seine Nachrichten unter einem eigenen Topic, einer Adresse wie
"halle1/ofen/temperatur". Ein kleiner Rechner sammelt die Werte und
muss zwei Dinge umrechnen:

Erstens liefern die Sensoren keine Grad Celsius, sondern einen Rohwert
von 1 bis 1023 aus ihrem Wandler. Laut Datenblatt gilt
Temperatur = (Rohwert - 400) / 10. Ein Rohwert von 0 bedeutet, dass der
Sensor ausgefallen ist; solche Sensoren sollen im Ergebnis fehlen.

Zweitens kennt die Konfiguration zu jeder Sensorkennung das Topic. Kommt
aber eine Nachricht an, kennt der Rechner nur das Topic und braucht die
Kennung. Er braucht das Dictionary also andersherum.

Schreiben Sie zwei Funktionen, jede mit einer Dict Comprehension und
ohne for-Schleife:

- `in_celsius(rohwerte)`: rohwerte ordnet jeder Sensorkennung ihren
  Rohwert zu. Gibt ein neues Dictionary zurück, das jeder Kennung mit
  einem Rohwert ungleich 0 die Temperatur in Grad Celsius zuordnet.
- `umdrehen(topics)`: topics ordnet jeder Sensorkennung ihr Topic zu.
  Gibt ein neues Dictionary zurück, das jedem Topic die Kennung zuordnet.

    rohwerte = {"S1": 615, "S2": 0, "S3": 380}
    in_celsius(rohwerte)   →  {"S1": 21.5, "S3": -2.0}
    topics = {"S1": "halle1/ofen/temperatur", "S3": "halle2/tor/temperatur"}
    umdrehen(topics)       →  {"halle1/ofen/temperatur": "S1",
                               "halle2/tor/temperatur": "S3"}

Grenzen: Beide Dictionaries haben 0 bis 100 000 Einträge. Die Kennungen
und Topics sind nicht leere Texte; in topics gehört zu jeder Kennung ein
anderes Topic. Jeder Rohwert ist 0 oder eine ganze Zahl von 1 bis 1023.

Hintergrund: Wie eine List Comprehension (Aufgabe 3_017) eine Liste
baut, baut eine Dict Comprehension ein Dictionary. Sie steht in
geschweiften Klammern, und vorne steht ein Paar schluessel: wert:

    preise = {"Maus": 20, "Kabel": 5, "Monitor": 180}
    brutto = {name: preis * 1.19 for name, preis in preise.items()}
    teuer = {name: preis for name, preis in preise.items() if preis > 10}

preise.items() liefert die Paare (Schlüssel, Wert), die die for-Klausel
auspackt; mit if lassen sich Einträge auslassen. Vorne darf man
Schlüssel und Wert beliebig berechnen, also auch vertauschen. Kommt
dabei ein Schlüssel zweimal vor, gewinnt der letzte, und ein Eintrag
geht verloren. Darum funktioniert das Umdrehen nur, wenn die Werte
verschieden sind, wie es die Grenzen hier zusichern.
"""


def in_celsius(rohwerte):
    """Ordnet jeder Kennung mit Rohwert ungleich 0 die Temperatur in Grad Celsius zu."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def umdrehen(topics):
    """Ordnet jedem Topic die Kennung seines Sensors zu."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


rohwerte = {"S1": 615, "S2": 0, "S3": 380}
print(in_celsius(rohwerte))
print(umdrehen({"S1": "halle1/ofen/temperatur", "S3": "halle2/tor/temperatur"}))
