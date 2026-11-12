# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_033_importpakete.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_033_importpakete

"""Aufgabe 1_033 – Importpakete                                  Stufe 1 ★☆☆☆☆

Eine Firma zieht ihre Kundendaten in eine neue Datenbank um. Der
Datenbankserver nimmt höchstens 500 Datensätze auf einmal an. Das
Importprogramm schickt die Datensätze deshalb in Paketen: volle Pakete mit
je 500 Datensätzen und zum Schluss ein kleineres Paket mit dem Rest.

Der vorgegebene Code fragt, wie viele Datensätze es sind, und legt die
Variablen rest (noch nicht verschickte Datensätze) und paket (Nummer des
letzten Pakets) an. Ergänzen Sie eine while-Schleife, die so lange läuft,
wie noch Datensätze übrig sind. In jedem Durchlauf

- zählt sie paket um 1 hoch,
- legt die Größe des Pakets fest: 500, aber höchstens so viel, wie noch
  übrig ist (min aus Aufgabe 1_031 hilft),
- gibt eine Zeile wie unten aus und
- zieht die Größe des Pakets von rest ab.

Bei Eingabe 1200:

    Paket 1: 500 Datensätze
    Paket 2: 500 Datensätze
    Paket 3: 200 Datensätze
    Pakete insgesamt: 3

Grenzen: Die Eingabe ist eine ganze Zahl von 0 bis 100000. Bei 0 gibt es
kein Paket, nur die letzte Zeile.

Hintergrund: Eine for-Schleife (Aufgabe 1_022) läuft eine vorher bekannte
Anzahl von Malen. Eine while-Schleife wiederholt ihren Block dagegen so
lange, wie die Bedingung hinter while wahr ist; vor jedem Durchlauf prüft
Python sie neu. Ist sie falsch, geht es unter der Schleife weiter:

    while rest > 0:
        ...
        rest = rest - groesse

Im Block muss sich etwas ändern, das in der Bedingung vorkommt, hier rest.
Fehlt die letzte Zeile, bleibt die Bedingung immer wahr und die Schleife
läuft endlos; die Prüfung bricht dann nach 5 Sekunden ab.
"""

anzahl = int(input("Anzahl der Datensätze: "))
rest = anzahl
paket = 0

while rest > 0:
    paket = paket + 1
    groesse = min(rest, 500)
    print(f"Paket {paket}: {groesse} Datensätze")
    rest = rest - groesse

print(f"Pakete insgesamt: {paket}")


# Idee: Solange rest größer als 0 ist, kommt ein weiteres Paket: paket um 1 erhöhen, die Größe mit
# min(rest, 500) bestimmen, die Zeile ausgeben und die Größe von rest abziehen. Beim letzten Paket ist
# rest höchstens 500, danach 0, und die Bedingung ist falsch.
# Anderer Weg: statt min ein if: Ist rest >= 500, ist das Paket 500 groß, sonst so groß wie rest. Ohne
# Schleife ginge es mit // und % (Aufgabe 1_005): anzahl // 500 volle Pakete und ein Rest anzahl % 500.
# Typische Fehler: rest = rest - groesse vergessen (Endlosschleife), while rest >= 0 (dann kommt am
# Ende ein Paket mit 0 Datensätzen), immer 500 abziehen (das letzte Paket wäre zu groß) oder die
# Zeile „Pakete insgesamt“ in die Schleife einrücken.
