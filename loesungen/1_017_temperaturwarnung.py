# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_017_temperaturwarnung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_017_temperaturwarnung

"""Aufgabe 1_017 – Temperaturwarnung                             Stufe 1 ★☆☆☆☆

Im Serverraum misst ein Fühler regelmäßig die Temperatur der CPU eines
Servers. Ein kleines Überwachungsprogramm schreibt jeden Messwert auf.
Wird die CPU zu heiß, kann sie Schaden nehmen; deshalb soll das Programm
dann zusätzlich eine Warnung ausgeben, damit jemand nachsieht.

Das Programm fragt schon nach der Temperatur und gibt den Messwert und
am Schluss „Messung gespeichert.“ aus. Ergänzen Sie dazwischen die
Warnung: Nur wenn die Temperatur über 80 Grad liegt, soll zusätzlich
die Zeile „Warnung: Die CPU ist zu heiß!“ erscheinen. Bei Eingabe 85:

    Gemessen: 85 Grad
    Warnung: Die CPU ist zu heiß!
    Messung gespeichert.

Bei Eingabe 60 fehlt die mittlere Zeile:

    Gemessen: 60 Grad
    Messung gespeichert.

Grenzen: Die Temperatur ist eine ganze Zahl von 0 bis 120. Genau 80 Grad
sind noch in Ordnung.

Hintergrund: Mit if führt das Programm einen Codeblock nur dann aus, wenn
eine Bedingung wahr ist. Hinter if steht ein Vergleich wie in Aufgabe
1_016, dahinter ein Doppelpunkt. Die Zeilen, die nur unter der Bedingung
laufen sollen, stehen darunter und sind eingerückt (vier Leerzeichen):

    if anzahl > 10:
        print("Viele!")
    print("Fertig.")

Hier erscheint „Viele!“ nur bei mehr als 10, „Fertig.“ aber immer, weil
diese Zeile nicht mehr eingerückt ist.
"""

temperatur = int(input("Temperatur der CPU in Grad: "))
print("Gemessen:", temperatur, "Grad")

if temperatur > 80:
    print("Warnung: Die CPU ist zu heiß!")

print("Messung gespeichert.")


# Idee: Die Warnung steht eingerückt unter if temperatur > 80:. So wird sie nur ausgegeben, wenn
# der Vergleich True ergibt. Die Zeile „Messung gespeichert.“ darunter ist nicht eingerückt und
# läuft deshalb immer.
# Anderer Weg: if 80 < temperatur: mit vertauschten Seiten, oder if temperatur >= 81:, weil die
# Temperatur eine ganze Zahl ist. Beides ergibt dasselbe.
# Typische Fehler: >= statt > (dann warnt das Programm schon bei genau 80 Grad), den Doppelpunkt
# hinter der Bedingung vergessen (SyntaxError) oder die Warnung nicht einrücken (dann kommt sie
# immer).
