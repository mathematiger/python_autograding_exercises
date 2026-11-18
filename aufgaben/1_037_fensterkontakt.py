"""Aufgabe 1_037 – Fensterkontakt                                Stufe 1 ★☆☆☆☆

In einem Bürogebäude sitzt an jedem Fenster ein kleiner Funksensor, ein
Fensterkontakt. Wird ein Fenster geöffnet, meldet er das an die Zentrale
der Gebäudetechnik. Die Zentrale schließt dann das Heizventil in diesem
Raum (ein Aktor, also ein Gerät, das etwas bewegt) und zeigt zwei
Zeilen an. Das Programm fragt nach zwei Räumen, in denen gerade ein
Fenster offen ist, und ruft für jeden Raum die Funktion warnung auf.
Diese Funktion fehlt noch.

Schreiben Sie die Funktion warnung mit einem Parameter raum. Sie soll
zwei Zeilen ausgeben und nichts zurückgeben. Bei den Eingaben Büro 2
und Labor gibt das Programm aus:

    Fenster offen: Büro 2
    Heizventil in Büro 2 wird geschlossen.
    Fenster offen: Labor
    Heizventil in Labor wird geschlossen.
    Alle Meldungen verschickt.

Hintergrund: In Aufgabe 1_036 haben Sie eine fertige Funktion
aufgerufen. Eine eigene Funktion legen Sie mit def an: hinter def
stehen der Name, in Klammern der Parameter und ein Doppelpunkt. Die
Zeilen darunter sind eingerückt und bilden den Rumpf der Funktion.

    def begruesse(name):
        print("Hallo", name)

    begruesse("Ada")      # gibt Hallo Ada aus
    begruesse("Linus")    # gibt Hallo Linus aus

Beim Festlegen mit def passiert noch nichts; erst jeder Aufruf führt
den Rumpf aus. Bei jedem Aufruf bekommt der Parameter name den Wert in
den Klammern. Eine Funktion ohne return gibt nichts zurück, sie tut
nur etwas, hier eine Ausgabe.

Tipp: Die Aufrufe unten im Programm sind schon da. Benutzen Sie in der
Funktion den Parameter raum, nicht fenster_1 oder fenster_2.
"""

fenster_1 = input("Raum mit offenem Fenster: ")
fenster_2 = input("Zweiter Raum mit offenem Fenster: ")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

warnung(fenster_1)
warnung(fenster_2)
print("Alle Meldungen verschickt.")
