r"""Aufgabe 3_046 – Artikelexport                                 Stufe 3 ★★★☆☆

Ein Onlinehändler zieht mit seinem Artikelstamm in eine neue Datenbank
um. Die alte Datenbank hat alle Artikel in eine Textdatei exportiert,
einen Datensatz pro Zeile, die Felder durch Semikolons getrennt. Die
erste Zeile ist die Kopfzeile mit den Feldnamen:

    artikelnummer;bezeichnung;preis
    A-1001;USB-Kabel;4.99
    A-1002;;12.50
    A-1003;Maus;19.90

    A-1004;Tastatur
    A-1005;Headset;39.00;Restposten

Bevor die Daten importiert werden, soll ein Skript die Datenqualität
prüfen. Schreiben Sie zwei Funktionen, die beide den Pfad der Datei als
Text bekommen:

- `lies_zeilen(pfad)` gibt alle Zeilen der Datei als Liste zurück, in
  ihrer Reihenfolge und ohne den Zeilenumbruch am Ende. Sonst bleibt
  jede Zeile, wie sie ist, auch Leerzeichen am Rand und leere Zeilen.
  Gibt es die Datei nicht, fängt lies_zeilen den FileNotFoundError nicht
  ab, damit der Aufrufer merkt, dass sie fehlt.
- `pruefe_export(pfad)` benutzt lies_zeilen und gibt ein Tupel zurück:
  die Anzahl der gültigen Datensätze und die Liste der Zeilennummern
  (ab 1, gezählt wie in der Datei) der fehlerhaften. Gültig ist eine
  Zeile mit genau drei Feldern, von denen keins leer ist oder nur aus
  Leerraum (Leerzeichen, Tabulatoren) besteht. Die Kopfzeile und Zeilen,
  die leer sind oder nur Leerraum enthalten, zählen weder als gültig noch
  als fehlerhaft.

Für die Datei oben:

    lies_zeilen(pfad)[:2]   →  ["artikelnummer;bezeichnung;preis", "A-1001;USB-Kabel;4.99"]
    pruefe_export(pfad)     →  (2, [3, 6, 7])

Zeile 3 hat keine Bezeichnung, Zeile 5 ist leer, Zeile 6 hat zu wenige
und Zeile 7 zu viele Felder. Die Tests legen die Dateien selbst an.

Grenzen: Die Datei ist in UTF-8 gespeichert und hat 1 bis 100 000
Zeilen; die erste ist immer die Kopfzeile. Eine Zeile hat höchstens 200
Zeichen. Die letzte Zeile kann mit oder ohne Zeilenumbruch enden.
Semikolons kommen nur als Trennzeichen vor.

Hintergrund: Bisher standen alle Daten im Programm. Mit open(pfad,
encoding="utf-8") öffnet man eine Datei zum Lesen; encoding sagt, wie
die Zeichen gespeichert sind (ohne die Angabe nimmt Windows eine andere
Kodierung, und aus „ö“ wird Zeichensalat). Eine geöffnete Datei muss
wieder geschlossen werden. Das übernimmt with: Am Ende des eingerückten
Blocks wird die Datei geschlossen, auch wenn darin ein Fehler auftritt.
Eine geöffnete Datei ist ein Iterator (Aufgabe 3_020): for liefert eine
Zeile nach der anderen, jede mit dem Zeilenumbruch "\n" am Ende, nur die
letzte vielleicht ohne:

    with open("notizen.txt", encoding="utf-8") as datei:
        for zeile in datei:
            print(zeile.rstrip("\n"))

zeile.rstrip("\n") entfernt nur Zeilenumbrüche am rechten Rand, strip()
dagegen allen Leerraum (Leerzeichen, Tabulatoren, Zeilenumbrüche) an
beiden Rändern (Aufgabe 1_013). Alternativ liest
datei.read() den ganzen Inhalt als einen Text, und text.splitlines()
zerlegt ihn in Zeilen ohne Umbrüche. Gibt es die Datei nicht, löst open
einen FileNotFoundError aus, eine Unterart von OSError (Aufgabe 3_030).
"""


def lies_zeilen(pfad):
    """Gibt die Zeilen der Datei ohne den Zeilenumbruch am Ende zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def pruefe_export(pfad):
    """Gibt (Anzahl gültiger Datensätze, Nummern der fehlerhaften Zeilen) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
