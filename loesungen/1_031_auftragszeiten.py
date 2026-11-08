# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_031_auftragszeiten.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_031_auftragszeiten

"""Aufgabe 1_031 – Auftragszeiten                                Stufe 1 ★☆☆☆☆

Ein Versandlager will seinen Ablauf verbessern. Dazu misst es bei
jedem Auftrag die Durchlaufzeit: wie viele Minuten vom Eingang der
Bestellung bis zum fertig gepackten Paket vergehen. Für die
Auswertung braucht die Prozessanalyse die kürzeste und die längste
Zeit, die Summe aller Zeiten und alle Zeiten der Größe nach sortiert.
Die Reihenfolge, in der gemessen wurde, soll dabei erhalten bleiben.
Der vorgegebene Code liest die Zeiten (durch Kommas getrennt) in die
Liste zeiten und gibt am Ende alles aus. Ergänzen Sie dazwischen vier
Zeilen, die kuerzeste, laengste, gesamt und sortiert mit min, max,
sum und sorted berechnen. Bei der Eingabe 12,7,30,7,18:

    Gemessen: [12, 7, 30, 7, 18]
    Sortiert: [7, 7, 12, 18, 30]
    Kürzeste: 7 min, längste: 30 min
    Gesamt: 74 min für 5 Aufträge

Grenzen: Es gibt 1 bis 30 Zeiten, jede ist eine ganze Zahl von 1 bis
1000. Dieselbe Zeit darf mehrmals vorkommen.

Hintergrund: Für Listen mit Zahlen gibt es fertige Funktionen. min(liste)
liefert das kleinste Element, max(liste) das größte und sum(liste) die
Summe aller Elemente. sorted(liste) liefert eine neue Liste mit
denselben Elementen in aufsteigender Reihenfolge; die ursprüngliche
Liste bleibt dabei, wie sie war. Bei werte = [4, 1, 3] ist min(werte)
gleich 1, max(werte) gleich 4, sum(werte) gleich 8 und sorted(werte)
gleich [1, 3, 4], während werte weiter [4, 1, 3] ist. min und max
brauchen mindestens ein Element; bei einer leeren Liste brechen sie mit
einem ValueError ab.
"""

eingabe = input("Durchlaufzeiten in Minuten, durch Kommas getrennt: ")
zeiten = []
for teil in eingabe.split(","):
    zeiten.append(int(teil))

kuerzeste = min(zeiten)
laengste = max(zeiten)
gesamt = sum(zeiten)
sortiert = sorted(zeiten)

print(f"Gemessen: {zeiten}")
print(f"Sortiert: {sortiert}")
print(f"Kürzeste: {kuerzeste} min, längste: {laengste} min")
print(f"Gesamt: {gesamt} min für {len(zeiten)} Aufträge")


# Idee: Jede der vier Größen ist genau ein Aufruf einer fertigen Funktion: min(zeiten), max(zeiten),
# sum(zeiten) und sorted(zeiten). sorted baut eine neue Liste, darum steht unter „Gemessen“ weiter die
# Reihenfolge der Messung.
# Anderer Weg: Man kann alles mit einer Schleife selbst ausrechnen, etwa gesamt = 0 und in der Schleife
# gesamt = gesamt + zeit. Das ist viel länger. Nach sortiert = sorted(zeiten) gilt außerdem
# kuerzeste = sortiert[0] und laengste = sortiert[-1].
# Typische Fehler: sortiert = zeiten.sort() (sort gibt None zurück und sortiert dazu noch zeiten selbst,
# dann stimmt „Gemessen“ nicht mehr), min und max vertauschen oder mit dem Text eingabe statt mit der
# Liste zeiten rechnen.
