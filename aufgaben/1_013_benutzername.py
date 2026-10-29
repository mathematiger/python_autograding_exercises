"""Aufgabe 1_013 – Benutzername                                   Stufe 1 ★☆☆☆☆

Neue Mitarbeitende legen sich im Intranet einer Firma über ein Formular ein
Konto an. Dort tippen sie ihren Benutzernamen und das Kürzel ihres Standorts
ein, zum Beispiel PB für Paderborn. Dabei passiert oft dasselbe: Jemand
tippt ein Leerzeichen zu viel vor oder hinter den Namen, schreibt den
Namen mal groß und mal klein oder das Kürzel klein. Das System soll solche
Eingaben selbst bereinigen, statt eine Fehlermeldung zu zeigen: Der
Benutzername wird ohne Leerzeichen am Rand und ganz in Kleinbuchstaben
gespeichert, das Standortkürzel ohne Leerzeichen am Rand und ganz in
Großbuchstaben.

Das Programm fragt schon nach beiden Eingaben. Ergänzen Sie die zwei
Zeilen, die die bereinigten Werte in die Variablen benutzer und standort
schreiben. Bei den Eingaben "  AMueller " und " pb  " soll das Programm
ausgeben:

    Benutzername: amueller (8 Zeichen)
    Standort: PB

Grenzen: Der Benutzername besteht aus 1 bis 20 Buchstaben ohne Umlaute, das
Standortkürzel aus zwei Buchstaben. Vor und hinter beiden Eingaben können bis
zu fünf Leerzeichen stehen.

Hintergrund: Texte bringen eigene Werkzeuge mit, die Methoden. Man ruft sie
mit einem Punkt hinter dem Text auf: text.upper() liefert den Text in
Großbuchstaben, text.lower() in Kleinbuchstaben, und text.strip() entfernt
Leerzeichen (auch Tabulatoren und Zeilenumbrüche) am Anfang und am Ende,
nicht aber in der Mitte. Bei text = "  Hallo Welt " ist text.strip() also
"Hallo Welt" und text.upper() "  HALLO WELT ". Der ursprüngliche Text
bleibt dabei unverändert; die Methode liefert einen neuen Text, den man in
einer Variablen speichern muss. Methoden kann man hintereinander hängen:
text.strip().lower() entfernt erst die Leerzeichen und macht dann alles
klein.

Tipp: Die Anzahl der Zeichen in der Ausgabe zeigt, ob noch Leerzeichen am
Rand übrig sind.
"""

eingabe_name = input("Benutzername: ")
eingabe_standort = input("Standort: ")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"Benutzername: {benutzer} ({len(benutzer)} Zeichen)")
print("Standort:", standort)
