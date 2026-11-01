"""Aufgabe 4_018 – Abfragen                                        Stufe 4 ★★★★☆

Eine Firma hält ihre Kundendaten als Tabelle: eine Liste von
Datensätzen, jeder ein Dictionary mit denselben Spalten. Wer etwas
wissen will, schreibt bisher jedes Mal eine eigene Schleife. Das soll
einfacher werden, ähnlich wie eine Abfrage in SQL, die bestimmte Spalten
der Zeilen liefert, die alle Bedingungen erfüllen:

    SELECT name, ort FROM kunden WHERE ort = 'Paderborn' AND aktiv = 1

Außerdem will die Datenschutzbeauftragte nachvollziehen können, welche
Abfragen gelaufen sind. Dafür soll eine Hilfsfunktion jede beliebige
Funktion aufrufen und den Aufruf vorher in ein Protokoll schreiben.

Vervollständigen Sie:

- `waehle(datensaetze, *spalten, **bedingungen)`: Gibt eine Liste neuer
  Dictionaries zurück, eins für jeden Datensatz, bei dem jede Bedingung
  spalte=wert erfüllt ist (datensatz[spalte] == wert), in der Reihenfolge
  der Datensätze. Die neuen Dictionaries enthalten nur die angegebenen
  Spalten, in der Reihenfolge der Angabe; ohne Spaltenangabe alle
  Spalten. Ohne Bedingungen passt jeder Datensatz.
- `mit_protokoll(protokoll, funktion, *args, **kwargs)`: Hängt an die
  Liste protokoll einen Text an und ruft dann funktion mit allen
  weiteren Positions- und Schlüsselwortargumenten auf; gibt deren
  Ergebnis zurück. Der Text lautet
  "<Name der Funktion>: <Anzahl> Positionsargumente, Schlüsselwörter: <Namen>",
  die Namen der Schlüsselwortargumente in der Reihenfolge des Aufrufs mit
  ", " getrennt, oder "keine", wenn es keine gibt. Löst funktion eine
  Ausnahme aus, steht der Eintrag trotzdem im Protokoll, und die Ausnahme
  kommt beim Aufrufer an.

    kunden = [
        {"nr": 1, "name": "Ada", "ort": "Paderborn", "aktiv": True},
        {"nr": 2, "name": "Alan", "ort": "Bielefeld", "aktiv": True},
        {"nr": 3, "name": "Grace", "ort": "Paderborn", "aktiv": False},
    ]
    waehle(kunden, "name", ort="Paderborn")
        →  [{"name": "Ada"}, {"name": "Grace"}]
    waehle(kunden, "name", "nr", ort="Paderborn", aktiv=True)
        →  [{"name": "Ada", "nr": 1}]
    waehle(kunden, aktiv=False)
        →  [{"nr": 3, "name": "Grace", "ort": "Paderborn", "aktiv": False}]
    protokoll = []
    mit_protokoll(protokoll, waehle, kunden, "name", ort="Bielefeld")
        →  [{"name": "Alan"}]
    protokoll  →  ["waehle: 2 Positionsargumente, Schlüsselwörter: ort"]

Grenzen: datensaetze hat 0 bis 100 000 Einträge, alle mit denselben
Spalten; jede Spalte, die in spalten oder bedingungen vorkommt, gibt es.
Die Spalten in spalten sind verschieden. Die Schlüsselwortargumente von
mit_protokoll heißen nie protokoll oder funktion; funktion ist eine
gewöhnliche Funktion mit Namen.

Hintergrund: Ein Parameter mit einem Stern sammelt alle übrigen
Positionsargumente in einem Tupel, einer mit zwei Sternen alle übrigen
Schlüsselwortargumente in einem Dictionary:

    def zeige(titel, *werte, **optionen):
        print(titel, werte, optionen)

    zeige("A", 1, 2, farbe="rot", fett=True)
        →  A (1, 2) {'farbe': 'rot', 'fett': True}
    zeige("B")
        →  B () {}

Die Namen sind frei; üblich sind *args und **kwargs. Die Reihenfolge in
der Parameterliste ist fest: gewöhnliche Parameter, dann *args, dann
**kwargs. Im Dictionary stehen die Schlüsselwörter in der Reihenfolge,
in der der Aufrufer sie geschrieben hat.

Beim Aufruf tun die Sterne das Umgekehrte und packen aus: f(*liste)
übergibt die Elemente der Liste als einzelne Positionsargumente,
f(**dictionary) die Einträge als Schlüsselwortargumente. Zusammen
ergibt das das wichtigste Muster dafür: eine Funktion, die alles, was
sie bekommt, unverändert weiterreicht, ohne die Parameter der anderen
Funktion zu kennen:

    def zweimal(funktion, *args, **kwargs):
        funktion(*args, **kwargs)
        return funktion(*args, **kwargs)

    zweimal(print, "Hallo", end="!\\n")   →  gibt zweimal Hallo! aus

Den Namen einer Funktion liefert funktion.__name__, etwa "print".
"""


def waehle(datensaetze, *spalten, **bedingungen):
    """Gibt die passenden Datensätze als neue Dictionaries mit den angegebenen Spalten zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def mit_protokoll(protokoll, funktion, *args, **kwargs):
    """Schreibt den Aufruf ins Protokoll, ruft funktion(*args, **kwargs) auf und gibt das Ergebnis zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kunden = [
    {"nr": 1, "name": "Ada", "ort": "Paderborn", "aktiv": True},
    {"nr": 2, "name": "Alan", "ort": "Bielefeld", "aktiv": True},
    {"nr": 3, "name": "Grace", "ort": "Paderborn", "aktiv": False},
]
print(waehle(kunden, "name", ort="Paderborn"))
print(waehle(kunden, "name", "nr", ort="Paderborn", aktiv=True))
protokoll = []
print(mit_protokoll(protokoll, waehle, kunden, "name", ort="Bielefeld"))
print(protokoll)
