"""Aufgabe 1_019 – ABC-Analyse                                   Stufe 1 ★☆☆☆☆

Im Lager eines IT-Händlers liegen Hunderte Artikel, vom teuren Server
bis zum Netzwerkkabel. Damit sich das Team auf das Wichtige konzentriert,
macht es eine ABC-Analyse: Jeder Artikel kommt nach seinem Anteil am
gesamten Lagerwert in eine von drei Klassen. Artikel der Klasse A sind
wenige, aber sehr wertvoll und werden genau überwacht, Artikel der
Klasse C sind viele billige Kleinteile.

Die Regel lautet:

    Anteil ab 20 Prozent      Klasse A
    Anteil ab 5 Prozent       Klasse B
    Anteil unter 5 Prozent    Klasse C

Das Programm fragt schon nach dem Anteil eines Artikels. Ergänzen Sie
die Entscheidung, sodass die passende Klasse ausgegeben wird. Bei
Eingabe 25:

    Anteil: 25 Prozent
    Klasse: A
    Analyse beendet.

Bei Eingabe 12 steht in der mittleren Zeile „Klasse: B“, bei Eingabe 3
„Klasse: C“.

Grenzen: Der Anteil ist eine ganze Zahl von 0 bis 100.

Hintergrund: Mit elif (kurz für „else if“) bekommt ein if beliebig viele
weitere Fälle. Python prüft die Bedingungen von oben nach unten und führt
nur den Block der ersten wahren Bedingung aus; alle weiteren werden
übersprungen, auch wenn sie ebenfalls wahr wären. Der Block unter else
läuft nur, wenn keine Bedingung wahr war:

    if punkte >= 90:
        print("sehr gut")
    elif punkte >= 50:
        print("bestanden")
    else:
        print("nicht bestanden")

Bei 95 Punkten sind beide Bedingungen wahr, ausgegeben wird aber nur
„sehr gut“. Darum kommt die strengste Bedingung nach oben.
"""

anteil = int(input("Anteil am Lagerwert in Prozent: "))
print("Anteil:", anteil, "Prozent")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print("Analyse beendet.")
