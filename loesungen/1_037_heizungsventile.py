# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_037_heizungsventile.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_037_heizungsventile

"""Aufgabe 1_037 – Heizungsventile                               Stufe 1 ★☆☆☆☆

Im Bürogebäude melden Fenstersensoren an eine Steuerzentrale, wenn ein
Fenster offen steht. Die Zentrale schließt dann das smarte Heizungsventil
in diesem Raum, damit nicht zum Fenster hinaus geheizt wird. Das Programm
fragt nach zwei Räumen mit offenem Fenster.

Schreiben Sie oben im Programm eine eigene Funktion ventil_schliessen mit
einem Parameter raum. Sie soll für diesen Raum eine Zeile ausgeben:

    Ventil im Raum <raum> geschlossen, Heizung aus.

Unten im Programm wird die Funktion schon für den ersten Raum aufgerufen.
Ergänzen Sie an der zweiten markierten Stelle den Aufruf für den zweiten
Raum. Bei den Eingaben Büro und Küche soll das Programm ausgeben:

    Ventil im Raum Büro geschlossen, Heizung aus.
    Ventil im Raum Küche geschlossen, Heizung aus.
    Alle Meldungen bearbeitet.

Hintergrund: In Aufgabe 1_036 haben Sie eine fertige Funktion aufgerufen.
Eine eigene Funktion legen Sie mit def fest: def, der Name, in Klammern der
Parameter und ein Doppelpunkt. Darunter steht eingerückt der Rumpf, also
der Code, der bei jedem Aufruf läuft:

    def begruessen(name):
        print(f"Hallo {name}!")

    begruessen("Ada")       # gibt Hallo Ada! aus
    begruessen("Linus")     # gibt Hallo Linus! aus

Beim Aufruf bekommt der Parameter name den Wert in den Klammern. Die
Funktion muss festgelegt sein, bevor sie aufgerufen wird; darum steht def
oben im Programm. Diese Funktion gibt nur etwas aus und liefert keinen Wert
zurück, sie braucht kein return.
"""

def ventil_schliessen(raum):
    """Gibt aus, dass das Heizungsventil in diesem Raum geschlossen ist."""
    print(f"Ventil im Raum {raum} geschlossen, Heizung aus.")


raum_a = input("Erster Raum mit offenem Fenster: ")
raum_b = input("Zweiter Raum mit offenem Fenster: ")

ventil_schliessen(raum_a)
ventil_schliessen(raum_b)
print("Alle Meldungen bearbeitet.")


# Idee: Die Funktion bekommt den Raum als Parameter und gibt mit print die Zeile für genau diesen
# Raum aus. Unten wird sie zweimal aufgerufen, einmal mit raum_a und einmal mit raum_b; die
# Zeile mit dem Text steht so nur einmal im Programm.
# Anderer Weg: Im Rumpf geht auch print("Ventil im Raum", raum, "geschlossen, Heizung aus.").
# Ohne Funktion könnte man zwei print-Zeilen schreiben, aber dann müsste man bei einer Änderung
# des Textes beide Zeilen anpassen.
# Typische Fehler: im Rumpf raum_a statt raum benutzen (dann steht zweimal derselbe Raum da), den
# zweiten Aufruf vergessen, den Rumpf nicht einrücken (IndentationError) oder def erst unter den
# Aufrufen schreiben (NameError, die Funktion ist beim Aufruf noch nicht festgelegt).
