# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_032_energiezaehler.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_032_energiezaehler

"""Aufgabe 2_032 – Energiezähler                                 Stufe 2 ★★☆☆☆

In einem Bürogebäude melden smarte Zwischenstecker jede Stunde, wie
viel elektrische Energie das angeschlossene Gerät verbraucht hat. Die
Gebäudesteuerung legt die Meldungen als Tabelle ab: eine Liste von
Dictionaries, eines je Zeile, und alle Zeilen haben dieselben
Schlüssel, die Spalten der Tabelle:

    messungen = [
        {"geraet": "Kaffeemaschine", "raum": "Kueche", "stunde": 8, "wh": 350},
        {"geraet": "Drucker", "raum": "Flur", "stunde": 8, "wh": 40},
        {"geraet": "Kaffeemaschine", "raum": "Kueche", "stunde": 9, "wh": 120},
        {"geraet": "Monitor", "raum": "Buero 1", "stunde": 9, "wh": 30},
    ]

wh steht für Wattstunden, die Einheit der Energie. Die Haustechnik
möchte für beliebige Spalten auswerten können. Schreiben Sie drei
Funktionen, die immer neue Listen oder Zahlen zurückgeben und die
Tabelle nicht verändern:

- `spalte(tabelle, name)`: alle Werte der Spalte name als Liste, von
  der ersten bis zur letzten Zeile.
- `filtere(tabelle, name, wert)`: eine neue Tabelle (Liste) mit den
  Zeilen, in denen die Spalte name den Wert wert hat, in derselben
  Reihenfolge.
- `summe(tabelle, name)`: die Summe der Spalte name; bei einer
  leeren Tabelle 0.

    spalte(messungen, "geraet")
        →  ["Kaffeemaschine", "Drucker", "Kaffeemaschine", "Monitor"]
    filtere(messungen, "stunde", 9)
        →  [{"geraet": "Kaffeemaschine", …, "stunde": 9, "wh": 120},
            {"geraet": "Monitor", …, "stunde": 9, "wh": 30}]
    summe(filtere(messungen, "raum", "Kueche"), "wh")   →  470

Grenzen: 0 ≤ len(tabelle) ≤ 100 000. Alle Zeilen haben dieselben
Schlüssel, name ist immer einer davon. Die Werte sind Texte oder ganze
Zahlen von 0 bis 10**6; summe bekommt nur Spalten mit Zahlen. Groß-
und Kleinschreibung zählt beim Vergleich von Texten.

Hintergrund: Eine Tabelle mit Zeilen und benannten Spalten lässt sich
ohne jede Bibliothek als Liste von Dictionaries speichern; genau so
liefern viele Schnittstellen und Datenbanken ihre Daten aus, und
Bibliotheken wie pandas (Stufe 3) bauen darauf auf. Eine Zeile ist ein
Dictionary (Aufgabe 2_027), eine Spalte sind die Werte zu einem
Schlüssel in allen Zeilen. Der Schlüssel muss nicht fest im Code
stehen, er darf in einer Variablen stecken: Bei name = "wh" liefert
zeile[name] dasselbe wie zeile["wh"]. Darum kann eine Funktion mit
for zeile in tabelle (Aufgabe 2_030) jede beliebige Spalte auswerten.
Filtern heißt: eine neue Liste anlegen und nur die passenden Zeilen
mit append anhängen; die Zeilen selbst darf man dabei unverändert
übernehmen. Die Funktionen lassen sich hintereinanderschalten, weil
filtere wieder eine Tabelle liefert.
"""


def spalte(tabelle, name):
    """Gibt die Werte der Spalte name aus allen Zeilen als Liste zurück."""
    werte = []
    for zeile in tabelle:
        werte.append(zeile[name])
    return werte


def filtere(tabelle, name, wert):
    """Gibt die Zeilen zurück, deren Spalte name gleich wert ist."""
    passend = []
    for zeile in tabelle:
        if zeile[name] == wert:
            passend.append(zeile)
    return passend


def summe(tabelle, name):
    """Gibt die Summe der Spalte name zurück."""
    gesamt = 0
    for zeile in tabelle:
        gesamt = gesamt + zeile[name]
    return gesamt


messungen = [
    {"geraet": "Kaffeemaschine", "raum": "Kueche", "stunde": 8, "wh": 350},
    {"geraet": "Drucker", "raum": "Flur", "stunde": 8, "wh": 40},
    {"geraet": "Kaffeemaschine", "raum": "Kueche", "stunde": 9, "wh": 120},
    {"geraet": "Monitor", "raum": "Buero 1", "stunde": 9, "wh": 30},
]
print(spalte(messungen, "geraet"))
print(len(filtere(messungen, "stunde", 9)))
print(summe(filtere(messungen, "raum", "Kueche"), "wh"))


# Idee: Alle drei Funktionen gehen mit for zeile in tabelle einmal durch die Tabelle und greifen mit
# zeile[name] auf die gewünschte Spalte zu; weil name eine Variable ist, funktioniert jede Funktion für jede
# Spalte. spalte hängt den Wert an, filtere hängt die ganze Zeile an, wenn der Wert passt, summe addiert.
#
# Anderer Weg: summe kann die eingebaute Funktion benutzen: sum(spalte(tabelle, name)). Mit List
# Comprehensions (Stufe 3) wird jede Funktion ein Einzeiler, etwa [zeile for zeile in tabelle if zeile[name] == wert].
#
# Typische Fehler: zeile["name"] mit Anführungszeichen (dann wird die Spalte mit dem Namen „name“ gesucht,
# KeyError), die Tabelle selbst zurückgeben oder Zeilen aus ihr entfernen statt eine neue Liste aufzubauen,
# in summe mit gesamt = zeile[name] überschreiben statt addieren, oder "8" mit 8 verwechseln: Ein Text ist
# nie gleich einer Zahl.
