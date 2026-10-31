# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_019_abc_analyse.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_019_abc_analyse

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

if anteil >= 20:
    print("Klasse: A")
elif anteil >= 5:
    print("Klasse: B")
else:
    print("Klasse: C")

print("Analyse beendet.")


# Idee: Die strengste Bedingung kommt zuerst: if anteil >= 20 gibt „Klasse: A“ aus, elif anteil >= 5
# „Klasse: B“ und else „Klasse: C“. Bei 25 Prozent ist auch anteil >= 5 wahr, aber elif wird gar
# nicht mehr geprüft, weil schon die erste Bedingung gepasst hat.
# Anderer Weg: von unten anfangen, also if anteil < 5 für C, elif anteil < 20 für B, else für A. Oder
# die mittlere Bedingung ganz ausschreiben: elif anteil >= 5 and anteil < 20 (das kommt in 1_020).
# Typische Fehler: drei einzelne if statt elif (dann erscheinen bei 25 Prozent A und B), die
# Reihenfolge vertauschen (if anteil >= 5 zuerst, dann wird nie A ausgegeben) oder > statt >=
# (dann landet genau 20 Prozent in Klasse B).
