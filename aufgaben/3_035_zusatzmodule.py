"""Aufgabe 3_035 – Zusatzmodule                                  Stufe 3 ★★★☆☆

Ein Betrieb führt eine neue Software für die Warenwirtschaft ein. Das
Grundpaket ist gesetzt, dazu gibt es Zusatzmodule mit jährlichen
Lizenzkosten, etwa „Mahnwesen“ für 900 Euro oder „Lager“ für 1500 Euro.
Bevor die Geschäftsführung entscheidet, soll jede mögliche Auswahl von
Zusatzmodulen einmal auf dem Tisch liegen, auch „gar keins“ und „alle“.
Danach interessieren nur die Auswahlen, die ins Jahresbudget passen.

- `kombinationen(module)` bekommt eine Liste von Modulnamen und liefert eine
  Liste aller Auswahlen. Jede Auswahl ist eine Liste von Namen in derselben
  Reihenfolge wie in module; jede Auswahl kommt genau einmal vor. In
  welcher Reihenfolge die Auswahlen selbst in der Ergebnisliste stehen, ist
  egal.
- `bezahlbare(module, preise, budget)` liefert nur die Auswahlen, deren
  Summe der Preise höchstens budget ist. preise ist ein Dictionary von
  Modulname auf Preis. Benutzen Sie dafür kombinationen.

    kombinationen(["Mahnwesen", "Lager"])
        →  [[], ["Lager"], ["Mahnwesen"], ["Mahnwesen", "Lager"]]
    preise = {"Mahnwesen": 900, "Lager": 1500, "Shop": 1200}
    bezahlbare(["Mahnwesen", "Lager", "Shop"], preise, 2200)
        →  [[], ["Shop"], ["Lager"], ["Mahnwesen"], ["Mahnwesen", "Shop"]]

Lösen Sie kombinationen rekursiv und ohne itertools.

Grenzen: 0 ≤ len(module) ≤ 15, die Namen sind verschiedene, nicht leere
Texte. Jedes Modul steht in preise mit einem ganzzahligen Preis von 1 bis
10**6; 0 ≤ budget ≤ 10**7. Bei n Modulen gibt es 2**n Auswahlen, bei 15
also 32 768.

Hintergrund: Backtracking („Zurückverfolgen“) baut eine Lösung Schritt für
Schritt auf und probiert an jeder Stelle alle Möglichkeiten durch. Für
Teilmengen gibt es bei jedem Modul genau zwei Möglichkeiten: Es kommt in
die Auswahl oder nicht. Eine rekursive Hilfsfunktion bekommt die Nummer des
Moduls, über das sie gerade entscheidet, und die bisherige Auswahl. Sind
alle Module entschieden (Abbruchbedingung), wird eine Kopie der Auswahl
gespeichert. Sonst probiert sie erst „ohne“, dann „mit“: Sie hängt das
Modul an, ruft sich für das nächste auf und nimmt es danach mit pop()
wieder heraus (pop() entfernt das letzte Element einer Liste). Dieses
Zurücknehmen ist das „Zurückverfolgen“: Die Auswahl ist danach wieder
so wie vorher, und der nächste Versuch beginnt sauber.

    def entscheide(nummer, auswahl):
        if nummer == len(module):
            ergebnis.append(auswahl[:])      # Kopie, auswahl ändert sich noch
            return
        entscheide(nummer + 1, auswahl)      # ohne module[nummer]
        auswahl.append(module[nummer])
        entscheide(nummer + 1, auswahl)      # mit module[nummer]
        auswahl.pop()                        # zurücknehmen

Rekursion selbst kennen Sie aus den Aufgaben 2_044 und 3_005. Eine
Funktion darf innerhalb einer anderen definiert werden (Aufgabe 3_032);
dann sieht sie deren Variablen wie module und ergebnis. Sie darf ergebnis
mit append verändern; eine neue Zuweisung ergebnis = … würde dagegen eine
eigene lokale Variable anlegen (Aufgabe 2_013).

Tipp: Ohne die Kopie auswahl[:] stünde am Ende 2**n-mal dieselbe, leere
Liste im Ergebnis, weil append nur einen Verweis auf die Liste speichert.
"""


def kombinationen(module):
    """Gibt alle Auswahlen aus module als Listen zurück, je in der Reihenfolge von module."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bezahlbare(module, preise, budget):
    """Gibt alle Auswahlen zurück, deren Preise zusammen höchstens budget sind."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(kombinationen(["Mahnwesen", "Lager"]))
