"""Aufgabe 4_021 – Prozesskennzahlen                            Stufe 4 ★★★★☆

Ein Versandhändler misst, wie lange jede Bestellung vom Eingang bis zum
Versand braucht (die Durchlaufzeit, in Minuten). Die Messwerte kommen
einzeln an, während der Tag läuft, und für jeden Prozess (Kommissionieren,
Verpacken, Retouren …) soll eine eigene laufende Auswertung mitgeführt
werden. Für ein Diagramm sollen die Zeiten außerdem auf den Bereich 0
bis 1 umgerechnet werden (normalisiert). Beides soll ohne Klasse und
ohne globale Variablen gehen, mit Funktionen, die sich ihren Zustand
selbst merken. Vervollständigen Sie zwei Funktionen:

- `normierer(kleinster, groesster)` gibt eine Funktion zurück, die einen
  Wert x auf (x - kleinster) / (groesster - kleinster) umrechnet. Ist
  groesster nicht größer als kleinster, löst normierer sofort einen
  ValueError aus, dessen Meldung beide Werte enthält.
- `auswertung()` gibt eine Funktion erfasse(minuten) zurück. Jeder
  Aufruf von erfasse nimmt einen Messwert auf und gibt das Tupel
  (anzahl, durchschnitt, laengste) aller bisher erfassten Werte zurück.
  Jeder Aufruf von auswertung() beginnt eine neue, unabhängige
  Auswertung.

    auf_eins = normierer(10, 50)
    auf_eins(30), auf_eins(10), auf_eins(60)   →  (0.5, 0.0, 1.25)
    normierer(5, 5)                            →  ValueError
    verpacken = auswertung()
    verpacken(12)                              →  (1, 12.0, 12)
    verpacken(20)                              →  (2, 16.0, 20)
    retouren = auswertung()
    retouren(45)                               →  (1, 45.0, 45)
    verpacken(4)                               →  (3, 12.0, 20)

Grenzen: kleinster, groesster und x sind ganze Zahlen oder Kommazahlen
von -10**6 bis 10**6. minuten ist eine ganze Zahl von 0 bis 10**6;
eine Auswertung erfasst bis zu 100 000 Werte, jeder Aufruf von erfasse
soll O(1) Schritte brauchen. Es dürfen beliebig viele Auswertungen
gleichzeitig laufen.

Hintergrund: Eine Funktion kann innerhalb einer anderen Funktion
definiert und von ihr zurückgegeben werden (Funktionen sind Werte). Die
innere Funktion sieht die lokalen Variablen der äußeren, auch dann
noch, wenn die äußere längst fertig ist. Python hebt diese Variablen
für sie auf; eine Funktion zusammen mit den aufgehobenen Variablen
heißt Closure (Abschluss):

    def multiplikator(faktor):
        def mal(x):
            return x * faktor
        return mal

    verdoppeln = multiplikator(2)
    verdreifachen = multiplikator(3)
    print(verdoppeln(5), verdreifachen(5))   # 10 15

Jeder Aufruf von multiplikator legt ein eigenes faktor an, darum
stören sich verdoppeln und verdreifachen nicht. Lesen geht ohne Weiteres.
Will die innere Funktion einer solchen Variablen aber einen neuen Wert
zuweisen, muss sie das mit nonlocal ankündigen. Sonst macht die
Zuweisung daraus eine neue lokale Variable der inneren Funktion, und
schon das Lesen davor scheitert mit UnboundLocalError:

    def zaehler():
        stand = 0
        def weiter():
            nonlocal stand
            stand = stand + 1
            return stand
        return weiter

    z = zaehler()
    print(z(), z(), z())                     # 1 2 3

nonlocal ist wie global (Aufgabe 2_013), nur für die Variablen der
umgebenden Funktion statt des Moduls. Ändert man ein Objekt nur, ohne
die Variable neu zuzuweisen (liste.append(x)), braucht man kein
nonlocal. Mit inspect.getclosurevars(z).nonlocals oder z.__closure__
kann man sich die aufgehobenen Variablen ansehen. Closures sind die
leichtgewichtige Alternative zu einer Klasse mit einer einzigen
Methode; Dekoratoren (nächste Aufgabe) sind genau so gebaut.
"""


def normierer(kleinster, groesster):
    """Gibt eine Funktion zurück, die Werte von [kleinster, groesster] auf [0, 1] umrechnet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auswertung():
    """Gibt eine Funktion erfasse(minuten) zurück, die (anzahl, durchschnitt, laengste) mitführt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


auf_eins = normierer(10, 50)
print(auf_eins(30), auf_eins(10), auf_eins(60))
verpacken = auswertung()
verpacken(12)
print(verpacken(20))
