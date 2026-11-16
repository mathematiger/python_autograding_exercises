# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_034_speicherbaum.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_034_speicherbaum

"""Aufgabe 3_034 – Speicherbaum                                  Stufe 3 ★★★☆☆

Auf einem Dateiserver im Rechenzentrum wird der Speicher knapp. Ein
Werkzeug liest die Ordner eines Laufwerks aus und liefert sie als
verschachtelte Liste: Eine Zahl ist eine Datei mit ihrer Größe in
Megabyte (MB), eine Liste ist ein Ordner mit seinem Inhalt, der
wieder Dateien und Unterordner enthalten kann.

    laufwerk = [120, [30, 5, [700, 2]], [], [[15]]]

Das Laufwerk enthält also eine Datei mit 120 MB, einen Ordner mit
zwei Dateien und einem Unterordner, einen leeren Ordner und einen
Ordner, in dem nur ein weiterer Ordner mit einer Datei liegt.
Schreiben Sie drei rekursive Funktionen:

- `belegung(ordner)`: die Summe aller Dateigrößen, auch in allen
  Unterordnern.
- `tiefe(ordner)`: wie tief die Ordner verschachtelt sind. Ein Ordner
  ohne Unterordner hat die Tiefe 1, auch wenn er leer ist; sonst ist
  die Tiefe 1 plus die größte Tiefe seiner Unterordner.
- `gespiegelt(ordner)`: eine neue Liste mit umgekehrter Reihenfolge,
  und zwar in jedem Ordner; die Dateien selbst bleiben, wie sie sind.
  Das Werkzeug zeigt so die zuletzt angelegten Einträge zuerst an.
  Die Liste ordner darf nicht verändert werden.

    belegung(laufwerk)     →  872
    tiefe(laufwerk)        →  3
    gespiegelt(laufwerk)   →  [[[15]], [], [[2, 700], 5, 30], 120]
    belegung([])           →  0
    tiefe([])              →  1

Grenzen: Es gibt höchstens 10 000 Einträge (Dateien und Ordner
zusammen), und die Ordner sind höchstens 100 Ebenen tief. Jede
Dateigröße ist eine ganze Zahl von 0 bis 10**6. Ihre Lösung soll jeden
Eintrag nur einmal ansehen, also O(n) Schritte bei n Einträgen
brauchen.

Hintergrund: Eine Funktion, die sich selbst aufruft, heißt rekursiv
(Aufgabe 3_005). Das passt immer dann, wenn eine Struktur Teile von
derselben Art enthält: Ein Ordner enthält Ordner. Jede rekursive
Funktion braucht einen Fall, der ohne Selbstaufruf auskommt (die
Abbruchbedingung, hier: eine Datei), und einen Fall, der das Problem
auf kleinere Teile derselben Art zurückführt (hier: die Unterordner).
Ob ein Eintrag ein Ordner ist, sagt isinstance(eintrag, list):

    def anzahl_dateien(ordner):
        anzahl = 0
        for eintrag in ordner:
            if isinstance(eintrag, list):
                anzahl = anzahl + anzahl_dateien(eintrag)
            else:
                anzahl = anzahl + 1
        return anzahl

Man muss dabei nicht verfolgen, was in den tieferen Aufrufen
passiert: Man verlässt sich darauf, dass anzahl_dateien(eintrag) für
den Unterordner das richtige Ergebnis liefert, und baut daraus das
Ergebnis für den ganzen Ordner. Python merkt sich jeden noch nicht
beendeten Aufruf; bei 100 Ebenen sind das 100 gleichzeitig, das geht
problemlos (die Grenze liegt bei etwa 1000).
"""


def belegung(ordner):
    """Gibt die Summe aller Dateigrößen in ordner und allen Unterordnern zurück."""
    gesamt = 0
    for eintrag in ordner:
        if isinstance(eintrag, list):
            gesamt = gesamt + belegung(eintrag)
        else:
            gesamt = gesamt + eintrag
    return gesamt


def tiefe(ordner):
    """Gibt zurück, wie viele Ebenen von Ordnern ineinander verschachtelt sind."""
    tiefste = 0
    for eintrag in ordner:
        if isinstance(eintrag, list):
            tiefste = max(tiefste, tiefe(eintrag))
    return 1 + tiefste


def gespiegelt(ordner):
    """Gibt eine neue Liste zurück, in der jeder Ordner rückwärts geordnet ist."""
    ergebnis = []
    for eintrag in reversed(ordner):
        if isinstance(eintrag, list):
            ergebnis.append(gespiegelt(eintrag))
        else:
            ergebnis.append(eintrag)
    return ergebnis


laufwerk = [120, [30, 5, [700, 2]], [], [[15]]]
print(belegung(laufwerk))
print(tiefe(laufwerk))
print(gespiegelt(laufwerk))


# Idee: Alle drei Funktionen gehen den Ordner einmal durch und unterscheiden mit isinstance(eintrag, list)
# zwei Fälle. Eine Datei wird direkt verarbeitet (Abbruchbedingung), ein Unterordner mit einem Selbstaufruf.
# belegung addiert die Teilergebnisse, tiefe nimmt das Maximum der Unterordner und zählt 1 für die eigene
# Ebene dazu, gespiegelt durchläuft den Ordner mit reversed und hängt für Unterordner deren Spiegelbild an.
#
# Anderer Weg: ohne Rekursion mit einem eigenen Stapel, wie die Vergleichslösung in den Tests: Man legt
# (Ordner, Ebene) auf eine Liste, nimmt immer den obersten herunter und legt seine Unterordner wieder drauf.
# Das ist länger, stößt aber auch bei sehr tiefen Ordnern nicht an Pythons Grenze von etwa 1000 Aufrufen.
#
# Typische Fehler: die Dateien in Unterordnern vergessen (nur die oberste Ebene addieren), bei tiefe die
# Tiefen der Unterordner addieren statt das Maximum zu nehmen, für einen leeren Ordner 0 statt 1 liefern,
# oder in gespiegelt ordner.reverse() aufrufen (verändert die Liste des Aufrufers).
#
# Laufzeit: O(n) bei n Einträgen, denn jeder Eintrag wird genau einmal in der Schleife seines Ordners angesehen
# und jeder Ordner genau einmal aufgerufen.
