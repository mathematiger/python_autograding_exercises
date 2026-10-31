"""Aufgabe 3_016 – Kundenimport                                  Stufe 3 ★★★☆☆

Eine Firma übernimmt die Kundendaten eines anderen Unternehmens. Jeder
Datensatz ist ein Dictionary mit Texten, etwa {"name": "Ada", "alter":
"36"}. Bevor die Daten in die eigene Datenbank kommen, soll ein kleines
Skript import.py das Durchschnittsalter berechnen, um die Datenqualität
zu prüfen. Die Zahlen links gehören nicht zum Code, sondern sind die
Zeilennummern:

     1  def lies_alter(datensatz):
     2      # Das Alter steht als Text im Datensatz
     3      return int(datensatz["alter"])
     4
     5
     6  def durchschnittsalter(kunden):
     7      summe = 0
     8      anzahl = 0
     9      for datensatz in kunden:
    10          if datensatz["alter"] != "":
    11              summe = summe + lies_alter(datensatz)
    12              anzahl = anzahl + 1
    13      return round(summe / anzahl, 1)
    14
    15
    16  kunden = lade_kunden()
    17  print(durchschnittsalter(kunden))

Mit drei verschiedenen Exportdateien bricht das Skript dreimal ab:

    Traceback (most recent call last):
      File "import.py", line 17, in <module>
        print(durchschnittsalter(kunden))
              ^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "import.py", line 11, in durchschnittsalter
        summe = summe + lies_alter(datensatz)
                        ^^^^^^^^^^^^^^^^^^^^^
      File "import.py", line 3, in lies_alter
        return int(datensatz["alter"])
               ^^^^^^^^^^^^^^^^^^^^^^^
    ValueError: invalid literal for int() with base 10: 'unbekannt'

    Traceback (most recent call last):
      File "import.py", line 17, in <module>
        print(durchschnittsalter(kunden))
              ^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "import.py", line 10, in durchschnittsalter
        if datensatz["alter"] != "":
           ~~~~~~~~~^^^^^^^^^
    KeyError: 'alter'

    Traceback (most recent call last):
      File "import.py", line 17, in <module>
        print(durchschnittsalter(kunden))
              ^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "import.py", line 13, in durchschnittsalter
        return round(summe / anzahl, 1)
                     ~~~~~~^~~~~~~~
    ZeroDivisionError: division by zero

Schreiben Sie zwei Funktionen:

- `fehlerstellen()` gibt für die drei Tracebacks in dieser Reihenfolge je
  ein Tupel (funktion, zeile, fehlerart) zurück: den Namen der Funktion
  und die Zeilennummer, in der der Fehler tatsächlich passiert ist, und
  den Namen der Ausnahme, zum Beispiel ("main", 5, "TypeError").
- `durchschnittsalter(kunden)` ist die korrigierte Fassung: Sie
  berücksichtigt nur Datensätze, die einen Schlüssel "alter" haben, dessen
  Text aus mindestens einer Ziffer und sonst nichts besteht. Sie gibt den
  Durchschnitt dieser Alter auf eine Nachkommastelle gerundet zurück,
  oder None, wenn es keinen solchen Datensatz gibt.

    durchschnittsalter([{"name": "Ada", "alter": "36"}, {"name": "Bo", "alter": "unbekannt"},
                        {"name": "Cem"}, {"name": "Dana", "alter": "41"}])   →  38.5
    durchschnittsalter([{"name": "Eli", "alter": ""}])                      →  None

Grenzen: kunden hat 0 bis 100 000 Einträge. Jeder ist ein Dictionary mit
einem Schlüssel "name" und vielleicht einem Schlüssel "alter"; dessen
Wert ist ein Text aus 0 bis 10 Zeichen, nur Buchstaben a bis z, Ziffern
0 bis 9, Leerzeichen, "-" und ".". Ein gültiges Alter liegt zwischen 0
und 150.

Hintergrund: Bricht ein Programm mit einer Ausnahme ab, druckt Python
einen Traceback, den Weg durch die Aufrufe bis zur Fehlerstelle. Man
liest ihn von unten nach oben. Die letzte Zeile nennt die Art der
Ausnahme und eine Beschreibung, etwa ValueError: invalid literal for
int() with base 10: 'unbekannt' (der Text 'unbekannt' ließ sich nicht in
eine ganze Zahl umwandeln). Darüber stehen die Aufrufe, der zuletzt
aufgerufene ganz unten: Jeder Eintrag File "…", line …, in … nennt Datei,
Zeile und Funktion, darunter steht die Zeile selbst. Die Marken ^^^ und
~~~ zeigen, welcher Teil der Zeile den Fehler ausgelöst hat. Der
unterste Eintrag ist die Stelle, an der der Fehler passiert ist; die
Einträge darüber zeigen, wer diese Funktion aufgerufen hat. <module>
heißt: auf oberster Ebene des Skripts, außerhalb jeder Funktion.

Die Ursache liegt nicht immer in der untersten Zeile. int(...) in
lies_alter ist richtig; falsch ist, dass durchschnittsalter die Funktion
mit einem Text aufruft, der keine Zahl ist. Darum fragt man nach dem
Lesen: Mit welchem Wert ist das Programm hier angekommen, und wo hätte
dieser Wert aussortiert werden müssen?

Tipp: Mit datensatz.get("alter", "") bekommt man auch bei einem fehlenden
Schlüssel einen Text; "36".isdigit() ist True, "".isdigit() und
"3 6".isdigit() sind False.
"""


def fehlerstellen():
    """Gibt für die drei Tracebacks je (funktion, zeile, fehlerart) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def durchschnittsalter(kunden):
    """Gibt das Durchschnittsalter der Datensätze mit gültigem Alter zurück, gerundet; None, wenn es keine gibt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kunden = [
    {"name": "Ada", "alter": "36"},
    {"name": "Bo", "alter": "unbekannt"},
    {"name": "Cem"},
    {"name": "Dana", "alter": "41"},
]
print(fehlerstellen())
print(durchschnittsalter(kunden))
print(durchschnittsalter([{"name": "Eli", "alter": ""}]))
