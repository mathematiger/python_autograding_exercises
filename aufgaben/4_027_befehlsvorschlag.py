"""Aufgabe 4_027 – Befehlsvorschlag                              Stufe 4 ★★★★☆

Ein Team entwickelt ein Kommandozeilenwerkzeug für seine Build- und
Testabläufe, mit Unterbefehlen wie build, test oder deploy. Gute
Werkzeuge reagieren freundlich auf Tippfehler: Wer „tset“ eintippt,
bekommt nicht nur „Unbekannter Befehl“, sondern „Meinten Sie test?“.
Dafür braucht man ein Maß, wie ähnlich sich zwei Wörter sind: die
Editierdistanz (auch Levenshtein-Distanz), die kleinste Zahl von
Einzelschritten, mit denen man ein Wort in das andere umbaut. Ein
Schritt fügt ein Zeichen ein, löscht eines oder ersetzt eines durch
ein anderes. Schreiben Sie zwei Funktionen:

- `editierdistanz(a, b)` gibt die Editierdistanz der Texte a und b
  zurück. Groß- und Kleinschreibung zählt.
- `vorschlaege(eingabe, befehle, hoechstens=2)` gibt die Befehle
  zurück, deren Editierdistanz zu eingabe höchstens hoechstens ist,
  die ähnlichsten zuerst, bei gleicher Distanz alphabetisch. Steht die
  Eingabe selbst unter den Befehlen, kommt sie mit Distanz 0 zuerst.

    editierdistanz("tset", "test")       →  2   (zwei Zeichen ersetzen)
    editierdistanz("biuld", "build")     →  2
    editierdistanz("deploy", "deplo")    →  1   (ein Zeichen löschen)
    editierdistanz("", "test")           →  4   (vier Zeichen einfügen)
    vorschlaege("tset", ["build", "test", "reset", "deploy"])
        →  ["reset", "test"]     (beide Distanz 2)
    vorschlaege("bild", ["build", "bind", "lint"], hoechstens=1)
        →  ["bind", "build"]

Grenzen: a, b und eingabe sind Texte mit 0 bis 500 Zeichen. befehle
hat 0 bis 200 verschiedene Einträge mit je 0 bis 30 Zeichen.
hoechstens ist eine ganze Zahl von 0 bis 30. editierdistanz soll
O(len(a) · len(b)) Schritte brauchen.

Hintergrund: Probiert man rekursiv alle Möglichkeiten aus, verzweigt
jeder Schritt in drei Richtungen; schon bei zwei Wörtern mit zehn
Buchstaben sind das Millionen Aufrufe, und fast alle rechnen
Teilprobleme aus, die es schon gab. Wie beim Rucksack (Aufgabe 4_026)
hilft dynamische Programmierung: Ein Teilproblem ist „Wie weit sind
die ersten i Zeichen von a von den ersten j Zeichen von b entfernt?“,
also durch zwei Zahlen bestimmt. Diese Distanzen d[i][j] schreibt man
in eine Tabelle mit len(a) + 1 Zeilen und len(b) + 1 Spalten.

Die erste Zeile und die erste Spalte sind leicht: Vom leeren Text zu
j Zeichen braucht man j Einfügungen, also d[0][j] = j, und umgekehrt
d[i][0] = i. Für jedes andere Feld schaut man auf das letzte Zeichen
der beiden Anfänge, a[i - 1] und b[j - 1]:

    Sind sie gleich, kostet es nichts:   d[i][j] = d[i - 1][j - 1]
    Sonst das Billigste aus drei Wegen:  d[i][j] = 1 + min(
        d[i - 1][j],        # a[i - 1] löschen
        d[i][j - 1],        # b[j - 1] einfügen
        d[i - 1][j - 1],    # a[i - 1] durch b[j - 1] ersetzen
    )

Man füllt die Tabelle Zeile für Zeile von oben nach unten, jede Zeile
von links nach rechts; dann sind die drei Nachbarn immer schon
ausgerechnet. Das Ergebnis steht rechts unten in d[len(a)][len(b)].
Für „ab“ und „b“:

            ""   "b"
    ""       0    1
    "a"      1    1      (a durch b ersetzen)
    "ab"     2    1      (b = b: wie links oben, also a löschen)

Jedes Feld kostet O(1), zusammen O(len(a) · len(b)). Zum Ordnen der
Vorschläge passt sorted mit einem Tupel als Schlüssel (Aufgabe 3_027).
"""


def editierdistanz(a, b):
    """Gibt die kleinste Zahl von Einfügungen, Löschungen und Ersetzungen zurück, die a in b umbaut."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def vorschlaege(eingabe, befehle, hoechstens=2):
    """Gibt die Befehle mit Editierdistanz höchstens hoechstens zurück, ähnlichste zuerst, dann alphabetisch."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(editierdistanz("tset", "test"))
print(vorschlaege("tset", ["build", "test", "reset", "deploy"]))
print(vorschlaege("bild", ["build", "bind", "lint"], hoechstens=1))
