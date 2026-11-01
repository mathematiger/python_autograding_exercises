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

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print("Löschen abgeschlossen.")
