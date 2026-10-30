"""Aufgabe 2_018 – Abfrageseiten                                 Stufe 2 ★★☆☆☆

Eine Datenbankabfrage liefert die Namen aller Kundinnen und Kunden als
Liste, oft mehrere Tausend. Die Weboberfläche zeigt davon immer nur eine
Seite mit wenigen Einträgen an; mit „Weiter“ blättert man zur nächsten.
Außerdem kann man einen Namen korrigieren. Bevor die Korrektur in der
Datenbank landet, zeigt die Oberfläche eine Vorschau der geänderten
Liste. Bricht man ab, muss die ursprüngliche Liste noch unverändert da
sein.

Schreiben Sie zwei Funktionen:

- `seite(ergebnisse, nummer, groesse)` gibt die Einträge der Seite nummer
  als neue Liste zurück, wenn jede Seite groesse Einträge hat. Seite 1
  sind die ersten groesse Einträge, Seite 2 die nächsten und so weiter.
  Die letzte Seite darf kürzer sein; eine Seite hinter dem Ende ist leer.
- `mit_korrektur(werte, index, neu)` gibt eine neue Liste zurück, in der
  an der Stelle index der Text neu steht. Die Liste werte selbst bleibt
  unverändert.

    namen = ["Abel", "Bauer", "Celik", "Dorn", "Ernst"]
    seite(namen, 1, 2)                →  ["Abel", "Bauer"]
    seite(namen, 3, 2)                →  ["Ernst"]
    seite(namen, 4, 2)                →  []
    mit_korrektur(namen, 2, "Çelik")  →  ["Abel", "Bauer", "Çelik", "Dorn", "Ernst"]
    namen                             →  ["Abel", "Bauer", "Celik", "Dorn", "Ernst"]

Grenzen: ergebnisse und werte sind Listen von Texten mit
0 ≤ len(ergebnisse) ≤ 100 000 und 1 ≤ len(werte) ≤ 100 000.
1 ≤ nummer ≤ 10**6, 1 ≤ groesse ≤ 1000, 0 ≤ index < len(werte), neu ist
ein Text.

Hintergrund: Mit liste[start:ende] schneidet man einen Teil einer Liste
heraus, genau wie bei Texten (Aufgabe 1_012): Er beginnt bei start und
endet vor ende. Reicht ende über das Listenende hinaus, ist das kein
Fehler; man bekommt einfach, was da ist, notfalls eine leere Liste. Das
Ergebnis ist immer eine neue Liste.

Anders die Zuweisung: kopie = liste legt keine neue Liste an, sondern gibt
derselben Liste einen zweiten Namen. Ändert man über einen der Namen ein
Element, sieht man die Änderung auch über den anderen:

    a = [1, 2, 3]
    b = a          # derselbe Gegenstand mit zwei Namen
    b[0] = 99
    a              →  [99, 2, 3]
    c = a[:]       # Slicing ohne Grenzen: eine neue Liste mit denselben Elementen
    c[1] = 0
    a              →  [99, 2, 3]

Ob zwei Namen dieselbe Liste meinen, prüft a is b. Auch eine Funktion
bekommt die Liste selbst, keine Kopie: Ändert sie werte[index], ist die
Liste des Aufrufers geändert.
"""


def seite(ergebnisse, nummer, groesse):
    """Gibt die Einträge der Seite nummer zurück, wenn jede Seite groesse Einträge hat."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def mit_korrektur(werte, index, neu):
    """Gibt eine Kopie von werte zurück, in der an der Stelle index der Text neu steht."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


namen = ["Abel", "Bauer", "Celik", "Dorn", "Ernst"]
print(seite(namen, 3, 2))
print(mit_korrektur(namen, 2, "Çelik"))
print(namen)
