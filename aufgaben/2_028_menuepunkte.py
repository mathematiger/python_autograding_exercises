"""Aufgabe 2_028 – Menüpunkte                                   Stufe 2 ★★☆☆☆

Eine Firma testet das neue Menü ihrer Buchhaltungssoftware. In einem
Usability-Test (einem Test, wie gut sich etwas bedienen lässt) lösen
mehrere Testpersonen dieselben Aufgaben, und die Software zeichnet für
jede Person auf, welche Menüpunkte sie angeklickt hat, in der
Reihenfolge der Klicks und oft mehrfach. Das Designteam will daraus
ablesen, welche Menüpunkte unverzichtbar sind und welche man
streichen oder besser platzieren sollte. Schreiben Sie drei
Funktionen; jede gibt eine alphabetisch sortierte Liste ohne Doppelte
zurück:

- `angeklickt(klicks)` bekommt die Klicks einer Person als Liste und
  gibt alle Menüpunkte zurück, die sie mindestens einmal benutzt hat.
- `von_allen(protokolle)` bekommt eine Liste mit den Klicklisten aller
  Personen und gibt die Menüpunkte zurück, die jede Person mindestens
  einmal benutzt hat.
- `ungenutzt(menue, protokolle)` gibt die Menüpunkte aus der Liste
  menue zurück, die keine Person benutzt hat.

Alle drei lassen die übergebenen Listen unverändert.

    klicks_a = ["Datei", "Rechnung", "Datei", "Hilfe"]
    klicks_b = ["Rechnung", "Export", "Datei", "Rechnung"]
    angeklickt(klicks_a)                        →  ["Datei", "Hilfe", "Rechnung"]
    von_allen([klicks_a, klicks_b])             →  ["Datei", "Rechnung"]
    menue = ["Datei", "Export", "Hilfe", "Rechnung", "Steuern", "Vorlagen"]
    ungenutzt(menue, [klicks_a, klicks_b])      →  ["Steuern", "Vorlagen"]

Grenzen: Menüpunkte sind nicht leere Texte; Groß- und Kleinschreibung
zählt ("Datei" und "datei" sind verschieden). klicks hat 0 bis 100 000
Einträge. protokolle hat 1 bis 1000 Klicklisten, zusammen höchstens
100 000 Klicks, jede Klickliste darf auch leer sein. menue hat 1 bis
1000 verschiedene Menüpunkte; in den Klicklisten können auch Punkte
stehen, die nicht in menue stehen (etwa aus einer alten Version).

Hintergrund: Eine Menge (set) ist eine Sammlung ohne Reihenfolge, in
der jeder Wert höchstens einmal vorkommt. set(liste) macht aus einer
Liste eine Menge und entfernt dabei alle Doppelten; sorted(menge)
macht daraus wieder eine sortierte Liste. Ob ein Wert in einer Menge
steht, prüft in, und das geht auch bei sehr großen Mengen schnell.
Zwei Mengen verknüpft man mit Operatoren:

    a = {"Datei", "Hilfe"}
    b = {"Datei", "Export"}
    a & b      # Schnitt: {"Datei"}, was in beiden steht
    a | b      # Vereinigung: {"Datei", "Hilfe", "Export"}, was in mindestens einer steht
    a - b      # Differenz: {"Hilfe"}, was in a steht, aber nicht in b

Eine leere Menge schreibt man set(), denn {} ist ein leeres
Dictionary. Mit a = a | b oder kurz a |= b wächst eine Menge Schritt
für Schritt, etwa in einer for-Schleife über mehrere Listen.
"""


def angeklickt(klicks):
    """Gibt die sortierte Liste der Menüpunkte zurück, die in klicks vorkommen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def von_allen(protokolle):
    """Gibt die sortierte Liste der Menüpunkte zurück, die in jeder Klickliste vorkommen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ungenutzt(menue, protokolle):
    """Gibt die sortierte Liste der Menüpunkte aus menue zurück, die niemand benutzt hat."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


klicks_a = ["Datei", "Rechnung", "Datei", "Hilfe"]
klicks_b = ["Rechnung", "Export", "Datei", "Rechnung"]
print(angeklickt(klicks_a))
print(von_allen([klicks_a, klicks_b]))
print(ungenutzt(["Datei", "Export", "Hilfe", "Rechnung", "Steuern", "Vorlagen"], [klicks_a, klicks_b]))
