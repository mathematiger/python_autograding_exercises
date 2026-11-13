"""Aufgabe 1_034 – Ping-Zeiten                                   Stufe 1 ★☆☆☆☆

Bei einer Störung im Netzwerk misst eine Technikerin mit dem Befehl ping
mehrmals, wie lange ein Datenpaket zum Server und zurück braucht, die
Antwortzeit in Millisekunden (ms). Die Werte tippt sie nacheinander in
ein kleines Programm ein. Wenn sie fertig ist, gibt sie stop ein. Das
Programm zählt die Messungen, addiert sie und zeigt am Ende den
Durchschnitt an.

Der vorgegebene Code fragt einmal nach einer Eingabe und gibt am Ende das
Ergebnis aus. Ergänzen Sie dazwischen eine while-Schleife, die läuft,
solange die Eingabe nicht "stop" ist: Im Block zählen Sie anzahl um 1
hoch, addieren die Zahl zu summe und fragen mit derselben input-Zeile
nach dem nächsten Wert. Bei den Eingaben 12, 18, 30 und stop:

    3 Messungen, Durchschnitt: 20.0 ms

Gibt die Technikerin gleich stop ein, erscheint „Keine Messungen.“.

Grenzen: Es gibt 0 bis 50 Messungen, jede ist eine ganze Zahl von 1 bis
2000. Das Wort stop ist immer klein geschrieben.

Hintergrund: Eine while-Schleife wiederholt ihren Block, solange ihre
Bedingung wahr ist (Aufgabe 1_033). Weiß man nicht, wie viele Eingaben
kommen, liest man die erste vor der Schleife und die nächste am Ende des
Blocks. So prüft die Bedingung immer die neueste Eingabe:

    eingabe = input("...")
    while eingabe != "stop":
        ...                      # eingabe verarbeiten
        eingabe = input("...")

Fehlt die letzte Zeile, bleibt eingabe für immer gleich, und die Schleife
läuft endlos.
"""

anzahl = 0
summe = 0
eingabe = input("Antwortzeit in ms (stop zum Beenden): ")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

if anzahl == 0:
    print("Keine Messungen.")
else:
    print(f"{anzahl} Messungen, Durchschnitt: {summe / anzahl:.1f} ms")
