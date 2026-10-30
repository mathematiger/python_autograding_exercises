# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_006_warteschlange.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_006_warteschlange

"""Aufgabe 2_006 – Warteschlange im Service-Desk                Stufe 2 ★★☆☆☆

Im Service-Desk einer Firma stehen die offenen Tickets in einer
Warteschlange, das älteste zuerst. Für jedes Ticket ist notiert, wie viele
Minuten es seit der letzten Nachricht des Kunden auf eine Antwort wartet.
Mit den Kunden ist eine Reaktionsfrist vereinbart (SLA): Ein Ticket, das
länger als die Frist wartet, ist überfällig. Genau die Frist ist noch in Ordnung.

Vervollständigen Sie die Funktion `ueberfaellig(wartezeiten, frist)`, die
zählt, wie viele Tickets überfällig sind. Gehen Sie dafür die Liste mit
einer for-Schleife durch.

    ueberfaellig([95, 40, 61, 12], 60)  →  2
    ueberfaellig([60, 59], 60)          →  0
    ueberfaellig([], 60)                →  0

Das Programm darunter ist schon fertig und gibt aus:

    Offene Tickets: 4
    Ältestes Ticket wartet seit 95 Minuten
    Überfällig: 2

Grenzen: wartezeiten ist eine Liste mit 0 ≤ len(wartezeiten) ≤ 10 000
ganzen Zahlen, jede mit 0 ≤ wartezeit ≤ 10**6. frist ist eine ganze Zahl
mit 0 ≤ frist ≤ 10**6.

Hintergrund: Eine Liste fasst mehrere Werte in einer Variablen zusammen. Man
schreibt sie in eckige Klammern, mit Kommas getrennt; [] ist die leere
Liste. Wie bei Texten kommt man mit einem Index an einzelne Elemente, das
erste hat den Index 0, das letzte den Index -1, und len(liste) ist die
Anzahl der Elemente:

    zeiten = [95, 40, 61]
    zeiten[0]      →  95
    zeiten[-1]     →  61
    len(zeiten)    →  3

Eine for-Schleife geht eine Liste von vorn nach hinten durch und nimmt dabei
jedes Element einmal in die Variable hinter for:

    for zeit in zeiten:
        print(zeit)

Das gibt 95, 40 und 61 untereinander aus. Bei einer leeren Liste läuft der
Block gar nicht.

Tipp: Beginnen Sie mit einem Zähler 0 und erhöhen Sie ihn in der Schleife
bei jedem Ticket, das länger als frist wartet.
"""


def ueberfaellig(wartezeiten, frist):
    """Gibt zurück, wie viele Wartezeiten größer als frist sind."""
    anzahl = 0
    for wartezeit in wartezeiten:
        if wartezeit > frist:
            anzahl = anzahl + 1
    return anzahl


warteschlange = [95, 40, 61, 12]
print("Offene Tickets:", len(warteschlange))
print("Ältestes Ticket wartet seit", warteschlange[0], "Minuten")
print("Überfällig:", ueberfaellig(warteschlange, 60))


# Idee: Ein Zähler beginnt bei 0. Die for-Schleife nimmt jede Wartezeit einmal
# in die Variable wartezeit; ist sie größer als die Frist, wächst der Zähler um 1.
# Nach der Schleife steht in ihm die Anzahl der überfälligen Tickets. Bei einer
# leeren Liste läuft die Schleife gar nicht, und es bleibt bei 0.
#
# Anderer Weg: über die Indizes laufen, for i in range(len(wartezeiten)), und
# wartezeiten[i] vergleichen. Das geht auch, ist aber länger und schwerer zu lesen.
#
# Typische Fehler: >= statt > (dann zählt genau die Frist schon als überfällig),
# return im Schleifenblock (dann endet die Funktion nach dem ersten Ticket) oder
# den Zähler in der Schleife auf 0 setzen.
