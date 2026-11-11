# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_018_sensorkarte.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_018_sensorkarte

"""Aufgabe 3_018 – Sensorkarte                                   Stufe 3 ★★★☆☆

In einem Gewächshaus melden Funksensoren ihre Temperatur über MQTT, ein
Nachrichtenprotokoll für kleine Geräte: Jeder Sensor schickt seine Werte
an ein Topic, eine Adresse wie "haus1/beet3/temp", und ein zentraler
Server, der Broker, sammelt sie ein. Die Sensoren senden ganze Zahlen in
Zehntelgrad, also 215 für 21,5 °C; der Wert -32768 bedeutet, dass der
Sensor einen Fehler meldet. Schreiben Sie zwei Funktionen:

- `in_celsius(rohwerte)` bekommt ein Dictionary, das jeder Sensorkennung
  ihren Rohwert zuordnet, und gibt ein neues Dictionary zurück, das jeder
  Sensorkennung die Temperatur in Grad Celsius als Kommazahl zuordnet
  (Rohwert / 10). Sensoren mit dem Fehlerwert -32768 fehlen im Ergebnis.
- `topic_von(sensoren)` bekommt die Konfiguration des Brokers, ein
  Dictionary, das jedem Topic die Kennung des Sensors zuordnet, der dort
  sendet. Die Funktion gibt das umgedrehte Dictionary zurück:
  Sensorkennung → Topic.
  So findet die Wartung zu einem defekten Sensor schnell sein Topic.

    in_celsius({"s1": 215, "s2": -32768, "s3": -45})
        →  {"s1": 21.5, "s3": -4.5}
    topic_von({"haus1/beet3/temp": "s1", "haus2/tisch1/temp": "s3"})
        →  {"s1": "haus1/beet3/temp", "s3": "haus2/tisch1/temp"}

Schreiben Sie beide Funktionen mit einer Dict Comprehension, ohne
for-Schleife als eigene Anweisung.

Grenzen: Beide Dictionaries haben 0 bis 100 000 Einträge. Alle
Kennungen und Topics sind nicht leere Texte. Die Rohwerte sind ganze
Zahlen von -400 bis 1250 oder genau -32768. In sensoren sendet jeder
Sensor an genau ein Topic, keine Kennung kommt also zweimal als Wert
vor. Die übergebenen Dictionaries bleiben unverändert.

Hintergrund: Was die List Comprehension (Aufgabe 3_017) für Listen
ist, ist die Dict Comprehension für Dictionaries. Sie steht in
geschweiften Klammern, und vorn stehen Schlüssel und Wert, getrennt durch
einen Doppelpunkt:

    preise_brutto = {artikel: netto * 1.19 for artikel, netto in preise.items()}
    teuer = {artikel: netto for artikel, netto in preise.items() if netto > 100}

preise.items() liefert die Paare (schlüssel, wert), die man gleich
auspackt. Vorn darf man Schlüssel und Wert beliebig neu berechnen, auch
vertauschen:

    nummer_von = {name: nummer for nummer, name in namen.items()}

Das dreht ein Dictionary um. Das geht aber nur gut, wenn jeder Wert nur
einmal vorkommt: Taucht ein Wert zweimal auf, überschreibt der zweite
Eintrag den ersten, weil ein Schlüssel in einem Dictionary nur einmal
vorkommen kann. Wie bei Listen entsteht immer ein neues Dictionary, das
alte bleibt unverändert.
"""

FEHLERWERT = -32768


def in_celsius(rohwerte):
    """Gibt zu jedem Sensor ohne Fehlerwert die Temperatur in Grad Celsius zurück."""
    return {sensor: roh / 10 for sensor, roh in rohwerte.items() if roh != FEHLERWERT}


def topic_von(sensoren):
    """Dreht die Zuordnung Topic → Sensor um zu Sensor → Topic."""
    return {sensor: topic for topic, sensor in sensoren.items()}


print(in_celsius({"s1": 215, "s2": -32768, "s3": -45}))
print(topic_von({"haus1/beet3/temp": "s1", "haus2/tisch1/temp": "s3"}))


# Idee: Beide Funktionen sind eine einzige Dict Comprehension über .items(). in_celsius behält den
# Schlüssel, rechnet vorn den Wert um (roh / 10) und filtert hinten mit if roh != FEHLERWERT.
# topic_von packt die Paare als topic, sensor aus und schreibt sie vorn vertauscht hin: sensor: topic.
#
# Anderer Weg: ein leeres Dictionary anlegen und in einer for-Schleife ergebnis[sensor] = roh / 10
# eintragen, mit continue für den Fehlerwert. Für das Umdrehen ginge auch dict(zip(sensoren.values(),
# sensoren.keys())), weil keys() und values() dieselbe Reihenfolge haben; das ist aber schwerer zu lesen.
# Beide Wege rechnen richtig, bestehen hier aber nicht, weil die Aufgabe eine Dict Comprehension verlangt.
#
# Typische Fehler: den Fehlerwert umrechnen statt weglassen (-3276.8 im Ergebnis), roh // 10 statt
# roh / 10 (dann geht die Nachkommastelle verloren, und -45 wird zu -5), beim Umdrehen vorn topic: sensor
# stehen lassen oder über sensoren statt sensoren.items() laufen (dann bekommt man nur die Schlüssel).
#
# Laufzeit: Jeder der n Einträge wird einmal angesehen und einmal eingetragen; Eintragen in ein
# Dictionary kostet im Mittel O(1), zusammen also O(n).
