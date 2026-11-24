# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_059_displaysymbole.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_059_displaysymbole

"""Aufgabe 2_059 – Displaysymbole                               Stufe 2 ★★☆☆☆

Die Ladesäulen für Elektroautos auf einem Firmenparkplatz haben eine
kleine Anzeige aus LEDs, auf der jedes Feld ein Zeichen zeigt, so wie ein
Textbildschirm. Die Steuerung der Säule zeichnet darauf Symbole aus
Sternchen: bei einer Störung ein Warndreieck, im Bereitschaftsbetrieb
eine Raute. Je nach Modell ist die Anzeige verschieden groß, deshalb soll
die Größe des Symbols einstellbar sein.

Schreiben Sie zwei Funktionen, die das Symbol als Liste seiner Zeilen
zurückgeben, von oben nach unten. Jede Zeile besteht aus Leerzeichen
links, die das Symbol in die Mitte rücken, und danach Sternchen; am
Zeilenende stehen keine Leerzeichen.

- `dreieck(hoehe)`: ein Dreieck mit hoehe Zeilen. Die oberste Zeile hat
  ein Sternchen, jede weitere zwei mehr; die Spitze steht genau über der
  Mitte der untersten Zeile. Bei hoehe 0 ist das Symbol ausgeschaltet,
  das Ergebnis ist die leere Liste.
- `raute(breite)`: eine Raute, deren breiteste Zeile breite Sternchen hat.
  Sie wächst wie das Dreieck um zwei Sternchen je Zeile bis zur
  breitesten Zeile in der Mitte und nimmt danach ebenso wieder ab; die
  breiteste Zeile kommt nur einmal vor. Die Raute hat also breite Zeilen.

    dreieck(3)  →  ["  *",
                    " ***",
                    "*****"]

    raute(5)    →  ["  *",
                    " ***",
                    "*****",
                    " ***",
                    "  *"]

Schreiben Sie sich vorher für jede Zeile auf, wie viele Leerzeichen und
wie viele Sternchen sie hat, und suchen Sie den Zusammenhang mit der
Nummer der Zeile.

Grenzen: hoehe ist eine ganze Zahl mit 0 ≤ hoehe ≤ 40. breite ist eine
ungerade ganze Zahl mit 1 ≤ breite ≤ 79. Die Anzeige hat 80 Zeichen je
Zeile, alle Symbole passen also hinein.

Hintergrund: Eine Figur aus Zeichen baut man Zeile für Zeile auf. Eine
for-Schleife über range(hoehe) (Aufgabe 2_001) liefert die Nummer der
Zeile, 0 für die oberste. Wie viele Leerzeichen und Sternchen in einer
Zeile stehen, hängt nur von dieser Nummer ab; beim Dreieck mit 3 Zeilen:

    nummer   Leerzeichen   Sternchen
      0           2            1
      1           1            3
      2           0            5

Jede Spalte ändert sich bei jeder Zeile um denselben Betrag, also lässt
sie sich als kurze Rechnung mit nummer (und hoehe) schreiben. Die Zeile
selbst setzt man mit * zusammen: Ein Text mal eine ganze Zahl wiederholt
den Text so oft, " " * 3 ergibt "   " und "*" * 0 den leeren Text "".
Man könnte die Zeichen auch mit einer inneren Schleife einzeln anhängen,
wie in den Aufgaben 1_042 und 2_014; mit * ist es eine Zeile. Jede fertige
Zeile hängen Sie mit append an eine Liste an, die vor der Schleife leer
beginnt. Bei der Raute darf die Funktion dreieck helfen: Ihre obere
Hälfte mit der Mittelzeile ist ein Dreieck.
"""


def dreieck(hoehe):
    """Gibt die Zeilen eines Dreiecks mit hoehe Zeilen zurück, oben ein Sternchen."""
    zeilen = []
    for nummer in range(hoehe):
        leerzeichen = hoehe - 1 - nummer
        sternchen = 2 * nummer + 1
        zeilen.append(" " * leerzeichen + "*" * sternchen)
    return zeilen


def raute(breite):
    """Gibt die Zeilen einer Raute zurück, deren breiteste Zeile breite Sternchen hat."""
    haelfte = breite // 2
    zeilen = dreieck(haelfte + 1)
    # Die untere Hälfte wiederholt die oberen Zeilen ohne die Mittelzeile, von unten nach oben
    for nummer in range(haelfte - 1, -1, -1):
        zeilen.append(zeilen[nummer])
    return zeilen


print(dreieck(3))
print(raute(5))


# Idee: In Zeile nummer (ab 0) eines Dreiecks mit hoehe Zeilen stehen 2 * nummer + 1 Sternchen und
# davor hoehe - 1 - nummer Leerzeichen; die unterste Zeile hat dann 2 * hoehe - 1 Sternchen und
# beginnt ganz links. Mit " " * leerzeichen + "*" * sternchen entsteht jede Zeile in einem Schritt,
# append hängt sie an die Liste. Die Raute besteht aus dem Dreieck mit breite // 2 + 1 Zeilen und
# darunter denselben Zeilen ohne die Mittelzeile in umgekehrter Reihenfolge; range(haelfte - 1, -1, -1)
# zählt dafür die Nummern rückwärts bis 0.
# Anderer Weg: Für jede Zeile der Raute den Abstand zur Mittelzeile ausrechnen,
# abstand = abs(nummer - breite // 2); dann hat die Zeile abstand Leerzeichen und
# breite - 2 * abstand Sternchen, und eine einzige Schleife reicht. Oder die Zeichen mit einer
# inneren Schleife einzeln anhängen wie in Aufgabe 2_014; das ist länger, geht aber genauso.
# Typische Fehler: die Mittelzeile der Raute zweimal ausgeben, die Leerzeichen links vergessen
# (dann entsteht ein schiefes Dreieck), mit f"{zeile:^{breite}}" zentrieren und dabei Leerzeichen am
# Zeilenende stehen lassen, oder range(1, hoehe) statt range(hoehe), dann fehlt die Spitze.
