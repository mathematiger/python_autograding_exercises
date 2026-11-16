# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_036_testabdeckung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_036_testabdeckung

"""Aufgabe 1_036 – Testabdeckung                                 Stufe 1 ★☆☆☆☆

Ein Entwicklungsteam misst, wie gut sein Code durch automatische Tests
abgesichert ist. Die Testabdeckung gibt an, wie viel Prozent der
Codezeilen beim Testen mindestens einmal ausgeführt werden. Das Team
hat sich in einem Sprint vorgenommen, mehr Tests zu schreiben, und
möchte nun sehen, ob es geholfen hat. Ein Kollege hat die Formel schon
als Funktion abdeckung geschrieben. Das Programm fragt nach der Zahl
aller Codezeilen und nach den getesteten Zeilen vor und nach dem
Sprint und gibt am Ende das Ergebnis aus. Ergänzen Sie zwei Zeilen,
die die Funktion abdeckung aufrufen: prozent_vorher soll die Abdeckung
vor dem Sprint sein, prozent_nachher die nach dem Sprint. Rechnen Sie
die Formel nicht selbst noch einmal aus. Bei den Eingaben 800, 412
und 536:

    Abdeckung vorher: 51.5 %
    Abdeckung nachher: 67.0 %
    Verbesserung: 15.5 Prozentpunkte

Grenzen: Die Zahl aller Zeilen ist eine ganze Zahl von 1 bis 100 000,
die getesteten Zeilen sind ganze Zahlen von 0 bis zur Zahl aller
Zeilen, und nach dem Sprint sind es mindestens so viele wie vorher.

Hintergrund: Eine Funktion ist ein Stück Code mit einem Namen, das man
einmal aufschreibt und dann beliebig oft benutzt. Sie kennen das schon
von print, len oder round. Beim Aufruf schreibt man den Namen, dann in
Klammern die Werte für die Parameter in derselben Reihenfolge wie in
der Zeile mit def: abdeckung(412, 800) setzt getestet = 412 und
gesamt = 800. Was die Funktion mit return zurückgibt, kann man in
einer Variablen speichern: ergebnis = abdeckung(412, 800). Steht eine
Formel nur an einer Stelle, muss man sie bei einem Fehler auch nur an
einer Stelle verbessern; deshalb ruft man die Funktion auf, statt die
Formel abzuschreiben.
"""


def abdeckung(getestet, gesamt):
    """Gibt den Anteil getestet von gesamt in Prozent zurück, auf eine Nachkommastelle gerundet."""
    return round(getestet / gesamt * 100, 1)


gesamt = int(input("Codezeilen insgesamt: "))
vorher = int(input("Getestete Zeilen vor dem Sprint: "))
nachher = int(input("Getestete Zeilen nach dem Sprint: "))

prozent_vorher = abdeckung(vorher, gesamt)
prozent_nachher = abdeckung(nachher, gesamt)

print(f"Abdeckung vorher: {prozent_vorher} %")
print(f"Abdeckung nachher: {prozent_nachher} %")
print(f"Verbesserung: {round(prozent_nachher - prozent_vorher, 1)} Prozentpunkte")


# Idee: Die Formel steht schon in der Funktion abdeckung. Man ruft sie zweimal auf, einmal mit den
# getesteten Zeilen vor und einmal mit denen nach dem Sprint, jeweils mit der Zahl aller Zeilen als
# zweitem Argument, und speichert die Rückgabewerte in den beiden Variablen.
# Anderer Weg: Mit Schlüsselwort-Argumenten zählt die Reihenfolge nicht: abdeckung(gesamt=gesamt,
# getestet=vorher) liefert dasselbe. Die Formel round(vorher / gesamt * 100, 1) noch einmal hinzuschreiben
# rechnet zwar richtig, verdoppelt aber die Regel, die die Funktion an einer Stelle bündeln soll.
# Typische Fehler: die Argumente vertauschen, abdeckung(gesamt, vorher) (dann kommen Werte über 100 % heraus),
# die Funktion ohne Klammern hinschreiben (prozent_vorher = abdeckung ist die Funktion selbst, kein Ergebnis)
# oder beide Male vorher übergeben.
