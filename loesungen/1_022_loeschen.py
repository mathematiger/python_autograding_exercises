# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_022_loeschen.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_022_loeschen

"""Aufgabe 1_022 – Sicheres Löschen                              Stufe 1 ★☆☆☆☆

Alte Festplatten aus der Buchhaltung sollen verkauft werden. Vorher
müssen die Daten darauf sicher gelöscht werden, denn einfaches Löschen
entfernt nur den Verweis auf eine Datei, die Daten selbst bleiben
lesbar. Ein Löschprogramm überschreibt deshalb die ganze Platte mehrmals
mit Zufallsdaten; jeder solche Durchgang heißt Überschreibdurchgang. Das
Programm fragt schon nach der Anzahl der Durchgänge. Ergänzen Sie eine
for-Schleife, die für jeden Durchgang eine Zeile ausgibt. Bei Eingabe 3:

    Durchgang 1 von 3: überschrieben
    Durchgang 2 von 3: überschrieben
    Durchgang 3 von 3: überschrieben
    Löschen abgeschlossen.

Grenzen: Die Anzahl der Durchgänge ist eine ganze Zahl von 1 bis 35.

Hintergrund: Eine for-Schleife wiederholt die eingerückten Zeilen unter
ihr. range(n) liefert nacheinander die Zahlen 0, 1, 2 bis n - 1, also
genau n Zahlen; die Variable hinter for bekommt bei jedem Durchlauf die
nächste davon:

    for nummer in range(3):
        print("Hallo", nummer)

gibt „Hallo 0“, „Hallo 1“ und „Hallo 2“ aus. Weil range bei 0 anfängt,
schreibt man nummer + 1, wenn ab 1 gezählt werden soll. Was nicht mehr
eingerückt ist, läuft erst nach der Schleife, und zwar nur einmal.
"""

durchgaenge = int(input("Anzahl der Überschreibdurchgänge: "))

for nummer in range(durchgaenge):
    print(f"Durchgang {nummer + 1} von {durchgaenge}: überschrieben")

print("Löschen abgeschlossen.")


# Idee: for nummer in range(durchgaenge) wiederholt den Block genau durchgaenge-mal, nummer läuft
# dabei von 0 bis durchgaenge - 1. Darum steht in der Ausgabe nummer + 1. Das print für
# „Löschen abgeschlossen.“ ist nicht eingerückt und läuft nach der Schleife einmal.
# Anderer Weg: range(1, durchgaenge + 1) liefert gleich die Zahlen ab 1 (das kommt in der nächsten
# Aufgabe), oder eine while-Schleife mit eigenem Zähler (Aufgabe 2_004).
# Typische Fehler: nummer statt nummer + 1 ausgeben (dann beginnt die Liste mit Durchgang 0),
# range(durchgaenge + 1) (ein Durchgang zu viel) oder die letzte Zeile mit in die Schleife einrücken.
