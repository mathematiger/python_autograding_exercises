# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_041_einmalcode.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_041_einmalcode

"""Aufgabe 1_041 – Einmalcode                                    Stufe 1 ★☆☆☆☆

Beim Anmelden mit zwei Faktoren bekommt man nach dem Passwort einen
Einmalcode: eine sechsstellige Zahl, die nur einmal gilt. Ein Angreifer,
der den Code raten will, hat bei 900 000 möglichen Codes kaum eine
Chance. Für die Tests des Anmeldesystems soll ein kleines Programm
solche Codes erzeugen. Damit die Tester einen Fehler nachstellen können,
geben sie eine Startzahl ein; zur selben Startzahl entsteht immer
derselbe Code.

Das Programm fragt schon nach der Startzahl und stellt damit den Zufall
ein. Ergänzen Sie zwei Zeilen: Ziehen Sie mit random.randint eine
zufällige ganze Zahl von 100000 bis 999999 und geben Sie sie aus. Bei
der Startzahl 42 soll das Programm ausgeben:

    Ihr Einmalcode: 770487

Grenzen: Die Startzahl ist eine ganze Zahl von 0 bis 1000000.

Hintergrund: Nach import random liefert random.randint(a, b) eine
zufällige ganze Zahl von a bis b, und zwar einschließlich a und b:
random.randint(1, 6) würfelt also 1, 2, 3, 4, 5 oder 6. Der Rechner
würfelt dabei nicht wirklich, sondern rechnet aus einer Startzahl eine
lange Folge von Zahlen aus, die zufällig aussehen. random.seed(7) legt
diese Startzahl fest: Danach kommt bei jedem Programmlauf dieselbe Folge
heraus. Für echte Anmeldecodes nimmt man darum ein anderes Modul
(secrets), für Tests ist die feste Folge gerade richtig.
"""

import random

startzahl = int(input("Startzahl: "))
random.seed(startzahl)

code = random.randint(100000, 999999)
print("Ihr Einmalcode:", code)


# Idee: random.seed(startzahl) ist schon vorgegeben, danach liefert random.randint(100000, 999999)
# immer dieselbe Zahl zur selben Startzahl. Die legt man in eine Variable und gibt sie mit print
# hinter dem Text aus.
# Anderer Weg: Beides in einer Zeile, print("Ihr Einmalcode:", random.randint(100000, 999999)),
# oder mit einem f-String: print(f"Ihr Einmalcode: {code}").
# Typische Fehler: random.randint(0, 999999) (dann gibt es auch kürzere Codes und andere Zahlen),
# random.randint(100000, 1000000) (die Obergrenze gehört dazu, so wäre 1000000 möglich und die
# Folge eine andere), zweimal randint aufrufen (dann wird der zweite Code ausgegeben) oder den Code
# fest hinschreiben.
