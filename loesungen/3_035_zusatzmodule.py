# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_035_zusatzmodule.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_035_zusatzmodule

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
wieder heraus. Dieses Zurücknehmen ist das „Zurückverfolgen“: Die Auswahl
ist danach wieder so wie vorher, und der nächste Versuch beginnt sauber.

    def entscheide(nummer, auswahl):
        if nummer == len(module):
            ergebnis.append(auswahl[:])      # Kopie, auswahl ändert sich noch
            return
        entscheide(nummer + 1, auswahl)      # ohne module[nummer]
        auswahl.append(module[nummer])
        entscheide(nummer + 1, auswahl)      # mit module[nummer]
        auswahl.pop()                        # zurücknehmen

Rekursion selbst kennen Sie aus Aufgabe 3_005. Eine Funktion darf innerhalb
einer anderen definiert werden; dann sieht sie deren Variablen wie module
und ergebnis.

Tipp: Ohne die Kopie auswahl[:] stünde am Ende 2**n-mal dieselbe, leere
Liste im Ergebnis, weil append nur einen Verweis auf die Liste speichert.
"""


def kombinationen(module):
    """Gibt alle Auswahlen aus module als Listen zurück, je in der Reihenfolge von module."""
    ergebnis = []

    def entscheide(nummer, auswahl):
        """Entscheidet über module[nummer] und alle folgenden Module."""
        if nummer == len(module):
            ergebnis.append(auswahl[:])
            return
        entscheide(nummer + 1, auswahl)
        auswahl.append(module[nummer])
        entscheide(nummer + 1, auswahl)
        auswahl.pop()

    entscheide(0, [])
    return ergebnis


def bezahlbare(module, preise, budget):
    """Gibt alle Auswahlen zurück, deren Preise zusammen höchstens budget sind."""
    passende = []
    for auswahl in kombinationen(module):
        kosten = 0
        for modul in auswahl:
            kosten = kosten + preise[modul]
        if kosten <= budget:
            passende.append(auswahl)
    return passende


print(kombinationen(["Mahnwesen", "Lager"]))


# Idee: Eine innere Hilfsfunktion entscheidet Modul für Modul: erst ohne das Modul
# weitermachen, dann mit ihm (anhängen, rekursiv weiter, mit pop() zurücknehmen). Sind
# alle Module entschieden, wird eine Kopie der Auswahl gespeichert. bezahlbare geht alle
# Auswahlen aus kombinationen durch und behält die, deren Preissumme höchstens budget ist.
# Anderer Weg: rekursiv ohne Hilfsfunktion: Die Auswahlen von module[1:] berechnen und
# jede einmal ohne und einmal mit module[0] vorn übernehmen; Abbruchbedingung: für []
# gibt es nur [[]]. Ohne Rekursion: Die Zahlen 0 bis 2**n - 1 durchgehen, Bit Nummer i
# sagt, ob module[i] dabei ist.
# Typische Fehler: auswahl statt auswahl[:] speichern (am Ende lauter gleiche, leere
# Listen); pop() vergessen (die Auswahl wächst immer weiter); die leere Auswahl vergessen;
# bei bezahlbare kosten < budget statt kosten <= budget.
# Laufzeit: Es gibt 2**n Auswahlen mit bis zu n Namen, also O(n · 2**n) für beide
# Funktionen. Schneller geht es nicht, weil das Ergebnis selbst so groß ist; bei 15
# Modulen sind das 32 768 Auswahlen, bei 30 schon über eine Milliarde.
