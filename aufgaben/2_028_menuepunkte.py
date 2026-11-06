"""Aufgabe 2_028 – Menüpunkte                                   Stufe 2 ★★☆☆☆

Eine Firma hat das Menü ihrer Buchhaltungssoftware neu geordnet. In
einem Usability-Test (einem Test, wie gut sich etwas bedienen lässt)
lösen mehrere Testpersonen dieselben Aufgaben, und die Software
protokolliert für jede Person, welche Menüpunkte sie der Reihe nach
angeklickt hat, auch denselben Punkt mehrmals. Das Team will wissen,
welche Menüpunkte überhaupt jemand benutzt hat und welche alle
gefunden haben. Schreiben Sie drei Funktionen, die jeweils eine Menge
(set) zurückgeben:

- `angeklickt(klicks)`: die Menüpunkte aus der Liste klicks einer
  Person, jeder nur einmal.
- `von_allen(protokolle)`: die Menüpunkte, die jede Person mindestens
  einmal angeklickt hat. protokolle ist eine Liste, die für jede Person
  ihre Liste klicks enthält.
- `von_irgendwem(protokolle)`: die Menüpunkte, die mindestens eine
  Person angeklickt hat.

Die Listen in protokolle bleiben dabei unverändert.

    anna = ["Datei", "Rechnung", "Datei", "Hilfe"]
    ben = ["Rechnung", "Export", "Rechnung"]
    angeklickt(anna)              →  {"Datei", "Rechnung", "Hilfe"}
    von_allen([anna, ben])        →  {"Rechnung"}
    von_irgendwem([anna, ben])    →  {"Datei", "Rechnung", "Hilfe", "Export"}

Grenzen: protokolle enthält 1 bis 100 Listen klicks. Jede hat 0 bis
1000 Einträge; ein Eintrag ist der nicht leere Name eines Menüpunkts.
Das Menü hat höchstens 200 Menüpunkte.

Hintergrund: Eine Menge (Typ set) enthält jedes Element höchstens
einmal und hat keine Reihenfolge. Man schreibt sie in geschweiften
Klammern wie {"Datei", "Hilfe"}; die leere Menge ist set(), denn {}
ist das leere Dictionary. set(liste) macht aus einer Liste eine Menge
und entfernt dabei die Duplikate. Mit in fragt man, ob ein Element
dazugehört, mit menge.add(x) fügt man eines hinzu. Zwei Mengen
verknüpft man mit Operatoren:

    a = {"Datei", "Rechnung", "Hilfe"}
    b = {"Rechnung", "Export"}
    a & b      →  {"Rechnung"}                               (Schnitt: in beiden)
    a | b      →  {"Datei", "Rechnung", "Hilfe", "Export"}   (Vereinigung: in mindestens einer)

Beide liefern eine neue Menge, a und b bleiben, wie sie waren. Zwei
Mengen sind gleich (==), wenn sie dieselben Elemente haben. Weil eine
Menge keine Reihenfolge hat, kann print sie bei jedem Programmstart
anders ordnen; sorted(menge) gibt die Elemente als sortierte Liste
zurück.
"""


def angeklickt(klicks):
    """Gibt die Menge der Menüpunkte in klicks zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def von_allen(protokolle):
    """Gibt die Menge der Menüpunkte zurück, die in jedem Protokoll vorkommen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def von_irgendwem(protokolle):
    """Gibt die Menge der Menüpunkte zurück, die in mindestens einem Protokoll vorkommen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


anna = ["Datei", "Rechnung", "Datei", "Hilfe"]
ben = ["Rechnung", "Export", "Rechnung"]
print(sorted(angeklickt(anna)))
print(sorted(von_allen([anna, ben])))
print(sorted(von_irgendwem([anna, ben])))
