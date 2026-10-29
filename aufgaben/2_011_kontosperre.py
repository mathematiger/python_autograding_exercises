"""Aufgabe 2_011 – Kontosperre                                  Stufe 2 ★★☆☆☆

Wer ein Passwort durch Ausprobieren erraten will, braucht viele Versuche.
Deshalb sperrt die Anmeldung eines Firmennetzes ein Benutzerkonto für eine
Weile, wenn zu oft ein falsches Passwort eingegeben wurde. Einige
Fehlversuche sind erlaubt, denn jeder vertippt sich einmal. Für jeden
weiteren Fehlversuch darüber hinaus wird das Konto eine feste Zahl von
Minuten länger gesperrt.

Schreiben Sie die Funktion `sperrzeit` mit den drei Parametern fehlversuche,
erlaubt mit dem Standardwert 3 und minuten mit dem Standardwert 5. Sie gibt
zurück, wie viele Minuten das Konto gesperrt wird: 0,
solange fehlversuche nicht größer als erlaubt ist, sonst die Zahl der
Fehlversuche über erlaubt mal minuten. Für normale Konten gelten die
Standardwerte; für Administratorkonten, die besonders geschützt werden
müssen, gibt das Programm unten strengere Werte an.

    sperrzeit(2)          →  0
    sperrzeit(3)          →  0
    sperrzeit(5)          →  10
    sperrzeit(5, 4)       →  5
    sperrzeit(5, 1, 30)   →  120

Grenzen: Alle Werte sind ganze Zahlen mit 0 ≤ fehlversuche ≤ 1000,
0 ≤ erlaubt ≤ 100 und 1 ≤ minuten ≤ 1440.

Hintergrund: Ein Parameter kann im Funktionskopf einen Standardwert
bekommen, indem man ihn mit = dahinterschreibt: def gruss(name, text="Hallo").
Wer die Funktion aufruft, darf diesen Wert dann weglassen; gruss("Ada")
benutzt "Hallo". Gibt man ihn an, gilt der angegebene Wert: gruss("Ada",
"Moin"). Die Argumente werden von links nach rechts verteilt, deshalb
stehen Parameter mit Standardwert immer hinter denen ohne. So bleibt der
häufige Aufruf kurz, und man kann trotzdem alles einstellen.

Tipp: Der Funktionskopf beginnt mit def sperrzeit(fehlversuche, …
"""

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print("Normales Konto, 5 Fehlversuche:", sperrzeit(5), "Minuten")
print("Administratorkonto, 5 Fehlversuche:", sperrzeit(5, 1, 30), "Minuten")
