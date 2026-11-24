# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_068_integrationsplan.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_068_integrationsplan

"""Aufgabe 3_068 – Integrationsplan                              Stufe 3 ★★★☆☆

Zwei Teams bauen gemeinsam eine neue Version einer Bestell-App: Team A
die Oberfläche, Team B die Schnittstelle zum Lager. Beide arbeiten ihre
Arbeitspakete in einer festen Reihenfolge ab, und es wird immer genau
ein Paket auf einmal abgenommen, mal eins von Team A, mal eins von
Team B. Ein Zwischenstand ist ein Paar (a, b): Team A hat a Pakete
fertig, Team B b Pakete. Manche Zwischenstände darf es nicht geben, zum
Beispiel weil dann eine Oberfläche ausgeliefert würde, deren
Schnittstelle noch fehlt. Die Projektleitung will wissen, wie viele
mögliche Reihenfolgen der Abnahmen es gibt, die nie durch einen
gesperrten Zwischenstand führen.

Die Zwischenstände stehen in einem Raster aus Textzeilen: Zeile a,
Spalte b ist der Zwischenstand (a, b), "." heißt erlaubt, "#" gesperrt.
Der Start ist oben links (0, 0), das Ziel unten rechts, wenn beide Teams
fertig sind. Jede Abnahme geht genau ein Feld nach unten (Team A) oder
nach rechts (Team B). Schreiben Sie zwei Funktionen:

- `tabelle(raster)` gibt eine Liste von Listen zurück, so groß wie das
  Raster: In Zeile a, Spalte b steht, auf wie vielen Wegen man vom Start
  zum Zwischenstand (a, b) kommt, ohne ein gesperrtes Feld zu betreten.
  Ein gesperrtes Feld bekommt 0.
- `reihenfolgen(raster)` gibt die Anzahl der Wege bis zum Ziel zurück.

    raster = ["....",
              ".#..",
              "...#",
              "...."]
    tabelle(raster)
        →  [[1, 1, 1, 1],
            [1, 0, 1, 2],
            [1, 1, 2, 0],
            [1, 2, 4, 4]]
    reihenfolgen(raster)          →  4
    reihenfolgen(["...", "..."])  →  3

Ist der Start oder das Ziel gesperrt, gibt es keinen Weg, das Ergebnis
ist 0.

Grenzen: 1 ≤ len(raster) ≤ 300, alle Zeilen sind gleich lang mit
1 ≤ len(zeile) ≤ 300 und bestehen nur aus "." und "#". Auch Start und
Ziel dürfen "#" sein. Die Anzahlen werden sehr groß (bei 300 × 300 ohne
Sperre hat sie 179 Stellen); Python rechnet mit ganzen Zahlen beliebiger
Größe genau. Ihre Lösung soll O(Zeilen · Spalten) Schritte brauchen.

Hintergrund: In Aufgabe 3_067 haben Sie Möglichkeiten mit einer Tabelle
von unten gezählt: Man beginnt beim kleinsten Fall, dessen Anzahl man
kennt, und berechnet jeden weiteren Eintrag aus den schon fertigen
Einträgen davor, ganz ohne Rekursion. Das geht auch in zwei Dimensionen.
Auf das Feld (a, b) kommt man nur von oben, aus (a - 1, b), oder von
links, aus (a, b - 1). Jeder Weg zu (a, b) ist also ein Weg zu einem der
beiden Nachbarn plus ein letzter Schritt, und deshalb gilt:

    wege[a][b] = wege[a - 1][b] + wege[a][b - 1]

Fehlt ein Nachbar, weil (a, b) in der obersten Zeile oder der linken
Spalte liegt, zählt er als 0. Ein gesperrtes Feld bekommt 0, damit kein
Weg über es weiterläuft, und der Start bekommt 1 (der leere Weg), wenn er
frei ist. Füllen Sie die Tabelle Zeile für Zeile von oben nach unten und
in jeder Zeile von links nach rechts: Dann sind oben und links immer
schon fertig, wenn Sie ein Feld berechnen. Eine Liste von Listen legen
Sie wie in Aufgabe 2_020 an, und zwar jede Zeile als eigene Liste:
[[0] * spalten for _ in range(zeilen)]. Mit [[0] * spalten] * zeilen
stünde dieselbe Liste mehrmals darin (Aufgabe 2_018).

Rekursiv mit Memoisierung (Aufgabe 3_033) ginge es auch, aber die
Tabelle braucht keinen Aufrufstapel und zeigt alle Zwischenergebnisse
auf einen Blick. Alle Wege einzeln abzulaufen wäre hoffnungslos: Schon
bei 20 × 20 Feldern ohne Sperre sind es über 35 Milliarden.

Tipp: Achten Sie auf die oberste Zeile und die linke Spalte. Dort gibt
es nicht überall genau einen Weg: Hinter einem "#" in der obersten Zeile
kommt man nur noch von oben hin, und da ist nichts.
"""


def tabelle(raster):
    """Gibt zu jedem Feld die Anzahl der Wege vom Start dorthin zurück (gesperrte Felder 0)."""
    zeilen = len(raster)
    spalten = len(raster[0])
    wege = [[0] * spalten for _ in range(zeilen)]
    for a in range(zeilen):
        for b in range(spalten):
            if raster[a][b] == "#":
                continue
            if a == 0 and b == 0:
                wege[a][b] = 1
                continue
            von_oben = wege[a - 1][b] if a > 0 else 0
            von_links = wege[a][b - 1] if b > 0 else 0
            wege[a][b] = von_oben + von_links
    return wege


def reihenfolgen(raster):
    """Gibt die Anzahl der Wege vom Start zum Ziel unten rechts zurück."""
    return tabelle(raster)[-1][-1]


raster = ["....",
          ".#..",
          "...#",
          "...."]
print(tabelle(raster))
print(reihenfolgen(raster))


# Idee: Legen Sie eine Tabelle wege so groß wie das Raster an, mit lauter Nullen. Gehen Sie Zeile für
# Zeile und darin von links nach rechts durch: Ein gesperrtes Feld bleibt 0, der freie Start bekommt 1,
# jedes andere freie Feld die Summe aus dem Feld darüber und dem links daneben (fehlt eins am Rand,
# zählt es 0). reihenfolgen gibt das Feld unten rechts zurück, also tabelle(raster)[-1][-1].
# Anderer Weg: Für die Anzahl allein genügt eine einzige Zeile Speicher. Man überschreibt sie Zeile für
# Zeile: zeile[b] = zeile[b] + zeile[b - 1], wobei zeile[b] vor dem Überschreiben noch der Wert von oben
# ist. Rekursiv mit Memoisierung (Aufgabe 3_033) geht es auch, braucht aber einen Aufrufstapel so tief
# wie der Weg lang ist. Naiv läuft man jeden Weg einzeln ab; ohne Sperre sind das bei n × n Feldern
# etwa 4**n / √n Wege, also exponentiell viele.
# Typische Fehler: die oberste Zeile und linke Spalte pauschal mit 1 füllen (hinter einem # ist dort 0),
# gesperrten Start oder gesperrtes Ziel vergessen, wege[a - 1][b] in Zeile 0 lesen (Index -1 ist in
# Python die letzte Zeile, das gibt keinen Fehler, aber falsche Zahlen), die Tabelle mit
# [[0] * spalten] * zeilen anlegen (alle Zeilen sind dieselbe Liste).
# Laufzeit: Jedes der Zeilen · Spalten Felder wird einmal mit zwei Additionen berechnet, also
# O(Zeilen · Spalten); die Tabelle braucht ebenso viel Speicher, die Variante mit einer Zeile nur O(Spalten).
