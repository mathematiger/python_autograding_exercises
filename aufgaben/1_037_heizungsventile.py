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

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


raum_a = input("Erster Raum mit offenem Fenster: ")
raum_b = input("Zweiter Raum mit offenem Fenster: ")

ventil_schliessen(raum_a)
pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
print("Alle Meldungen bearbeitet.")
