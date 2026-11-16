"""Aufgabe 3_035 – Anschaffungen                                 Stufe 3 ★★★☆☆

Die IT-Abteilung eines Betriebs darf am Jahresende noch Geld aus ihrem
Budget ausgeben. Auf der Wunschliste stehen mehrere Anschaffungen mit
Preisen aus den Angeboten der Händler. Bevor die Abteilungsleitung
entscheidet, möchte sie alle Möglichkeiten sehen: jede Auswahl von
Anschaffungen, die zusammen ins Budget passt. Schreiben Sie zwei
Funktionen:

- `alle_auswahlen(posten)` bekommt eine Liste von Namen und gibt alle
  Auswahlen daraus zurück, also alle Teilmengen, als Liste von Listen.
  Dazu gehört auch die leere Auswahl []. Innerhalb einer Auswahl
  stehen die Namen in derselben Reihenfolge wie in posten; die
  Reihenfolge der Auswahlen untereinander ist egal.
- `im_budget(angebote, budget)` bekommt eine Liste von Tupeln
  (name, preis) und gibt alle Auswahlen der Namen zurück, deren
  Preise zusammen höchstens budget Euro ergeben, ebenso geordnet.

    alle_auswahlen(["Firewall", "Switch"])
        →  [[], ["Firewall"], ["Switch"], ["Firewall", "Switch"]]
           (in beliebiger Reihenfolge)
    angebote = [("Firewall", 1200), ("Switch", 800), ("Schulung", 600), ("USV", 450)]
    im_budget(angebote, 2000)
        →  12 Auswahlen, darunter [], ["Firewall", "Switch"] (genau 2000 Euro)
           und ["Switch", "Schulung", "USV"], aber nicht
           ["Firewall", "Schulung", "USV"] (2250 Euro)

Die beiden Hilfsfunktionen sammle und sammle_im_budget sind ein
Vorschlag für den Aufbau; Sie dürfen auch anders vorgehen.

Grenzen: alle_auswahlen bekommt 0 bis 15 verschiedene Namen.
im_budget bekommt 0 bis 20 Angebote mit verschiedenen Namen, jeder
Preis ist eine ganze Zahl von 1 bis 10**6 und das Budget eine ganze
Zahl von 0 bis 10**7; es gibt höchstens 10 000 passende Auswahlen.
Ihre Lösung für im_budget soll eine Auswahl nicht weiter ausbauen,
sobald das Budget überschritten wäre: Bei 20 Angeboten, die alle
teurer sind als das Budget, soll sie nicht erst über eine Million
Auswahlen bilden.

Hintergrund: Bei Backtracking baut man eine Lösung Schritt für Schritt
auf und probiert an jeder Stelle alle Möglichkeiten durch. Für
Teilmengen gibt es bei jedem Posten genau zwei: Er kommt in die
Auswahl, oder er kommt nicht hinein. Eine rekursive Funktion (Aufgabe
3_005) entscheidet über den Posten an der Stelle index und überlässt
den Rest einem Selbstaufruf mit index + 1. Ist index am Ende der Liste
angekommen, ist eine Auswahl fertig und wird als Kopie gespeichert:

    def sammle(posten, index, auswahl, ergebnisse):
        if index == len(posten):
            ergebnisse.append(auswahl[:])   # Kopie, auswahl ändert sich weiter
            return
        auswahl.append(posten[index])       # 1. Möglichkeit: mit
        sammle(posten, index + 1, auswahl, ergebnisse)
        auswahl.pop()                       # zurücknehmen
        sammle(posten, index + 1, auswahl, ergebnisse)   # 2. Möglichkeit: ohne

Das Zurücknehmen mit pop gibt dem Verfahren seinen Namen (englisch
backtrack: denselben Weg zurückgehen). Bei n Posten gibt es 2**n
Teilmengen, bei 20 schon über eine Million. Der Vorteil von
Backtracking zeigt sich, wenn eine Regel gilt: Passt ein Posten nicht
mehr ins restliche Budget, probiert man ihn gar nicht erst aus und
spart damit alle Auswahlen, die darauf aufbauen würden.
"""


def sammle(posten, index, auswahl, ergebnisse):
    """Hängt an ergebnisse alle Auswahlen an, die mit auswahl beginnen und über posten[index:] entscheiden."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def alle_auswahlen(posten):
    """Gibt alle Teilmengen von posten als Liste von Listen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def sammle_im_budget(angebote, index, auswahl, rest, ergebnisse):
    """Wie sammle, aber nur mit Angeboten, die noch in das restliche Budget rest passen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def im_budget(angebote, budget):
    """Gibt alle Auswahlen der Namen zurück, deren Preise zusammen höchstens budget sind."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


angebote = [("Firewall", 1200), ("Switch", 800), ("Schulung", 600), ("USV", 450)]
print(len(alle_auswahlen(["Firewall", "Switch", "Schulung", "USV"])))
print(len(im_budget(angebote, 2000)))
