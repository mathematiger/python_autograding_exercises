# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_044_lebenszykluskosten.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_044_lebenszykluskosten

"""Aufgabe 1_044 – Lebenszykluskosten                            Stufe 1 ★☆☆☆☆

Ihre Abteilung will neue Arbeitsplatzrechner kaufen. Beim Vergleich der
Angebote zählt nicht nur der Kaufpreis, sondern auch der Strom, den ein
Rechner in jedem Jahr seiner Nutzung verbraucht. Die Gesamtkosten sind
Kaufpreis plus Stromkosten pro Jahr mal Nutzungsdauer in Jahren; teilt
man sie durch die Nutzungsdauer, erhält man die Kosten pro Jahr.

Die Funktion kosten rechnet die Gesamtkosten schon aus. Ergänzen Sie
zwei Zeilen:

- In der Funktion: Geben Sie die Gesamtkosten und die Kosten pro Jahr
  zusammen als ein Tupel zurück, in dieser Reihenfolge.
- Im Programm: Packen Sie das Tupel, das kosten liefert, in die beiden
  Variablen gesamt und pro_jahr aus. Die Ausgabe darunter ist
  vorgegeben.

Bei Kaufpreis 900, Stromkosten 45 pro Jahr und 5 Jahren:

    Gesamtkosten: 1125.00 Euro
    Pro Jahr: 225.00 Euro

Grenzen: Kaufpreis und Stromkosten sind Zahlen von 0 bis 10000 mit
höchstens zwei Nachkommastellen, die Nutzungsdauer ist eine ganze Zahl
von 1 bis 10.

Hintergrund: Ein Tupel fasst mehrere Werte zu einem zusammen. Man
schreibt sie durch Kommas getrennt in runde Klammern: (1125.0, 225.0).
Anders als eine Liste lässt sich ein Tupel nach dem Anlegen nicht mehr
ändern. So kann eine Funktion mit einem einzigen return zwei Werte
zurückgeben. Beim Auspacken schreibt man links vom = so viele Variablen,
wie das Tupel Werte hat:

    punkt = (3, 4)
    x, y = punkt          # x ist 3, y ist 4

Das klappt auch direkt mit dem Ergebnis einer Funktion:
a, b = funktion(...).
"""


def kosten(kaufpreis, strom_pro_jahr, jahre):
    """Gibt die Gesamtkosten und die Kosten pro Jahr als Tupel zurück."""
    gesamt = kaufpreis + strom_pro_jahr * jahre
    return (gesamt, gesamt / jahre)


kaufpreis = float(input("Kaufpreis in Euro: "))
strom = float(input("Stromkosten pro Jahr in Euro: "))
jahre = int(input("Nutzungsdauer in Jahren: "))

gesamt, pro_jahr = kosten(kaufpreis, strom, jahre)

print(f"Gesamtkosten: {gesamt:.2f} Euro")
print(f"Pro Jahr: {pro_jahr:.2f} Euro")


# Idee: return (gesamt, gesamt / jahre) packt beide Ergebnisse in ein Tupel. Im Programm verteilt
# gesamt, pro_jahr = kosten(kaufpreis, strom, jahre) die beiden Werte des Tupels auf zwei
# Variablen, in derselben Reihenfolge, in der die Funktion sie hineingelegt hat.
# Anderer Weg: Die Klammern dürfen fehlen, return gesamt, gesamt / jahre ist ebenfalls ein Tupel.
# Man kann das Tupel auch erst in einer Variablen speichern und mit ergebnis[0] und ergebnis[1]
# auf die Werte zugreifen; das Auspacken ist aber kürzer und sagt gleich, was welcher Wert ist.
# Typische Fehler: nur einen Wert zurückgeben, die Reihenfolge vertauschen, links vom = nur eine
# Variable schreiben (dann steht das ganze Tupel darin und :.2f schlägt fehl) oder
# kaufpreis / jahre statt gesamt / jahre rechnen.
