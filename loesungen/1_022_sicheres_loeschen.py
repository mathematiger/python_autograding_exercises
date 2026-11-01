# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_022_sicheres_loeschen.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_022_sicheres_loeschen

"""Aufgabe 1_022 – Sicheres Löschen                              Stufe 1 ★☆☆☆☆

Bevor eine Firma alte Festplatten verkauft oder entsorgt, müssen alle
Kundendaten darauf verschwinden. Eine Datei einfach zu löschen reicht
nicht: Dabei entfernt das Betriebssystem nur den Verweis auf die Datei,
die Daten selbst bleiben stehen und lassen sich mit passenden Werkzeugen
wiederherstellen. Ein Löschprogramm überschreibt darum die ganze Platte
mehrmals hintereinander mit Zufallswerten; jedes Überschreiben heißt ein
Durchgang.

Das Programm fragt schon, wie viele Durchgänge es machen soll. Ergänzen
Sie die Schleife, die für jeden Durchgang eine Zeile ausgibt. Bei
Eingabe 3:

    Sicheres Löschen mit 3 Durchgängen
    Durchgang 1 von 3: Platte wird überschrieben
    Durchgang 2 von 3: Platte wird überschrieben
    Durchgang 3 von 3: Platte wird überschrieben
    Löschen abgeschlossen.

Bei Eingabe 0 erscheinen nur die erste und die letzte Zeile.

Grenzen: Die Anzahl der Durchgänge ist eine ganze Zahl von 0 bis 35.

Hintergrund: Eine for-Schleife wiederholt den eingerückten Block darunter.
range(n) liefert die Zahlen 0, 1, 2 bis n - 1, also genau n Zahlen, aber
bei 0 beginnend. Bei jedem Durchlauf bekommt die Variable hinter for die
nächste davon:

    for nummer in range(3):
        print("Runde", nummer)

gibt Runde 0, Runde 1 und Runde 2 aus. Soll die Zählung bei 1 beginnen,
rechnet man im Block nummer + 1. Bei range(0) läuft der Block gar nicht.
Was nach der Schleife nicht mehr eingerückt ist, läuft genau einmal,
wenn die Schleife fertig ist.
"""

anzahl = int(input("Anzahl der Durchgänge: "))
print(f"Sicheres Löschen mit {anzahl} Durchgängen")

for durchgang in range(anzahl):
    print(f"Durchgang {durchgang + 1} von {anzahl}: Platte wird überschrieben")

print("Löschen abgeschlossen.")


# Idee: for durchgang in range(anzahl) läuft genau anzahl-mal, durchgang ist dabei 0, 1, 2 und so
# weiter. Weil die Ausgabe bei 1 beginnen soll, steht im f-String durchgang + 1. Bei anzahl 0 läuft
# die Schleife gar nicht, und es bleiben nur die beiden vorgegebenen Zeilen.
# Anderer Weg: for durchgang in range(1, anzahl + 1) zählt gleich von 1 bis anzahl (das kommt in der
# nächsten Aufgabe), dann ohne + 1 im f-String.
# Typische Fehler: durchgang statt durchgang + 1 ausgeben (dann beginnt es bei Durchgang 0), range(3)
# statt range(anzahl) fest hinschreiben, den print nicht einrücken (dann läuft er nur einmal nach der
# Schleife) oder „von {anzahl}“ vergessen.
