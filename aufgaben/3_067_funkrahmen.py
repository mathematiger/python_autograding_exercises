"""Aufgabe 3_067 – Funkrahmen                                    Stufe 3 ★★★☆☆

Ein Bodenfeuchte-Sensor auf einem Versuchsfeld schickt seine Messdaten per
Funk an ein Gateway, einen Empfänger, der sie ins Netz weiterleitet. Sein
Funkmodul kann nur Rahmen (Datenpakete) mit bestimmten Nutzlastgrößen
senden, zum Beispiel 2 oder 3 Byte, und jeder Rahmen wird ganz gefüllt. Ein
Messbericht von n Byte wird deshalb in eine Folge von Rahmen zerlegt, deren
Größen zusammen genau n ergeben. Die Reihenfolge zählt: 2 + 3 und 3 + 2 sind
zwei verschiedene Folgen. Das Testteam will die Software des Gateways mit
jeder möglichen Folge prüfen und muss vorher wissen, wie viele es sind.
Schreiben Sie zwei Funktionen:

- `rahmen_tabelle(n, groessen)` gibt eine Liste anzahl mit n + 1 Zahlen
  zurück: anzahl[k] ist die Zahl der Rahmenfolgen für genau k Byte, für
  jedes k von 0 bis n. Für 0 Byte gibt es genau eine Folge, die leere.
- `rahmenfolgen(n, groessen)` gibt die Zahl der Rahmenfolgen für genau
  n Byte zurück.

groessen ist die Liste der erlaubten Rahmengrößen. Lässt sich n gar nicht
zerlegen, ist die Anzahl 0.

    rahmen_tabelle(7, [2, 3])  →  [1, 0, 1, 1, 1, 2, 2, 3]
    rahmenfolgen(7, [2, 3])    →  3        (2+2+3, 2+3+2, 3+2+2)
    rahmenfolgen(4, [1, 2])    →  5
    rahmenfolgen(1, [2, 3])    →  0

Grenzen: 0 ≤ n ≤ 5000. groessen enthält 1 bis 20 verschiedene ganze Zahlen
mit 1 ≤ groesse ≤ 1000 in beliebiger Reihenfolge; Größen über n dürfen
vorkommen. Die Anzahlen dürfen sehr groß werden (Python-Ganzzahlen haben
keine Obergrenze). Ihre Lösung soll O(n · k) Schritte brauchen, wobei k die
Zahl der Größen ist, und auch bei n = 5000 funktionieren.

Hintergrund: In Aufgabe 3_033 haben Sie Varianten rekursiv gezählt und jedes
Teilergebnis in einem Dictionary gemerkt (Memoisierung). Dieselbe Idee geht
auch ohne Rekursion: Jede Rahmenfolge für k Byte beginnt mit einem Rahmen
der Größe g aus groessen, danach folgt irgendeine Folge für die restlichen
k - g Byte. Also ist

    anzahl[k] = Summe von anzahl[k - g] über alle g in groessen mit g ≤ k

Kennt man die Anzahlen für alle kleineren Zahlen, kennt man die für k. Man
füllt deshalb eine Tabelle von unten: zuerst anzahl[0] = 1, dann anzahl[1],
anzahl[2] und so weiter bis anzahl[n]. Jeder Eintrag wird genau einmal
berechnet und danach nur noch nachgeschlagen. Dieses Vorgehen heißt
dynamische Programmierung: ein Problem in kleinere Teilprobleme zerlegen,
deren Lösungen sich überschneiden, und jedes Teilproblem nur einmal lösen,
hier in der Reihenfolge vom kleinsten zum größten. Für die Fibonacci-Zahlen
sähe das so aus:

    fib = [0, 1]
    for k in range(2, n + 1):
        fib.append(fib[k - 1] + fib[k - 2])

Warum nicht einfach die Rekursion mit merker aus Aufgabe 3_033? Jeder
rekursive Aufruf, der noch nicht fertig ist, belegt Platz auf dem
Aufrufstapel, und Python bricht bei etwa 1000 gleichzeitig offenen Aufrufen
mit RecursionError ab (das Rekursionslimit). Bei n = 5000 und der Größe 1
wären es 5000. Die Tabelle braucht nur eine Schleife und kennt diese Grenze
nicht; außerdem sieht man ihr an, in welcher Reihenfolge gerechnet wird.

Tipp: Legen Sie die Liste mit [0] * (n + 1) an, setzen Sie anzahl[0] = 1 und
füllen Sie die übrigen Einträge mit zwei geschachtelten for-Schleifen: außen
über k, innen über die Größen. rahmenfolgen kann rahmen_tabelle benutzen.
"""


def rahmen_tabelle(n, groessen):
    """Gibt die Liste der Anzahlen von Rahmenfolgen für 0 bis n Byte zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def rahmenfolgen(n, groessen):
    """Gibt die Zahl der Rahmenfolgen zurück, deren Größen zusammen genau n Byte ergeben."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(rahmen_tabelle(7, [2, 3]))
print(rahmenfolgen(7, [2, 3]))
