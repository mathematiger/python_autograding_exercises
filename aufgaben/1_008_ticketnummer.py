"""Aufgabe 1_008 – Ticketnummer                                  Stufe 1 ★☆☆☆☆

Im IT-Support meldet man Störungen über ein Ticketsystem. Jede Störung bekommt
eine Ticketnummer aus dem Kürzel INC (für englisch „incident“, Störung), einem
Bindestrich und einer fortlaufenden Zahl, zum Beispiel INC-4712. Das Programm
fragt schon nach dem Namen der Person, die die Störung meldet, und nach der
Nummer des letzten Tickets; die neue Nummer ist um eins größer und steht
bereits in der Variablen nummer. Setzen Sie daraus die Bestätigung zusammen
und geben Sie sie aus. Bei Eingabe Meier und 4711 soll das Programm ausgeben:

    Hallo Meier, Ihre Störung hat die Nummer INC-4712.

Achten Sie genau auf die Zeichen: Zwischen INC- und der Zahl steht kein
Leerzeichen, und das Komma folgt direkt auf den Namen.

Hintergrund: Mit + kann man Texte aneinanderhängen: "INC-" + "4712" ergibt
"INC-4712". Anders als bei print mit Kommas fügt + kein Leerzeichen ein; wo
eines hingehört, muss es im Text selbst stehen. Eine Zahl kann man aber nicht
an einen Text hängen: "INC-" + 4712 bricht mit einem TypeError ab, weil Python
nicht weiß, ob es rechnen oder Text anhängen soll. Die Funktion str(...)
wandelt die Zahl vorher in einen Text um: "INC-" + str(4712) ergibt
"INC-4712".

Tipp: Bauen Sie zuerst die Ticketnummer in einer eigenen Variablen zusammen,
dann den ganzen Satz.
"""

name = input("Ihr Name: ")
letzte = int(input("Nummer des letzten Tickets: "))
nummer = letzte + 1

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
