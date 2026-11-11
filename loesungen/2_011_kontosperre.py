# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_011_kontosperre.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_011_kontosperre

"""Aufgabe 2_011 – Kontosperre                                  Stufe 2 ★★☆☆☆

Der Anmeldedienst im Firmennetz bremst jeden aus, der zu oft ein falsches
Passwort eingibt. Einige Fehlversuche sind erlaubt, denn jeder vertippt
sich einmal. Danach muss man vor dem nächsten Versuch warten, und mit
jedem weiteren Fehlversuch wird diese Wartezeit um eine feste Zahl von
Minuten länger. So kommt niemand weit, der Passwörter durch Ausprobieren
erraten will.

Schreiben Sie die Funktion `sperrzeit` mit den drei Parametern
`fehlversuche`, `erlaubt` mit dem Standardwert 3 und `minuten` mit dem
Standardwert 5. Sie gibt zurück, wie viele Minuten man vor dem nächsten
Versuch warten muss: 0, wenn `fehlversuche` höchstens `erlaubt` ist,
sonst (`fehlversuche` − `erlaubt`) · `minuten`, also `minuten` Minuten für
jeden Fehlversuch über die erlaubte Zahl hinaus. Für normale Konten
gelten die Standardwerte; für Administratorkonten, die besonders
geschützt werden müssen, gibt das Programm unten strengere Werte an.

    sperrzeit(2)          →  0
    sperrzeit(3)          →  0
    sperrzeit(5)          →  10
    sperrzeit(5, 4)       →  5
    sperrzeit(5, 1, 30)   →  120

Grenzen: Alle Werte sind ganze Zahlen mit 0 ≤ fehlversuche ≤ 100,
0 ≤ erlaubt ≤ 100 und 1 ≤ minuten ≤ 60.

Hintergrund: Diesmal schreiben Sie den Funktionskopf selbst. Er ist so
aufgebaut wie in den Vorlagen ab Aufgabe 2_002: def, Name, Parameter in
Klammern, Doppelpunkt, darunter eingerückt der Rumpf. Ein Parameter kann
im Funktionskopf einen Standardwert bekommen, indem man den Wert mit =
hinter den Parameternamen schreibt:

    def gruss(name, text="Hallo"):
        return text + ", " + name

Die Werte, die man beim Aufruf in die Klammern schreibt, heißen
Argumente. Das Argument für text darf man hier weglassen: gruss("Ada")
benutzt "Hallo" und ergibt "Hallo, Ada". Gibt man es an, gilt der
angegebene Wert: gruss("Ada", "Moin") ergibt "Moin, Ada". Die Argumente
werden von links nach rechts auf die Parameter verteilt, deshalb stehen
Parameter mit Standardwert immer hinter denen ohne; sonst meldet Python
einen SyntaxError. So bleibt der häufige Aufruf kurz, und man kann
trotzdem alles einstellen. Das kennen Sie schon von round:
round(2.2222) ergibt 2, round(2.2222, 1) ergibt 2.2 (Aufgabe 1_007); die
Zahl der Nachkommastellen ist ein Parameter mit Standardwert.

Tipp: Der Funktionskopf beginnt mit def sperrzeit(fehlversuche, …
"""

def sperrzeit(fehlversuche, erlaubt=3, minuten=5):
    """Gibt die Sperrzeit in Minuten nach fehlversuche falschen Anmeldungen zurück."""
    if fehlversuche <= erlaubt:
        return 0
    return (fehlversuche - erlaubt) * minuten


print("Normales Konto, 5 Fehlversuche:", sperrzeit(5), "Minuten")
print("Administratorkonto, 5 Fehlversuche:", sperrzeit(5, 1, 30), "Minuten")


# Idee: Die Standardwerte stehen im Funktionskopf: def sperrzeit(fehlversuche,
# erlaubt=3, minuten=5). Im Rumpf gibt es zwei Fälle: Bis zur erlaubten Zahl
# ist die Sperrzeit 0, darüber sind es (fehlversuche - erlaubt) * minuten.
#
# Anderer Weg: ohne if mit max(0, fehlversuche - erlaubt) * minuten, denn max
# macht aus einer negativen Zahl von Versuchen über erlaubt einfach 0.
#
# Typische Fehler: in der Rechnung fest mit 3 oder 5 statt mit den Parametern
# rechnen, das if vergessen (dann wird die Sperrzeit bei wenigen Fehlversuchen
# negativ) oder fehlversuche * minuten ohne das Abziehen der erlaubten Versuche.
