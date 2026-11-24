# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_048_fehlerregister.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_048_fehlerregister

"""Aufgabe 2_048 – Fehlerregister                                Stufe 2 ★★☆☆☆

Ein Überwachungsmodul in einem Serverschrank meldet seinen Zustand als
eine einzige ganze Zahl, das Fehlerregister. In der Binärdarstellung
dieser Zahl steht jede Stelle für einen möglichen Fehler (Lüfter,
Netzteil, Temperatur, …): Eine 1 heißt, der Fehler ist gerade aktiv.
Das Register 13 ist binär 1101, also sind drei Fehler aktiv. Außerdem
liefert das Modul eine Messreihe von Temperaturen, und die Bereitschaft
will wissen, an welcher Stelle die Temperatur zum ersten Mal über der
Alarmgrenze lag.

Schreiben Sie beide Funktionen rekursiv, ohne for, ohne while und ohne
fertige Hilfen wie bin(), count() oder index(). Die Abbruchbedingung und
das kleinere Teilproblem finden Sie selbst:

- `aktive_fehler(register)` gibt zurück, wie viele Einsen die
  Binärdarstellung von register hat.
- `erste_ueberschreitung(werte, grenze)` gibt die Position (den Index)
  des ersten Werts zurück, der größer als grenze ist, und -1, wenn kein
  Wert darüber liegt.

    aktive_fehler(13)                              →  3
    aktive_fehler(0)                               →  0
    erste_ueberschreitung([61, 64, 72, 70], 65)    →  2
    erste_ueberschreitung([61, 64], 65)            →  -1
    erste_ueberschreitung([], 65)                  →  -1

Grenzen: 0 ≤ register < 2**60. werte hat 0 bis 400 Einträge, alle Werte
und grenze sind ganze Zahlen von -1000 bis 1000. Ein Wert genau auf der
Grenze liegt nicht darüber.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. Eine rekursive
Funktion braucht einen Fall, dessen Antwort feststeht, und ruft sich
sonst mit einem kleineren Problem auf (Aufgaben 2_044 bis 2_047). Was
„kleiner“ heißt, hängt vom Problem ab: Bei Zahlen ist es oft n - 1 oder
n // 2, bei Listen und Texten ein Stück ohne das erste Element (Slicing,
Aufgaben 1_012 und 2_018). Die letzte Binärstelle einer Zahl ist
zahl % 2, und zahl // 2 ist die Zahl ohne diese Stelle (Aufgaben 2_039
und 2_040):

    13 % 2   →  1      13 // 2  →  6   (binär 110)

Manchmal muss man das Ergebnis des kleineren Problems noch anpassen,
bevor man es zurückgibt. Ein Beispiel: Die Summe einer Liste ist das
erste Element plus die Summe des Rests.

    def summe(werte):
        if werte == []:
            return 0
        return werte[0] + summe(werte[1:])

Überlegen Sie bei erste_ueberschreitung genau, was die Position im Rest
werte[1:] für die Position in der ganzen Liste bedeutet, und was mit -1
geschehen soll.
"""


def aktive_fehler(register):
    """Gibt zurück, wie viele Einsen die Binärdarstellung von register hat."""
    if register == 0:
        return 0
    return register % 2 + aktive_fehler(register // 2)


def erste_ueberschreitung(werte, grenze):
    """Gibt den Index des ersten Werts über grenze zurück, sonst -1."""
    if werte == []:
        return -1
    if werte[0] > grenze:
        return 0
    im_rest = erste_ueberschreitung(werte[1:], grenze)
    if im_rest == -1:
        return -1
    return im_rest + 1


print("Aktive Fehler:", aktive_fehler(13))
print("Erste Überschreitung bei Index", erste_ueberschreitung([61, 64, 72, 70], 65))


# Idee: aktive_fehler: Bei 0 gibt es keine Einsen. Sonst ist die letzte Stelle register % 2 (0 oder
# 1), und die übrigen Einsen zählt der Aufruf für register // 2; beides wird addiert.
# erste_ueberschreitung: Eine leere Liste hat keinen Wert über der Grenze (-1). Liegt werte[0]
# darüber, ist die Antwort 0. Sonst sucht man im Rest werte[1:]; eine Fundstelle dort liegt in der
# ganzen Liste eine Position weiter hinten (+ 1), nur -1 bleibt -1.
# Anderer Weg: eine eigene rekursive Hilfsfunktion suche_ab(werte, grenze, position), die bei jedem
# Aufruf position um eins erhöht und sie bei einem Fund direkt zurückgibt; erste_ueberschreitung ruft
# sie mit position 0 auf. Dann entfällt das Anpassen und das Slicing. Der Test „ruft sich selbst auf“
# verlangt aber, dass sich auch erste_ueberschreitung selbst aufruft.
# Typische Fehler: bei -1 aus dem Rest trotzdem + 1 rechnen (dann kommt statt -1 die Länge der Liste
# minus 1 heraus), >= statt > (ein Wert auf der Grenze zählt dann mit), register // 10 statt // 2
# (Dezimal- statt Binärstellen) oder die Abbruchbedingung erst nach dem Zugriff auf werte[0] prüfen.
# Laufzeit: aktive_fehler braucht einen Aufruf mehr, als register Binärstellen hat (höchstens 61);
# erste_ueberschreitung bis zu n + 1 Aufrufe, wegen des Slicings insgesamt etwa n² / 2 kopierte Werte.
