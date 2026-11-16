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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def tiefe(ordner):
    """Gibt zurück, wie viele Ebenen von Ordnern ineinander verschachtelt sind."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gespiegelt(ordner):
    """Gibt eine neue Liste zurück, in der jeder Ordner rückwärts geordnet ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


laufwerk = [120, [30, 5, [700, 2]], [], [[15]]]
print(belegung(laufwerk))
print(tiefe(laufwerk))
print(gespiegelt(laufwerk))
